# Plan de rediseño de la arquitectura docente — de `talk`/`teching` a `Cursos`

> **Estado:** ✅ **IMPLEMENTADO** (2026-07-09). El análisis y el plan siguen abajo
> como registro; la sección "Estado de implementación" (final del documento)
> resume lo ejecutado y las decisiones tomadas.
>
> **Autor:** Claude Code · **Fecha:** 2026-07-09 · **Alcance:** solo `website-achalma`.

---

## 0. Resumen ejecutivo

El sitio organiza el material docente por **tipo de recurso** (`talk`, `teching`)
en lugar de por **curso**. Esto no escala: una "charla" y una "unidad" son ambas
sesiones de un curso, y la separación obliga a duplicar navegación, listings y
estilos. Se propone unificar ambas en una sección única **`Cursos`** con la
jerarquía de un OpenCourseWare:

```
Área → Curso (identidad estable) → Edición (una por dictado) → Sesión / Material
```

El rediseño reutiliza **íntegramente** el design system "Quiet Laboratory"
(tokens `--lab-*`, `05-pages/`, listings, microinteracciones), no rompe URLs
(vía `aliases` de Quarto + `_redirects` de Netlify), y convierte metadatos hoy
implícitos (institución, semestre, semana, tipo de material) en campos
consultables por los listings.

**Decisión pendiente de tu aprobación** antes de implementar: el nombre de la
ruta raíz (`cursos/` recomendado), y si se conserva `talk/` como redirección
permanente. Ver §7 y §10.

---

## 1. Arquitectura actual

### 1.1 Secciones de contenido

| Sección      | Ruta           | Contenido real hoy                                                                                                                               | Patrón de item                                |
| ------------ | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| **Talks**    | `talk/`        | 9 sesiones de un taller de metodología (APA/Vancouver) en CAU-UNSCH, ene–feb 2025                                                                | `talk/<YYYY-MM-DD-slug>/index.qmd`            |
| **Teaching** | `teching/`     | Curso _Economía Preuniversitaria_ (14 unidades, 2014) + _Matemática Preuniversitaria_ (**carpeta vacía**, solo `_metadata.yml` + `featured.jpg`) | `teching/<curso>/<YYYY-MM-DD-slug>/index.qmd` |
| Blog         | `blog/`        | Entradas APA trimestrales                                                                                                                        | `blog/posts/<slug>/index.qmd`                 |
| Publication  | `publication/` | Publicaciones formales                                                                                                                           | —                                             |

### 1.2 Navegación (`_quarto.yml`)

- `talk/` es **item de primer nivel** del navbar (`Talks`).
- `teching/` está **escondido** bajo el menú "More" como `Cursos`
  (`href: teching/index.qmd`), mezclado con enlaces a los ~11 blogs satélite.
- Incoherencia: lo que el usuario llama "Cursos" ya apunta a `teching`, pero
  `talk` (que también es material de curso) vive aparte y más visible.

### 1.3 Listings

- `talk/index.qmd`: `contents: "**/index.qmd"` (recursivo, recoge cualquier
  sesión que se cuelgue debajo).
- `teching/index.qmd`: `contents: "economia-preuniversitaria/*/index.qmd"`
  — **ruta de un solo curso escrita a mano**. `matematicas-preuniversitaria`
  **no aparece** en el listado: cada curso nuevo exige editar este archivo.
- Ambos comparten `assets/css/pages/listing.css` (cabecera editorial).

### 1.4 Design system (reutilizable tal cual)

- SCSS ITCSS en `assets/scss/` con contrato de tokens `$lab-*` → CSS vars
  `--lab-*` publicadas en `02-base/_root.scss`. Vars disponibles:
  `--lab-bg`, `--lab-bg-surface`, `--lab-bg-elevated`, `--lab-ink`, `--lab-ink-2`,
  `--lab-muted`, `--lab-accent`, `--lab-accent-2`, `--lab-border`,
  `--lab-border-strong`, `--lab-grid-line`, `--lab-glow`, `--lab-green`,
  `--lab-green-bg`, `--lab-code-bg`, `--lab-shadow-sm`, `--lab-shadow-md`.
- Estilos por página en `assets/scss/05-pages/*.scss`, compilados a
  `assets/css/pages/*.css` por `scripts/build-page-css.sh` (hook
  `project.pre-render`). **Regla del build:** solo compila archivos SIN guion
  bajo inicial; los `_*.scss` son stubs inactivos.
- **Ya existe `assets/scss/05-pages/_courses.scss`** (stub inactivo, sin reglas):
  el diseño de esta sección ya estaba previsto. Activarlo = renombrar a
  `courses.scss` + enlazarlo desde la página.
- JS modular en `assets/js/` (navbar, cursor, hero, scroll-effects) inyectado en
  todas las páginas por `assets/interactions.html`. No requiere cambios.

### 1.5 Metadatos y `_metadata.yml`

- `talk/_metadata.yml` (freeze, title-block-banner, partial de botones) está
  **hardlinkeado con `publication/_metadata.yml`** (2 enlaces, mismo inode).
- `teching/economia-preuniversitaria/_metadata.yml`,
  `teching/matematicas-preuniversitaria/_metadata.yml` y
  `blog/posts/_metadata.yml` **comparten inode** (3 enlaces): el bloque APA
  completo (autor, afiliación, disclosures) es idéntico.
- Cada sesión declara su institución/semestre de forma **narrativa** en
  `subtitle`/`categories` (p. ej. `"Tercera Clase en CAU - UNSCH"`), no como
  campos estructurados → no filtrable ni agrupable por los listings.

### 1.6 Hardlinks detectados (crítico para la migración)

| Inode compartido           | Archivos                                                                                     | Nº enlaces | Alcance    |
| -------------------------- | -------------------------------------------------------------------------------------------- | ---------- | ---------- |
| `_contenido-inicio.qmd`    | `blog/`, `teching/` … **y el resto de la familia de blogs `pub_*`**                          | **13**     | Cross-repo |
| `_contenido-final.qmd`     | ídem                                                                                         | **13**     | Cross-repo |
| `_metadata.yml` (APA)      | `blog/posts/`, `teching/economia-preuniversitaria/`, `teching/matematicas-preuniversitaria/` | 3          | Intra-repo |
| `_metadata.yml` (talk/pub) | `talk/`, `publication/`                                                                      | 2          | Intra-repo |

> **Riesgo real:** los `_contenido-*.qmd` (13 enlaces) están compartidos con
> otros proyectos del directorio `~/Documents` (la familia Quarto). Editarlos o
> `git mv`-los **modifica el mismo inode que ven `pub_axiomata`, `pub_optimums`,
> etc.** La migración **no debe tocar esos inodes**; ver §8.

### 1.7 Deuda técnica encontrada (colateral, no bloqueante)

- **42 artefactos LaTeX** commiteados dentro de `talk/*/` (`.aux`, `.log`,
  `.fls`, `.fdb_latexmk`, `.nav`, `.snm`, `.toc`, `.synctex.gz`). No deberían
  versionarse; inflan el repo (p. ej. `sesion 03.pdf` 3.3 MB + su `.log` 95 KB).
- **URLs rotas** en `teching/economia-preuniversitaria/_contenido_economia-preuniversitaria.qmd`:
  los enlaces apuntan a `…/economia-preuniversitaria/…` **sin el prefijo
  `/teching/`** → 404 en producción.
- `matematicas-preuniversitaria` es un curso **fantasma** (sin sesiones) que ya
  ensucia el árbol.
- No existe `_redirects` ni `netlify.toml`: hoy no hay ninguna gestión de
  redirecciones (todo se sirve tal cual desde `_site/`).

---

## 2. Problemas encontrados (síntesis)

1. **Eje de organización equivocado:** por tipo de recurso, no por curso. Con 80
   cursos futuros el árbol `talk/` + `teching/<curso>/` colapsa.
2. **Concepto de "curso" ausente:** no hay una entidad _curso_ estable con
   descripción/objetivos/sílabo separada de sus _ediciones_ (dictados).
3. **Sin dimensión "edición":** no se puede volver a dictar Python 2026-I sin
   mezclar con 2025-II.
4. **Listings frágiles:** `teching` lista un curso a mano; añadir cursos rompe la
   navegación automática.
5. **Metadatos pobres:** institución, semestre, semana, tipo de material viven en
   texto libre → sin filtros, sin agrupación, sin navegación por facetas.
6. **`talk` vs `teching` es una distinción sin diferencia:** ambas son sesiones
   docentes.
7. **Deuda:** artefactos LaTeX versionados, URLs rotas, curso vacío, hardlinks
   cross-repo peligrosos.

---

## 3. Nueva arquitectura propuesta

### 3.1 Modelo conceptual (4 niveles)

```
Área            (agrupación temática: Economía, Matemática, Investigación, Ciencia de Datos, Gestión)
  └── Curso     (identidad ESTABLE y única: descripción, objetivos, sílabo, bibliografía)
        └── Edición   (un dictado concreto: institución + periodo; p. ej. 2026-I · UNSCH)
              └── Sesión / Material  (clase, diapositiva, PDF, ejercicio, examen, solución…)
```

- **El curso nunca cambia.** Lo que cambia son las ediciones. (Modelo OCW/Canvas.)
- **Área** no es una carpeta física obligatoria: se modela como **metadato**
  (`area:`) para poder navegar por facetas sin encajonar la jerarquía de archivos.

### 3.2 Estructura física de directorios

```
cursos/
├── index.qmd                      # Landing: listing de cursos (auto, por metadatos)
├── _metadata.yml                  # Config común de la sección (freeze, partial botones…)
│
├── economia-preuniversitaria/
│   ├── index.qmd                  # Ficha del CURSO (descripción, objetivos, sílabo, ediciones)
│   ├── curso.yml                  # Metadatos estables del curso (area, nivel, etiquetas…)
│   └── 2014-i/                    # EDICIÓN
│       ├── index.qmd              # Portada de la edición (docente, institución, calendario)
│       └── sesiones/
│           ├── 01-conceptos-basicos-de-economia/index.qmd
│           ├── 02-las-necesidades-y-bienes/index.qmd
│           └── … (14 sesiones)
│
└── metodologia-de-la-investigacion/
    ├── index.qmd
    ├── curso.yml
    └── 2025-i-cau-unsch/          # ← las 9 "talks" actuales pasan aquí como una edición
        ├── index.qmd
        └── sesiones/
            ├── 01-monografia-e-informe/index.qmd
            └── … (09 sesiones)
```

**Materiales dentro de cada sesión** (subcarpetas por tipo, opcionales):
`slides/`, `pdf/`, `ejercicios/`, `laboratorios/`, `soluciones/`, `examenes/`,
`recursos/`, `src/` (LaTeX/notebooks). Hoy el PDF vive junto al `index.qmd`; se
mantiene esa convención y se añaden subcarpetas solo cuando el material lo pida.

> **Nota de altura:** no se crean carpetas físicas de "Área" ni de "semana".
> Ambas son metadatos (§3.4). Esto mantiene el árbol poco profundo y evita
> reorganizaciones futuras.

### 3.3 Esquema de URLs

```
/cursos/                                             → índice de cursos
/cursos/<curso>/                                     → ficha del curso
/cursos/<curso>/<edicion>/                           → portada de la edición
/cursos/<curso>/<edicion>/sesiones/<NN-slug>/        → sesión concreta
```

### 3.4 Metadatos ricos (contrato)

**`curso.yml`** (nivel curso, estable) — nuevo archivo por curso:

```yaml
course: "Economía Preuniversitaria"
course-slug: economia-preuniversitaria
area: Economía # faceta de navegación
level: Preuniversitario
summary: "Fundamentos de la ciencia económica para ingreso universitario."
tags: [economia, preuniversitario]
```

**Portada de edición** (`<edicion>/index.qmd`):

```yaml
title: "Economía Preuniversitaria — 2014-I"
edition: 2014-I
institution: Academia / UNSCH
professor: Edison Achalma
period: { start: 2014-01-01, end: 2014-03-29 }
weeks: 14
```

**Sesión** (`sesiones/<NN-slug>/index.qmd`) — se añaden campos estructurados a
lo que ya existe:

```yaml
title: "Conceptos básicos de economía"
course: economia-preuniversitaria # enlaza a la ficha del curso
edition: 2014-I
area: Economía
institution: UNSCH
week: 1
session: 1
type: clase # clase | diapositiva | practica | examen | solucion
tags: [escasez, costo-de-oportunidad]
# recursos (todos opcionales, alimentan botones/descargas):
pdf: index.pdf
slides: slides/sesion-01.pdf
source: src/sesion-01.tex
github: https://github.com/…
video: ~
duration: 90
date: 2014-01-01
```

Estos campos son los que consumen los listings (§3.5) para generar navegación,
filtros y facetas **sin escribir índices a mano**.

### 3.5 Listings automáticos (sin mantenimiento manual)

- **`cursos/index.qmd`** — listing de fichas de curso:
  `contents: "*/index.qmd"` (una tarjeta por curso), con
  `categories` alimentadas por `area`. Añadir un curso = crear su carpeta; el
  índice se actualiza solo.
- **`cursos/<curso>/index.qmd`** — la ficha del curso incrusta un listing de sus
  ediciones: `contents: "*/index.qmd"`.
- **`cursos/<curso>/<edicion>/index.qmd`** — listing de sesiones:
  `contents: "sesiones/*/index.qmd"`, `sort: "session"`, con `fields`
  mostrando `week`, `type`, `date`, botones de descarga.
- **Navegación por facetas** (Área / Institución / Año / Semestre / Etiqueta):
  se implementa con `filter-ui`/`categories` de Quarto sobre los campos
  estructurados, más (opcional, fase 3) páginas-índice generadas por listing con
  `contents` filtrado por metadato. Todo se apoya en el buscador nativo de
  Quarto (`search.json`), ya activo.

---

## 4. Diseño visual (cero CSS nuevo de base)

Se **reutiliza el design system existente**; nada de lenguaje visual nuevo:

1. **Activar el stub ya presente** `assets/scss/05-pages/_courses.scss` →
   renombrar a `courses.scss` y enlazarlo (`header-includes` + `resources`) desde
   las páginas de curso, igual que hoy hace `listing.css`.
2. Todas las reglas nuevas consumen **solo `var(--lab-*)`** (tabla §1.4) → soporte
   automático de modo claro/oscuro sin duplicar.
3. Componentes reutilizados sin cambios: cabecera editorial (`listing.scss`),
   tarjetas `quarto-post`/`card` del tema, botones (`04-components/_buttons.scss`),
   microinteracciones (`.lab-reveal`, glow del cursor), navbar, footer, TOC,
   breakpoints y grid de Bootstrap.
4. Novedades de UI que aporta `courses.scss` (todas sobre tokens existentes):
   tarjeta de curso, cabecera de ficha de curso, tira de "ediciones", tabla de
   sesiones por semana, y chips de faceta. Sin nuevas fuentes, colores ni sombras
   fuera del contrato de tokens.

**Prohibido:** hex directos, `$spc-*` en módulos compartidos, editar a mano
`assets/css/pages/*.css` (son generados por `build-page-css.sh`).

---

## 5. Impacto

| Área                    | Impacto                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `_quarto.yml` navbar    | `Talks` sale de primer nivel; `Cursos` sube a primer nivel apuntando a `cursos/index.qmd`. Se retira `Cursos` del menú "More". |
| `_quarto.yml` resources | `talk/sidebar.jpg` / `teching/sidebar.jpg` → `cursos/…`.                                                                       |
| Listings                | Se reemplazan 2 index frágiles por index auto-escalables.                                                                      |
| SCSS                    | Se activa `_courses.scss`; `listing.scss` se sigue compartiendo. Sin duplicación.                                              |
| Contenido               | 9 talks + 14 unidades se **mueven** (no se reescriben) a la nueva jerarquía; se enriquecen metadatos.                          |
| URLs                    | Cambian todas las de `talk/` y `teching/`; mitigado con `aliases` + `_redirects` (§7).                                         |
| Hardlinks               | Se preservan / sustituyen con cuidado (§8).                                                                                    |
| RSS / SEO / sitemap     | `feed: true` se mantiene en los nuevos listings; sitemap se regenera; canonical vía redirecciones 301.                         |

---

## 6. Plan de migración por fases

Cada fase termina con `quarto render` + revisión visual de `_site/` (no hay test
suite) y `bash -n` en cualquier script tocado. Trabajar en **rama aparte**.

**Fase 0 — Preparación y red de seguridad**

- Crear rama `feat/cursos-arquitectura`.
- Inventario de URLs actuales (extraer de `_site/sitemap.xml`) → base para el
  mapa de redirecciones.
- Documentar y "romper con intención" los hardlinks intra-repo que se moverán
  (§8), **sin tocar los cross-repo**.

**Fase 1 — Andamiaje de la sección `cursos/`**

- Crear `cursos/index.qmd`, `cursos/_metadata.yml`, `_courses.scss` activo.
- Aún sin mover contenido: validar que el listing vacío rinde y estiliza bien.

**Fase 2 — Migrar _Economía Preuniversitaria_** (piloto, curso con contenido)

- `git mv teching/economia-preuniversitaria` → `cursos/economia-preuniversitaria/2014-i/sesiones/…` con renombrado `NN-slug`.
- Crear `index.qmd` de curso + `curso.yml` + `index.qmd` de edición.
- Enriquecer metadatos de sesión (§3.4). Corregir las URLs rotas del
  `_contenido` (bug §1.7).
- Añadir `aliases:` a cada sesión con su URL antigua.

**Fase 3 — Migrar el taller de metodología (las 9 `talk/`)**

- `git mv talk/*` → `cursos/metodologia-de-la-investigacion/2025-i-cau-unsch/sesiones/…`.
- **Excluir del `git mv` los 42 artefactos LaTeX** (borrarlos y añadir patrones a
  `.gitignore`); conservar solo `.tex`, `.pdf` e `images/`.
- Añadir `aliases:` con las URLs `talk/` antiguas.

**Fase 4 — Navegación, redirecciones y facetas**

- Actualizar navbar/resources en `_quarto.yml`.
- Generar `_redirects` (Netlify) para las rutas de sección (`/talk/* /cursos/…`).
- Añadir navegación por facetas (Área/Institución/Año) con `filter-ui`.
- Eliminar el curso fantasma `matematicas-preuniversitaria` (o convertirlo en
  ficha de curso sin ediciones si se planea dictarlo).

**Fase 5 — Verificación y cierre**

- `rm -rf _site _freeze && quarto render`; revisar todas las páginas nuevas,
  las redirecciones (old→new devuelve 301/alias), RSS y sitemap.
- Actualizar `CLAUDE.md` (sección "Content sections") y `assets/scss/README.md`.
- PR siguiendo `docs/guia-flujo-pr.md`.

---

## 7. Estrategia para no romper enlaces (SEO)

Doble red, porque son mecanismos complementarios:

1. **`aliases:` de Quarto** (por página, preferente): en el frontmatter de cada
   sesión migrada se listan sus URLs antiguas. Quarto genera páginas-redirección
   HTML con `<meta refresh>` + canonical hacia la nueva URL. Es autocontenido en
   el repo y sobrevive a cambios de hosting.
   ```yaml
   aliases:
     - /talk/2025-01-14-sesion-03-citas-y-referencias/
     - /teching/economia-preuniversitaria/2014-01-01-conceptos-basicos-de-economia/
   ```
2. **`_redirects` de Netlify** (por patrón, para lo masivo y los 301 "de verdad"):
   ```
   /talk/*      /cursos/metodologia-de-la-investigacion/2025-i-cau-unsch/sesiones/:splat   301
   /teching/*   /cursos/:splat                                                             301
   ```
   (Los patrones se afinan tras el inventario de la Fase 0; se añade a
   `resources` de `_quarto.yml` para que se copie a `_site/`.)

Además: se conserva `feed: true` en los listings con RSS, `image`/`description`
por sesión para Open Graph, y se regenera `sitemap.xml` en el render final.

---

## 8. Manejo de hardlinks

**Principio:** nunca romper contenido compartido con otros proyectos.

- **`_contenido-inicio.qmd` / `_contenido-final.qmd` (13 enlaces, cross-repo):**
  no se referencian desde `talk/` ni desde los items a migrar; **no se tocan**.
  Si alguna página nueva necesitara ese include, se copia el contenido a un
  archivo propio (romper el hardlink deliberadamente con `cp --remove-destination`)
  **antes** de editar, para no alterar el inode que ven los blogs `pub_*`.
- **`_metadata.yml` APA (3 enlaces: blog/posts, economia, matematicas):** al mover
  `economia` a `cursos/…`, el `git mv` conserva el contenido pero el nuevo archivo
  debe ser **físico e independiente**. Procedimiento: copiar con
  `cp --remove-destination` a la nueva ubicación (rompe el hardlink), verificar
  con `stat`/`find -samefile` que blog/posts mantiene su inode intacto, y recién
  entonces borrar el original. Igual criterio para `talk`↔`publication`.
- **Verificación post-migración:**
  `find . -type f -links +1 -printf '%n %i %p\n'` no debe mostrar enlaces
  cruzados inesperados entre la nueva sección `cursos/` y `blog/`/`publication/`
  ni con archivos fuera de `website-achalma`.

---

## 9. Riesgos

| Riesgo                                                                         | Prob. | Impacto                    | Mitigación                                                                        |
| ------------------------------------------------------------------------------ | ----- | -------------------------- | --------------------------------------------------------------------------------- |
| Romper inode `_contenido-*.qmd` compartido con `pub_*`                         | Media | Alto (afecta otros sitios) | No tocarlos; `cp --remove-destination` si hay que editar (§8)                     |
| Pérdida de posicionamiento por cambio de URL                                   | Media | Medio                      | `aliases` + `_redirects` 301 (§7)                                                 |
| `git mv` masivo pierde historia o rompe rutas relativas a imágenes/PDF         | Media | Medio                      | Mover por fases, un curso a la vez; revisar rutas `image:`/`src` tras cada `mv`   |
| Listings recursivos capturan `index.qmd` no deseados (fichas de curso/edición) | Media | Bajo                       | `contents` con globs precisos por nivel (`sesiones/*/index.qmd`), no `**`         |
| `freeze: true` sirve HTML cacheado con rutas viejas                            | Alta  | Bajo                       | `rm -rf _freeze` antes del render final (Fase 5)                                  |
| Artefactos LaTeX arrastrados en el `git mv`                                    | Alta  | Bajo                       | Excluirlos y `.gitignore` (Fase 3)                                                |
| Metadatos incompletos en sesiones antiguas rompen filtros                      | Media | Bajo                       | Valores por defecto en `_metadata.yml` de la edición; enriquecer incrementalmente |

---

## 10. Decisiones que requieren tu confirmación antes de implementar

1. **Nombre de la ruta raíz:** `cursos/` (recomendado, coherente con el idioma
   del sitio) vs. `courses/` vs. `teaching/`.
2. **Destino de las 9 `talk/`:** ¿curso _"Metodología de la investigación"_,
   edición _2025-I CAU-UNSCH_? (es lo que su contenido indica).
3. **`talk/` de primer nivel en el navbar:** ¿se elimina y `Cursos` toma su lugar,
   o se conserva `Talks` como acceso directo filtrado?
4. **Curso fantasma `matematicas-preuniversitaria`:** ¿se elimina o se deja como
   ficha de curso sin ediciones?
5. **Limpieza de artefactos LaTeX** (42 archivos) y **corrección de las URLs
   rotas** del `_contenido` de economía: ¿se incluyen en esta migración?

> Con estas cinco respuestas se puede ejecutar la Fase 0 en firme. Hasta
> entonces, **no se implementa nada**.

---

## 11. Estado de implementación (2026-07-09)

### Decisiones confirmadas por el autor

1. Ruta raíz: **`cursos/`**.
2. `Talks` **eliminado** del navbar de primer nivel; **`Cursos`** ocupa su lugar
   (`href: cursos/index.qmd`). El antiguo `Cursos → teching/` se quitó del menú "More".
3. Las 9 `talk/` son la edición **2025-I · CAU-UNSCH** del curso
   **Metodología de la Investigación**.
4. Limpiezas aplicadas: borrado de 42 artefactos LaTeX, corrección de URLs rotas
   de economía, eliminación del curso fantasma `matematicas-preuniversitaria`.
5. **Netlify: no se tocó nada** (sin `_redirects` ni `netlify.toml`). La
   preservación de URLs se hace **solo con `aliases:` de Quarto** (páginas-
   redirección generadas dentro de `_site/`, íntegramente en el repo).
6. **Scaffolding de cursos futuros**: se crearon 19 fichas de curso listas para
   usar (17 vacías + 2 con contenido migrado), con plantillas en
   `cursos/_plantillas/` y guía en `cursos/README.md`, para migrar manualmente
   más adelante sin rehacer la arquitectura.

### Qué se construyó

- **Sección `cursos/`**: `index.qmd` (índice con facetas por Área), `_metadata.yml`
  (config ligera de sección), `README.md`, `_plantillas/{curso,edicion,sesion}.qmd`.
- **19 fichas de curso** en 5 áreas (Economía 5, Matemática 4, Investigación 3,
  Ciencia de Datos 4, Gestión 3).
- **Migración con `git mv`** (historia preservada):
  - Economía Preuniversitaria → `cursos/economia-preuniversitaria/2014-i/sesiones/01–14/`
    (portada de edición + `sesiones/_metadata.yml` APA independiente + footer de
    "Publicaciones similares" recreado con URLs corregidas).
  - Metodología → `cursos/metodologia-de-la-investigacion/2025-i-cau-unsch/sesiones/01–09/`
    (42 artefactos LaTeX purgados; PDFs/`.tex`/ODT/imágenes conservados).
- **`aliases:`** en las 23 sesiones con su URL antigua (`/teching/…`, `/talk/…`).
- **Diseño**: `assets/scss/05-pages/_courses.scss` activado → `courses.scss`
  (tarjetas, chips de faceta, tabla de sesiones), compilado a
  `assets/css/pages/courses.css`; cargado en toda la sección vía
  `cursos/_metadata.yml`. Cero CSS duplicado; solo `var(--lab-*)`.
- **`_quarto.yml`**: navbar + `resources` actualizados.
- **`about/index.qmd`**: widget "Cursos" y enlaces repuntados a `/cursos`.
- **`.gitignore`**: añadidos `*.nav`, `*.snm`, `*.vrb` (Beamer).
- **Docs**: `CLAUDE.md` (secciones de contenido) y comentarios SCSS actualizados.

### Hallazgo técnico clave

El comodín `*` de `contents:` en los *listings* de Quarto **coincide a través de
`/`** (es recursivo). Por eso los listados padre (`cursos/index.qmd` y las fichas
de curso) llevan exclusiones `!*/*/index.qmd` / `!*/sesiones/*/index.qmd` para no
arrastrar ediciones ni sesiones. Documentado en `cursos/README.md` y `CLAUDE.md`.

### Verificación

`quarto render cursos --to html` → 45 páginas sin errores ni warnings. Índice con
19 cursos y facetas correctas por Área; fichas con 1 edición; portada de edición
con tabla de sesiones; alias `/teching/…` y `/talk/…` generan redirección JS;
PDFs y materiales copiados a `_site/`. (Los formatos `apaquarto-pdf/docx` siguen
declarados solo a nivel de `sesiones/`, no en las páginas de índice.)

### Pendiente para el autor (manual)

- Rellenar objetivos/sílabo/bibliografía de las fichas (marcados _"Por completar"_).
- Añadir ediciones/sesiones a los 17 cursos vacíos copiando las plantillas.
- Revisar el render completo del sitio (`quarto render`) — que sí dispara la
  compilación PDF apaquarto de las sesiones de economía (requiere TinyTeX).
- Confirmar el despliegue en Netlify (sin cambios de configuración por parte de Claude).
