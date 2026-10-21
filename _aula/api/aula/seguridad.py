"""api/aula/seguridad.py — contraseñas con Argon2id, acceso por JWT corto, renovación rotativa y límite de intentos.

Sin cookies: el sitio (otro dominio, `*.netlify.app`) manda `Authorization: Bearer <acceso>`. El acceso dura
`AULA_MINUTOS_ACCESO`; la renovación es un secreto opaco del que la base guarda solo el resumen SHA-256, rota en
cada uso y, si alguien presenta uno ya rotado (señal de robo), se revocan todas las sesiones de esa cuenta.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
import time
from collections import defaultdict, deque
from datetime import timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from aula import tiempo
from aula.config import config
from aula.db import obtener_sesion
from aula.modelos import SesionRenovacion, Usuario

log = logging.getLogger("aula.seguridad")

_hasher = PasswordHasher()  # Argon2id con los parámetros recomendados por argon2-cffi (RFC 9106, perfil bajo en memoria)
_bearer = HTTPBearer(auto_error=False)
_secreto_efimero = secrets.token_urlsafe(48)

LARGO_MINIMO_CLAVE = 8
_CLAVES_PROHIBIDAS = {"12345678", "123456789", "1234567890", "password", "contrasena", "contraseña", "qwertyui", "abcd1234"}


# --- contraseñas ------------------------------------------------------------------------------------------------

def validar_clave(clave: str, correo: str = "") -> None:
    if len(clave) < LARGO_MINIMO_CLAVE:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"La contraseña debe tener al menos {LARGO_MINIMO_CLAVE} caracteres.")
    if clave.lower() in _CLAVES_PROHIBIDAS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Esa contraseña es de las primeras que alguien probaría. Elige otra.")
    if correo and clave.lower() == correo.lower():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "La contraseña no puede ser tu correo.")


def hashear_clave(clave: str) -> str:
    return _hasher.hash(clave)


def verificar_clave(clave: str, guardado: str) -> bool:
    try:
        return _hasher.verify(guardado, clave)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def necesita_rehash(guardado: str) -> bool:
    try:
        return _hasher.check_needs_rehash(guardado)
    except InvalidHashError:
        return True


# Hash de referencia para gastar el mismo tiempo cuando el correo no existe (no revela qué correos hay).
_HASH_SEÑUELO = _hasher.hash(secrets.token_urlsafe(16))


def gastar_tiempo_verificacion(clave: str) -> None:
    verificar_clave(clave, _HASH_SEÑUELO)


# --- tokens -----------------------------------------------------------------------------------------------------

def _secreto() -> str:
    if config.jwt_secreto:
        return config.jwt_secreto
    # Sin AULA_JWT_SECRETO (desarrollo, pruebas): un secreto por proceso; las sesiones mueren al reiniciar.
    return _secreto_efimero


def crear_acceso(usuario: Usuario) -> tuple[str, int]:
    ahora = tiempo.ahora()
    segundos = config.minutos_acceso * 60
    carga = {
        "sub": str(usuario.id),
        "rol": usuario.rol_global,
        "tipo": "acceso",
        "iat": int(ahora.timestamp()),
        "exp": int((ahora + timedelta(seconds=segundos)).timestamp()),
    }
    return jwt.encode(carga, _secreto(), algorithm="HS256"), segundos


def _resumen(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def crear_renovacion(sesion: AsyncSession, usuario: Usuario) -> str:
    token = secrets.token_urlsafe(32)
    sesion.add(SesionRenovacion(
        usuario_id=usuario.id,
        resumen=_resumen(token),
        expira_en=tiempo.ahora() + timedelta(days=config.dias_renovacion),
    ))
    return token


async def emitir_par(sesion: AsyncSession, usuario: Usuario) -> dict:
    acceso, segundos = crear_acceso(usuario)
    renovacion = await crear_renovacion(sesion, usuario)
    return {"acceso": acceso, "renovacion": renovacion, "tipo": "bearer", "expira_en_s": segundos}


async def rotar_renovacion(sesion: AsyncSession, token: str) -> Usuario:
    """Valida un token de renovación y lo revoca; devuelve su usuario. Un token ya revocado revoca todos."""
    invalido = HTTPException(status.HTTP_401_UNAUTHORIZED, "La sesión venció. Vuelve a iniciar sesión.")
    fila = (await sesion.execute(select(SesionRenovacion).where(SesionRenovacion.resumen == _resumen(token)))).scalar_one_or_none()
    if fila is None:
        raise invalido
    ahora = tiempo.ahora()
    if fila.revocado_en is not None:
        log.warning("renovación reutilizada para el usuario %s: se revocan todas sus sesiones", fila.usuario_id)
        await revocar_todas(sesion, fila.usuario_id)
        await sesion.commit()
        raise invalido
    if fila.expira_en <= ahora:
        raise invalido
    fila.revocado_en = ahora
    usuario = await sesion.get(Usuario, fila.usuario_id)
    if usuario is None or not usuario.activo:
        raise invalido
    return usuario


async def revocar(sesion: AsyncSession, token: str) -> None:
    fila = (await sesion.execute(select(SesionRenovacion).where(SesionRenovacion.resumen == _resumen(token)))).scalar_one_or_none()
    if fila is not None and fila.revocado_en is None:
        fila.revocado_en = tiempo.ahora()


async def revocar_todas(sesion: AsyncSession, usuario_id: int) -> None:
    await sesion.execute(
        update(SesionRenovacion)
        .where(SesionRenovacion.usuario_id == usuario_id, SesionRenovacion.revocado_en.is_(None))
        .values(revocado_en=tiempo.ahora())
    )


# --- dependencia: usuario autenticado ---------------------------------------------------------------------------

async def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer),
    sesion: AsyncSession = Depends(obtener_sesion),
) -> Usuario:
    no_autorizado = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Sesión inválida o vencida.", headers={"WWW-Authenticate": "Bearer"}
    )
    if credenciales is None:
        raise no_autorizado
    try:
        carga = jwt.decode(credenciales.credentials, _secreto(), algorithms=["HS256"], options={"require": ["exp", "sub"]})
    except jwt.InvalidTokenError:
        raise no_autorizado
    if carga.get("tipo") != "acceso":
        raise no_autorizado
    usuario = await sesion.get(Usuario, int(carga["sub"]))
    if usuario is None or not usuario.activo:
        raise no_autorizado
    return usuario


# --- límite de intentos ------------------------------------------------------------------------------------------

class Limitador:
    """Ventana deslizante en memoria: `limite` eventos por `segundos` y clave. Un solo proceso (uvicorn sin
    workers), que es como corre el aula en la laptop; con varios procesos haría falta guardarlo en la base."""

    def __init__(self, limite: int, segundos: int):
        self.limite = limite
        self.segundos = segundos
        self._eventos: dict[str, deque] = defaultdict(deque)

    def _purgar(self, clave: str, ahora: float) -> deque:
        cola = self._eventos[clave]
        while cola and cola[0] <= ahora - self.segundos:
            cola.popleft()
        return cola

    def bloqueado(self, clave: str) -> int:
        """Segundos que faltan para poder intentar de nuevo (0 = libre)."""
        ahora = time.monotonic()
        cola = self._purgar(clave, ahora)
        if len(cola) >= self.limite:
            return max(1, int(cola[0] + self.segundos - ahora))
        return 0

    def anotar(self, clave: str) -> None:
        self._eventos[clave].append(time.monotonic())

    def limpiar(self, clave: str | None = None) -> None:
        if clave is None:
            self._eventos.clear()
        else:
            self._eventos.pop(clave, None)


limitador_sesion = Limitador(config.intentos_sesion, config.minutos_ventana_sesion * 60)
limitador_registro = Limitador(config.registros_por_hora, 3600)
