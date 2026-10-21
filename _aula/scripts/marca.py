#!/usr/bin/env python3
"""scripts/marca.py — trazos de la marca de los 12 sitios: el ícono (squircle + monograma) y los textos de la imagen
Open Graph, convertidos en `path` con Inter para que no dependan de las fuentes instaladas donde se construya.

Lee config/vitrina.yml (monograma de cada pub y del hub), web/_pubs/pubs.yml (nombres y dominios) y
docencia/config/areas.yml (el área de cada pub); escribe src/lib/marca.generado.mjs (GENERADO; no editar). Las fuentes
son los .woff de @fontsource/inter (dependencia de desarrollo, versión exacta en package.json; licencia SIL OFL).

Uso (desde web/_aula):
    python3 scripts/marca.py            # simula: imprime lo que escribiría
    python3 scripts/marca.py --aplicar  # escribe src/lib/marca.generado.mjs

Decisión: docs/decisiones.md §1.16.
"""
from __future__ import annotations

import json
import logging
import math
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

FUENTES = AULA / "node_modules" / "@fontsource" / "inter" / "files"
VITRINA = AULA / "config" / "vitrina.yml"
SALIDA = AULA / "src" / "lib" / "marca.generado.mjs"
logging.getLogger("fontTools").setLevel(logging.ERROR)

_fuentes: dict[int, TTFont] = {}


def fuente(peso: int) -> TTFont:
    if peso not in _fuentes:
        _fuentes[peso] = TTFont(FUENTES / f"inter-latin-{peso}-normal.woff")
    return _fuentes[peso]


def texto(cadena: str, peso: int, tracking: float = 0.0) -> dict:
    """Contorno de una línea de texto en unidades de fuente (eme = 2048), línea base en y = 0, y hacia abajo."""
    f = fuente(peso)
    cmap, glifos, metricas = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    pluma = SVGPathPen(glifos, ntos=lambda v: f"{v:.0f}")  # con el juego de glifos: las letras con tilde son compuestas
    cotas = BoundsPen(glifos)
    x = 0.0
    for car in cadena:
        nombre = cmap.get(ord(car))
        if nombre is None:
            raise SystemExit(f"marca: «{car}» no está en Inter latin {peso}")
        for p in (pluma, cotas):
            glifos[nombre].draw(TransformPen(p, (1, 0, 0, -1, x, 0)))
        x += metricas[nombre][0] + tracking
    x -= tracking
    b = cotas.bounds or (0, 0, 0, 0)
    return {"d": pluma.getCommands(), "avance": round(x), "caja": [round(v) for v in b]}


def squircle(n: float = 5.0, puntos: int = 96, lado: float = 100.0) -> str:
    """Superelipse |x|^n + |y|^n = 1 (la forma de los íconos de macOS), en una caja de 0 a `lado`."""
    r = lado / 2
    trazo = []
    for i in range(puntos):
        t = 2 * math.pi * i / puntos
        c, s = math.cos(t), math.sin(t)
        x = r + r * math.copysign(abs(c) ** (2 / n), c)
        y = r + r * math.copysign(abs(s) ** (2 / n), s)
        trazo.append(f"{'M' if i == 0 else 'L'}{x:.2f} {y:.2f}")
    return "".join(trazo) + "Z"


def monograma(letras: str) -> dict:
    """Las dos letras del ícono, en Inter 600 con el espaciado cerrado de un logotipo."""
    return texto(letras, 600, tracking=-60)


def main() -> int:
    aplicar = "--aplicar" in sys.argv[1:]
    vitrina = yaml.safe_load(VITRINA.read_text(encoding="utf-8"))
    registro = yaml.safe_load((Path(env.INDEX_DIR) / "_pubs" / "pubs.yml").read_text(encoding="utf-8"))
    areas = yaml.safe_load((Path(env.CLASS_DIR) / "config" / "areas.yml").read_text(encoding="utf-8"))["areas"]
    area_de = {a["pub"]: a["nombre"] for a in areas if a.get("pub")}

    sitios: dict[str, dict] = {}
    for p in registro["pubs"]:
        conf = (vitrina.get("pubs") or {}).get(p["carpeta"]) or {}
        if not conf.get("monograma"):
            raise SystemExit(f"marca: {p['carpeta']} no declara monograma en config/vitrina.yml")
        nombre = conf.get("nombre") or " ".join(
            w if i and w in {"y", "e", "de", "del", "la", "el"} else w.capitalize() for i, w in enumerate(p["carpeta"].split("-"))
        )
        sitios[p["carpeta"]] = {
            "letras": conf["monograma"],
            "monograma": monograma(conf["monograma"]),
            "nombre": texto(nombre, 600, tracking=-40),
            "area": texto(area_de.get(p["carpeta"], p["tema"]), 400),
            "dominio": texto(re.sub(r"^https?://|/$", "", p["url"]), 500),
        }
    hub = vitrina.get("hub") or {}
    sitios["hub"] = {
        "letras": hub.get("monograma", "EA"),
        "monograma": monograma(hub.get("monograma", "EA")),
        "nombre": texto(hub.get("nombre", registro["autor"]["nombre"]), 600, tracking=-40),
        "area": texto(hub.get("area", ""), 400) if hub.get("area") else None,
        "dominio": texto(re.sub(r"^https?://|/$", "", registro["hub"]["url"]), 500),
    }
    marca = {
        "eme": 2048,
        "squircle": squircle(),
        "firma": texto(f"por {registro['autor']['nombre']}", 500),
        "sitios": sitios,
    }
    salida = (
        "// GENERADO por scripts/marca.py desde config/vitrina.yml, web/_pubs/pubs.yml, docencia/config/areas.yml y Inter\n"
        "// (@fontsource/inter, SIL OFL); no editar. Trazos en unidades de fuente (eme = 2048, línea base en y = 0).\n"
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
