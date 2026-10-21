"""api/aula/rutas/clases.py — clases (un grupo de un curso de `docencia` en un pub), inscripción con código, miembros
y libro de calificaciones (el docente ve a todos; el estudiante, solo su fila).
"""

from __future__ import annotations

import csv
import io
import secrets

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from aula import esquemas, permisos, seguridad
from aula.db import obtener_sesion
from aula.modelos import Calificacion, Clase, Entrega, Examen, Inscripcion, Intento, Tarea, Usuario

rutas = APIRouter(tags=["clases"])

_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # sin 0/O ni 1/I: se dicta en voz alta


def _codigo() -> str:
    return "".join(secrets.choice(_ALFABETO) for _ in range(7))


async def _codigo_libre(sesion: AsyncSession) -> str:
    while True:
        c = _codigo()
        if not (await sesion.execute(select(Clase.id).where(Clase.codigo == c))).first():
            return c


def _salida(clase: Clase, rol: str) -> dict:
    return {
        "id": clase.id, "nombre": clase.nombre, "curso_id": clase.curso_id, "pub": clase.pub,
        "periodo": clase.periodo, "archivada": clase.archivada, "mi_rol": rol,
        "codigo": clase.codigo if rol == "docente" else None,
    }


@rutas.post("/clases", response_model=esquemas.ClaseSalida, status_code=201)
async def crear(datos: esquemas.ClaseNueva, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    permisos.exigir_rol_global(usuario, "docente", "admin")
    clase = Clase(nombre=datos.nombre, curso_id=datos.curso_id, pub=datos.pub, periodo=datos.periodo, codigo=await _codigo_libre(sesion))
    sesion.add(clase)
    await sesion.flush()
    sesion.add(Inscripcion(clase_id=clase.id, usuario_id=usuario.id, rol="docente"))
    await sesion.commit()
    return _salida(clase, "docente")


@rutas.get("/clases", response_model=list[esquemas.ClaseSalida])
async def mis_clases(
    pub: str | None = Query(default=None, max_length=60),
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    consulta = (
        select(Clase, Inscripcion.rol).join(Inscripcion, Inscripcion.clase_id == Clase.id)
        .where(Inscripcion.usuario_id == usuario.id).order_by(Clase.archivada, Clase.nombre)
    )
    if pub:
        consulta = consulta.where(Clase.pub == pub)
    return [_salida(c, rol) for c, rol in (await sesion.execute(consulta)).all()]


@rutas.get("/clases/{clase_id}", response_model=esquemas.ClaseSalida)
async def ver(clase_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    clase, ins = await permisos.exigir_miembro(sesion, clase_id, usuario)
    return _salida(clase, ins.rol)


@rutas.patch("/clases/{clase_id}", response_model=esquemas.ClaseSalida)
async def cambiar(clase_id: int, datos: esquemas.ClaseCambio, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    clase = await permisos.exigir_docente(sesion, clase_id, usuario)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        if valor is not None:
            setattr(clase, campo, valor)
    await sesion.commit()
    return _salida(clase, "docente")


@rutas.post("/clases/{clase_id}/codigo", response_model=esquemas.ClaseSalida)
async def nuevo_codigo(clase_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    clase = await permisos.exigir_docente(sesion, clase_id, usuario)
    clase.codigo = await _codigo_libre(sesion)
    await sesion.commit()
    return _salida(clase, "docente")


@rutas.post("/clases/inscribirse", response_model=esquemas.ClaseSalida)
async def inscribirse(datos: esquemas.Inscribirse, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    clave = f"codigo:{usuario.id}"
    if espera := seguridad.limitador_sesion.bloqueado(clave):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Demasiados códigos equivocados. Espera unos minutos.", headers={"Retry-After": str(espera)})
    clase = (await sesion.execute(select(Clase).where(Clase.codigo == datos.codigo.strip().upper()))).scalar_one_or_none()
    if clase is None or clase.archivada:
        seguridad.limitador_sesion.anotar(clave)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ese código no corresponde a ninguna clase abierta.")
    ins = await permisos.inscripcion(sesion, clase.id, usuario)
    if ins is None:
        ins = Inscripcion(clase_id=clase.id, usuario_id=usuario.id, rol="estudiante")
        sesion.add(ins)
        await sesion.commit()
    return _salida(clase, ins.rol)


@rutas.get("/clases/{clase_id}/miembros", response_model=list[esquemas.Miembro])
async def miembros(clase_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    """El docente ve a todos con su correo; el estudiante solo ve a los docentes (no la lista de compañeros)."""
    _, ins = await permisos.exigir_miembro(sesion, clase_id, usuario)
    consulta = (
        select(Inscripcion, Usuario).join(Usuario, Usuario.id == Inscripcion.usuario_id)
        .where(Inscripcion.clase_id == clase_id).order_by(Inscripcion.rol, Usuario.nombre_visible)
    )
    if ins.rol != "docente":
        consulta = consulta.where(Inscripcion.rol == "docente")
    return [
        {"usuario_id": u.id, "nombre_visible": u.nombre_visible, "rol": i.rol, "correo": u.correo if ins.rol == "docente" else None}
        for i, u in (await sesion.execute(consulta)).all()
    ]


@rutas.post("/clases/{clase_id}/docentes", response_model=esquemas.Miembro, status_code=201)
async def sumar_docente(clase_id: int, datos: esquemas.NuevoDocente, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    await permisos.exigir_docente(sesion, clase_id, usuario)
    otro = (await sesion.execute(select(Usuario).where(Usuario.correo == datos.correo.strip().lower()))).scalar_one_or_none()
    if otro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No hay una cuenta con ese correo: que se registre primero.")
    ins = await permisos.inscripcion(sesion, clase_id, otro)
    if ins is None:
        ins = Inscripcion(clase_id=clase_id, usuario_id=otro.id, rol="docente")
        sesion.add(ins)
    else:
        ins.rol = "docente"
    await sesion.commit()
    return {"usuario_id": otro.id, "nombre_visible": otro.nombre_visible, "rol": "docente", "correo": otro.correo}


@rutas.delete("/clases/{clase_id}/miembros/{usuario_id}", status_code=204)
async def retirar(clase_id: int, usuario_id: int, usuario: Usuario = Depends(seguridad.usuario_actual), sesion: AsyncSession = Depends(obtener_sesion)):
    """El docente retira a alguien; cualquiera puede salir de una clase. Sus entregas e intentos en esa clase se
    conservan para el docente hasta que la persona borre su cuenta."""
    _, ins = await permisos.exigir_miembro(sesion, clase_id, usuario)
    if usuario_id != usuario.id and ins.rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el docente puede retirar a otra persona.")
    objetivo = (
        await sesion.execute(select(Inscripcion).where(Inscripcion.clase_id == clase_id, Inscripcion.usuario_id == usuario_id))
    ).scalar_one_or_none()
    if objetivo is None:
        raise permisos.no_encontrado("miembro")
    if objetivo.rol == "docente" and await permisos.cuantos_docentes(sesion, clase_id) == 1:
        raise HTTPException(status.HTTP_409_CONFLICT, "La clase se quedaría sin docente.")
    await sesion.delete(objetivo)
    await sesion.commit()
    return Response(status_code=204)


@rutas.get("/clases/{clase_id}/notas")
async def notas(
    clase_id: int,
    formato: str = Query(default="json", pattern="^(json|csv)$"),
    usuario: Usuario = Depends(seguridad.usuario_actual),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    """Libro de calificaciones: tareas (nota de la entrega) y exámenes (mejor intento corregido)."""
    _, ins = await permisos.exigir_miembro(sesion, clase_id, usuario)
    tareas = (await sesion.execute(select(Tarea).where(Tarea.clase_id == clase_id).order_by(Tarea.creado_en, Tarea.id))).scalars().all()
    examenes = (await sesion.execute(select(Examen).where(Examen.clase_id == clase_id).order_by(Examen.creado_en, Examen.id))).scalars().all()
    estudiantes_q = (
        select(Usuario).join(Inscripcion, Inscripcion.usuario_id == Usuario.id)
        .where(Inscripcion.clase_id == clase_id, Inscripcion.rol == "estudiante").order_by(Usuario.nombre_visible)
    )
    if ins.rol != "docente":
        estudiantes_q = estudiantes_q.where(Usuario.id == usuario.id)
    estudiantes = (await sesion.execute(estudiantes_q)).scalars().all()
    ids = [e.id for e in estudiantes]
    notas_tareas = {}
    if ids and tareas:
        filas = (
            await sesion.execute(
                select(Entrega.estudiante_id, Entrega.tarea_id, Calificacion.puntaje)
                .join(Calificacion, Calificacion.entrega_id == Entrega.id)
                .where(Entrega.tarea_id.in_([t.id for t in tareas]), Entrega.estudiante_id.in_(ids))
            )
        ).all()
        notas_tareas = {(e, t): p for e, t, p in filas}
    notas_examenes = {}
    if ids and examenes:
        filas = (
            await sesion.execute(
                select(Intento.estudiante_id, Intento.examen_id, func.max(Intento.puntaje))
                .where(Intento.examen_id.in_([x.id for x in examenes]), Intento.estudiante_id.in_(ids), Intento.estado != "en_curso")
                .group_by(Intento.estudiante_id, Intento.examen_id)
            )
        ).all()
        notas_examenes = {(e, x): p for e, x, p in filas}
    libro = {
        "tareas": [{"id": t.id, "titulo": t.titulo, "puntaje_max": t.puntaje_max} for t in tareas],
        "examenes": [{"id": x.id, "titulo": x.titulo} for x in examenes],
        "estudiantes": [
            {
                "id": e.id, "nombre_visible": e.nombre_visible,
                "tareas": {str(t.id): notas_tareas.get((e.id, t.id)) for t in tareas},
                "examenes": {str(x.id): notas_examenes.get((e.id, x.id)) for x in examenes},
            }
            for e in estudiantes
        ],
    }
    if formato == "json":
        return libro
    if ins.rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "La exportación es del docente.")
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(["estudiante"] + [f"T: {t['titulo']}" for t in libro["tareas"]] + [f"E: {x['titulo']}" for x in libro["examenes"]])
    for e in libro["estudiantes"]:
        escritor.writerow([e["nombre_visible"]] + [e["tareas"][str(t["id"])] for t in libro["tareas"]] + [e["examenes"][str(x["id"])] for x in libro["examenes"]])
    return Response(
        content=salida.getvalue(), media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="notas-clase-{clase_id}.csv"'},
    )
