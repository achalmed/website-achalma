---
tipo: doc
titulo: "Referencia de opciones de `_quarto.yml` (sitio Quarto)"
estado: activo
---

# Referencia de opciones de `_quarto.yml` (sitio Quarto)

Qué hace cada bloque del `_quarto.yml` del hub y de los 11 `_pubs/pub_*`, y en qué se diferencian. Es
documentación: los valores viven en el `_quarto.yml` de la raíz de cada sitio (el archivo lleva sus propios
comentarios) y no se copian aquí. Los 12 manifiestos comparten la misma plantilla: un pub difiere de otro
solo en su nombre (cabecera, `comments.utterances.repo`, `site-url`, `repo-url`). La referencia completa de
Quarto: <https://quarto.org/docs/reference/projects/websites.html>.

## `project`

| clave | para qué | hub | pubs |
|---|---|---|---|
| `type: website` · `output-dir: _site` | proyecto de tipo sitio; el render sale a `_site/`, que se versiona y es el despliegue (`decisiones.md` §4.1) | igual | igual |
| `render` | qué entradas renderiza: `*.qmd`, `*.md` y `!docs/` (la documentación del repo no es página del sitio; `decisiones.md` §3.3). Las carpetas que empiezan por `_` o `.` quedan fuera por defecto | sí | no la declaran: renderizan todo lo que no empieza por `_` |
| `pre-render` | `scripts/build-page-css.sh`: compila `assets/scss/05-pages/*.scss` → `assets/css/pages/*.css` antes de cada render | sí | sí (la copia propagada del script) |
| `resources` | archivos que se copian a `_site/` sin renderizar: `observatorio/plataforma.html` (`decisiones.md` §1.6), `resources/cv.pdf`, imágenes de cabecera y las hojas `assets/css/pages/*.css` que cargan las páginas de listado | sí | solo `assets/img/sidebar.jpg` |

## `website`

| clave | para qué | hub | pubs |
|---|---|---|---|
| `title`, `description`, `favicon`, `image` | identidad del sitio y vista previa por defecto (`assets/img/`) | igual | igual |
| `announcement`, `google-analytics`, `cookie-consent` | comentados: no se usan; la analítica entra por Google Tag Manager (`format.html.include-in-header`) | comentados | comentados |
| `open-graph`, `twitter-card` | metadatos de compartir (imagen 1200×630, `locale: es_ES`, `creator`) | igual | igual |
| `comments.utterances` | comentarios sobre los issues de GitHub del **propio** repo (`repo: achalmed/<repo>`, `issue-term: title`) | `achalmed/website-achalma` | el repo de cada blog (`_pubs/pubs.yml`) |
| `site-url`, `repo-url` | dominio Netlify y repo del sitio; `scripts/pubs.py verificar` comprueba que el `site-url` de cada pub coincide con `_pubs/pubs.yml` | el hub | cada blog |
| `navbar` | la barra: `logo`, `tools` (redes) y las entradas `right` (About, Cursos, Publications, Datos, Blog y el menú «More» con los 11 blogs) | completa | solo About (enlace absoluto al hub), «More» e iconos; sin logo ni secciones propias |
| `page-footer` | pie: `left` (copyright), `center` (accesibilidad y redes, con iconos `{{< fa … >}}` de la extensión fontawesome) y `right` (Accessibility, Contact, License, RSS) | enlaces relativos a sus páginas | los mismos enlaces, absolutos al hub |

El menú «More» y el `site-url` de cada blog siguen a mano en cada `_quarto.yml`: `scripts/pubs.py` no los escribe
(`decisiones.md` §2.3).

## `lang` y `format.html`

| clave | para qué | hub | pubs |
|---|---|---|---|
| `lang: es` | idioma del sitio (afecta a Quarto y a apaquarto) | igual | igual |
| `theme.light` / `theme.dark` | `cosmo` + `assets/scss/theme-light.scss` / `theme-dark.scss`: el design system «Quiet Laboratory» (`assets/scss/README.md`); Quarto compila dos bundles y los intercambia con su toggle nativo | igual | igual (copia propagada) |
| `css` | hojas a mano globales: `assets/css/global.css` y `assets/css/components/bibbase.css` | igual | igual |
| `include-in-header`, `include-after-body` | Google Tag Manager (`assets/gtm-head.html`, `assets/gtm-body.html`; no se propagan) y los módulos JS (`assets/interactions.html`, `assets/js/README.md`) | igual | igual, con su propio GTM |
| `highlight-style: a11y`, `code-link`, `pagetitle`, `lightbox` | resaltado accesible, enlaces en el código, título de pestaña y lightbox de imágenes (`_extensions/quarto-ext/lightbox`) | igual | igual |

Los formatos de salida de las entradas (`html`, `apaquarto-pdf`, `apaquarto-docx`), la ejecución
(`execute.freeze`, `execute.enabled: false`) y los metadatos APA no están aquí sino en el `_metadata.yml` de
cada sección: `metadata-guia.md`.

## Comprobar

```bash
quarto inspect . | python3 -c "import json,sys; print(len(json.load(sys.stdin)['files']['input']))"   # entradas que renderiza el hub
python3 scripts/pubs.py verificar        # site-url de cada pub = _pubs/pubs.yml
scripts/sync-theme-pubs.sh --verificar   # el tema que carga format.html.theme es el del hub
```
