"""api/aula/rutas/progreso.py — lecciones completadas por pub, para sincronizar `aula:<pub>:completadas` entre
dispositivos. La fusión es una unión: gana la fecha más antigua de cada lección y `null` la desmarca.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aula import esquemas, seguridad
from aula.db import obtener_sesion
from aula.modelos import Progreso, Usuario

rutas = APIRouter(prefix="/progreso", tags=["progreso"])

Pub = Annotated[str, Path(pattern=r"^[a-z0-9][a-z0-9-]{0,59}$")]


async def _mapa(sesion: AsyncSession, usuario_id: int, pub: str) -> dict[str, Progreso]:
    filas = (await sesion.execute(select(Progreso).where(Progreso.usuario_id == usuario_id, Progreso.pub == pub))).scalars().all()
    return {p.leccion: p for p in filas}


@rutas.get("/{pub}")
async def leer(pub: Pub, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    return {"completadas": {k: p.completada_el for k, p in sorted((await _mapa(sesion, usuario.id, pub)).items())}}


@rutas.put("/{pub}")
async def fusionar(
    pub: Pub,
    datos: esquemas.Progreso,
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    mapa = await _mapa(sesion, usuario.id, pub)
    if len(mapa) + len(datos.completadas) > 5000:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Demasiadas lecciones para un pub.")
    for leccion, fecha in datos.completadas.items():
        actual = mapa.get(leccion)
        if fecha is None:
            if actual is not None:
                await sesion.delete(actual)
                del mapa[leccion]
        elif actual is None:
            nuevo = Progreso(usuario_id=usuario.id, pub=pub, leccion=leccion, completada_el=fecha)
            sesion.add(nuevo)
            mapa[leccion] = nuevo
        elif fecha < actual.completada_el:
            actual.completada_el = fecha
    await sesion.commit()
    return {"completadas": {k: p.completada_el for k, p in sorted(mapa.items())}}
