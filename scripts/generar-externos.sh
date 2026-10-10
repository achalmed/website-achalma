#!/usr/bin/env bash
# generar-externos.sh — el hub invoca los generadores de sus maestros ajenos (ADR 14: el consumidor invoca; ola 6, 6e)
# Antes de renderizar para publicar. Cada maestro vive en su repo y aquí solo se le pide su salida:
#   temario   docencia/scripts/temario.py generar --que web  → la sección «Contenidos / Sílabo» de cursos/*/index.qmd
#   plataforma datafw/tools/plataforma.py --salida            → observatorio/plataforma.html (con marca GENERADO)
#   cv         cv/scripts/construir-pdf.sh --web               → resources/cv.pdf (perfil docencia, sin anexos; solo los
#              correos institucionales; marca GENERADO en los metadatos)
# Simula por defecto; --aplicar escribe. Los repos se buscan por CLASS_DIR y DATAFW_DIR (core/env.sh) o junto al hub;
# si uno no está (un clon del hub solo), se dice y se sigue: el hub no depende de ellos para renderizar.
# --verificar (el doctor, RQ-DOC-07): en seco, cada derivado está confirmado en el hub después del último commit de
# su maestro (fechas de commit, no de archivo) y lleva la marca GENERADO; sale 1 si alguno está desfasado.
# Uso: scripts/generar-externos.sh [--aplicar|--verificar]      Salida: 0 bien · 1 algún generador falló o derivado desfasado
set -euo pipefail
HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APLICAR=""; [[ "${1:-}" == "--aplicar" ]] && APLICAR="--aplicar"
CLASE="${CLASS_DIR:-$HUB/../docencia}"; DATOS="${DATAFW_DIR:-$HUB/../datafw}"; CV="${CV_DIR:-$HUB/../cv}"
fallos=0
if [[ "${1:-}" == "--verificar" ]]; then
    # derivado en el hub · repo maestro · rutas del maestro que lo producen · marca que debe llevar (vacío: ninguna)
    verificar() {
        local derivado="$1" maestro="$2" rutas="$3" marca="$4" t_der t_mae ultimo
        if [[ ! -d "$maestro/.git" && ! -f "$maestro/.git" ]]; then echo "= $derivado: no está el maestro $maestro (se omite)"; return; fi
        t_der="$(git -C "$HUB" log -1 --format=%ct -- "$derivado")"
        [[ -n "$t_der" ]] || { echo "✖ $derivado: no está confirmado en el hub"; fallos=1; return; }
        # shellcheck disable=SC2086
        t_mae="$(git -C "$maestro" log -1 --format=%ct -- $rutas)"
        if [[ -n "$t_mae" && "$t_mae" -gt "$t_der" ]]; then
            # shellcheck disable=SC2086
            ultimo="$(git -C "$maestro" log -1 --format='%h %s' -- $rutas | cut -c1-70)"
            echo "✖ $derivado: desfasado; el maestro cambió después ($ultimo): scripts/generar-externos.sh --aplicar"; fallos=1; return
        fi
        if [[ -n "$marca" ]]; then      # un PDF lleva la marca en sus metadatos (Subject), no en bytes legibles
            if [[ "$derivado" == *.pdf ]]; then pdfinfo "$HUB/$derivado" 2>/dev/null | grep -q -- "$marca" || { echo "✖ $derivado: sin la marca «$marca» en sus metadatos"; fallos=1; return; }
            elif ! grep -aq -- "$marca" "$HUB/$derivado"; then echo "✖ $derivado: sin la marca «$marca»"; fallos=1; return; fi
        fi
        echo "✔ $derivado: confirmado después del último commit de su maestro"
    }
    verificar resources/cv.pdf "$CV" "main scripts Makefile" "GENERADO"
    verificar observatorio/plataforma.html "$DATOS" "tools/plataforma.py data/publicado" "GENERADO"
    exit $fallos
fi
if [[ -f "$CLASE/scripts/temario.py" ]]; then
    echo "── temario (docencia)"; python3 "$CLASE/scripts/temario.py" generar --que web $APLICAR | tail -3 || fallos=1
else echo "── temario: no está $CLASE/scripts/temario.py (se omite)"; fi
if [[ -f "$DATOS/tools/plataforma.py" ]]; then
    if [[ -n "$APLICAR" ]]; then
        echo "── plataforma (datafw)"; (cd "$DATOS" && python3 tools/plataforma.py --salida "$HUB/observatorio/plataforma.html") | tail -1 || fallos=1
    else echo "── plataforma (datafw): regeneraría observatorio/plataforma.html (simulación; --aplicar escribe)"; fi
else echo "── plataforma: no está $DATOS/tools/plataforma.py (se omite)"; fi
if [[ -x "$CV/scripts/construir-pdf.sh" ]]; then
    echo "── cv"; "$CV/scripts/construir-pdf.sh" --perfil docencia --sin-anexos --web --salida "$HUB/resources/cv.pdf" $APLICAR | tail -2 || fallos=1
else echo "── cv: no está $CV/scripts/construir-pdf.sh (se omite)"; fi
exit $fallos
