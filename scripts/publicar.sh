#!/usr/bin/env bash
# publicar.sh — publica la familia de sitios: push de los pubs y después del hub (Netlify despliega con cada push)
# Antes de empujar, cada sitio debe estar limpio, con su `_site/` confirmado y la puerta R6 en verde
# (scripts/puerta-r6.sh; el hook pre-push la repite). Los pubs van primero para que el puntero del hub nunca
# apunte a un commit que GitHub no tiene. Un sitio sin commits nuevos se salta.
# Uso: scripts/publicar.sh [--pub <x>|--hub] [--aplicar]     (sin --aplicar, simula: dice qué empujaría)
# Salida: 0 bien · 1 algún sitio no está listo o un push falló · 2 uso incorrecto
set -euo pipefail
HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APLICAR=0; SOLO=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --aplicar) APLICAR=1 ;;
        --pub) SOLO="${2:?falta el pub}"; shift ;;
        --hub) SOLO="hub" ;;
        -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
        *) echo "opción desconocida: $1" >&2; exit 2 ;;
    esac
    shift
done
sitios=()
for d in "$HUB"/_pubs/pub_*; do [[ -z "$SOLO" || "$SOLO" == "${d##*/}" || "pub_$SOLO" == "${d##*/}" ]] && sitios+=("$d"); done
[[ -z "$SOLO" || "$SOLO" == "hub" ]] && sitios+=("$HUB")
fallos=0
for d in "${sitios[@]}"; do
    n="${d##*/}"; [[ "$d" == "$HUB" ]] && n="hub"
    if [[ -n "$(git -C "$d" status --porcelain --ignore-submodules=dirty)" ]]; then
        echo "✖ $n: hay cambios sin confirmar; no se publica"; fallos=1; continue
    fi
    nuevos="$(git -C "$d" rev-list --count @{u}..HEAD 2>/dev/null || echo '?')"
    [[ "$nuevos" == "0" ]] && { echo "= $n: nada que publicar"; continue; }
    if ! bash "$HUB/scripts/puerta-r6.sh" "$d" >/dev/null 2>&1; then echo "✖ $n: la puerta R6 no pasa"; fallos=1; continue; fi
    if (( APLICAR )); then
        if git -C "$d" push --quiet; then echo "✔ $n: $nuevos commits publicados"; else echo "✖ $n: falló el push"; fallos=1; fi
    else
        echo "→ $n: publicaría $nuevos commits (simulación; --aplicar empuja)"
    fi
done
exit $fallos
