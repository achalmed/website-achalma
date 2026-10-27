---
tipo: doc
titulo: "Despliegue en Netlify: cómo llegan a producción el hub y los 11 blogs"
estado: activo
---
# Despliegue en Netlify: cómo llegan a producción el hub y los 11 blogs

Los 12 sitios de la familia se sirven en Netlify y **se publican igual**: `scripts/render.sh` (HTML) y
`scripts/render.sh --documentos --aplicar` (PDF y DOCX que cambiaron) en local → commit de `_site/` →
`git push`. Cada sitio Netlify está enlazado a su repo de GitHub con directorio de
publicación `_site` y sin comando de build, así que el `_site/` versionado **es** el despliegue. Por qué es
así y por qué `_site/` no se saca de git: `decisiones.md` §4.1–§4.3. Nada de la configuración de Netlify
vive en los repos salvo un `netlify.toml` por sitio (ola 6) que fija lo mismo que la interfaz: `publish = "_site"` y ningún comando de build; no hay `_redirects` ni variables de build versionadas.

## El hub (`web` → <https://achalmaedison.netlify.app>)

**Cómo se publica.** Push de `_site/` a `main` de `website-achalma`; Netlify sirve ese directorio tal cual.
Lo confirma el historial (`git log -- _site`: los cambios del sitio llegan como commits de `_site/`) y lo
demostró el incidente del 2026-09-21 (`decisiones.md` §4.3): un push sin `_site/` publicó un sitio vacío,
no un build fallido.

`_publish.yml` solo registra el id del sitio que `quarto publish` creó en su día:

```yaml
- source: project
  netlify:
    - id: 6d1408cc-afc8-4b2d-8706-26c28e536a05
      url: "https://achalmaedison.netlify.app"
```

Un sitio enlazado a git acepta también deploys por API, así que `quarto publish netlify` (renderiza y sube
`_site/`; `--no-render` sube el último render) es una vía posible al mismo sitio, pero no es el flujo del
autor: en una máquina nueva exige autorizar la cuenta en el navegador y, observado el 2026-09-21, sin
cuenta y sin terminal interactiva (`--no-prompt`, stdin cerrado) **sale con código 0 sin publicar nada ni
avisar**: un script no puede fiarse de su código de salida.

**Lo que hace el render antes de publicar.** `_quarto.yml` declara `pre-render: scripts/build-page-css.sh`
(compila `assets/scss/05-pages/*.scss` → `assets/css/pages/*.css` con el dart-sass que trae Quarto) y
`freeze: true` (un render global no ejecuta R ni Python: reutiliza `_freeze/`). `blog/posts/_metadata.yml`
y `cursos/_metadata.yml` además fijan `execute.enabled: false`. Los PDF y DOCX de los posts los produce
`apaquarto`, que necesita TinyTeX: por eso el render se hace en la máquina del autor, no en Netlify.
`observatorio/plataforma.html` no pasa por el render: va en `project.resources` y se copia tal cual
(`decisiones.md` §1.6).

**Render rápido y documentos aparte** (fase 2 de `plataforma-educativa.md`, 2026-10-20; el porqué en
`decisiones.md` §4.5). Cada post declara `html`, `apaquarto-pdf` y `apaquarto-docx`, y compilar los dos
últimos con LuaLaTeX en cada render era casi todo el tiempo de publicar (unos 47 min los 12 sitios).
`scripts/render.sh`, que viaja con el tema, hace ahora tres cosas:

| orden | qué hace | methodica (7 posts) |
|---|---|---|
| `scripts/render.sh` | `quarto render --to html`; antes aparta los PDF y DOCX de `_site/` (un render completo de Quarto vacía `_site/`) y después devuelve los de las páginas que siguen publicadas | 20 s (antes 109 a 184 s) |
| `scripts/render.sh --documentos [--aplicar]` | `scripts/documentos.py`: compila los formatos de documento solo de las páginas cuya clave cambió; simula sin `--aplicar` | 1 s sin cambios · unos 20 s por post cambiado · 157 s todo desde cero |
| `scripts/render.sh --completo` | el render de antes: todos los formatos de cada página | 184 s |

Los enlaces «Otros formatos» de cada página no dependen de esto: Quarto los escribe con los formatos
declarados aunque no los compile. La caché es `_documentos.tsv` en la raíz de cada sitio (GENERADO,
versionada con el `_site/` que describe; se confirma junto con él): página, formato, salida, clave y
sha256 de la salida. Si alguien pisa o borra un PDF de `_site/`, el siguiente `--documentos` lo rehace.
Para adoptar un sitio cuyo `_site/` salió de un render completo con las fuentes confirmadas, sin
recompilar: `scripts/render.sh --documentos --registrar --aplicar`. `--verificar` sale 1 si a alguna
página publicada le falta un documento al día.

**Qué queda fuera del render.** `project.render` en `_quarto.yml` renderiza `*.qmd` y `*.md` y excluye
`!docs/`; las carpetas y archivos que empiezan por `_` o `.` los excluye Quarto por defecto (`_pubs/`,
`_plantillas/`, `_extensions/`, `_filters/`, `_partials/`, los `_metadata.yml`); los `README.md` tampoco
se renderizan. `quarto inspect .` lista las entradas exactas.

**URL antiguas.** Desde el retiro de `cursos/` (`decisiones.md` §4.7) el hub lleva `_redirects` (recurso de
`_quarto.yml`, generado por `scripts/redirecciones-cursos.py`): cada curso, edición, sesión, material y alias
`/talk/…` va con 301 a su pub. Lo preuniversitario que queda en `cursos/` conserva sus `aliases:` (Quarto genera
la página de redirección).

**Residuos.** `CNAME` (`kapitan.net`) y `.nojekyll` son de la época de GitHub Pages; Netlify no los lee.
`.github/` solo tiene `FUNDING.yml`: no hay GitHub Actions.

**Submódulos.** Como el hub no renderiza `_pubs/` (empieza por `_`) y Netlify no construye nada, los
submódulos no aportan nada al sitio del hub; `.gitmodules` los registra por https y `shallow = true` para
que un clon anónimo pueda traerlos.

**Lo que queda por confirmar en el panel** (sitio `6d1408cc-…`): si hay un dominio propio configurado (el
`CNAME` sugiere que lo hubo en GitHub Pages).

## Los pubs (`_pubs/*`): publican la vitrina

Desde la fase 7 de `plataforma-educativa.md` (2026-10-20) cada pub publica `_vitrina/`, el sitio que construye
`_aula` (catálogo, cursos, lecciones, ediciones, blog), y no el `_site/` de Quarto, que sigue en el repo como fuente
del texto de las lecciones y de sus PDF/DOCX. Su `netlify.toml` dice `base = "/"` (cinco sitios tenían `_site` como
base en el panel) y `publish = "_vitrina"`; `_vitrina/_redirects` lleva con 301 cada URL del sitio Quarto. Publicar un
pub, de principio a fin:

1. En el pub: escribir y confirmar; `scripts/render.sh` (solo HTML) y, si cambió un documento,
   `scripts/render.sh --documentos --aplicar`; confirmar `_site/`, `_freeze/` y `_documentos.tsv`.
2. En el hub: `_aula/scripts/publicar.sh <pub> --aplicar` (construye la vitrina, exige 0 rutas perdidas y 0 enlaces
   rotos, falla si el `.gitignore` deja fuera algo de `_vitrina/`) y confirmar `_vitrina/` en el pub.
3. `git push` del pub (la puerta R6 del gancho `pre-push` comprueba el render) y el puntero en el hub
   (`pubs-submodulos.md`). Un cambio grande (estructura, rutas) va por rama y *pull request*: Netlify da una vista
   previa (`deploy-preview-N--<sitio>.netlify.app`) antes del merge.

Volver al sitio Quarto de un pub: `_aula/scripts/publicar.sh <pub> --volver --aplicar` (`publish = "_site"`).
Su despliegue no depende del hub: los pubs respondían `200` con el hub caído el 2026-09-21.

## Verificación

```bash
quarto inspect . | python3 -c "import json,sys; print(len(json.load(sys.stdin)['files']['input']))"  # entradas del hub
scripts/render.sh && ls _site/                      # el sitio completo en local, solo HTML (conserva PDF y DOCX)
scripts/render.sh --documentos --verificar          # 0 si cada página publicada tiene sus PDF y DOCX al día
git ls-files _site | wc -l                          # cuántos archivos de _site versiona el hub; 0 = el sitio saldrá vacío
git status --short _site | head                     # tras un render: lo que cambia y hay que confirmar antes del push
curl -sS -o /dev/null -w "%{http_code}\n" https://achalmaedison.netlify.app/   # 200 tras el push (Netlify tarda ~1 min)
git -C _pubs/axiomata ls-files _site | wc -l    # lo mismo en un pub
```

## Consumidores

Leen o publican lo que producen estos 12 sitios:

- `scripts-quarto/backend/script_blogs_manager` (`main.sh render|publish <blog>`; `publish` envuelve
  `quarto publish`, que no es el flujo vigente).
- `raphi`: su «Inventario de páginas» con la fuente «blogs del hub» (`raphi/fuentes/hub.py`, receta
  `paginas-de-los-blogs`) cuenta las páginas de los PDF de `web/_site` y de `_pubs/*/_site`.
- `meta/doctor/main.sh` y `core/archivos.py` (D08): aceptan `_site/` versionado solo donde el `.gitignore`
  lo declara con una negación.
