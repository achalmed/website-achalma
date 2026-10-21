"""api/aula/origenes.py — la lista blanca de CORS: los 12 sitios de web/_pubs/pubs.yml, más localhost para desarrollo.

`python -m aula.origenes` simula (muestra la lista y si el archivo está al día); `--aplicar` escribe
`aula/origenes.generado.json`; `--verificar` sale 1 si el archivo no coincide con `pubs.yml`. La API lee el JSON
generado (no `pubs.yml`), para que también arranque en un contenedor que no ve el hub.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

GENERADO = Path(__file__).with_name("origenes.generado.json")
AVISO = "GENERADO por `python -m aula.origenes --aplicar` desde web/_pubs/pubs.yml; no editar"
# Vistas previas y despliegues por rama de Netlify del mismo sitio: https://<algo>--<sitio>.netlify.app
_PLANTILLA_PREVIA = r"https://[a-z0-9]+(?:-[a-z0-9]+)*--{sitio}\.netlify\.app"
LOCAL = r"http://(localhost|127\.0\.0\.1)(:\d{1,5})?"


def _pubs_yml() -> Path:
    """web/_pubs/pubs.yml por INDEX_DIR (core/env.py) o, si no está, por la posición de este archivo en el hub."""
    raiz = Path(__file__).resolve()
    for carpeta in raiz.parents:
        if (carpeta / "core" / "env.py").exists():
            sys.path.insert(0, str(carpeta / "core"))
            try:
                import env  # type: ignore

                return Path(env.INDEX_DIR) / "_pubs" / "pubs.yml"
            except Exception:
                break
            finally:
                sys.path.pop(0)
    index_dir = os.environ.get("INDEX_DIR")
    if index_dir:
        return Path(index_dir) / "_pubs" / "pubs.yml"
    return raiz.parents[3] / "_pubs" / "pubs.yml"  # web/_aula/api/aula/origenes.py → web


def _origen(url: str) -> str:
    m = re.match(r"^(https://[^/]+)", url.strip())
    if not m:
        raise ValueError(f"URL de sitio no https: {url!r}")
    return m.group(1).lower()


def calcular(ruta: Path | None = None) -> dict:
    datos = yaml.safe_load((ruta or _pubs_yml()).read_text(encoding="utf-8"))
    urls = [datos["hub"]["url"]] + [p["url"] for p in datos["pubs"]]
    origenes = sorted({_origen(u) for u in urls})
    previas = []
    for o in origenes:
        sitio = re.match(r"^https://([a-z0-9-]+)\.netlify\.app$", o)
        if sitio:
            previas.append(_PLANTILLA_PREVIA.format(sitio=re.escape(sitio.group(1))))
    return {"generado": AVISO, "origenes": origenes, "previas": sorted(previas)}


def cargar() -> dict:
    try:
        return json.loads(GENERADO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"origenes": [], "previas": []}


def lista_blanca(cors_local: bool, extra: str) -> tuple[list[str], str | None]:
    """(orígenes exactos, expresión regular) para CORSMiddleware."""
    datos = cargar()
    exactos = list(datos.get("origenes", [])) + [o.strip().rstrip("/") for o in extra.split(",") if o.strip()]
    patrones = list(datos.get("previas", []))
    if cors_local:
        patrones.append(LOCAL)
    regex = "^(" + "|".join(patrones) + ")$" if patrones else None
    return exactos, regex


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m aula.origenes", description=__doc__.split("\n\n")[0])
    grupo = ap.add_mutually_exclusive_group()
    grupo.add_argument("--aplicar", action="store_true", help="escribe aula/origenes.generado.json")
    grupo.add_argument("--verificar", action="store_true", help="sale 1 si el archivo generado no está al día")
    args = ap.parse_args(argv)
    nuevo = calcular()
    texto = json.dumps(nuevo, ensure_ascii=False, indent=2) + "\n"
    actual = GENERADO.read_text(encoding="utf-8") if GENERADO.exists() else ""
    al_dia = actual == texto
    if args.aplicar:
        if not al_dia:
            GENERADO.write_text(texto, encoding="utf-8")
        print(f"{'sin cambios' if al_dia else 'escrito'}: {GENERADO.name} ({len(nuevo['origenes'])} orígenes)")
        return 0
    if args.verificar:
        print(f"{GENERADO.name}: {'al día' if al_dia else 'DESACTUALIZADO (python -m aula.origenes --aplicar)'}")
        return 0 if al_dia else 1
    print("\n".join(nuevo["origenes"]))
    print(f"[simulación] {GENERADO.name}: {'al día' if al_dia else 'cambiaría (use --aplicar)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
