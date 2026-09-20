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
§7): sacar `_site/` de git en los 11 blogs.

## El hub (`04 index` → <https://achalmaedison.netlify.app>)

**Cómo se publica.** Con `quarto publish netlify` desde la raíz del repo. El comando renderiza el sitio
(`_site/`), lo sube a Netlify por su API y anota el destino en `_publish.yml`:

```yaml
- source: project
  netlify:
    - id: 6d1408cc-afc8-4b2d-8706-26c28e536a05
      url: "https://achalmaedison.netlify.app"
```

`_publish.yml` lo escribe `quarto publish` la primera vez y lo lee las siguientes; está versionado para que
el destino no se pregunte de nuevo. `quarto publish netlify --no-render` sube el último `_site/` sin
renderizar; `--no-prompt` no pide confirmación.

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

1. Si el sitio está **además** enlazado al repositorio de GitHub con un comando de build. Si lo está, cada
   `git push` dispararía un build que, sin Quarto ni TinyTeX en la imagen de Netlify, fallaría o
   publicaría un sitio incompleto; lo esperable es que no lo esté y que solo reciba despliegues de
   `quarto publish`.
2. Si hay un dominio propio configurado (el `CNAME` sugiere que lo hubo en GitHub Pages).

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
quarto publish netlify --no-prompt                  # el hub, al sitio de _publish.yml
git -C _pubs/pub_axiomata log --oneline -3          # en un pub: ¿los commits siguen siendo «render: _site actualizado»?
git -C _pubs/pub_axiomata ls-files _site | wc -l    # cuántos archivos de _site versiona ese pub
```

## Consumidores

Los 11 blogs (`_pubs/pub_*`) y `scripts_quarto_studio/backend/script_blogs_manager` (`main.sh publish
<blog> [netlify]`, que envuelve `quarto publish`). El doctor (`meta/doctor/main.sh`) avisa mientras un
sitio Quarto versione `_site/` (D08), con la excepción declarada de los pubs hasta D1.
