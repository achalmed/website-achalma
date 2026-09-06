#!/usr/bin/env bash
# =============================================================================
# sync-theme-pubs.sh — Propaga el tema compartido del hub a los pub_* (_pubs/).
# -----------------------------------------------------------------------------
# Fuente de verdad del tema: ESTE repositorio (website-achalma). Los 11 blogs
# satélite son submódulos en _pubs/pub_* y llevaban copias idénticas del tema;
# desde 2026-09-06 se editan aquí y se propagan con este script.
#
# Conjunto sincronizado (THEME_PATHS): extensiones vendorizadas, filtro Lua de
# flotantes APA, SCSS base (todo menos 05-pages), JS, CSS global y de
# componentes, y el compilador de CSS por página.
# Excluidos A PROPÓSITO (difieren entre hub y satélites por diseño):
#   assets/scss/05-pages/, assets/css/pages/, _filters/_metadata-pdf.lua,
#   _quarto.yml, index.qmd, assets/img/, assets/fonts/, assets/gtm-*.html.
#
# Uso:
#   scripts/sync-theme-pubs.sh              # simula (muestra qué cambiaría)
#   scripts/sync-theme-pubs.sh --aplicar    # escribe en los submódulos
#   scripts/sync-theme-pubs.sh --verificar  # sale 1 si algún pub_* difiere (doctor)
#   scripts/sync-theme-pubs.sh --solo pub_axiomata [--aplicar]
# Tras --aplicar: revisar, hacer commit en cada pub_* y luego en el hub
# (actualiza los punteros de submódulo). Ver docs/pubs-submodulos.md.
# =============================================================================
set -euo pipefail

HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PUBS_DIR="$HUB/_pubs"
THEME_PATHS=(
    "_extensions/"
    "_filters/apa-floats-html.lua"
    "assets/scss/"
    "assets/js/"
    "assets/css/global.css"
    "assets/css/components/"
    "scripts/build-page-css.sh"
)
RSYNC_EXCLUDES=(--exclude '05-pages/' --exclude '.Rhistory' --exclude '.directory')

MODO="simular"; SOLO=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --aplicar)   MODO="aplicar" ;;
        --verificar) MODO="verificar" ;;
        --solo)      SOLO="$2"; shift ;;
        -h|--help)   sed -n '2,22p' "$0"; exit 0 ;;
        *) echo "Opción desconocida: $1" >&2; exit 2 ;;
    esac
    shift
done

command -v rsync >/dev/null || { echo "Falta rsync" >&2; exit 5; }
[[ -d "$PUBS_DIR" ]] || { echo "No existe $PUBS_DIR" >&2; exit 3; }

mapfile -t PUBS < <(find "$PUBS_DIR" -mindepth 1 -maxdepth 1 -type d -name 'pub_*' | sort)
[[ -n "$SOLO" ]] && PUBS=("$PUBS_DIR/${SOLO#"$PUBS_DIR"/}")

difieren=0
for pub in "${PUBS[@]}"; do
    [[ -d "$pub" ]] || { echo "No existe: $pub" >&2; exit 3; }
    nombre="$(basename "$pub")"
    cambios=""
    for rel in "${THEME_PATHS[@]}"; do
        src="$HUB/$rel"; dst="$pub/$rel"
        [[ -e "$src" ]] || { echo "  [$nombre] falta en el hub: $rel" >&2; continue; }
        if [[ "$rel" == */ ]]; then
            mkdir -p "$dst"
            out="$(rsync -rci --delete "${RSYNC_EXCLUDES[@]}" $([[ "$MODO" == "aplicar" ]] || echo --dry-run) "$src" "$dst")"
        else
            mkdir -p "$(dirname "$dst")"
            out="$(rsync -ci $([[ "$MODO" == "aplicar" ]] || echo --dry-run) "$src" "$dst")"
        fi
        [[ -n "$out" ]] && cambios+="$out"$'\n'
    done
    if [[ -n "$cambios" ]]; then
        difieren=$((difieren + 1))
        case "$MODO" in
            aplicar)   echo "✔ $nombre: tema actualizado"; printf '%s' "$cambios" | sed 's/^/    /' ;;
            verificar) echo "✖ $nombre: difiere del hub"; printf '%s' "$cambios" | sed 's/^/    /' ;;
            *)         echo "→ $nombre: cambiaría (simulación)"; printf '%s' "$cambios" | sed 's/^/    /' ;;
        esac
    else
        echo "= $nombre: al día"
    fi
done

echo "── $MODO: ${#PUBS[@]} blogs, $difieren con diferencias"
[[ "$MODO" == "verificar" && $difieren -gt 0 ]] && exit 1
exit 0
