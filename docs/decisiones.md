---
tipo: doc
forma: explicacion
titulo: "Decisiones de aula"
estado: activo
---
# Decisiones de aula

La arquitectura y las decisiones del autor (A1–A10, B1–B6, C1) viven en `web/docs/plataforma-educativa.md`;
aquí solo lo que es propio del código de este repo.

### §1.1 Nombre y alcance (2026-10-20)

El autor eligió `aula` (B4): un nombre propio del ecosistema, sin relación con la familia Qillqa (Qillqa, Tiqsi,
Unancha), para que la plataforma educativa no se confunda con la de gestión documental. El repo guarda el código de
la vitrina y, después, el de la API del aula; los 12 sitios lo usan como dependencia versionada.

### §1.2 El cuerpo de lecciones y artículos sale del HTML ya renderizado (2026-10-20)

Se lee `web/_pubs/<pub>/_site/<post>/index.html` y se toma `main#quarto-document-content` (opción a del encargo),
no `index.html.md`. Razón: el HTML es lo que hoy ve el lector, con las matemáticas, el código resaltado (clases de
Pandoc), las tablas, las figuras y las notas tal como Quarto las compuso; el `.md` intermedio obligaría a repetir
filtros, citas y extensiones de Quarto. `src/lib/contenido.mjs` limpia el bloque de título, el apéndice (rescata
las notas al pie y la bibliografía), los `<style>`/`<script>` incrustados y la sección «Publicaciones similares»
que cada pub añade al final; compone las matemáticas con KaTeX en la construcción (sin JS en el navegador); baja
un nivel los encabezados (el `h1` es el título); repara las anclas de los índices escritos a mano al estilo de
GitHub (`#1-conceptos…` → `#conceptos…`, 93 en numerus-scriptum) y convierte en texto los enlaces sin destino.
Los recursos del post (figuras, `index.pdf`, `index.docx`) se copian junto a la página nueva; los enlaces a otro
post publicado se reescriben a su URL nueva.

**Límite.** Depende de que `_site/` esté al día (hoy se versiona, decisión del 2026-09-22); el código que solo
corre en el navegador de Quarto (pestañas de Bootstrap, widgets) no se conserva: las pestañas se muestran una tras
otra. Las lecciones de Python se publican **sin salidas**, porque `web/_pubs/numerus-scriptum/python/_metadata.yml` tiene
`execute.enabled: false`; la vitrina muestra lo que hay y no inventa salidas. En la fase 7, con el perfil
`documentos` y `freeze`, Quarto entregará Markdown con figuras y esta extracción se sustituye por un lector de
ese Markdown (plataforma-educativa §4.6).

### §1.3 Curso ↔ pub y lección ↔ tema (2026-10-20)

Un curso vive en el pub de su **primer** `area` (`docencia/config/areas.yml`); las áreas siguientes lo listan en
su catálogo con «Vive en …» y un enlace a su pub. Una lección publicada es un post del pub con destino `leccion`
en `docencia/contenido/migracion/mapa-lecciones.csv`, sin `draft: true` en su frontmatter y con HTML en `_site/`
(el frontmatter manda sobre la columna `draft` del CSV; hoy coinciden). Si su `tema_id` existe en `curso.yml`,
ocupa ese tema; si no lo tiene, o es un post `revisar` ya publicado, va a «Lecturas complementarias» del curso,
para que nada publicado se pierda. Un tema sin lección aparece «En preparación», sin enlace. El blog son los
posts `blog` publicados. Una edición (`dictado.yml`) pertenece al pub donde vive alguno de sus cursos; una edición
legado sin `cursos:` hereda el pub de otra edición con la misma `web.materia`. Los materiales de cada sesión se
toman de `publicacion/<sesión>/` del dictado o, si no está, de `web/cursos/<materia>/<edición>/<sesión>/`.

### §1.4 Rutas nuevas y cómo se conservan las URL actuales (2026-10-20)

| página | ruta |
|---|---|
| curso | `/cursos/<curso.id>/` |
| lección | `/cursos/<curso.id>/<slug>/` |
| artículo | `/blog/<slug>/` |
| edición | `/ediciones/<dictado.id>/` |

El `slug` es la carpeta del post sin fecha ni número de serie (`2021-06-21-05-iteraciones-con-python` →
`iteraciones-con-python`): no depende del número de tema, que cambiará cuando se reconstruyan los temarios (C1).
Cada build escribe `dist/<pub>/_redirects` (formato de Netlify) con una regla 301 por post publicado,
`/<sección>/<carpeta>/*  /<ruta nueva>/:splat`, que cubre la página, su PDF, su DOCX y sus figuras. Las URL de
`web/cursos/…` del hub se redirigen desde el hub en la fase 7.

### §1.5 Un proyecto, un pub por build (2026-10-20)

`PUB=<carpeta> npm run build` escribe `dist/<pub>/`; `astro.config.mjs` falla si `PUB` no está en
`web/_pubs/pubs.yml`. Las rutas a las fuentes se resuelven como en `core/env.py` (`src/lib/rutas.mjs`: raíz =
carpeta con `core/env.py`, y `DOCS_ROOT`, `CLASS_DIR`, `INDEX_DIR`, `SIMULADORES_DIR` por entorno). Lo que ninguna
fuente dice aún (acento del pub y nombre visible con tildes) está en `config/vitrina.yml`, provisional hasta el
`pub.yml` de cada pub (§4.7 del plan). Los tokens de color salen de la paleta del hub: `npm run build` regenera
`src/styles/paleta.generado.css` desde `web/assets/scss/00-settings/_palette-*.scss` y `tokens.css` les da rol;
los acentos por pub son la única extensión, y viven en `tokens.css`. Sin islas React: el poco JavaScript
(filtros, progreso, lector, autoevaluación) va en `<script>` de cada componente.

### §1.6 Progreso y preferencias en el navegador (2026-10-20)

Sin cuenta, el progreso vive en `localStorage` del visitante: `aula:<pub>:completadas` (`{"curso/slug":
"AAAA-MM-DD"}`), `aula:tema` (`light`/`dark`) y `aula:lectura` (modo lectura). Todo acceso va envuelto en
`try/catch` (`src/scripts/almacen.js`): en una ventana privada o con el almacenamiento bloqueado la página
funciona igual y no recuerda nada. No sale del navegador; la sincronización entre dispositivos es del aula con
cuenta (fase 6).

### §1.7 Autoevaluación: formato `quiz:` (2026-10-20)

Una lección declara sus preguntas en el frontmatter; el componente `Autoevaluacion.astro` las corrige al instante.

```yaml
quiz:
  - tipo: opcion        # opción múltiple
    enunciado: "…"
    opciones: ["…", "…", "…"]
    correcta: 0         # índice desde 0
    explicacion: "…"    # opcional, se muestra al comprobar
  - tipo: vf
    enunciado: "…"
    respuesta: false
  - tipo: numerica
    enunciado: "…"
    respuesta: 3.14
    tolerancia: 0.01    # opcional; acepta coma o punto decimal
    unidad: "%"         # opcional
```

Es práctica: la respuesta viaja en la página. Los exámenes con nota se corrigen en la API (plan §4.5). Ninguna
lección tiene `quiz:` todavía; la página `/demo/autoevaluacion/` (preguntas de muestra sobre el propio
componente) solo existe con `npm run dev` o al construir con `AULA_DEMO=1`, y lo dice en pantalla.
