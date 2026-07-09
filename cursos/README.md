# Sección `cursos/` — repositorio docente

Arquitectura tipo *OpenCourseWare* que unifica lo que antes eran `talk/` y
`teching/`. Diseño y decisiones completas en
[`../docs/course-redesign-plan.md`](../docs/course-redesign-plan.md).

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

**Regla de oro:** el curso nunca cambia; lo que cambia son las ediciones. Para
volver a dictar un curso, se agrega una nueva carpeta de edición y nada más.

## Estructura ESTÁNDAR de una sesión (todos los cursos)

Cada sesión es una carpeta `session_NN_slug/` (numerada) directamente bajo la
edición, con subcarpetas de nombres **fijos** para poder solo "arrastrar PDFs":

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

Nombres estandarizados: `slides` · `practice` · `homework` · `evaluation` ·
`resources/readings`, el PDF de la clase como `slides/slides.pdf` y los enlaces en
`resources/_links.md` (lleva guion bajo para que Quarto no lo publique como página suelta). Plantilla en `_plantillas/sesion.qmd`. Los `.gitkeep`
conservan las carpetas vacías en git hasta que agregues los archivos.

## Cómo añadir contenido (manual)

1. **Curso nuevo:** crea `cursos/<slug>/` y copia `_plantillas/curso.qmd` como
   `index.qmd`. Rellena `title`, `subtitle` (Área), `description` y
   `categories: [Área]`. Aparecerá solo en `cursos/index.qmd`.
2. **Edición nueva:** dentro del curso crea `<edicion>/` (p. ej. `2026-1-cau-unsch/`)
   y copia `_plantillas/edicion.qmd` como `index.qmd`. En la ficha del curso,
   sustituye la nota "próximamente" por `::: {#ediciones} :::` y descomenta el
   bloque `listing` de ediciones (ver `_plantillas/curso.qmd`).
3. **Sesión nueva:** dentro de `<edicion>/` crea `session_NN_slug/` (numerada:
   `session_01_…`, `session_02_…`) con las subcarpetas estándar y copia
   `_plantillas/sesion.qmd` como su `index.qmd`.

Los listados (`listing`) se regeneran solos: no se editan índices a mano.

## Áreas disponibles (facetas)

`Preuniversitario` · `Economía` · `Matemática` · `Investigación` ·
`Ciencia de Datos` · `Gestión`. El área es el valor de `categories:` en la ficha
del curso; para una nueva área basta usarla ahí y la faceta aparece sola.

## Convención de nombres de edición

Cada dictado es una edición con la forma **`<año>-<ciclo>-<institución>`**, p. ej.
`2026-1-cau-unsch`. El curso es general (sin números romanos): los niveles I/II/III
son ediciones sucesivas — Micro I → `2026-1-cau-unsch`, Micro II → `2026-2-cau-unsch`,
y el año siguiente otra vez `2027-1-…`, `2027-2-…`.

## Diseño

Reutiliza el design system "Quiet Laboratory": `listing.css` (masthead) +
`courses.css` (retoques de tarjetas/tablas), ambos generados desde
`assets/scss/05-pages/` y cargados vía `cursos/_metadata.yml`. No se escribe CSS
suelto ni se duplican tokens: todo usa `var(--lab-*)`.

## Preservación de URLs

Cada sesión migrada desde `talk/` o `teching/` conserva su URL antigua mediante
`aliases:` en su frontmatter (Quarto genera páginas-redirección dentro de
`_site/`). La configuración de Netlify NO se gestiona desde este repo.
