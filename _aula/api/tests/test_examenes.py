"""api/tests/test_examenes.py — exámenes corregidos en el servidor sin filtrar la clave, con tiempo, azar e intentos."""

import json
from datetime import timedelta

import pytest

from aula import tiempo
from aula.config import config

pytestmark = pytest.mark.anyio

BANCO = [
    {"tipo": "opcion", "enunciado": "¿Capital del Perú?", "opciones": ["Cusco", "Lima", "Arequipa", "Trujillo"], "clave": 1, "puntos": 2},
    {"tipo": "vf", "enunciado": "La media es sensible a valores extremos.", "clave": True},
    {"tipo": "numerica", "enunciado": "¿Cuánto es 1/4 en decimal?", "clave": 0.25, "tolerancia": 0.001},
    {"tipo": "opcion", "enunciado": "¿Medida de dispersión?", "opciones": ["Moda", "Varianza", "Mediana"], "clave": 1},
    {"tipo": "vf", "enunciado": "Una muestra siempre es la población entera.", "clave": False},
]
CAMPOS_SECRETOS = {"clave", "tolerancia", "claves", "detalle"}


async def _examen(cliente, aula, **extra):
    cid = aula["clase"]["id"]
    datos = {"titulo": "Control 1", "preguntas": BANCO, "publicado": True, **extra}
    r = await cliente.post(f"/clases/{cid}/examenes", headers=aula["docente"]["h"], json=datos)
    assert r.status_code == 201, r.text
    return r.json()


def _sin_secretos(objeto):
    """Recorre la respuesta: ninguna clave del diccionario puede ser un campo secreto."""
    if isinstance(objeto, dict):
        assert not (set(objeto) & CAMPOS_SECRETOS), set(objeto) & CAMPOS_SECRETOS
        for v in objeto.values():
            _sin_secretos(v)
    elif isinstance(objeto, list):
        for v in objeto:
            _sin_secretos(v)


def _respuestas_correctas(intento, banco_docente):
    """Lo que respondería quien sabe: traduce la opción correcta al orden barajado que vio el estudiante."""
    por_id = {p["id"]: p for p in banco_docente}
    respuestas = {}
    for p in intento["preguntas"]:
        original = por_id[p["id"]]
        if p["tipo"] == "opcion":
            respuestas[str(p["id"])] = p["opciones"].index(original["opciones"][original["clave"]])
        elif p["tipo"] == "vf":
            respuestas[str(p["id"])] = original["clave"]
        else:
            respuestas[str(p["id"])] = str(original["clave"]).replace(".", ",")  # coma decimal
    return respuestas


async def test_intento_sin_clave_y_corregido_en_servidor(cliente, aula):
    examen = await _examen(cliente, aula, preguntas_por_intento=3, intentos_max=2)
    ana = aula["ana"]["h"]
    ficha = await cliente.get(f"/examenes/{examen['id']}", headers=ana)
    assert "preguntas" not in ficha.json()
    r = await cliente.post(f"/examenes/{examen['id']}/intentos", headers=ana)
    assert r.status_code == 201
    intento = r.json()
    assert len(intento["preguntas"]) == 3
    _sin_secretos(intento)
    _sin_secretos((await cliente.get(f"/intentos/{intento['id']}", headers=ana)).json())
    # el banco con claves solo lo ve el docente
    banco = (await cliente.get(f"/examenes/{examen['id']}", headers=aula["docente"]["h"])).json()["preguntas"]
    assert all("clave" in p for p in banco)
    respuestas = _respuestas_correctas(intento, banco)
    r = await cliente.post(f"/intentos/{intento['id']}/entregar", headers=ana, json={"respuestas": respuestas})
    assert r.status_code == 200
    nota = r.json()
    assert nota["estado"] == "entregado" and nota["puntaje"] == nota["puntaje_max"] > 0
    assert all(d["correcta"] for d in nota["detalle"].values())
    assert "claves" not in nota  # sin revelar_claves, nunca
    # segundo intento, todo mal
    intento2 = (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=ana)).json()
    malas = {}
    for p in intento2["preguntas"]:
        malas[str(p["id"])] = {"opcion": -1, "vf": "nada", "numerica": "abc"}[p["tipo"]]
    nota2 = (await cliente.post(f"/intentos/{intento2['id']}/entregar", headers=ana, json={"respuestas": malas})).json()
    assert nota2["puntaje"] == 0
    # se acabaron los intentos; el libro de notas toma el mejor
    assert (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=ana)).status_code == 409
    libro = (await cliente.get(f"/clases/{aula['clase']['id']}/notas", headers=aula["docente"]["h"])).json()
    fila = next(e for e in libro["estudiantes"] if e["id"] == aula["ana"]["id"])
    assert fila["examenes"][str(examen["id"])] == nota["puntaje"]


async def test_el_azar_cambia_el_orden_pero_no_la_nota(cliente, aula):
    examen = await _examen(cliente, aula, intentos_max=20)
    banco = (await cliente.get(f"/examenes/{examen['id']}", headers=aula["docente"]["h"])).json()["preguntas"]
    ordenes = set()
    for _ in range(6):
        intento = (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=aula["ana"]["h"])).json()
        ordenes.add(json.dumps([(p["id"], p["opciones"]) for p in intento["preguntas"]]))
        nota = (await cliente.post(f"/intentos/{intento['id']}/entregar", headers=aula["ana"]["h"], json={"respuestas": _respuestas_correctas(intento, banco)})).json()
        assert nota["puntaje"] == nota["puntaje_max"] == 6
    assert len(ordenes) > 1


async def test_vencido_se_corrige_con_lo_guardado(cliente, aula, monkeypatch):
    examen = await _examen(cliente, aula, minutos=10, aleatorio=False)
    ana = aula["ana"]["h"]
    intento = (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=ana)).json()
    banco = (await cliente.get(f"/examenes/{examen['id']}", headers=aula["docente"]["h"])).json()["preguntas"]
    buenas = _respuestas_correctas(intento, banco)
    primera = next(iter(buenas))
    r = await cliente.put(f"/intentos/{intento['id']}/respuestas", headers=ana, json={"respuestas": {primera: buenas[primera]}})
    assert r.status_code == 200
    # una pregunta ajena al intento se rechaza
    assert (await cliente.put(f"/intentos/{intento['id']}/respuestas", headers=ana, json={"respuestas": {"999999": 1}})).status_code == 422
    tarde = tiempo.ahora() + timedelta(minutes=10, seconds=config.gracia_examen_s + 5)
    monkeypatch.setattr(tiempo, "ahora", lambda: tarde)
    r = await cliente.post(f"/intentos/{intento['id']}/entregar", headers=ana, json={"respuestas": buenas})
    assert r.status_code == 200
    nota = r.json()
    assert nota["estado"] == "vencido" and "aviso" in nota
    assert nota["puntaje"] == 2  # solo la primera (opción, 2 puntos) se guardó a tiempo
    assert (await cliente.put(f"/intentos/{intento['id']}/respuestas", headers=ana, json={"respuestas": buenas})).status_code == 409


async def test_dentro_de_la_gracia_se_acepta(cliente, aula, monkeypatch):
    examen = await _examen(cliente, aula, minutos=5, aleatorio=False)
    intento = (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=aula["ana"]["h"])).json()
    casi = tiempo.ahora() + timedelta(minutes=5, seconds=config.gracia_examen_s - 5)
    monkeypatch.setattr(tiempo, "ahora", lambda: casi)
    r = await cliente.post(f"/intentos/{intento['id']}/entregar", headers=aula["ana"]["h"], json={"respuestas": {}})
    assert r.json()["estado"] == "entregado"


async def test_claves_solo_tras_el_cierre_si_el_docente_lo_pide(cliente, aula, monkeypatch):
    cierre = tiempo.ahora() + timedelta(hours=1)
    examen = await _examen(cliente, aula, revelar_claves=True, cierra_en=cierre.isoformat())
    ana = aula["ana"]["h"]
    intento = (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=ana)).json()
    assert intento["vence_en"] is not None  # el cierre limita el intento aunque no tenga minutos
    nota = (await cliente.post(f"/intentos/{intento['id']}/entregar", headers=ana, json={"respuestas": {}})).json()
    assert "claves" not in nota
    despues = cierre + timedelta(minutes=1)
    monkeypatch.setattr(tiempo, "ahora", lambda: despues)
    vista = (await cliente.get(f"/intentos/{intento['id']}", headers=ana)).json()
    assert set(vista["claves"]) == {str(p["id"]) for p in intento["preguntas"]}
    assert (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=ana)).status_code == 409  # ya cerró


async def test_examen_no_publicado_y_ajeno(cliente, aula):
    examen = await _examen(cliente, aula, publicado=False)
    assert (await cliente.get(f"/examenes/{examen['id']}", headers=aula["ana"]["h"])).status_code == 404
    assert (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=aula["ana"]["h"])).status_code == 404
    await cliente.patch(f"/examenes/{examen['id']}", headers=aula["docente"]["h"], json={"publicado": True})
    intento = (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=aula["ana"]["h"])).json()
    # Beto no ve, no responde ni entrega el intento de Ana
    beto = aula["beto"]["h"]
    assert (await cliente.get(f"/intentos/{intento['id']}", headers=beto)).status_code == 404
    assert (await cliente.post(f"/intentos/{intento['id']}/entregar", headers=beto, json={"respuestas": {}})).status_code == 404
    assert (await cliente.get(f"/examenes/{examen['id']}/intentos", headers=beto)).json() == []
    # el docente sí lo ve, con claves, pero no puede responder por ella
    vista = await cliente.get(f"/intentos/{intento['id']}", headers=aula["docente"]["h"])
    assert vista.status_code == 200
    assert (await cliente.put(f"/intentos/{intento['id']}/respuestas", headers=aula["docente"]["h"], json={"respuestas": {}})).status_code == 403
    # un intento abierto a la vez
    assert (await cliente.post(f"/examenes/{examen['id']}/intentos", headers=aula["ana"]["h"])).status_code == 409


async def test_banco_mal_formado(cliente, aula):
    cid, h = aula["clase"]["id"], aula["docente"]["h"]
    malas = [
        {"tipo": "opcion", "enunciado": "x", "opciones": ["a"], "clave": 0},
        {"tipo": "opcion", "enunciado": "x", "opciones": ["a", "b"], "clave": 5},
        {"tipo": "vf", "enunciado": "x", "clave": 1.5},
        {"tipo": "numerica", "enunciado": "x", "clave": True},
    ]
    for p in malas:
        r = await cliente.post(f"/clases/{cid}/examenes", headers=h, json={"titulo": "Malo", "preguntas": [p]})
        assert r.status_code == 422, p
    r = await cliente.post(f"/clases/{cid}/examenes", headers=h, json={"titulo": "Malo", "preguntas": BANCO, "preguntas_por_intento": 9})
    assert r.status_code == 422
