---
tipo: changelog
estado: activo
---
# CHANGELOG — hub `04 index` (repo `website-achalma`)

Cambios del **sitio y su repositorio**, no de cada post (eso es el `git log` y el listado del blog).
Fechas ISO del `git log` real, lo más reciente arriba. Las razones están en `docs/decisiones.md`; lo
cumplido, en `docs/historial/`. `CITATION.cff` declara `version: '3.10'` y no se mueve con estas entradas.

## 2026-09-21 — incidente: el hub caído con un deploy vacío en Netlify

- Causa: DOC2 sacó `_site/` de git «por higiene» y el push siguiente publicó un sitio vacío, porque Netlify
  sirve el `_site` del repo sin build (igual que en los 11 blogs). El `.gitignore` original ya tenía
  `#_site/` comentado a propósito. Detalle en `docs/despliegue-netlify.md` («Incidente 2026-09-21»).
- `_site/` vuelve a git (329 archivos, el render local verificado del 2026-09-20 18:10) y
  `!/_site/**/*_files/` re-incluye las figuras de los posts frente a la regla general `*_files/`.
- Corregida la documentación que desde DOC5 decía que el hub se publicaba con `quarto publish netlify`
  (`README.md`, `CLAUDE.md`, `docs/despliegue-netlify.md`, `docs/publicar-un-post.md`,
  `scripts/README.md`); D1 pasa a cubrir los 12 sitios y, mientras no se decida, `_site/` no se excluye.

## 2026-09-20 — DOC5: documentación de los sitios Quarto

- `README.md` en la raíz (antes el README vivía en `docs/README.md` con rutas de dos reorganizaciones
  atrás); `docs/README.md` pasa a ser el índice generado de `docs/`.
- `CLAUDE.md` en español y por contrato (NORMATIVA §15.5); `CHANGELOG.md`, `docs/decisiones.md`,
  `docs/despliegue-netlify.md`, `docs/publicar-un-post.md`, `docs/historial/`, `scripts/README.md`.
- `docs/`, `SECURITY.md` y `CODE_OF_CONDUCT.md` fuera del render (`project.render` en `_quarto.yml`).
- `_pubs/pubs.yml` como registro de los 11 blogs y `scripts/pubs.py` que genera desde él los README y
  `CITATION.cff` de cada pub y la tabla del README del hub.
- Plantillas apaquarto a `_plantillas/apaquarto/`; `docs/course-redesign-plan.md` a `docs/historial/`;
  `docs/image.png` a `docs/img/`; `publication/_index.md` (residuo de Hugo) eliminado.
- `cursos/README.md`, `assets/scss/README.md` y `assets/js/README.md` con frontmatter, H1 §9.6 y, en los
  propagados, la marca «fuente de verdad: el hub».
- Pendientes declarados: D1 (`_site/` de los pubs), D9 (licencia), D16 (manual de Git).

## 2026-09-20 — DOC2 y DOC3: higiene y punteros

- `_site/`, `_freeze/`, `estructura.txt`, `.claude/`, `.idea/`, `.vscode/` y `.directory` fuera de git;
  `AGENTS.md` como enlace a `CLAUDE.md` (NORMATIVA §15.8).
- Punteros de los 11 blogs tras su higiene; `docs/pubs-submodulos.md` apunta a `meta/diagnosticos/`.
- Páginas de cursos regeneradas.

## 2026-09-15 — M6 y M7: fechas ISO y rutas de cursos

- Todo `date:` en `AAAA-MM-DD`; identidad §6.2 en YAML, fragmentos y diapositivas; las guías de metadatos
  pasan de YAML a Markdown (`docs/_metadata-guia*.md`, `docs/_quarto-guia.md`).
- Rutas de los nueve cursos renombrados en `10 Class` (`course_NN_slug_snake`); fichas «Contenidos /
  Sílabo» regeneradas; la edición `2025-1-cau-unsch` de Metodología marcada como legado; `cursos/README.md`
  al modelo nuevo; títulos entrecomillados en 15 `_links.md`.

## 2026-09-06 — Fusión con el vault, submódulos y fichas desde el temario

- La carpeta pasa a llamarse `04 index` (fusión con el índice del vault; `_indice/` y `_vault/` ignorados).
- Los 11 blogs satélite pasan a submódulos en `_pubs/` (https, shallow); el hub es la fuente del tema y lo
  propaga con `scripts/sync-theme-pubs.sh`; guía `docs/pubs-submodulos.md` (F3a).
- Fichas de curso con la sección «Contenidos / Sílabo» generada desde `curso.yml` (F5.1), edición de
  Metodología 2026-1 enlazada por hardlink desde el framework (F5.2), simuladores, bancos y publicaciones
  relacionadas (F5.3), bibliografía desde Calibre (F5.4).
- Manual de Git ampliado con imagen; `AGENTS.md`.

## 2026-07-13 — About y manual de Git

- Página About actualizada; la guía de flujo de PR pasa a ser el manual `docs/git-github-workflow.md`.

## 2026-07-09 — `cursos/`: repositorio docente (PR #10)

- Nace `cursos/` (OpenCourseWare) y unifica `talk/` y `teching/`; URL antiguas conservadas por `aliases`;
  plan en `docs/historial/course-redesign-plan.md`.

## 2026-07-01 y 2026-07-02 — Design system «Quiet Laboratory»

- Rediseño visual con temas claro y oscuro (PR #9); arquitectura SCSS modular con tokens `$lab-*`, capa
  `05-pages/` compilada por `scripts/build-page-css.sh`, módulos JS independientes, TOC en árbol y
  numeración jerárquica en los posts; `site_libs/` fuera de git; documentación a `docs/`; primer
  `CLAUDE.md` (PR #8).

## 2026-06-16 — Documentación con plantillas APA

- README, plantillas apaquarto (`doc`, `jou`, `man`, `stu`) y guías de metadatos; `CITATION.cff`,
  `LICENSE` (MPL-2.0), `SECURITY.md`, `CODE_OF_CONDUCT.md`.
