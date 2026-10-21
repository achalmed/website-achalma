---
tipo: readme
estado: borrador
---
# _aula/ — la plataforma de cursos de los pubs

`_aula` (en el hub `web`) es el código de la plataforma educativa: convierte cada pub (los blogs de `web/_pubs`) en un aula con
catálogo, cursos, lecciones, materiales, autoevaluaciones y simuladores, y en un aula con cuenta
(inscripción, tareas, entregas, notas, exámenes calificados) servida por la API de `api/`. No guarda contenido: lo lee de sus fuentes (`docencia` para el currículo,
cada pub para el texto de las lecciones y los artículos, `simuladores` para los modelos). La arquitectura y las
decisiones están en `web/docs/plataforma-educativa.md`.

## Uso

```bash
cd web/_aula                               # desde ~/Documents
npm install                                # una vez; versiones exactas en package.json (Astro 7.4.1)
PUB=methodica npm run build                # → dist/methodica/        (unos 4 s)
PUB=numerus-scriptum npm run build         # → dist/numerus-scriptum/ (unos 7 s)
node scripts/enlaces.mjs dist/methodica    # enlaces internos rotos (sale 1 si hay alguno)
node scripts/rutas.mjs methodica           # prueba de rutas: cada URL del sitio Quarto vive o redirige (sale 1 si alguna se pierde)
scripts/publicar.sh methodica [--aplicar]  # cambio del pub a la vitrina: construye, prueba, copia a _vitrina/ y apunta netlify.toml (--volver deshace)
npm run vista:methodica                    # sirve dist/methodica en http://127.0.0.1:4331 (npx astro preview stop lo detiene)
npm run vista:numerus-scriptum             # ídem en el puerto 4332
PUB=methodica npm run dev                  # desarrollo con recarga; incluye /demo/autoevaluacion/
AULA_DEMO=1 PUB=methodica npm run build    # build con la página de demostración de la autoevaluación
node scripts/tokens.mjs                    # simula la regeneración de la paleta desde el hub (--aplicar escribe)
python3 scripts/marca.py                   # simula los trazos del colofón y de la imagen Open Graph (--aplicar escribe)
AULA_API_URL=http://127.0.0.1:8040 PUB=methodica npm run build   # añade «Mi aula» (/aula/) contra la API local
```

La API del aula (cuentas, clases, tareas, exámenes, progreso) se levanta con `api/iniciar.sh` y se detiene con
`api/detener.sh`; su uso, pruebas y respaldo están en `api/README.md`. Sin `AULA_API_URL` el build no genera «Mi aula»
ni su enlace y el sitio sale como siempre.

`PUB` es la carpeta del pub en `web/_pubs/pubs.yml`; sin él, el build falla con la lista de válidos. Cada build
deja `dist/<pub>/_redirects` (las URL viejas del pub) y un informe de los datos de origen en
`.cache/informe-<pub>.json`. Construye un pub a la vez: cada build ocupa unos 600 MB de memoria.

## Estructura

| carpeta | qué contiene |
|---|---|
| `astro.config.mjs` | un proyecto, un pub por build (`PUB`), salida en `dist/<pub>/` |
| `config/vitrina.yml` | lo que ninguna fuente dice aún: acento, monograma y nombre visible de cada pub (provisional) |
| `src/lib/` | lectura de las fuentes (`rutas.mjs`, `fuentes.mjs`), extracción del HTML de Quarto (`contenido.mjs`) y el modelo del pub (`modelo.mjs`) |
| `src/pages/` | inicio, `cursos/` (catálogo, curso, lección), `blog/`, `ediciones/`, 404 y la demo interna de autoevaluación |
| `src/layouts/` | `base.astro` (esqueleto) y `lector.astro` (lector de lecciones y artículos) |
| `src/components/` | colofón (`marca.astro`), íconos Lucide, búsqueda ⌘K, banda de cifras, tarjetas de curso, entrada y edición, retícula del temario, lección en curso, autoevaluación, laboratorio, cabecera y pie |
| `src/lib/marca.mjs`, `imagenes.mjs`, `iconos.mjs` | el colofón en la página y en archivos (favicon, PNG, Open Graph), la miniatura de cada tarjeta y los íconos (decisiones §1.16–§1.18) |
| `src/styles/` | `paleta.generado.css` (GENERADO desde el hub), `tokens.css` (roles y acentos), `base.css`, `contenido.css` |
| `src/scripts/almacen.js` | progreso y preferencias del visitante en `localStorage` |
| `src/scripts/aula-api.js` | cliente de la API del aula (sesión por `Authorization: Bearer`, renovación, progreso) |
| `src/rutas/aula-cuenta.astro` | «Mi aula»: entrar, crear cuenta con consentimiento, clases, progreso, datos propios (solo con `AULA_API_URL`) |
| `api/` | la API del aula con cuenta (FastAPI + PostgreSQL 16; `api/README.md`) |
| `src/integracion/recursos.mjs` | copia figuras, PDF, DOCX y materiales; escribe `_redirects` y el informe |
| `scripts/` | `tokens.mjs` (paleta del hub → CSS), `marca.py` (monogramas y textos → trazos), `enlaces.mjs` (enlaces), `rutas.mjs` (URL viejas) y `publicar.sh` |
| `docs/` | decisiones (`docs/decisiones.md`), capturas de la vitrina (`docs/img/`) e índice generado |

## Límite honesto

- Es un prototipo: ningún sitio en producción lo usa todavía; los 12 sitios siguen siendo Quarto hasta la fase 7.
  Los enlaces a cursos que viven en otro pub apuntan a rutas que ese pub aún no publica.
- El cuerpo de las lecciones sale del `_site/` de Quarto (decisiones §1.2): si el `_site` de un pub no está al
  día, la vitrina tampoco. Las lecciones de Python se ven sin salidas porque el pub no ejecuta su código.
- Solo methodica y numerus-scriptum están probados; methodica aún no tiene ninguna lección publicada.
- El aula con cuenta es un MVP (fase 6) que corre solo en la laptop y no está publicado: sin `AULA_API_URL` el progreso
  vive solo en el navegador. «Mi aula» aún no deja entregar tareas ni rendir exámenes (eso se hace por la API) y no hay
  panel del docente (`api/README.md`, Límite honesto).
- Lighthouse móvil en methodica servida en local (2026-10-20): rendimiento 96–98 y 100 en accesibilidad, buenas
  prácticas y SEO (inicio, un curso y un artículo). No hay vista previa en Netlify.
