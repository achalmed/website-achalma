#!/usr/bin/env python3
"""scripts/marca.py — trazos del colofón de los 12 sitios y de los textos de su imagen Open Graph.

El colofón es un sello tipográfico: el monograma del sitio en Petrona (la serif de los títulos) dentro de un cuadrado
de doble filete, como el de una editorial universitaria. Se guardan los contornos como `path` para que el favicon, el
PNG y la imagen Open Graph no dependan de las fuentes instaladas donde se construya.

Lee config/vitrina.yml (monogramas), web/_pubs/pubs.yml (nombres y dominios) y docencia/config/areas.yml (áreas);
escribe src/lib/marca.generado.mjs (GENERADO; no editar). Fuentes: los .woff de @fontsource/petrona y
@fontsource/source-serif-4 (dependencias de desarrollo con versión exacta; licencia SIL OFL).

Uso (desde web/_aula):
    python3 scripts/marca.py            # simula: imprime lo que escribiría
    python3 scripts/marca.py --aplicar  # escribe src/lib/marca.generado.mjs

Decisión: docs/decisiones.md §1.18.
"""
from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

import yaml
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AULA = Path(__file__).resolve().parent.parent
RAIZ = next(p for p in AULA.parents if (p / "core" / "env.py").exists())
sys.path.insert(0, str(RAIZ / "core"))
import env  # noqa: E402  (rutas del ecosistema: normativa 5.1)

FONTSOURCE = AULA / "node_modules" / "@fontsource"
VITRINA = AULA / "config" / "vitrina.yml"
SALIDA = AULA / "src" / "lib" / "marca.generado.mjs"
logging.getLogger("fontTools").setLevel(logging.ERROR)

_fuentes: dict[str, TTFont] = {}


def fuente(familia: str, peso: int, estilo: str = "normal") -> TTFont:
    clave = f"{familia}-latin-{peso}-{estilo}"
    if clave not in _fuentes:
        _fuentes[clave] = TTFont(FONTSOURCE / familia / "files" / f"{clave}.woff")
    return _fuentes[clave]


def texto(cadena: str, familia: str, peso: int, estilo: str = "normal", tracking: float = 0.0) -> dict:
    """Contorno de una línea de texto en unidades de fuente (eme = 1000), línea base en y = 0, y hacia abajo."""
    f = fuente(familia, peso, estilo)
    cmap, glifos, metricas = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    pluma = SVGPathPen(glifos, ntos=lambda v: f"{v:.0f}")  # con el juego de glifos: las letras con tilde son compuestas
    cotas = BoundsPen(glifos)
    x = 0.0
    for car in cadena:
        nombre = cmap.get(ord(car))
        if nombre is None:
            raise SystemExit(f"marca: «{car}» no está en {familia} {peso} {estilo}")
        for p in (pluma, cotas):
            glifos[nombre].draw(TransformPen(p, (1, 0, 0, -1, x, 0)))
        x += metricas[nombre][0] + tracking
    x -= tracking
    b = cotas.bounds or (0, 0, 0, 0)
    return {"d": pluma.getCommands(), "avance": round(x), "caja": [round(v) for v in b], "eme": f["head"].unitsPerEm}


def nombre_de(carpeta: str) -> str:
    return " ".join(w if i and w in {"y", "e", "de", "del", "la", "el"} else w.capitalize() for i, w in enumerate(carpeta.split("-")))


def main() -> int:
    aplicar = "--aplicar" in sys.argv[1:]
    vitrina = yaml.safe_load(VITRINA.read_text(encoding="utf-8"))
    registro = yaml.safe_load((Path(env.INDEX_DIR) / "_pubs" / "pubs.yml").read_text(encoding="utf-8"))
    areas = yaml.safe_load((Path(env.CLASS_DIR) / "config" / "areas.yml").read_text(encoding="utf-8"))["areas"]
    area_de = {a["pub"]: a["nombre"] for a in areas if a.get("pub")}
    dominio = lambda url: re.sub(r"^https?://|/$", "", url)  # noqa: E731

    sitios: dict[str, dict] = {}
    for p in registro["pubs"]:
        conf = (vitrina.get("pubs") or {}).get(p["carpeta"]) or {}
        if not conf.get("monograma"):
            raise SystemExit(f"marca: {p['carpeta']} no declara monograma en config/vitrina.yml")
        sitios[p["carpeta"]] = {
            "letras": conf["monograma"],
            "monograma": texto(conf["monograma"], "petrona", 500, tracking=-10),
            "nombre": texto(conf.get("nombre") or nombre_de(p["carpeta"]), "petrona", 400, tracking=-12),
            "area": texto(area_de.get(p["carpeta"], p["tema"]), "source-serif-4", 400),
            "dominio": texto(dominio(p["url"]), "source-serif-4", 400),
        }
    hub = vitrina.get("hub") or {}
    sitios["hub"] = {
        "letras": hub.get("monograma", "EA"),
        "monograma": texto(hub.get("monograma", "EA"), "petrona", 500, tracking=-10),
        "nombre": texto(hub.get("nombre", registro["autor"]["nombre"]), "petrona", 400, tracking=-12),
        "area": texto(hub["area"], "source-serif-4", 400) if hub.get("area") else None,
        "dominio": texto(dominio(registro["hub"]["url"]), "source-serif-4", 400),
    }
    marca = {"firma": texto(f"por {registro['autor']['nombre']}", "source-serif-4", 400, "italic"), "sitios": sitios}
    salida = (
        "// GENERADO por scripts/marca.py desde config/vitrina.yml, web/_pubs/pubs.yml, docencia/config/areas.yml, Petrona y\n"
        "// Source Serif 4 (@fontsource, SIL OFL); no editar. Trazos en unidades de fuente (línea base en y = 0).\n"
        f"export const MARCA = {json.dumps(marca, ensure_ascii=False)};\n"
    )
    actual = SALIDA.read_text(encoding="utf-8") if SALIDA.exists() else ""
    if actual == salida:
        print("marca: src/lib/marca.generado.mjs al día")
    elif aplicar:
        SALIDA.write_text(salida, encoding="utf-8")
        print(f"marca: escrito {SALIDA.relative_to(AULA)} ({len(sitios)} sitios, {len(salida) // 1024} KB)")
    else:
        for k, s in sitios.items():
            print(f"  {k:22} {s['letras']:3} nombre {s['nombre']['avance']} u")
        print(f"marca: simulación; escribiría {SALIDA.relative_to(AULA)}. Usa --aplicar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
