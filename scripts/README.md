---
tipo: readme
estado: activo
---
# scripts/ — los scripts del hub: compilar el CSS por página, propagar el tema a los blogs, generar lo que sale de `_pubs/pubs.yml` y la puerta de publicación R6

Ninguno tiene rutas de máquina: cada uno resuelve la raíz del repo desde su propia ubicación. Los que
escriben fuera del hub (`sync-theme-pubs.sh`, `pubs.py`, `puerta-r6.sh --instalar`) **simulan por defecto** y
solo escriben con `--aplicar`; `build-page-css.sh` escribe siempre, porque es el gancho `pre-render` de `_quarto.yml`.

## Uso

```bash
scripts/build-page-css.sh                 # assets/scss/05-pages/*.scss → assets/css/pages/*.css (lo corre cada render)
scripts/sync-theme-pubs.sh                # simula: qué cambiaría en cada _pubs/pub_*
scripts/sync-theme-pubs.sh --aplicar      # escribe el tema del hub en los 11 blogs
scripts/sync-theme-pubs.sh --verificar    # sale 1 si algún blog difiere (lo usa el doctor)
scripts/sync-theme-pubs.sh --pub methodica [--aplicar]   # un solo blog (pub_methodica o methodica; --solo es sinónimo)
scripts/sync-theme-pubs.sh --sello        # el THEME_VERSION que corresponde al tema del hub
scripts/puerta-r6.sh _pubs/pub_methodica  # puerta R6: _site/index.html presente, no vacío y al día (0 pasa · 1 no)
scripts/puerta-r6.sh --instalar --pub methodica [--aplicar]   # la instala como hook pre-push del blog
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
| `sync-theme-pubs.sh` | único mecanismo del tema (normativa 7.11): el tema se comparte por hardlink; con `--aplicar` iguala el contenido, enlaza al final los nombres de `tema-hardlinks.txt` con `scripts-linux/script_hardlinks-creator` (`--verificar` sale 1 si uno quedó sin enlazar), escribe su sello `THEME_VERSION` (commit del hub y sha256 del conjunto) y propaga por `rsync` el conjunto `THEME_PATHS` del hub a cada `_pubs/<blog>`: `_extensions/`, `_filters/apa-floats-html.lua`, `assets/scss/` (menos `05-pages/`), `assets/js/`, `assets/css/global.css`, `assets/css/components/`, `scripts/build-page-css.sh`. Excluidos a propósito: `assets/scss/05-pages/`, `assets/css/pages/`, `_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd`, `assets/img/`, `assets/fonts/`, `assets/gtm-*.html` | el hub | los pubs elegidos (solo con `--aplicar`) |
| `puerta-r6.sh` | comprueba que `_site/index.html` existe, no está vacío, que ninguna fuente (`.qmd`, `_quarto.yml`, `_metadata.yml`, tema) tiene cambios sin confirmar y que el último commit de `_site/index.html` (o de `_site/`, si el render no la cambió) no es anterior al de ninguna fuente: fechas de commit, no de archivo (normativa 7.10, RQ-PRE-03); un `index.html` recién renderizado sin confirmar pasa; `--instalar` copia el script como hook `pre-push` de un blog, con marca GENERADO, y git aborta el push si no pasa; sus casos, en `prueba-puerta-r6.sh` | el sitio (`git status`, `git log` de `_site/` y de las fuentes) | `<blog>/.git/hooks/pre-push` (solo con `--instalar --aplicar`) |
| `render.sh` | render reproducible de un sitio: fija `SOURCE_DATE_EPOCH` y `FORCE_SOURCE_DATE` a la fecha del último commit (fecha interna de PDF y DOCX) y llama a `nice quarto render`; viaja con el tema (hardlink) | el sitio | su `_site/` |
| `fechas-desde-git.py` | `pre-render` de los 12 sitios: fija la fecha de modificación de cada página fuente rastreada, sin cambios y sin hardlinks, a la de su último commit; así `date-modified: last-modified`, los listados y el `sitemap.xml` no dependen del `checkout`; simula sin `--aplicar` | git (fechas de commit) | fechas de los archivos fuente |
| `comparar-produccion.py` | antes de publicar: compara el texto visible de cada página y PDF del `_site/` local con lo que sirve Netlify (que reescribe el marcado) y lista distintas, nuevas y retiradas; solo lee | los `_site/` y los sitios publicados | un informe Markdown con `--salida` |
| `generar-externos.sh` | el hub invoca a los generadores de sus maestros ajenos (ADR 14): `temario.py generar --que web` de `docencia` (sección «Contenidos / Sílabo» de `cursos/*/index.qmd`) y `plataforma.py` de `datafw` (`observatorio/plataforma.html`); busca los repos por `CLASS_DIR`/`DATAFW_DIR` o junto al hub y omite el que falte; simula sin `--aplicar` | `docencia`, `datafw` | `cursos/*/index.qmd` (entre marcas), `observatorio/plataforma.html` |
| `pubs.py` | genera desde `_pubs/pubs.yml` (registro carpeta ↔ repo ↔ dominio ↔ tema ↔ descripción de los 11 blogs) el `README.md` y el `CITATION.cff` completos de cada pub (con marca GENERADO) y el bloque `<!-- pubs:inicio -->` … `<!-- pubs:fin -->` del `README.md` del hub; las secciones temáticas de cada blog las lee del disco; `verificar` compara con `.gitmodules` y el `site-url` de cada `_quarto.yml` sin escribir. Solo requiere PyYAML; no carga `core/` (el hub es un repo público y clonable) | `_pubs/pubs.yml`, `.gitmodules`, el `_quarto.yml` y las carpetas de entradas de cada pub | los 11 pubs y `README.md` del hub (solo con `--aplicar`) |

`build-page-css.sh` viaja con el tema: la copia que hay en cada pub la escribe `sync-theme-pubs.sh` y no
se edita allí.

## Límite honesto

- `sync-theme-pubs.sh` exige `rsync` y trata `_pubs/pub_*` como submódulos ya inicializados: en un clon sin
  `git submodule update --init` no hay nada que sincronizar.
- `--verificar` detecta deriva de archivos, no de significado: un pub puede tener el tema al día y un
  `_quarto.yml` que no lo carga.
- Transición (ola 6): solo los blogs que ya pasaron por `--aplicar` llevan `THEME_VERSION`; en los demás
  `--verificar` lo informa sin contarlo como deriva.
- Con hardlinks, el contenido del tema es el mismo por construcción: lo que `--verificar` vigila es que el enlace
  siga en pie (git y muchos editores lo rompen al reescribir un archivo).
- El hook `pre-push` vive en `.git/hooks/` y no viaja con el repo: un clon nuevo no lo tiene hasta
  `puerta-r6.sh --instalar --aplicar`.
- `pubs.py` escribe solo entre marcas y solo lo que declara `_pubs/pubs.yml`: si un blog cambia de dominio
  y nadie toca el registro, el generador propaga el dato viejo. Tampoco toca `_quarto.yml` ni el menú
  «More» de la navegación: eso sigue siendo a mano.
- No hay comando único de publicación (RQ-WIP-08, ola 6): el hub y cada blog se publican con `quarto render`,
  commit de `_site/` y `git push` desde su propia carpeta; Netlify sirve ese `_site` sin build
  (`../docs/despliegue-netlify.md`). La puerta R6 existe como script y como hook, no como orden de la familia.
