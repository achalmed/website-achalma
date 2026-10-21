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

