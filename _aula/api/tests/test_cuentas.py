"""api/tests/test_cuentas.py — registro con consentimiento, Argon2id, sesión, renovación rotativa y límite de intentos."""

from datetime import timedelta

import pytest

from aula import db, tiempo
from aula.config import config
from aula.modelos import Usuario
from tests.conftest import CLAVE, registrar

pytestmark = pytest.mark.anyio


async def test_registro_exige_consentimiento_y_politica_vigente(cliente):
    base = {"correo": "x@ejemplo.test", "nombre_visible": "Equis", "clave": CLAVE, "politica_version": config.politica_version,
            "tengo_14_o_mas": True}
    r = await cliente.post("/cuentas/registro", json={**base, "consentimiento": False})
    assert r.status_code == 422
    r = await cliente.post("/cuentas/registro", json={**base, "consentimiento": True, "tengo_14_o_mas": False})
    assert r.status_code == 422 and "tutor" in r.json()["detail"]
    r = await cliente.post("/cuentas/registro", json={**base, "consentimiento": True, "politica_version": "2000-01-01"})
    assert r.status_code == 409
    r = await cliente.post("/cuentas/registro", json={**base, "consentimiento": True, "clave": "corta"})
    assert r.status_code == 422
    r = await cliente.post("/cuentas/registro", json={**base, "consentimiento": True})
    assert r.status_code == 201
    assert r.json()["usuario"]["rol_global"] == "estudiante"
    r = await cliente.post("/cuentas/registro", json={**base, "consentimiento": True, "correo": "X@Ejemplo.test"})
    assert r.status_code == 409  # el correo se normaliza a minúsculas


async def test_clave_se_guarda_con_argon2id_y_consentimiento_con_fecha(cliente):
    u = await registrar(cliente, "hash@ejemplo.test")
    async with db.fabrica()() as sesion:
        fila = await sesion.get(Usuario, u["id"])
        assert fila.clave_hash.startswith("$argon2id$")
        assert CLAVE not in fila.clave_hash
        assert fila.consentimiento_version == config.politica_version and fila.consentimiento_en is not None


async def test_sesion_y_yo(cliente):
    await registrar(cliente, "yo@ejemplo.test", "Yo Mismo")
    r = await cliente.post("/cuentas/sesion", json={"correo": "YO@ejemplo.test", "clave": CLAVE})
    assert r.status_code == 200
    h = {"Authorization": f"Bearer {r.json()['acceso']}"}
    r = await cliente.get("/cuentas/yo", headers=h)
    assert r.status_code == 200 and r.json()["nombre_visible"] == "Yo Mismo"
    assert (await cliente.get("/cuentas/yo")).status_code == 401
    assert (await cliente.get("/cuentas/yo", headers={"Authorization": "Bearer x.y.z"})).status_code == 401


async def test_acceso_vencido(cliente, monkeypatch):
    await registrar(cliente, "viejo@ejemplo.test")
    pasado = tiempo.ahora() - timedelta(hours=2)
    monkeypatch.setattr(tiempo, "ahora", lambda: pasado)
    r = await cliente.post("/cuentas/sesion", json={"correo": "viejo@ejemplo.test", "clave": CLAVE})
    monkeypatch.undo()
    assert r.status_code == 200
    r = await cliente.get("/cuentas/yo", headers={"Authorization": f"Bearer {r.json()['acceso']}"})
    assert r.status_code == 401


async def test_limite_de_intentos_de_sesion(cliente):
    await registrar(cliente, "lim@ejemplo.test")
    for _ in range(config.intentos_sesion):
        r = await cliente.post("/cuentas/sesion", json={"correo": "lim@ejemplo.test", "clave": "equivocada-123"})
        assert r.status_code == 401
    r = await cliente.post("/cuentas/sesion", json={"correo": "lim@ejemplo.test", "clave": CLAVE})
    assert r.status_code == 429  # bloqueado aunque ahora acierte
    assert int(r.headers["Retry-After"]) > 0
    # el bloqueo es por correo: otra cuenta entra
    await registrar(cliente, "otra@ejemplo.test")
    r = await cliente.post("/cuentas/sesion", json={"correo": "otra@ejemplo.test", "clave": CLAVE})
    assert r.status_code == 200


async def test_correo_inexistente_responde_igual(cliente):
    r = await cliente.post("/cuentas/sesion", json={"correo": "nadie@ejemplo.test", "clave": CLAVE})
    assert r.status_code == 401 and r.json()["detail"] == "Correo o contraseña incorrectos."


async def test_renovacion_rota_y_detecta_reuso(cliente):
    u = await registrar(cliente, "rota@ejemplo.test")
    r = await cliente.post("/cuentas/renovar", json={"renovacion": u["renovacion"]})
    assert r.status_code == 200
    nueva = r.json()["renovacion"]
    assert nueva != u["renovacion"]
    # reusar la vieja (robada) revoca también la nueva
    assert (await cliente.post("/cuentas/renovar", json={"renovacion": u["renovacion"]})).status_code == 401
    assert (await cliente.post("/cuentas/renovar", json={"renovacion": nueva})).status_code == 401


async def test_salir_revoca(cliente):
    u = await registrar(cliente, "sale@ejemplo.test")
    assert (await cliente.post("/cuentas/salir", json={"renovacion": u["renovacion"]})).status_code == 204
    assert (await cliente.post("/cuentas/renovar", json={"renovacion": u["renovacion"]})).status_code == 401


async def test_cambiar_clave_pide_la_actual_y_cierra_sesiones(cliente):
    u = await registrar(cliente, "cambia@ejemplo.test")
    r = await cliente.patch("/cuentas/yo", headers=u["h"], json={"clave_actual": "mala-mala-mala", "clave_nueva": "otra-clave-larga"})
    assert r.status_code == 403
    r = await cliente.patch("/cuentas/yo", headers=u["h"], json={"clave_actual": CLAVE, "clave_nueva": "otra-clave-larga"})
    assert r.status_code == 200
    assert (await cliente.post("/cuentas/renovar", json={"renovacion": u["renovacion"]})).status_code == 401
    r = await cliente.post("/cuentas/sesion", json={"correo": "cambia@ejemplo.test", "clave": "otra-clave-larga"})
    assert r.status_code == 200


async def test_cuenta_de_menor_la_crea_el_docente(base, capsys):
    """Menor de 14 años: no se registra solo (422 arriba); el docente crea la cuenta con el consentimiento del tutor."""
    from aula import cli

    assert await cli._cuenta("Menor@Ejemplo.test", "Menor Ficticio", aplicar=False) == 0
    assert "[simulación]" in capsys.readouterr().out
    assert await cli._cuenta("menor@ejemplo.test", "Menor Ficticio", aplicar=True) == 0
    assert "contraseña temporal" in capsys.readouterr().out
    assert await cli._cuenta("menor@ejemplo.test", "Menor Ficticio", aplicar=True) == 1
