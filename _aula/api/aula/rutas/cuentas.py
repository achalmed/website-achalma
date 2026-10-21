"""api/aula/rutas/cuentas.py — registro con consentimiento, sesión, renovación, perfil, y los derechos sobre los datos
propios (exportarlos y borrarlos; Ley 29733, docs/privacidad.md).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from aula import archivos, esquemas, permisos, seguridad, tiempo
from aula.config import config
from aula.db import obtener_sesion
from aula.modelos import (
    Anuncio, Calificacion, Clase, Entrega, Inscripcion, Intento, Progreso, SesionRenovacion, Tarea, Usuario,
)

rutas = APIRouter(prefix="/cuentas", tags=["cuentas"])


def _ip(request: Request) -> str:
    return request.client.host if request.client else "desconocida"


@rutas.post("/registro", response_model=esquemas.SesionSalida, status_code=201)
async def registrar(datos: esquemas.Registro, request: Request, sesion: AsyncSession = Depends(obtener_sesion)):
    if not config.permitir_registro:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "El registro está cerrado.")
    clave_ip = f"registro:{_ip(request)}"
    if espera := seguridad.limitador_registro.bloqueado(clave_ip):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Demasiados registros desde esta conexión.", headers={"Retry-After": str(espera)})
    if not datos.consentimiento:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Para crear la cuenta debes aceptar la política de privacidad.")
    if not datos.tengo_14_o_mas:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Si tienes menos de 14 años, tu madre, padre o tutor debe pedir tu cuenta al docente y aceptar la política por ti.")
    if datos.politica_version != config.politica_version:
        raise HTTPException(status.HTTP_409_CONFLICT, f"La política de privacidad vigente es la del {config.politica_version}; léela y acéptala de nuevo.")
    seguridad.validar_clave(datos.clave, datos.correo)
    existe = (await sesion.execute(select(Usuario.id).where(Usuario.correo == datos.correo))).first()
    if existe:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya hay una cuenta con ese correo. Inicia sesión.")
    ahora = tiempo.ahora()
    usuario = Usuario(
        correo=datos.correo,
        nombre_visible=datos.nombre_visible,
        clave_hash=seguridad.hashear_clave(datos.clave),
        rol_global="estudiante",
        consentimiento_version=datos.politica_version,
        consentimiento_en=ahora,
        ultimo_acceso_en=ahora,
    )
    sesion.add(usuario)
    await sesion.flush()
    par = await seguridad.emitir_par(sesion, usuario)
    await sesion.commit()
    seguridad.limitador_registro.anotar(clave_ip)
    return {**par, "usuario": usuario}


@rutas.post("/sesion", response_model=esquemas.SesionSalida)
async def iniciar_sesion(datos: esquemas.InicioSesion, sesion: AsyncSession = Depends(obtener_sesion)):
    clave_lim = f"sesion:{datos.correo}"
    if espera := seguridad.limitador_sesion.bloqueado(clave_lim):
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "Demasiados intentos fallidos. Espera unos minutos.",
            headers={"Retry-After": str(espera)},
        )
    usuario = (await sesion.execute(select(Usuario).where(Usuario.correo == datos.correo))).scalar_one_or_none()
    if usuario is None:
        seguridad.gastar_tiempo_verificacion(datos.clave)
    if usuario is None or not usuario.activo or not seguridad.verificar_clave(datos.clave, usuario.clave_hash):
        seguridad.limitador_sesion.anotar(clave_lim)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos.")
    if seguridad.necesita_rehash(usuario.clave_hash):
        usuario.clave_hash = seguridad.hashear_clave(datos.clave)
    usuario.ultimo_acceso_en = tiempo.ahora()
    par = await seguridad.emitir_par(sesion, usuario)
    await sesion.commit()
    seguridad.limitador_sesion.limpiar(clave_lim)
    return {**par, "usuario": usuario}


@rutas.post("/renovar", response_model=esquemas.Tokens)
async def renovar(datos: esquemas.Renovar, sesion: AsyncSession = Depends(obtener_sesion)):
    usuario = await seguridad.rotar_renovacion(sesion, datos.renovacion)
    usuario.ultimo_acceso_en = tiempo.ahora()
    par = await seguridad.emitir_par(sesion, usuario)
    await sesion.commit()
    return par


@rutas.post("/salir", status_code=204)
async def salir(datos: esquemas.Renovar, sesion: AsyncSession = Depends(obtener_sesion)):
    await seguridad.revocar(sesion, datos.renovacion)
    await sesion.commit()
    return Response(status_code=204)


@rutas.get("/yo", response_model=esquemas.UsuarioSalida)
async def yo(usuario: Usuario = Depends(seguridad.usuario_actual)):
    return usuario


@rutas.patch("/yo", response_model=esquemas.UsuarioSalida)
async def cambiar(
    datos: esquemas.CambioCuenta,
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    if datos.nombre_visible is not None:
        usuario.nombre_visible = " ".join(datos.nombre_visible.split())
    if datos.clave_nueva is not None:
        if not datos.clave_actual or not seguridad.verificar_clave(datos.clave_actual, usuario.clave_hash):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "La contraseña actual no es correcta.")
        seguridad.validar_clave(datos.clave_nueva, usuario.correo)
        usuario.clave_hash = seguridad.hashear_clave(datos.clave_nueva)
        await seguridad.revocar_todas(sesion, usuario.id)  # cierra las demás sesiones
    await sesion.commit()
    return usuario


# --- derechos ARCO: acceso (exportar) y cancelación (borrar) ------------------------------------------------------

def _iso(fecha):
    return fecha.isoformat() if fecha else None


def _progreso_por_pub(filas) -> dict:
    salida: dict[str, dict[str, str]] = {}
    for p in filas:
        salida.setdefault(p.pub, {})[p.leccion] = p.completada_el
    return salida


@rutas.get("/yo/datos")
async def exportar(usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    """Todo lo que el aula guarda de la persona, en JSON (los archivos se descargan por su enlace)."""
    inscripciones = (
        await sesion.execute(
            select(Inscripcion, Clase).join(Clase, Clase.id == Inscripcion.clase_id).where(Inscripcion.usuario_id == usuario.id)
        )
    ).all()
    entregas = (
        await sesion.execute(
            select(Entrega, Tarea, Calificacion)
            .join(Tarea, Tarea.id == Entrega.tarea_id)
            .outerjoin(Calificacion, Calificacion.entrega_id == Entrega.id)
            .where(Entrega.estudiante_id == usuario.id)
        )
    ).all()
    intentos = (await sesion.execute(select(Intento).where(Intento.estudiante_id == usuario.id))).scalars().all()
    progreso = (await sesion.execute(select(Progreso).where(Progreso.usuario_id == usuario.id))).scalars().all()
    anuncios = (await sesion.execute(select(Anuncio).where(Anuncio.autor_id == usuario.id))).scalars().all()
    sesiones = (await sesion.execute(select(SesionRenovacion).where(SesionRenovacion.usuario_id == usuario.id))).scalars().all()
    return {
        "exportado_en": tiempo.ahora().isoformat(),
        "politica_version": config.politica_version,
        "cuenta": {
            "id": usuario.id, "correo": usuario.correo, "nombre_visible": usuario.nombre_visible,
            "rol_global": usuario.rol_global, "creado_en": _iso(usuario.creado_en),
            "ultimo_acceso_en": _iso(usuario.ultimo_acceso_en),
            "consentimiento": {"version": usuario.consentimiento_version, "en": _iso(usuario.consentimiento_en)},
        },
        "clases": [
            {"clase_id": c.id, "nombre": c.nombre, "curso_id": c.curso_id, "pub": c.pub, "rol": i.rol, "desde": _iso(i.creado_en)}
            for i, c in inscripciones
        ],
        "entregas": [
            {
                "entrega_id": e.id, "tarea_id": t.id, "tarea": t.titulo, "texto": e.texto,
                "archivo": ({"nombre": e.archivo_nombre, "bytes": e.archivo_bytes, "descarga": f"/entregas/{e.id}/archivo"} if e.archivo_ruta else None),
                "entregado_en": _iso(e.entregado_en), "tardia": e.tardia,
                "calificacion": ({"puntaje": c.puntaje, "comentario": c.comentario, "por_criterio": c.por_criterio, "en": _iso(c.calificado_en)} if c else None),
            }
            for e, t, c in entregas
        ],
        "intentos": [
            {"intento_id": x.id, "examen_id": x.examen_id, "numero": x.numero, "estado": x.estado,
             "iniciado_en": _iso(x.iniciado_en), "entregado_en": _iso(x.entregado_en),
             "respuestas": x.respuestas, "puntaje": x.puntaje, "puntaje_max": x.puntaje_max}
            for x in intentos
        ],
        "progreso": _progreso_por_pub(progreso),
        "anuncios_publicados": [{"id": a.id, "clase_id": a.clase_id, "texto": a.texto, "creado_en": _iso(a.creado_en)} for a in anuncios],
        "sesiones": [{"creada_en": _iso(s.creado_en), "expira_en": _iso(s.expira_en), "revocada_en": _iso(s.revocado_en)} for s in sesiones],
    }


async def borrar_clase(sesion: AsyncSession, clase_id: int) -> None:
    """Borra una clase con todo lo suyo, incluidos los archivos de sus entregas."""
    rutas_archivos = (
        await sesion.execute(
            select(Entrega.archivo_ruta).join(Tarea, Tarea.id == Entrega.tarea_id).where(Tarea.clase_id == clase_id)
        )
    ).scalars().all()
    clase = await sesion.get(Clase, clase_id)
    if clase is not None:
        await sesion.delete(clase)
    for r in rutas_archivos:
        archivos.borrar(r)


async def borrar_datos_de(sesion: AsyncSession, usuario: Usuario) -> list[str]:
    """Borra la cuenta y todos sus datos (sin confirmar la transacción); devuelve los archivos a borrar después
    del commit. Si es el único docente de una clase con otros miembros, 409: borrarla se llevaría datos ajenos."""
    mis_clases_docente = (
        await sesion.execute(select(Inscripcion.clase_id).where(Inscripcion.usuario_id == usuario.id, Inscripcion.rol == "docente"))
    ).scalars().all()
    huerfanas = []
    for clase_id in mis_clases_docente:
        if await permisos.cuantos_docentes(sesion, clase_id) == 1:
            otros = (
                await sesion.execute(select(Inscripcion.id).where(Inscripcion.clase_id == clase_id, Inscripcion.usuario_id != usuario.id))
            ).first()
            if otros:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    f"Eres el único docente de la clase {clase_id}, que tiene estudiantes: suma otro docente o retíralos antes de borrar tu cuenta.",
                )
            huerfanas.append(clase_id)
    for clase_id in huerfanas:
        await borrar_clase(sesion, clase_id)
    rutas_archivos = list((await sesion.execute(select(Entrega.archivo_ruta).where(Entrega.estudiante_id == usuario.id))).scalars().all())
    # Lo que la persona dejó en clases ajenas como docente queda, sin su nombre.
    await sesion.execute(update(Anuncio).where(Anuncio.autor_id == usuario.id).values(autor_id=None))
    await sesion.execute(update(Calificacion).where(Calificacion.calificado_por == usuario.id).values(calificado_por=None))
    entregas_ids = select(Entrega.id).where(Entrega.estudiante_id == usuario.id)
    await sesion.execute(delete(Calificacion).where(Calificacion.entrega_id.in_(entregas_ids)))
    for modelo, campo in (
        (Entrega, Entrega.estudiante_id), (Intento, Intento.estudiante_id), (Progreso, Progreso.usuario_id),
        (Inscripcion, Inscripcion.usuario_id), (SesionRenovacion, SesionRenovacion.usuario_id),
    ):
        await sesion.execute(delete(modelo).where(campo == usuario.id))
    await sesion.execute(delete(Usuario).where(Usuario.id == usuario.id))
    return [r for r in rutas_archivos if r]


@rutas.delete("/yo", status_code=204)
async def borrar_cuenta(
    datos: esquemas.Baja,
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    """Borra la cuenta y todos sus datos (derecho de cancelación), previa contraseña."""
    if not seguridad.verificar_clave(datos.clave, usuario.clave_hash):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "La contraseña no es correcta.")
    rutas_archivos = await borrar_datos_de(sesion, usuario)
    await sesion.commit()
    for r in rutas_archivos:
        archivos.borrar(r)
    return Response(status_code=204)
