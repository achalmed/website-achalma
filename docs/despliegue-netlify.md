---
tipo: doc
titulo: "Despliegue en Netlify: el hub y los 11 blogs (qué se sabe y qué hay que confirmar)"
estado: activo
---
# Despliegue en Netlify: el hub y los 11 blogs (qué se sabe y qué hay que confirmar)

Los 12 sitios de la familia se sirven en Netlify. Nada de la configuración de Netlify vive en los repos:
no hay `netlify.toml`, ni `_redirects`, ni variables de build versionadas. Este documento reúne lo que el
repositorio permite afirmar y separa, con claridad, lo que solo el panel de Netlify puede confirmar. Es
la base de la decisión **D1** del diagnóstico documental (`meta/diagnosticos/DIAGNOSTICO_DOCUMENTACION_2026-09.md`
§7): sacar `_site/` de git en los 12 sitios (hub y 11 blogs).

## El hub (`04 index` → <https://achalmaedison.netlify.app>)

**Cómo se publica.** Igual que los blogs: `quarto render` en local → commit de `_site/` → `git push`. El
sitio Netlify está enlazado al repo de GitHub con directorio de publicación `_site` y **sin comando de
build**: cada push publica el `_site` versionado tal cual. Por eso `_site/` está en git a propósito (el
`.gitignore` original tenía `#_site/` comentado) y el historial son commits «render: `_site` actualizado».
Se confirmó el 2026-09-21, cuando sacar `_site/` de git (DOC2) dejó el hub vacío (véase el incidente).

Esta sección decía, desde DOC5 hasta ese día, que el hub se publicaba con `quarto publish netlify`. Era una
inferencia a partir de `_publish.yml`, que solo registra el id del sitio que `quarto publish` creó:

```yaml
- source: project
  netlify:
    - id: 6d1408cc-afc8-4b2d-8706-26c28e536a05
      url: "https://achalmaedison.netlify.app"
```

Un sitio enlazado a git también acepta deploys por API, así que `quarto publish netlify` (que renderiza y
sube `_site/`; `--no-render` sube el último render) sigue siendo una vía posible, pero no es el flujo del
autor y en una máquina reinstalada exige volver a autorizar la cuenta de Netlify en el navegador.

**Lo que hace el render antes de publicar.** `_quarto.yml` declara `pre-render: scripts/build-page-css.sh`
(compila `assets/scss/05-pages/*.scss` → `assets/css/pages/*.css` con el dart-sass que trae Quarto) y
`freeze: true` (un render global no ejecuta R ni Python: reutiliza `_freeze/`). `blog/posts/_metadata.yml`
y `cursos/_metadata.yml` además fijan `execute.enabled: false`. Los PDF y DOCX de los posts los produce
`apaquarto`, que necesita TinyTeX: por eso el render se hace en la máquina del autor, no en Netlify.

**Qué queda fuera del render.** `project.render` en `_quarto.yml` excluye `docs/`, `SECURITY.md` y
`CODE_OF_CONDUCT.md` (DOC5); las carpetas y archivos que empiezan por `_` o `.` los excluye Quarto por
defecto (`_pubs/`, `_plantillas/`, `_extensions/`, `_filters/`, `_partials/`, los `_metadata.yml`); los
`README.md` tampoco se renderizan. `quarto inspect .` lista las entradas exactas.

**URL antiguas.** Las sesiones migradas de `talk/` y `teching/` a `cursos/` conservan su URL por
`aliases:` en el frontmatter: Quarto genera páginas de redirección dentro de `_site/`. No hay `_redirects`
de Netlify; el plan de rediseño lo contemplaba (`historial/course-redesign-plan.md` §7) y no se aplicó.

**Residuos.** `CNAME` (`kapitan.net`) y `.nojekyll` son de la época de GitHub Pages; Netlify no los lee.
`.github/` solo tiene `FUNDING.yml` y una plantilla de issue: no hay GitHub Actions.

**Submódulos.** `.gitmodules` registra los 11 blogs con URL **https** y `shallow = true` para que un clon
anónimo (Netlify incluido) pueda traerlos. Si Netlify construyera el hub desde git, inicializaría los 11
submódulos en cada build; si el tiempo creciera, `git config -f .gitmodules submodule.<ruta>.update none`
evita que los descargue en CI (localmente se fuerzan con `git submodule update --init --checkout`).
Como el hub no renderiza `_pubs/` (empieza por `_`), los submódulos no aportan nada al sitio del hub.

**Lo que hay que confirmar en el panel** (sitio `6d1408cc-…`):

1. ~~Si el sitio está además enlazado al repositorio de GitHub con un comando de build.~~ Confirmado el
   2026-09-21 por el incidente: está enlazado, con directorio `_site` y sin build (el push sin `_site/`
   publicó un sitio vacío, no un build fallido). Queda por mirar en el panel el *deploy log* de ese push,
   solo para documentar cómo trata Netlify un directorio de publicación ausente.
2. Si hay un dominio propio configurado (el `CNAME` sugiere que lo hubo en GitHub Pages).

### Incidente 2026-09-21: el hub caído con un deploy vacío

**Síntoma.** Todas las rutas de <https://achalmaedison.netlify.app> respondían `404` con la página genérica
de Netlify («Page not found», en inglés), no con la `404.html` del sitio. Los 11 blogs seguían en pie.

**Causa.** DOC2 (`e1ee589`, 2026-09-20 15:35) sacó `_site/` de git en el hub «por higiene» (NORMATIVA
§5, §15.8): borró sus 333 archivos y añadió `/_site/` al `.gitignore`, pasando por alto que el `.gitignore`
original tenía `#_site/` comentado a propósito. El push siguiente llegó a Netlify sin directorio de
publicación y Netlify publicó un deploy **vacío** (no un build fallido, que habría conservado el deploy
anterior). La guía de despliegue, escrita horas después en DOC5, dedujo de `_publish.yml` que el hub se
publicaba con `quarto publish netlify` y consolidó el error.

**Cómo se acotó.** Netlify tiene dos 404 distintos: «Not Found – Request ID: …» (50 bytes) cuando el
subdominio no pertenece a ningún sitio, y «Page not found» cuando el sitio existe pero el deploy publicado
no contiene ese archivo. Sondear rutas que solo existen en las fuentes (`_quarto.yml`, `README.md`), solo
en la salida (`CHANGELOG.html`) y en ambas (`assets/css/global.css`), y obtener `404` en todas, demostró
que el deploy publicado no contenía **ningún** archivo. La pista decisiva fue el historial: `git log --
_site` mostraba commits «render: `_site` actualizado» hasta DOC2 (`git ls-files` en HEAD, que fue lo
primero que se miró, ya no decía nada). Lección de método: ante un artefacto ausente, preguntar al
historial si alguna vez estuvo, no solo al árbol actual.

**Remedio.** Restaurar `_site/` en git con el render local verificado (las 82 entradas de `quarto inspect
.` con su HTML, las redirecciones de `aliases:` en `talk/` y `teching/` —páginas de redirección por
JavaScript, no `meta refresh`—, 60 PDF/DOCX, sin enlaces simbólicos; frente al `_site` anterior a DOC2
solo faltan `SECURITY.html`, `CODE_OF_CONDUCT.html` y `docs/*.html`, excluidos en DOC5, y se añade
`CHANGELOG.html`). Al volver a añadirlo, la regla general `*_files/` del `.gitignore` dejaba fuera 14
figuras de dos posts (`_site/**/index_files/figure-html/*.png`): antes no actuaba porque ya estaban
rastreadas. Se re-incluyen con `!/_site/**/*_files/` en vez de forzarlas con `git add -f`, para que una
figura nueva de un render futuro no quede fuera en silencio. Commit y push: Netlify publica el `_site`.

**Verificación.** `curl -sS -o /dev/null -w "%{http_code}\n" https://achalmaedison.netlify.app/` → `200`;
después `/blog/`, `/cursos/`, una URL antigua (`/talk/2025-01-07-sesion-01-monografia-e-informe/`) y una
figura (`/blog/posts/2022-04-22-economia-agraria/index_files/figure-html/figura1.png`).

**Consecuencias.** `_site/` queda en git en los 12 sitios hasta que D1 se decida (`decisiones.md`); D08 del
doctor avisará en el hub por ello. `quarto publish netlify` sigue siendo una vía alternativa al mismo
sitio, pero sin cuenta y sin terminal interactiva (`--no-prompt`, stdin cerrado) **sale con código 0 sin
publicar nada ni avisar**: un script no puede fiarse de su código de salida.

**Residuo observado, no causa.** `resources: assets/css/pages/listing.css` en `_quarto.yml` casa también
con las copias de cada blog y deja 22 archivos en `_site/_pubs/` (444 KB); ya estaban en el `_site`
versionado antes de DOC2. Inocuo, pendiente de acotar.

## Los 11 blogs (`_pubs/pub_*`)

**Lo que dice el repositorio de cada pub.** Ninguno tiene `_publish.yml`, `netlify.toml` ni `_redirects`.
Los 11 tienen `_site/` **versionado** y su historial reciente son commits «render: `_site` actualizado
(fecha)». El `.gitignore` compartido (528 líneas, idéntico en los 11) no excluye `_site/`. El dominio de
cada uno solo consta en su `_quarto.yml` (`site-url`) y, desde DOC5, en `_pubs/pubs.yml`.

**Lo que eso indica.** Todo apunta a que cada sitio Netlify de un blog está enlazado a su repo de GitHub
con **directorio de publicación `_site` y sin comando de build**: el autor renderiza en local, confirma
`_site/` y el `git push` es el despliegue. Es coherente con que los PDF apaquarto necesiten TinyTeX y con
que ningún pub tenga `_publish.yml`.

**Por qué importa (D1).** Si eso se confirma, sacar `_site/` de git en un pub **rompe su publicación**: el
siguiente push dejaría a Netlify sin nada que servir. Sacar `_site/` exige antes elegir una de dos:

| alternativa | qué implica | costo |
|---|---|---|
| **A. `quarto publish netlify` por pub** (como el hub) | desvincular el sitio del repo o dejar el build vacío; correr `quarto publish netlify` en cada pub la primera vez (crea su `_publish.yml`, que se versiona); `_site/` sale de git y del `.gitignore` compartido pasa a excluirlo | uno a uno, 11 veces; el render sigue en local (TinyTeX) |
| **B. build en Netlify** | comando de build que instale Quarto y renderice (`quarto render`); `_freeze/` tendría que viajar en git o la ejecución estar desactivada; los PDF apaquarto necesitarían TinyTeX en la imagen | builds largos; PDF en CI sin garantía |

La recomendación del diagnóstico es A, probada primero en un solo pub, con reversión `git revert` +
`git checkout` del `_site` anterior.

**Lo que hay que confirmar en el panel, por cada blog:** el repo enlazado, la rama (`main`), el comando
de build (se espera vacío) y el directorio de publicación (se espera `_site`). Hasta entonces, D1 queda sin
aplicar y los 11 `_site/` siguen en git.

## Verificación

```bash
quarto inspect . | python3 -c "import json,sys; print(len(json.load(sys.stdin)['files']['input']))"  # entradas del hub
quarto render && ls _site/                          # el sitio completo en local
git ls-files _site | wc -l                          # el hub versiona su _site (329 el 2026-09-21); 0 = el sitio saldrá vacío
git status --short _site | head                     # tras un render: lo que cambia y hay que confirmar antes del push
curl -sS -o /dev/null -w "%{http_code}\n" https://achalmaedison.netlify.app/   # 200 tras el push (Netlify tarda ~1 min)
git -C _pubs/pub_axiomata log --oneline -3          # en un pub: ¿los commits siguen siendo «render: _site actualizado»?
git -C _pubs/pub_axiomata ls-files _site | wc -l    # cuántos archivos de _site versiona ese pub
```

## Consumidores

Los 11 blogs (`_pubs/pub_*`) y `scripts_quarto_studio/backend/script_blogs_manager` (`main.sh publish
<blog> [netlify]`, que envuelve `quarto publish`). El doctor (`meta/doctor/main.sh`) avisa mientras un
sitio Quarto versione `_site/` (D08); los pubs no se validan (el validador no desciende a `_pubs/`) y el hub
avisará hasta que D1 se decida.
