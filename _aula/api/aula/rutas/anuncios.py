"""api/aula/rutas/anuncios.py — el tablón de la clase: el docente publica y borra; todos los miembros leen."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aula import esquemas, permisos, seguridad
from aula.db import obtener_sesion
from aula.modelos import Anuncio, Usuario

rutas = APIRouter(tags=["anuncios"])


def _salida(a: Anuncio, autor: str | None) -> dict:
    return {"id": a.id, "clase_id": a.clase_id, "autor": autor, "texto": a.texto, "creado_en": a.creado_en}


@rutas.get("/clases/{clase_id}/anuncios", response_model=list[esquemas.AnuncioSalida])
async def listar(clase_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    await permisos.exigir_miembro(sesion, clase_id, usuario)
    filas = (
        await sesion.execute(
            select(Anuncio, Usuario.nombre_visible).outerjoin(Usuario, Usuario.id == Anuncio.autor_id)
            .where(Anuncio.clase_id == clase_id).order_by(Anuncio.creado_en.desc(), Anuncio.id.desc())
        )
    ).all()
    return [_salida(a, n) for a, n in filas]


@rutas.post("/clases/{clase_id}/anuncios", response_model=esquemas.AnuncioSalida, status_code=201)
async def publicar(clase_id: int, datos: esquemas.AnuncioNuevo, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    await permisos.exigir_docente(sesion, clase_id, usuario)
    anuncio = Anuncio(clase_id=clase_id, autor_id=usuario.id, texto=datos.texto)
    sesion.add(anuncio)
    await sesion.commit()
    return _salida(anuncio, usuario.nombre_visible)


@rutas.delete("/anuncios/{anuncio_id}", status_code=204)
async def borrar(anuncio_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    anuncio = await sesion.get(Anuncio, anuncio_id)
    if anuncio is None:
        raise permisos.no_encontrado("anuncio")
    await permisos.exigir_docente(sesion, anuncio.clase_id, usuario)
    await sesion.delete(anuncio)
    await sesion.commit()
    return Response(status_code=204)
