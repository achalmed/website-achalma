#!/usr/bin/env python3
"""comparar-produccion.py — compara el `_site/` local de cada sitio con lo que sirve Netlify, antes de publicar (ola 6, 6d).

Solo lee: descarga las páginas publicadas y no escribe en los sitios. Compara el **texto visible** de cada página
HTML (sin etiquetas, scripts ni estilos, espacios normalizados), porque Netlify reescribe el marcado al servir (un
comentario inicial y enlaces a URL limpias) y comparar bytes daría diferencias falsas. Para cada sitio informa:
páginas iguales, distintas (con las primeras líneas que cambian), nuevas (en local y no publicadas) y retiradas
(en el `sitemap.xml` publicado y no en local); los PDF se comparan por número de páginas y texto.

Uso:  python3 scripts/comparar-produccion.py [--sitio hub|<pub>] [--salida informe.md] [--max N]
      (sin --sitio, los 12; el registro carpeta ↔ dominio es `_pubs/pubs.yml`)
Salida: 0 sin diferencias de contenido · 1 con diferencias · 2 error de uso o de red.
"""
import argparse
import difflib
import http.client
import html.parser
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

HUB = Path(__file__).resolve().parents[1]
URL_HUB = "https://achalmaedison.netlify.app/"
AGENTE = "comparar-produccion/1.0 (ecosistema; solo lectura)"


class Texto(html.parser.HTMLParser):
    OCULTOS = {"script", "style", "noscript", "template", "svg"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes, self.ocultos = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.OCULTOS:
            self.ocultos += 1

    def handle_endtag(self, tag):
        if tag in self.OCULTOS and self.ocultos:
            self.ocultos -= 1

    def handle_data(self, data):
        if not self.ocultos and data.strip():
            self.partes.append(re.sub(r"\s+", " ", data.strip()))


def texto_html(datos):
    p = Texto()
    p.feed(datos.decode("utf-8", "replace"))
    return p.partes


def texto_pdf(datos):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(datos)
        f.flush()
        r = subprocess.run(["pdftotext", "-q", "-layout", f.name, "-"], capture_output=True)
        info = subprocess.run(["pdfinfo", f.name], capture_output=True, text=True).stdout
    paginas = next((l.split()[-1] for l in info.splitlines() if l.startswith("Pages:")), "?")
    return paginas, [re.sub(r"\s+", " ", l).strip() for l in r.stdout.decode("utf-8", "replace").splitlines() if l.strip()]


def bajar(url, intentos=3):
    for i in range(intentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENTE}), timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, b""
        except (urllib.error.URLError, http.client.HTTPException, OSError):   # incluye lecturas incompletas
            time.sleep(2 * (i + 1))
    return None, b""


def sitios(filtro):
    reg = yaml.safe_load((HUB / "_pubs" / "pubs.yml").read_text(encoding="utf-8"))
    pubs = reg["pubs"] if isinstance(reg, dict) and "pubs" in reg else reg
    todos = [("hub", HUB, URL_HUB)] + [(p["carpeta"], HUB / "_pubs" / p["carpeta"], p["url"]) for p in pubs]
    if filtro:
        todos = [s for s in todos if filtro in (s[0], s[0].removeprefix("pub_"))]
    return todos


def comparar(nombre, raiz, url, maximo):
    site = raiz / "_site"
    locales = sorted(p.relative_to(site).as_posix() for p in site.rglob("*") if p.suffix in (".html", ".pdf")
                     and "site_libs" not in p.parts)
    res = {"iguales": 0, "distintas": [], "nuevas": [], "retiradas": [], "errores": []}
    for rel in locales[:maximo] if maximo else locales:
        codigo, remoto = bajar(url + urllib.parse.quote(rel))     # espacios y tildes en las rutas
        if codigo == 404:
            res["nuevas"].append(rel)
            continue
        if codigo != 200:
            res["errores"].append(f"{rel}: {codigo}")
            continue
        try:
            local = (site / rel).read_bytes()
        except OSError:                    # un render en curso lo quitó: se anota y se sigue
            res["errores"].append(f"{rel}: desapareció del _site durante la comparación")
            continue
        if rel.endswith(".pdf"):
            (pl, tl), (pr, tr) = texto_pdf(local), texto_pdf(remoto)
            if tl == tr and pl == pr:
                res["iguales"] += 1
            else:
                cambio = [l for l in difflib.unified_diff(tr, tl, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
                res["distintas"].append((rel, f"PDF: {pr} → {pl} páginas; {len(cambio)} líneas de texto cambian", cambio[:4]))
            continue
        tl, tr = texto_html(local), texto_html(remoto)
        if tl == tr:
            res["iguales"] += 1
        else:
            cambio = [l for l in difflib.unified_diff(tr, tl, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
            res["distintas"].append((rel, f"{len(cambio)} fragmentos de texto cambian", cambio[:6]))
    codigo, mapa = bajar(url + "sitemap.xml")
    if codigo == 200:
        publicadas = {re.sub(r"^https?://[^/]+/", "", u) for u in re.findall(r"<loc>([^<]+)</loc>", mapa.decode("utf-8", "replace"))}
        res["retiradas"] = sorted(p for p in publicadas if p and not (site / p).exists() and not (site / p / "index.html").exists())
    return res


def informe(resultados):
    out = ["# Comparación del render local con producción", "",
           "Generado por `04 index/scripts/comparar-produccion.py` (solo lectura). Texto visible de cada página; "
           "los PDF por páginas y texto.", "",
           "| sitio | iguales | distintas | nuevas | retiradas | errores |", "|---|---|---|---|---|---|"]
    for n, r in resultados:
        out.append(f"| {n} | {r['iguales']} | {len(r['distintas'])} | {len(r['nuevas'])} | {len(r['retiradas'])} | {len(r['errores'])} |")
    for n, r in resultados:
        if not (r["distintas"] or r["nuevas"] or r["retiradas"] or r["errores"]):
            continue
        out += ["", f"## {n}", ""]
        for rel, resumen, muestra in r["distintas"]:
            out.append(f"- **{rel}**: {resumen}")
            out += [f"  - `{m[:160]}`" for m in muestra]
        if r["nuevas"]:
            out.append(f"- nuevas (no publicadas): {', '.join(r['nuevas'][:30])}{' …' if len(r['nuevas']) > 30 else ''}")
        if r["retiradas"]:
            out.append(f"- en el sitemap publicado y no en local: {', '.join(r['retiradas'][:30])}{' …' if len(r['retiradas']) > 30 else ''}")
        if r["errores"]:
            out.append(f"- errores de red: {', '.join(r['errores'][:10])}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sitio")
    ap.add_argument("--salida")
    ap.add_argument("--max", type=int, default=0, help="como mucho N páginas por sitio (0 = todas)")
    a = ap.parse_args()
    elegidos = sitios(a.sitio)
    if not elegidos:
        print(f"No existe el sitio: {a.sitio}", file=sys.stderr)
        return 2
    resultados = []
    for n, raiz, url in elegidos:
        r = comparar(n, raiz, url.rstrip("/") + "/", a.max)
        resultados.append((n, r))
        print(f"{n}: {r['iguales']} iguales · {len(r['distintas'])} distintas · {len(r['nuevas'])} nuevas · "
              f"{len(r['retiradas'])} retiradas · {len(r['errores'])} errores", flush=True)
        if a.salida:                       # el informe se reescribe tras cada sitio: un corte no lo pierde todo
            Path(a.salida).write_text(informe(resultados), encoding="utf-8")
    texto = informe(resultados)
    if a.salida:
        Path(a.salida).write_text(texto, encoding="utf-8")
    return 1 if any(r["distintas"] or r["nuevas"] or r["retiradas"] for _, r in resultados) else 0


if __name__ == "__main__":
    sys.exit(main())
