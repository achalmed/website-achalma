---
tipo: readme
estado: activo
---
# cursos/ — portada de cursos del hub y lo preuniversitario que aún no tiene sitio

Desde la fase 7 de la plataforma educativa (2026-10-20, `../docs/decisiones.md` §4.7) los cursos viven en el sitio de
su área (los pubs, construidos por `../_aula`). Aquí quedan:

- `index.qmd`: la portada del menú «Cursos», con la tabla área → sitio entre las marcas `sitios:inicio/fin`
  (la escribe `../scripts/redirecciones-cursos.py --aplicar`; no se edita a mano).
- Lo preuniversitario (`pre_algebra`, `pre_aritmetica`, `pre_economia`, `curso-0`) y `sql`, hasta que tengan pub
  (12.º sitio, decisión B3). Su jerarquía es la heredada; `pre_economia/2014-i/sesiones/` conserva sus `aliases:`.
- `_plantillas/` y `_metadata.yml` de esas fichas.

Las URL viejas de los cursos retirados redirigen (301) a su pub por `../_redirects`, generado desde el currículo.

## Límite honesto

- Las fichas preuniversitarias siguen el modelo antiguo de fichas web hasta su traslado.
