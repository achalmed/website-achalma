---
tipo: procedimiento
titulo: "Publicar un post de principio a fin: carpeta, frontmatter APA, metadatos, render, commit, puntero e índice"
estado: activo
---
# Publicar un post de principio a fin: carpeta, frontmatter APA, metadatos, render, commit, puntero e índice

Un post vive en el hub (`blog/posts/`) o en uno de los 11 blogs (`_pubs/pub_*`); el procedimiento es el
mismo salvo en dónde se confirma y cómo llega a producción. Todos los comandos de `scripts_quarto_studio`
se ejecutan desde la carpeta de la herramienta (`scripts_quarto_studio/backend/<herramienta>/`) y aceptan el
nombre de carpeta (`pub_axiomata`) o el corto (`axiomata`); los que escriben en masa simulan con
`--dry-run` y esa es siempre la primera corrida.

## 1. Dónde va

- **Tema de un blog** → dentro de ese pub, en `posts/` o en su carpeta temática (`pub_axiomata` tiene
  `posts/` y `economia-matematica/`; `pub_chaska`, `pub_epsilon-y-beta` y `pub_numerus-scriptum` no tienen
  `posts/`, solo carpetas temáticas). Qué blog cubre qué tema: `_pubs/pubs.yml` y la tabla «Los 11 blogs
  satélite» del `README.md`.
- **Transversal o personal** → el hub, `blog/posts/`.

La carpeta es `AAAA-MM-DD-slug/` (la fecha es la de publicación y el slug, en kebab) y dentro va
`index.qmd` con sus adjuntos (`featured.jpg`, imágenes, `mybibliography.bib`, datos). Ejemplo real:
`blog/posts/2023-05-12-la-economia-peruana-entre-1970-1990/index.qmd`.

## 2. Crear el post

A mano (copiar un post vecino y vaciarlo) o con el asistente interactivo del gestor de blogs:

```bash
cd scripts_quarto_studio/backend/script_blogs_manager
./main.sh new-post pub_epsilon-y-beta      # formulario: título, slug, fecha, categorías…
```

## 3. Frontmatter

Los valores comunes ya están en el `_metadata.yml` de la sección (`blog/posts/_metadata.yml` en el hub;
`_pubs/pub_axiomata/posts/_metadata.yml` en ese pub, y análogo en los demás): autor, afiliación, ORCID, formatos `html`, `apaquarto-pdf` y
`apaquarto-docx`, comentarios Utterances, `execute.enabled: false` y **`draft: true` por defecto**. El
`index.qmd` declara lo propio:

```yaml
title: Economía peruana 1970-1990
subtitle: crisis y reformas
shorttitle: ECONOMÍA PERUANA 1970-1990       # cabecera APA
abstract: …
keywords: [Peruvian Economy, Economic reforms]
categories: [Política Económica]             # facetas del listado
tags: [economia_peruana]                     # snake_case; los normaliza normalize-tags
description: …                               # resumen de la tarjeta
date: 2023-05-12                             # ISO, igual que la carpeta
draft: false                                 # sin esto el post no se publica
image: ../featured.jpg
citation:
  type: article-journal
  author: [Edison Achalma]
  pdf-url: https://achalmaedison.netlify.app/blog/posts/2023-05-12-la-economia-peruana-entre-1970-1990/index.pdf
```

Referencia de cada clave: `_metadata-guia.md` (completa) y `_metadata-guia-simplificada.md` (cotidiana);
`_quarto-guia.md` para el sitio. Para un documento académico completo (ensayo, artículo en dos columnas,
manuscrito, trabajo de estudiante) se parte de `../_plantillas/apaquarto/index_{doc,jou,man,stu}.qmd`. Los
posts se citan como *Actus Mercator*: volumen = año, número 1–4 = trimestre (ene–mar, abr–jun, jul–sep,
oct–dic).

Ordenar y entrecomillar el YAML, si se escribió a mano:

```bash
cd scripts_quarto_studio/backend/script_format_yaml
python3 main.py --file "<ruta al post>/index.qmd"
python3 main.py --directory "<carpeta de posts>" --recursive --dry-run   # varios, simulando
```

## 4. Metadatos en masa (Excel) y derivados de la ruta

La base de metadatos de toda la familia es
`scripts_quarto_studio/backend/script_metadata_manager/excel_databases/quarto_metadata.xlsx`; **el frontmatter
de los `.qmd` es la verdad** y el Excel, la herramienta para editarlo en lote. `~/Documents` es la raíz que
la herramienta recorre (resuelve `04 index` y `_pubs/` por su configuración).

```bash
cd scripts_quarto_studio/backend/script_metadata_manager
python3 main.py create-template ~/Documents --config metadata_config.yml     # Excel con lo que hay hoy
python3 main.py update ~/Documents excel_databases/quarto_metadata.xlsx --dry-run   # qué cambiaría
python3 main.py update ~/Documents excel_databases/quarto_metadata.xlsx             # aplica
python3 main.py sync-dates ~/Documents --config metadata_config.yml --dry-run   # date ← carpeta AAAA-MM-DD
python3 main.py sync-pdf-urls ~/Documents --config metadata_config.yml --dry-run # citation.pdf-url ← ruta real
python3 main.py fechas-iso "~/Documents/04 index" --dry-run                    # solo la grafía de date
python3 main.py normalize-tags ~/Documents --dry-run                           # tags a snake_case
python3 main.py audit-tags ~/Documents                                         # informe de etiquetas
```

Dos límites que conviene saber: `sync-pdf-urls` **nunca crea** el bloque `citation`, solo actualiza uno
existente (escríbelo en el post); y los posts sin `tags` se omiten en las operaciones de etiquetas. La URL
base de cada blog se deduce por mayoría de las `pdf-url` existentes (`pub_chaska` → `chaska-x.netlify.app`)
y puede fijarse en `blog_base_urls` de `metadata_config.yml`.

## 5. Renderizar y revisar

```bash
cd "04 index/_pubs/pub_axiomata"          # o la raíz del hub
quarto preview                            # con recarga
quarto render posts/<AAAA-MM-DD-slug>/index.qmd   # solo el post (ejecuta su código, produce HTML, PDF y DOCX)
quarto render                             # el sitio entero (freeze: no re-ejecuta código)
```

O con el gestor: `./main.sh preview pub_axiomata`, `./main.sh render pub_axiomata` desde
`scripts_quarto_studio/backend/script_blogs_manager`. Revisar en `_site/` el HTML, el PDF (`index.pdf`) y
que `citation.pdf-url` apunte a él.

## 6. Índices de contenido del blog

Cada blog lleva índices `_contenido_<sección>.qmd` con enlaces al artículo y a su PDF; los regenera el
generador, no se editan a mano:

```bash
cd scripts_quarto_studio/backend/script_generador_publicacion_similar
./main.sh "<ruta al pub>" --dry-run
./main.sh "<ruta al pub>"
```

## 7. Confirmar

En un **blog**: commit y push dentro del pub y después el puntero en el hub.

```bash
cd "04 index/_pubs/pub_axiomata"
git add -A && git commit -m "post: <título>" && git push
cd "04 index"
git add _pubs/pub_axiomata && git commit -m "pubs: axiomata al último commit" && git push
```

En el **hub** (`blog/posts/`): commit normal en `04 index`.

## 8. Publicar

- **Hub:** igual que un blog: `quarto render` → commit de `_site/` → `git push`; Netlify sirve el `_site`
  del repo, sin build (confirmado el 2026-09-21: sacar `_site/` de git en DOC2 dejó el hub vacío).
- **Blog:** hoy los 11 versionan `_site/` y todo indica que Netlify publica el `_site` empujado, sin build
  (`despliegue-netlify.md`, D1): el `quarto render` del paso 5 tiene que estar hecho **antes** del commit
  del paso 7, y `_site/` incluido en él. Si D1 cambia el modo, este paso cambia con él.

## 9. El índice del vault

`04 index/_indice/` (ignorado en git) enlaza por año cada carpeta de publicación de la familia; se
regenera, no se cura:

```bash
cd scripts_quarto_studio/backend/script_pub_index_symlink
./main.sh --dry-run
./main.sh
```

## Lista de comprobación

1. Carpeta `AAAA-MM-DD-slug/` con `index.qmd`; `date` igual a la carpeta; `draft: false`.
2. `title`, `shorttitle`, `abstract`, `keywords`, `categories`, `tags`, `description`, `citation` completos.
3. Render del post sin errores; PDF generado; `pdf-url` correcta.
4. `_contenido_*.qmd` regenerados (blog).
5. Commit en el pub → puntero en el hub (blog) · render, commit de `_site/` y push (hub).
6. `_indice/` regenerado.
