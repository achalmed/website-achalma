---
tipo: decision
titulo: "Decisiones, convenciones y pendientes del hub"
estado: activo
---
# Decisiones, convenciones y pendientes del hub

Archivo único y acumulativo (NORMATIVA §15.6, modelo `datafw/docs/decisiones.md`): cada decisión con
su fecha, al final de la sección que le corresponde. `CLAUDE.md` resume; aquí está el porqué. Lo cumplido
y fechado va a `historial/`; lo que cambió y cuándo, al historial de git (no hay `CHANGELOG`: §3.7).

---

## 1. Contenido y secciones

**1.1 `cursos/` unifica `talk/` y `teching/` como repositorio docente tipo OpenCourseWare** (2026-07-09,
PR #10). Jerarquía curso (identidad estable) → edición (un dictado: `<año>-<ciclo>-<institución>`) →
sesión (`session_NN_slug/` con subcarpetas fijas `slides`, `practice`, `homework`, `evaluation`,
`resources/readings`). El curso nunca cambia; se añaden ediciones. Las áreas son `categories:` de la ficha y
facetan solas. Las URL antiguas se conservan con `aliases:`; el `_redirects` de Netlify previsto no se
aplicó. El plan completo: `historial/course-redesign-plan.md`. La excepción heredada
`cursos/pre_economia/2014-i/sesiones/` no se migró al nombre `session_NN_slug`.

**1.2 La ficha de un curso se genera desde `docencia`** (2026-09-06, F5.1–F5.4). La sección «Contenidos /
Sílabo» de `cursos/<curso>/index.qmd` sale de `contenido/cursos/<slug>/curso.yml` con
`docencia/scripts/temario-generar.sh generar --que web --aplicar`, entre marcas `temario:inicio/fin`; las
ediciones se enlazan por hardlink con `publish-web.sh`. Las fichas sin curso en el framework llevan
`draft: true`. Corolario: `cursos/_metadata.yml` es un archivo físico independiente para que un hardlink no
propague cambios.

**1.3 Fechas ISO en toda la familia** (2026-09-15, M6). Todo `date:` es `AAAA-MM-DD`;
`scripts-quarto` normaliza (`fechas-iso`) y deriva de la carpeta (`sync-dates`). Los nueve cursos
renombrados en `docencia` (M7) cambiaron de ruta aquí en la misma fecha; la edición `2025-1-cau-unsch` de
Metodología quedó marcada como legado por no tener fuentes en el framework.

**1.4 Los posts se citan como *Actus Mercator*** (anterior a 2026-07): volumen = año, número 1–4 =
trimestre. Se declara en el `citation` del frontmatter; el esquema no está en ningún manifiesto.

**1.5 El repo `website-achalma` vive en la carpeta `04 index`** (2026-09-06, fusión con el índice del
vault). El nombre del repo y del sitio no cambió; `_indice/` y `_vault/` son del vault Obsidian y no se
versionan (`.gitignore`). `site_libs/` tampoco: lo reconstruye cada render (2026-07-01).

**1.6 El observatorio se copia, no se renderiza** (2026-09-28). `observatorio/index.qmd` es la página de
entrada, con el tema del hub; `observatorio/plataforma.html` es el observatorio completo, autocontenido
(datos, estilos y gráficos dentro), y va en `project.resources` para que Quarto lo copie tal cual: pasarlo
por el render le impondría el tema del hub y rompería su paleta, validada aparte. Los dos los escribe
`datafw/tools/plataforma.py` (`--salida` para la plataforma; `--cifras-en` para el bloque
`<!-- cifras:inicio/fin -->` de la página de entrada): no se editan aquí. El contrato del lado del
proveedor: `datafw/docs/integracion-ecosistema.md` §2 (el observatorio) y §4 (consumidores).

## 2. Los blogs satélite

**2.1 Los 11 blogs son submódulos del hub en `_pubs/`** (2026-09-06, F3a). Cada uno conserva repo,
`_quarto.yml` y sitio Netlify; el hub los registra por https y `shallow = true`. La carpeta lleva guion
bajo para que Quarto no la renderice. Las herramientas los resolvían entonces por `website-achalma/_pubs`;
hoy por `04 index/_pubs` (`pubs-submodulos.md`, «Consumidores»). La reversión de entonces vivía en las
reparaciones de meta, retiradas el 2026-09-20: hoy se revierte con git. Detalle: `pubs-submodulos.md`.

**2.2 El hub es la fuente de verdad del tema** (2026-09-06). SCSS, JS, CSS global y de componentes,
extensiones, `_filters/apa-floats-html.lua` y `scripts/build-page-css.sh` se editan aquí y se propagan con
`scripts/sync-theme-pubs.sh`; `assets/scss/05-pages/`, `assets/css/pages/`, `_filters/_metadata-pdf.lua`, `_quarto.yml`, `index.qmd`,
imágenes, fuentes y GTM se excluyen porque difieren por diseño. Desde DOC5 (2026-09-20) las copias
propagadas lo dicen en su cabecera (`assets/scss/README.md`, `assets/js/README.md`, `build-page-css.sh`).

**2.3 Un registro para los nombres de los blogs** (2026-09-20, DOC5). Carpeta, repo, dominio, tema y
descripción no se derivan unos de otros (`pub_chaska` → `chaska` → `chaska-x.netlify.app`) y estaban
repartidos entre `_quarto.yml`, el menú «More», el README viejo y un comentario de `scripts-quarto`.
Ahora viven en `_pubs/pubs.yml` y de ahí salen, con `scripts/pubs.py`, el `README.md` y el `CITATION.cff`
de cada pub y la tabla del README del hub (NORMATIVA §15.9). El `_quarto.yml` de cada pub y el menú de
navegación siguen a mano.

## 3. Documentación del repo

**3.1 El README del repo está en la raíz y `docs/README.md` es el índice de `docs/`** (2026-09-20, DOC5).
Hasta aquí el README real vivía en `docs/README.md` (296 líneas, con `talk/`, `teching/`, `README/`,
`requirements.txt` y otras seis rutas inexistentes; copiado además en los 11 pubs) y la raíz no tenía
ninguno. Se reescribió desde cero con el contrato §15.4; el índice lo genera `core/docs.py indice`.

**3.2 `CLAUDE.md` en español y por contrato** (2026-09-20, DOC5). Se conservan todos sus detalles
(freeze, glob recursivo, jerarquía real de `cursos/` —el anterior documentaba la excepción `sesiones/`
como regla—, design system, partials, extensiones vendorizadas, Utterances, submódulos y herramientas que
resuelven `_pubs`), sin historial ni árbol.

**3.3 `docs/` queda fuera del render del sitio** (2026-09-20, DOC5). Quarto renderizaba `docs/*.md`
como páginas públicas (el plan de cursos y el manual de Git salían como `.html` bajo `docs/` del sitio) y
también `SECURITY.md` y `CODE_OF_CONDUCT.md`; ninguna estaba enlazada desde la navegación. `project.render`
en `_quarto.yml` los excluía; desde que DOC9 retiró esos dos archivos, solo queda `!docs/`, y
`quarto inspect .` lo comprueba. Con ello, un documento nuevo en `docs/` ya no es
una página del sitio: si algo de `docs/` debe publicarse, se publica como post.

**3.4 Las plantillas apaquarto no son documentación** (2026-09-20, DOC5). `_index_{doc,jou,man,stu}.qmd`
pasan a `_plantillas/apaquarto/` (§15.3: plantillas nunca dentro de `docs/`; el guion bajo de la carpeta
las aparta del render, como `cursos/_plantillas/`). Las tres guías de claves (renombradas en §3.7)
se quedan en `docs/`: son referencia, no plantilla.

**3.5 El plan de `cursos/` pasa a `historial/`** (2026-09-20, DOC5) con `tipo: plan` y `estado: hecho`,
que ya declaraba. publication/_index.md (frontmatter de Hugo/Blogdown, sin cuerpo, `estado: archivado`,
sin referencias) se elimina; git conserva su historia.

**3.6 La licencia se declara tal cual está, sin unificar** (2026-09-20, DOC5; decisión D9 pendiente).
`LICENSE` y `CITATION.cff`: MPL-2.0; `license.qmd` y los `_metadata.yml`: CC BY-SA 4.0; el manual de Git
ya lo formula como código MPL-2.0 / contenido CC BY-SA. Una sola licencia en los 12 sitios la elige el
autor.

**3.7 La documentación se ajusta al perfil del ecosistema** (2026-10-04, DOC10; NORMATIVA §15.11). Las
guías de claves pierden el guion bajo inicial (`metadata-guia.md`, `quarto-guia.md`): lo que las apartaba
del render ya lo hace `!docs/`. La guía simplificada de metadatos se elimina: todas sus claves están ya en la
completa, y el frontmatter de uso diario, en `publicar-un-post.md` §3. Sale la plantilla de issue de GitHub sin rellenar: los issues del repo los usa
Utterances para los comentarios. Se apartan del perfil común, a sabiendas:

- **`.github/FUNDING.yml` se conserva**: el autor lo creó con cuentas reales (Patreon, Buy Me a Coffee,
  thanks.dev), así que acepta financiación en este repo; se queda solo con esas cuentas.
- **Sin `CHANGELOG.md`**: ningún manifiesto declara una versión que alguien consuma (el `version: '3.10'`
  de `CITATION.cff` no lo leía nadie y también sale). Lo que el changelog tenía de decisión vigente está
  en este archivo (§1.5, §1.6, §4.1–§4.3); el resto, en `git log`.
- **Sin `CLAUDE.md` en los pubs**: el del hub es su ancestro en disco y rige para los 11; el README de
  cada pub es generado (`scripts/pubs.py`) y remite al hub.

## 4. Despliegue

**4.1 `_site/` se versiona en los 12 sitios; el push es el despliegue** (2026-09-22, decisión del autor;
cierra D1). Netlify sirve el `_site` del repo con directorio de publicación `_site` y sin comando de
build, así que el artefacto **es** el mecanismo de publicación: `quarto render` → commit de `_site/` →
`git push`. Queda versionado **hasta que el autor diga lo contrario**, en el hub y en los 11 pubs.

Esto contradice a propósito la NORMATIVA §5 y §15.8 («los derivados no se versionan»), que está escrita
para artefactos reconstruibles que nadie sirve. Aquí la regla general choca con la realidad del
despliegue y gana el despliegue. Consecuencia aceptada entonces: `core/archivos.py` marcaba **D08** como
fallo en el hub (superado: §4.2). El precedente que obliga a dejarlo escrito: §4.3.

Las alternativas que se estudiaron y quedan descartadas mientras esta decisión siga en pie: publicar con
`quarto publish netlify` por sitio (exige autorizar la cuenta en cada máquina y no sobrevive a una
reinstalación sin más) y construir en Netlify (`quarto render` en CI necesitaría TinyTeX para los PDF de
apaquarto y `_freeze/` en git).

**4.2 La excepción se declara en el `.gitignore` de los 12 sitios** (2026-10-04, DOC10). Desde el
2026-09-29 el validador acepta `_site/` versionado si el repo lo declara con una línea de negación
(NORMATIVA §15.10, D08). El hub ya la tenía (`!/_site/**/*_files/`, que además devuelve a git las figuras de
los posts frente a la regla general `*_files/`) y pasa; diez pubs reciben el mismo bloque comentado y
`pub_epsilon-y-beta` lo recibirá cuando se resuelva su render (§5).
En `pub_numerus-scriptum` eso deja a la vista unas figuras de `_site/` que la regla general había dejado
fuera de git: confirmarlas es publicar, y queda para el autor (§5).

**4.3 El incidente del 2026-09-21, en breve.** DOC2 sacó `_site/` de git en el hub «por higiene» y añadió
`/_site/` al `.gitignore`, pasando por alto el `#_site/` comentado a propósito; el push siguiente llegó a
Netlify sin directorio de publicación y Netlify publicó un deploy **vacío** (no un build fallido, que
habría conservado el anterior): todas las rutas daban el 404 genérico de Netlify. Se restauró `_site/` con
el render local verificado y la negación de `*_files/`. Lección de método: ante un artefacto ausente, se
pregunta al historial (`git log -- _site`) si alguna vez estuvo, no solo al árbol actual.

### 4.4 El tema se comparte por hardlink (autor, 2026-10-08)

El ADR-06 (ola 1) y el piloto 3 rompían los hardlinks del tema para que cada pub tuviera una copia real. El
autor lo revisa al abrir la ola 6: el tema **se comparte por hardlink**, administrado con
`scripts-linux/script_hardlinks-creator`, para que una edición en un sitio llegue a los doce. Quedan así:
`scripts/tema-hardlinks.txt` (los 60 nombres que el hub y los pubs ya compartían), `sync-theme-pubs.sh`
(iguala, sella y enlaza; `--verificar` detecta un enlace roto) y el doctor RQ-MAN-08, que ya no cuenta un
hardlink como hallazgo sino un enlace roto. `pub_methodica` recuperó sus 61 enlaces (63 creados). Mapa de inodos
de antes y después en `$RESPALDOS_DIR/hardlinks/2026-10-08-tema-sitios/`.

## 5. Pendientes con dueño y fecha

| id | qué | desde | dueño · estado |
|---|---|---|---|
| **epsilon** | `pub_epsilon-y-beta`: el render global del 2026-09-22 se cortó; `_site/` está borrado en disco y hay salidas sueltas en las carpetas fuente. Hay que renderizarlo entero (`quarto render` en el pub), revisar y confirmar **antes de cualquier push** de ese pub, o el sitio quedará vacío (§4.3); después, el bloque de `.gitignore` de §4.2 | 2026-10-04 | autor · **prioritario** |
| figuras de numerus | `_pubs/pub_numerus-scriptum/_site/python/2025-05-10-visualizacion-de-datos-con-python/index_files/`: visibles desde §4.2, sin confirmar; confirmarlas las publica | 2026-10-04 | autor |
| `_freeze/` de numerus | `pub_numerus-scriptum` versiona `_freeze/` (caché de ejecución de sus posts con código); ningún otro sitio lo hace y nada lo declara, así que D08 sigue fallando en ese pub. Decidir si se declara (como `_site/`) o sale de git | 2026-10-04 | autor |
| `CHANGELOG.html` | la página publicada del changelog retirado sigue en `_site/` hasta el próximo render del hub, que ya no la produce | 2026-10-04 | autor · se resuelve con el próximo render |
| **D9** | una sola licencia en los 12 sitios (hoy MPL-2.0 en `LICENSE`/`CITATION.cff` y CC BY-SA en `license.qmd`) | 2026-09-20 | pendiente del autor; el README lo cuenta partido |
| **D16** | destino de `git-github-workflow.md` (manual de Git de 1 088 líneas, material educativo del autor, no documentación del repo): `prompts/` (skill o guía), un post de `pub_numerus-scriptum` o `pub_methodica`, o quedarse | 2026-09-20 | pendiente del autor; mientras tanto sigue en `docs/` con sus rutas corregidas |
| `_redirects` de Netlify | el plan de `cursos/` lo previó para las rutas de sección y no se aplicó; hoy solo hay `aliases:` | 2026-07-09 | autor; D1 se cerró sin él (§4.1) |
| `_site/_pubs/` | `resources: assets/css/pages/listing.css` de `_quarto.yml` casa también con las copias de cada blog y deja copias de esa hoja en `_site/_pubs/`; inocuo | 2026-09-21 | autor · por acotar |
| **`assets/fonts/DankMono-*.woff2` (prioritario)** | Dank Mono es una fuente comercial («All rights reserved» en sus metadatos) y se redistribuye en un repo público y en el sitio: retirarla del repo (y decidir sobre la historia) o comprar una licencia que lo permita; mientras tanto, cambiarla en el tema por una libre. Petrona y Red Hat Text llevan ya su OFL 1.1 (`assets/fonts/LICENSE`) | 2026-10-04 | autor |
| `_extensions/quarto-ext/fontawesome/` (hub y pubs) | extensión incorporada sin su `LICENSE`: reinstalarla con `quarto add quarto-ext/fontawesome`, que trae la suya | 2026-10-04 | autor |
| `resources/cv.pdf` | copia manual desde `09 trabajo`; no hay script que la refresque (el contrato lo declara el proveedor: `09 trabajo/cv/docs/publicar.md` §Consumidores) | 2026-09-20 | autor |
