---
tipo: estado
estado: activo
actualizado: 2026-10-20
---
# estado.md — web/_aula

## Hecho

| fecha | qué | dónde se ve |
|---|---|---|
| 2026-10-20 | Identidad sobria y moderna (pedido del autor): grafito con un acento por pub, Inter y JetBrains Mono, vidrio y sombras de capa, íconos Lucide, marca por sitio (squircle con monograma, favicon, PNG y Open Graph), paleta de comandos ⌘K, barra en los bloques de código, banda de cifras, tarjetas con miniatura o índice, pie «La familia»; Lighthouse móvil 97–98/100/100/100 en methodica | `docs/decisiones.md` §1.16–§1.17 · `docs/img/` |
| 2026-10-20 | Alta del repo con el nombre que eligió el autor (B4) y entrada en `meta/workspace.yml` | `528a696` · `meta/workspace.yml` |
| 2026-10-20 | Pasa a `web/_aula` con su historia (`git subtree`); el repo suelto, su entrada en `meta/workspace.yml` y su remoto se retiran (decisión del autor); rutas dinámicas por `injectRoute` y componentes en kebab-case, con las URL idénticas | `web` · respaldo y `UNDO.sh` en `$RESPALDOS_DIR/renombres/2026-10-20-aula-a-web-_aula/` |
| 2026-10-20 | API del aula (fase 6, MVP) en `api/`: cuentas con consentimiento, clases con código, anuncios, tareas con rúbrica, entregas con archivo y calificación, exámenes corregidos en el servidor, progreso sincronizado, exportar y borrar los datos propios; 58 pruebas en verde en SQLite y en PostgreSQL 16; respaldo cifrado probado con una clave gpg desechable; «Mi aula» en la vitrina solo con `AULA_API_URL` | `api/README.md` · `docs/decisiones.md` §1.9–§1.14 · `api/docs/privacidad.md` |
| 2026-10-20 | Prototipo de la vitrina con Astro 7.4.1: inicio, catálogo con filtros y búsqueda, portada de curso con retícula, temario y progreso, lector de lecciones, blog, ediciones, autoevaluación (demo interna); `_redirects` por pub; builds de methodica (4 s) y numerus-scriptum (7 s) sin advertencias, 0 enlaces internos rotos | `README.md` §Uso · `docs/decisiones.md` §1.2–§1.7 · `docs/img/` |

## En curso

**Fase 4: prototipo de la vitrina** (abierta 2026-10-20, rama `main` de `web`; sin producción).
Punto exacto: prototipo funcional y verificado en el navegador (escritorio y 375 px, claro y oscuro, consola
limpia); Lighthouse móvil medido (97–98 y 100 en lo demás, 2026-10-20); siguiente paso: publicar una vista previa en Netlify de methodica, y después
el generador `curso.yml` → pub (§4.3 del plan). En paralelo, **fase 6** (API del aula): MVP hecho y probado en
local (2026-10-20), sin publicar; siguiente paso: el dictado de prueba con cuentas ficticias.

## Por hacer

- 2026-10-20 · dueño: autor · Antes de abrir el aula a estudiantes reales: contacto para los derechos, inscripción del banco de datos si corresponde, consentimiento de tutores para menores, rotación de respaldos (`api/docs/privacidad.md` §7); generar la clave de respaldo (age o gpg) y guardarla fuera de la laptop.
- 2026-10-20 · dueño: autor · Decidir cuándo publicar la API con Tailscale Funnel (`tailscale funnel --bg 8040`) y construir los sitios con `AULA_API_URL`.
- 2026-10-20 · dueño: director · Un dictado real de prueba con cuentas ficticias (prueba de salida de la fase 6 del plan).
- 2026-10-20 · dueño: director · Lo que falta del aula: panel del docente en la vitrina (crear tareas y exámenes, calificar con rúbrica, libro de notas), rendir exámenes y entregar tareas desde la vitrina, foros, certificados verificables, liberación condicional, avisos por correo o push, Alembic.

- 2026-10-20 · dueño: director · Vista previa en Netlify (methodica), sin tocar el sitio en producción.
- 2026-10-20 · dueño: autor · Corregir en `docencia` los datos de origen que la vitrina muestra tal cual: títulos de tema sin tildes (methodica: 47; gretl y spss: 8), unidades «Unidad NN» y temas en inglés en python/stata, cursos sin unidades (geogebra, matlab, power-bi). Lista en `.cache/informe-<pub>.json` tras cada build.
- 2026-10-20 · dueño: autor · numerus-scriptum: las lecciones de Python se publican sin salidas (`web/_pubs/numerus-scriptum/python/_metadata.yml`, `execute.enabled: false`); decidir si se ejecutan con `freeze`.

## Futuro

- El generador `curso.yml` → estructura del curso en cada pub (fase 4–5) y el paquete compartido por los 12 sitios (§4.7).
- La API del aula pasa de la laptop a un VPS si algún día hace falta disponibilidad continua (B1): la misma receta Docker.
