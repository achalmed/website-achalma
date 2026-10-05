#!/usr/bin/env bash
# =============================================================================
# prueba-puerta-r6.sh — Casos de la puerta R6 por fechas de commit (puerta-r6.sh, lección 3.6 g).
# -----------------------------------------------------------------------------
# Crea un sitio de juguete en un repo git temporal (fuera del hub) y comprueba:
#   1. render posterior a la fuente            → pasa
#   2. fuente confirmada después del render    → falla
#   3. fuente con cambios sin confirmar        → falla
#   4. _site/index.html sin confirmar          → pasa (recién renderizado)
#   5. render confirmado con index.html igual  → pasa (vale el commit de _site/)
#   6. tema confirmado después del render      → falla
#   7. sin _site/index.html                    → falla
#   8. como hook pre-push (la copia que hace --instalar) → mismo veredicto
# Uso: scripts/prueba-puerta-r6.sh        # 0 si todos los casos dan lo esperado
# Límite: no toca el hub ni los pubs; el repo temporal se borra al salir.
# =============================================================================
set -euo pipefail

PUERTA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/puerta-r6.sh"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/prueba-puerta-r6.XXXXXX")"
limpiar() { [[ "$TMP" == */prueba-puerta-r6.?????? ]] && rm -r -- "$TMP"; }
trap limpiar EXIT
S="$TMP/sitio"
fallos=0
T=1767225600                                   # 2026-01-01T00:00:00Z; cada commit, un minuto después

g() { git -C "$S" "$@"; }
confirmar() {                                  # confirmar <mensaje> <rutas…>: commit con fecha creciente
    local msg="$1"; shift
    T=$((T + 60))
    g add -- "$@"
    GIT_AUTHOR_DATE="@$T +0000" GIT_COMMITTER_DATE="@$T +0000" g commit -q -m "$msg"
}
espera() {                                     # espera <0|1> <caso> [orden…]: corre la puerta y compara
    local quiero="$1" caso="$2" rc=0; shift 2
    "${@:-$PUERTA}" "$S" >/dev/null 2>&1 || rc=$?
    if [[ "$rc" == "$quiero" ]]; then echo "  ✔ $caso"; else echo "  ✖ $caso: salida $rc, se esperaba $quiero"; fallos=$((fallos + 1)); fi
}

mkdir -p "$S/_site" "$S/blog" "$S/assets/scss"
git init -q "$S"
g config user.name prueba; g config user.email prueba@example.invalid; g config core.excludesFile /dev/null
printf 'project:\n  type: website\n' > "$S/_quarto.yml"
printf -- '---\ntitle: Inicio\n---\n' > "$S/index.qmd"
printf -- '---\ntitle: Entrada\n---\nuno\n' > "$S/blog/entrada.qmd"
printf '$c: #000;\n' > "$S/assets/scss/_tema.scss"
confirmar "fuentes" _quarto.yml index.qmd blog/entrada.qmd assets/scss/_tema.scss
printf '<html>v1</html>\n' > "$S/_site/index.html"
confirmar "render" _site/index.html
espera 0 "1. render posterior a la fuente"

printf -- '---\ntitle: Entrada\n---\ndos\n' > "$S/blog/entrada.qmd"
confirmar "fuente nueva" blog/entrada.qmd
espera 1 "2. fuente confirmada después del render"

printf '<html>v2</html>\n' > "$S/_site/index.html"
confirmar "render" _site/index.html
printf -- '---\ntitle: Entrada\n---\ntres\n' > "$S/blog/entrada.qmd"
espera 1 "3. fuente con cambios sin confirmar"
g checkout -q -- blog/entrada.qmd
printf -- '---\ntitle: Borrador\n---\n' > "$S/blog/borrador.qmd"
espera 1 "3b. fuente nueva sin rastrear"
mv -- "$S/blog/borrador.qmd" "$TMP/borrador.qmd"

printf '<html>v3</html>\n' > "$S/_site/index.html"
espera 0 "4. _site/index.html sin confirmar"
g checkout -q -- _site/index.html

printf 'project:\n  type: website\n  title: x\n' > "$S/_quarto.yml"
confirmar "configuración" _quarto.yml
printf '<html>otra</html>\n' > "$S/_site/otra.html"
confirmar "render (portada igual)" _site/otra.html
espera 0 "5. render confirmado con index.html igual"

printf '$c: #111;\n' > "$S/assets/scss/_tema.scss"
confirmar "tema" assets/scss/_tema.scss
espera 1 "6. tema confirmado después del render"
printf '<html>v4</html>\n' > "$S/_site/index.html"
confirmar "render" _site/index.html
espera 0 "6b. y renderizado después"

mv -- "$S/_site/index.html" "$TMP/index.html"
espera 1 "7. sin _site/index.html"
mv -- "$TMP/index.html" "$S/_site/index.html"

# 8. la copia que escribe --instalar, invocada con el nombre pre-push desde el repo
mkdir -p "$TMP/hook"
{ echo '#!/usr/bin/env bash'; echo '# pre-push — copia de prueba'; sed -n '2,$p' "$PUERTA"; } > "$TMP/hook/pre-push"
chmod +x "$TMP/hook/pre-push"
hook() { (cd "$S" && "$TMP/hook/pre-push" origin url </dev/null); }
espera 0 "8. hook pre-push con el render al día" hook
printf -- '---\ntitle: Entrada\n---\ncuatro\n' > "$S/blog/entrada.qmd"
confirmar "fuente nueva" blog/entrada.qmd
espera 1 "8b. hook pre-push con una fuente posterior" hook

if (( fallos )); then echo "prueba-puerta-r6: $fallos caso(s) fallaron"; exit 1; fi
echo "prueba-puerta-r6: todos los casos dan lo esperado"
