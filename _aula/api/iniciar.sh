#!/usr/bin/env bash
# api/iniciar.sh — levanta el aula en la laptop: PostgreSQL 16 (docker compose), crea las tablas y arranca la API.
#
#   ./iniciar.sh                 base en 127.0.0.1:5442 y API (uvicorn de .venv) en 127.0.0.1:8040, en segundo plano
#   ./iniciar.sh --primer-plano  igual, con la API en esta terminal (Ctrl+C la detiene; la base sigue: ./detener.sh)
#   ./iniciar.sh --docker        la API también en contenedor (perfil «api» del compose)
#   ./iniciar.sh --dry-run       muestra lo que haría, sin tocar nada
#
# La primera vez crea $XDG_CONFIG_HOME/aula/aula.env (permisos 600) con una clave de base y un secreto JWT al azar,
# y AULA_DATOS_DIR (por omisión $XDG_DATA_HOME/aula). Nada de eso entra al repo. NO publica el aula en internet:
# exponerla con Tailscale Funnel lo decide el autor (README §Uso). Se detiene con ./detener.sh.
set -euo pipefail

DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/aula"
ESTADO_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/aula"
ENTORNO="$CONFIG_DIR/aula.env"
PIDFILE="$ESTADO_DIR/api.pid"
REGISTRO="$ESTADO_DIR/api.log"
PUERTO_API="${AULA_PUERTO_API:-8040}"
PUERTO_DB="${AULA_PUERTO_DB:-5442}"

SECO=0; DOCKER=0; PRIMER_PLANO=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) SECO=1 ;;
    --docker) DOCKER=1 ;;
    --primer-plano) PRIMER_PLANO=1 ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argumento desconocido: $arg (use --help)" >&2; exit 2 ;;
  esac
done

paso() { printf '→ %s\n' "$*"; }
hacer() { if [ "$SECO" = 1 ]; then printf '  [simulación] %s\n' "$*"; else "$@"; fi; }

command -v docker >/dev/null || { echo "falta docker" >&2; exit 1; }
cd "$DIR"

# 1. Entorno virtual (solo si la API corre en esta máquina).
if [ "$DOCKER" = 0 ] && [ ! -x "$DIR/.venv/bin/uvicorn" ]; then
  paso "creando .venv e instalando requirements.txt"
  hacer python3 -m venv "$DIR/.venv"
  hacer "$DIR/.venv/bin/pip" install -q -r "$DIR/requirements.txt"
fi

# 2. Configuración fuera del repo.
if [ ! -f "$ENTORNO" ]; then
  paso "creando $ENTORNO (clave de base y secreto JWT al azar)"
  if [ "$SECO" = 0 ]; then
    mkdir -p -m 700 "$CONFIG_DIR"
    umask 077
    python3 - "$ENTORNO" <<'PY'
import os, secrets, sys
datos = os.path.join(os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share"), "aula")
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("# aula.env — configuración local del aula (secretos); NO se versiona. Ver web/_aula/api/README.md.\n")
    f.write(f"AULA_POSTGRES_CLAVE={secrets.token_urlsafe(24)}\n")
    f.write(f"AULA_JWT_SECRETO={secrets.token_urlsafe(48)}\n")
    f.write(f"AULA_DATOS_DIR={datos}\n")
    f.write("# Respaldo cifrado (respaldar.sh): descomente uno, con el destinatario age (age1…) o la clave gpg.\n")
    f.write("# AULA_RESPALDO_AGE=age1...\n# AULA_RESPALDO_GPG=correo-o-id-de-la-clave\n")
PY
    chmod 600 "$ENTORNO"
  fi
fi
if [ -f "$ENTORNO" ]; then
  set -a; # shellcheck disable=SC1090
  source "$ENTORNO"; set +a
fi

# 3. Base de datos (y la API, si va en contenedor).
if [ "$DOCKER" = 1 ]; then
  paso "docker compose --profile api up -d --build (base en :$PUERTO_DB, API en :$PUERTO_API)"
  hacer docker compose --env-file "$ENTORNO" --profile api up -d --build
else
  paso "docker compose up -d db (127.0.0.1:$PUERTO_DB)"
  hacer docker compose --env-file "$ENTORNO" up -d db
fi
if [ "$SECO" = 0 ]; then
  for _ in $(seq 1 40); do
    docker compose --env-file "$ENTORNO" exec -T db pg_isready -h 127.0.0.1 -U aula -d aula >/dev/null 2>&1 && break
    sleep 1
  done
  docker compose --env-file "$ENTORNO" exec -T db pg_isready -h 127.0.0.1 -U aula -d aula >/dev/null || { echo "la base no respondió" >&2; exit 1; }
fi
[ "$DOCKER" = 1 ] && { paso "listo: http://127.0.0.1:$PUERTO_API/salud"; exit 0; }

export AULA_DATABASE_URL="postgresql+asyncpg://aula:${AULA_POSTGRES_CLAVE:-}@127.0.0.1:${PUERTO_DB}/aula"

# 4. Tablas y lista blanca de CORS.
paso "creando las tablas que falten"
hacer "$DIR/.venv/bin/python" -m aula.cli tablas --aplicar
if [ "$SECO" = 0 ] && ! "$DIR/.venv/bin/python" -m aula.origenes --verificar >/dev/null; then
  echo "aviso: aula/origenes.generado.json no coincide con web/_pubs/pubs.yml (python -m aula.origenes --aplicar)" >&2
fi

# 5. La API.
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  paso "la API ya corre (pid $(cat "$PIDFILE")): http://127.0.0.1:$PUERTO_API/salud"
  exit 0
fi
UVICORN=("$DIR/.venv/bin/uvicorn" aula.main:app --host 127.0.0.1 --port "$PUERTO_API" --proxy-headers --no-access-log)
if [ "$PRIMER_PLANO" = 1 ]; then
  paso "API en primer plano: http://127.0.0.1:$PUERTO_API/docs"
  [ "$SECO" = 1 ] && { printf '  [simulación] %s\n' "${UVICORN[*]}"; exit 0; }
  exec "${UVICORN[@]}"
fi
paso "API en segundo plano (registro: $REGISTRO)"
if [ "$SECO" = 0 ]; then
  mkdir -p -m 700 "$ESTADO_DIR"
  nohup "${UVICORN[@]}" >>"$REGISTRO" 2>&1 &
  echo $! >"$PIDFILE"
  for _ in $(seq 1 20); do
    curl -fsS "http://127.0.0.1:$PUERTO_API/salud" >/dev/null 2>&1 && break
    sleep 0.5
  done
  curl -fsS "http://127.0.0.1:$PUERTO_API/salud" >/dev/null || { echo "la API no respondió; mire $REGISTRO" >&2; exit 1; }
else
  printf '  [simulación] nohup %s &\n' "${UVICORN[*]}"
fi
paso "listo: http://127.0.0.1:$PUERTO_API/docs · detener con ./detener.sh"
