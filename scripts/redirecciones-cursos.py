#!/usr/bin/env python3
"""redirecciones-cursos.py — retiro de web/cursos (fase 7 de docs/plataforma-educativa.md): cada URL que el hub publica
bajo /cursos/ pasa, con una redirección 301, a su casa nueva en el pub de su área (la vitrina de web/_aula).

Reglas (en `_redirects`, formato de Netlify, que el render copia a _site/):
  · ficha /cursos/<materia>/            → https://<pub>/cursos/<curso>/ si la materia es un solo curso; si agrupa
                                          varios, al catálogo https://<pub>/cursos/
  · edición /cursos/<materia>/<edicion>/ → https://<pub>/ediciones/<dictado>/ ; cada sesión, al ancla de su sesión;
                                          sus materiales (slides/, practice/…), uno a uno a la misma ruta bajo la edición
  · post trasladado del hub a un pub (frontmatter `aliases_hub:` con sus URL viejas, p. ej. las sesiones de
    pre_economia/2014-i en propaedeutica/economia/) → su página en la vitrina del pub (la regla de su carpeta en
    `_redirects` de la vitrina), o la portada de su curso si sigue en borrador; la portada de su edición
    (/cursos/<materia>/<edicion>/) y lo que cuelgue de ella sin regla propia, también a la portada del curso
  · lo que no tiene pub todavía (sql) NO se redirige y se queda en el hub.
Las carpetas redirigidas se pueden retirar de web/cursos/; este script no borra nada: lo dice.

Uso: python3 scripts/redirecciones-cursos.py [--aplicar]   (sin --aplicar simula: imprime las reglas y las pruebas)
     python3 scripts/redirecciones-cursos.py verificar     (sale 1 si _redirects está desfasado o un destino no existe)
Las pruebas de destino leen la vitrina construida en web/_aula/dist/<pub>/ (PUB=<pub> npm run build).
Salida: 0 bien · 1 _redirects desfasado o destino inexistente · 2 uso incorrecto.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

_d = Path(__file__).resolve().parent
while _d != _d.parent and not (_d / "core" / "env.py").is_file():
    _d = _d.parent
sys.path.insert(0, str(_d / "core"))
import env  # noqa: E402

HUB = Path(env.INDEX_DIR)
SITE = HUB / "_site"
CLASS = Path(env.CLASS_DIR)
AULA_DIST = HUB / "_aula" / "dist"
SALIDA = HUB / "_redirects"
sys.path.insert(0, str(CLASS / "scripts"))
import areas  # noqa: E402


def leer(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def contexto():
    urls = {p["carpeta"]: p["url"].rstrip("/") for p in leer(HUB / "_pubs" / "pubs.yml")["pubs"]}
    materias: dict[str, list[tuple[str, str | None]]] = {}
    for cy in sorted((CLASS / "contenido" / "cursos").glob("*/curso.yml")):
        c = leer(cy)
        if c.get("materia_web"):
            materias.setdefault(c["materia_web"], []).append((c["id"], areas.pub_de(cy)))
    ediciones = {}
    for dy in sorted((CLASS / "contenido" / "dictados").glob("*/dictado.yml")):
        d = leer(dy)
        web = d.get("web") or {}
        if not web.get("materia"):
            continue
        cursos = list(d.get("cursos") or []) or [s["curso"] for s in d.get("sesiones") or [] if s.get("curso")]
        pub = areas.pub_de(CLASS / "contenido" / "cursos" / cursos[0] / "curso.yml") if cursos else None
        ediciones[(web["materia"], web["edicion"])] = (d["id"], pub, [s.get("web") for s in d.get("sesiones") or []])
    return urls, materias, ediciones


# Fichas del hub que no son un curso sino unidades de uno (decisión de la fase 1, 2026-10-20).
EQUIVALENCIAS = {"algebra-lineal": "matematicas-ii", "calculo": "matematicas-ii", "optimizacion": "matematicas-iii"}
EDICION_VIEJA = re.compile(r"^/cursos/([^/]+)/([^/]+)/sesiones/[^/]+/$")


def frontmatter(qmd: Path) -> dict:
    t = qmd.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return {}
    return yaml.safe_load(t.split("\n---", 1)[0].lstrip("-\n")) or {}


def reglas_vitrina(pub: str) -> dict[str, str]:
    """{/<sección>/<post>/: ruta nueva} del _redirects de la vitrina del pub (la construida en _aula/dist o la
    publicada en _pubs/<pub>/_vitrina): así la URL nueva de un post es la que la vitrina le da, no una copia de su regla."""
    for f in (AULA_DIST / pub / "_redirects", HUB / "_pubs" / pub / "_vitrina" / "_redirects"):
        if f.exists():
            out = {}
            for linea in f.read_text(encoding="utf-8").splitlines():
                partes = linea.split()
                if len(partes) == 3 and not linea.startswith("#") and partes[0].endswith("/*"):
                    out.setdefault(partes[0][:-1], partes[1].removesuffix(":splat"))
            return out
    return {}


def trasladados(urls: dict[str, str]) -> list[tuple[str, str]]:
    """301 de los posts que vivían en el hub y pasaron a un pub (frontmatter `aliases_hub:`), y de la portada de su
    edición vieja. Primero las reglas exactas; al final, por edición, la regla `*` que recoge el resto."""
    exactas, ediciones = [], {}
    for pub, base in sorted(urls.items()):
        raiz = HUB / "_pubs" / pub
        posts = sorted(q for q in raiz.glob("*/*/index.qmd") if not q.parts[-3].startswith((".", "_")))
        vitrina = None
        for q in posts:
            fm = frontmatter(q)
            viejas = fm.get("aliases_hub") or []
            if not viejas:
                continue
            if vitrina is None:
                vitrina = reglas_vitrina(pub)
            curso = f"{base}/cursos/{fm['curso']}/" if fm.get("curso") else f"{base}/"
            nueva = vitrina.get(f"/{q.parent.parent.name}/{q.parent.name}/")
            for a in viejas:
                a = "/" + str(a).strip("/") + "/"
                if nueva:
                    exactas += [(a, base + nueva), (a + "index.html", base + nueva), (a + "*", base + nueva + ":splat")]
                else:                                   # borrador: aún sin página propia en la vitrina
                    exactas += [(a, curso), (a + "index.html", curso)]
                m = EDICION_VIEJA.match(a)
                if m:
                    ediciones.setdefault((m.group(1), m.group(2)), curso)
    for (mat, ed), curso in sorted(ediciones.items()):
        e = f"/cursos/{mat}/{ed}/"
        exactas += [(e, curso), (e + "index.html", curso)]
    return exactas + [(f"/cursos/{mat}/{ed}/*", curso) for (mat, ed), curso in sorted(ediciones.items())]


def reglas() -> tuple[list[tuple[str, str]], list[str], list[str]]:
    """[(desde, hacia)], carpetas de web/cursos que quedan redirigidas, materias que se quedan en el hub."""
    urls, materias, ediciones = contexto()
    # pub de una materia heredada sin curso: el de su edición (metodología vive en methodica por sus dictados)
    pub_de_materia = {m: next((p for _, p in cs if p), None) for m, cs in materias.items()}
    for (m, _), (_, pub, _) in ediciones.items():      # materia heredada sin curso: el pub de sus ediciones
        if pub and not pub_de_materia.get(m):
            pub_de_materia[m] = pub
    cursos_dir = CLASS / "contenido" / "cursos"
    # Las reglas salen del currículo, no del disco del hub (las carpetas se retiran después de escribirlas):
    # materias web, materias de los dictados, equivalencias, ids de curso y las fichas que aún queden en web/cursos.
    candidatas = sorted(set(materias) | {k[0] for k in ediciones} | set(EQUIVALENCIAS)
                        | {d.name for d in cursos_dir.iterdir() if (d / "curso.yml").exists()}
                        | {f.parent.name for f in (HUB / "cursos").glob("*/index.qmd")})
    for m in candidatas:                                # ficha con nombre de curso, o equivalente a uno
        cid = EQUIVALENCIAS.get(m, m)
        if not pub_de_materia.get(m) and (cursos_dir / cid / "curso.yml").exists():
            pub_de_materia[m] = areas.pub_de(cursos_dir / cid / "curso.yml")
            materias.setdefault(m, []).append((cid, pub_de_materia[m]))
    ediciones = {k: (dic, pub or pub_de_materia.get(k[0]), ses) for k, (dic, pub, ses) in ediciones.items()}
    out, retirables, quedan = trasladados(urls), [], []
    for m in candidatas:
        pub = pub_de_materia.get(m)
        if not pub or pub not in urls:
            if (HUB / "cursos" / m / "index.qmd").exists():
                quedan.append(m)
            continue
        base = urls[pub]
        cs = [c for c, p in materias.get(m, []) if p == pub]
        destino = f"{base}/cursos/{cs[0]}/" if len(cs) == 1 else f"{base}/cursos/"
        for (mm, ed), (dic, pubd, sesiones) in sorted(ediciones.items()):
            if mm != m or not pubd:
                continue
            bd = f"{urls[pubd]}/ediciones/{dic}"
            for s in sesiones:
                if s:
                    out += [(f"/cursos/{m}/{ed}/{s}/", f"{bd}/#{s}"), (f"/cursos/{m}/{ed}/{s}/index.html", f"{bd}/#{s}")]
                    # los `aliases:` de la sesión (URL aún más viejas, /talk/…) que Quarto ya no generará
                    fm = HUB / "_pubs" / pubd / "_ediciones" / dic / s / "index.qmd"
                    if fm.exists():
                        cab = fm.read_text(encoding="utf-8").split("\n---", 1)[0]
                        for alias in (yaml.safe_load(cab.lstrip("-\n")) or {}).get("aliases") or []:
                            a = "/" + str(alias).strip("/") + "/"
                            out += [(a, f"{bd}/#{s}"), (a + "index.html", f"{bd}/#{s}")]
            out += [(f"/cursos/{m}/{ed}/", f"{bd}/"), (f"/cursos/{m}/{ed}/index.html", f"{bd}/"),
                    (f"/cursos/{m}/{ed}/*", f"{bd}/:splat")]
        out += [(f"/cursos/{m}/", destino), (f"/cursos/{m}/index.html", destino)]
        if (HUB / "cursos" / m).exists():
            retirables.append(m)
    return out, retirables, quedan


def bloque_sitios() -> str:
    """Tabla área → sitio para la portada de cursos del hub (cursos/index.qmd, entre las marcas sitios:)."""
    pubs = {p["carpeta"]: p for p in leer(HUB / "_pubs" / "pubs.yml")["pubs"]}
    filas = ["| Área | Sitio |", "|---|---|"]
    for a in leer(CLASS / "config" / "areas.yml")["areas"]:
        p = pubs.get(a.get("pub") or "")
        if p:
            nombre = p["carpeta"].replace("-", " ").title().replace(" Y ", " y ")
            filas.append(f"| {a['nombre']} | [{nombre}]({p['url']}cursos/) |")
    return ("Los cursos viven en el sitio de su área: allí están el temario, las lecciones, las ediciones dictadas y "
            "los materiales. Lo que aún no tiene sitio sigue aquí abajo.\n\n" + "\n".join(filas) + "\n")


def escribir_portada(aplicar: bool) -> bool:
    """Reescribe el bloque entre <!-- sitios:inicio --> y <!-- sitios:fin -->; devuelve si estaba al día."""
    p = HUB / "cursos" / "index.qmd"
    t = p.read_text(encoding="utf-8")
    i = t.index("<!-- sitios:inicio"); i = t.index("-->", i) + 3
    j = t.index("<!-- sitios:fin -->")
    nuevo = t[:i] + "\n" + bloque_sitios() + t[j:]
    if aplicar and nuevo != t:
        p.write_text(nuevo, encoding="utf-8")
    return nuevo == t


def texto(rs: list[tuple[str, str]]) -> str:
    cab = ["# _redirects — GENERADO por web/scripts/redirecciones-cursos.py; no editar.",
           "# Retiro de web/cursos (fase 7): cada curso y edición vive en el pub de su área (vitrina web/_aula)."]
    return "\n".join(cab + [f"{a}  {b}  301" for a, b in rs]) + "\n"


def destino_existe(url: str, urls: dict[str, str]) -> bool | None:
    """True/False si el destino está (o no) en la vitrina construida; None si ese pub no está construido."""
    for pub, base in urls.items():
        if url.startswith(base + "/"):
            dist = AULA_DIST / pub
            if not dist.exists():
                return None
            ruta = url[len(base) + 1:].split("#")[0]
            if ruta.endswith(":splat"):
                return (dist / ruta[: -len(":splat")]).is_dir()
            f = dist / ruta
            return f.is_file() or (f / "index.html").is_file()
    return False


def main(argv: list[str]) -> int:
    if set(argv) - {"--aplicar", "verificar"}:
        print(__doc__, file=sys.stderr)
        return 2
    rs, retirables, quedan = reglas()
    urls = contexto()[0]
    nuevo = texto(rs)
    malos = [(a, b) for a, b in rs if destino_existe(b, urls) is False]
    sin_construir = sorted({b.split("/")[2] for a, b in rs if destino_existe(b, urls) is None})
    if "verificar" in argv:
        al_dia = SALIDA.exists() and SALIDA.read_text(encoding="utf-8") == nuevo and escribir_portada(False)
        print(f"_redirects {'al día' if al_dia else 'desfasado'} · {len(rs)} reglas · {len(malos)} destinos inexistentes")
        for a, b in malos:
            print(f"  ✖ {a} → {b}")
        return 0 if al_dia and not malos else 1
    if "--aplicar" in argv:
        SALIDA.write_text(nuevo, encoding="utf-8")
        escribir_portada(True)
        print(f"escrito {SALIDA.relative_to(HUB)} ({len(rs)} reglas)")
    else:
        print(nuevo, end="")
    print(f"carpetas de web/cursos aún en disco y ya redirigidas (retirables): {', '.join(retirables) or '—'}")
    print(f"se quedan en el hub (sin pub todavía): {', '.join(quedan) or '—'}")
    if sin_construir:
        print(f"sin vitrina construida para comprobar: {', '.join(sin_construir)}")
    for a, b in malos:
        print(f"  ✖ destino inexistente: {a} → {b}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
