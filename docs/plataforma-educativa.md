---
tipo: doc
titulo: "Plataforma educativa: diagnóstico y arquitectura objetivo (los 11 pubs como aulas)"
estado: borrador
forma: explicacion
creado: 2026-10-20
---
# Plataforma educativa: diagnóstico y arquitectura objetivo

> Encargo del autor (2026-10-20): convertir la web en un ecosistema educativo (cursos completos, blogs, materiales
> docentes, simuladores) con identidad propia, tomando principios del sitio de demostración de Qillqa sin confundirse con
> él, y decidir qué se hace con Quarto. **Versión 2**, con las decisiones que el autor tomó el mismo día (§0). No se ha movido ni
> renombrado nada. Las cifras se midieron el 2026-10-20 en solo lectura.

## 0. Decisiones del autor (2026-10-20)

| id | decisión |
|---|---|
| A1 | **Los 11 sitios Netlify de los pubs se quedan.** Se crean más solo si hace falta (§5 propone uno). |
| A2 | **Cada pub se convierte en una plataforma de cursos** con las funciones de Google Classroom, Moodle y los MOOC. **No se usa Google Classroom**: la plataforma es propia. |
| A3 | **`docencia` es la fuente única del currículo.** Los pubs, con sus sesiones en borrador o ya desarrolladas, se adaptan a él. |
| A4 | **`web/cursos` desaparece.** Su función pasa a los pubs. |
| A5 | **Los esqueletos se conservan.** Se aprovechan sus metadatos para ordenar los cursos y quedan listos para llenarse. |
| A6 | **`simuladores` será un proyecto independiente**, igual que `divulgacion`. Depende del currículo y de `datafw` y da soporte a `docencia`, `divulgacion` y los pubs. |
| A7 | **El render de 47 min es un problema** y se resuelve. |
| A8 | **Las duplicaciones se eliminan.** Es el objetivo central del proyecto. |
| A9 | **Lo que necesita servidor corre en esta laptop**, como Qillqa: Docker y Tailscale Funnel (enlace fijo y gratuito, `qillqa/enlace.sh`). Cierra B1. |
| A10 | **Los `.tex` de los exámenes se conservan en `docencia`**; los pubs muestran solo sus PDF. |

## 1. Resumen

1. El contenido docente se escribe hoy en tres lugares (`docencia`, los 11 pubs, `web/cursos`) y se publica en 12 sitios. Con A1–A4, la
   regla pasa a ser **una casa por cada pieza**:
   - el currículo vive en `docencia`;
   - la lección, en su pub;
   - el examen fuente y su clave, en `docencia` (repo privado);
   - el simulador, en `simuladores`.

   Todo lo demás lee esas fuentes o recibe artefactos generados.
2. **La estructura de cada curso en su pub se genera desde `curso.yml`**: unidades, temas, sílabo y esqueletos. El autor solo escribe el
   cuerpo de la lección. Si cambia el currículo, el generador ajusta la estructura sin tocar lo escrito. Así manda el currículo (A3)
   sin duplicarlo.
3. **Cada pub se construye en dos capas.** La vitrina pública (catálogo, cursos, lecciones, simuladores, autoevaluaciones) es **estática**:
   carga rápido, la indexa Google y no necesita servidor. El aula con cuenta (inscripción, tareas, entregas, notas, anuncios)
   es una **API compartida por los 11 pubs**, con la misma tecnología que Qillqa: FastAPI y PostgreSQL.
4. **Quarto deja de construir los sitios** y queda como compilador de documentos (PDF, DOCX, lecciones con código, diapositivas
   reveal.js), junto con LuaLaTeX para los exámenes y los decks Beamer. El sitio se construye con Astro en segundos. Los 47 min actuales se deben
   sobre todo a que **cada post compila su PDF y su DOCX en cada render**.
5. **Áreas y pubs casan 11 a 11 con ajustes** (§5): normalizar el vocabulario de `area`, mover 5 cursos de área y darle a `chaska` un área
   propia. Además se propone un **12.º sitio para preuniversitario y nivelación**, porque su público es otro.

## 2. Diagnóstico

La foto del 2026-10-20 (la web, los 11 pubs, `docencia`, las duplicaciones, `simuladores`, `divulgacion`, los marcos LaTeX y el
costo del render) está en [historial/diagnostico-plataforma-2026-10-20.md](historial/diagnostico-plataforma-2026-10-20.md).
Lo que de ella decide el diseño está en §1 y en las tablas de §4.

## 3. Identidad: qué se toma del demo de Qillqa

El sitio `qillqa/demo/vendor/sitio` funciona por cinco principios:

1. **Mostrar en vez de describir:** el oficio avanza de estado, el tablero se arrastra.
2. **Un solo acento.**
3. **Superficies translúcidas.**
4. **Movimiento con freno:** respeta `prefers-reduced-motion` y se detiene en cuanto el usuario toca algo.
5. **Primero 375 px**, accesible y con modo claro y oscuro.

**Se adoptan los cinco principios. No se adoptan** su tipografía de sistema estilo Apple, sus grises `#f5f5f7` y `#1d1d1f` ni su estética de ventanas y
docks.

Identidad propia: **«Laboratorio abierto»**, una evolución de Quiet Laboratory:

- papel cálido, tinta azulada, azul de revista y verde de laboratorio;
- **un acento por pub** dentro de la misma paleta;
- serif académica para leer, sans para la interfaz y monoespaciada para datos y fórmulas;
- motivo gráfico de retícula milimetrada, ecuaciones y curvas, que emparenta con «Laboratorio en movimiento», la identidad de `divulgacion`.

Cada pub conserva su nombre y su color. Todos comparten el mismo esqueleto, así que se reconocen como una sola institución. El equivalente al recorrido de Qillqa es un
**simulador vivo** en la portada de cada pub (IS-LM en aequilibria, oferta y demanda en optimums, el TCL en epsilon-y-beta) y una
«lección en curso» de muestra.

## 4. Arquitectura objetivo

### 4.1 Una casa por pieza

```
PROYECTO              QUÉ ES SU CASA (fuente única)                    QUÉ PUBLICA O DA A OTROS
────────────────────  ──────────────────────────────────────────────  ─────────────────────────────────────
docencia              currículo (curso.yml, rutas.yml), dictados,      la estructura de cada curso (generada
 (taller del docente)  marcos LaTeX (classes, themes, templates),      en su pub), PDF compilados (decks,
                       fuentes .tex de evaluaciones y claves           prácticas, exámenes liberados)
                       (privado), registro (sensible)
11 pubs (+1)          el TEXTO de lecciones y artículos, páginas de    los sitios: vitrina pública + aula
 (las aulas)           cada edición, blog del área, acento visual
web/_aula             el CÓDIGO de la plataforma: componentes Astro,   un paquete versionado que los 12 sitios
 (la plataforma)       esquemas del contenido, generadores, y la API   usan; la API compartida (cuentas,
                       del aula (FastAPI + PostgreSQL)                 tareas, notas)
simuladores           modelos numpy, fichas con fuentes, adaptador     simuladores en el navegador; modelos a
 (repo propio)         web                                             docencia y divulgacion
divulgacion           piezas de vídeo                                  catalogo.json → vídeo en la lección
datafw                datos y observatorio                             datasets por curso; observatorio
web (hub)             perfil, publicaciones, observatorio, catálogo    la puerta de entrada; /cursos/* → 301
                       general de los 12 sitios (generado)             al pub que corresponda
```

**Regla.** Un archivo tiene una sola casa. Fuera de ella solo se **lee** o se recibe una **copia generada** marcada `GENERADO …; no editar`
(N 7.2, 7.7). Si algo aparece escrito a mano en dos casas, es un error que el doctor detecta.

### 4.2 Qué queda en `docencia` y qué se va

| se queda en `docencia` | pasa a los pubs | pasa a `simuladores` | desaparece |
|---|---|---|---|
| `curso.yml` (currículo), `rutas.yml` nuevo, `dictado.yml` | el texto de las lecciones (las notas de `02-contenido` y lo escrito en los posts) | `simuladores/` con su historia | `web/cursos` (su contenido va a methodica y al 12.º sitio) |
| marcos LaTeX: `classes/`, `themes/`, `templates/`, `scaffolds/` | las páginas de cada edición (hoy en `web/cursos/<materia>/<edicion>`) | | `temario.py --que web` y `publicar-web.py` hacia `web` (los sustituye el generador hacia los pubs) |
| fuentes de evaluaciones y claves (`contenido/`, privado); guiones y `deck.tex` | los PDF compilados que el autor libera (decks, prácticas, exámenes ya tomados) | | |
| `registro/` (sensible) | | | |

`docencia` no desaparece: deja de ser un lugar donde se lee y pasa a ser el **taller del docente**. Allí se diseña el curso,
se escriben y compilan las evaluaciones y se guarda lo privado. Lo que el estudiante ve vive en los pubs.

### 4.3 Cómo manda el currículo sin duplicarse

1. **Estructura generada.** `aula generar <pub>` lee los `curso.yml` del área del pub y escribe, en el pub, la estructura de cada curso:
   `cursos/<curso>/index.md` (portada y sílabo), `cursos/<curso>/<NN-unidad>/<NN-tema>/index.qmd` (una lección por tema) y las páginas de
   cada edición desde `dictado.yml`. El frontmatter va entre marcas (`<!-- curriculo:inicio … fin -->`) y lo reescribe el generador.
   **El cuerpo es del autor y el generador nunca lo toca.**
2. **Esqueleto de la lección.** Las secciones vacías y listas para llenar son Objetivos, Desarrollo, Ejemplos, Ejercicios, Autoevaluación y Recursos, con
   indicaciones de lo que va en cada una.
3. **Esqueletos actuales (A5).** Los unos 130 posts en borrador se emparejan con su tema por `curso:`, la numeración y el título. Su metadato (fecha,
   categorías, título) pasa a la lección, y la URL publicada, si existe, queda como redirección. Los temas del pub que no están en `curso.yml`
   (control sintético, bayesiana, VBA, Power Query…) se proponen como altas en el currículo; no se pierden.
4. **Verificación.** El doctor comprueba que cada tema tenga exactamente una lección y que ninguna lección quede sin tema.

### 4.4 La vitrina estática y el aula con cuenta

**Qué significa «estático».** El servidor entrega archivos ya construidos (HTML, CSS, JS, PDF) sin calcular nada por cada visita. Es lo que hace hoy
Netlify con los 12 sitios. Una página estática **puede ser muy interactiva**, porque la interactividad corre en el navegador del visitante:

- simuladores con deslizadores;
- autoevaluaciones que se corrigen solas;
- progreso, marcadores y notas guardados en ese navegador;
- búsqueda instantánea;
- vídeo y descargas.

Lo que no puede hacer sola es **guardar algo que otra persona deba ver**: la tarea que entrega un alumno, la nota que pone el docente, el anuncio a un grupo.
Para eso hace falta un servidor con base de datos.

Es la arquitectura de Platzi o de los MOOC: catálogo y lecciones rápidos y públicos, más un área con cuenta.

| capa | tecnología | qué hace |
|---|---|---|
| Vitrina (12 sitios) | **Astro**: generador de sitios estáticos. Toma Markdown, `.qmd` ya compilados y YAML, y produce HTML. Las «islas» de React añaden interactividad solo donde hace falta | catálogo, cursos, lecciones, autoevaluaciones, simuladores, descargas, búsqueda (Pagefind) |
| Aula (una API para los 12) | **FastAPI + PostgreSQL**, como Qillqa (`qillqa/backend`), en Docker | cuentas, inscripción con código, tareas y entregas, calificaciones, anuncios, foros, certificados |
| Panel del docente | islas React dentro del mismo sitio, con MUI o los componentes propios, como el frontend de Qillqa | crear tareas, calificar con rúbrica, ver el libro de notas |

**Respuesta a «¿usamos la tecnología de Qillqa?».** En el aula, sí: es la misma pila (FastAPI, PostgreSQL, React) que el autor ya opera.
En la vitrina, no: Qillqa es una aplicación detrás de un login, mientras que un curso público debe cargar al instante, verse en el celular e
indexarse en Google, y eso lo da un sitio estático.

**Respuesta a «¿Astro es como Quarto?».** Sí, en lo esencial: ambos convierten archivos de texto en un sitio estático. La diferencia es que Quarto está pensado para
documentos (artículos, libros, informes) y Astro para sitios con componentes (un lector de cursos, un catálogo con filtros, un panel). Por eso
Quarto se queda para los documentos y Astro construye los sitios.

### 4.5 Funciones: Classroom, Moodle y MOOC

| función | inspirada en | capa |
|---|---|---|
| Catálogo por área con filtros (tipo, nivel, estado), rutas de aprendizaje, búsqueda de texto completo | Platzi, MOOC | vitrina |
| Portada del curso: objetivos, requisitos, duración, nivel, unidades, docente, bibliografía (Calibre y Zotero) | MOOC | vitrina |
| Lector de lección: índice de la unidad, anterior y siguiente, tiempo de lectura, matemáticas, código, figuras, modo lectura, impresión y PDF | Platzi | vitrina |
| Vídeo de la lección con capítulos; vídeo de `divulgacion` por tema | Platzi | vitrina |
| Materiales descargables por lección y por edición (decks, prácticas, datos, cuadernos) | Classroom | vitrina |
| Autoevaluación con corrección inmediata (opción múltiple, numérica, verdadero o falso, emparejar) | MOOC, H5P | vitrina |
| Ejercicios con pista y solución desplegable; banco de problemas por tema | Moodle | vitrina |
| Simulador integrado y «laboratorio» del curso | propio | vitrina |
| Glosario del curso y fórmulas clave | Moodle | vitrina |
| Progreso, marcadores y notas personales sin cuenta (en el navegador) | Platzi | vitrina |
| Ediciones o dictados con calendario de sesiones | Classroom | vitrina |
| Blog del área y del curso | propio | vitrina |
| Cuenta, perfil, inscripción a una clase con código o enlace | Classroom | aula |
| Tablón de anuncios por clase y avisos por correo y push | Classroom | aula |
| Tareas con fecha, entrega de archivos, devolución con nota y comentarios | Classroom | aula |
| Rúbricas (las de `docencia/templates/report/rubrica`) | Classroom, Moodle | aula |
| **Exámenes calificados en el servidor**, con tiempo y preguntas aleatorias de un banco | Moodle | aula |
| Libro de calificaciones, exportación a Excel, ponderaciones | Classroom, Moodle | aula |
| Progreso sincronizado entre dispositivos | Platzi | aula |
| Foro por lección y por clase, con moderación | Moodle, MOOC | aula |
| Liberación condicional (se abre la unidad 3 al aprobar la 2) | Moodle | aula |
| Certificado verificable por enlace | Platzi, MOOC | aula |
| Roles: docente, co-docente, estudiante, invitado | Classroom | aula |
| Estadísticas del curso para el docente | Moodle | aula |

Dos reglas que se desprenden de esta tabla:

- **Las respuestas de un examen calificado no pueden viajar al navegador.** En una página estática el alumno podría leerlas. Por eso los
  exámenes con nota se corrigen en la API; las autoevaluaciones de práctica sí se corrigen en el navegador.
- **El aula guarda datos personales de estudiantes.** Eso exige tres cosas:
  - entra en `sensibles:` de `workspace.yml` como `registro_docente`;
  - tiene política de privacidad y consentimiento conforme a la Ley 29733 de protección de datos personales y su reglamento;
  - tiene respaldo cifrado, y sus datos nunca entran en un repo (regla 8).

### 4.6 Quarto, LuaLaTeX y el render rápido

| producto | herramienta | cuándo corre |
|---|---|---|
| Los 12 sitios | Astro | en cada publicación; segundos por sitio |
| Lección o artículo en prosa | Markdown con KaTeX y citas APA (CSL, BibTeX de Better BibTeX), leído por Astro | ídem |
| Lección o artículo con código (17 hoy) | **Quarto** → Markdown con figuras, con `freeze` | solo si cambió su fuente |
| PDF y DOCX APA de lecciones y artículos | **Quarto/apaquarto**, perfil `documentos` | bajo demanda o en un trabajo nocturno, con caché por hash de la fuente |
| Decks de clase | **Beamer** (`academic`) o **reveal.js** (`deck.qmd`), desde `docencia` | al preparar la sesión |
| Exámenes, prácticas, solucionarios, sílabos, rúbricas | **LuaLaTeX y Biber** con `docencia/classes` | al compilar en `docencia`; al pub solo va el PDF liberado |
| Láminas de ponencias y defensas | **`escritura`** (`lamina.cls`) | sin cambios |

Efecto esperado: publicar un pub pasa de minutos a segundos, porque los PDF ya compilados se reutilizan. El autor sigue escribiendo en `.qmd` y `.tex`.

### 4.7 El código de la plataforma en un solo lugar

Hoy el tema de los 12 sitios se reparte con hardlinks (decisión del 2026-10-08). Con la plataforma, el código vive en **`web/_aula`**
(dentro del hub, que ya era el dueño del tema; el autor no quiere repos sueltos) y construye cada pub leyendo su contenido. Un pub queda reducido a su
contenido, un `pub.yml` (nombre, acento, área, dominio) y su página de inicio. Los hardlinks se retiran al terminar la migración (hasta
entonces se respetan).

### 4.8 `simuladores`

| aspecto | diseño |
|---|---|
| Repo | `simuladores` propio (L3). Sale de `docencia/simuladores` conservando su historia (N 3.13) |
| Depende de | `datafw` (`DATAFW_DIR`), Calibre (`core/py-common/biblioteca.py`) y el currículo: cada modelo declara `curriculo: [{curso, tema}]`, igual que una pieza de `divulgacion` |
| Da a | `docencia` (`recursos: {tipo: simulador, id}`), `divulgacion` (`SIMULADORES_DIR` en `core/env.sh`, con alias temporal a la ruta vieja), los pubs (`catalogo.json` y el paquete web) |
| Web | adaptador que corre el mismo `base.Modelo` en Pyodide (numpy en el navegador) con gráficos en JS; vista ligera con escenarios precalculados en JSON para el celular |
| Escritorio | `python3 main.py` sigue igual |
| No se rompe | `Modelo.curvas/parametros/escenarios/verificaciones/ecuaciones_calibradas/ficha`, que `divulgacion` usa directamente |

## 5. Áreas del currículo y pubs

El vocabulario cerrado de 12 áreas, una por sitio, y el pub de cada una viven en `docencia/config/areas.yml` (fase 1, hecha). El
primer `area` de cada `curso.yml` decide su pub; los demás lo listan también en otros. El reparto vigente lo imprime
`python3 docencia/scripts/areas.py listar`, y `docencia/scripts/validate.sh` rechaza un área fuera del vocabulario. El porqué de
cada traslado (los cursos que cambiaron de área, el área nueva de `chaska`, el 12.º sitio para preuniversitario) está en
`docencia/contenido/migracion/mapa-areas.csv` y en `docencia/docs/decisiones.md`.

## 6. Plan de implementación

Cada fase deja todo funcionando. Los sitios en producción no cambian hasta la fase 7, y cada paso estructural sigue N 3.13 (auditoría,
propuesta, aprobación, `core/renombrar.py` con etiqueta, simulación, respaldo y `UNDO.sh`).

| fase | qué | prueba de salida | ¿producción? |
|---|---|---|---|
| **1. Currículo** (**hecha** 2026-10-20: vocabulario de 12 áreas en `docencia/config/areas.yml`, 29 cursos normalizados, `validate.sh` lo exige, altas de MATLAB y Linux, título de Matemáticas I; las rutas por `core/env.py` ya estaban; los campos nuevos de `curso.yml` y `rutas.yml` pasan a la fase 4, donde los fija el generador que los lee) | vocabulario de 12 áreas; mover los 5 cursos; altas que faltan (Linux, ciberseguridad, Power BI, SQL, temas que solo están en los pubs); esquema de `curso.yml` ampliado (nivel, duración, requisitos, `pub`), `rutas.yml`; scripts de `docencia` a `core/env.py` | cada curso con un área válida y un pub; validador sin empeorar | no |
| **2. Render rápido** (**hecha en el hub y en methodica** 2026-10-20: `scripts/render.sh` solo HTML y `--documentos` con caché `_documentos.tsv`; methodica 184 s → 20 s, epsilon-y-beta 708 s → 43 s; uso y porqué en `decisiones.md` §4.5; falta confirmar los scripts propagados en los otros 10 pubs y registrar sus documentos) | en los 12 sitios Quarto actuales, perfil `html` por defecto y PDF/DOCX en el perfil `documentos` con caché | de unos 47 min a pocos minutos; PDF idénticos byte a byte (`SOURCE_DATE_EPOCH`) | sí, sin cambiar contenido |
| **3. `simuladores`** (**hecha** 2026-10-20: repo propio con 64 commits de historia, `SIMULADORES_DIR`, `main.py catalogo` → `catalogo.json` con 138 modelos, verificaciones idénticas; respaldo y `UNDO.sh` en `$RESPALDOS_DIR/renombres/2026-10-20-docencia-simuladores-a-simuladores/`; alta en `workspace.yml`, remoto y adaptador web pendientes) | repo propio con su historia; `SIMULADORES_DIR`; adaptador web con IS-LM y TCL | `main.py verificar` igual; `divulgacion` renderiza una pieza; el simulador corre a 375 px | no |
| **4. `aula` (vitrina)** (**prototipo hecho** 2026-10-20 en `web/_aula`: methodica y numerus-scriptum en segundos, 0 enlaces rotos, escritorio y 375 px, claro y oscuro; faltan Lighthouse y la vista previa en Netlify) | paquete Astro con la identidad «Laboratorio abierto»; generador `curso.yml` → pub; piloto **methodica** (tiene ediciones reales) | build en segundos; Lighthouse ≥ 90 a 375 px; claro y oscuro; vista previa en Netlify | no (vista previa) |
| **5. Contenido** (mapa hecho 2026-10-20: `docencia/contenido/migracion/mapa-lecciones.csv`, 223 posts → 44 lecciones con tema, 80 sin tema, 54 blog, 45 a revisar; ver §6.1) | por pub: generar la estructura, emparejar los esqueletos con sus temas, llevar las notas de `02-contenido` y las ediciones de `web/cursos`; los artículos quedan como blog del área | cada tema con exactamente una lección; ningún contenido sin casa; redirección para cada URL vieja | no |
| **6. `aula` (API)** | FastAPI + PostgreSQL: cuentas, clases, tareas, entregas, notas, anuncios, exámenes calificados; política de privacidad; respaldo cifrado | pruebas de la API; un dictado real de prueba con cuentas ficticias | no |
| **7. Cambio** | los 11 pubs (más el 12.º) publican la plataforma uno por uno, empezando por methodica; `web/cursos` → 301; se retiran los hardlinks | prueba de las unas 149 URL (200 o 301 a un destino 200); `comparar-produccion.py`; vuelta atrás probada | **sí** |
| **8. Integraciones** (contrato hecho 2026-10-20: `divulgacion/main.py catalogo --json` → `catalogo.json`; falta que `web/_aula` lo lea, y que haya piezas publicadas) | `divulgacion` publica su `catalogo.json`; los vídeos aparecen por tema | el vídeo aparece en la lección de su tema | sí |

Las fases 2 y 3 no dependen de las demás. La 2 alivia hoy mismo el problema de los 47 min.

### 6.1 Hallazgo del mapa: el temario de varios cursos es peor que la serie del pub

`mapa-lecciones.py` empareja cada post con un tema de `curso.yml` por curso, numeración y título. La confianza alta acierta
16 de 16 en la muestra revisada a mano y la media, alrededor del 81 %. Solo 44 de 223 posts casan, y la razón no es el emparejador:
muchos temarios de `curso.yml` son esquemas genéricos. En las herramientas son índices tipo w3schools en inglés; en economía,
unidades vagas. Las series de los pubs, en cambio, tienen una estructura real y pensada (Python 01–11, econometría 01–07,
aequilibria 01–11). Que «mande el currículo» no puede querer decir que una lista genérica pise una serie mejor.

**Propuesta (decisión C1 del autor):** el currículo sigue viviendo en `curso.yml` (A3), pero su temario se **reconstruye** curso
por curso a partir de la mejor estructura que exista. Puede salir de la malla o sílabo oficial, de la serie del pub o de las
sesiones dictadas, y se elige una de esas fuentes por curso. Las otras se emparejan contra ella. Así el currículo manda y no se
pierde lo ya escrito. Primero van los cursos con contenido real: Python, R, econometría I–II, microeconometría, organización
industrial, finanzas internacionales y Linux. Los casos que necesitan al autor (aequilibria 01–11 reparte temas de varios cursos
de macro; los temas que solo existen en los pubs; los cursos Power BI y ciberseguridad) están en el informe del mapa.


## 7. Decisiones abiertas

| id | pregunta | recomendación |
|---|---|---|
| ~~B1~~ | ¿Dónde vive la API del aula? | **decidido (A9)**: en la laptop, con Docker y Tailscale Funnel; con la laptop apagada el aula no responde (la vitrina sigue en Netlify) y el enlace no cambia. Si algún día hace falta disponibilidad continua, la misma receta Docker sube a un VPS sin cambios |
| B2 | ¿Dominio propio? Los 12 `*.netlify.app` son dominios distintos: una sesión iniciada en aequilibria no vale en optimums | un dominio propio con subdominios (`aequilibria.<dominio>`…) permite una sola sesión para los 12; sin él, se inicia sesión en cada sitio con la misma cuenta |
| ~~B3~~ | ¿12.º sitio para preuniversitario y nivelación? | **decidido** (director por encargo del autor, 2026-10-20): sí; nombre propuesto *Propaedeutica*; crear el repo y el sitio Netlify es publicar, así que entra en la fase 7 con el visto bueno del autor. Hasta entonces el área `preuniversitario` de `docencia/config/areas.yml` lleva `pub: null` |
| ~~B4~~ | ¿Nombre y lugar de la plataforma? | **decidido por el autor: `aula`, dentro del hub como `web/_aula`** (2026-10-20); sin repo ni remoto propios |
| ~~B5~~ | ¿`_site` versionado (decisión del 2026-09-22)? | **decidido** (director, 2026-10-20): se mantiene la decisión del autor: los sitios se construyen en la laptop y se versiona lo publicado; Netlify no construye, porque no puede leer `docencia` (privado) ni Quarto/LuaLaTeX. Con Astro, `dist/<pub>` ocupa el lugar de `_site/` |
| B6 | ¿Licencia única de los 12 sitios? (D9 del diagnóstico de documentación) | cerrarla antes de la fase 7 |

## 8. Límite honesto

- Los tiempos de build con Astro son una estimación hasta medirlos en el piloto (fase 4).
- La API del aula es software con usuarios reales: requiere servidor, mantenimiento, copias y cuidado legal. Es la fase más costosa y
  la única con un costo mensual.
- Pyodide pesa unos 10 MB en la primera carga; la vista ligera precalculada cubre los celulares lentos.
- Los exámenes, según `docencia/contenido/migracion/estado-examenes.csv` (945 expedientes): **222 transformados**, es decir, el
  original (PDF escaneado, Word o foto) ya está reescrito como `.tex` de la clase `academic-exam`, del que salen enunciado, clave y
  solucionario; **698 pendientes**, con solo la ficha `.md` de procedencia y el original, todavía sin `.tex`; y **25 manuales**
  (manuscritos o ilegibles). Nada se borra: los `.tex` y los originales se quedan en `docencia` (privado) y el pub muestra el PDF que el
  autor libere. Transformar los pendientes es trabajo de contenido, no de plataforma.
- Este diagnóstico no abrió `docencia/registro` ni el contenido de ningún examen.
