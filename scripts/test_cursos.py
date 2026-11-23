"""Pruebas de `cursos.py` con la propuesta de lección de docencia (plan «aprender y enseñar», fase 4.3).

    python3 -m pytest scripts/test_cursos.py -q

Arma en una carpeta temporal un ecosistema de juguete (un curso de docencia con su banco, un apunte que declara un
tema y un pub con git) y corre `cursos.py` de verdad, con --aplicar: no toca `web/_pubs` ni `docencia` reales. Toma de
docencia (CLASS_DIR) `areas.py`, `alineamiento.py`, `leccion.py`, `config/areas.yml` y `mapa-lecciones.py`; si falta
alguno, se salta.
"""
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

AQUI = Path(__file__).resolve().parent
_d = AQUI
while _d != _d.parent and not (_d / "core" / "env.py").is_file():
    _d = _d.parent
_s = importlib.util.spec_from_file_location("core_env_test_cursos", _d / "core" / "env.py")
env = importlib.util.module_from_spec(_s)
_s.loader.exec_module(env)
CLASE = Path(os.environ.get("CLASS_DIR") or env.CLASS_DIR)
NECESARIOS = [CLASE / "scripts" / x for x in ("areas.py", "alineamiento.py", "leccion.py")] + [
    CLASE / "config" / "areas.yml", CLASE / "contenido" / "migracion" / "mapa-lecciones.py"]
pytestmark = pytest.mark.skipif(not all(p.is_file() for p in NECESARIOS),
                                reason="falta docencia con leccion.py y mapa-lecciones.py (CLASS_DIR)")
CENTINELA = "FRASE-DEL-APUNTE-QUE-NO-SE-COPIA"


@pytest.fixture
def eco(tmp_path):
    (tmp_path / "core").symlink_to(_d / "core")
    if (_d / "meta").exists():
        (tmp_path / "meta").symlink_to(_d / "meta")
    sc = tmp_path / "docencia" / "scripts"
    sc.mkdir(parents=True)
    for x in ("areas.py", "alineamiento.py"):
        shutil.copy(CLASE / "scripts" / x, sc / x)             # leccion.py entra después: primero, sin propuesta
    (tmp_path / "docencia" / "config").mkdir()
    shutil.copy(CLASE / "config" / "areas.yml", tmp_path / "docencia" / "config" / "areas.yml")
    mig = tmp_path / "docencia" / "contenido" / "migracion"
    mig.mkdir(parents=True)
    shutil.copy(CLASE / "contenido" / "migracion" / "mapa-lecciones.py", mig / "mapa-lecciones.py")
    k = tmp_path / "docencia" / "contenido" / "cursos" / "curso-juguete"
    s = k / "03-sesiones" / "s01-uno"
    s.mkdir(parents=True)
    (k / "curso.yml").write_text(yaml.safe_dump({
        "id": "curso-juguete", "titulo": "Curso de juguete", "temario": "revisado", "area": ["estadistica-econometria"],
        "unidades": [{"id": 1, "titulo": "Uno", "temas": [
            {"id": "1.1", "titulo": "Regresión simple", "archivo": None},
            {"id": "1.2", "titulo": "Mínimos cuadrados", "archivo": None},
            {"id": "1.3", "titulo": "Sin nada", "archivo": None}]}],
        "alineamiento": {"resultados": [{"id": "ra1", "nivel": "relacional", "enunciado": "Interpreta la pendiente."}]},
    }, allow_unicode=True), encoding="utf-8")
    (s / "sesion.yml").write_text(yaml.safe_dump({"id": "s01-uno", "titulo": "Uno", "tipo": "laboratorio"}), encoding="utf-8")
    (s / "recuperacion.yml").write_text(yaml.safe_dump({"sesion": "s01-uno", "preguntas": [
        {"id": "s01-p01", "resultado": "ra1", "tema": "1.1", "tipo": "vf", "enunciado": "Puede ser negativa.", "respuesta": True},
        {"id": "s01-p02", "resultado": "ra1", "tema": "1.2", "tipo": "abierta", "enunciado": "¿Por qué cuadrados?",
         "respuesta": "Por la solución cerrada"}]}, allow_unicode=True), encoding="utf-8")
    apunte = tmp_path / "notas" / "40-cursos-y-formacion" / "autoestudio" / "apunte-01.md"
    apunte.parent.mkdir(parents=True)
    apunte.write_text("\n".join(["---", "titulo: Apunte", "calibre_id: 501", "---", "", "## 1. La recta", "", CENTINELA, "",
                                 "- Curso anfitrión: [1 1 regresion](<../../../docencia/contenido/cursos/curso-juguete>)", ""]),
                      encoding="utf-8")
    web = tmp_path / "web"
    (web / "scripts").mkdir(parents=True)
    shutil.copy(AQUI / "cursos.py", web / "scripts" / "cursos.py")
    pub = web / "_pubs" / "epsilon-y-beta"
    (pub / "01-sec" / "2021-01-01-patron").mkdir(parents=True)
    (pub / "01-sec" / "2021-01-01-patron" / "index.qmd").write_text(
        "---\ntitle: Patrón\ndraft: true\n---\n\nEste artículo está actualmente en proceso de edición, y todas las secciones "
        "serán ampliadas y refinadas en futuras revisiones.\n\n{{< include ../_x.qmd >}}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(pub), "init", "-q"], check=True)
    return tmp_path


def cursos(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    entorno = {k: v for k, v in os.environ.items() if not k.endswith("_DIR")} | {
        "DOCS_ROOT": str(raiz), "CALIBRE_DB": str(raiz / "no-hay.db")}
    return subprocess.run([sys.executable, str(raiz / "web" / "scripts" / "cursos.py"), *args, "--curso", "curso-juguete"],
                          capture_output=True, text=True, env=entorno)


def leccion(raiz: Path, n: str) -> Path:
    [q] = (raiz / "web" / "_pubs" / "epsilon-y-beta" / "curso-juguete").glob(f"*-{n}-*/index.qmd")
    return q


def fm(q: Path) -> dict:
    return yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", q.read_text(encoding="utf-8"), re.S).group(1))


def huellas(raiz: Path) -> dict:
    return {q: hashlib.sha256(q.read_bytes()).hexdigest() for q in (raiz / "web" / "_pubs").rglob("index.qmd")}


def palabras(raiz: Path, q: Path) -> int:
    s = importlib.util.spec_from_file_location("mapa_test", raiz / "docencia" / "contenido" / "migracion" / "mapa-lecciones.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.leer_post(q)["palabras"]


def test_sin_leccion_py_los_esqueletos_nacen_vacios_y_con_ella_se_rellenan(eco):
    r = cursos(eco, "--aplicar")
    assert r.returncode == 0, r.stdout + r.stderr
    q1 = leccion(eco, "01")
    assert "Propuesta" not in q1.read_text(encoding="utf-8") and "quiz" not in fm(q1)
    shutil.copy(CLASE / "scripts" / "leccion.py", eco / "docencia" / "scripts" / "leccion.py")
    antes = huellas(eco)
    r = cursos(eco)                                             # simula: no escribe
    assert "propuestas 2 · quiz 1" in r.stdout, r.stdout + r.stderr
    assert huellas(eco) == antes
    r = cursos(eco, "--aplicar")
    assert r.returncode == 0, r.stdout + r.stderr
    texto = q1.read_text(encoding="utf-8")
    assert "<!-- Propuesta:" in texto and "ra1 (relacional)" in texto and "La recta" in texto
    assert CENTINELA not in texto                               # del apunte salen sus encabezados, no su texto
    f = fm(q1)
    assert f["quiz"] == [{"id": "s01-p01", "tipo": "vf", "enunciado": "Puede ser negativa.", "respuesta": True}]
    assert f["quiz_origen"].startswith("docencia/scripts/alineamiento.py exportar curso-juguete s01")
    assert f["propuesta"] and f["draft"] is True and f["tema"] == "1.1"
    assert palabras(eco, q1) == 0                               # todo en comentarios: el mapa la sigue viendo vacía
    assert "Propuesta" not in leccion(eco, "03").read_text(encoding="utf-8")   # un tema sin nada queda vacío
    r = cursos(eco, "--aplicar")                                # idempotente
    assert "propuestas 0 · quiz 0" in r.stdout
    assert cursos(eco, "verificar").returncode == 0


def test_lo_que_toco_el_autor_no_se_rehace_y_el_quiz_sigue_al_banco(eco):
    shutil.copy(CLASE / "scripts" / "leccion.py", eco / "docencia" / "scripts" / "leccion.py")
    assert cursos(eco, "--aplicar").returncode == 0
    q2 = leccion(eco, "02")
    q2.write_text(q2.read_text(encoding="utf-8").replace("Escribe de tres a cinco", "MI NOTA. Escribe de tres a cinco"),
                  encoding="utf-8")
    banco = eco / "docencia" / "contenido" / "cursos" / "curso-juguete" / "03-sesiones" / "s01-uno" / "recuperacion.yml"
    b = yaml.safe_load(banco.read_text(encoding="utf-8"))
    b["preguntas"][0]["tema"] = "1.3"                           # la vf deja el tema 1.1
    banco.write_text(yaml.safe_dump(b, allow_unicode=True), encoding="utf-8")
    r = cursos(eco, "--aplicar")
    assert "tiene comentarios o cambios del autor; no se rellena" in r.stdout
    assert "MI NOTA" in q2.read_text(encoding="utf-8")
    q1, q3 = leccion(eco, "01"), leccion(eco, "03")
    assert "quiz" not in fm(q1) and "quiz_origen" not in fm(q1)  # el banco ya no tiene preguntas del 1.1
    assert [x["id"] for x in fm(q3)["quiz"]] == ["s01-p01"]      # y el 1.3 la recibe, con su propuesta
    assert "<!-- Propuesta:" in q3.read_text(encoding="utf-8")
