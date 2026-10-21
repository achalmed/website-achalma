#!/usr/bin/env python3
"""scripts/cv-a-web.py — lleva la experiencia del CV (repo `cv`) a la portada y al About del hub (2026-10-21).

El CV es el maestro: cada empleo vive una sola vez en `cv/main/sections/experiencias/entradas/<AAAA-MM_slug>.tex`
(macro `\\experience` de siete argumentos) y el selector `2_experiencias_larga.tex` fija cuáles están activos y en qué
orden. Este script los lee y escribe sus bloques generados (entre marcas; no se editan a mano):
  about/index.qmd   <!-- trayectoria:inicio --> … <!-- trayectoria:fin -->   línea de tiempo con filtros por área
  about/index.qmd   <!-- ahora:inicio --> … <!-- ahora:fin -->               el cargo o cargos en curso («Actualidad»)
  index.qmd         <!-- ahora:inicio --> … <!-- ahora:fin -->               el mismo bloque, en la portada
El área de cada empleo (sector público, docencia, datos, finanzas) sale de los selectores de perfil del CV donde aparece
el empleo o una variante suya (`<slug>--<perfil>`): no se declara aquí. Solo se publica lo que el CV ya publica (su
repo es público); del pie de cada entrada se toman el proceso y las herramientas, no los identificadores de la entidad.

Uso: python3 scripts/cv-a-web.py [--aplicar | --verificar]
  sin opción   simula: dice qué bloques cambiarían y no escribe nada
  --aplicar    reescribe los dos bloques
  --verificar  sale 1 si algún bloque no coincide con el CV (lo usa scripts/generar-externos.sh --verificar)
Salida: 0 bien · 1 desfasado o error de lectura · 2 uso incorrecto.
Rutas: el CV por CV_DIR (core/env.sh) o junto al hub, como scripts/generar-externos.sh.
"""
from __future__ import annotations

import html
import os
import pathlib
import re
import sys

HUB = pathlib.Path(__file__).resolve().parents[1]
CV = pathlib.Path(os.environ.get("CV_DIR") or HUB.parent / "cv")
EXP = CV / "main" / "sections" / "experiencias"
SELECTOR = EXP / "2_experiencias_larga.tex"
# Selector de perfil → (clave, rótulo), en el orden de los filtros. Solo los dos perfiles principales del autor: los de
# datos y finanzas reúnen empleos por afinidad del CV (ONPE en el financiero), no por área, y confundirían el filtro.
AREAS = {
    "2_experiencias_sector_publico.tex": ("sector-publico", "Sector público"),
    "2_experiencias_docencia.tex": ("docencia", "Docencia"),
}
MESES = {"enero": "ene.", "febrero": "feb.", "marzo": "mar.", "abril": "abr.", "mayo": "may.", "junio": "jun.",
         "julio": "jul.", "agosto": "ago.", "septiembre": "sept.", "setiembre": "sept.", "octubre": "oct.",
         "noviembre": "nov.", "diciembre": "dic."}


# ── Lectura del LaTeX ─────────────────────────────────────────────────────────────────────────────────────────────
def sin_comentarios(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def activas(selector: pathlib.Path) -> list[str]:
    return re.findall(r"\\entradaExperiencia\{([^}]+)\}", sin_comentarios(selector.read_text(encoding="utf-8")))


def grupos(tex: str, desde: int, n: int) -> list[str]:
    """Los n grupos {…} equilibrados que siguen a `desde` (saltando espacios)."""
    out, i = [], desde
    while len(out) < n:
        while i < len(tex) and tex[i].isspace():
            i += 1
        if i >= len(tex) or tex[i] != "{":
            raise ValueError(f"se esperaba «{{» en la posición {i}")
        prof, j = 0, i
        while True:
            c = tex[j]
            if c == "\\":
                j += 2
                continue
            if c == "{":
                prof += 1
            elif c == "}":
                prof -= 1
                if prof == 0:
                    break
            j += 1
        out.append(tex[i + 1:j])
        i = j + 1
    return out


def a_html(tex: str) -> str:
    """LaTeX de texto corrido → HTML seguro (solo lo que usan las entradas del CV)."""
    t = tex
    for _ in range(3):  # macros anidadas
        t = re.sub(r"\\(?:footnotesize|small|scriptsize|normalsize)\b\s*", "", t)
        t = re.sub(r"\\href\{([^{}]*)\}\{([^{}]*)\}", lambda m: f"\x00a {m.group(1)}\x00{m.group(2)}\x00/a\x00", t)
        t = re.sub(r"\\url\{([^{}]*)\}", lambda m: m.group(1), t)
        t = re.sub(r"\\(?:emph|textit)\{([^{}]*)\}", "\x00i\x00\\1\x00/i\x00", t)
        t = re.sub(r"\\textbf\{([^{}]*)\}", "\x00b\x00\\1\x00/b\x00", t)
        t = re.sub(r"\\(?:textsc|text|mbox|textnormal)\{([^{}]*)\}", r"\1", t)
        t = re.sub(r"\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\fa[A-Za-z]+\b\s*", "", t)
    t = t.replace("\\\\", " ").replace("\\&", "&").replace("\\%", "%").replace("\\$", "$").replace("\\_", "_")
    t = t.replace("\\#", "#").replace("---", "—").replace("--", "–").replace("~", "\u00a0").replace("\\,", "\u202f")
    t = re.sub(r"\\[A-Za-z]+\*?", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = html.escape(t, quote=False)
    t = re.sub(r"\x00a (.*?)\x00(.*?)\x00/a\x00", lambda m: f'<a href="{html.escape(m.group(1))}">{m.group(2)}</a>', t)
    return t.replace("\x00i\x00", "<em>").replace("\x00/i\x00", "</em>").replace("\x00b\x00", "<strong>").replace("\x00/b\x00", "</strong>")


def fecha(txt: str) -> str:
    t = re.sub(r"\s+", " ", txt).strip()
    if t.lower() in {"actualidad", "presente", "la fecha"}:
        return "actualidad"
    m = re.fullmatch(r"([A-Za-zÁÉÍÓÚáéíóú]+)\s+(\d{4})", t)
    return f"{MESES.get(m.group(1).lower(), m.group(1).lower())} {m.group(2)}" if m else t


def entrada(slug: str) -> dict:
    tex = sin_comentarios((EXP / "entradas" / f"{slug}.tex").read_text(encoding="utf-8"))
    pos = tex.index("\\experience") + len("\\experience")
    fin, titulo, org, lugar, inicio, cuerpo, pie = grupos(tex, pos, 7)
    items = [a_html(x) for x in re.findall(r"\\item\s+(.*?)(?=\\item|\\end\{itemize\})", cuerpo, re.S)]
    resumen = a_html(re.sub(r"\\begin\{itemize\}.*?\\end\{itemize\}", "", cuerpo, flags=re.S))
    detalles, herramientas = [], []
    for parte in a_html(pie).split("|"):
        p = re.sub(r"</?em>", "", parte).strip()
        clave, _, valor = p.partition(":")
        clave = clave.strip().lower()
        if clave.startswith("herramienta") and valor:
            herramientas = [x.strip() for x in re.split(r",|;", valor) if x.strip()]
        elif clave.startswith(("proceso", "programa", "proyecto")) and valor:
            detalles.append(p)
    areas = [clave for sel, (clave, _) in AREAS.items()
             if any(a == slug or a.startswith(slug + "--") for a in activas(EXP / sel))]
    return {"slug": slug, "titulo": a_html(titulo), "org": a_html(org), "lugar": a_html(lugar),
            "inicio": fecha(inicio), "fin": fecha(fin), "resumen": resumen, "items": items,
            "detalles": detalles, "herramientas": herramientas, "areas": areas}


# ── Bloques HTML ──────────────────────────────────────────────────────────────────────────────────────────────────
def periodo(e: dict) -> str:
    return e["inicio"] if e["inicio"] == e["fin"] else f"{e['inicio']} – {e['fin']}"


def bloque_trayectoria(es: list[dict]) -> str:
    presentes = [(c, r) for c, r in AREAS.values() if any(c in e["areas"] for e in es)]
    filtros = "".join(f'<button type="button" data-filtro="{c}" aria-pressed="false">{r}</button>' for c, r in presentes)
    rot = dict(AREAS.values())
    lis = []
    for e in es:
        actual = e["fin"] == "actualidad"
        chips = "".join(f'<span class="hito-area">{rot[a]}</span>' for a in e["areas"])
        extra = ""
        if e["items"] or e["detalles"] or e["herramientas"]:
            lista = "".join(f"<li>{x}</li>" for x in e["items"])
            meta = "".join(f'<p class="hito-meta">{d}</p>' for d in e["detalles"])
            herr = ('<p class="hito-herramientas">' + "".join(f"<span>{h}</span>" for h in e["herramientas"]) + "</p>") if e["herramientas"] else ""
            extra = f'<details><summary>Funciones y logros</summary>{"<ul>" + lista + "</ul>" if lista else ""}{meta}{herr}</details>'
        clase = "hito hito-actual" if actual else "hito"
        ahora = '<span class="hito-ahora">En curso</span>' if actual else ""
        resumen = f'<p class="hito-resumen">{e["resumen"]}</p>' if e["resumen"] else ""
        lis.append(
            f'<li class="{clase}" data-areas="{" ".join(e["areas"])}">'
            f'<p class="hito-fecha"><time>{periodo(e)}</time>{ahora}</p>'
            f'<div class="hito-cuerpo"><h3>{e["titulo"]}</h3><p class="hito-org">{e["org"]} · {e["lugar"]}</p>'
            f'{resumen}<p class="hito-areas">{chips}</p>{extra}</div></li>')
    return ("```{=html}\n"
            f'<div class="trayectoria" data-trayectoria>\n'
            f'<div class="trayectoria-filtros" role="group" aria-label="Filtrar la trayectoria por área">'
            f'<button type="button" data-filtro="todo" aria-pressed="true">Todo</button>{filtros}</div>\n'
            f'<ol class="hitos">\n' + "\n".join(lis) + "\n</ol>\n"
            f'<p class="trayectoria-fuente">Fuente: <a href="/resources/cv.pdf">CV en PDF</a> · {len(es)} cargos</p>\n'
            "</div>\n```")


def bloque_ahora(es: list[dict]) -> str:
    actuales = [e for e in es if e["fin"] == "actualidad"] or es[:1]
    filas = "".join(
        f'<li><span class="ahora-cargo">{e["titulo"]}</span><span class="ahora-org">{e["org"]}</span>'
        f'<span class="ahora-desde">desde {e["inicio"]}</span></li>' for e in actuales)
    return "```{=html}\n" + f'<ul class="ahora-lista">{filas}</ul>\n' + "```"


def reemplazar(texto: str, nombre: str, contenido: str) -> str:
    patron = re.compile(rf"(<!-- {nombre}:inicio[^>]*-->\n).*?(\n<!-- {nombre}:fin -->)", re.S)
    if not patron.search(texto):
        raise SystemExit(f"falta el bloque <!-- {nombre}:inicio --> … <!-- {nombre}:fin -->")
    return patron.sub(lambda m: m.group(1) + contenido + m.group(2), texto, count=1)


def main(argv: list[str]) -> int:
    opciones = set(argv)
    if opciones - {"--aplicar", "--verificar"} or len(opciones) > 1:
        print(__doc__, file=sys.stderr)
        return 2
    if not SELECTOR.exists():
        print(f"✖ no está el CV en {CV} (CV_DIR)", file=sys.stderr)
        return 1
    try:
        # El slug empieza por la fecha de inicio (AAAA-MM): la trayectoria va de lo más reciente a lo más antiguo.
        es = [entrada(s) for s in sorted(activas(SELECTOR), reverse=True)]
    except (OSError, ValueError) as err:
        print(f"✖ no se pudo leer una entrada del CV: {err}", file=sys.stderr)
        return 1
    destinos = [(HUB / "about" / "index.qmd", "trayectoria", bloque_trayectoria(es)),
                (HUB / "about" / "index.qmd", "ahora", bloque_ahora(es)),
                (HUB / "index.qmd", "ahora", bloque_ahora(es))]
    cambios = 0
    for ruta, nombre, bloque in destinos:
        viejo = ruta.read_text(encoding="utf-8")
        nuevo = reemplazar(viejo, nombre, bloque)
        rel = ruta.relative_to(HUB)
        if nuevo == viejo:
            print(f"= {rel}: bloque «{nombre}» al día ({len(es)} cargos del CV)")
            continue
        cambios += 1
        if "--aplicar" in opciones:
            ruta.write_text(nuevo, encoding="utf-8")
            print(f"✔ {rel}: bloque «{nombre}» reescrito desde el CV")
        else:
            print(f"{'✖' if '--verificar' in opciones else '→'} {rel}: el bloque «{nombre}» no coincide con el CV")
    if "--verificar" in opciones:
        return 1 if cambios else 0
    if cambios and "--aplicar" not in opciones:
        print("Simulación: con --aplicar se escriben.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
