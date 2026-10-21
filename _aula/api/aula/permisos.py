"""api/aula/permisos.py — quién puede qué en una clase: el docente crea, edita y califica; el estudiante ve lo suyo.

Regla de privacidad: a quien no es miembro de una clase se le responde 404 (no se revela que existe); a un
estudiante que intenta algo de docente, 403. Ninguna consulta de un estudiante devuelve entregas, intentos ni
notas de otra persona: lo comprueba `tests/test_permisos.py`.
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from aula.modelos import Clase, Inscripcion, Usuario


def no_encontrado(que: str = "recurso") -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"No existe ese {que} o no tienes acceso.")


async def inscripcion(sesion: AsyncSession, clase_id: int, usuario: Usuario) -> Inscripcion | None:
    return (
        await sesion.execute(
            select(Inscripcion).where(Inscripcion.clase_id == clase_id, Inscripcion.usuario_id == usuario.id)
        )
    ).scalar_one_or_none()


async def exigir_miembro(sesion: AsyncSession, clase_id: int, usuario: Usuario) -> tuple[Clase, Inscripcion]:
    clase = await sesion.get(Clase, clase_id)
    if clase is None:
        raise no_encontrado("clase")
    ins = await inscripcion(sesion, clase_id, usuario)
    if ins is None:
        raise no_encontrado("clase")
    return clase, ins


async def exigir_docente(sesion: AsyncSession, clase_id: int, usuario: Usuario) -> Clase:
    clase, ins = await exigir_miembro(sesion, clase_id, usuario)
    if ins.rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente de la clase puede hacer esto.")
    return clase


def exigir_rol_global(usuario: Usuario, *roles: str) -> None:
    if usuario.rol_global not in roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tu cuenta no tiene permiso para esto.")


async def cuantos_docentes(sesion: AsyncSession, clase_id: int) -> int:
    return (
        await sesion.execute(
            select(func.count()).select_from(Inscripcion).where(Inscripcion.clase_id == clase_id, Inscripcion.rol == "docente")
        )
    ).scalar_one()
