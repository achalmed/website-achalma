#!/usr/bin/env bash
# =============================================================================
# puerta-r6.sh — Puerta de publicación R6 de la familia Quarto (normativa 7.10, RQ-PRE-03).
# -----------------------------------------------------------------------------
# No se empuja un sitio sin `_site/index.html` (o vacío), con fuentes sin confirmar
# o con una fuente confirmada después que `_site/index.html`: se comparan fechas de
# commit (`git log -1 --format=%ct`), no de archivo, que un reset o un clon reescriben
# (lección 3.6 g). Fuentes: `.qmd`, `_quarto.yml`, `_metadata.yml` y el tema (FUENTES).
# `_site/index.html` sin confirmar (recién renderizado) pasa; si un render confirmado
# no lo cambió, vale el último commit de `_site/` (el hub el 2026-09-28, 79bfb9b).
# Uso:
#   scripts/puerta-r6.sh [<carpeta del sitio>]          # comprueba (por defecto, el hub); 0 pasa · 1 no pasa
#   scripts/puerta-r6.sh --instalar --pub methodica [--aplicar]     # hook pre-push en ese pub (simula sin --aplicar)
#   scripts/puerta-r6.sh --desinstalar --pub methodica --aplicar
#   scripts/prueba-puerta-r6.sh                          # sus casos en un repo temporal
# Como hook (`<repo>/.git/hooks/pre-push`) comprueba el repo que empuja; git aborta el push si sale ≠ 0.
# Límite: no sabe si el push lleva `_site/`; solo que el render confirmado está al día.
# =============================================================================
set -euo pipefail

HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARCA="# pre-push — GENERADO por \`04 index/scripts/puerta-r6.sh --instalar\`; no editar aquí"
# Fuentes del sitio (pathspecs de git, relativos a la raíz del sitio); _site/ y _freeze/ nunca lo son.
FUENTES=(':(glob)**/*.qmd' ':(glob)**/_quarto.yml' ':(glob)**/_metadata.yml'
         '_extensions/' '_filters/' '_partials/' 'assets/scss/' 'assets/js/' 'assets/css/'
         '_brand.yml' 'THEME_VERSION'
         ':(exclude)_site/' ':(exclude)_freeze/' ':(exclude,glob)**/README.md')   # la guía de una carpeta del tema no se publica

comprobar() {
    local sitio="$1" idx sucias t_idx t_site salida t_src f_src
    idx="$sitio/_site/index.html"
    if [[ ! -s "$idx" ]]; then
        echo "✖ R6: $sitio sin _site/index.html (o vacío): renderiza antes de empujar" >&2; return 1
    fi
    sucias="$(git -C "$sitio" status --porcelain --untracked-files=all -- "${FUENTES[@]}")"
    if [[ -n "$sucias" ]]; then
        echo "✖ R6: fuentes con cambios sin confirmar ($(wc -l <<<"$sucias") ruta(s), p. ej. $(head -1 <<<"$sucias" | cut -c4-)): confirma y renderiza antes de empujar" >&2
        return 1
    fi
    if [[ -n "$(git -C "$sitio" status --porcelain --untracked-files=all -- _site/index.html)" ]]; then
        echo "✔ R6: _site/index.html recién renderizado (sin confirmar) y fuentes confirmadas"; return 0
    fi
    t_idx="$(git -C "$sitio" log -1 --format=%ct -- _site/index.html)"
    if [[ -z "$t_idx" ]]; then
        echo "✖ R6: _site/index.html no está en git (el sitio publica su _site/ versionado; decisiones §4.1)" >&2; return 1
    fi
    salida="$(git -C "$sitio" -c core.quotePath=false log -1 --format=%ct --name-only -- "${FUENTES[@]}")"
    t_src="$(sed -n 1p <<<"$salida")"
    f_src="$(sed '/^$/d' <<<"$salida" | sed -n 2p)"
    if [[ -n "$t_src" ]] && (( t_src > t_idx )); then
        t_site="$(git -C "$sitio" log -1 --format=%ct -- _site/)"
        if (( t_site >= t_src )); then
            echo "✔ R6: _site/ confirmado después de la última fuente ($f_src); _site/index.html no cambió en ese render"
            return 0
        fi
        echo "✖ R6: el último commit de _site/index.html es anterior al de $f_src: renderiza y confirma antes de empujar" >&2
        return 1
    fi
    echo "✔ R6: _site/index.html presente, no vacío y confirmado después de la última fuente (${f_src:-ninguna})"
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
        -h|--help)     sed -n '2,/^# =\{10,\}$/p' "$0"; exit 0 ;;
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
