#!/usr/bin/env bash
# generar-externos.sh — el hub invoca los generadores de sus maestros ajenos (ADR 14: el consumidor invoca; ola 6, 6e)
# Antes de renderizar para publicar. Cada maestro vive en su repo y aquí solo se le pide su salida:
#   temario   docencia/scripts/temario.py generar --que web  → la sección «Contenidos / Sílabo» de cursos/*/index.qmd
#   plataforma datafw/tools/plataforma.py --salida            → observatorio/plataforma.html (con marca GENERADO)
#   cv         cv/scripts/construir-pdf.sh --web               → resources/cv.pdf (perfil docencia, sin anexos; solo los
#              correos institucionales; marca GENERADO en los metadatos)
# Simula por defecto; --aplicar escribe. Los repos se buscan por CLASS_DIR y DATAFW_DIR (core/env.sh) o junto al hub;
# si uno no está (un clon del hub solo), se dice y se sigue: el hub no depende de ellos para renderizar.
# Uso: scripts/generar-externos.sh [--aplicar]      Salida: 0 bien · 1 algún generador falló
set -euo pipefail
HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APLICAR=""; [[ "${1:-}" == "--aplicar" ]] && APLICAR="--aplicar"
CLASE="${CLASS_DIR:-$HUB/../docencia}"; DATOS="${DATAFW_DIR:-$HUB/../datafw}"; CV="${CV_DIR:-$HUB/../cv}"
fallos=0
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
