# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal academic website for Edison Achalma, built with [Quarto](https://quarto.org) (a `.qmd`-based static site generator) and deployed on Netlify at https://achalmaedison.netlify.app. Content is in Spanish. It serves as the hub for a network of ~11 topic-specific satellite blogs (econometrics, philosophy, finance, math, etc.), each hosted on its own Netlify domain and linked from the navbar "More" menu in `_quarto.yml`.

Academic content (blog posts, publications) uses the [`apaquarto`](https://github.com/wjschne/apaquarto) extension to produce APA 7-formatted output in HTML, PDF, and DOCX from a single `.qmd` source.

## Commands

```bash
# Full site render (regenerates _site/, uses cached _freeze/ results — R/Python code NOT re-executed)
quarto render

# Live preview with hot reload while editing
quarto preview

# Render a single post or section only (code in that file IS re-executed regardless of freeze)
quarto render blog/posts/2023-05-16-economia-regional/index.qmd
quarto render cursos/

# Force full re-execution of all cached code chunks
quarto render --cache-refresh
# ...or, for a total reset, delete the freeze cache first:
rm -rf _freeze
quarto render

# Clean build artifacts
rm -rf _site .quarto

# Update the apaquarto extension
quarto update wjschne/apaquarto

# Reinstall extensions from scratch (already vendored in _extensions/, normally not needed)
quarto add wjschne/apaquarto
quarto add quarto-ext/fontawesome
quarto add quarto-ext/lightbox
```

Prerequisites: Quarto CLI ≥ 1.6, R ≥ 4.0, Python 3 (`pip install -r requirements.txt`), TinyTeX for PDF output (`quarto install tinytex`).

There is no lint/test suite — correctness is verified by rendering and visually checking output in `_site/`.

## Architecture

**Content model:** every page/post is a `.qmd` file (Quarto Markdown = YAML frontmatter + Markdown + optional R/Python/Lua code chunks). Site-wide config (navbar, footer, theme, comments, SEO) lives in `_quarto.yml` — this is the single place that wires together navigation across the main site and links out to the satellite blogs.

**Freeze/cache behavior matters:** `_quarto.yml` sets `freeze: true`. A global `quarto render` reuses cached computational results from `_freeze/` and does not re-run R/Python code, but rendering an individual file always re-executes its code. Keep this in mind when a change to code in a `.qmd` doesn't seem to show up after `quarto render` — either render that file directly or clear `_freeze/`.

**Content sections**, each with its own `index.qmd` listing page:
- `blog/posts/<date-slug>/index.qmd` — blog entries, each with full APA metadata (abstract, keywords, categories, tags, author-note, citation block). Published quarterly under the "Actus Mercator" citation scheme (Vol. = year, No. 1–4 = quarter).
- `cursos/` — **unified teaching repository** (OCW-style), replacing the former `talk/` and `teching/` sections. Hierarchy: `cursos/<curso>/<edición>/sesiones/<NN-slug>/index.qmd`. A *course* is a stable identity (ficha with description/syllabus); an *edition* is one delivery (institution + period); sessions hold notes/slides/PDF/materials. Areas (Economía, Matemática, Investigación, Ciencia de Datos, Gestión) are `categories:` metadata, faceted automatically by the `cursos/index.qmd` listing. Migrated sessions preserve old `/talk/…` and `/teching/…` URLs via `aliases:`. Full design in `docs/course-redesign-plan.md`; how-to and templates in `cursos/README.md` + `cursos/_plantillas/`. **Gotcha:** Quarto's `*` in listing `contents` matches across `/` (recursive), so parent listings need `!…/sesiones/*/index.qmd` exclusions to avoid pulling in nested sessions.
- `publication/` — formal publications and external reports.

**`docs/` folder** contains apaquarto *template* references (`_index_doc.qmd`, `_index_jou.qmd`, `_index_man.qmd`, `_index_stu.qmd` for different apaquarto output modes, plus the metadata reference guides `_metadata-guia.md` / `_metadata-guia-simplificada.md` / `_quarto-guia.md`, annotated YAML inside a fenced block) — these are documentation/starting points for new academic documents, not site pages themselves (the leading underscore keeps Quarto from rendering them). Dates: every `date:` in the family is ISO `AAAA-MM-DD` (`meta/NORMATIVA_ARCHIVOS.md` §3, M6 2026-09-15); `scripts_quarto_studio` `main.py fechas-iso` normalizes and `sync-dates` writes ISO.

**Styling:** design system "Quiet Laboratory" in `assets/scss/` (full guide in `assets/scss/README.md`). Two Quarto theme entries (`theme-light.scss`, `theme-dark.scss`, wired in `format.html.theme` after `cosmo`) share one set of modules parameterized by semantic `$lab-*` tokens (`00-settings/` palettes+tokens, `01-tools/`, `02-base/`, `03-layout/`, `04-components/`, `05-interactions/`, `06-themes/`). Page-specific styles are authored in `assets/scss/05-pages/*.scss` and compiled to plain `assets/css/pages/*.css` by `scripts/build-page-css.sh` (a `project.pre-render` hook using Quarto's bundled dart-sass) — never hand-edit that generated CSS. `assets/css/global.css` and `assets/css/components/bibbase.css` are hand-written and loaded site-wide from `_quarto.yml`. Interaction JS lives in `assets/js/` modules loaded on every page by `assets/interactions.html` (`include-after-body`; see `assets/js/README.md`).

**`_partials/title-block-link-buttons`** — custom HTML partial overriding Quarto's default title-block rendering (used for the per-page action buttons under post titles).

**`_extensions/`** — vendored (checked-in) Quarto extensions: `wjschne/apaquarto` (APA 7 formatting engine for PDF/DOCX/HTML/Typst) and `quarto-ext/` (FontAwesome icons, Lightbox image viewer). These are committed, not fetched at build time.

**Generated/do-not-edit directories:** `_site/` (build output), `_freeze/` (cached computation results), `.quarto/` (session cache). Never hand-edit files here — they're regenerated by `quarto render`.

**Comments** are handled via Utterances (GitHub Issues-backed), configured in `_quarto.yml` under `website.comments.utterances`, pointing at this repo (`achalmed/website-achalma`).

## `_pubs/` — the 11 satellite blogs as submodules (2026-09-06)

- `_pubs/pub_*` are **git submodules** (`.gitmodules`, https URLs, `shallow = true`): each `pub_*` keeps its own repo, `_quarto.yml`, Netlify site and history. The leading underscore makes Quarto ignore the folder when rendering the hub (`quarto inspect` lists 0 inputs under `_pubs`).
- Workflow: edit and commit **inside** `_pubs/pub_x` (its own remote is `git@github.com:achalmed/x.git`), then `git add _pubs/pub_x && git commit` in the hub to move the submodule pointer. Fresh clone: `git clone --recurse-submodules` (or `git submodule update --init`). Details: `docs/pubs-submodulos.md`.
- The shared theme is edited **here** and propagated with `scripts/sync-theme-pubs.sh` (simulates by default; `--aplicar` writes; `--verificar` exits 1 on drift). `assets/scss/05-pages/`, `assets/css/pages/`, `_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd` and images are deliberately NOT synced.
- Never `git rm` or move `_pubs/` by hand: the tooling in `scripts_quarto_studio` (blog manager, metadata manager, `04 index` symlinks) and `scripts_document_studio/backends/page-counter` resolve the blogs through `website-achalma/_pubs`.
