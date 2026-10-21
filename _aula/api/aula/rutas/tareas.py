"""api/aula/rutas/tareas.py — tareas con fecha límite, puntaje y rúbrica; entregas (texto y/o archivo) y su calificación.

El estudiante solo ve y toca su propia entrega; el docente de la clase ve todas y califica. Una entrega ya
calificada no se reemplaza (el docente puede devolverla borrando la calificación en una versión futura).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aula import archivos, esquemas, permisos, seguridad, tiempo
from aula.db import obtener_sesion
from aula.modelos import Calificacion, Entrega, Tarea, Usuario

rutas = APIRouter(tags=["tareas"])


async def _tarea_y_rol(sesion: AsyncSession, tarea_id: int, usuario: Usuario) -> tuple[Tarea, str]:
    tarea = await sesion.get(Tarea, tarea_id)
    if tarea is None:
        raise permisos.no_encontrado("tarea")
    _, ins = await permisos.exigir_miembro(sesion, tarea.clase_id, usuario)
    if ins.rol != "docente" and not tarea.publicada:
        raise permisos.no_encontrado("tarea")
    return tarea, ins.rol


def _salida_entrega(e: Entrega, c: Calificacion | None, nombre: str | None = None) -> dict:
    return {
        "id": e.id, "tarea_id": e.tarea_id, "estudiante_id": e.estudiante_id, "estudiante": nombre,
        "texto": e.texto, "archivo_nombre": e.archivo_nombre, "archivo_bytes": e.archivo_bytes,
        "entregado_en": e.entregado_en, "tardia": e.tardia,
        "calificacion": (
            {"puntaje": c.puntaje, "comentario": c.comentario, "por_criterio": c.por_criterio, "calificado_en": c.calificado_en}
            if c else None
        ),
    }


@rutas.get("/clases/{clase_id}/tareas", response_model=list[esquemas.TareaSalida])
async def listar(clase_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    _, ins = await permisos.exigir_miembro(sesion, clase_id, usuario)
    consulta = select(Tarea).where(Tarea.clase_id == clase_id).order_by(Tarea.creado_en, Tarea.id)
    if ins.rol != "docente":
        consulta = consulta.where(Tarea.publicada.is_(True))
    return (await sesion.execute(consulta)).scalars().all()


@rutas.post("/clases/{clase_id}/tareas", response_model=esquemas.TareaSalida, status_code=201)
async def crear(clase_id: int, datos: esquemas.TareaNueva, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    await permisos.exigir_docente(sesion, clase_id, usuario)
    valores = datos.model_dump()
    valores["rubrica"] = [c.model_dump() for c in datos.rubrica] if datos.rubrica else None
    tarea = Tarea(clase_id=clase_id, **valores)
    sesion.add(tarea)
    await sesion.commit()
    return tarea


@rutas.get("/tareas/{tarea_id}", response_model=esquemas.TareaSalida)
async def ver(tarea_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    tarea, _ = await _tarea_y_rol(sesion, tarea_id, usuario)
    return tarea


@rutas.patch("/tareas/{tarea_id}", response_model=esquemas.TareaSalida)
async def cambiar(tarea_id: int, datos: esquemas.TareaCambio, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    tarea, rol = await _tarea_y_rol(sesion, tarea_id, usuario)
    if rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente de la clase puede hacer esto.")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        if valor is not None or campo == "fecha_limite":
            setattr(tarea, campo, valor)
    await sesion.commit()
    return tarea


@rutas.delete("/tareas/{tarea_id}", status_code=204)
async def borrar(tarea_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    tarea, rol = await _tarea_y_rol(sesion, tarea_id, usuario)
    if rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente de la clase puede hacer esto.")
    rutas_archivos = (await sesion.execute(select(Entrega.archivo_ruta).where(Entrega.tarea_id == tarea.id))).scalars().all()
    await sesion.delete(tarea)
    await sesion.commit()
    for r in rutas_archivos:
        archivos.borrar(r)
    return Response(status_code=204)


# --- entregas -----------------------------------------------------------------------------------------------------

@rutas.put("/tareas/{tarea_id}/entrega", response_model=esquemas.EntregaSalida)
async def entregar(
    tarea_id: int,
    texto: str = Form(default="", max_length=50_000),
    archivo: UploadFile | None = File(default=None),
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    tarea, rol = await _tarea_y_rol(sesion, tarea_id, usuario)
    if rol != "estudiante":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo los estudiantes de la clase entregan tareas.")
    if archivo is not None and not archivo.filename:
        archivo = None
    if archivo is not None and not tarea.acepta_archivo:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Esta tarea no acepta archivos.")
    if not texto.strip() and archivo is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "La entrega necesita un texto o un archivo.")
    entrega = (
        await sesion.execute(select(Entrega).where(Entrega.tarea_id == tarea.id, Entrega.estudiante_id == usuario.id))
    ).scalar_one_or_none()
    if entrega is not None:
        calificada = (await sesion.execute(select(Calificacion.id).where(Calificacion.entrega_id == entrega.id))).first()
        if calificada:
            raise HTTPException(status.HTTP_409_CONFLICT, "La entrega ya fue calificada; no se puede reemplazar.")
    ruta_vieja = entrega.archivo_ruta if entrega else None
    nuevo = None
    if archivo is not None:
        nuevo = await archivos.guardar(archivo, tarea.id, usuario.id)
    ahora = tiempo.ahora()
    if entrega is None:
        entrega = Entrega(tarea_id=tarea.id, estudiante_id=usuario.id)
        sesion.add(entrega)
    entrega.texto = texto
    if nuevo is not None:
        entrega.archivo_ruta, entrega.archivo_nombre, entrega.archivo_bytes = nuevo
    entrega.entregado_en = ahora
    entrega.tardia = bool(tarea.fecha_limite and ahora > tarea.fecha_limite)
    try:
        await sesion.commit()
    except Exception:
        if nuevo is not None:
            archivos.borrar(nuevo[0])
        raise
    if nuevo is not None and ruta_vieja and ruta_vieja != entrega.archivo_ruta:
        archivos.borrar(ruta_vieja)
    return _salida_entrega(entrega, None, usuario.nombre_visible)


@rutas.get("/tareas/{tarea_id}/entrega", response_model=esquemas.EntregaSalida | None)
async def mi_entrega(tarea_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    tarea, _ = await _tarea_y_rol(sesion, tarea_id, usuario)
    fila = (
        await sesion.execute(
            select(Entrega, Calificacion).outerjoin(Calificacion, Calificacion.entrega_id == Entrega.id)
            .where(Entrega.tarea_id == tarea.id, Entrega.estudiante_id == usuario.id)
        )
    ).first()
    return _salida_entrega(fila[0], fila[1], usuario.nombre_visible) if fila else None


@rutas.get("/tareas/{tarea_id}/entregas", response_model=list[esquemas.EntregaSalida])
async def entregas(tarea_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    tarea, rol = await _tarea_y_rol(sesion, tarea_id, usuario)
    if rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente ve las entregas de la clase.")
    filas = (
        await sesion.execute(
            select(Entrega, Calificacion, Usuario.nombre_visible)
            .outerjoin(Calificacion, Calificacion.entrega_id == Entrega.id)
            .join(Usuario, Usuario.id == Entrega.estudiante_id)
            .where(Entrega.tarea_id == tarea.id).order_by(Usuario.nombre_visible)
        )
    ).all()
    return [_salida_entrega(e, c, n) for e, c, n in filas]


async def _entrega_visible(sesion: AsyncSession, entrega_id: int, usuario: Usuario) -> tuple[Entrega, Tarea, str]:
    entrega = await sesion.get(Entrega, entrega_id)
    if entrega is None:
        raise permisos.no_encontrado("entrega")
    tarea = await sesion.get(Tarea, entrega.tarea_id)
    ins = await permisos.inscripcion(sesion, tarea.clase_id, usuario)
    es_docente = ins is not None and ins.rol == "docente"
    if not es_docente and entrega.estudiante_id != usuario.id:
        raise permisos.no_encontrado("entrega")  # 404: ni siquiera se confirma que exista
    return entrega, tarea, ("docente" if es_docente else "estudiante")


@rutas.get("/entregas/{entrega_id}", response_model=esquemas.EntregaSalida)
async def ver_entrega(entrega_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    entrega, _, _ = await _entrega_visible(sesion, entrega_id, usuario)
    c = (await sesion.execute(select(Calificacion).where(Calificacion.entrega_id == entrega.id))).scalar_one_or_none()
    return _salida_entrega(entrega, c)


@rutas.get("/entregas/{entrega_id}/archivo")
async def descargar(entrega_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    entrega, _, _ = await _entrega_visible(sesion, entrega_id, usuario)
    if not entrega.archivo_ruta:
        raise permisos.no_encontrado("archivo")
    ruta = archivos.ruta_absoluta(entrega.archivo_ruta)
    if not ruta.exists():
        raise permisos.no_encontrado("archivo")
    # Siempre como descarga y sin adivinar el tipo: un archivo subido nunca se interpreta en el navegador.
    return FileResponse(
        ruta, media_type="application/octet-stream", filename=entrega.archivo_nombre or ruta.name,
        headers={"X-Content-Type-Options": "nosniff", "Cache-Control": "no-store"},
    )


@rutas.put("/entregas/{entrega_id}/calificacion", response_model=esquemas.EntregaSalida)
async def calificar(
    entrega_id: int,
    datos: esquemas.CalificacionNueva,
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    entrega, tarea, rol = await _entrega_visible(sesion, entrega_id, usuario)
    if rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente de la clase califica.")
    puntaje = datos.puntaje
    if tarea.rubrica:
        criterios = {c["criterio"]: c["puntos"] for c in tarea.rubrica}
        if datos.por_criterio is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Esta tarea tiene rúbrica: califica cada criterio en `por_criterio`.")
        if set(datos.por_criterio) != set(criterios):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Los criterios son: {', '.join(criterios)}.")
        for nombre, puntos in datos.por_criterio.items():
            if not 0 <= puntos <= criterios[nombre]:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"«{nombre}» va de 0 a {criterios[nombre]}.")
        puntaje = round(sum(datos.por_criterio.values()), 4)
    if puntaje is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Falta el puntaje.")
    if puntaje > tarea.puntaje_max:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"El puntaje máximo es {tarea.puntaje_max}.")
    c = (await sesion.execute(select(Calificacion).where(Calificacion.entrega_id == entrega.id))).scalar_one_or_none()
    if c is None:
        c = Calificacion(entrega_id=entrega.id, puntaje=puntaje)
        sesion.add(c)
    c.puntaje = puntaje
    c.comentario = datos.comentario
    c.por_criterio = datos.por_criterio if tarea.rubrica else None
    c.calificado_por = usuario.id
    c.calificado_en = tiempo.ahora()
    await sesion.commit()
    nombre = (await sesion.get(Usuario, entrega.estudiante_id)).nombre_visible
    return _salida_entrega(entrega, c, nombre)
