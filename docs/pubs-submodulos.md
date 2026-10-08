---
tipo: doc
titulo: "Los blogs satélite (`_pubs/pub_*`) como submódulos del hub"
estado: activo
---

# Los blogs satélite (`_pubs/pub_*`) como submódulos del hub

Cómo se trabaja con los 11 blogs satélite, que viven dentro del hub como submódulos git, y qué
herramientas dependen de esa ruta. Por qué se organizó así: `decisiones.md` §2.1.

## Qué es y qué no es

- Cada `pub_*` **sigue siendo su propio repositorio** (remote ssh
  `git@github.com:achalmed/<nombre>.git`), su propio proyecto Quarto y su
  propio sitio Netlify. Nada de eso cambió.
- El hub registra los 11 en `.gitmodules` con URL **https** (para que
  cualquier clon anónimo pueda traerlos) y `shallow = true` (clon
  superficial: solo el árbol de trabajo, no el historial).
- La carpeta se llama `_pubs/` con guion bajo porque Quarto ignora los
  directorios que empiezan por `_`: el hub no renderiza ni copia los blogs
  (`quarto inspect .` → 0 inputs bajo `_pubs`). Al ejecutar `quarto render`
  dentro de `_pubs/pub_x`, Quarto usa el `_quarto.yml` del propio blog.
- El `.git` de cada pub sigue **dentro** de su carpeta (no se absorbió en
  `.git/modules` del hub), así que borrar `website-achalma/` borraría también
  los repos de los blogs: tratar `_pubs/` como parte del hub.

## Flujo de trabajo diario

```bash
# 1) Escribir/editar en el blog y confirmar allí
cd "04 index/_pubs/pub_axiomata"
quarto preview            # o quarto render, que regenera _site/
git add -- <rutas del post> _site && git commit -m "post: ..."
git push                  # remote propio del blog (ssh); es el despliegue (despliegue-netlify.md)

# 2) Mover el puntero del submódulo en el hub
cd ../..
git add _pubs/pub_axiomata
git commit -m "pubs: axiomata al último commit"
git push
```

Si se olvida el paso 2, el hub sigue apuntando al commit anterior del blog:
no rompe nada, pero un clon nuevo del hub verá el blog desactualizado.

```bash
# Ver en qué commit está cada blog respecto al hub
git submodule status

# Traer los últimos commits de main de todos los blogs y actualizar punteros
git submodule update --remote --merge
git add _pubs && git commit -m "pubs: actualizar punteros"
```

## Clon nuevo

```bash
git clone --recurse-submodules git@github.com:achalmed/website-achalma.git
# o, si ya está clonado:
git submodule update --init
```

Los submódulos se clonan por https (solo lectura). Para poder hacer push
desde un clon nuevo, cambiar el remote de cada blog a ssh:

```bash
git -C _pubs/pub_axiomata remote set-url origin git@github.com:achalmed/axiomata.git
```

## Tema compartido

El tema (SCSS, JS, filtros Lua, extensiones `apaquarto`/`fontawesome`/
`lightbox`, `build-page-css.sh`) vive **en el hub** y se propaga a los blogs:

```bash
scripts/sync-theme-pubs.sh                          # simula: muestra qué cambiaría
scripts/sync-theme-pubs.sh --pub methodica --aplicar   # escribe en un blog (sin --pub, en todos)
scripts/sync-theme-pubs.sh --verificar              # sale 1 si algún blog difiere
```

El tema se comparte **por hardlink** (decisión del autor, 2026-10-08; normativa 7.11): editar un archivo del
tema en el hub lo cambia en los doce sitios. `--aplicar` iguala el contenido con `rsync`, escribe `THEME_VERSION`
(el sello con el commit del hub y la suma del conjunto) y al final enlaza los archivos de igual nombre y contenido
de `scripts/tema-hardlinks.txt` con `scripts-linux/script_hardlinks-creator`. `_extensions/` no se enlaza: se copia.
`rsync`, `git checkout` y los editores que guardan con un temporal y un renombre rompen el enlace sin avisar:
`--verificar` sale 1 si un archivo de la lista quedó sin enlazar, y `--aplicar` lo repara.

No se sincronizan a propósito: `assets/scss/05-pages/`, `assets/css/pages/`,
`_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd`, `assets/img/`,
`assets/fonts/`, `assets/gtm-*.html` (difieren entre hub y satélites por
diseño). Tras `--aplicar`, hacer commit en cada blog y luego en el hub.

## Netlify

Cada blog se publica desde su propio repo con el push de su `_site/`, y el hub
no construye ni sirve los blogs: `despliegue-netlify.md`.

## Consumidores

Herramientas del workspace que resuelven los blogs bajo `04 index/_pubs`. El
valor por defecto de cada variable lo fija su herramienta; si los blogs se
mueven, se cambia ahí.

| Archivo que lo fija | Variable |
|---|---|
| `scripts-quarto/backend/script_blogs_manager/lib/00-config.sh` | `QBLOG_WEBSITE_DIR`, `QBLOG_PUBS_SUBDIR` |
| `scripts-quarto/backend/script_pub_index_symlink/lib/00-config.sh` | `PUBINDEX_PUBS_SUBDIR` |
| `scripts-quarto/backend/script_metadata_manager/lib/config.py` | `HUB_DIR`, `PUBS_SUBDIR` |
| `scripts_document_studio/backends/page-counter/config.py` | `SUBDIR_PUBS` |
| `scripts-linux/script_git_sync_respos/repos-config.yml` | una entrada por pub |

Las de `scripts-quarto` aceptan el nombre de carpeta (`pub_axiomata`) o
el corto (`axiomata`). Qué escribe `scripts-quarto` en el hub y en los
pubs: su `README.md`, «Contrato con el hub».
