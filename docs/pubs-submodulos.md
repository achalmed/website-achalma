# Los blogs satélite (`_pubs/pub_*`) como submódulos del hub

> Reorganización aplicada el 2026-09-06 (fase F3a del diagnóstico integral,
> `~/Documents/ecosistema/DIAGNOSTICO_INTEGRAL_2026-09.md`). Antes los 11
> `pub_*` eran carpetas hermanas de `website-achalma` en `~/Documents`.

## Qué es y qué no es

- Cada `pub_*` **sigue siendo su propio repositorio** (remote ssh
  `git@github.com:achalmed/<nombre>.git`), su propio proyecto Quarto y su
  propio sitio Netlify. Nada de eso cambió.
- El hub registra los 11 en `.gitmodules` con URL **https** (para que Netlify
  y cualquier clon anónimo puedan traerlos) y `shallow = true` (clon
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
cd ~/Documents/website-achalma/_pubs/pub_axiomata
quarto preview            # o render
git add -A && git commit -m "post: ..."
git push                  # remote propio del blog (ssh)

# 2) Mover el puntero del submódulo en el hub
cd ~/Documents/website-achalma
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
scripts/sync-theme-pubs.sh              # simula: muestra qué cambiaría
scripts/sync-theme-pubs.sh --aplicar    # escribe en cada _pubs/pub_*
scripts/sync-theme-pubs.sh --verificar  # sale 1 si algún blog difiere
```

No se sincronizan a propósito: `assets/scss/05-pages/`, `assets/css/pages/`,
`_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd`, `assets/img/`,
`assets/fonts/`, `assets/gtm-*.html` (difieren entre hub y satélites por
diseño). Tras `--aplicar`, hacer commit en cada blog y luego en el hub.

## Herramientas que conocen la nueva ruta

| Herramienta | Variable | Valor por defecto |
|---|---|---|
| `scripts_quarto_studio/backend/script_blogs_manager` | `QBLOG_PUBS_SUBDIR` | `website-achalma/_pubs` |
| `scripts_quarto_studio/backend/script_pub_index_symlink` (`04 index`) | `PUBINDEX_PUBS_SUBDIR` | `website-achalma/_pubs` |
| `scripts_quarto_studio/backend/script_metadata_manager` | `PUBS_SUBDIR` (`lib/config.py`) | `website-achalma/_pubs` |
| `scripts_document_studio/backends/page-counter` | `SUBDIR_PUBS` (`config.py`) | `website-achalma/_pubs` |
| `scripts_for_linux/.../script_git_sync_respos` | `repos-config.yml` (`name` = ruta relativa) | `website-achalma/_pubs/pub_*` |

Todas aceptan el nombre de carpeta (`pub_axiomata`) o el corto (`axiomata`).
Si alguna vez los blogs se mueven, cambiar solo esas variables.

## Netlify

- Sitios de cada blog: sin cambios (construyen desde su propio repo).
- Sitio del hub: al construir, Netlify inicializa los submódulos (https,
  superficiales). Si el tiempo de build crece demasiado, la alternativa es
  `git config -f .gitmodules submodule.<ruta>.update none` para que el hub no
  los descargue en CI (localmente se fuerzan con
  `git submodule update --init --checkout`).

## Reversión

`~/Documents/ecosistema/reparaciones/F3a_pubs_submodulos_2026-09-06/UNDO.sh`
(simula por defecto; `--aplicar` devuelve los 11 blogs a `~/Documents/pub_*`,
quita los submódulos del hub, restaura las herramientas y regenera `04 index`).
