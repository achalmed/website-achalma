#!/usr/bin/env python3
"""scripts/cursos.py — una lección por tema en el pub de cada curso con temario revisado (fase 5 de la plataforma educativa,
2026-10-20; web/docs/plataforma-educativa.md §4.3 y web/docs/decisiones.md §4.6).

Objetivo: que cada pub tenga, para cada curso que aloja con `temario: revisado` en su `curso.yml` (docencia), una lección
  por tema —la que ya existe o un esqueleto listo para llenar— y que la correspondencia lección ↔ tema esté DECLARADA en el
  frontmatter del post (`curso:` y `tema:`), no adivinada. El currículo manda (A3); el texto de la lección vive en el pub.
Método, por curso revisado y su pub (`docencia/scripts/areas.py pub <curso>`):
  a) declarar   a cada post que el mapa (docencia/contenido/migracion/mapa-lecciones.csv) da como lección de un tema del
                curso le escribe `curso: <id canónico>` y `tema: "<id>"`, cambiando o insertando solo esas dos líneas (no
                re-serializa el YAML ni toca el cuerpo). Un `tema:` ya declarado manda sobre el mapa.
  b) retirar    los posts que el mapa manda a revisar por duplicado (motivo con «duplica») y que son esqueletos (0
                palabras reales y `draft: true`) salen con `git rm` en su pub. Nada con texto real se borra.
  c) notas      un tema sin lección cuyo `archivo` es una nota de docencia (`02-contenido/…`) pasa al pub como lección
                con la nota de cuerpo; el `archivo` del tema apunta al post (relativo a DOCS_ROOT) y la nota sale de
                docencia con `git rm`. Si la nota casa con un patrón de meta/doctor/patrones_sensibles.txt, no se mueve.
  d) esqueletos un tema sin lección ni nota recibe un post en borrador en la sección de las lecciones del curso (la más
                común entre las de su unidad; si la unidad no tiene, la del curso; si el curso no tiene, `<curso>/`), en
                `AAAA-MM-DD-NN-<slug>` (fecha de generación, NN = orden del tema en el curso), con el frontmatter de un
                esqueleto de esa sección más `curso`, `tema` y `generado: curriculo`, y las secciones guía Objetivos,
                Desarrollo, Ejemplos, Ejercicios, Autoevaluación y Recursos. Si el título del tema cambió, se actualiza
                solo `title:` de los esqueletos generados que siguen sin texto.
  Idempotente: un tema que ya tiene un post con su `curso` + `tema` no recibe otro.
Límite: no renderiza ni confirma (eso es scripts/render.sh y git en cada pub, docencia/contenido y el hub); no inventa
  texto de lección; no mira nombres de estudiantes (el registro es sensible): solo los patrones del doctor.
Rutas por core/env.py (DOCS_ROOT, INDEX_DIR, CLASS_DIR, META_DIR).

Uso:
  python3 scripts/cursos.py [--pub PUB] [--curso CURSO]            # simula: qué declararía, retiraría, movería y crearía
  python3 scripts/cursos.py --aplicar [--pub PUB] [--curso CURSO]  # escribe
  python3 scripts/cursos.py verificar [--pub PUB] [--curso CURSO]  # 0 todo cuadra · 1 algo pendiente o incoherente
Salida: 0 bien · 1 pendiente o incoherencia (verificar) o fallo al aplicar · 2 error de uso.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

_d = Path(__file__).resolve()
while _d != _d.parent and not (_d / "core" / "env.py").exists():
    _d = _d.parent
_s = importlib.util.spec_from_file_location("core_env", _d / "core" / "env.py")
env = importlib.util.module_from_spec(_s)
_s.loader.exec_module(env)

DOCS = Path(env.DOCS_ROOT)
PUBS = Path(env.INDEX_DIR) / "_pubs"
CLASS = Path(env.CLASS_DIR)
CONTENIDO = CLASS / "contenido"
CURSOS = CONTENIDO / "cursos"
MAPA_CSV = CONTENIDO / "migracion" / "mapa-lecciones.csv"
PATRONES = Path(env.META_DIR) / "doctor" / "patrones_sensibles.txt"
HOY = date.today().isoformat()


def _modulo(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


areas = _modulo("areas", CLASS / "scripts" / "areas.py")
# El mapa define qué es «palabra real» (sin includes, comentarios, la frase de plantilla ni los encabezados guía):
# se reutiliza su lector para que cursos.py y el mapa cuenten igual.
mapa = _modulo("mapa_lecciones", CONTENIDO / "migracion" / "mapa-lecciones.py")

GUIA = {  # sección → qué va allí (una línea, como comentario del esqueleto)
    "Objetivos": "qué podrá hacer el estudiante al terminar la lección: de tres a cinco objetivos observables (explicar, calcular, estimar, programar…).",
    "Desarrollo": "la exposición del tema, de la intuición a la formalización: conceptos, supuestos o reglas, resultados y su interpretación.",
    "Ejemplos": "ejemplos resueltos paso a paso, con datos reales cuando los haya (datasets de datafw por su clave) y el código que los reproduce.",
    "Ejercicios": "ejercicios graduados para practicar, con la respuesta o una pista; los del banco del curso se citan, no se copian.",
    "Autoevaluación": "preguntas de corrección inmediata, declaradas en el frontmatter con la clave `quiz:` (web/_aula/docs/decisiones.md §1.7).",
    "Recursos": "lecturas (por su clave de Calibre o Zotero), simuladores del tema, datasets y enlaces a las lecciones vecinas.",
}
assert tuple(GUIA) == tuple(mapa.GUIA), "las secciones guía deben ser las del mapa (mapa-lecciones.py GUIA)"
QUIZ_EJEMPLO = """Ejemplo del bloque `quiz:` (va en el frontmatter, no aquí):
quiz:
  - tipo: opcion
    enunciado: "…"
    opciones: ["…", "…", "…"]
    correcta: 0
    explicacion: "…"
  - tipo: vf
    enunciado: "…"
    respuesta: false
  - tipo: numerica
    enunciado: "…"
    respuesta: 3.14
    tolerancia: 0.01"""
# claves del frontmatter del patrón que son de un post concreto y no pasan al esqueleto
NO_COPIAR = {"aliases", "bibliography", "csl", "nocite", "execute", "jupyter", "format", "quiz", "date-modified",
             "curso", "tema", "generado", "keep-ipynb"}
FM = re.compile(r"^---\n(.*?)\n---\n", re.S)


# ── utilidades ────────────────────────────────────────────────────────────────────────────────────────────────

def slug(texto: str, maximo: int = 60) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    if len(t) > maximo:
        t = t[:maximo].rsplit("-", 1)[0]
    return t


def linea_yaml(clave: str, valor) -> str:
    return yaml.safe_dump({clave: valor}, allow_unicode=True, width=1000, default_flow_style=False).rstrip("\n")


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)} en {repo}: {r.stderr.strip()}")
    return r.stdout


def partir(texto: str) -> tuple[str, str] | None:
    """(frontmatter sin delimitadores, cuerpo) o None si el archivo no abre con frontmatter."""
    m = FM.match(texto)
    return (m.group(1), texto[m.end():]) if m else None


def fijar_lineas(texto: str, cambios: dict[str, str]) -> str:
    """Cambia o inserta en el frontmatter solo las líneas `clave: valor` de `cambios`, en orden; el resto, intacto.

    Una clave existente se reemplaza en su línea (con sus líneas de continuación indentadas); una nueva se inserta tras
    la clave anterior de `cambios` o, si no hay, al final del frontmatter."""
    fm, cuerpo = partir(texto)
    lineas = fm.split("\n")
    previa = None
    for clave, linea in cambios.items():
        i = next((k for k, x in enumerate(lineas) if re.match(rf"^{re.escape(clave)}:", x)), None)
        if i is not None:
            j = i + 1
            while j < len(lineas) and lineas[j].startswith((" ", "\t")):
                j += 1
            lineas[i:j] = [linea]
        else:
            k = next((k for k, x in enumerate(lineas) if previa and re.match(rf"^{re.escape(previa)}:", x)), None)
            if k is not None:
                lineas.insert(k + 1, linea)
            else:
                lineas.append(linea)
        previa = clave
    return "---\n" + "\n".join(lineas) + "\n---\n" + cuerpo


def patrones_sensibles() -> list[str]:
    if not PATRONES.exists():
        return []
    return [x.strip() for x in PATRONES.read_text(encoding="utf-8").splitlines() if x.strip() and not x.startswith("#")]


# ── fuentes ───────────────────────────────────────────────────────────────────────────────────────────────────

def cargar_cursos() -> tuple[dict[str, dict], dict[str, str]]:
    """({id: curso revisado}, {id|alias|etiqueta: id} de todos los cursos)."""
    revisados, resolver = {}, {}
    voc = areas.vocabulario()
    for ruta in sorted(CURSOS.glob("*/curso.yml")):
        d = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
        cid = d.get("id") or ruta.parent.name
        for clave in [cid, *(d.get("alias") or []), d.get("etiqueta")]:
            if clave:
                resolver.setdefault(str(clave), cid)
        if d.get("temario") != "revisado":
            continue
        temas = []
        for u in d.get("unidades") or []:
            for t in u.get("temas") or []:
                temas.append({"id": str(t["id"]), "titulo": str(t.get("titulo", "")), "archivo": t.get("archivo"),
                              "unidad": u.get("id"), "orden": len(temas) + 1})
        revisados[cid] = {"id": cid, "titulo": d.get("titulo", cid), "yml": ruta, "temas": temas,
                          "pub": areas.pub_de(ruta, voc) or ""}
    return revisados, resolver


def leer_posts(pub: str) -> dict[str, dict]:
    """{ruta relativa a DOCS_ROOT de la carpeta del post: post} de las secciones del pub."""
    out = {}
    raiz = PUBS / pub
    for sec in sorted(s for s in raiz.iterdir() if s.is_dir() and not s.name.startswith((".", "_"))):
        for qmd in sorted(sec.glob("*/index.qmd")):
            texto = qmd.read_text(encoding="utf-8")
            partes = partir(texto)
            try:
                fm = (yaml.safe_load(partes[0]) or {}) if partes else {}
            except yaml.YAMLError:
                fm = {}
            info = mapa.leer_post(qmd)
            rel = str(qmd.parent.relative_to(DOCS))
            out[rel] = {"rel": rel, "dir": qmd.parent, "qmd": qmd, "seccion": sec.name, "texto": texto, "fm": fm,
                        "palabras": info["palabras"], "draft": info["draft"],
                        "curso_fm": str(fm.get("curso") or "").strip(), "tema_fm": str(fm.get("tema") or "").strip()}
    return out


def leer_mapa() -> dict[str, dict]:
    if not MAPA_CSV.exists():
        return {}
    with MAPA_CSV.open(encoding="utf-8") as f:
        return {r["ruta_post"]: r for r in csv.DictReader(f, delimiter=";")}


# ── el plan ───────────────────────────────────────────────────────────────────────────────────────────────────

def planear(curso: dict, posts: dict[str, dict], filas: dict[str, dict], resolver: dict[str, str]) -> dict:
    cid, pub = curso["id"], curso["pub"]
    temas = {t["id"]: t for t in curso["temas"]}
    plan = {"declarar": [], "retirar": [], "notas": [], "esqueletos": [], "titulos": [], "problemas": [], "avisos": [],
            "lecciones": defaultdict(list)}
    lec = plan["lecciones"]
    # 1. lo ya declarado en el frontmatter manda
    for p in posts.values():
        if p["tema_fm"] and resolver.get(p["curso_fm"]) == cid:
            if p["tema_fm"] in temas:
                lec[p["tema_fm"]].append(p)
                if p["curso_fm"] != cid:
                    plan["declarar"].append((p, p["tema_fm"], "curso: alias → id canónico"))
            else:
                plan["problemas"].append(f"{p['rel']} declara tema «{p['tema_fm']}», que no existe en {cid}/curso.yml")
    # 2. a) lecciones del mapa por declarar
    for rel, f in sorted(filas.items()):
        if f["pub"] != pub or f["curso"] != cid or f["destino"] != "leccion" or not f["tema_id"]:
            continue
        p = posts.get(rel)
        if p is None:
            plan["problemas"].append(f"el mapa cita un post que no existe: {rel}")
            continue
        if p["tema_fm"]:
            continue                                   # declarado: ya contado (o es de otro curso y manda)
        if f["tema_id"] not in temas:
            plan["problemas"].append(f"el mapa da a {rel} el tema {f['tema_id']}, que no existe en {cid}/curso.yml")
            continue
        if lec[f["tema_id"]]:
            plan["problemas"].append(f"tema {cid} {f['tema_id']}: ya lo tiene {lec[f['tema_id']][0]['rel']}; el mapa también da {rel}")
            continue
        lec[f["tema_id"]].append(p)
        plan["declarar"].append((p, f["tema_id"], f"mapa: {f['confianza']}"))
    for tid, ps in lec.items():
        if len(ps) > 1:
            plan["problemas"].append(f"tema {cid} {tid} declarado por {len(ps)} posts: " + ", ".join(x["rel"] for x in ps))
    # 3. b) duplicados que son esqueletos
    for rel, f in sorted(filas.items()):
        if f["pub"] != pub or f["curso"] != cid or f["destino"] != "revisar" or "duplica" not in f["motivo"]:
            continue
        p = posts.get(rel)
        if p is None:
            continue                                   # ya retirado; el mapa se regenera después
        if p["palabras"] == 0 and p["draft"] and not p["tema_fm"]:
            plan["retirar"].append((p, f["motivo"]))
        else:
            plan["avisos"].append(f"duplicado con texto o declarado, no se borra: {rel} ({f['motivo']})")
    # 4. secciones donde viven las lecciones (por unidad y por curso)
    por_unidad, por_curso = defaultdict(Counter), Counter()
    for tid, ps in lec.items():
        for p in ps:
            por_unidad[temas[tid]["unidad"]][p["seccion"]] += 1
            por_curso[p["seccion"]] += 1

    def seccion_de(tema: dict) -> str:
        c = por_unidad.get(tema["unidad"]) or por_curso
        return c.most_common(1)[0][0] if c else cid

    # 5. c) y d) temas sin lección
    for t in curso["temas"]:
        if lec.get(t["id"]):
            if t["archivo"] and str(t["archivo"]).startswith("02-contenido/"):
                plan["avisos"].append(f"tema {cid} {t['id']}: la nota {t['archivo']} sigue en docencia y el tema ya tiene lección "
                                      f"({lec[t['id']][0]['rel']}); fundirlas es del autor")
            continue
        archivo = str(t["archivo"] or "")
        sec = seccion_de(t)
        carpeta = f"{HOY}-{t['orden']:02d}-{slug(t['titulo'])}"
        destino = PUBS / pub / sec / carpeta
        if archivo.startswith("web/"):
            plan["problemas"].append(f"tema {cid} {t['id']}: su archivo {archivo} no es un post que declare el tema")
            continue
        if destino.exists():
            plan["problemas"].append(f"tema {cid} {t['id']}: {destino.relative_to(DOCS)} ya existe y no declara el tema")
            continue
        if archivo.startswith("02-contenido/") and (CURSOS / cid / archivo).exists():
            nota = CURSOS / cid / archivo
            texto = nota.read_text(encoding="utf-8")
            hallados = [x for x in patrones_sensibles() if x.lower() in texto.lower()]
            if hallados:
                plan["problemas"].append(f"nota {nota.relative_to(DOCS)}: casa con {len(hallados)} patrón(es) sensible(s); no se mueve")
                continue
            plan["notas"].append((t, nota, destino))
        else:
            plan["esqueletos"].append((t, destino))
    # 6. títulos de los esqueletos generados que siguen sin texto
    for p in posts.values():
        if str(p["fm"].get("generado") or "") != "curriculo" or resolver.get(p["curso_fm"]) != cid:
            continue
        t = temas.get(p["tema_fm"])
        if t and p["palabras"] == 0 and str(p["fm"].get("title") or "") != t["titulo"]:
            plan["titulos"].append((p, t))
    return plan


# ── escritura ─────────────────────────────────────────────────────────────────────────────────────────────────

def patron(pub: str, sec: str, posts: dict[str, dict]) -> dict | None:
    """El post que sirve de patrón en la sección: un borrador con menos palabras reales; si no hay, el de menos palabras."""
    cands = [p for p in posts.values() if p["seccion"] == sec and not p["fm"].get("generado")]
    if not cands:
        cands = [p for p in posts.values() if not p["fm"].get("generado")]
    if not cands:
        return None
    return min(cands, key=lambda p: (not p["draft"], p["palabras"], p["rel"]))


def etiquetas_comunes(sec: str, posts: dict[str, dict]) -> list[str]:
    conjuntos = [p["fm"].get("tags") for p in posts.values() if p["seccion"] == sec and isinstance(p["fm"].get("tags"), list)]
    if not conjuntos:
        return []
    comun = set(conjuntos[0]).intersection(*map(set, conjuntos[1:]))
    return [x for x in conjuntos[0] if x in comun]


def frontmatter_nuevo(base: dict, curso: dict, tema: dict, pub: str, sec: str, carpeta: str, posts: dict,
                      draft: bool, descripcion: str, generado: bool) -> str:
    fm = {}
    for k, v in base.items():
        if k in NO_COPIAR:
            continue
        fm[k] = v
    titulo = tema["titulo"]
    fm["title"] = titulo
    if "shorttitle" in fm:
        corto = titulo.upper()
        fm["shorttitle"] = corto if len(corto) <= 40 else corto[:40].rsplit(" ", 1)[0]
    if "copyrightnotice" in fm:
        fm["copyrightnotice"] = int(HOY[:4])
    if "tags" in fm:
        fm["tags"] = etiquetas_comunes(sec, posts)
    fm["description"] = descripcion
    if isinstance(fm.get("citation"), dict) and fm["citation"].get("pdf-url"):
        m = re.match(r"(https?://[^/]+)/", str(fm["citation"]["pdf-url"]))
        if m:
            fm["citation"] = {**fm["citation"], "pdf-url": f"{m.group(1)}/{sec}/{carpeta}/index.pdf"}
    fm["date"] = date.fromisoformat(HOY)
    fm["draft"] = draft
    fm["curso"] = curso["id"]
    fm["tema"] = tema["id"]
    if generado:
        fm["generado"] = "curriculo"
    texto = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)
    texto = re.sub(r"^tema: .*$", lambda _: linea_yaml("tema", tema["id"]).replace("'", '"'), texto, count=1, flags=re.M)
    return "---\n" + texto + "---\n"


def includes(base_post: dict | None) -> str:
    if not base_post:
        return ""
    lineas = [x for x in base_post["texto"].splitlines() if re.match(r"^\{\{<\s*include\s", x)]
    return ("\n" + "\n\n".join(lineas) + "\n") if lineas else ""


def cuerpo_esqueleto(curso: dict, tema: dict, base_post: dict | None) -> str:
    out = [f"<!-- Esqueleto generado desde el currículo (docencia/contenido/cursos/{curso['id']}/curso.yml, tema {tema['id']}) "
           f"por web/scripts/cursos.py. El cuerpo es del autor: el generador solo actualiza el título mientras siga sin texto. -->", ""]
    if base_post and mapa.PLANTILLA in base_post["texto"]:
        out += [mapa.PLANTILLA, ""]
    for sec, guia in GUIA.items():
        out += [f"## {sec}", "", f"<!-- {guia[0].upper()}{guia[1:]}" + (f"\n{QUIZ_EJEMPLO}\n" if sec == "Autoevaluación" else " ") + "-->", ""]
    return "\n".join(out) + includes(base_post)


def cuerpo_nota(nota: Path, base_post: dict | None) -> tuple[str, str]:
    """(cuerpo adaptado, descripción) de una nota de docencia: sin su frontmatter, sin lo previo a su título ni el título
    (el del post es el del tema), sin el menú final del tutor («¿Qué sigue?») y con una línea en blanco tras cada `---`
    para que Pandoc no lo lea como bloque YAML."""
    texto = nota.read_text(encoding="utf-8")
    partes = partir(texto)
    cuerpo = partes[1] if partes else texto
    lineas = cuerpo.splitlines()
    h1 = next((i for i, x in enumerate(lineas) if re.match(r"^# ", x)), None)
    if h1 is not None:
        lineas = lineas[h1 + 1:]
    lineas = [x for x in lineas if not x.startswith("> **¿Qué sigue?**")]
    out = []
    for i, x in enumerate(lineas):
        out.append(x)
        if x.strip() == "---" and i + 1 < len(lineas) and lineas[i + 1].strip():
            out.append("")
    while out and not out[-1].strip():
        out.pop()
    while out and (not out[-1].strip() or out[-1].strip() == "---"):
        out.pop()
    while out and not out[0].strip():
        out.pop(0)
    # descripción: la primera oración del primer párrafo de texto
    desc = ""
    for x in out:
        s = x.strip()
        if s and not s.startswith(("#", ">", "-", "*", "`", "|", "<", "!")) and not re.match(r"^\d+\.", s):
            desc = re.sub(r"[*_`]", "", s)
            desc = re.split(r"(?<=\.)\s", desc)[0]
            break
    return "\n".join(out) + "\n" + includes(base_post), desc


def aplicar(curso: dict, plan: dict, posts: dict[str, dict]) -> list[str]:
    cid, pub = curso["id"], curso["pub"]
    hechos = []
    # a) declarar
    for p, tid, _ in plan["declarar"]:
        texto = p["qmd"].read_text(encoding="utf-8")
        cambios = {"curso": linea_yaml("curso", cid)}
        if not re.search(r"^tema:", partir(texto)[0], re.M):
            cambios["tema"] = f'tema: "{tid}"'
        nuevo = fijar_lineas(texto, cambios)
        if nuevo != texto:
            p["qmd"].write_text(nuevo, encoding="utf-8")
            hechos.append(f"declarado {p['rel']} → {cid} {tid}")
    # b) retirar
    for p, motivo in plan["retirar"]:
        repo = PUBS / pub
        rel = str(p["dir"].relative_to(repo))
        git(repo, "rm", "-r", "-q", "--", rel)
        if (repo / "_freeze" / rel).exists() and git(repo, "ls-files", "--", f"_freeze/{rel}").strip():
            git(repo, "rm", "-r", "-q", "--", f"_freeze/{rel}")
        hechos.append(f"retirado {p['rel']} ({motivo})")
    # c) notas
    yml_texto = curso["yml"].read_text(encoding="utf-8")
    for t, nota, destino in plan["notas"]:
        sec = destino.parent.name
        base = patron(pub, sec, posts)
        cuerpo, desc = cuerpo_nota(nota, base)
        fm = frontmatter_nuevo(base["fm"] if base else {}, curso, t, pub, sec, destino.name, posts, draft=False,
                               descripcion=desc or t["titulo"], generado=False)
        destino.mkdir(parents=True)
        (destino / "index.qmd").write_text(fm + "\n" + cuerpo, encoding="utf-8")
        nuevo_archivo = str((destino / "index.qmd").relative_to(DOCS))
        patron_archivo = re.compile(rf"^(\s*archivo:\s*){re.escape(t['archivo'])}\s*$", re.M)
        if len(patron_archivo.findall(yml_texto)) != 1:
            raise RuntimeError(f"{cid}: el archivo {t['archivo']} no aparece una sola vez en curso.yml")
        yml_texto = patron_archivo.sub(lambda m: m.group(1) + nuevo_archivo, yml_texto)
        git(CONTENIDO, "rm", "-q", "--", str(nota.relative_to(CONTENIDO)))
        hechos.append(f"nota {nota.relative_to(CURSOS)} → {nuevo_archivo}")
    if plan["notas"]:
        curso["yml"].write_text(yml_texto, encoding="utf-8")
    # d) esqueletos
    for t, destino in plan["esqueletos"]:
        sec = destino.parent.name
        base = patron(pub, sec, posts)
        fm = frontmatter_nuevo(base["fm"] if base else {}, curso, t, pub, sec, destino.name, posts, draft=True,
                               descripcion=f"Lección {t['id']} de {curso['titulo']}: {t['titulo']}.", generado=True)
        destino.mkdir(parents=True)
        (destino / "index.qmd").write_text(fm + "\n" + cuerpo_esqueleto(curso, t, base), encoding="utf-8")
        hechos.append(f"esqueleto {destino.relative_to(DOCS)}")
    # títulos
    for p, t in plan["titulos"]:
        texto = p["qmd"].read_text(encoding="utf-8")
        p["qmd"].write_text(fijar_lineas(texto, {"title": linea_yaml("title", t["titulo"])}), encoding="utf-8")
        hechos.append(f"título {p['rel']} → «{t['titulo']}»")
    return hechos


# ── salida ────────────────────────────────────────────────────────────────────────────────────────────────────

def informe(curso: dict, plan: dict) -> None:
    n = len(curso["temas"])
    con = sum(1 for t in curso["temas"] if plan["lecciones"].get(t["id"]))
    print(f"== {curso['pub']} · {curso['id']}: {n} temas · {con} con lección · declarar {len(plan['declarar'])} · "
          f"retirar {len(plan['retirar'])} · notas {len(plan['notas'])} · esqueletos {len(plan['esqueletos'])} · "
          f"títulos {len(plan['titulos'])}")
    for p, tid, por in plan["declarar"]:
        print(f"   declarar  {tid:5} {p['rel']}  ({por})")
    for p, motivo in plan["retirar"]:
        print(f"   retirar         {p['rel']}  ({motivo})")
    for t, nota, destino in plan["notas"]:
        print(f"   nota      {t['id']:5} {nota.relative_to(CURSOS)} → {destino.relative_to(DOCS)}/index.qmd")
    for t, destino in plan["esqueletos"]:
        print(f"   esqueleto {t['id']:5} {destino.relative_to(DOCS)}")
    for p, t in plan["titulos"]:
        print(f"   título    {t['id']:5} {p['rel']} → «{t['titulo']}»")
    for x in plan["avisos"]:
        print(f"   aviso: {x}")
    for x in plan["problemas"]:
        print(f"   PROBLEMA: {x}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", nargs="?", choices=["generar", "verificar"], default="generar")
    ap.add_argument("--aplicar", action="store_true", help="escribe (sin él, simula)")
    ap.add_argument("--pub", action="append", default=[], help="limita a este pub (se repite)")
    ap.add_argument("--curso", action="append", default=[], help="limita a este curso (se repite)")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 2
    if a.accion == "verificar" and a.aplicar:
        print("verificar no escribe: quita --aplicar", file=sys.stderr)
        return 2
    revisados, resolver = cargar_cursos()
    desconocidos = [c for c in a.curso if c not in revisados]
    if desconocidos:
        print(f"cursos sin `temario: revisado` o inexistentes: {', '.join(desconocidos)}", file=sys.stderr)
        return 2
    cursos = [c for c in revisados.values() if (not a.curso or c["id"] in a.curso) and (not a.pub or c["pub"] in a.pub)]
    sin_pub = [c["id"] for c in cursos if not c["pub"] or not (PUBS / c["pub"]).is_dir()]
    if sin_pub:
        print(f"cursos revisados sin pub: {', '.join(sin_pub)}", file=sys.stderr)
        cursos = [c for c in cursos if c["id"] not in sin_pub]
    filas = leer_mapa()
    pendientes = problemas = 0
    hechos_total = []
    for pub in sorted({c["pub"] for c in cursos}):
        posts = leer_posts(pub)
        for curso in sorted((c for c in cursos if c["pub"] == pub), key=lambda c: c["id"]):
            plan = planear(curso, posts, filas, resolver)
            informe(curso, plan)
            n = sum(len(plan[k]) for k in ("declarar", "retirar", "notas", "esqueletos", "titulos"))
            pendientes += n
            problemas += len(plan["problemas"])
            if a.aplicar and n:
                hechos = aplicar(curso, plan, posts)
                hechos_total += hechos
                posts = leer_posts(pub)        # lo escrito cuenta para el curso siguiente del mismo pub
    print()
    if a.accion == "verificar":
        ok = pendientes == 0 and problemas == 0
        print(f"{'OK' if ok else 'FALLA'}: {len(cursos)} curso(s) revisado(s) · {pendientes} acción(es) pendiente(s) · {problemas} problema(s)")
        return 0 if ok else 1
    if a.aplicar:
        print(f"APLICADO: {len(hechos_total)} cambio(s) · {problemas} problema(s). Siguen: mapa-lecciones.py --aplicar, "
              "render y commits (web/scripts/README.md).")
        return 1 if problemas else 0
    print(f"SIMULACIÓN: {pendientes} acción(es) · {problemas} problema(s); con --aplicar se escriben.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
