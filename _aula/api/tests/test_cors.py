"""api/tests/test_cors.py — origen cruzado: solo los 13 sitios de pubs.yml (el hub y los 12 pubs), sus vistas previas de Netlify y localhost."""

import pytest

from aula import origenes

pytestmark = pytest.mark.anyio


async def _preflight(cliente, origen):
    return await cliente.options("/cuentas/sesion", headers={
        "Origin": origen, "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "authorization,content-type",
    })


@pytest.mark.parametrize("origen", [
    "https://methodica.netlify.app",
    "https://achalmaedison.netlify.app",
    "https://chaska-x.netlify.app",
    "https://deploy-preview-12--methodica.netlify.app",
    "http://127.0.0.1:4331",
    "http://localhost:4321",
])
async def test_origenes_permitidos(cliente, origen):
    r = await _preflight(cliente, origen)
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == origen
    assert "access-control-allow-credentials" not in r.headers  # sin cookies
    assert "authorization" in r.headers["access-control-allow-headers"].lower()


@pytest.mark.parametrize("origen", [
    "https://malicioso.example",
    "https://methodica.netlify.app.malicioso.example",
    "https://otro-sitio.netlify.app",
    "https://x--y--methodica.netlify.app",
    "http://methodica.netlify.app",
    "https://chaska.netlify.app",
])
async def test_origenes_rechazados(cliente, origen):
    r = await _preflight(cliente, origen)
    assert r.status_code == 400
    assert "access-control-allow-origin" not in r.headers
    r = await cliente.get("/salud", headers={"Origin": origen})
    assert "access-control-allow-origin" not in r.headers


async def test_peticion_simple_lleva_el_origen(cliente):
    r = await cliente.get("/salud", headers={"Origin": "https://numerus-scriptum.netlify.app"})
    assert r.headers["access-control-allow-origin"] == "https://numerus-scriptum.netlify.app"
    assert r.headers["x-content-type-options"] == "nosniff"


def test_lista_generada_al_dia_con_pubs_yml():
    try:
        calculado = origenes.calcular()
    except FileNotFoundError:
        pytest.skip("web/_pubs/pubs.yml no está a la vista (contenedor)")
    assert origenes.cargar() == calculado, "python -m aula.origenes --aplicar"
    assert len(calculado["origenes"]) == 13
