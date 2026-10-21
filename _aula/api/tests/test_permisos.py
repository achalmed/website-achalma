"""api/tests/test_permisos.py — el docente crea y califica; el estudiante ve lo suyo; nadie ve entregas ni notas ajenas."""

import pytest

from tests.conftest import hacer_docente, registrar

pytestmark = pytest.mark.anyio


async def test_solo_un_docente_crea_clases(cliente):
    e = await registrar(cliente, "est@ejemplo.test")
    r = await cliente.post("/clases", headers=e["h"], json={"nombre": "Mía", "curso_id": "python", "pub": "numerus-scriptum"})
    assert r.status_code == 403


async def test_el_codigo_solo_lo_ve_el_docente(cliente, aula):
    cid = aula["clase"]["id"]
    assert (await cliente.get(f"/clases/{cid}", headers=aula["docente"]["h"])).json()["codigo"]
    assert (await cliente.get(f"/clases/{cid}", headers=aula["ana"]["h"])).json()["codigo"] is None


async def test_quien_no_es_miembro_recibe_404(cliente, aula):
    extra = await registrar(cliente, "extra@ejemplo.test")
    cid = aula["clase"]["id"]
    for ruta in (f"/clases/{cid}", f"/clases/{cid}/anuncios", f"/clases/{cid}/tareas", f"/clases/{cid}/examenes", f"/clases/{cid}/notas", f"/clases/{cid}/miembros"):
        assert (await cliente.get(ruta, headers=extra["h"])).status_code == 404, ruta


async def test_estudiante_no_crea_ni_califica(cliente, aula):
    cid, h = aula["clase"]["id"], aula["ana"]["h"]
    assert (await cliente.post(f"/clases/{cid}/anuncios", headers=h, json={"texto": "hola"})).status_code == 403
    assert (await cliente.post(f"/clases/{cid}/tareas", headers=h, json={"titulo": "Tarea"})).status_code == 403
    examen = {"titulo": "Ex", "preguntas": [{"tipo": "vf", "enunciado": "¿Sí?", "clave": True}]}
    assert (await cliente.post(f"/clases/{cid}/examenes", headers=h, json=examen)).status_code == 403
    assert (await cliente.patch(f"/clases/{cid}", headers=h, json={"nombre": "Otra"})).status_code == 403


async def test_nadie_ve_entregas_ni_notas_ajenas(cliente, aula):
    cid, doc, ana, beto = aula["clase"]["id"], aula["docente"], aula["ana"], aula["beto"]
    tarea = (await cliente.post(f"/clases/{cid}/tareas", headers=doc["h"], json={"titulo": "Ensayo", "puntaje_max": 20})).json()
    r = await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=ana["h"], data={"texto": "Texto secreto de Ana"},
                          files={"archivo": ("ensayo.pdf", b"%PDF-1.4 ana", "application/pdf")})
    assert r.status_code == 200, r.text
    entrega_ana = r.json()["id"]
    await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=beto["h"], data={"texto": "Lo de Beto"})
    r = await cliente.put(f"/entregas/{entrega_ana}/calificacion", headers=doc["h"], json={"puntaje": 17, "comentario": "Bien"})
    assert r.status_code == 200

    # Beto no ve la entrega, el archivo ni la nota de Ana
    assert (await cliente.get(f"/entregas/{entrega_ana}", headers=beto["h"])).status_code == 404
    assert (await cliente.get(f"/entregas/{entrega_ana}/archivo", headers=beto["h"])).status_code == 404
    assert (await cliente.get(f"/tareas/{tarea['id']}/entregas", headers=beto["h"])).status_code == 403
    assert (await cliente.put(f"/entregas/{entrega_ana}/calificacion", headers=beto["h"], json={"puntaje": 0})).status_code == 404
    mia = (await cliente.get(f"/tareas/{tarea['id']}/entrega", headers=beto["h"])).json()
    assert mia["texto"] == "Lo de Beto" and mia["calificacion"] is None
    notas = (await cliente.get(f"/clases/{cid}/notas", headers=beto["h"])).json()
    assert [e["id"] for e in notas["estudiantes"]] == [beto["id"]]
    assert "Texto secreto de Ana" not in (await cliente.get(f"/clases/{cid}/notas", headers=beto["h"])).text
    assert (await cliente.get(f"/clases/{cid}/notas?formato=csv", headers=beto["h"])).status_code == 403
    # el estudiante solo ve a los docentes, sin correos
    miembros = (await cliente.get(f"/clases/{cid}/miembros", headers=beto["h"])).json()
    assert {m["rol"] for m in miembros} == {"docente"} and all(m["correo"] is None for m in miembros)

    # Ana sí ve lo suyo con la nota; el docente ve todo
    mia = (await cliente.get(f"/tareas/{tarea['id']}/entrega", headers=ana["h"])).json()
    assert mia["calificacion"]["puntaje"] == 17
    assert len((await cliente.get(f"/tareas/{tarea['id']}/entregas", headers=doc["h"])).json()) == 2
    libro = (await cliente.get(f"/clases/{cid}/notas", headers=doc["h"])).json()
    assert {e["id"] for e in libro["estudiantes"]} == {ana["id"], beto["id"]}
    csv = await cliente.get(f"/clases/{cid}/notas?formato=csv", headers=doc["h"])
    assert csv.status_code == 200 and "Ana Prueba" in csv.text


async def test_docente_de_otra_clase_no_ve_nada(cliente, aula):
    otro = await registrar(cliente, "otro-docente@ejemplo.test")
    await hacer_docente(otro["id"])
    await cliente.post("/clases", headers=otro["h"], json={"nombre": "Otra", "curso_id": "python", "pub": "numerus-scriptum"})
    cid = aula["clase"]["id"]
    tarea = (await cliente.post(f"/clases/{cid}/tareas", headers=aula["docente"]["h"], json={"titulo": "T1"})).json()
    entrega = (await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=aula["ana"]["h"], data={"texto": "x"})).json()
    assert (await cliente.get(f"/tareas/{tarea['id']}/entregas", headers=otro["h"])).status_code == 404
    assert (await cliente.get(f"/entregas/{entrega['id']}", headers=otro["h"])).status_code == 404


async def test_rubrica_y_puntaje_maximo(cliente, aula):
    cid, doc = aula["clase"]["id"], aula["docente"]
    rubrica = [{"criterio": "argumento", "puntos": 12}, {"criterio": "redaccion", "puntos": 8}]
    r = await cliente.post(f"/clases/{cid}/tareas", headers=doc["h"], json={"titulo": "Con rúbrica", "puntaje_max": 10, "rubrica": rubrica})
    assert r.status_code == 422  # la rúbrica suma 20 > 10
    tarea = (await cliente.post(f"/clases/{cid}/tareas", headers=doc["h"], json={"titulo": "Con rúbrica", "puntaje_max": 20, "rubrica": rubrica})).json()
    e = (await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=aula["ana"]["h"], data={"texto": "x"})).json()
    url = f"/entregas/{e['id']}/calificacion"
    assert (await cliente.put(url, headers=doc["h"], json={"puntaje": 15})).status_code == 422
    assert (await cliente.put(url, headers=doc["h"], json={"por_criterio": {"argumento": 13, "redaccion": 1}})).status_code == 422
    r = await cliente.put(url, headers=doc["h"], json={"por_criterio": {"argumento": 10, "redaccion": 6.5}, "comentario": "Claro"})
    assert r.status_code == 200 and r.json()["calificacion"]["puntaje"] == 16.5
    # ya calificada: Ana no puede reemplazarla
    assert (await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=aula["ana"]["h"], data={"texto": "y"})).status_code == 409


async def test_tarea_no_publicada_no_la_ve_el_estudiante(cliente, aula):
    cid = aula["clase"]["id"]
    t = (await cliente.post(f"/clases/{cid}/tareas", headers=aula["docente"]["h"], json={"titulo": "Borrador", "publicada": False})).json()
    assert (await cliente.get(f"/tareas/{t['id']}", headers=aula["ana"]["h"])).status_code == 404
    assert (await cliente.get(f"/clases/{cid}/tareas", headers=aula["ana"]["h"])).json() == []


async def test_anuncios_y_retiro(cliente, aula):
    cid, doc, ana = aula["clase"]["id"], aula["docente"], aula["ana"]
    r = await cliente.post(f"/clases/{cid}/anuncios", headers=doc["h"], json={"texto": "Bienvenidos"})
    assert r.status_code == 201
    assert (await cliente.get(f"/clases/{cid}/anuncios", headers=ana["h"])).json()[0]["texto"] == "Bienvenidos"
    assert (await cliente.delete(f"/anuncios/{r.json()['id']}", headers=ana["h"])).status_code == 403
    # Ana no puede retirar a Beto; sí salir ella; el único docente no puede irse
    assert (await cliente.delete(f"/clases/{cid}/miembros/{aula['beto']['id']}", headers=ana["h"])).status_code == 403
    assert (await cliente.delete(f"/clases/{cid}/miembros/{doc['id']}", headers=doc["h"])).status_code == 409
    assert (await cliente.delete(f"/clases/{cid}/miembros/{ana['id']}", headers=ana["h"])).status_code == 204
    assert (await cliente.get(f"/clases/{cid}", headers=ana["h"])).status_code == 404


async def test_codigo_equivocado_tiene_limite(cliente):
    e = await registrar(cliente, "adivina@ejemplo.test")
    for _ in range(5):
        assert (await cliente.post("/clases/inscribirse", headers=e["h"], json={"codigo": "ZZZZZZZ"})).status_code == 404
    assert (await cliente.post("/clases/inscribirse", headers=e["h"], json={"codigo": "ZZZZZZZ"})).status_code == 429
