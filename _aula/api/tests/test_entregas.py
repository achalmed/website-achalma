"""api/tests/test_entregas.py — archivos de entregas: fuera del repo, límite de tamaño, tipos permitidos y reemplazo."""

import stat
from datetime import timedelta
from pathlib import Path

import pytest

from aula import archivos, tiempo
from aula.config import config

pytestmark = pytest.mark.anyio


async def _tarea(cliente, aula, **extra):
    cid = aula["clase"]["id"]
    r = await cliente.post(f"/clases/{cid}/tareas", headers=aula["docente"]["h"], json={"titulo": "Informe", **extra})
    assert r.status_code == 201, r.text
    return r.json()


def _archivos_guardados() -> list[Path]:
    raiz = Path(config.datos_dir)
    return [p for p in raiz.rglob("*") if p.is_file()] if raiz.exists() else []


async def test_archivo_se_guarda_fuera_del_repo_y_se_descarga(cliente, aula):
    t = await _tarea(cliente, aula)
    contenido = b"%PDF-1.4 contenido ficticio"
    r = await cliente.put(f"/tareas/{t['id']}/entrega", headers=aula["ana"]["h"], files={"archivo": ("Mi informe final.pdf", contenido, "application/pdf")})
    assert r.status_code == 200, r.text
    assert r.json()["archivo_nombre"] == "Mi informe final.pdf" and r.json()["archivo_bytes"] == len(contenido)
    guardados = _archivos_guardados()
    assert len(guardados) == 1 and archivos.dentro_de_repo(guardados[0]) is None
    assert stat.S_IMODE(guardados[0].stat().st_mode) == 0o600
    assert "informe" not in guardados[0].name  # el nombre original no se usa como ruta
    d = await cliente.get(f"/entregas/{r.json()['id']}/archivo", headers=aula["docente"]["h"])
    assert d.status_code == 200 and d.content == contenido
    assert d.headers["content-type"] == "application/octet-stream" and "attachment" in d.headers["content-disposition"]


async def test_limite_de_tamano(cliente, aula, monkeypatch):
    monkeypatch.setattr(config, "max_archivo_mb", 1)
    t = await _tarea(cliente, aula)
    url, h = f"/tareas/{t['id']}/entrega", aula["ana"]["h"]
    # muy por encima: lo corta el intermedio por Content-Length
    r = await cliente.put(url, headers=h, files={"archivo": ("grande.pdf", b"0" * (2 * 1024 * 1024), "application/pdf")})
    assert r.status_code == 413
    # apenas por encima (dentro del margen del formulario): lo corta la escritura por trozos y no deja restos
    r = await cliente.put(url, headers=h, files={"archivo": ("justo.pdf", b"0" * (1024 * 1024 + 10), "application/pdf")})
    assert r.status_code == 413
    assert _archivos_guardados() == []
    r = await cliente.put(url, headers=h, files={"archivo": ("cabe.pdf", b"0" * (1024 * 1024), "application/pdf")})
    assert r.status_code == 200


async def test_tipos_no_permitidos_y_entrega_vacia(cliente, aula):
    t = await _tarea(cliente, aula)
    url, h = f"/tareas/{t['id']}/entrega", aula["ana"]["h"]
    for nombre in ("virus.exe", "pagina.html", "dibujo.svg", "sin-extension"):
        r = await cliente.put(url, headers=h, files={"archivo": (nombre, b"x", "application/octet-stream")})
        assert r.status_code == 415, nombre
    assert (await cliente.put(url, headers=h, data={"texto": "   "})).status_code == 422
    assert (await cliente.put(url, headers=h, files={"archivo": ("vacio.txt", b"", "text/plain")})).status_code == 422
    assert _archivos_guardados() == []


async def test_reentrega_reemplaza_el_archivo_y_marca_tardia(cliente, aula, monkeypatch):
    t = await _tarea(cliente, aula, fecha_limite=(tiempo.ahora() + timedelta(days=1)).isoformat())
    url, h = f"/tareas/{t['id']}/entrega", aula["ana"]["h"]
    r1 = await cliente.put(url, headers=h, files={"archivo": ("v1.txt", b"uno", "text/plain")})
    assert r1.json()["tardia"] is False
    futuro = tiempo.ahora() + timedelta(days=2)
    monkeypatch.setattr(tiempo, "ahora", lambda: futuro)
    r2 = await cliente.put(url, headers=h, files={"archivo": ("v2.txt", b"dos", "text/plain")})
    assert r2.json()["id"] == r1.json()["id"] and r2.json()["tardia"] is True
    guardados = _archivos_guardados()
    assert len(guardados) == 1 and guardados[0].read_bytes() == b"dos"


async def test_tarea_que_no_acepta_archivo(cliente, aula):
    t = await _tarea(cliente, aula, acepta_archivo=False)
    r = await cliente.put(f"/tareas/{t['id']}/entrega", headers=aula["ana"]["h"], files={"archivo": ("a.txt", b"x", "text/plain")})
    assert r.status_code == 422


async def test_el_docente_no_entrega(cliente, aula):
    t = await _tarea(cliente, aula)
    assert (await cliente.put(f"/tareas/{t['id']}/entrega", headers=aula["docente"]["h"], data={"texto": "x"})).status_code == 403


def test_datos_dentro_de_un_repo_se_rechazan(tmp_path, monkeypatch):
    (tmp_path / "repo" / ".git").mkdir(parents=True)
    monkeypatch.setattr(config, "datos_dir", str(tmp_path / "repo" / "datos"))
    with pytest.raises(archivos.DatosEnRepo):
        archivos.raiz_datos()
    monkeypatch.setattr(config, "datos_dir", str(tmp_path / "fuera"))
    assert archivos.raiz_datos().exists()


def test_el_defecto_de_datos_esta_fuera_del_repo():
    from aula.config import _datos_por_defecto

    assert archivos.dentro_de_repo(Path(_datos_por_defecto())) is None
