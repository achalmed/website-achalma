"""api/aula/rutas/examenes.py — exámenes calificados en el servidor: banco de preguntas con su clave (solo aquí),
intentos con tiempo límite y preguntas al azar, guardado parcial y corrección al entregar o al vencer.

El docente ve el banco con las claves y todos los intentos; el estudiante ve la ficha del examen, sus intentos y,
en un intento abierto, solo enunciados y opciones. La clave se le muestra únicamente si el docente lo pidió
(`revelar_claves`) y el examen ya cerró.
"""

from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from aula import correccion, esquemas, permisos, seguridad, tiempo
from aula.config import config
from aula.db import obtener_sesion
from aula.modelos import Examen, Intento, Pregunta, Usuario

rutas = APIRouter(tags=["exámenes"])


def _ficha(x: Examen) -> dict:
    return {
        "id": x.id, "clase_id": x.clase_id, "titulo": x.titulo, "instrucciones": x.instrucciones,
        "minutos": x.minutos, "intentos_max": x.intentos_max, "preguntas_por_intento": x.preguntas_por_intento,
        "aleatorio": x.aleatorio, "abre_en": x.abre_en, "cierra_en": x.cierra_en, "publicado": x.publicado,
        "revelar_claves": x.revelar_claves,
    }


def _banco_docente(preguntas: list[Pregunta]) -> list[dict]:
    return [
        {"id": p.id, "orden": p.orden, "tipo": p.tipo, "enunciado": p.enunciado, "opciones": p.opciones,
         "clave": p.clave, "tolerancia": p.tolerancia, "puntos": p.puntos}
        for p in preguntas
    ]


async def _banco(sesion: AsyncSession, examen_id: int) -> list[Pregunta]:
    return list((await sesion.execute(select(Pregunta).where(Pregunta.examen_id == examen_id).order_by(Pregunta.orden, Pregunta.id))).scalars().all())


async def _examen_y_rol(sesion: AsyncSession, examen_id: int, usuario: Usuario) -> tuple[Examen, str]:
    examen = await sesion.get(Examen, examen_id)
    if examen is None:
        raise permisos.no_encontrado("examen")
    _, ins = await permisos.exigir_miembro(sesion, examen.clase_id, usuario)
    if ins.rol != "docente" and not examen.publicado:
        raise permisos.no_encontrado("examen")
    return examen, ins.rol


def _cerrado(examen: Examen) -> bool:
    return examen.cierra_en is not None and tiempo.ahora() > examen.cierra_en


async def _cerrar_si_vencio(sesion: AsyncSession, intento: Intento) -> bool:
    """Un intento en curso cuyo tiempo (más la gracia) pasó se corrige con lo guardado y queda «vencido»."""
    if intento.estado != "en_curso" or intento.vence_en is None:
        return False
    if tiempo.ahora() <= intento.vence_en + timedelta(seconds=config.gracia_examen_s):
        return False
    banco = {p.id: p for p in await _banco(sesion, intento.examen_id)}
    correccion.corregir(intento, banco)
    intento.estado = "vencido"
    intento.entregado_en = intento.vence_en
    return True


def _vista_intento(intento: Intento, examen: Examen, banco: dict[int, Pregunta], rol: str) -> dict:
    vista = {
        "id": intento.id, "examen_id": intento.examen_id, "estudiante_id": intento.estudiante_id,
        "numero": intento.numero, "estado": intento.estado, "iniciado_en": intento.iniciado_en,
        "vence_en": intento.vence_en, "entregado_en": intento.entregado_en,
        "preguntas": correccion.presentar(intento, banco), "respuestas": intento.respuestas or {},
    }
    if intento.estado != "en_curso":
        vista["puntaje"] = intento.puntaje
        vista["puntaje_max"] = intento.puntaje_max
        vista["detalle"] = intento.detalle
        if rol == "docente" or (examen.revelar_claves and _cerrado(examen)):
            vista["claves"] = {
                str(item["id"]): correccion.clave_presentada(banco[item["id"]], item.get("opciones"))
                for item in intento.orden if item["id"] in banco
            }
    return vista


@rutas.post("/clases/{clase_id}/examenes", status_code=201)
async def crear(clase_id: int, datos: esquemas.ExamenNuevo, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    await permisos.exigir_docente(sesion, clase_id, usuario)
    valores = datos.model_dump(exclude={"preguntas"})
    examen = Examen(clase_id=clase_id, **valores)
    sesion.add(examen)
    await sesion.flush()
    for i, p in enumerate(datos.preguntas):
        sesion.add(Pregunta(examen_id=examen.id, orden=i, **p.model_dump()))
    await sesion.commit()
    return {**_ficha(examen), "preguntas": _banco_docente(await _banco(sesion, examen.id))}


@rutas.get("/clases/{clase_id}/examenes")
async def listar(clase_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    _, ins = await permisos.exigir_miembro(sesion, clase_id, usuario)
    consulta = select(Examen).where(Examen.clase_id == clase_id).order_by(Examen.creado_en, Examen.id)
    if ins.rol != "docente":
        consulta = consulta.where(Examen.publicado.is_(True))
    return [_ficha(x) for x in (await sesion.execute(consulta)).scalars().all()]


@rutas.get("/examenes/{examen_id}")
async def ver(examen_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    examen, rol = await _examen_y_rol(sesion, examen_id, usuario)
    ficha = _ficha(examen)
    if rol == "docente":
        ficha["preguntas"] = _banco_docente(await _banco(sesion, examen.id))
    else:
        usados = (
            await sesion.execute(select(func.count()).select_from(Intento).where(Intento.examen_id == examen.id, Intento.estudiante_id == usuario.id))
        ).scalar_one()
        ficha["intentos_usados"] = usados
    return ficha


@rutas.patch("/examenes/{examen_id}")
async def cambiar(examen_id: int, datos: esquemas.ExamenCambio, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    examen, rol = await _examen_y_rol(sesion, examen_id, usuario)
    if rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente de la clase puede hacer esto.")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        if valor is not None or campo in ("minutos", "abre_en", "cierra_en"):
            setattr(examen, campo, valor)
    await sesion.commit()
    return _ficha(examen)


@rutas.post("/examenes/{examen_id}/intentos", status_code=201)
async def empezar(examen_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    examen, rol = await _examen_y_rol(sesion, examen_id, usuario)
    if rol != "estudiante":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo los estudiantes de la clase rinden el examen.")
    ahora = tiempo.ahora()
    if examen.abre_en and ahora < examen.abre_en:
        raise HTTPException(status.HTTP_409_CONFLICT, "El examen todavía no abre.")
    if _cerrado(examen):
        raise HTTPException(status.HTTP_409_CONFLICT, "El examen ya cerró.")
    previos = list((await sesion.execute(
        select(Intento).where(Intento.examen_id == examen.id, Intento.estudiante_id == usuario.id).order_by(Intento.numero)
    )).scalars().all())
    for previo in previos:
        if await _cerrar_si_vencio(sesion, previo):
            await sesion.commit()
    abierto = next((p for p in previos if p.estado == "en_curso"), None)
    if abierto is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, {"mensaje": "Ya tienes un intento en curso.", "intento_id": abierto.id})
    if len(previos) >= examen.intentos_max:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya usaste todos tus intentos.")
    banco_lista = await _banco(sesion, examen.id)
    vence = None
    if examen.minutos:
        vence = ahora + timedelta(minutes=examen.minutos)
    if examen.cierra_en and (vence is None or examen.cierra_en < vence):
        vence = examen.cierra_en
    intento = Intento(
        examen_id=examen.id, estudiante_id=usuario.id, numero=len(previos) + 1, iniciado_en=ahora,
        vence_en=vence, orden=correccion.armar_orden(examen, banco_lista), respuestas={},
    )
    sesion.add(intento)
    await sesion.commit()
    return _vista_intento(intento, examen, {p.id: p for p in banco_lista}, rol)


async def _intento_visible(sesion: AsyncSession, intento_id: int, usuario: Usuario) -> tuple[Intento, Examen, str]:
    intento = await sesion.get(Intento, intento_id)
    if intento is None:
        raise permisos.no_encontrado("intento")
    examen = await sesion.get(Examen, intento.examen_id)
    ins = await permisos.inscripcion(sesion, examen.clase_id, usuario)
    es_docente = ins is not None and ins.rol == "docente"
    if not es_docente and intento.estudiante_id != usuario.id:
        raise permisos.no_encontrado("intento")
    return intento, examen, ("docente" if es_docente else "estudiante")


@rutas.get("/intentos/{intento_id}")
async def ver_intento(intento_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    intento, examen, rol = await _intento_visible(sesion, intento_id, usuario)
    if await _cerrar_si_vencio(sesion, intento):
        await sesion.commit()
    banco = {p.id: p for p in await _banco(sesion, examen.id)}
    return _vista_intento(intento, examen, banco, rol)


def _validas(intento: Intento, respuestas: dict) -> dict:
    ids = {str(item["id"]) for item in intento.orden}
    ajenas = set(respuestas) - ids
    if ajenas:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Preguntas que no son de este intento: {', '.join(sorted(ajenas))}.")
    return respuestas


@rutas.put("/intentos/{intento_id}/respuestas")
async def guardar(intento_id: int, datos: esquemas.Respuestas, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    intento, examen, rol = await _intento_visible(sesion, intento_id, usuario)
    if intento.estudiante_id != usuario.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo quien rinde el intento puede responder.")
    if await _cerrar_si_vencio(sesion, intento):
        await sesion.commit()
    if intento.estado != "en_curso":
        raise HTTPException(status.HTTP_409_CONFLICT, "El intento ya terminó.")
    intento.respuestas = {**(intento.respuestas or {}), **_validas(intento, datos.respuestas)}
    await sesion.commit()
    return {"guardadas": len(intento.respuestas), "vence_en": intento.vence_en}


@rutas.post("/intentos/{intento_id}/entregar")
async def entregar(intento_id: int, datos: esquemas.Respuestas, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    intento, examen, rol = await _intento_visible(sesion, intento_id, usuario)
    if intento.estudiante_id != usuario.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo quien rinde el intento puede entregarlo.")
    banco = {p.id: p for p in await _banco(sesion, examen.id)}
    if not await _cerrar_si_vencio(sesion, intento):
        if intento.estado != "en_curso":
            raise HTTPException(status.HTTP_409_CONFLICT, "El intento ya fue entregado.")
        intento.respuestas = {**(intento.respuestas or {}), **_validas(intento, datos.respuestas)}
        correccion.corregir(intento, banco)
        intento.estado = "entregado"
        intento.entregado_en = tiempo.ahora()
    await sesion.commit()
    vista = _vista_intento(intento, examen, banco, rol)
    if intento.estado == "vencido":
        vista["aviso"] = "El tiempo ya había vencido: se corrigió con las respuestas guardadas antes del vencimiento."
    return vista


@rutas.get("/examenes/{examen_id}/intentos")
async def intentos(examen_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    """El docente ve todos los intentos (resumen); el estudiante, solo los suyos."""
    examen, rol = await _examen_y_rol(sesion, examen_id, usuario)
    consulta = (
        select(Intento, Usuario.nombre_visible).join(Usuario, Usuario.id == Intento.estudiante_id)
        .where(Intento.examen_id == examen.id).order_by(Usuario.nombre_visible, Intento.numero)
    )
    if rol != "docente":
        consulta = consulta.where(Intento.estudiante_id == usuario.id)
    filas = (await sesion.execute(consulta)).all()
    cambio = False
    for intento, _ in filas:
        cambio |= await _cerrar_si_vencio(sesion, intento)
    if cambio:
        await sesion.commit()
    return [
        {"id": i.id, "estudiante_id": i.estudiante_id, "estudiante": n, "numero": i.numero, "estado": i.estado,
         "iniciado_en": i.iniciado_en, "entregado_en": i.entregado_en,
         "puntaje": i.puntaje if i.estado != "en_curso" else None, "puntaje_max": i.puntaje_max}
        for i, n in filas
    ]
