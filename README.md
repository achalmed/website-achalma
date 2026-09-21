---
tipo: readme
estado: activo
---
# 04 index/ — hub académico Quarto de Edison Achalma y fuente del tema de sus 11 blogs (repo `website-achalma`)

## Qué es

El sitio personal <https://achalmaedison.netlify.app>: un proyecto Quarto (`type: website`) en español con
blog, repositorio docente (`cursos/`), publicaciones y páginas de contacto, que además es el **hub** de una
familia de 11 blogs temáticos. Los artículos y entradas usan la extensión `apaquarto` para salir en HTML,
PDF y DOCX con formato APA 7 desde un mismo `.qmd`. Los 11 blogs son submódulos git en `_pubs/pub_*`, cada
uno con su repo, su `_quarto.yml` y su sitio Netlify; el hub es la **fuente de verdad del tema** (SCSS, JS,
extensiones y filtros Lua, `meta/workspace.yml` → `verdad:`) y lo propaga con `scripts/sync-theme-pubs.sh`.

Depende de dos vecinos del workspace: `scripts_quarto_studio` (metadatos por Excel, render y publicación de
la familia, enlaces de `_indice/`) y `10 Class` (genera la sección «Contenidos / Sílabo» de cada ficha de
curso y enlaza por hardlink los materiales de cada edición). **No es** un framework de documentos (eso es
`03 writing`), ni el estándar docente (eso es `10 Class`), ni el lugar donde se escribe un post de un blog
satélite: eso se hace dentro del pub, que es su propio repositorio.

## Uso

```bash
quarto preview                                           # vista previa con recarga
quarto render                                            # todo el sitio → _site/ (freeze: no re-ejecuta código)
quarto render blog/posts/2023-05-12-la-economia-peruana-entre-1970-1990/index.qmd   # un solo documento (sí ejecuta)
quarto publish netlify                                   # renderiza y publica el hub en el sitio de _publish.yml
scripts/sync-theme-pubs.sh --verificar                   # ¿algún blog difiere del tema del hub? (sale 1 si sí)
scripts/sync-theme-pubs.sh --aplicar                     # propaga el tema a los 11 blogs (sin --aplicar simula)
python3 scripts/pubs.py verificar                        # README y CITATION.cff de los pubs y la tabla de abajo, al día
python3 scripts/pubs.py readme --aplicar                 # los regenera desde _pubs/pubs.yml (sin --aplicar simula)
git submodule update --remote --merge                    # trae main de cada blog y mueve los punteros del hub
```

Publicar un post, de principio a fin: `docs/publicar-un-post.md`. Trabajar con los blogs como submódulos
(commit dentro del pub, puntero en el hub, clon nuevo): `docs/pubs-submodulos.md`.

## Los 11 blogs satélite

Registro canónico carpeta ↔ repo ↔ dominio ↔ tema: `_pubs/pubs.yml`. La tabla la escribe
`python3 scripts/pubs.py readme --aplicar`; no se edita a mano.

<!-- pubs:inicio -->
| carpeta | tema | repo | sitio | entradas |
|---|---|---|---|--:|
| `_pubs/pub_actus-mercator` | Gestión empresarial | `achalmed/actus-mercator` | https://actus-mercator.netlify.app/ | 5 |
| `_pubs/pub_aequilibria` | Macroeconomía | `achalmed/aequilibria` | https://aequilibria.netlify.app/ | 13 |
| `_pubs/pub_axiomata` | Matemática | `achalmed/axiomata` | https://axiomata.netlify.app/ | 2 |
| `_pubs/pub_chaska` | Tecnología y seguridad | `achalmed/chaska` | https://chaska-x.netlify.app/ | 32 |
| `_pubs/pub_dialectica-y-mercado` | Filosofía y política | `achalmed/dialectica-y-mercado` | https://dialectica-y-mercado.netlify.app/ | 9 |
| `_pubs/pub_epsilon-y-beta` | Econometría | `achalmed/epsilon-y-beta` | https://epsilon-y-beta.netlify.app/ | 49 |
| `_pubs/pub_methodica` | Investigación y metodología | `achalmed/methodica` | https://methodica.netlify.app/ | 7 |
| `_pubs/pub_numerus-scriptum` | Programación y software | `achalmed/numerus-scriptum` | https://numerus-scriptum.netlify.app/ | 80 |
| `_pubs/pub_optimums` | Microeconomía | `achalmed/optimums` | https://optimums.netlify.app/ | 14 |
| `_pubs/pub_pecunia-fluxus` | Finanzas | `achalmed/pecunia-fluxus` | https://pecunia-fluxus.netlify.app/ | 9 |
| `_pubs/pub_res-publica` | Gestión pública | `achalmed/res-publica` | https://res-publica.netlify.app/ | 3 |

<sub>Bloque generado por `scripts/pubs.py readme --aplicar` desde `_pubs/pubs.yml` (2026-09-20); no se edita a mano.</sub>
<!-- pubs:fin -->

## Estructura

| carpeta / archivo | qué es | dueño / generador |
|---|---|---|
| `_quarto.yml` | el manifiesto: proyecto, navegación (incluido el menú «More» con los 11 blogs), tema, formatos, comentarios, `render` | a mano |
| `index.qmd`, `about/`, `contact.qmd`, `appointment/`, `beschikbaarheid/`, `accessibility.qmd`, `license.qmd`, `404.qmd` | páginas del sitio | a mano |
| `blog/posts/<AAAA-MM-DD-slug>/index.qmd` | entradas con metadatos APA completos; `blog/posts/_metadata.yml` fija autor, formatos y `draft: true` por defecto | a mano; el frontmatter lo edita en masa `scripts_quarto_studio` (`script_metadata_manager`); los `_contenido-*.qmd`, `script_generador_publicacion_similar` |
| `cursos/` | repositorio docente tipo OpenCourseWare: `<curso>/index.qmd` (ficha) → `<edicion>/` → `session_NN_slug/`; README propio | fichas a mano; la sección «Contenidos / Sílabo» la genera `10 Class/scripts/temario-generar.sh`; las ediciones las enlaza `10 Class/scripts/publish-web.sh` |
| `publication/` | publicaciones formales (informe ENIS 2022–2023) | a mano |
| `_pubs/` | los 11 blogs como submódulos (`.gitmodules`: https, `shallow = true`) y `pubs.yml`, su registro | contenido en cada pub; README y `CITATION.cff` de cada pub, `scripts/pubs.py` |
| `assets/` | design system «Quiet Laboratory»: `assets/scss/` (fuente), `assets/css/pages/` (**generado** por `scripts/build-page-css.sh`), `assets/css/global.css` y `assets/css/components/bibbase.css` (a mano), `assets/js/`, `assets/img/`, `assets/fonts/`, `assets/gtm-*.html`, `assets/interactions.html` | a mano salvo `assets/css/pages/`; README en `assets/scss/` y `assets/js/` |
| `_extensions/` · `_filters/` · `_partials/` | extensiones vendorizadas (apaquarto, fontawesome, lightbox); filtros Lua (`_metadata-pdf.lua`, `apa-floats-html.lua`); bloque de título propio | vendorizado y versionado; a mano |
| `scripts/` | `build-page-css.sh` (gancho `pre-render`), `sync-theme-pubs.sh`, `pubs.py`; README propio | a mano |
| `docs/` | documentación permanente (fuera del render); índice generado; `historial/` con lo cumplido | a mano; `docs/README.md` lo genera `core/docs.py indice` |
| `_plantillas/apaquarto/` | las cuatro plantillas apaquarto (`doc`, `jou`, `man`, `stu`) para un documento nuevo | a mano; el guion bajo las aparta del render |
| `resources/` | `cv.pdf` (copia manual del CV de `09 trabajo`) e `indice.ods` | a mano |
| `_publish.yml` · `.gitmodules` · `CITATION.cff` · `LICENSE` · `CNAME` | registro del sitio Netlify (lo escribe `quarto publish`); submódulos; cita; MPL-2.0; residuo de GitHub Pages | `quarto publish`; git; a mano |
| `_site/` · `_freeze/` · `.quarto/` · `_indice/` · `_vault/` | artefactos de render y carpetas del vault Obsidian: fuera de git (`.gitignore`) | `quarto render`; `scripts_quarto_studio` (`_indice/`) |

## Documentación

El índice, con tipo y estado de cada documento, está en `docs/README.md` (generado). Puertas de entrada:
`docs/publicar-un-post.md` para escribir y publicar, `docs/pubs-submodulos.md` para los blogs,
`docs/despliegue-netlify.md` para saber cómo llega cada sitio a producción, `docs/_metadata-guia.md` y
`docs/_quarto-guia.md` como referencia de claves, `docs/decisiones.md` para el porqué y lo pendiente. Los README
de carpeta: `cursos/README.md`, `assets/scss/README.md`, `assets/js/README.md`, `scripts/README.md`. Las
versiones, en `CHANGELOG.md`; lo cumplido, en `docs/historial/`.

## Límite honesto

- **Sin lint ni pruebas.** Se comprueba renderizando y mirando `_site/`; `python3 core/archivos.py validar
  "04 index"` revisa la documentación, no el sitio.
- **El hub no renderiza los blogs.** `_pubs/` empieza por `_` y Quarto lo ignora; cada pub se renderiza y
  publica desde su carpeta. Los README de los pubs los genera el hub, pero su contenido no se escribe aquí.
- **Los requisitos no son reproducibles desde el repo.** Hacen falta Quarto (≥ 1.6; hoy 1.9), TinyTeX para
  los PDF apaquarto y, solo para renderizar un documento con código, R o Python. No hay `requirements.txt`
  ni `renv`; con `freeze: true` un render global no ejecuta nada.
- **La licencia está partida y así se declara:** `LICENSE` y `CITATION.cff` dicen MPL-2.0 (código);
  `license.qmd` y los `_metadata.yml` dicen CC BY-SA 4.0 (contenido). Unificarla en los 12 sitios es la
  decisión D9, pendiente del autor.
- **Netlify no se configura desde el repo.** No hay `netlify.toml` ni `_redirects`; las URL antiguas de
  `/talk/` y `/teching/` sobreviven por `aliases:` de Quarto. Cómo publica cada uno de los 12 sitios y qué
  falta por confirmar en el panel: `docs/despliegue-netlify.md` (D1).
- **Los nombres de un blog no se derivan unos de otros** (`pub_chaska` → repo `chaska` → dominio
  `chaska-x.netlify.app`): el único registro es `_pubs/pubs.yml`.
- Los comentarios (Utterances) viven en los issues de `achalmed/website-achalma`, también los de los blogs.
