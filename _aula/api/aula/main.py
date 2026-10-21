"""api/aula/main.py — la API del aula con cuenta: arma la aplicación FastAPI, CORS por lista blanca y las rutas.

Arranque: `uvicorn aula.main:app` (lo hace `iniciar.sh`). Al arrancar comprueba que AULA_DATOS_DIR esté fuera de
todo repo y crea las tablas que falten (decisiones §1.10).
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from aula import archivos, db, origenes
from aula.config import config
from aula.rutas import anuncios, clases, cuentas, examenes, progreso, tareas

log = logging.getLogger("aula")
VERSION = "0.1.0"
# Margen sobre el archivo para los demás campos del formulario multipart.
_MARGEN_CUERPO = 256 * 1024


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    archivos.raiz_datos()  # falla si AULA_DATOS_DIR cae dentro de un repo
    if config.crear_tablas:
        await db.crear_tablas()
    if not config.jwt_secreto:
        log.warning("AULA_JWT_SECRETO no está definido: se usa un secreto efímero y las sesiones caen al reiniciar.")
    yield
    await db.motor().dispose()


def crear_app() -> FastAPI:
    app = FastAPI(
        title="Aula — API",
        version=VERSION,
        description="Cuentas, clases, anuncios, tareas, exámenes calificados y progreso para los 12 sitios.",
        lifespan=ciclo_de_vida,
    )
    exactos, regex = origenes.lista_blanca(config.cors_local, config.origenes_extra)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=exactos,
        allow_origin_regex=regex,
        allow_credentials=False,  # sin cookies: el token va en Authorization
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["Retry-After", "Content-Disposition"],
        max_age=600,
    )

    @app.middleware("http")
    async def limites_y_cabeceras(request: Request, siguiente):
        largo = request.headers.get("content-length")
        if largo and largo.isdigit() and int(largo) > config.max_archivo_bytes + _MARGEN_CUERPO:
            return JSONResponse(
                {"detail": f"La petición pasa del límite de {config.max_archivo_mb} MB."}, status_code=413
            )
        respuesta = await siguiente(request)
        respuesta.headers.setdefault("X-Content-Type-Options", "nosniff")
        respuesta.headers.setdefault("Referrer-Policy", "no-referrer")
        respuesta.headers.setdefault("Cache-Control", "no-store")
        return respuesta

    @app.get("/salud", tags=["sistema"])
    async def salud():
        return {"estado": "ok", "version": VERSION}

    @app.get("/privacidad", tags=["sistema"])
    async def privacidad():
        """Lo que la vitrina muestra antes del registro; el texto completo está en api/docs/privacidad.md."""
        return {
            "version": config.politica_version,
            "ley": "Ley 29733, de Protección de Datos Personales, y su reglamento vigente",
            "datos": ["correo", "nombre visible", "contraseña (solo su resumen Argon2id)", "clases e inscripciones",
                      "entregas, archivos y calificaciones", "intentos de examen y su nota", "lecciones completadas"],
            "finalidad": "dar el servicio educativo del aula: clases, tareas, exámenes, notas y progreso",
            "conservacion_dias_sin_actividad": config.dias_inactividad,
            "derechos": "descargar todos tus datos o borrar tu cuenta con todo lo tuyo cuando quieras, desde «Mi aula»",
            "contacto": config.contacto,
            "edad_minima": 14,
            "menores": "desde los 14 años aceptas tú; si tienes menos, tu madre, padre o tutor pide la cuenta al docente",
            "max_archivo_mb": config.max_archivo_mb,
        }

    for modulo in (cuentas, clases, anuncios, tareas, examenes, progreso):
        app.include_router(modulo.rutas)
    return app


app = crear_app()
