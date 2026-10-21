---
tipo: doc
forma: explicacion
titulo: "Decisiones de aula"
estado: activo
---
# Decisiones de aula

La arquitectura y las decisiones del autor (A1–A10, B1–B6, C1) viven en `web/docs/plataforma-educativa.md`;
aquí solo lo que es propio del código de este repo.

### §1.1 Nombre y alcance (2026-10-20)

El autor eligió `aula` (B4): un nombre propio del ecosistema, sin relación con la familia Qillqa (Qillqa, Tiqsi,
Unancha), para que la plataforma educativa no se confunda con la de gestión documental. El repo guarda el código de
la vitrina y, después, el de la API del aula; los 12 sitios lo usan como dependencia versionada.

### §1.2 El cuerpo de lecciones y artículos sale del HTML ya renderizado (2026-10-20)

Se lee `web/_pubs/<pub>/_site/<post>/index.html` y se toma `main#quarto-document-content` (opción a del encargo),
no `index.html.md`. Razón: el HTML es lo que hoy ve el lector, con las matemáticas, el código resaltado (clases de
Pandoc), las tablas, las figuras y las notas tal como Quarto las compuso; el `.md` intermedio obligaría a repetir
filtros, citas y extensiones de Quarto. `_aula/src/lib/contenido.mjs` limpia el bloque de título, el apéndice (rescata
las notas al pie y la bibliografía), los `<style>`/`<script>` incrustados y la sección «Publicaciones similares»
que cada pub añade al final; compone las matemáticas con KaTeX en la construcción (sin JS en el navegador); baja
un nivel los encabezados (el `h1` es el título); repara las anclas de los índices escritos a mano al estilo de
GitHub (`#1-conceptos…` → `#conceptos…`, 93 en numerus-scriptum) y convierte en texto los enlaces sin destino.
Los recursos del post (figuras, `index.pdf`, `index.docx`) se copian junto a la página nueva; los enlaces a otro
post publicado se reescriben a su URL nueva.

**Límite.** Depende de que `_site/` esté al día (hoy se versiona, decisión del 2026-09-22); el código que solo
corre en el navegador de Quarto (pestañas de Bootstrap, widgets) no se conserva: las pestañas se muestran una tras
otra. Las lecciones de Python se publican **sin salidas**, porque `web/_pubs/numerus-scriptum/python/_metadata.yml` tiene
`execute.enabled: false`; la vitrina muestra lo que hay y no inventa salidas. En la fase 7, con el perfil
`documentos` y `freeze`, Quarto entregará Markdown con figuras y esta extracción se sustituye por un lector de
ese Markdown (plataforma-educativa §4.6).

### §1.3 Curso ↔ pub y lección ↔ tema (2026-10-20)

Un curso vive en el pub de su **primer** `area` (`docencia/config/areas.yml`); las áreas siguientes lo listan en
su catálogo con «Vive en …» y un enlace a su pub. Una lección publicada es un post del pub con destino `leccion`
en `docencia/contenido/migracion/mapa-lecciones.csv`, sin `draft: true` en su frontmatter y con HTML en `_site/`
(el frontmatter manda sobre la columna `draft` del CSV; hoy coinciden). Si su `tema_id` existe en `curso.yml`,
ocupa ese tema; si no lo tiene, o es un post `revisar` ya publicado, va a «Lecturas complementarias» del curso,
para que nada publicado se pierda. Un tema sin lección aparece «En preparación», sin enlace. El blog son los
posts `blog` publicados. Una edición (`dictado.yml`) pertenece al pub donde vive alguno de sus cursos; una edición
legado sin `cursos:` hereda el pub de otra edición con la misma `web.materia`. Los materiales de cada sesión se
toman de `publicacion/<sesión>/` del dictado o, si no está, de `web/cursos/<materia>/<edición>/<sesión>/`.

### §1.4 Rutas nuevas y cómo se conservan las URL actuales (2026-10-20)

| página | ruta |
|---|---|
| curso | `/cursos/<curso.id>/` |
| lección | `/cursos/<curso.id>/<slug>/` |
| artículo | `/blog/<slug>/` |
| edición | `/ediciones/<dictado.id>/` |

El `slug` es la carpeta del post sin fecha ni número de serie (`2021-06-21-05-iteraciones-con-python` →
`iteraciones-con-python`): no depende del número de tema, que cambiará cuando se reconstruyan los temarios (C1).
Cada build escribe `dist/<pub>/_redirects` (formato de Netlify) con una regla 301 por post publicado,
`/<sección>/<carpeta>/*  /<ruta nueva>/:splat`, que cubre la página, su PDF, su DOCX y sus figuras. Las URL de
`web/cursos/…` del hub se redirigen desde el hub en la fase 7.

### §1.5 Un proyecto, un pub por build (2026-10-20)

`PUB=<carpeta> npm run build` escribe `dist/<pub>/`; `astro.config.mjs` falla si `PUB` no está en
`web/_pubs/pubs.yml`. Las rutas a las fuentes se resuelven como en `core/env.py` (`_aula/src/lib/rutas.mjs`: raíz =
carpeta con `core/env.py`, y `DOCS_ROOT`, `CLASS_DIR`, `INDEX_DIR`, `SIMULADORES_DIR` por entorno). Lo que ninguna
fuente dice aún (acento del pub y nombre visible con tildes) está en `_aula/config/vitrina.yml`, provisional hasta el
`pub.yml` de cada pub (§4.7 del plan). Los tokens de color salen de la paleta del hub: `npm run build` regenera
`_aula/src/styles/paleta.generado.css` desde `web/assets/scss/00-settings/_palette-*.scss` y `tokens.css` les da rol;
los acentos por pub son la única extensión, y viven en `tokens.css`. Sin islas React: el poco JavaScript
(filtros, progreso, lector, autoevaluación) va en `<script>` de cada componente.

### §1.6 Progreso y preferencias en el navegador (2026-10-20)

Sin cuenta, el progreso vive en `localStorage` del visitante: `aula:<pub>:completadas` (`{"curso/slug":
"AAAA-MM-DD"}`), `aula:tema` (`light`/`dark`) y `aula:lectura` (modo lectura). Todo acceso va envuelto en
`try/catch` (`_aula/src/scripts/almacen.js`): en una ventana privada o con el almacenamiento bloqueado la página
funciona igual y no recuerda nada. No sale del navegador; la sincronización entre dispositivos es del aula con
cuenta (fase 6).

### §1.7 Autoevaluación: formato `quiz:` (2026-10-20)

Una lección declara sus preguntas en el frontmatter; el componente `autoevaluacion.astro` las corrige al instante.

```yaml
quiz:
  - tipo: opcion        # opción múltiple
    enunciado: "…"
    opciones: ["…", "…", "…"]
    correcta: 0         # índice desde 0
    explicacion: "…"    # opcional, se muestra al comprobar
  - tipo: vf
    enunciado: "…"
    respuesta: false
  - tipo: numerica
    enunciado: "…"
    respuesta: 3.14
    tolerancia: 0.01    # opcional; acepta coma o punto decimal
    unidad: "%"         # opcional
```

Es práctica: la respuesta viaja en la página. Los exámenes con nota se corrigen en la API (plan §4.5). Ninguna
lección tiene `quiz:` todavía; la página `/demo/autoevaluacion/` (preguntas de muestra sobre el propio
componente) solo existe con `npm run dev` o al construir con `AULA_DEMO=1`, y lo dice en pantalla.

### §1.8 Vive en el hub, con rutas registradas por código (2026-10-20)

El autor no quiere repos sueltos: `aula` pasó a `web/_aula` con su historia. El hub ya era el dueño del tema de los
12 sitios y tiene los pubs como submódulos; la dependencia queda en un solo sentido (los sitios leen el currículo de
`docencia`, nunca al revés). El guion bajo hace que Quarto lo ignore mientras siga construyendo los sitios actuales.
Al entrar en la norma del hub, las rutas dinámicas dejaron las carpetas con corchetes (`src/pages/cursos/[curso]/`):
se registran en `_aula/src/integracion/rutas.mjs` con `injectRoute` desde archivos en kebab-case de `_aula/src/rutas/`,
y los componentes pasaron de PascalCase a kebab-case. Las URL generadas son idénticas (comprobado archivo por archivo).


### §1.9 La API del aula: FastAPI, PostgreSQL y la vitrina que la usa solo si existe (2026-10-20)

La API vive en `_aula/api/` con la misma pila que Qillqa, que el autor ya opera en la laptop (A9): FastAPI, SQLAlchemy 2
asíncrono con asyncpg, PostgreSQL 16 en un `docker compose` propio (base en `127.0.0.1:5442`, API en `127.0.0.1:8040`;
Qillqa usa 5432 y 8000), pydantic-settings y versiones fijadas en `requirements.txt`. No comparte código ni base con
Qillqa: la receta es la misma, los datos no. La vitrina sigue siendo estática: el cliente `_aula/src/scripts/aula-api.js` y la
página «Mi aula» (`_aula/src/rutas/aula-cuenta.astro`, ruta `/aula/`, enlace en la cabecera) solo se generan si el build
recibe `AULA_API_URL`; sin ella el sitio sale idéntico al de antes. Publicar la API con Tailscale Funnel es decisión
del autor; ningún script lo hace.

### §1.10 Sesión sin cookies de terceros (2026-10-20)

Los 12 sitios están en dominios distintos (`*.netlify.app`, sin dominio propio: B2), así que una cookie de la API sería
de terceros y los navegadores la bloquean. El sitio manda `Authorization: Bearer <acceso>`; el acceso es un JWT HS256
de 15 minutos y la renovación, un secreto opaco de 30 días del que la base guarda solo el resumen SHA-256. La
renovación rota en cada uso y, si alguien presenta una ya rotada, se revocan todas las sesiones de la cuenta (señal de
robo). Ambos viven en `localStorage` del sitio (`aula:sesion`), con el mismo `try/catch` que §1.6. CORS: lista blanca
generada desde `web/_pubs/pubs.yml` (`_aula/api/aula/origenes.generado.json`: los 12 orígenes y sus vistas previas de Netlify
`<rama>--<sitio>.netlify.app`) más `localhost` para desarrollo; sin `allow_credentials`. Contraseñas con Argon2id
(argon2-cffi), límite de 5 intentos fallidos por correo en 15 minutos (en memoria: un proceso) y de códigos de clase
equivocados por cuenta. Las tablas se crean al arrancar (`create_all`, como Qillqa) hasta que el modelo se estabilice;
entonces, Alembic.

### §1.11 Dónde viven los datos de estudiantes (2026-10-20)

Nunca en un repo (regla 8). La base, en el volumen de Docker `aula_aula-db`; los archivos de las entregas, en
`AULA_DATOS_DIR` (por omisión `$XDG_DATA_HOME/aula`, permisos 700/600, nombre aleatorio: el nombre original solo está en
la base); los secretos (clave de la base, secreto JWT, destinatario del respaldo), en `$XDG_CONFIG_HOME/aula/aula.env`.
La API se niega a arrancar si `AULA_DATOS_DIR` cae dentro de un repo git y `respaldar.sh` se niega a escribir en uno.
El respaldo cifra con clave pública (age si está instalado, si no gpg) y escribe en `$RESPALDOS_DIR/aula/<fecha>/`
sin pasar nunca por un archivo en claro. Los archivos subidos tienen límite (10 MB, cortado al escribir por trozos y
antes, por `Content-Length`), lista de extensiones permitidas (sin HTML ni SVG) y se sirven siempre como descarga
(`application/octet-stream`, `nosniff`). La API corre sin registro de accesos: no guarda direcciones IP.

### §1.12 Cómo se corrige un examen (2026-10-20)

La clave solo existe en el servidor (plan §4.5): el banco (`Pregunta`) guarda la clave; al empezar un intento se eligen
`preguntas_por_intento` del banco al azar (`random.SystemRandom`) y, si el examen es aleatorio, se barajan preguntas y
opciones; el intento guarda ese orden y la permutación de opciones de cada pregunta. El estudiante recibe solo
enunciado, opciones en su orden y puntos; responde con el índice que vio, y el servidor lo traduce por la permutación.
La numérica acepta coma o punto decimal con tolerancia absoluta. El tiempo lo manda el servidor: `vence_en` = inicio +
minutos (o el cierre del examen, si llega antes); hay 30 s de gracia por la red; pasado eso, el intento se corrige con
lo guardado (`PUT /intentos/{id}/respuestas`) y queda «vencido». La clave se le muestra al estudiante solo si el
docente lo pidió (`revelar_claves`) y el examen ya cerró. Las pruebas recorren cada respuesta buscando campos de
clave (`_aula/api/tests/test_examenes.py`). Las autoevaluaciones de práctica siguen en el navegador (§1.7).

### §1.13 Pruebas en SQLite y en PostgreSQL (2026-10-20)

El modelo usa solo tipos portables (JSON genérico, un `FechaUTC` que guarda instantes en UTC en los dos motores y
claves foráneas activadas en SQLite), así que la misma suite corre en SQLite en memoria (por omisión: rápida, sin
Docker, la que se corre en cada cambio) y en el PostgreSQL 16 del compose con `AULA_PRUEBAS_DATABASE_URL` (la base
`aula_prueba` se crea si falta), que es la prueba de verdad antes de un commit que toque el modelo. Las dos dieron
58 de 58 el 2026-10-20. Ninguna prueba usa datos reales: correos `@ejemplo.test` y nombres inventados.

### §1.14 Privacidad: consentimiento, exportación y baja (2026-10-20)

El registro exige `consentimiento: true` y la versión vigente de la política (`_aula/api/docs/privacidad.md`); la cuenta
guarda versión y fecha. `GET /cuentas/yo/datos` exporta todo lo de la persona; `DELETE /cuentas/yo` (con la
contraseña) lo borra, archivos incluidos; lo que un docente dejó en clases ajenas queda sin su nombre, y el único
docente de una clase con estudiantes no puede borrarse sin antes sumar otro o retirarlos (borraría datos ajenos). El
estudiante ve solo a los docentes de su clase, sin correos; quien no es miembro recibe 404 en vez de 403, para no
confirmar que una clase, entrega o intento existe. Conservación: 730 días sin actividad (`python -m aula.cli depurar`).

### §1.15 El cambio de un pub: `_vitrina/` y una línea de `netlify.toml` (2026-10-20)

Netlify publica lo que está en git, sin compilar (decisión del autor del 2026-09-22). El `_site/` de Quarto no se
reemplaza porque es la fuente de las lecciones (§1.2): la vitrina se copia a `web/_pubs/<pub>/_vitrina/` y el cambio
es la línea `publish` del `netlify.toml` del pub, de `"_site"` a `"_vitrina"`; volver atrás es devolverla
(`_aula/scripts/publicar.sh <pub> --volver --aplicar`). Antes de copiar, `_aula/scripts/rutas.mjs` exige que cada
página, PDF y DOCX que el sitio viejo publicaba siga en la vitrina o redirija (301) a un archivo que exista; por eso
las figuras en PDF que Quarto deja junto a cada post (carpeta figure-pdf de sus recursos) viajan con él. Se cambia un pub a la vez: rama,
*pull request* con vista previa de Netlify, revisión y merge a `main`.


### §1.16 Se queda «Quiet Laboratory»; se mejoran íconos, búsqueda y cifras (2026-10-20)

El autor probó una estética de macOS (grafito, vidrio, Inter, íconos de aplicación) y la descartó el mismo día: «parece
una copia barata». Rige la identidad que ya estaba en producción en methodica: papel cálido, tinta azulada, serif
académica para títulos y lectura, sans para la interfaz, monoespaciada para datos y la retícula milimetrada en la
portada. El intento se deshizo con un solo commit de reversión y sobre ese estilo se rehizo solo lo que mejora la
experiencia sin imitar a nadie, dibujado con filetes finos y papel (sin vidrio, sin sombras flotantes nuevas):

- **Íconos:** un único juego de línea, Lucide (`lucide-static`, versión exacta), en línea desde `_aula/src/lib/iconos.mjs`
  con trazo 1,5, en lugar de los SVG y glifos sueltos (tema, flechas, copiar, fecha, descargas, teclas).
- **Búsqueda ⌘K / Ctrl K / «/»** (`_aula/src/components/paleta-comandos.astro`): cursos, lecciones, artículos y
  ediciones, con el patrón ARIA de combobox; aspecto de ficha de papel con filete y la franja del acento arriba. Su
  índice (`/buscar.json`, `_aula/src/pages/buscar.json.js`) se pide solo al abrirla.
- **Bloques de código** con una cabecera discreta (lenguaje y copiar) que escribe el build (`_aula/src/lib/contenido.mjs`).
- **Banda de cifras** de la portada (`_aula/src/components/cifras.astro`): solo cifras del modelo, números en Petrona y
  rótulos en monoespaciada, entre dos filetes como la cabecera de una tabla; suben una vez al entrar en pantalla.
- **Tarjetas** de artículos, lecturas complementarias y ediciones con filete y sin sombra; el pie «La familia» lista
  los 12 sitios con su colofón y su área, desde `pubs.yml`, `areas.yml` y `_aula/config/vitrina.yml`.
- **Lectura:** tablas de tres filetes en un contenedor que se desplaza solo él, figuras con carga diferida y pegadas a
  su código, guiones a 375 px.

### §1.17 Las tarjetas muestran la imagen propia del post o su índice (2026-10-20)

Los posts declaran `image:`, pero casi todos apuntan a la misma foto genérica de la serie (el `featured.jpg` de la
carpeta superior, una sola imagen en 38 carpetas): repetida en cada tarjeta no distingue nada.
`_aula/src/lib/imagenes.mjs` usa la imagen propia del post solo si ningún otro post del pub la comparte (por huella del
contenido); si no, la primera figura del cuerpo con tamaño y proporción de tarjeta; si tampoco hay, la tarjeta muestra
el índice del texto (sus primeras secciones) sobre la retícula, con el colofón del pub. La miniatura sale a 640 × 400
en WebP con `sharp`, con `width`, `height`, `loading="lazy"`, `decoding="async"` y `alt` vacío, porque el título
enlazado ya dice qué es.

### §1.18 El colofón: la marca de los 12 sitios (2026-10-20)

Cada sitio firma con un colofón al modo de una editorial universitaria: su monograma en Petrona (Me, Ns, Eb, Ae, Op,
Ax, Pf, Am, Rp, Dm, Ch y EA para el hub) dentro de un cuadrado de doble filete, en el acento del sitio, con el nombre
en Petrona y «por Edison Achalma» al lado. Las letras al estilo de la tabla periódica evitan el choque de iniciales
(tres pubs empiezan por A); el sello cuadrado de filete no se confunde con Qillqa, cuya marca es una pluma en un
squircle oscuro. Hay dos variantes del mismo signo: de filete (cabecera, pie, familia, tarjetas) y lleno, con el
cuadrado en el acento (favicon e ícono de pantalla de inicio, donde un filete fino no se vería). `_aula/scripts/marca.py`
convierte monogramas y textos en trazos (`_aula/src/lib/marca.generado.mjs`) y `_aula/src/integracion/recursos.mjs`
escribe en cada build el favicon (SVG y PNG 32), el `apple-touch-icon` (180) y la imagen Open Graph (1200 × 630, papel
con retícula, colofón, nombre, área y firma), sin depender de las fuentes instaladas.

### §1.19 Rendimiento: menos fuente y CSS en línea (2026-10-20)

La primera medición del estilo de producción dio 83–88 en móvil: la hoja de estilos bloqueaba la primera pintura y se
bajaban 360 KB de fuentes, entre ellos Source Serif con eje óptico (122 KB) y su cursiva (127 KB) en todas las
páginas. Ahora Source Serif carga solo su eje de peso (51 KB), la cursiva solo en el lector (donde hay texto en
cursiva), la firma de la cabecera va sin cursiva y el CSS va en línea (`inlineStylesheets: 'always'` en
`_aula/astro.config.mjs`). Con eso methodica marca 96–98 en móvil y 100 en accesibilidad, buenas prácticas y SEO.

### §1.20 El laboratorio en el navegador: el mismo `base.Modelo` en Pyodide (2026-10-21)

Fase 3 del plan (`web/docs/plataforma-educativa.md` §4.8). El navegador ejecuta el MISMO código Python que el
laboratorio de escritorio, sin reescribir una sola ecuación en JavaScript:

- **Contrato.** `simuladores/main.py web --aplicar` escribe `simuladores/navegador.json`: por cada modelo que corre en el
  navegador, los `.py` mínimos (`base.py`, el adaptador `navegador.py`, el `config.py` de la disciplina, los `__init__.py`
  y el módulo con sus auxiliares, por análisis estático de sus `import`), sus parámetros con rango y paso, escenarios,
  ficha y una vista inicial (las curvas con los valores por defecto, 300 puntos por línea). Los que importan algo más que
  numpy y la biblioteca estándar sin archivos (el nivel 12 de macro lee datafw) o tardan más de 0,3 s de CPU quedan
  fuera, con su motivo, y el curso los lista como «solo en el escritorio».
- **Asociación.** Un modelo tiene página en un pub si un curso que vive en ese pub lo asocia a un tema, por
  `catalogo.json` (los `temario.yml` de simuladores) o por un recurso `{tipo: simulador}` de su `curso.yml`
  (`_aula/src/lib/modelo.mjs`). Hoy: aequilibria 22, epsilon-y-beta 18 y optimums 1.
- **Página `/laboratorio/<id>/`** (`_aula/src/rutas/laboratorio-modelo.astro`) e índice `/laboratorio/`: deslizadores
  nativos con `<label>`, `aria-valuetext` y la definición como descripción; escenarios con su lectura y su cadena de
  transmisión; «Restablecer»; tabla de resultados; ficha (contexto, supuestos, ecuaciones, intuición, limitaciones,
  procedencia y fuentes) y enlace a los `.py`, que el build copia a `/laboratorio/py/` (solo los de los modelos del pub).
- **Gráfico.** `_aula/src/lib/grafico-lab.mjs` dibuja en SVG el contrato de `Modelo.curvas` (líneas, barras, puntos,
  equilibrio, anotación) con la paleta del laboratorio traducida a roles (`--graf-1`, `--graf-2`, `--graf-3`,
  `--graf-eq`, `--graf-aux` en `_aula/src/styles/tokens.css`, claro y oscuro), retícula de filetes, auxiliares
  discontinuas y la notación `$…$` en cursiva con índices. El mismo módulo pinta la figura del build (visible sin
  JavaScript) y cada recálculo, así que ambas son idénticas.
- **Pyodide 0.29.5** (Python 3.13, numpy 2.2; versión exacta, `cdn.jsdelivr.net`) corre en un Web Worker
  (`_aula/src/scripts/laboratorio-trabajador.js`): la página no se congela mientras Python arranca. Se pide solo en esta
  página, tras el evento `load` y en un momento ocioso (con plazo de 1,5 s, porque en una pestaña de fondo
  `requestIdleCallback` puede no llegar). Sus mensajes de carga no van a la consola. Si no carga (sin red, sin
  trabajadores) la página lo dice y conserva la figura por defecto; sin JavaScript, igual (`<noscript>`).
- **Las ecuaciones de la ficha van en MathML nativo** (KaTeX con `output: 'mathml'`), sin la hoja ni las fuentes de
  KaTeX: en HTML, la flecha extensible de `\xrightarrow` es un SVG de 400em que un móvil tarda segundos en pintar
  (Lighthouse: 77 con KaTeX en HTML, 97 sin él).

Medido el 2026-10-21 en la laptop, servido en local: primera carga del motor 7,2 s con la caché vacía (unos 12 MB:
Pyodide, numpy y los `.py`) y 2,3–2,9 s con la caché del navegador; cada recálculo de IS-LM, 5–10 ms, y del TCL
(4 000 muestras), 25–65 ms. Los 22 modelos de aequilibria, los 18 de epsilon-y-beta y el de optimums cargan y calculan
su valor por defecto y cada escenario en el navegador (prueba en la propia página con el trabajador del build).
Lighthouse móvil: `/laboratorio/e67/` y `/laboratorio/m10/` dan 97 de rendimiento y 100 en accesibilidad, buenas
prácticas y SEO; Lighthouse no espera a Pyodide, que va en otro hilo y después de la carga. Capturas:
`_aula/docs/img/laboratorio-islm-375-claro.webp`, `_aula/docs/img/laboratorio-tcl-375-oscuro.webp` y
`_aula/docs/img/laboratorio-tcl-escritorio-claro.webp`.

### §1.21 Los vídeos de divulgacion en la lección de su tema (2026-10-21)

Fase 8 del plan. La vitrina lee `divulgacion/catalogo.json` (`DIVULGACION_DIR`, o `<raíz>/divulgacion`; contrato:
piezas con `curriculo: [{curso, tema}]` y `publicaciones: [{red, fecha, url}]`) y, en la lección del tema, muestra
«En vídeo» solo con las piezas que tienen al menos una publicación con url `https` (`_aula/src/lib/videos.mjs`).
YouTube va primero y se incrusta con `youtube-nocookie.com` detrás de una fachada: nada se pide a YouTube hasta que el
lector pulsa, y sin JavaScript queda un enlace al vídeo. TikTok, Facebook y las demás redes son enlaces simples. Hoy
ninguna pieza está publicada, así que la sección no aparece en ningún pub; el componente se prueba con datos de
muestra en `_aula/scripts/prueba-videos.mjs` (`npm run prueba`) y en la página interna `/demo/videos/`, que solo
existe con `astro dev` o `AULA_DEMO=1` (captura: `_aula/docs/img/videos-demo.webp`).

### §1.22 Pauta editorial de lectura (2026-10-21)

El autor pidió que leer una lección o un artículo en el celular sea tan limpio como una buena app de lectura y que
transmita rigor: sin distracciones, una o dos tintas como máximo, como una revista académica. Decisiones (autor):
**tinta sobre papel y un solo acento por pub**, solo para enlaces y lo que importa (el número de sección pasa a gris);
**serif de lectura** con sans para tablas, pies y código, a 17 px en el celular y 18 px desde 720 px. En
`src/styles/contenido.css` y `src/layouts/lector.astro`:

- **Tablas** de tres filetes, sin rayas interiores, cifras tabulares, 13 px en el celular; `contenido.mjs` quita los
  anchos fijos de Pandoc (`colgroup`) y el contenedor muestra una sombra en el borde por donde la tabla sigue. Las
  ecuaciones anchas usan el mismo aviso.
- **Pies de figura y tabla al estilo APA 7**: `contenido.mjs` separa el rótulo («Tabla 1») del título; el rótulo va en
  negrita en su línea y el título en cursiva, en sans de 14 px con su propio interlineado.
- **Código** en la tarjeta oscura de la demo de Qillqa (`--tc-*` en `tokens.css`, igual en claro y oscuro): pastilla con
  el lenguaje, botón «Copiar» en píldora, resaltado casi monocromo. La muestra de código de la portada del curso usa la
  misma tarjeta.
- **Índice de la página** sin filete vertical: la sección en curso va en tinta con un punto del acento; las barras de
  desplazamiento de las dos columnas laterales no se ven en reposo.
- **Referencias y notas** separadas por un filete, más pequeñas, con sangría francesa y los enlaces largos partidos.
- **Avisos** en papel teñido, sin colores de semáforo.

