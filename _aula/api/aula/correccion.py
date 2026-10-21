"""api/aula/correccion.py — arma cada intento desde el banco y lo corrige en el servidor.

La clave nunca viaja al navegador mientras el intento está abierto: `presentar()` construye la vista del
estudiante con enunciado, opciones (en el orden barajado de ese intento) y puntos, y nada más. `corregir()` compara
con la clave guardada: en opción múltiple, el índice que eligió el estudiante se traduce por la permutación de su
intento; en numérica, se acepta coma o punto decimal y una tolerancia absoluta.
"""

from __future__ import annotations

import math
import random

from aula.modelos import Examen, Intento, Pregunta

_azar = random.SystemRandom()


def armar_orden(examen: Examen, banco: list[Pregunta]) -> list[dict]:
    """Elige las preguntas del intento y, si el examen es aleatorio, baraja preguntas y opciones."""
    elegidas = list(banco)
    if examen.preguntas_por_intento and examen.preguntas_por_intento < len(elegidas):
        elegidas = _azar.sample(elegidas, examen.preguntas_por_intento)
        elegidas.sort(key=lambda p: (p.orden, p.id))
    if examen.aleatorio:
        _azar.shuffle(elegidas)
    orden = []
    for p in elegidas:
        perm = None
        if p.tipo == "opcion":
            perm = list(range(len(p.opciones or [])))
            if examen.aleatorio:
                _azar.shuffle(perm)
        orden.append({"id": p.id, "opciones": perm})
    return orden


def presentar(intento: Intento, banco: dict[int, Pregunta]) -> list[dict]:
    """La vista del estudiante: sin `clave` ni `tolerancia`."""
    vista = []
    for item in intento.orden:
        p = banco.get(item["id"])
        if p is None:
            continue
        opciones = None
        if p.tipo == "opcion":
            opciones = [p.opciones[i] for i in item["opciones"]]
        vista.append({"id": p.id, "tipo": p.tipo, "enunciado": p.enunciado, "opciones": opciones, "puntos": p.puntos})
    return vista


def _numero(valor) -> float | None:
    if isinstance(valor, bool) or valor is None:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        texto = valor.strip().replace(" ", "").replace(",", ".")
        try:
            n = float(texto)
        except ValueError:
            return None
        return n if math.isfinite(n) else None
    return None


def es_correcta(p: Pregunta, permutacion: list[int] | None, respuesta) -> bool:
    if respuesta is None:
        return False
    if p.tipo == "opcion":
        if isinstance(respuesta, bool):
            return False
        try:
            indice = int(respuesta)
        except (TypeError, ValueError):
            return False
        perm = permutacion or list(range(len(p.opciones or [])))
        if not 0 <= indice < len(perm):
            return False
        return perm[indice] == p.clave
    if p.tipo == "vf":
        if isinstance(respuesta, str):
            respuesta = {"true": True, "false": False, "v": True, "f": False}.get(respuesta.strip().lower())
        return isinstance(respuesta, bool) and respuesta is p.clave
    n = _numero(respuesta)
    if n is None:
        return False
    return abs(n - float(p.clave)) <= max(p.tolerancia or 0.0, 1e-9)


def corregir(intento: Intento, banco: dict[int, Pregunta]) -> None:
    """Pone `detalle`, `puntaje` y `puntaje_max` en el intento con lo que tenga en `respuestas`."""
    detalle = {}
    total = maximo = 0.0
    respuestas = intento.respuestas or {}
    for item in intento.orden:
        p = banco.get(item["id"])
        if p is None:
            continue
        ok = es_correcta(p, item.get("opciones"), respuestas.get(str(p.id)))
        puntos = p.puntos if ok else 0.0
        detalle[str(p.id)] = {"correcta": ok, "puntos": puntos}
        total += puntos
        maximo += p.puntos
    intento.detalle = detalle
    intento.puntaje = round(total, 4)
    intento.puntaje_max = round(maximo, 4)


def clave_presentada(p: Pregunta, permutacion: list[int] | None):
    """La clave en los términos que vio el estudiante (índice de su orden), para revelarla tras el cierre."""
    if p.tipo == "opcion":
        perm = permutacion or list(range(len(p.opciones or [])))
        return perm.index(p.clave)
    return p.clave
