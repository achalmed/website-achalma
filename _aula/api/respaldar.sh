#!/usr/bin/env bash
# api/respaldar.sh — respaldo cifrado del aula: volcado de la base y del directorio de datos (entregas) a $RESPALDOS_DIR.
#
#   ./respaldar.sh                 simula: dice qué respaldaría, con qué cifra y adónde
#   ./respaldar.sh --aplicar       escribe $RESPALDOS_DIR/aula/<AAAA-MM-DD_HHMMSS>/{base.dump,datos.tar.gz}.{age|gpg}
#   ./respaldar.sh --destino DIR   otra carpeta de destino (nunca dentro de un repo)
#
# Conservación (docs/privacidad.md §4): tras un respaldo bueno se borran las carpetas <AAAA-MM-DD_HHMMSS> del destino
# con más de AULA_RESPALDO_DIAS días (90 por omisión), pero nunca las 3 más recientes; la simulación dice cuáles.
#
# Cifra con clave pública, sin contraseñas en la terminal: `age -r $AULA_RESPALDO_AGE` si age está instalado, o
# `gpg --encrypt -r $AULA_RESPALDO_GPG`; ambos destinatarios se declaran en $XDG_CONFIG_HOME/aula/aula.env. Nada se
# escribe sin cifrar: el volcado y el tar van por tubería al cifrador. Restaurar: README §Respaldo.
set -euo pipefail

DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
d="$DIR"; while [ "$d" != / ] && [ ! -f "$d/core/env.sh" ]; do d="$(dirname "$d")"; done
if [ -f "$d/core/env.sh" ]; then
  # shellcheck disable=SC1091
  source "$d/core/env.sh"
fi
ENTORNO="${XDG_CONFIG_HOME:-$HOME/.config}/aula/aula.env"

APLICAR=0; DESTINO_BASE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --aplicar) APLICAR=1 ;;
    --destino) DESTINO_BASE="${2:?--destino necesita una carpeta}"; shift ;;
    -h|--help) sed -n '2,11p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argumento desconocido: $1 (use --help)" >&2; exit 2 ;;
  esac
  shift
done

[ -f "$ENTORNO" ] || { echo "no hay $ENTORNO: el aula nunca se inició (./iniciar.sh)" >&2; exit 1; }
set -a; # shellcheck disable=SC1090
source "$ENTORNO"; set +a

if [ -z "$DESTINO_BASE" ]; then
  [ -n "${RESPALDOS_DIR:-}" ] || { echo "RESPALDOS_DIR no está definido (core/env.sh)" >&2; exit 1; }
  DESTINO_BASE="$RESPALDOS_DIR/aula"
fi
SELLO="$(date +%Y-%m-%d_%H%M%S)"
DESTINO="$DESTINO_BASE/$SELLO"
DIAS_CONSERVAR="${AULA_RESPALDO_DIAS:-90}"
[[ "$DIAS_CONSERVAR" =~ ^[0-9]+$ ]] || { echo "AULA_RESPALDO_DIAS debe ser un número de días" >&2; exit 1; }

# Respaldos vencidos: carpetas con sello de fecha más viejas que el plazo, salvo las 3 más recientes.
vencidos() {
  [ -d "$DESTINO_BASE" ] || return 0
  local limite; limite="$(date -d "-$DIAS_CONSERVAR days" +%Y-%m-%d)"
  find "$DESTINO_BASE" -mindepth 1 -maxdepth 1 -type d -regextype posix-extended \
       -regex '.*/[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}' -printf '%f\n' | sort -r | tail -n +4 \
    | while read -r d; do [[ "${d%%_*}" < "$limite" ]] && echo "$d"; done
}
DATOS="${AULA_DATOS_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/aula}"

dentro_de_repo() {
  local c; c="$(readlink -m "$1")"
  while [ "$c" != / ]; do [ -e "$c/.git" ] && { echo "$c"; return 0; }; c="$(dirname "$c")"; done
  return 1
}
if repo="$(dentro_de_repo "$DESTINO")"; then
  echo "el destino $DESTINO está dentro del repo $repo: los datos del aula nunca van a un repo" >&2; exit 1
fi

# Cifrador: age (preferido) o gpg, siempre con destinatario de clave pública.
if command -v age >/dev/null 2>&1 && [ -n "${AULA_RESPALDO_AGE:-}" ]; then
  EXT=age; cifrar() { age -r "$AULA_RESPALDO_AGE"; }
  CIFRA="age → ${AULA_RESPALDO_AGE:0:16}…"
elif command -v gpg >/dev/null 2>&1 && [ -n "${AULA_RESPALDO_GPG:-}" ]; then
  EXT=gpg; cifrar() { gpg --batch --yes --trust-model always --encrypt --recipient "$AULA_RESPALDO_GPG"; }
  CIFRA="gpg → $AULA_RESPALDO_GPG"
else
  cat >&2 <<EOF
No hay con qué cifrar. Elija una de dos y declárela en $ENTORNO:
  · age (recomendado): sudo apt install age; age-keygen -o <archivo-de-clave-privada fuera de la laptop>;
    AULA_RESPALDO_AGE=age1… (la clave pública que imprime age-keygen)
  · gpg (ya instalado en esta laptop): gpg --quick-generate-key "Aula respaldo"; AULA_RESPALDO_GPG=<id o correo de la clave>
La clave privada se guarda fuera de la laptop (sin ella, el respaldo no se puede abrir).
EOF
  exit 1
fi

cd "$DIR"
echo "respaldo del aula · cifra: $CIFRA"
echo "  base:  pg_dump de «aula» (contenedor db) → $DESTINO/base.dump.$EXT"
if [ -d "$DATOS" ]; then
  echo "  datos: $DATOS ($(du -sh "$DATOS" | cut -f1)) → $DESTINO/datos.tar.gz.$EXT"
else
  echo "  datos: $DATOS no existe aún (sin entregas): se omite"
fi
echo "  conservación: $DIAS_CONSERVAR días (siempre quedan los 3 más recientes)"
vencidos | sed 's/^/  se borraría (vencido): /'
if [ "$APLICAR" = 0 ]; then
  echo "[simulación] use --aplicar para escribirlo"
  exit 0
fi

[ -d "$DESTINO_BASE" ] || [ -d "$(dirname "$DESTINO_BASE")" ] || { echo "no existe $(dirname "$DESTINO_BASE") (¿disco de respaldos montado?)" >&2; exit 1; }
docker compose --env-file "$ENTORNO" exec -T db pg_isready -h 127.0.0.1 -U aula -d aula >/dev/null \
  || { echo "la base no está arriba: ./iniciar.sh primero" >&2; exit 1; }
mkdir -p -m 700 "$DESTINO"
umask 077
docker compose --env-file "$ENTORNO" exec -T db pg_dump -U aula -d aula --format=custom | cifrar >"$DESTINO/base.dump.$EXT"
if [ -d "$DATOS" ]; then
  tar -C "$(dirname "$DATOS")" -czf - "$(basename "$DATOS")" | cifrar >"$DESTINO/datos.tar.gz.$EXT"
fi
( cd "$DESTINO" && sha256sum ./* >SHA256SUMS )
echo "escrito: $DESTINO"
ls -l "$DESTINO"
vencidos | while read -r d; do rm -rf -- "${DESTINO_BASE:?}/$d" && echo "borrado (vencido): $DESTINO_BASE/$d"; done
