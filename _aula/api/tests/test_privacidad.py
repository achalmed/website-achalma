"""api/tests/test_privacidad.py — derechos sobre los datos propios: exportarlos y borrarlos (Ley 29733)."""

from pathlib import Path

import pytest

from aula.config import config
from tests.conftest import CLAVE, hacer_docente, registrar

pytestmark = pytest.mark.anyio


async def _con_datos(cliente, aula):
    cid = aula["clase"]["id"]
    tarea = (await cliente.post(f"/clases/{cid}/tareas", headers=aula["docente"]["h"], json={"titulo": "Informe"})).json()
    await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=aula["ana"]["h"], data={"texto": "Texto de Ana"},
                      files={"archivo": ("a.txt", b"archivo de ana", "text/plain")})
    await cliente.put(f"/tareas/{tarea['id']}/entrega", headers=aula["beto"]["h"], data={"texto": "Texto de Beto"},
                      files={"archivo": ("b.txt", b"archivo de beto", "text/plain")})
    await cliente.put("/progreso/methodica", headers=aula["ana"]["h"], json={"completadas": {"metodologia-investigacion/el-metodo": "2026-10-01"}})
    return tarea


async def test_politica_publica(cliente):
    r = await cliente.get("/privacidad")
    assert r.status_code == 200 and r.json()["version"] == config.politica_version and "29733" in r.json()["ley"]
    assert r.json()["edad_minima"] == 14 and "contacto" in r.json()


async def test_exportar_solo_lo_propio(cliente, aula):
    await _con_datos(cliente, aula)
    r = await cliente.get("/cuentas/yo/datos", headers=aula["ana"]["h"])
    assert r.status_code == 200
    datos = r.json()
    assert datos["cuenta"]["correo"] == "ana@ejemplo.test"
    assert datos["cuenta"]["consentimiento"]["version"] == config.politica_version
    assert datos["entregas"][0]["texto"] == "Texto de Ana" and datos["entregas"][0]["archivo"]["descarga"]
    assert datos["progreso"] == {"methodica": {"metodologia-investigacion/el-metodo": "2026-10-01"}}
    assert datos["clases"][0]["rol"] == "estudiante"
    assert "Texto de Beto" not in r.text and "beto@" not in r.text and "argon2" not in r.text


async def test_borrar_la_cuenta_se_lleva_todo_lo_suyo(cliente, aula):
    await _con_datos(cliente, aula)
    raiz = Path(config.datos_dir)
    assert len(list(raiz.rglob("*.txt"))) == 2
    assert (await cliente.request("DELETE", "/cuentas/yo", headers=aula["ana"]["h"], json={"clave": "no-es-la-clave"})).status_code == 403
    assert (await cliente.request("DELETE", "/cuentas/yo", headers=aula["ana"]["h"], json={"clave": CLAVE})).status_code == 204
    restantes = list(raiz.rglob("*.txt"))
    assert len(restantes) == 1 and restantes[0].read_bytes() == b"archivo de beto"
    assert (await cliente.post("/cuentas/sesion", json={"correo": "ana@ejemplo.test", "clave": CLAVE})).status_code == 401
    assert (await cliente.get("/cuentas/yo", headers=aula["ana"]["h"])).status_code == 401  # el token ya no vale
    # lo de los demás sigue
    cid = aula["clase"]["id"]
    libro = (await cliente.get(f"/clases/{cid}/notas", headers=aula["docente"]["h"])).json()
    assert [e["id"] for e in libro["estudiantes"]] == [aula["beto"]["id"]]
    # el correo queda libre para volver a registrarse
    await registrar(cliente, "ana@ejemplo.test")


async def test_unico_docente_con_estudiantes_no_puede_borrarse(cliente, aula):
    r = await cliente.request("DELETE", "/cuentas/yo", headers=aula["docente"]["h"], json={"clave": CLAVE})
    assert r.status_code == 409
    # con un co-docente, sí; sus anuncios quedan sin autor
    cid = aula["clase"]["id"]
    await cliente.post(f"/clases/{cid}/anuncios", headers=aula["docente"]["h"], json={"texto": "Aviso"})
    co = await registrar(cliente, "co@ejemplo.test", "Co Docente")
    assert (await cliente.post(f"/clases/{cid}/docentes", headers=aula["docente"]["h"], json={"correo": "co@ejemplo.test"})).status_code == 201
    assert (await cliente.request("DELETE", "/cuentas/yo", headers=aula["docente"]["h"], json={"clave": CLAVE})).status_code == 204
    anuncios = (await cliente.get(f"/clases/{cid}/anuncios", headers=co["h"])).json()
    assert anuncios[0]["autor"] is None and anuncios[0]["texto"] == "Aviso"


async def test_docente_con_clase_vacia_se_borra_con_ella(cliente):
    d = await registrar(cliente, "solo@ejemplo.test")
    await hacer_docente(d["id"])
    clase = (await cliente.post("/clases", headers=d["h"], json={"nombre": "Vacía", "curso_id": "python", "pub": "numerus-scriptum"})).json()
    assert (await cliente.request("DELETE", "/cuentas/yo", headers=d["h"], json={"clave": CLAVE})).status_code == 204
    otro = await registrar(cliente, "mira@ejemplo.test")
    assert (await cliente.post("/clases/inscribirse", headers=otro["h"], json={"codigo": clase["codigo"]})).status_code == 404
