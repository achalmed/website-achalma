"""api/aula/db.py — motor asíncrono de SQLAlchemy y una sesión por petición.

El motor se crea al primer uso con `config.database_url`; las pruebas lo cambian con `iniciar_motor(url)`
(SQLite en memoria o la base `aula_prueba` del compose). En SQLite se activan las claves foráneas, que ese motor
trae apagadas, para que las dos bases se comporten igual.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from aula.config import config

_estado: dict = {"motor": None, "fabrica": None}


def iniciar_motor(url: str | None = None) -> AsyncEngine:
    """Crea (o recrea) el motor y la fábrica de sesiones."""
    url = url or config.database_url
    opciones: dict = {}
    if url.startswith("sqlite"):
        opciones = {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
    else:
        opciones = {"pool_pre_ping": True, "pool_size": 5, "max_overflow": 5}
    motor = create_async_engine(url, **opciones)
    if url.startswith("sqlite"):
        @event.listens_for(motor.sync_engine, "connect")
        def _claves_foraneas(conexion, _registro):  # pragma: no cover - trivial
            cursor = conexion.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    _estado["motor"] = motor
    _estado["fabrica"] = async_sessionmaker(motor, expire_on_commit=False)
    return motor


def motor() -> AsyncEngine:
    if _estado["motor"] is None:
        iniciar_motor()
    return _estado["motor"]


def fabrica() -> async_sessionmaker[AsyncSession]:
    if _estado["fabrica"] is None:
        iniciar_motor()
    return _estado["fabrica"]


async def obtener_sesion() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia de FastAPI: una sesión por petición, siempre cerrada."""
    async with fabrica()() as sesion:
        yield sesion


async def crear_tablas() -> None:
    from aula.modelos import Base

    async with motor().begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)
