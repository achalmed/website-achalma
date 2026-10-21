#!/usr/bin/env bash
# api/detener.sh — detiene la API del aula y su base (docker compose down). Conserva los datos: el volumen «aula-db»
# y AULA_DATOS_DIR no se tocan. --dry-run muestra lo que haría.
set -euo pipefail

DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
ENTORNO="${XDG_CONFIG_HOME:-$HOME/.config}/aula/aula.env"
PIDFILE="${XDG_STATE_HOME:-$HOME/.local/state}/aula/api.pid"

SECO=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) SECO=1 ;;
    -h|--help) sed -n '2,3p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argumento desconocido: $arg (use --help)" >&2; exit 2 ;;
  esac
done
hacer() { if [ "$SECO" = 1 ]; then printf '  [simulación] %s\n' "$*"; else "$@"; fi; }

if [ -f "$PIDFILE" ]; then
  pid="$(cat "$PIDFILE")"
  if kill -0 "$pid" 2>/dev/null; then
    echo "→ deteniendo la API (pid $pid)"
    hacer kill "$pid"
  fi
  hacer rm -f "$PIDFILE"
fi

cd "$DIR"
# `down` interpola el compose: sin aula.env basta un valor cualquiera, la clave no se usa para detener.
if [ -f "$ENTORNO" ]; then
  opciones=(--env-file "$ENTORNO")
else
  export AULA_POSTGRES_CLAVE=- AULA_JWT_SECRETO=- AULA_DATOS_DIR=/nada
  opciones=()
fi
echo "→ docker compose down (los datos se conservan)"
hacer docker compose "${opciones[@]}" --profile api down
