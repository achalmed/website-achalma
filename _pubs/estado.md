---
tipo: estado
estado: activo
actualizado: 2026-10-05
---
# estado.md — pubs

<!-- Estado único del proyecto `pubs` de meta/workspace.yml (los blogs satélite). Vive aquí, en el hub, y no
     dentro de cada pub: la normativa documental 2.3, fila 10, prohíbe E en un pub («todo vive en el hub»). -->

## Hecho

| fecha | qué | dónde se ve |
|---|---|---|
| 2026-10-05 | piloto 3 en `pub_methodica`: 61 hardlinks rotos, `THEME_VERSION`, `netlify.toml`, `_freeze/` declarado, README regenerado, render y puerta R6 en verde, hook `pre-push` instalado | `pub_methodica` 947af53 · be55860; acta en `meta/programa/05-piloto/piloto.md` §3 |

## En curso

nada en curso

## Por hacer

- 2026-10-05 · dueño: autor · push de `pub_methodica` y del hub (Puerta P5): `git push` en el pub (el hook R6 lo comprueba), después el puntero del hub
- 2026-10-05 · dueño: director (ola 6) · los demás pubs: `scripts/sync-theme-pubs.sh --aplicar`, `netlify.toml`, `!/_freeze/`, README regenerado, render y `puerta-r6.sh --instalar`, uno por commit
- 2026-10-05 · dueño: director (ola 6) · renombre `_pubs/pub_<x>` → `_pubs/<x>` con `git mv` (DC8: funciona con `.git` embebido; `.gitmodules` cambia solo `path`; no renombrar la sección)
- 2026-10-05 · dueño: autor · enlaces internos rotos que ya estaban: `/accessibility.html` del pie (`_quarto.yml`) y `privacy`/`terms` de ejemplo en `posts/2026-01-02-configuracion-de-quarto-yml`
- 2026-10-05 · dueño: director (ola 6) · el PDF de las entradas sale con XeLaTeX (apaquarto): `pdf-engine: lualatex` según la regla 7
- 2026-10-05 · dueño: director (ola 6) · `_pubs/README.md` de la colección (RQ-DOC-01), generado por `scripts/pubs.py`

## Futuro

- un solo comando de publicación de la familia (orden pubs → punteros → hub, RQ-WIP-08) que llame a `scripts/puerta-r6.sh`
- `posts/_metadata.yml` y los `_metadata.yml` de sección son configuración común copiada en cada pub: candidatos a `_quarto-comun.yml` sincronizado
