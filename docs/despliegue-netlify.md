---
tipo: doc
titulo: "Despliegue en Netlify: cómo llegan a producción el hub y los 11 blogs"
estado: activo
---
# Despliegue en Netlify: cómo llegan a producción el hub y los 11 blogs

Los 12 sitios de la familia se sirven en Netlify y **se publican igual**: `quarto render` en local →
commit de `_site/` → `git push`. Cada sitio Netlify está enlazado a su repo de GitHub con directorio de
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

**Qué queda fuera del render.** `project.render` en `_quarto.yml` renderiza `*.qmd` y `*.md` y excluye
`!docs/`; las carpetas y archivos que empiezan por `_` o `.` los excluye Quarto por defecto (`_pubs/`,
`_plantillas/`, `_extensions/`, `_filters/`, `_partials/`, los `_metadata.yml`); los `README.md` tampoco
se renderizan. `quarto inspect .` lista las entradas exactas.

**URL antiguas.** Las sesiones migradas de `talk/` y `teching/` a `cursos/` conservan su URL por
`aliases:` en el frontmatter: Quarto genera páginas de redirección dentro de `_site/`. No hay `_redirects`
de Netlify; el plan de rediseño lo contemplaba (`historial/course-redesign-plan.md` §7) y no se aplicó.

**Residuos.** `CNAME` (`kapitan.net`) y `.nojekyll` son de la época de GitHub Pages; Netlify no los lee.
`.github/` solo tiene `FUNDING.yml`: no hay GitHub Actions.

**Submódulos.** Como el hub no renderiza `_pubs/` (empieza por `_`) y Netlify no construye nada, los
submódulos no aportan nada al sitio del hub; `.gitmodules` los registra por https y `shallow = true` para
que un clon anónimo pueda traerlos.

**Lo que queda por confirmar en el panel** (sitio `6d1408cc-…`): si hay un dominio propio configurado (el
`CNAME` sugiere que lo hubo en GitHub Pages).

## Los 11 blogs (`_pubs/*`)

Ninguno tiene `_publish.yml` ni `_redirects`; todos llevan el mismo `netlify.toml` que el hub; los 11 versionan `_site/` y lo declaran en su
`.gitignore` (`decisiones.md` §4.2; `epsilon-y-beta`, pendiente de su render: §5). Su dominio consta en su `_quarto.yml` (`site-url`) y en
`_pubs/pubs.yml`. Se publican como el hub: render en el pub, commit de `_site/` dentro del pub, `git push`
a su remoto; después, el puntero en el hub (`pubs-submodulos.md`). Los 11 respondían `200` con el hub caído
el 2026-09-21: su despliegue no depende del hub.

Por confirmar en el panel, por cada blog, si alguna vez cambia algo: el repo enlazado, la rama (`main`), el
comando de build (se espera vacío) y el directorio de publicación (se espera `_site`).

## Verificación

```bash
quarto inspect . | python3 -c "import json,sys; print(len(json.load(sys.stdin)['files']['input']))"  # entradas del hub
quarto render && ls _site/                          # el sitio completo en local
git ls-files _site | wc -l                          # cuántos archivos de _site versiona el hub; 0 = el sitio saldrá vacío
git status --short _site | head                     # tras un render: lo que cambia y hay que confirmar antes del push
curl -sS -o /dev/null -w "%{http_code}\n" https://achalmaedison.netlify.app/   # 200 tras el push (Netlify tarda ~1 min)
git -C _pubs/axiomata ls-files _site | wc -l    # lo mismo en un pub
```

## Consumidores

Leen o publican lo que producen estos 12 sitios:

- `scripts-quarto/backend/script_blogs_manager` (`main.sh render|publish <blog>`; `publish` envuelve
  `quarto publish`, que no es el flujo vigente).
- `scripts_document_studio`: `backends/page-counter` cuenta las páginas de los PDF de `web/_site` y
  de `_pubs/*/_site`; `backends/pdf-suite` incluye `web` entre sus carpetas de búsqueda.
- `meta/doctor/main.sh` y `core/archivos.py` (D08): aceptan `_site/` versionado solo donde el `.gitignore`
  lo declara con una negación.
