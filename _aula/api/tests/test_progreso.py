"""api/tests/test_progreso.py — sincronización del progreso de lecciones con `aula:<pub>:completadas`."""

import pytest

from tests.conftest import registrar

pytestmark = pytest.mark.anyio


async def test_fusion_union_fecha_mas_antigua_y_desmarcar(cliente):
    u = await registrar(cliente, "lee@ejemplo.test")
    url, h = "/progreso/numerus-scriptum", u["h"]
    r = await cliente.put(url, headers=h, json={"completadas": {"python/variables": "2026-10-05", "python/listas": "2026-10-06"}})
    assert r.json()["completadas"] == {"python/listas": "2026-10-06", "python/variables": "2026-10-05"}
    # otro dispositivo: una fecha más antigua gana, una nueva se suma, null desmarca
    r = await cliente.put(url, headers=h, json={"completadas": {"python/variables": "2026-10-01", "python/bucles": "2026-10-07", "python/listas": None}})
    assert r.json()["completadas"] == {"python/bucles": "2026-10-07", "python/variables": "2026-10-01"}
    r = await cliente.put(url, headers=h, json={"completadas": {"python/variables": "2026-10-09"}})
    assert r.json()["completadas"]["python/variables"] == "2026-10-01"
    assert (await cliente.get(url, headers=h)).json() == r.json()
    assert (await cliente.get("/progreso/methodica", headers=h)).json() == {"completadas": {}}


async def test_progreso_es_de_cada_quien(cliente):
    a = await registrar(cliente, "a@ejemplo.test")
    b = await registrar(cliente, "b@ejemplo.test")
    await cliente.put("/progreso/methodica", headers=a["h"], json={"completadas": {"curso/leccion": "2026-10-01"}})
    assert (await cliente.get("/progreso/methodica", headers=b["h"])).json() == {"completadas": {}}
    assert (await cliente.get("/progreso/methodica")).status_code == 401


@pytest.mark.parametrize("cuerpo", [
    {"completadas": {"sin-barra": "2026-10-01"}},
    {"completadas": {"curso/leccion": "01/10/2026"}},
    {"completadas": {"../etc/passwd": "2026-10-01"}},
])
async def test_entradas_invalidas(cliente, cuerpo):
    u = await registrar(cliente, "mal@ejemplo.test")
    assert (await cliente.put("/progreso/methodica", headers=u["h"], json=cuerpo)).status_code == 422
    assert (await cliente.put("/progreso/Pub_Raro", headers=u["h"], json={"completadas": {}})).status_code == 422
