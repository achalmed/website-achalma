#!/usr/bin/env bash
# =============================================================================
# sync-theme-pubs.sh — Propaga el tema compartido del hub a los pubs (_pubs/), con sello THEME_VERSION.
# -----------------------------------------------------------------------------
# Fuente de verdad del tema: ESTE repositorio (website-achalma). Los 11 blogs
# satélite son submódulos en _pubs/ y comparten el tema con el hub por HARDLINKS
# (decisión del autor, 2026-10-08; ADR-06 revisado, normativa 7.11): editar el tema
# en un sitio lo cambia en los doce. Este script es el único mecanismo: iguala el
# contenido y deja que scripts-linux/script_hardlinks-creator enlace.
#
# Conjunto sincronizado (THEME_PATHS): extensiones vendorizadas, filtro Lua de
# flotantes APA, SCSS base (todo menos 05-pages), JS, CSS global y de
# componentes, y el compilador de CSS por página.
# Excluidos A PROPÓSITO (difieren entre hub y satélites por diseño):
#   assets/scss/05-pages/, assets/css/pages/, _filters/_metadata-pdf.lua,
#   _quarto.yml, index.qmd, assets/img/, assets/fonts/, assets/gtm-*.html.
#
# Con --aplicar, en cada pub elegido:
#   1. rsync del conjunto (solo lo que difiere, por suma);
#   2. escribe THEME_VERSION: commit del hub que fijó el tema por última vez y
#      sha256 del conjunto (GENERADO; no se edita);
#   3. al final, una sola vez, enlaza por hardlink los archivos de igual nombre y
#      contenido de scripts/tema-hardlinks.txt en todo el hub (script_hardlinks-creator
#      --batch; _site/ y _extensions/ quedan fuera, a cualquier profundidad).
# rsync reescribe un archivo distinto con un temporal y lo renombra (rompe su enlace);
# git checkout y los editores que guardan por renombrado también: el paso 3 lo repara
# y --verificar lo detecta (sale 1 si un archivo de la lista quedó sin enlazar).
#
# Uso:
#   scripts/sync-theme-pubs.sh                         # simula en los 11 (qué cambiaría)
#   scripts/sync-theme-pubs.sh --pub methodica         # simula en uno (pub_methodica o methodica)
#   scripts/sync-theme-pubs.sh --pub methodica --aplicar
#   scripts/sync-theme-pubs.sh --verificar             # sale 1 si algún pub difiere (doctor)
#   scripts/sync-theme-pubs.sh --sello                 # imprime el THEME_VERSION que corresponde al hub
#   (--solo es sinónimo de --pub)
# Transición (ola 6): un pub sin THEME_VERSION aún no pasó por --aplicar con esta
# versión; --verificar lo informa sin contarlo como deriva. Un pub con THEME_VERSION
# debe coincidir con el sello del hub.
# Tras --aplicar: revisar, hacer commit en cada pub y luego en el hub
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
    "scripts/fechas-desde-git.py"
    "scripts/render.sh"
)
RSYNC_EXCLUDES=(--exclude '05-pages/' --exclude '.Rhistory' --exclude '.directory')
SELLO="THEME_VERSION"
LISTA="$HUB/scripts/tema-hardlinks.txt"
CREADOR="${SCRIPTS_LINUX:-$HUB/../scripts-linux}/script_hardlinks-creator/main.py"

MODO="simular"; SOLO=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --aplicar)    MODO="aplicar" ;;
        --verificar)  MODO="verificar" ;;
        --sello)      MODO="sello" ;;
        --pub|--solo) SOLO="${2:?falta el nombre del pub}"; shift ;;
        -h|--help)    sed -n '2,34p' "$0"; exit 0 ;;
        *) echo "Opción desconocida: $1" >&2; exit 2 ;;
    esac
    shift
done

command -v rsync >/dev/null || { echo "Falta rsync" >&2; exit 5; }
[[ -d "$PUBS_DIR" ]] || { echo "No existe $PUBS_DIR" >&2; exit 3; }

# Archivos del conjunto bajo una raíz (hub o pub), relativos y ordenados; mismas exclusiones que el rsync.
conjunto() {
    local raiz="$1" rel
    for rel in "${THEME_PATHS[@]}"; do
        if [[ "$rel" == */ ]]; then
            [[ -d "$raiz/$rel" ]] || continue
            (cd "$raiz" && find "${rel%/}" -type f -not -path '*/05-pages/*' -not -name '.Rhistory' -not -name '.directory')
        else
            [[ -f "$raiz/$rel" ]] && echo "$rel"
        fi
    done | LC_ALL=C sort
}

suma_conjunto() {   # sha256 de la lista «suma  ruta» del conjunto
    local raiz="$1"
    conjunto "$raiz" | (cd "$raiz" && tr '\n' '\0' | xargs -0 -r sha256sum) | sha256sum | cut -d' ' -f1
}

texto_sello() {
    local commit n
    commit="$(git -C "$HUB" log -1 --format=%H -- "${THEME_PATHS[@]}" 2>/dev/null || echo desconocido)"
    n="$(conjunto "$HUB" | wc -l)"
    printf '%s\n' \
        "# THEME_VERSION — GENERADO por \`04 index/scripts/sync-theme-pubs.sh --aplicar\` desde el hub (website-achalma); no editar aquí" \
        "# Sello del tema compartido (ADR-06, normativa 7.11): commit del hub que lo fijó por última vez y sha256 del conjunto." \
        "commit_hub: $commit" \
        "sha256_conjunto: $(suma_conjunto "$HUB")" \
        "archivos: $n"
}

enlazar() {         # $1 = --dry-run o nada; imprime cuántos hardlinks crea (o crearía) el creador en el hub
    local out
    [[ -f "$CREADOR" && -f "$LISTA" ]] || { echo "Falta $CREADOR o $LISTA" >&2; exit 5; }
    out="$(python3 "$CREADOR" --batch "$LISTA" -d "$HUB" --auto --no-color ${1:+"$1"} 2>&1)" || { printf '%s\n' "$out" >&2; exit 6; }
    sed -n 's/.*Hard links creados: *\([0-9]*\).*/\1/p' <<<"$out" | tail -1
}

resolver_pub() {
    local x="${1#"$PUBS_DIR"/}"
    if [[ -d "$PUBS_DIR/$x" ]]; then echo "$PUBS_DIR/$x"
    elif [[ -d "$PUBS_DIR/pub_$x" ]]; then echo "$PUBS_DIR/pub_$x"
    else echo "No existe el pub: $1" >&2; exit 3; fi
}

if [[ "$MODO" == "sello" ]]; then texto_sello; exit 0; fi

if [[ "$MODO" == "aplicar" && -n "$(git -C "$HUB" status --porcelain -- "${THEME_PATHS[@]}" 2>/dev/null)" ]]; then
    echo "El tema del hub tiene cambios sin confirmar: confírmalos antes de --aplicar (el sello cita un commit)." >&2
    exit 4
fi

if [[ -n "$SOLO" ]]; then
    PUBS=("$(resolver_pub "$SOLO")")
else
    mapfile -t PUBS < <(find "$PUBS_DIR" -mindepth 1 -maxdepth 1 -type d -not -name '.*' | sort)
fi
SELLO_HUB="$(texto_sello)"
DRY=(--dry-run); [[ "$MODO" == "aplicar" ]] && DRY=()

difieren=0
for pub in "${PUBS[@]}"; do
    [[ -f "$pub/_quarto.yml" ]] || continue
    nombre="$(basename "$pub")"
    cambios=""
    for rel in "${THEME_PATHS[@]}"; do
        src="$HUB/$rel"; dst="$pub/$rel"
        [[ -e "$src" ]] || { echo "  [$nombre] falta en el hub: $rel" >&2; continue; }
        if [[ "$rel" == */ ]]; then
            [[ "$MODO" == "aplicar" ]] && mkdir -p "$dst"
            out="$(rsync -rci --delete "${RSYNC_EXCLUDES[@]}" "${DRY[@]}" "$src" "$dst")"
            [[ -d "$dst" || "$MODO" == "aplicar" ]] || out="  falta $rel"
        else
            [[ "$MODO" == "aplicar" ]] && mkdir -p "$(dirname "$dst")"
            out="$(rsync -ci "${DRY[@]}" "$src" "$dst")"
        fi
        [[ -n "$out" ]] && cambios+="$out"$'\n'
    done

    tiene_sello=0; [[ -f "$pub/$SELLO" ]] && tiene_sello=1
    sello_igual=0; [[ $tiene_sello == 1 && "$(cat "$pub/$SELLO")" == "$SELLO_HUB" ]] && sello_igual=1
    # La deriva es de contenido: un commit del hub que solo toca comentarios mueve commit_hub pero no el sha256 del
    # conjunto, y eso no es deriva (ola 3: el renombre 02 analysis → datafw tocó un comentario de _quarto.yml).
    conjunto_igual=0
    [[ $tiene_sello == 1 && "$(grep '^sha256_conjunto:' "$pub/$SELLO")" == "$(grep '^sha256_conjunto:' <<<"$SELLO_HUB")" ]] && conjunto_igual=1

    case "$MODO" in
        aplicar)
            if [[ $sello_igual == 0 ]]; then
                printf '%s\n' "$SELLO_HUB" > "$pub/$SELLO"
                cambios+="  $SELLO escrito"$'\n'
            fi
            ;;
        verificar)
            if [[ $tiene_sello == 1 ]]; then
                [[ $conjunto_igual == 0 ]] && cambios+="  $SELLO distinto del sello del hub (sha256 del conjunto)"$'\n'
            fi
            ;;
        *)
            [[ $sello_igual == 0 ]] && cambios+="  $SELLO $([[ $tiene_sello == 1 ]] && echo 'se reescribiría' || echo 'se crearía')"$'\n'
            ;;
    esac

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
    if [[ "$MODO" == "verificar" && $tiene_sello == 0 ]]; then
        echo "    · sin $SELLO: pendiente de --aplicar (ola 6)"
    fi
done

case "$MODO" in
    aplicar) n="$(enlazar)"; echo "── hardlinks del tema: ${n:-0} creados (scripts/tema-hardlinks.txt)" ;;
    *)       n="$(enlazar --dry-run)"
             [[ "${n:-0}" -gt 0 ]] && { echo "✖ hardlinks del tema: ${n} archivos de la lista sin enlazar (--aplicar los enlaza)"; difieren=$((difieren + 1)); }
             [[ "${n:-0}" -eq 0 ]] && echo "= hardlinks del tema: todo enlazado" ;;
esac
echo "── $MODO: ${#PUBS[@]} blogs, $difieren con diferencias"
[[ "$MODO" == "verificar" && $difieren -gt 0 ]] && exit 1
exit 0
