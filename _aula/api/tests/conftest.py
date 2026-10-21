"""api/tests/conftest.py — base, carpeta de datos y cliente de cada prueba.

Por omisión las pruebas corren sobre SQLite en memoria (rápidas, sin Docker). Con
`AULA_PRUEBAS_DATABASE_URL=postgresql+asyncpg://…/aula_prueba` corren las mismas sobre el PostgreSQL 16 del compose
(la base se crea si falta). Cada prueba empieza con tablas vacías y una carpeta de datos temporal fuera del repo.
"""

from __future__ import annotations

import os

import httpx
import pytest

from aula import db, seguridad
from aula.config import config
from aula.main import crear_app
from aula.modelos import Base, Usuario

URL_PRUEBAS = os.environ.get("AULA_PRUEBAS_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
CLAVE = "clave-larga-de-prueba"


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def _crear_base_si_falta(url: str) -> None:
    if not url.startswith("postgresql"):
        return
    import asyncpg

    base, _, nombre = url.replace("postgresql+asyncpg://", "postgresql://").rpartition("/")
    conexion = await asyncpg.connect(f"{base}/postgres")
    try:
        if not await conexion.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", nombre):
            await conexion.execute(f'CREATE DATABASE "{nombre}"')
    finally:
        await conexion.close()


@pytest.fixture
async def base(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "datos_dir", str(tmp_path / "datos-aula"))
    seguridad.limitador_sesion.limpiar()
    seguridad.limitador_registro.limpiar()
    await _crear_base_si_falta(URL_PRUEBAS)
    motor = db.iniciar_motor(URL_PRUEBAS)
    async with motor.begin() as conexion:
        await conexion.run_sync(Base.metadata.drop_all)
        await conexion.run_sync(Base.metadata.create_all)
    yield motor
    async with motor.begin() as conexion:
        await conexion.run_sync(Base.metadata.drop_all)
    await motor.dispose()


@pytest.fixture
async def cliente(base):
    app = crear_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://aula.prueba") as c:
        yield c


# --- ayudas ---------------------------------------------------------------------------------------------------------

async def registrar(cliente, correo: str, nombre: str = "Persona Ficticia", clave: str = CLAVE) -> dict:
    r = await cliente.post("/cuentas/registro", json={
        "correo": correo, "nombre_visible": nombre, "clave": clave,
        "consentimiento": True, "tengo_14_o_mas": True, "politica_version": config.politica_version,
    })
    assert r.status_code == 201, r.text
    datos = r.json()
    return {"id": datos["usuario"]["id"], "h": {"Authorization": f"Bearer {datos['acceso']}"}, "renovacion": datos["renovacion"], "correo": correo}


async def hacer_docente(usuario_id: int) -> None:
    async with db.fabrica()() as sesion:
        u = await sesion.get(Usuario, usuario_id)
        u.rol_global = "docente"
        await sesion.commit()


@pytest.fixture
async def aula(cliente):
    """Una clase con su docente y dos estudiantes (todos ficticios)."""
    docente = await registrar(cliente, "docente@ejemplo.test", "Docente Ficticia")
    await hacer_docente(docente["id"])
    r = await cliente.post("/clases", headers=docente["h"], json={"nombre": "Clase de prueba", "curso_id": "metodologia-investigacion", "pub": "methodica"})
    assert r.status_code == 201, r.text
    clase = r.json()
    ana = await registrar(cliente, "ana@ejemplo.test", "Ana Prueba")
    beto = await registrar(cliente, "beto@ejemplo.test", "Beto Ensayo")
    for e in (ana, beto):
        r = await cliente.post("/clases/inscribirse", headers=e["h"], json={"codigo": clase["codigo"]})
        assert r.status_code == 200, r.text
    return {"clase": clase, "docente": docente, "ana": ana, "beto": beto}
