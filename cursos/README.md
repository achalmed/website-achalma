---
tipo: readme
estado: activo
---
# cursos/ — repositorio docente (OpenCourseWare)

Arquitectura tipo *OpenCourseWare* que unifica lo que antes eran `talk/` y `teching/`. Diseño y decisiones
completas en el plan cumplido [`../docs/historial/course-redesign-plan.md`](../docs/historial/course-redesign-plan.md);
el porqué resumido, en `../docs/decisiones.md` §1.

## Fuente de verdad (F5.1/F5.2, 2026-09-06)

- La sección **«Contenidos / Sílabo»** de cada ficha `<curso>/index.qmd` se genera desde el `curso.yml`
  del curso en `10 Class/docencia/cursos/<slug>/` (`10 Class/scripts/temario-generar.sh generar --que web --aplicar`);
  está entre marcadores `temario:inicio/fin` y no se edita a mano.
- Las **ediciones** se publican desde el framework: `publish-session.sh` congela cada sesión y
  `publish-web.sh` enlaza sus PDF y materiales aquí **por hardlink** según `docencia/dictados/<clave>/dictado.yml`
  (`10 Class/scripts/publish-web.sh <clave> --aplicar`; sin `--aplicar` simula). El `index.qmd` y el
  `<sesión>/resources/_links.md` de cada sesión se crean si faltan y luego son editables.
- Las fichas sin curso en el framework ni ediciones llevan `draft: true` hasta que exista contenido.

## Jerarquía

```
cursos/
├── index.qmd                     # Índice de cursos (listing automático, facetas por Área)
├── _metadata.yml                 # Config común de la sección (HTML, freeze, botones, CSS)
├── _plantillas/                  # Plantillas (carpeta con "_" → NO se renderiza)
│   ├── curso.qmd · edicion.qmd · sesion.qmd
│
└── <curso>/                      # CURSO — identidad estable (una vez)
    ├── index.qmd                 # Ficha: descripción, objetivos, sílabo, bibliografía, ediciones
    └── <edicion>/                # EDICIÓN — un dictado (p. ej. 2026-1-cau-unsch)
        ├── _metadata.yml         # config de las sesiones (banner, citation:false)
        ├── index.qmd             # Portada de la edición (docente, institución, listado de sesiones)
        └── session_NN_slug/      # SESIÓN — ver "Estructura ESTÁNDAR" abajo
            └── index.qmd
```

**Regla de oro:** el curso nunca cambia; lo que cambia son las ediciones. Para volver a dictar un curso, se
agrega una nueva carpeta de edición y nada más.

**Excepción heredada:** `pre_economia/2014-i/sesiones/` conserva un nivel `sesiones/` con carpetas `NN-slug`
(14 sesiones migradas de `teching/`); es la única y no se replica. Hoy hay 32 fichas de curso y dos con
ediciones (`metodologia-de-la-investigacion/` con `2025-1-cau-unsch` —legado— y `2026-1-cau-unsch`, y
`pre_economia/2014-i`).

## Estructura ESTÁNDAR de una sesión (todos los cursos)

Cada sesión es una carpeta `session_NN_slug/` (numerada) directamente bajo la edición, con subcarpetas de
nombres **fijos** para poder solo "arrastrar PDFs":

```
<edicion>/                         # p. ej. 2026-1-cau-unsch
├── _metadata.yml                  # title-block-banner + citation:false
├── index.qmd                      # portada: listing de sesiones (session_*/index.qmd, sort: order)
└── session_NN_slug/
    ├── index.qmd                  # página: embebe slides/slides.pdf + incluye resources/_links.md
    ├── slides/       slides.pdf   # la presentación (o .gitkeep)
    ├── practice/     …            # prácticas (o .gitkeep)
    ├── homework/     …            # tareas (o .gitkeep)
    ├── evaluation/   …            # exámenes/rúbricas (o .gitkeep)
    └── resources/
        ├── _links.md              # enlaces y descargas (partial de include; "_" ⇒ no genera página)
        └── readings/  …           # lecturas (o .gitkeep)
```

Nombres estandarizados: `slides` · `practice` · `homework` · `evaluation` · `resources/readings`; el PDF de
la clase es `<sesión>/slides/slides.pdf` y los enlaces van en `<sesión>/resources/_links.md` (lleva guion
bajo para que Quarto no lo publique como página suelta). Plantilla en `_plantillas/sesion.qmd`. Los
`.gitkeep` conservan las carpetas vacías en git hasta que agregues los archivos.

## Cómo añadir contenido (manual)

1. **Curso nuevo:** crea `cursos/<slug>/` y copia `_plantillas/curso.qmd` como `index.qmd`. Rellena `title`,
   `subtitle` (Área), `description` y `categories: [Área]`. Aparecerá solo en `cursos/index.qmd`.
2. **Edición nueva:** dentro del curso crea `<edicion>/` (p. ej. `2026-1-cau-unsch/`) y copia
   `_plantillas/edicion.qmd` como `index.qmd`. En la ficha del curso, sustituye la nota "próximamente" por
   `::: {#ediciones} :::` y descomenta el bloque `listing` de ediciones (ver `_plantillas/curso.qmd`).
3. **Sesión nueva:** dentro de `<edicion>/` crea `session_NN_slug/` (numerada: `session_01_…`,
   `session_02_…`) con las subcarpetas estándar y copia `_plantillas/sesion.qmd` como su `index.qmd`.

Los listados (`listing`) se regeneran solos: no se editan índices a mano. Ojo con el glob de Quarto: `*`
cruza `/`, así que `cursos/index.qmd` excluye `!*/*/index.qmd` (y niveles más profundos) y cada portada de
edición excluye `!*/session_*/index.qmd` para no arrastrar sesiones.

## Áreas disponibles (facetas)

`Preuniversitario` · `Economía` · `Matemática` · `Investigación` · `Ciencia de Datos` · `Gestión`. El área
es el valor de `categories:` en la ficha del curso; para una nueva área basta usarla ahí y la faceta
aparece sola.

## Convención de nombres de edición

Cada dictado es una edición con la forma **`<año>-<ciclo>-<institución>`**, p. ej. `2026-1-cau-unsch`. El
curso es general (sin números romanos): los niveles I/II/III son ediciones sucesivas — Micro I →
`2026-1-cau-unsch`, Micro II → `2026-2-cau-unsch`, y el año siguiente otra vez `2027-1-…`, `2027-2-…`.

## Diseño

Reutiliza el design system "Quiet Laboratory": `listing.css` (masthead) + `courses.css` (retoques de
tarjetas/tablas), ambos generados desde `../assets/scss/05-pages/` y cargados por `header-includes` en las
páginas de listado (índice, fichas, portadas), no en `_metadata.yml`: las sesiones compilan PDF apaquarto y
un `<link>` a nivel de sección rompe el build LaTeX. No se escribe CSS suelto ni se duplican tokens: todo
usa `var(--lab-*)`.

## Preservación de URLs

Cada sesión migrada desde `talk/` o `teching/` conserva su URL antigua mediante `aliases:` en su
frontmatter (Quarto genera páginas-redirección dentro de `_site/`). La configuración de Netlify NO se
gestiona desde este repo (`../docs/despliegue-netlify.md`).

## Límite honesto

- Solo 2 de los 32 cursos tienen ediciones publicadas; el resto son fichas (varias en `draft: true`).
- Esta carpeta no es la fuente docente: el contenido, el sílabo y el registro de alumnos viven en
  `10 Class`; aquí solo se publica lo que el framework enlaza o genera.
