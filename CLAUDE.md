---
tipo: guia_ia
estado: activo
---
# CLAUDE.md — 04 index (repo `website-achalma`)

Guía para el asistente. En español, como todo el ecosistema. `AGENTS.md` es un enlace a este archivo.
Léase antes: `README.md` (qué es y cómo se usa), `docs/README.md` (índice), `_quarto.yml` (el manifiesto
del sitio) y, si se toca un blog, `docs/pubs-submodulos.md` y `_pubs/pubs.yml`.

## Reglas que no se negocian

- **`_quarto.yml` es el único sitio que cablea la navegación**: navbar, pie, tema, comentarios, SEO y el
  menú «More» con los 11 blogs. Un blog nuevo o renombrado se declara ahí y en `_pubs/pubs.yml`, nunca a
  mano en un README: los README y `CITATION.cff` de los pubs y la tabla «Los 11 blogs satélite» del
  `README.md` los escribe `python3 scripts/pubs.py readme --aplicar` (sin `--aplicar` simula).
- **Los blogs se editan y confirman dentro de `_pubs/pub_*`** (cada uno es repo, `_quarto.yml` y sitio
  Netlify propios) y después se mueve el puntero en el hub (`git add _pubs/pub_x && git commit`). Nunca
  `git rm` ni mover `_pubs/` a mano: `scripts_quarto_studio` (gestor de blogs, metadatos, `_indice/`) y
  `scripts_document_studio` (`page-counter`) resuelven los blogs por `website-achalma/_pubs`. Detalle:
  `docs/pubs-submodulos.md`.
- **El tema vive aquí y se propaga**: SCSS, JS, CSS global y de componentes, `_extensions/`,
  `_filters/apa-floats-html.lua` y `scripts/build-page-css.sh` se editan en el hub y van a los blogs con
  `scripts/sync-theme-pubs.sh` (simula; `--aplicar` escribe; `--verificar` sale 1 si hay deriva).
  Excluidos a propósito: `assets/scss/05-pages/`, `assets/css/pages/`, `_filters/_metadata-pdf.lua`,
  `_quarto.yml`, `index.qmd`, `assets/img/`, `assets/fonts/`, `assets/gtm-*.html`. La copia que hay en un
  pub no se edita: el siguiente `--aplicar` la pisaría.
- **Generado no se edita**: `assets/css/pages/*.css` (los compila `scripts/build-page-css.sh`, gancho
  `pre-render`), la sección «Contenidos / Sílabo» de `cursos/<curso>/index.qmd` entre las marcas
  `temario:inicio/fin` (la escribe `10 Class/scripts/temario-generar.sh generar --que web --aplicar`),
  `docs/README.md` (`core/docs.py indice`), los README de los pubs, `_site/`, `_freeze/`, `.quarto/`,
  `_indice/`.
- **Un color o medida nuevo entra por la paleta** (`assets/scss/00-settings/`), recibe rol `$lab-*` en los
  dos archivos de tokens y recién entonces se usa; los módulos compartidos nunca usan `$spc-*` ni hex.
  Guía: `assets/scss/README.md`.
- **Fechas ISO `AAAA-MM-DD`** en todo `date:` de la familia (NORMATIVA §3); `scripts_quarto_studio` las
  normaliza (`main.py fechas-iso`) y las deriva de la carpeta del post (`main.py sync-dates`).
- **Documentación por contrato** (NORMATIVA §15): README con `Uso · Estructura · Límite honesto`, `docs/`
  en kebab con frontmatter `tipo`/`estado`/`titulo`, lo cumplido en `docs/historial/`, el porqué en
  `docs/decisiones.md`. `docs/`, `SECURITY.md` y `CODE_OF_CONDUCT.md` están fuera del render
  (`project.render` en `_quarto.yml`): un `.md` nuevo en `docs/` ya no se publica como página del sitio.
- **Nada del despacho** ni identificadores de un cliente en este repo público (regla 8 del CLAUDE.md raíz).
- **No decidir por el autor** lo que está en `decision`: D1 (`_site/` del hub y de los pubs en git, que
  es lo que Netlify publica, frente a NORMATIVA §5/§15.8), D9 (una sola licencia en los 12 sitios) y D16
  (destino del manual de Git).

## Cómo se verifica un cambio

```bash
quarto preview                                    # vista previa con recarga
quarto render                                     # todo el sitio; freeze: no re-ejecuta código
quarto render cursos/index.qmd                    # un archivo suelto: sí ejecuta su código
# cuántas entradas renderiza el proyecto (docs/, SECURITY.md y CODE_OF_CONDUCT.md no deben aparecer)
quarto inspect . | python3 -c "import json,sys; print(len(json.load(sys.stdin)['files']['input']))"
scripts/sync-theme-pubs.sh --verificar            # tema de los 11 blogs igual al del hub
python3 scripts/pubs.py verificar                 # README/CITATION de los pubs y tabla del hub al día
python3 core/archivos.py validar "04 index"       # normativa A01–A14 y D01–D12
python3 core/docs.py verificar "04 index"         # índice de docs/ al día
git submodule status                              # en qué commit está cada blog respecto al hub
```

No hay lint ni pruebas: se comprueba renderizando y mirando `_site/`. **Publicar el hub y cada blog es
`quarto render` → commit de `_site/` → `git push`**: Netlify sirve el `_site` del repo, sin build. Por eso
`_site/` está **versionado a propósito** en los 12 sitios y nunca se saca de git «por higiene»: hacerlo en
DOC2 dejó el hub vacío el 2026-09-21 (`docs/despliegue-netlify.md`, D1).

## Detalles que cuesta redescubrir

- **`freeze: true`**: `quarto render` global reutiliza `_freeze/` y no ejecuta R/Python; renderizar un
  archivo suelto sí lo ejecuta. Si un cambio de código no aparece: renderiza ese archivo, o
  `quarto render --cache-refresh`, o borra `_freeze/`. `blog/posts/_metadata.yml` y `cursos/_metadata.yml`
  además desactivan la ejecución (`execute.enabled: false`).
- **El glob `*` de Quarto cruza `/`**: en un `listing`, `*/index.qmd` también trae las sesiones anidadas;
  `cursos/index.qmd` excluye con `!*/*/index.qmd` (y más profundo) y cada portada de edición con
  `!*/session_*/index.qmd`.
- **Jerarquía real de `cursos/`**: `cursos/<curso>/<edicion>/session_NN_slug/index.qmd`, la sesión
  directamente bajo la edición; la única excepción heredada es `cursos/pre_economia/2014-i/sesiones/`. Las
  áreas son `categories:` de la ficha y facetan solas; las URL antiguas `/talk/…` y `/teching/…`
  sobreviven por `aliases:`. Cómo se añade contenido: `cursos/README.md` y `cursos/_plantillas/`; por qué
  es así: `docs/historial/course-redesign-plan.md`.
- **Dos escritores externos en `cursos/`**: `10 Class/scripts/temario-generar.sh` (la sección generada de
  cada ficha) y `10 Class/scripts/publish-web.sh` (PDF y materiales de una edición, por hardlink). Por eso
  `cursos/_metadata.yml` es un archivo físico independiente: un hardlink compartido propagaría cambios.
- **`docs/` no se renderiza, pero sigue siendo referencia viva**: `_metadata-guia.md`,
  `_metadata-guia-simplificada.md` y `_quarto-guia.md` anotan cada clave (YAML dentro de bloque de
  código). Las cuatro plantillas apaquarto (`doc`, `jou`, `man`, `stu`) están en `_plantillas/apaquarto/`.
  Los posts se citan como *Actus Mercator*: volumen = año, número 1–4 = trimestre.
- **Estilos por página** se autoran en `assets/scss/05-pages/*.scss` y cada página carga su CSS por
  `header-includes` + `resources`; `assets/css/global.css` y `assets/css/components/bibbase.css` son a
  mano y globales (`_quarto.yml`). El JS de interacción entra por `assets/interactions.html`
  (`include-after-body`); módulos en `assets/js/` (`assets/js/README.md`).
- **`_partials/title-block-link-buttons/title-block.html`** sustituye el bloque de título de Quarto
  (botones de acción bajo el título). `_extensions/` (apaquarto, fontawesome, lightbox) está vendorizado y
  versionado: `quarto update wjschne/apaquarto` para actualizar; nada se descarga en el build.
- **Comentarios**: Utterances sobre los issues de `achalmed/website-achalma`, también desde los blogs.
- **Nombres no derivables**: `pub_chaska` publica en `chaska-x.netlify.app` y su repo se llama `chaska`;
  el único registro carpeta ↔ repo ↔ dominio ↔ tema es `_pubs/pubs.yml`.
- **Residuos de GitHub Pages**: `CNAME` (`kapitan.net`) y `.nojekyll`; Netlify no los usa.
- **`resources/cv.pdf` es copia manual** del CV de `09 trabajo`; `_indice/` y `_vault/` son del vault
  Obsidian y están ignorados. `requirements.txt` no existe, aunque un README antiguo lo citara.
- **Licencia, tal cual está**: `LICENSE` y `CITATION.cff` dicen MPL-2.0 (código); `license.qmd` y los
  `_metadata.yml` dicen CC BY-SA 4.0 (contenido). Unificarla en los 12 sitios es D9, sin decidir.

## Dónde está cada cosa

| pregunta | documento |
|---|---|
| qué es el repo, comandos, estructura, límites | `README.md` |
| los blogs como submódulos: flujo diario, clon, tema, herramientas, reversión | `docs/pubs-submodulos.md` |
| cómo se publica el hub y, hasta donde se sabe, cada blog | `docs/despliegue-netlify.md` |
| publicar un post de principio a fin | `docs/publicar-un-post.md` |
| claves de `_metadata.yml` y de `_quarto.yml`, anotadas | `docs/_metadata-guia.md`, `docs/_quarto-guia.md` |
| por qué se decidió así, con fecha; lo pendiente | `docs/decisiones.md` |
| planes cumplidos | `docs/historial/` |
| la sección docente y su jerarquía | `cursos/README.md` |
| el design system y los módulos JS | `assets/scss/README.md`, `assets/js/README.md` |
| los tres scripts del hub | `scripts/README.md` |
| herramientas externas que escriben aquí | `scripts_quarto_studio/README.md`, `10 Class/scripts/README.md` |
| versiones con fecha | `CHANGELOG.md` |
