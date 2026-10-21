#!/usr/bin/env bash
# scripts/publicar.sh — pasa un pub a la vitrina (fase 7 de web/docs/plataforma-educativa.md): construye el sitio con
# aula, exige la prueba de rutas (ninguna URL publicada se pierde) y la de enlaces, copia dist/<pub>/ a
# web/_pubs/<pub>/_vitrina/ y apunta el netlify.toml del pub a esa carpeta. El _site/ de Quarto se queda: es la fuente
# de las lecciones. No hace commit ni push: eso lo decide quien publica (rama, vista previa y merge).
# Uso: scripts/publicar.sh <pub> [--aplicar]      (sin --aplicar construye, prueba y dice qué cambiaría)
#      scripts/publicar.sh <pub> --volver --aplicar   (vuelta atrás: netlify.toml publica otra vez _site/)
# Salida: 0 bien · 1 una prueba falla (no se copia nada) · 2 uso incorrecto.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
source "$(cd ../.. && pwd)/core/env.sh" >/dev/null

pub="${1:-}"; shift || true
aplicar=0; volver=0
for a in "$@"; do case "$a" in --aplicar) aplicar=1 ;; --volver) volver=1 ;; *) echo "opción desconocida: $a" >&2; exit 2 ;; esac; done
dir_pub="$INDEX_DIR/_pubs/$pub"
[[ -n "$pub" && -d "$dir_pub" && -f "$dir_pub/netlify.toml" ]] || { sed -n '2,9p' "${BASH_SOURCE[0]}"; exit 2; }

toml="$dir_pub/netlify.toml"
publicar_en() {   # $1 = carpeta; reescribe solo la línea publish de [build]
  local actual; actual="$(sed -n 's/^[[:space:]]*publish[[:space:]]*=[[:space:]]*"\(.*\)".*/\1/p' "$toml" | head -1)"
  if [[ "$actual" == "$1" ]]; then echo "netlify.toml ya publica $1"; return; fi
  if ((aplicar)); then
    python3 - "$toml" "$1" <<'PY'
import re, sys
p, carpeta = sys.argv[1], sys.argv[2]
t = open(p, encoding="utf-8").read()
t, n = re.subn(r'^(\s*publish\s*=\s*)"[^"]*"', rf'\g<1>"{carpeta}"', t, count=1, flags=re.M)
assert n == 1, "netlify.toml sin línea publish"
open(p, "w", encoding="utf-8").write(t)
PY
    echo "netlify.toml: publish = \"$1\" (antes \"$actual\")"
  else
    echo "simulación: netlify.toml pasaría de publish = \"$actual\" a \"$1\""
  fi
}

if ((volver)); then publicar_en "_site"; exit 0; fi

echo "== $pub: construir"
ASTRO_TELEMETRY_DISABLED=1 PUB="$pub" npx astro build >/dev/null
echo "== $pub: pruebas"
node scripts/rutas.mjs "$pub"
node scripts/enlaces.mjs "dist/$pub"
if ((aplicar)); then
  rsync -a --delete --checksum "dist/$pub/" "$dir_pub/_vitrina/"
  echo "copiado dist/$pub/ → $dir_pub/_vitrina/ ($(du -sh "$dir_pub/_vitrina" | cut -f1))"
  # Nada de la vitrina puede quedar fuera de git: Netlify publica lo empujado (pasó con index_files/, 2026-10-20).
  ignorados="$(git -C "$dir_pub" status --porcelain --ignored _vitrina | grep -c '^!!' || true)"
  if [[ "$ignorados" != 0 ]]; then
    git -C "$dir_pub" status --porcelain --ignored _vitrina | grep '^!!' >&2
    echo "✖ $ignorados rutas de _vitrina/ ignoradas por el .gitignore de $pub: re-inclúyelas (!/_vitrina/…)" >&2; exit 1
  fi
else
  echo "simulación: rsync dist/$pub/ → $dir_pub/_vitrina/ ($(du -sh "dist/$pub" | cut -f1))"
fi
publicar_en "_vitrina"
