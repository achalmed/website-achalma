---
tipo: decision
titulo: "Decisiones, convenciones y pendientes del hub"
estado: activo
---
# Decisiones, convenciones y pendientes del hub

Archivo único y acumulativo (NORMATIVA §15.6, modelo `02 analysis/docs/decisiones.md`): cada decisión con
su fecha, al final de la sección que le corresponde. `CLAUDE.md` resume; aquí está el porqué. Lo cumplido
y fechado va a `historial/`; las versiones, a `../CHANGELOG.md`.

---

## 1. Contenido y secciones

**1.1 `cursos/` unifica `talk/` y `teching/` como repositorio docente tipo OpenCourseWare** (2026-07-09,
PR #10). Jerarquía curso (identidad estable) → edición (un dictado: `<año>-<ciclo>-<institución>`) →
sesión (`session_NN_slug/` con subcarpetas fijas `slides`, `practice`, `homework`, `evaluation`,
`resources/readings`). El curso nunca cambia; se añaden ediciones. Las áreas son `categories:` de la ficha y
facetan solas. Las URL antiguas se conservan con `aliases:`; el `_redirects` de Netlify previsto no se
aplicó. El plan completo: `historial/course-redesign-plan.md`. La excepción heredada
`cursos/pre_economia/2014-i/sesiones/` no se migró al nombre `session_NN_slug`.

**1.2 La ficha de un curso se genera desde `10 Class`** (2026-09-06, F5.1–F5.4). La sección «Contenidos /
Sílabo» de `cursos/<curso>/index.qmd` sale de `docencia/cursos/<slug>/curso.yml` con
`10 Class/scripts/temario-generar.sh generar --que web --aplicar`, entre marcas `temario:inicio/fin`; las
ediciones se enlazan por hardlink con `publish-web.sh`. Las fichas sin curso en el framework llevan
`draft: true`. Corolario: `cursos/_metadata.yml` es un archivo físico independiente para que un hardlink no
propague cambios.

**1.3 Fechas ISO en toda la familia** (2026-09-15, M6). Todo `date:` es `AAAA-MM-DD`;
`scripts_quarto_studio` normaliza (`fechas-iso`) y deriva de la carpeta (`sync-dates`). Los nueve cursos
renombrados en `10 Class` (M7) cambiaron de ruta aquí en la misma fecha; la edición `2025-1-cau-unsch` de
Metodología quedó marcada como legado por no tener fuentes en el framework.

**1.4 Los posts se citan como *Actus Mercator*** (anterior a 2026-07): volumen = año, número 1–4 =
trimestre. Se declara en el `citation` del frontmatter; el esquema no está en ningún manifiesto.

## 2. Los blogs satélite

**2.1 Los 11 blogs son submódulos del hub en `_pubs/`** (2026-09-06, F3a). Cada uno conserva repo,
`_quarto.yml` y sitio Netlify; el hub los registra por https y `shallow = true`. La carpeta lleva guion
bajo para que Quarto no la renderice. Las herramientas los resuelven por `website-achalma/_pubs`. Reversión:
`meta/reparaciones/F3a_pubs_submodulos_2026-09-06/UNDO.sh`. Detalle: `pubs-submodulos.md`.

**2.2 El hub es la fuente de verdad del tema** (2026-09-06). SCSS, JS, CSS global y de componentes,
extensiones, `_filters/apa-floats-html.lua` y `scripts/build-page-css.sh` se editan aquí y se propagan con
`scripts/sync-theme-pubs.sh`; `assets/scss/05-pages/`, `assets/css/pages/`, `_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd`,
imágenes, fuentes y GTM se excluyen porque difieren por diseño. Desde DOC5 (2026-09-20) las copias
propagadas lo dicen en su cabecera (`assets/scss/README.md`, `assets/js/README.md`, `build-page-css.sh`).

**2.3 Un registro para los nombres de los blogs** (2026-09-20, DOC5). Carpeta, repo, dominio, tema y
descripción no se derivan unos de otros (`pub_chaska` → `chaska` → `chaska-x.netlify.app`) y estaban
repartidos entre `_quarto.yml`, el menú «More», el README viejo y un comentario de `scripts_quarto_studio`.
Ahora viven en `_pubs/pubs.yml` y de ahí salen, con `scripts/pubs.py`, el `README.md` y el `CITATION.cff`
de cada pub y la tabla del README del hub (NORMATIVA §15.9). El `_quarto.yml` de cada pub y el menú de
navegación siguen a mano.

## 3. Documentación del repo

**3.1 El README del repo está en la raíz y `docs/README.md` es el índice de `docs/`** (2026-09-20, DOC5).
Hasta aquí el README real vivía en `docs/README.md` (296 líneas, con `talk/`, `teching/`, `README/`,
`requirements.txt` y otras seis rutas inexistentes; copiado además en los 11 pubs) y la raíz no tenía
ninguno. Se reescribió desde cero con el contrato §15.4; el índice lo genera `core/docs.py indice`.

**3.2 `CLAUDE.md` en español y por contrato** (2026-09-20, DOC5). Se conservan todos sus detalles
(freeze, glob recursivo, jerarquía real de `cursos/` —el anterior documentaba la excepción `sesiones/`
como regla—, design system, partials, extensiones vendorizadas, Utterances, submódulos y herramientas que
resuelven `_pubs`), sin historial ni árbol.

**3.3 `docs/` queda fuera del render del sitio** (2026-09-20, DOC5). Quarto renderizaba `docs/*.md`
como páginas públicas (`_site/docs/course-redesign-plan.html`, `git-github-workflow.html`) y también
`SECURITY.md` y `CODE_OF_CONDUCT.md`; ninguna estaba enlazada desde la navegación. `project.render` en
`_quarto.yml` los excluye; `quarto inspect .` lo comprueba. Con ello, un documento nuevo en `docs/` ya no es
una página del sitio: si algo de `docs/` debe publicarse, se publica como post.

**3.4 Las plantillas apaquarto no son documentación** (2026-09-20, DOC5). `_index_{doc,jou,man,stu}.qmd`
pasan a `_plantillas/apaquarto/` (§15.3: plantillas nunca dentro de `docs/`; el guion bajo de la carpeta
las aparta del render, como `cursos/_plantillas/`). Las tres guías `_metadata-guia*.md` y `_quarto-guia.md`
se quedan en `docs/`: son referencia, no plantilla.

**3.5 El plan de `cursos/` pasa a `historial/`** (2026-09-20, DOC5) con `tipo: plan` y `estado: hecho`,
que ya declaraba. `publication/_index.md` (frontmatter de Hugo/Blogdown, sin cuerpo, `estado: archivado`,
sin referencias) se elimina; git conserva su historia.

**3.6 La licencia se declara tal cual está, sin unificar** (2026-09-20, DOC5; decisión D9 pendiente).
`LICENSE` y `CITATION.cff`: MPL-2.0; `license.qmd` y los `_metadata.yml`: CC BY-SA 4.0; el manual de Git
ya lo formula como código MPL-2.0 / contenido CC BY-SA. Una sola licencia en los 12 sitios la elige el
autor.

## 4. Pendientes con dueño y fecha

| id | qué | desde | estado |
|---|---|---|---|
| **D1** | sacar `_site/` de git en los 11 pubs (el hub ya lo tiene fuera desde DOC2) | 2026-09-20 | pendiente: confirmar en el panel de Netlify el modo de publicación de cada blog (`despliegue-netlify.md`) y elegir `quarto publish netlify` por pub o build en Netlify |
| **D9** | una sola licencia en los 12 sitios (hoy MPL-2.0 en `LICENSE`/`CITATION.cff` y CC BY-SA en `license.qmd`) | 2026-09-20 | pendiente del autor; el README lo cuenta partido |
| **D16** | destino de `git-github-workflow.md` (manual de Git de 1 088 líneas, material educativo del autor, no documentación del repo): `prompts/` (skill o guía), un post de `pub_numerus-scriptum` o `pub_methodica`, o quedarse | 2026-09-20 | pendiente del autor; mientras tanto sigue en `docs/` con sus rutas corregidas |
| `SECURITY.md` · `CODE_OF_CONDUCT.md` | plantillas de GitHub sin rellenar, idénticas en los 12 sitios | 2026-09-20 | pendiente: rellenar (contacto y alcance real) o eliminar en los 12; ya están fuera del render |
| `_redirects` de Netlify | el plan de `cursos/` lo previó para las rutas de sección y no se aplicó; hoy solo hay `aliases:` | 2026-07-09 | sin dueño; se decide con D1 |
| `resources/cv.pdf` | copia manual desde `09 trabajo`; no hay script que la refresque | 2026-09-20 | sin dueño |
