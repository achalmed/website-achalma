---
tipo: readme
estado: borrador
---
# aula/ — la plataforma de cursos de los pubs

`aula` es el código de la plataforma educativa: convierte cada pub (los blogs de `web/_pubs`) en un aula con
catálogo, cursos, lecciones, materiales, autoevaluaciones y simuladores, y, más adelante, en un aula con cuenta
(inscripción, tareas, entregas, notas). No guarda contenido: lo lee de sus fuentes (`docencia` para el currículo,
cada pub para el texto de las lecciones y los artículos, `simuladores` para los modelos). La arquitectura y las
decisiones están en `web/docs/plataforma-educativa.md`.

## Uso

```bash
npm install                                # una vez; versiones exactas en package.json (Astro 7.4.1)
PUB=methodica npm run build                # → dist/methodica/        (unos 4 s)
PUB=numerus-scriptum npm run build         # → dist/numerus-scriptum/ (unos 7 s)
node scripts/enlaces.mjs dist/methodica    # enlaces internos rotos (sale 1 si hay alguno)
npm run vista:methodica                    # sirve dist/methodica en http://127.0.0.1:4331 (npx astro preview stop lo detiene)
npm run vista:numerus-scriptum             # ídem en el puerto 4332
PUB=methodica npm run dev                  # desarrollo con recarga; incluye /demo/autoevaluacion/
AULA_DEMO=1 PUB=methodica npm run build    # build con la página de demostración de la autoevaluación
node scripts/tokens.mjs                    # simula la regeneración de la paleta desde el hub (--aplicar escribe)
```

`PUB` es la carpeta del pub en `web/_pubs/pubs.yml`; sin él, el build falla con la lista de válidos. Cada build
deja `dist/<pub>/_redirects` (las URL viejas del pub) y un informe de los datos de origen en
`.cache/informe-<pub>.json`. Construye un pub a la vez: cada build ocupa unos 600 MB de memoria.

## Estructura

| carpeta | qué contiene |
|---|---|
| `astro.config.mjs` | un proyecto, un pub por build (`PUB`), salida en `dist/<pub>/` |
| `config/vitrina.yml` | lo que ninguna fuente dice aún: acento y nombre visible de cada pub (provisional) |
| `src/lib/` | lectura de las fuentes (`rutas.mjs`, `fuentes.mjs`), extracción del HTML de Quarto (`contenido.mjs`) y el modelo del pub (`modelo.mjs`) |
| `src/pages/` | inicio, `cursos/` (catálogo, curso, lección), `blog/`, `ediciones/`, 404 y la demo interna de autoevaluación |
| `src/layouts/` | `Base.astro` (esqueleto) y `Lector.astro` (lector de lecciones y artículos) |
| `src/components/` | retícula del temario, tarjeta de curso, lección en curso, autoevaluación, laboratorio, cabecera y pie |
| `src/styles/` | `paleta.generado.css` (GENERADO desde el hub), `tokens.css` (roles y acentos), `base.css`, `contenido.css` |
| `src/scripts/almacen.js` | progreso y preferencias del visitante en `localStorage` |
| `src/integracion/recursos.mjs` | copia figuras, PDF, DOCX y materiales; escribe `_redirects` y el informe |
| `scripts/` | `tokens.mjs` (paleta del hub → CSS) y `enlaces.mjs` (comprobador de enlaces) |
| `docs/` | decisiones (`docs/decisiones.md`), capturas del prototipo (`docs/img/`) e índice generado |

## Límite honesto

- Es un prototipo: ningún sitio en producción lo usa todavía; los 12 sitios siguen siendo Quarto hasta la fase 7.
  Los enlaces a cursos que viven en otro pub apuntan a rutas que ese pub aún no publica.
- El cuerpo de las lecciones sale del `_site/` de Quarto (decisiones §1.2): si el `_site` de un pub no está al
  día, la vitrina tampoco. Las lecciones de Python se ven sin salidas porque el pub no ejecuta su código.
- Solo methodica y numerus-scriptum están probados; methodica aún no tiene ninguna lección publicada.
- El aula con cuenta (API) no existe aún (fase 6); el progreso vive solo en el navegador del visitante.
- No se ha medido Lighthouse ni hay vista previa en Netlify (objetivos de la fase 4 que quedan pendientes).
