"""api/aula/tiempo.py — el reloj de la API (UTC) y el tipo de columna que lo guarda igual en PostgreSQL y SQLite.

Todo el código llama `tiempo.ahora()` (no `datetime.now`), para que las pruebas puedan adelantar el reloj y
comprobar vencimientos sin esperar.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


def ahora() -> datetime:
    return datetime.now(timezone.utc)


class FechaUTC(TypeDecorator):
    """Instante con zona: entra en UTC y sale con zona aunque el motor (SQLite) no la guarde."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, valor, dialecto):
        if valor is None:
            return None
        if valor.tzinfo is None:
            valor = valor.replace(tzinfo=timezone.utc)
        valor = valor.astimezone(timezone.utc)
        return valor.replace(tzinfo=None) if dialecto.name == "sqlite" else valor

    def process_result_value(self, valor, dialecto):
        if valor is None:
            return None
        if valor.tzinfo is None:
            return valor.replace(tzinfo=timezone.utc)
        return valor.astimezone(timezone.utc)
