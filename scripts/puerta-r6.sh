#!/usr/bin/env bash
# =============================================================================
# puerta-r6.sh — Puerta de publicación R6 de la familia Quarto (normativa 7.10, RQ-PRE-03).
# -----------------------------------------------------------------------------
# Un sitio no se empuja si su `_site/index.html` falta, está vacío o es más viejo
# que el `.qmd` rastreado más reciente (Netlify sirve el `_site/` empujado, sin
# build: un push sin render publica un sitio vacío o viejo; decisiones §4.1–§4.3).
#
# Uso:
#   scripts/puerta-r6.sh [<carpeta del sitio>]          # comprueba (por defecto, el hub); 0 pasa · 1 no pasa
#   scripts/puerta-r6.sh --instalar --pub methodica     # simula instalar el hook pre-push en ese pub
#   scripts/puerta-r6.sh --instalar --pub methodica --aplicar
#   scripts/puerta-r6.sh --desinstalar --pub methodica --aplicar
# Como hook (`<repo>/.git/hooks/pre-push`, copia de este archivo) comprueba el repo
# que empuja; git aborta el push si sale distinto de 0 (Pro Git §8.3).
# Límite: no sabe si el push lleva `_site/`; solo que el render local está al día.
# =============================================================================
set -euo pipefail

HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARCA="# pre-push — GENERADO por \`04 index/scripts/puerta-r6.sh --instalar\`; no editar aquí"

comprobar() {
    local sitio="$1" idx mas="" t tmax=0 f
    idx="$sitio/_site/index.html"
    if [[ ! -s "$idx" ]]; then
        echo "✖ R6: $sitio sin _site/index.html (o vacío): renderiza antes de empujar" >&2; return 1
    fi
    while IFS= read -r -d '' f; do
        [[ "$f" == _site/* || "$f" == _freeze/* ]] && continue
        [[ -e "$sitio/$f" ]] || continue
        t="$(stat -c %Y -- "$sitio/$f")"
        if (( t > tmax )); then tmax=$t; mas="$f"; fi
    done < <(git -C "$sitio" ls-files -z -- '*.qmd')
    if (( tmax > $(stat -c %Y -- "$idx") )); then
        echo "✖ R6: _site/index.html es más viejo que $mas: renderiza antes de empujar" >&2; return 1
    fi
    echo "✔ R6: _site/index.html presente, no vacío y al día (fuente más reciente: ${mas:-ninguna})"
}

# Invocado como hook pre-push: comprobar el repo que empuja.
if [[ "$(basename "$0")" == "pre-push" ]]; then
    comprobar "$(git rev-parse --show-toplevel)"; exit $?
fi

ACCION=""; PUB=""; APLICAR=0; SITIO=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --instalar)    ACCION="instalar" ;;
        --desinstalar) ACCION="desinstalar" ;;
        --pub)         PUB="${2:?falta el nombre del pub}"; shift ;;
        --aplicar)     APLICAR=1 ;;
        -h|--help)     sed -n '2,18p' "$0"; exit 0 ;;
        -*)            echo "Opción desconocida: $1" >&2; exit 2 ;;
        *)             SITIO="$1" ;;
    esac
    shift
done

if [[ -z "$ACCION" ]]; then comprobar "${SITIO:-$HUB}"; exit $?; fi

[[ -n "$PUB" ]] || { echo "--$ACCION exige --pub <x>" >&2; exit 2; }
if [[ -d "$HUB/_pubs/$PUB" ]]; then dir="$HUB/_pubs/$PUB"
elif [[ -d "$HUB/_pubs/pub_$PUB" ]]; then dir="$HUB/_pubs/pub_$PUB"
else echo "No existe el pub: $PUB" >&2; exit 3; fi
hooks="$(git -C "$dir" rev-parse --path-format=absolute --git-path hooks)"
destino="$hooks/pre-push"
if [[ -e "$destino" ]] && ! grep -qF "GENERADO por \`04 index/scripts/puerta-r6.sh" "$destino"; then
    echo "$destino ya existe y no es de esta herramienta: no se toca" >&2; exit 4
fi
case "$ACCION" in
    instalar)
        if (( APLICAR )); then
            mkdir -p "$hooks"
            { echo '#!/usr/bin/env bash'; echo "$MARCA"; sed -n '2,$p' "${BASH_SOURCE[0]}"; } > "$destino"
            chmod +x "$destino"; echo "✔ hook pre-push instalado en $destino"
        else
            echo "→ instalaría el hook pre-push en $destino (simulación; --aplicar escribe)"
        fi ;;
    desinstalar)
        if [[ ! -e "$destino" ]]; then echo "= no hay hook pre-push en $destino"
        elif (( APLICAR )); then rm -f -- "$destino"; echo "✔ hook pre-push retirado de $destino"
        else echo "→ retiraría $destino (simulación; --aplicar escribe)"; fi ;;
esac
