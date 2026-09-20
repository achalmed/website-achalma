#!/usr/bin/env python3
"""scripts/pubs.py — README y CITATION.cff de los 11 blogs satélite y el bloque «pubs» del README del hub, generados
desde _pubs/pubs.yml (DOC5, 2026-09-20).

Objetivo: que cada pub_* tenga un README propio (de qué trata, URL, repo, relación con el hub, flujo de commit,
  estructura de secciones) sin escribirlo once veces, y que el registro carpeta ↔ repo ↔ dominio ↔ tema viva en un
  solo sitio (`_pubs/pubs.yml`), comprobable contra `.gitmodules` y el `site-url` de cada `_quarto.yml`.
Método: lee pubs.yml y, por pub, las secciones temáticas del disco (carpetas de entradas con `*/index.qmd`);
  escribe `_pubs/<pub>/README.md` y `_pubs/<pub>/CITATION.cff` completos (con marca GENERADO) y el bloque entre
  `<!-- pubs:inicio -->` y `<!-- pubs:fin -->` del README del hub. Simula por defecto; `--aplicar` escribe.
  `verificar` sale 1 si el registro, los submódulos, los site-url o los archivos generados no coinciden (doctor).
Límite: no toca `_quarto.yml`, `index.qmd` ni las entradas; no propaga el tema (eso es sync-theme-pubs.sh);
  no sabe cómo publica Netlify cada pub (D1): lo que escribe en «Límite honesto» es lo que pubs.yml declara.
Sin dependencias del workspace (`core/`): el hub es un repo público y clonable; solo requiere PyYAML.

Uso:
  python3 scripts/pubs.py readme   [--aplicar] [--solo pub_x]   # 11 README + bloque del README del hub
  python3 scripts/pubs.py citation [--aplicar] [--solo pub_x]   # 11 CITATION.cff
  python3 scripts/pubs.py verificar [--doctor]                  # 0 al día · 1 desfase
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:                                   # pragma: no cover
    sys.exit("scripts/pubs.py: falta PyYAML (pip install pyyaml)")

HUB = Path(__file__).resolve().parents[1]
PUBS_DIR = HUB / "_pubs"
REGISTRO = PUBS_DIR / "pubs.yml"
MARCAS = ("<!-- pubs:inicio -->", "<!-- pubs:fin -->")
HOY = date.today().isoformat()
NO_SECCION = {"assets", "docs", "scripts", "site_libs"}        # carpetas que no son secciones de entradas
FECHA = re.compile(r"\d{4}-\d{2}-\d{2}")


def cargar():
    if not REGISTRO.exists():
        sys.exit(f"falta {REGISTRO.relative_to(HUB)}")
    d = yaml.safe_load(REGISTRO.read_text(encoding="utf-8"))
    return d, d.get("pubs") or []


def secciones(pub_dir):
    """[(carpeta, nº de entradas)] de las carpetas de primer nivel que contienen entradas `*/index.qmd`."""
    out = []
    for h in sorted(pub_dir.iterdir()):
        if not h.is_dir() or h.name.startswith(("_", ".")) or h.name in NO_SECCION:
            continue
        n = len(list(h.glob("*/index.qmd")))
        if n:
            out.append((h.name, n))
    return out


def site_url(pub_dir):
    m = re.search(r"^\s*site-url:\s*(\S+)", (pub_dir / "_quarto.yml").read_text(encoding="utf-8"), re.M) \
        if (pub_dir / "_quarto.yml").exists() else None
    return m.group(1).strip("'\"") if m else None


def submodulos():
    """Rutas declaradas en .gitmodules del hub (`_pubs/pub_x`)."""
    f = HUB / ".gitmodules"
    return set(re.findall(r"^\s*path\s*=\s*(\S+)", f.read_text(encoding="utf-8"), re.M)) if f.exists() else set()


def sin_fecha(t):
    return FECHA.sub("(fecha)", t)


# --- README de un pub ---------------------------------------------------------------
def readme_pub(d, p):
    pub_dir = PUBS_DIR / p["carpeta"]
    hub = d["hub"]
    corto = p["carpeta"].removeprefix("pub_")
    dominio = p["url"].removeprefix("https://").rstrip("/")
    filas = [f"| `{c}/` | {'entradas sin sección temática' if c == 'posts' else 'sección temática'} | {n} |"
             for c, n in secciones(pub_dir)]
    total = sum(n for _, n in secciones(pub_dir))
    nota = f"\n{p['nota'][0].upper() + p['nota'][1:]}\n" if p.get("nota") else ""
    return f"""---
tipo: readme
estado: activo
---
# {p['carpeta']}/ — {p['tema']}: blog satélite del hub `{hub['carpeta']}` (repo {p['repo']}, {dominio})

<!-- GENERADO por `04 index/scripts/pubs.py readme --aplicar` desde `04 index/_pubs/pubs.yml` ({HOY}); no editar aquí: se regenera desde el hub -->

## Qué es

{p['descripcion']} Es uno de los 11 blogs satélite de la familia Quarto de {d['autor']['nombre']}: un sitio Quarto
con repositorio y sitio Netlify propios, incluido como submódulo git en el hub `{hub['carpeta']}` (repo
`{hub['repo']}`) bajo `04 index/_pubs/{p['carpeta']}/`. El mismo blog tiene tres nombres: carpeta `{p['carpeta']}`, repo
GitHub `{d['autor']['github']}/{p['repo']}` y dominio `{dominio}`; el registro de los tres es `04 index/_pubs/pubs.yml`.
{nota}
El tema visual (SCSS, JS, extensiones, filtros, `scripts/build-page-css.sh`) **no se edita aquí**: vive en el hub y
llega por `04 index/scripts/sync-theme-pubs.sh`. Lo propio de este blog es `_quarto.yml`, `index.qmd`, `_contenido-*.qmd`,
`assets/img/` y las entradas.

## Uso

```bash
quarto preview                              # vista previa local
quarto render                               # regenera _site/ (freeze: true: el código no se re-ejecuta)
git add -A && git commit -m "post: …"       # confirmar AQUÍ primero…
git push                                    # …al remoto propio (ssh git@github.com:{d['autor']['github']}/{p['repo']}.git)
cd ../.. && git add _pubs/{p['carpeta']} && git commit -m "pubs: {corto} al último commit"   # y mover el puntero en el hub
```

## Estructura

| carpeta | qué es | entradas |
|---|---|--:|
{chr(10).join(filas) if filas else '| — | sin entradas todavía | 0 |'}
| `_quarto.yml`, `index.qmd`, `404.qmd`, `_contenido-inicio.qmd`, `_contenido-final.qmd` | configuración y portada propias del blog | |
| `assets/`, `_extensions/`, `_filters/`, `_partials/`, `scripts/` | tema propagado desde el hub (salvo `assets/img/`) | |
| `_site/` | sitio generado por `quarto render`; versionado mientras Netlify lo publique tal cual (D1) | |

{total} entradas. Cada entrada es `<sección>/AAAA-MM-DD-slug/index.qmd` con frontmatter apaquarto y fecha ISO;
sus metadatos se editan en masa desde `scripts_quarto_studio` (`metadata_manager`).

## Documentación

Toda la familia se documenta una vez, en el hub: `04 index/README.md` (qué es la familia y cómo se opera),
`04 index/docs/pubs-submodulos.md` (submódulos y flujo de commit), `04 index/docs/publicar-un-post.md` (de
principio a fin), `04 index/docs/despliegue-netlify.md` (cómo publica cada sitio) y `assets/scss/README.md` (el tema).

## Límite honesto

- Este README es el único documento propio del blog y se regenera desde el hub: lo escrito aquí a mano se pierde.
- `_site/` sigue en git: {d.get('despliegue_pubs', 'sin _publish.yml ni netlify.toml')}. `SECURITY.md` es la plantilla de GitHub sin rellenar.
- Licencia: código {d['licencia_codigo']} (`LICENSE`), contenido {d['licencia_contenido']} según `license.qmd` del hub; unificarlas en los 12 sitios es la decisión D9.
"""


# --- CITATION.cff de un pub ---------------------------------------------------------
def citation_pub(d, p):
    a = d["autor"]
    return f"""# CITATION.cff — GENERADO por `04 index/scripts/pubs.py citation --aplicar` desde `04 index/_pubs/pubs.yml` ({HOY}); no editar aquí
cff-version: 1.2.0
title: "{p['tema']} — blog de {a['nombre']} ({p['repo']})"
message: "Si citas una entrada de este blog, usa los metadatos de este archivo y la URL de la entrada."
type: software
authors:
  - given-names: {a['given_names']}
    family-names: {a['family_names']}
    orcid: '{a['orcid']}'
identifiers:
  - type: url
    value: '{p['url']}'
repository-code: 'https://github.com/{a['github']}/{p['repo']}'
url: '{p['url']}'
abstract: "{p['descripcion']} Blog satélite del hub {d['hub']['url']} ({d['hub']['repo']})."
license: {d['licencia_codigo']}
"""


# --- bloque del README del hub ------------------------------------------------------
def bloque_hub(d, pubs):
    lineas = [MARCAS[0], "| carpeta | tema | repo | sitio | entradas |", "|---|---|---|---|--:|"]
    for p in pubs:
        n = sum(k for _, k in secciones(PUBS_DIR / p["carpeta"]))
        lineas.append(f"| `_pubs/{p['carpeta']}` | {p['tema']} | `{d['autor']['github']}/{p['repo']}` | {p['url']} | {n} |")
    lineas.append(f"\n<sub>Bloque generado por `scripts/pubs.py readme --aplicar` desde `_pubs/pubs.yml` ({HOY}); no se edita a mano.</sub>")
    lineas.append(MARCAS[1])
    return "\n".join(lineas)


def con_bloque(texto, cuerpo):
    a, b = MARCAS
    if a in texto and b in texto:
        pre, resto = texto.split(a, 1)
        _, post = resto.split(b, 1)
        return pre + cuerpo + post
    return texto.rstrip("\n") + "\n\n" + cuerpo + "\n"


# --- escritura común ----------------------------------------------------------------
def escribir(destino, nuevo, aplicar, mostrar=False):
    actual = destino.read_text(encoding="utf-8") if destino.exists() else ""
    rel = destino.relative_to(HUB)
    if sin_fecha(actual) == sin_fecha(nuevo):
        print(f"  = {rel} al día")
        return False
    if aplicar:
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(nuevo, encoding="utf-8")
        print(f"  ✓ {rel} {'reescrito' if actual else 'creado'}")
    else:
        print(f"  · {rel} {'cambiaría' if actual else 'se crearía'} ({nuevo.count(chr(10))} l.)")
        if mostrar:
            print("\n" + "\n".join("    " + l for l in nuevo.splitlines()) + "\n")
    return True


def seleccion(pubs, solo):
    if not solo:
        return pubs
    solo = solo if solo.startswith("pub_") else "pub_" + solo
    sel = [p for p in pubs if p["carpeta"] == solo]
    if not sel:
        sys.exit(f"{solo} no está en {REGISTRO.relative_to(HUB)}")
    return sel


def cmd_readme(aplicar, solo):
    d, pubs = cargar()
    cambios = 0
    for p in seleccion(pubs, solo):
        if not (PUBS_DIR / p["carpeta"]).is_dir():
            print(f"  ✖ falta la carpeta _pubs/{p['carpeta']} (git submodule update --init)")
            continue
        cambios += escribir(PUBS_DIR / p["carpeta"] / "README.md", readme_pub(d, p), aplicar, mostrar=bool(solo))
    if not solo:
        hub_readme = HUB / "README.md"
        actual = hub_readme.read_text(encoding="utf-8") if hub_readme.exists() else ""
        if not hub_readme.exists():
            print("  ✖ falta README.md del hub: el bloque pubs: no tiene dónde ir")
        else:
            cambios += escribir(hub_readme, con_bloque(actual, bloque_hub(d, pubs)), aplicar)
    print(f"[pubs] readme: {cambios} archivo(s) {'escritos' if aplicar else 'cambiarían (--aplicar escribe)'}")
    return 0


def cmd_citation(aplicar, solo):
    d, pubs = cargar()
    cambios = 0
    for p in seleccion(pubs, solo):
        if (PUBS_DIR / p["carpeta"]).is_dir():
            cambios += escribir(PUBS_DIR / p["carpeta"] / "CITATION.cff", citation_pub(d, p), aplicar, mostrar=bool(solo))
    print(f"[pubs] citation: {cambios} archivo(s) {'escritos' if aplicar else 'cambiarían (--aplicar escribe)'}")
    return 0


def cmd_verificar(doctor):
    d, pubs = cargar()
    fallos = []
    declaradas = {f"_pubs/{p['carpeta']}" for p in pubs}
    en_git = submodulos()
    for r in sorted(declaradas - en_git):
        fallos.append(f"{r}: en pubs.yml pero no en .gitmodules")
    for r in sorted(en_git - declaradas):
        fallos.append(f"{r}: en .gitmodules pero no en pubs.yml")
    for p in pubs:
        pd = PUBS_DIR / p["carpeta"]
        if not pd.is_dir():
            fallos.append(f"{p['carpeta']}: carpeta ausente")
            continue
        u = site_url(pd)
        if u and u.rstrip("/") != p["url"].rstrip("/"):
            fallos.append(f"{p['carpeta']}: site-url {u} ≠ pubs.yml {p['url']}")
        for nombre, texto in (("README.md", readme_pub(d, p)), ("CITATION.cff", citation_pub(d, p))):
            f = pd / nombre
            if not f.exists():
                fallos.append(f"{p['carpeta']}/{nombre}: no existe (scripts/pubs.py {nombre.split('.')[0].lower()} --aplicar)")
            elif sin_fecha(f.read_text(encoding="utf-8")) != sin_fecha(texto):
                fallos.append(f"{p['carpeta']}/{nombre}: desfasado respecto a pubs.yml o al disco")
    hub_readme = HUB / "README.md"
    if not hub_readme.exists():
        fallos.append("README.md del hub: no existe")
    else:
        t = hub_readme.read_text(encoding="utf-8")
        if MARCAS[0] not in t:
            fallos.append("README.md del hub: sin marcas pubs:inicio/fin")
        elif sin_fecha(con_bloque(t, bloque_hub(d, pubs))) != sin_fecha(t):
            fallos.append("README.md del hub: bloque pubs desfasado (scripts/pubs.py readme --aplicar)")
    if not doctor:
        for f in fallos:
            print("  [desfase]", f)
    print(f"[pubs] {len(pubs)} blogs · {len(fallos)} desfases" + ("" if fallos else " · al día"))
    return 1 if fallos else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("readme", "citation"):
        s = sub.add_parser(c); s.add_argument("--aplicar", action="store_true"); s.add_argument("--solo")
    v = sub.add_parser("verificar"); v.add_argument("--doctor", action="store_true")
    a = ap.parse_args()
    if a.cmd == "readme":
        sys.exit(cmd_readme(a.aplicar, a.solo))
    if a.cmd == "citation":
        sys.exit(cmd_citation(a.aplicar, a.solo))
    sys.exit(cmd_verificar(a.doctor))
