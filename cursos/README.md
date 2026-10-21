---
tipo: readme
estado: activo
---
# cursos/ — portada de cursos del hub y las fichas que aún no tienen sitio

Desde la fase 7 de la plataforma educativa (2026-10-20, `../docs/decisiones.md` §4.7) los cursos viven en el sitio de
su área (los pubs, construidos por `../_aula`). Aquí quedan:

- `index.qmd`: la portada del menú «Cursos», con la tabla área → sitio entre las marcas `sitios:inicio/fin`
  (la escribe `../scripts/redirecciones-cursos.py --aplicar`; no se edita a mano).
- Lo preuniversitario (`pre_algebra`, `pre_aritmetica`, `pre_economia`, `curso-0`) pasó
  el 2026-10-21 a `propaedeutica`, el 12.º pub (decisión B3); las sesiones de `pre_economia/2014-i` son posts de su
  sección `economia/`, con sus URL viejas en `aliases_hub:`.
- `_plantillas/` y `_metadata.yml`, por si una ficha vuelve antes de tener pub.

`sql` (borrador sin curso ni contenido, nunca publicado) se retiró el 2026-10-21.

Las URL viejas de los cursos retirados redirigen (301) a su pub por `../_redirects`, generado desde el currículo.

## Límite honesto

- La portada solo enlaza: los cursos, sus lecciones y sus ediciones viven en los pubs.
