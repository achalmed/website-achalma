---
tipo: estado
estado: activo
actualizado: 2026-10-20
---
# estado.md — web/_aula

## Hecho

| fecha | qué | dónde se ve |
|---|---|---|
| 2026-10-20 | Alta del repo con el nombre que eligió el autor (B4) y entrada en `meta/workspace.yml` | `528a696` · `meta/workspace.yml` |
| 2026-10-20 | Pasa a `web/_aula` con su historia (`git subtree`); el repo suelto, su entrada en `meta/workspace.yml` y su remoto se retiran (decisión del autor); rutas dinámicas por `injectRoute` y componentes en kebab-case, con las URL idénticas | `web` · respaldo y `UNDO.sh` en `$RESPALDOS_DIR/renombres/2026-10-20-aula-a-web-_aula/` |
| 2026-10-20 | Prototipo de la vitrina con Astro 7.4.1: inicio, catálogo con filtros y búsqueda, portada de curso con retícula, temario y progreso, lector de lecciones, blog, ediciones, autoevaluación (demo interna); `_redirects` por pub; builds de methodica (4 s) y numerus-scriptum (7 s) sin advertencias, 0 enlaces internos rotos | `README.md` §Uso · `docs/decisiones.md` §1.2–§1.7 · `docs/img/` |

## En curso

**Fase 4: prototipo de la vitrina** (abierta 2026-10-20, rama `main` de `web`; sin producción).
Punto exacto: prototipo funcional y verificado en el navegador (escritorio y 375 px, claro y oscuro, consola
limpia); siguiente paso: medir Lighthouse a 375 px y publicar una vista previa en Netlify de methodica, y después
el generador `curso.yml` → pub (§4.3 del plan).

## Por hacer

- 2026-10-20 · dueño: director · Lighthouse ≥ 90 a 375 px en los dos pilotos (prueba de salida de la fase 4).
- 2026-10-20 · dueño: director · Vista previa en Netlify (methodica), sin tocar el sitio en producción.
- 2026-10-20 · dueño: autor · Corregir en `docencia` los datos de origen que la vitrina muestra tal cual: títulos de tema sin tildes (methodica: 47; gretl y spss: 8), unidades «Unidad NN» y temas en inglés en python/stata, cursos sin unidades (geogebra, matlab, power-bi). Lista en `.cache/informe-<pub>.json` tras cada build.
- 2026-10-20 · dueño: autor · numerus-scriptum: las lecciones de Python se publican sin salidas (`web/_pubs/numerus-scriptum/python/_metadata.yml`, `execute.enabled: false`); decidir si se ejecutan con `freeze`.

## Futuro

- El generador `curso.yml` → estructura del curso en cada pub (fase 4–5) y el paquete compartido por los 12 sitios (§4.7).
- La API del aula (fase 6) aquí mismo, en `_aula/api/`.
