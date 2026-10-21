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

Prototipo en construcción (fase 4); los comandos se documentan aquí cuando existan.

## Estructura

| carpeta | qué contiene |
|---|---|
| `docs/` | decisiones y documentación del repo (`docs/README.md`, índice generado) |

## Límite honesto

- Es un prototipo: ningún sitio en producción lo usa todavía; los 12 sitios siguen siendo Quarto hasta la fase 7.
- El aula con cuenta (API) no existe aún (fase 6).
