---
tipo: readme
estado: activo
---
# scripts/ — los tres scripts del hub: compilar el CSS por página, propagar el tema a los blogs y generar lo que sale de `_pubs/pubs.yml`

Ninguno tiene rutas de máquina: cada uno resuelve la raíz del repo desde su propia ubicación. Los que
escriben fuera del hub (`sync-theme-pubs.sh`, `pubs.py`) **simulan por defecto** y solo escriben con
`--aplicar`; `build-page-css.sh` escribe siempre, porque es el gancho `pre-render` de `_quarto.yml`.

## Uso

```bash
scripts/build-page-css.sh                 # assets/scss/05-pages/*.scss → assets/css/pages/*.css (lo corre cada render)
scripts/sync-theme-pubs.sh                # simula: qué cambiaría en cada _pubs/pub_*
scripts/sync-theme-pubs.sh --aplicar      # escribe el tema del hub en los 11 blogs
scripts/sync-theme-pubs.sh --verificar    # sale 1 si algún blog difiere (lo usa el doctor)
scripts/sync-theme-pubs.sh --solo pub_axiomata [--aplicar]
python3 scripts/pubs.py readme            # simula los README de los pubs y la tabla del README del hub
python3 scripts/pubs.py readme --aplicar  # los escribe
python3 scripts/pubs.py citation --aplicar   # el CITATION.cff de cada pub (título, repo y URL propios)
python3 scripts/pubs.py readme --solo pub_axiomata   # un solo blog (readme y citation admiten --solo)
python3 scripts/pubs.py verificar         # sale 1 si el registro, .gitmodules, los site-url o lo generado no coinciden
python3 scripts/pubs.py verificar --doctor   # la misma comprobación, en el formato del doctor
```

Tras `sync-theme-pubs.sh --aplicar` o `pubs.py … --aplicar`: revisar, hacer commit **en cada pub** y luego
en el hub (mueve los punteros de submódulo). Ver `../docs/pubs-submodulos.md`.

## Estructura

| script | qué hace | lee | escribe |
|---|---|---|---|
| `build-page-css.sh` | compila con el dart-sass que trae Quarto (o `sass` del PATH) cada `assets/scss/05-pages/<página>.scss` sin guion bajo inicial y le antepone la marca `GENERADO … NO editar a mano`; los `_stub.scss` quedan inactivos hasta renombrarlos | `assets/scss/05-pages/` | `assets/css/pages/<página>.css` |
| `sync-theme-pubs.sh` | propaga por `rsync` el conjunto `THEME_PATHS` del hub a cada `_pubs/pub_*`: `_extensions/`, `_filters/apa-floats-html.lua`, `assets/scss/` (menos `05-pages/`), `assets/js/`, `assets/css/global.css`, `assets/css/components/`, `scripts/build-page-css.sh`. Excluidos a propósito: `assets/scss/05-pages/`, `assets/css/pages/`, `_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd`, `assets/img/`, `assets/fonts/`, `assets/gtm-*.html` | el hub | los 11 pubs (solo con `--aplicar`) |
| `pubs.py` | genera desde `_pubs/pubs.yml` (registro carpeta ↔ repo ↔ dominio ↔ tema ↔ descripción de los 11 blogs) el `README.md` y el `CITATION.cff` completos de cada pub (con marca GENERADO) y el bloque `<!-- pubs:inicio -->` … `<!-- pubs:fin -->` del `README.md` del hub; las secciones temáticas de cada blog las lee del disco; `verificar` compara con `.gitmodules` y el `site-url` de cada `_quarto.yml` sin escribir. Solo requiere PyYAML; no carga `core/` (el hub es un repo público y clonable) | `_pubs/pubs.yml`, `.gitmodules`, el `_quarto.yml` y las carpetas de entradas de cada pub | los 11 pubs y `README.md` del hub (solo con `--aplicar`) |

`build-page-css.sh` viaja con el tema: la copia que hay en cada pub la escribe `sync-theme-pubs.sh` y no
se edita allí.

## Límite honesto

- `sync-theme-pubs.sh` exige `rsync` y trata `_pubs/pub_*` como submódulos ya inicializados: en un clon sin
  `git submodule update --init` no hay nada que sincronizar.
- `--verificar` detecta deriva de archivos, no de significado: un pub puede tener el tema al día y un
  `_quarto.yml` que no lo carga.
- `pubs.py` escribe solo entre marcas y solo lo que declara `_pubs/pubs.yml`: si un blog cambia de dominio
  y nadie toca el registro, el generador propaga el dato viejo. Tampoco toca `_quarto.yml` ni el menú
  «More» de la navegación: eso sigue siendo a mano.
- No hay script para publicar: el hub y cada blog se publican con `quarto render`, commit de `_site/` y
  `git push` desde su propia carpeta; Netlify sirve ese `_site` sin build (`../docs/despliegue-netlify.md`).
