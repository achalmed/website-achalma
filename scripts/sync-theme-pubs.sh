#!/usr/bin/env bash
# =============================================================================
# sync-theme-pubs.sh — Propaga el tema compartido del hub a los pubs (_pubs/), con sello THEME_VERSION.
# -----------------------------------------------------------------------------
# Fuente de verdad del tema: ESTE repositorio (website-achalma). Los 11 blogs
# satélite son submódulos en _pubs/ y reciben una copia real del tema por este
# script, el único mecanismo (ADR-06, normativa 7.11): sin hardlinks.
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
#   2. rompe TODO hardlink del pub (copia real en el mismo sitio, mismo contenido,
#      modo y fecha): con hardlinks, --verificar es ciego y editar un pub edita el hub;
#   3. escribe THEME_VERSION: commit del hub que fijó el tema por última vez y
#      sha256 del conjunto (GENERADO; no se edita).
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
# debe coincidir con el sello del hub y no tener hardlinks.
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
)
RSYNC_EXCLUDES=(--exclude '05-pages/' --exclude '.Rhistory' --exclude '.directory')
SELLO="THEME_VERSION"

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

hardlinks() {       # archivos regulares del pub con más de un enlace (fuera de .git)
    find "$1" -path "$1/.git" -prune -o -type f -links +1 -print
}

romper() {          # copia real en el mismo directorio y rename atómico: mismo contenido, modo y fecha
    local f="$1" tmp
    tmp="$(dirname "$f")/.romper.$$.$(basename "$f")"
    cp -p -- "$f" "$tmp"
    mv -f -- "$tmp" "$f"
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

    mapfile -t enlaces < <(hardlinks "$pub")
    tiene_sello=0; [[ -f "$pub/$SELLO" ]] && tiene_sello=1
    sello_igual=0; [[ $tiene_sello == 1 && "$(cat "$pub/$SELLO")" == "$SELLO_HUB" ]] && sello_igual=1

    case "$MODO" in
        aplicar)
            for f in "${enlaces[@]}"; do romper "$f"; done
            [[ ${#enlaces[@]} -gt 0 ]] && cambios+="  ${#enlaces[@]} hardlinks rotos (copia real, mismo contenido)"$'\n'
            if [[ $sello_igual == 0 ]]; then
                printf '%s\n' "$SELLO_HUB" > "$pub/$SELLO"
                cambios+="  $SELLO escrito"$'\n'
            fi
            ;;
        verificar)
            if [[ $tiene_sello == 1 ]]; then
                [[ $sello_igual == 0 ]] && cambios+="  $SELLO distinto del sello del hub"$'\n'
                [[ ${#enlaces[@]} -gt 0 ]] && cambios+="  ${#enlaces[@]} hardlinks: la verificación sería ciega"$'\n'
            fi
            ;;
        *)
            [[ ${#enlaces[@]} -gt 0 ]] && cambios+="  romper ${#enlaces[@]} hardlinks"$'\n'
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
        echo "    · sin $SELLO y con ${#enlaces[@]} hardlinks: pendiente de --aplicar (ola 6); con hardlinks esta verificación es ciega"
    fi
done

echo "── $MODO: ${#PUBS[@]} blogs, $difieren con diferencias"
[[ "$MODO" == "verificar" && $difieren -gt 0 ]] && exit 1
exit 0
