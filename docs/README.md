---
tipo: readme
estado: activo
---
# docs/ — documentación permanente del hub `04 index`: cómo se publica, cómo se escribe un post, los blogs como submódulos y las referencias de claves

Orden de lectura, tipo y estado de cada documento (NORMATIVA §15.6). Los `_*.md` son referencias anotadas
(YAML dentro de bloques de código) y, como todo `docs/`, quedan fuera del render del sitio
(`project.render` en `_quarto.yml`). `historial/` guarda los planes cumplidos; `img/`, las imágenes de los
documentos. Las plantillas apaquarto no viven aquí sino en `_plantillas/apaquarto/`.

<!-- docs:inicio -->
| documento | tipo | estado | qué es |
|---|---|---|---|
| [_metadata-guia-simplificada.md](_metadata-guia-simplificada.md) | `doc` | `activo` | Guía simplificada de metadatos de `_metadata.yml` para uso cotidiano |
| [_metadata-guia.md](_metadata-guia.md) | `doc` | `activo` | Guía completa de metadatos de un `_metadata.yml` (apaquarto y Quarto) |
| [_quarto-guia.md](_quarto-guia.md) | `doc` | `activo` | Referencia de opciones de `_quarto.yml` (sitio Quarto) |
| [decisiones.md](decisiones.md) | `decision` | `activo` | Decisiones, convenciones y pendientes del hub |
| [despliegue-netlify.md](despliegue-netlify.md) | `doc` | `activo` | Despliegue en Netlify: el hub y los 11 blogs (qué se sabe y qué hay que confirmar) |
| [git-github-workflow.md](git-github-workflow.md) | `doc` | `activo` | Manual de Git y GitHub — flujo de trabajo de `website-achalma` |
| [publicar-un-post.md](publicar-un-post.md) | `procedimiento` | `activo` | Publicar un post de principio a fin: carpeta, frontmatter APA, metadatos, render, commit, puntero e índice |
| [pubs-submodulos.md](pubs-submodulos.md) | `doc` | `activo` | Los blogs satélite (`_pubs/pub_*`) como submódulos del hub |
| [historial/README.md](historial/README.md) | `readme` | `activo` | docs/historial/ — lo cumplido: planes ejecutados e instantáneas superadas del hub |
| [historial/course-redesign-plan.md](historial/course-redesign-plan.md) | `plan` | `hecho` | Plan de rediseño de la arquitectura docente — de `talk`/`teching` a `Cursos` |

<sub>Bloque generado por `core/docs.py indice` desde el frontmatter de docs/ (2026-09-20); no se edita a mano.</sub>
<!-- docs:fin -->
