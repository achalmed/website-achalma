---
tipo: doc
titulo: "Plataforma educativa: diagnóstico y arquitectura objetivo de la web personal"
estado: borrador
creado: 2026-10-20
---
# Plataforma educativa: diagnóstico y arquitectura objetivo

> Encargo del autor (2026-10-20): transformar la web personal en un ecosistema educativo y de divulgación
> (cursos completos, blogs, materiales docentes, simuladores), con una identidad propia que tome principios del sitio
> de demostración de Qillqa sin confundirse con él, y decidir qué se hace con Quarto y qué no. **Primero el
> diagnóstico; nada se ha movido ni renombrado.** Cifras medidas el 2026-10-20 en solo lectura; las decisiones
> abiertas están en §6 y no se ejecuta ninguna fase sin ellas.

## 1. Resumen

1. **El contenido docente se escribe en tres sitios y se publica en catorce.** El currículo está en
   `docencia/contenido` (52 `curso.yml`, 1 952 temas). Las lecciones están repartidas entre los 11 pubs (unos 160 posts con
   forma de lección), `docencia` (18 notas) y `web/cursos` (2 cursos con ediciones). El resultado se publica en el hub y en 11 sitios Netlify.
2. **Casi todo lo «publicado» como curso está vacío.** 146 de los 223 posts de los pubs son borradores y
   unos 130 son esqueletos que solo contienen los includes. Hay 31 fichas de curso con sílabo generado, pero solo 2 tienen sesiones.
   Una buena noticia para la migración: hay poco que mover y mucho que ordenar.
3. **Quarto no es el problema; el acoplamiento sí.** De 223 posts solo 17 tienen código, y todos están congelados. El render
   completo de la familia tarda unos **47 min** (pubs 2 800 s y hub entre 320 y 530 s; registro de la ola 6). La mayor parte de ese tiempo se va en el PDF
   (LuaLaTeX) y el DOCX que apaquarto genera para cada post en cada render. Además hay 12 proyectos separados y el tema
   copiado 11 veces.
4. **Recomendación:** un sitio único, construido con un generador estático (Astro), que hace de plataforma. Quarto
   y LuaLaTeX pasan a ser los **compiladores de documentos** (PDF, DOCX, diapositivas y lecciones con código), y solo se ejecutan cuando su
   fuente cambia. `docencia` sigue siendo la fuente única del currículo, `simuladores` pasa a ser un repo propio que corre en el navegador
   (Pyodide) y `divulgacion` sigue siendo independiente, aunque publica su catálogo.
5. **Las rutas se conservan.** Hoy hay unas 149 URL publicadas (60 del hub y 89 de los pubs). Cada una tendrá su página o su
   redirección 301, comprobadas con una prueba automática antes del cambio.

## 2. Diagnóstico

### 2.1 La web hoy (`web`, repo `website-achalma`)

| sección | fuentes | qué es | observación |
|---|---|---|---|
| Inicio, About, Contact, Appointment | 4 `.qmd` | perfil | presentación estática; la portada no muestra lo que el autor hace |
| Cursos | 70 `.qmd` y 30 `.md`, 100 MB | 31 fichas, facetas por área | 8 en `draft`; 22 con sílabo generado desde `curso.yml`; solo Metodología (ediciones 2025-1 y 2026-1) y `pre_economia` tienen sesiones |
| Publications | 2 `.qmd` | lista bibliográfica | — |
| Datos | 1 `.qmd` y `plataforma.html` | observatorio generado por `datafw/tools/plataforma.py` | autocontenido; funciona y no se toca |
| Blog | 11 `.qmd`, 6 posts | artículos generales | separado de los 11 pubs |
| «More» | menú con 11 enlaces | los pubs, cada uno en su dominio | el visitante sale del sitio para leer el 90 % del contenido |

La identidad actual es el design system «Quiet Laboratory» (`assets/scss/`, tokens `$lab-*`, papel cálido `#FBFBF8`, tinta
`#101820`, azul de revista `#0F5CA8`, verde `#2F7D5D`, rótulos en monoespaciada). Es sobria y coherente, y vale la pena conservarla. Su
debilidad es la experiencia: tarjetas grises sin imagen ni progreso, ningún elemento interactivo en la portada y una navegación que dispersa
al lector entre 12 dominios.

### 2.2 Los 11 pubs (`web/_pubs`, 985 MB)

| pub | tema | posts | esqueletos | naturaleza | destino propuesto |
|---|---|---|---|---|---|
| epsilon-y-beta | Econometría | 49 | 45 | ~92 % lecciones (01–07 por nivel) | lecciones → cursos de econometría; 2 investigaciones → blog |
| numerus-scriptum | Programación | 80 | 56 | ~87 % lecciones (python, r, stata, matlab, ofimática…) | lecciones → cursos de herramientas; guías sueltas → blog |
| aequilibria | Macroeconomía | 13 | 11 | serie 01–11 de macroeconomía I | lecciones → curso; 2 artículos → blog |
| optimums | Microeconomía | 14 | 7 | micro I y organización industrial (apuntes reales) | lecciones → cursos |
| pecunia-fluxus | Finanzas | 9 | 7 | finanzas I y finanzas internacionales | lecciones → cursos |
| axiomata | Matemática | 2 | 0 | apuntes escaneados y un artículo | apuntes → curso; artículo → blog |
| chaska | Linux y seguridad | 32 | 13 | tutoriales seriados (i3wm, Linux), no cursos dictados | **blog** con series |
| methodica | Metodología | 7 | 0 | guías y recursos (Quarto, Zotero) | **blog** del área de metodología |
| dialectica-y-mercado | Filosofía | 9 | 0 | ensayos y opinión | **blog** |
| actus-mercator | Gestión | 5 | 0 | trabajos y casos (planes de negocio) | **blog** o casos de estudio |
| res-publica | Gestión pública | 3 | 0 | artículos breves | **blog** |

**Conclusión:** unos 160 de los 223 posts (~70 %) tienen forma de lección, y unos 130 de ellos son esqueletos. Si se descuentan los esqueletos, quedan unos 85 posts con contenido real: unos 30 son apuntes de curso (Python 01–11, R, organización industrial, finanzas
internacionales, economía matemática) y unos 55 son blog. Todos los posts llevan `curso:` en el frontmatter, con ids que
`curso.yml` ya resuelve por `alias`. Por eso el mapeo a cursos es mecánico.

Peso: unos 417 MB son `.git` embebidos y unos 168 MB son `_site` versionados. `assets/` pesa 4,1 MB y está repetido 11 veces. Los 37 `_metadata.yml`
de sección son idénticos. Ningún pub usa reveal.js.

### 2.3 `docencia` (repo `CampusTeX-Research`) y su contenido

`docencia` ya tiene el modelo de datos que la plataforma necesita; solo le falta salida web:

- `curso.yml` es la fuente única del currículo. Contiene `unidades[].temas[]` con `archivo` y `recursos[]`, `bibliografia[].calibre_id`,
  `datasets[].clave` (datafw), `banco_examenes`, `materia_web` (varios cursos pueden ir a una ficha), `tipo` y `area[]`.
- Las sesiones tipadas (`clase`, `laboratorio`, `taller`, `evaluacion`) llevan `sesion.yml` y `guion.md`. Cada `dictado.yml` reúne las sesiones de una
  edición real (institución y ciclo).
- Contenido: 52 cursos, 303 unidades, 1 952 temas, **18 notas escritas**, 67 sesiones en 10 cursos y unos 850 `.tex` de
  evaluación (exámenes desde 2012) que la web no publica hoy.
- Escritores hacia la web: `temario-generar.sh` escribe el bloque del sílabo y `publish-web.sh` crea los hardlinks de PDF por edición.
- Pendiente propio (`docencia/estado.md`): `temario.py`, `enlazar.py` y `publicar-web.py` todavía deducen `~/Documents` en lugar
  de usar `core/env.py` (N 5.1).

**Lo sensible se queda fuera.** `docencia/registro` (estudiantes y notas) no se toca ni se publica; la plataforma no lo lee
nunca (regla 8).

### 2.4 Duplicaciones medidas

| tema | dónde aparece | fuente única propuesta |
|---|---|---|
| Metodología, APA, monografías | `sistema-apa` (6 sesiones), `monografias/s03`, web 2025-1 (9 sesiones sin fuente en docencia), web 2026-1 (hardlinks), 7 posts de methodica | `docencia`: cursos `monografias` y `sistema-apa`; methodica como su blog |
| Python | 18 notas en `docencia`, 14 posts en numerus-scriptum, ficha web | `docencia/contenido/cursos/python` |
| Excel y Power BI | 20 talleres en `docencia`, 20 posts de ofimática, ficha en borrador | `docencia` |
| Econometría | econometria-i/ii, con-python (13 notebooks), r-y-python, 50 páginas de epsilon-y-beta, ficha | `docencia`; los temas que solo están en el pub (control sintético, bayesiana) se suman a `curso.yml` |
| Macro y micro | `curso.yml` en `docencia`, series de aequilibria y optimums | `docencia` |
| Solo en la web | álgebra lineal, cálculo, optimización, SQL y las tres preuniversitarias | se dan de alta en `docencia` o, las preuniversitarias, se enlazan con `11 Book` |

### 2.5 Simuladores (`docencia/simuladores`, 5,5 MB)

- Contenido: 115 modelos de macro en 12 niveles (el nivel 12 usa series del BCRP vía datafw, con un snapshot de respaldo) y 23 de estadística,
  más animaciones Manim.
- Estructura: cada modelo es un `base.Modelo` con `Ficha` (contexto, derivación, supuestos, fuentes verificadas contra el PDF de Calibre),
  parámetros, escenarios y verificaciones.
- **Dependencias: solo `numpy`** en los modelos. matplotlib está únicamente en `graficos.py` y `app.py` (aplicación de escritorio).
- Consumidores: `docencia` (29 recursos `tipo: simulador` en los `curso.yml`) y `divulgacion` (`lib/simuladores.py` llama a
  `m.verificaciones` y a las curvas sin copiar ecuaciones).
- Hoy no se publican en ningún sitio.

### 2.6 `divulgacion`

Es una suite de microdivulgación audiovisual (9:16, 16:9, 1:1, 4:5; canal «achalmaedison», 7 series). Funciona así:

- Entradas: lee simuladores, paquetes de datafw, Calibre y los `curso.yml` en solo lectura. Cada pieza declara `curriculo: [{curso, tema}]`.
- Productos: los deja en `$VIDEOS_DIR/divulgacion/`.
- Estado: 9 piezas en borrador y `publicaciones: []` en todas. El «enlace de vuelta» (el vídeo como recurso del tema) está pendiente en su
  `docs/decisiones.md`.

**No es «divulgación de documentos»: es un estudio de producción de vídeo**, con dependencias pesadas (Manim y su entorno
conda) y un ciclo propio. No conviene meterlo en la plataforma, pero sí cerrar su enlace de vuelta.

### 2.7 Dependencias que no deben romperse

| quién | depende de | cómo | qué cuida la propuesta |
|---|---|---|---|
| `docencia/scripts/temario.py` | `web/cursos/*/index.qmd`, `web/_pubs` | escribe un bloque entre marcas y lee `curso:` | se sustituye por un **lector** de `curso.yml` en la plataforma; el escritor se retira solo después del cambio de sitio |
| `docencia/scripts/publicar-web.py` | `web/cursos/<materia>/<edicion>/` | hardlinks de PDF | la plataforma lee `dictado.yml` y `publicacion/` directamente; los hardlinks dejan de hacer falta |
| simuladores (nivel 12), 3 exámenes de econometría II | `datafw` | `DATAFW_DIR` | sin cambios; el repo nuevo usa la misma variable |
| `divulgacion/lib/simuladores.py` | `docencia/simuladores` | ruta | variable nueva `SIMULADORES_DIR` en `core/env.sh`, con el alias antiguo durante la migración |
| `scripts-quarto`, `scripts_document_studio` (`page-counter`) | `web/_pubs` | ruta | siguen funcionando mientras `_pubs` exista; se migran en la fase 6 |
| `observatorio/` | `datafw/tools/plataforma.py` | archivo autocontenido | se copia tal cual, igual que hoy |
| `cv` | `web/resources/cv.pdf` | `generar-externos.sh` | sin cambios |
| `docencia/classes`, `sistema-editorial` | LuaLaTeX y Biber | compilación de PDF | sin cambios (N 5.14) |

### 2.8 El uso real de Quarto

| uso | volumen | ¿necesita Quarto? |
|---|---|---|
| Páginas de presentación, listados, catálogo, fichas de curso | unas 100 | no: son plantillas y datos |
| Posts y lecciones en prosa, con matemáticas y citas | unos 200 | no estrictamente: Markdown, KaTeX y citeproc lo resuelven en el generador |
| Posts con código R o Python | 17 (congelados) | **sí**: Quarto ejecuta y congela |
| PDF y DOCX APA de cada post (apaquarto) | todos los posts | **sí**, pero bajo demanda, no en cada render del sitio |
| Diapositivas reveal.js y Beamer de las sesiones | `scaffolds/sesion/deck.qmd`, `deck.tex` | **sí** (Quarto y LuaLaTeX) |
| Exámenes, sílabos, rúbricas | unos 850 `.tex` | no: los compila LuaLaTeX con las clases de `docencia` |

## 3. Qué se toma del demo de Qillqa y qué no

El sitio de `qillqa/demo/vendor/sitio` (HTML, CSS y JS sin build, unas 1 400 líneas) funciona por cinco principios:

1. **Mostrar en vez de describir.** El recorrido es interactivo: el oficio avanza de borrador a archivado, el tablero se arrastra y el dock de módulos rota capturas reales.
2. **Un solo acento.** Neutros, la tinta como protagonista y el color solo para estados y enlaces.
3. **Profundidad translúcida.** Superficies de vidrio (`--vidrio`), sombras suaves y «manchas» de color de fondo.
4. **Movimiento con freno.** El contenido se revela al hacer scroll y los contadores suben, todo dentro de `prefers-reduced-motion`. El avance automático se detiene en cuanto el usuario toca algo.
5. **Diseñado primero para 375 px**, accesible (saltar al contenido, teclado en el tablero, `aria-live`) y con modo claro y oscuro.

**Lo que se adopta:** los cinco principios, el patrón «recorrido interactivo» y la disciplina de tokens.

**Lo que no se adopta**, para que no se confunda con Qillqa:

- la tipografía de sistema estilo Apple (SF Pro);
- los grises neutros `#f5f5f7` y `#1d1d1f`;
- el vocabulario de ventanas y docks de aplicación;
- el estilo de captura flotante.

**Identidad propia: «Laboratorio abierto».** Es una evolución de Quiet Laboratory y no un tema nuevo:

- **Paleta:** papel cálido, tinta azulada, azul de revista y verde de laboratorio, más un acento por área o revista dentro de la misma paleta. Así cada
  antiguo pub conserva un color y su nombre.
- **Tipografía:** serif académica para la lectura larga, sans para la interfaz y monoespaciada para rótulos, datos y fórmulas. Es la «voz de laboratorio»
  que ya tiene el sitio.
- **Motivo gráfico:** retícula de papel milimetrado, ecuaciones y curvas. Encaja con la identidad de `divulgacion`, «Laboratorio en movimiento», así que la web
  y el canal se reconocen como familia.
- **El equivalente al recorrido de Qillqa:** un simulador vivo en la portada (por ejemplo, IS-LM con dos deslizadores) y una «lección en curso»
  que muestra cómo se ve aprender aquí. Lo interactivo es el contenido, no la decoración.

## 4. Arquitectura objetivo

### 4.1 Separación lógica y física

```
LÓGICA (lo que ve el visitante)              FÍSICA (repos)
───────────────────────────────              ──────────────────────────────────────────────
Inicio · Sobre mí · Contacto                 web            plataforma (Astro): plantillas, tema,
Cursos ─┬─ catálogo y rutas                                 lectores de contenido, redirecciones
        ├─ curso: temario, lecciones,        docencia       FUENTE del currículo y de las lecciones
        │  materiales, evaluaciones,           └ contenido  (curso.yml, sesiones, dictados, exámenes)
        │  simuladores, blog del curso
        └─ ediciones (dictados con fechas)
Revistas (antiguos pubs) ─ artículos         _pubs/*        FUENTE de los artículos (se conservan
                                                            como repos; dejan de ser sitios)
Laboratorio ─ simuladores                    simuladores    repo propio (sale de docencia), modelo
                                                            numpy + adaptador web (Pyodide)
Datos ─ observatorio                         datafw         plataforma.html, como hoy
Divulgación ─ vídeos por tema                divulgacion    independiente; publica catalogo.json
Publicaciones                                escritura, cv  sin cambios
```

**Una fuente por contenido, muchas vistas.** La web no tiene contenido propio: lo lee de las fuentes.

### 4.2 Qué se construye con qué

| producto | herramienta | cuándo corre |
|---|---|---|
| Sitio (páginas, catálogo, fichas, lector de lecciones, búsqueda) | **Astro** (estático, colecciones de contenido con esquema) y Pagefind para la búsqueda | en cada publicación, en unos segundos |
| Lección o artículo en prosa (`.md`/`.qmd` sin código) | el lector Markdown de Astro, con KaTeX y citas (CSL APA, BibTeX de Better BibTeX) | ídem |
| Lección o artículo con código (17 hoy) | **Quarto** → Markdown con figuras (`format: hugo-md` o `gfm`) y `freeze` | solo si cambió su fuente |
| PDF y DOCX APA de artículos y apuntes | **Quarto/apaquarto**, perfil `documentos` | bajo demanda o por un trabajo nocturno, con caché por hash de la fuente |
| Diapositivas de sesión | Quarto reveal.js (`deck.qmd`) o Beamer (`deck.tex`) | al preparar la sesión (`build-session.sh`, como hoy) |
| Exámenes, solucionarios, sílabos, rúbricas | **LuaLaTeX y Biber** con las clases de `docencia` | al publicar el dictado |
| Cuadernos de laboratorio | Jupyter ejecutado por Quarto (`freeze`) | solo si cambió |
| Simuladores | Pyodide (numpy en el navegador) con gráficos en JS | en el navegador del alumno |

Efecto esperado: publicar el sitio pasa de unos 47 min a **menos de 2 min**, porque los PDF ya compilados se reutilizan. Escribir
sigue igual: `.qmd` y `.tex`, con las mismas plantillas APA y LuaLaTeX.

**Por qué Astro:**

- es estático, así que Netlify sirve archivos, como hoy;
- sus colecciones validan cada `curso.yml` contra un esquema al construir, de modo que un campo mal escrito rompe la build y no la página;
- las «islas» permiten interactividad solo donde hace falta (simulador, quiz, progreso) sin convertir el sitio en una SPA;
- lee Markdown, MDX, YAML y JSON de cualquier carpeta.

**Por qué no se descarta Quarto:** es la mejor herramienta para los documentos académicos reproducibles (APA, citas, código congelado,
PDF) y el autor ya tiene su flujo, sus plantillas y su normativa construidos sobre él.

**Alternativa sin cambiar de motor (opción B):** se queda Quarto como sitio, pero con perfil `html` rápido por defecto, PDF bajo demanda y
pubs fusionados como subcarpetas. Reduce el tiempo de forma parecida, pero el lector de cursos (progreso, quiz, navegación por unidad)
habría que escribirlo en JS dentro de las plantillas de Quarto, a contracorriente de su modelo de «sitio de documentos».

### 4.3 El curso como plataforma

Funciones tomadas de Platzi, los MOOC, CAF y Classroom, ordenadas por lo que puede dar un sitio estático (fase A) y lo que exige cuentas
(fase B):

| función | fase | de dónde sale |
|---|---|---|
| Catálogo con filtros (área, tipo, nivel, estado) y búsqueda de texto completo | A | `curso.yml` y Pagefind |
| Rutas de aprendizaje (p. ej., «Economista empírico»: estadística → econometría I y II → microeconometría con Python, R o Stata) | A | `rutas.yml` nuevo en `docencia` |
| Portada del curso: objetivos, requisitos, duración, nivel, unidades, bibliografía | A | `curso.yml` y Calibre/Zotero por clave |
| Lector de lección: índice lateral de la unidad, anterior y siguiente, tiempo de lectura, matemáticas, código, figuras | A | `temas[].archivo` |
| Materiales descargables por lección (PDF, diapositivas, datos, cuadernos) | A | `recursos[]` y `publicacion/` del dictado |
| Autoevaluación con corrección inmediata (opción múltiple, numérica, verdadero o falso) | A | bloque `quiz:` nuevo en la lección o en `sesion.yml` |
| Ejercicios con solución desplegable y banco de exámenes con solucionario | A | `04-evaluaciones`: los PDF ya compilados; la clave solo si el autor la publica |
| Simulador integrado en la lección | A | `recursos: {tipo: simulador, id}` |
| Vídeo de divulgación vinculado al tema | A | `catalogo.json` de `divulgacion` |
| Progreso, marcadores y notas personales | A | almacenamiento local del navegador, sin cuenta y sin datos en el servidor |
| Comentarios por lección | A | giscus (las discusiones de GitHub sustituyen a Utterances) |
| Ediciones o dictados con calendario de sesiones | A | `dictado.yml` |
| Blog del curso | A | artículos de las revistas con `curso:` |
| Inscripción, entregas, calificaciones, avisos a un grupo | B | **Google Classroom** del dictado (o un LMS libre): los datos de estudiantes no entran nunca en los repos (regla 8) |
| Certificados | B | solo con cuentas; fuera del alcance inicial |

### 4.4 Categorías

Las áreas salen de `curso.yml` y no se inventan:

- **Economía:** micro, macro, desarrollo, pública, monetaria, internacional.
- **Métodos cuantitativos:** matemáticas, estadística, econometría.
- **Finanzas.**
- **Gestión y proyectos.**
- **Metodología de la investigación.**
- **Herramientas:** programación y software.
- **Filosofía y economía política.**
- **Preuniversitario:** enlaza `11 Book`.

Facetas transversales: `tipo` (asignatura, herramienta, taller, nivelación) y `estado`. Un curso en `borrador` no aparece en el catálogo, aunque sí en
el temario interno.

### 4.5 Rutas que se conservan

- Las fichas `/cursos/<materia>/` y las ediciones `/cursos/<materia>/<edicion>/session_NN_slug/` mantienen su URL.
- Los alias `/talk/…` y `/teching/…` se conservan como redirecciones.
- Cada URL de los 11 pubs obtiene una 301 a su nueva casa. Los dominios `*.netlify.app` de cada pub siguen vivos con un `_redirects` mínimo, sin perder enlaces externos ni el posicionamiento.
- Prueba de salida: un script toma los `sitemap.xml` de hoy (unas 149 URL) y exige 200 o 301 a un destino 200 para cada una.

## 5. Plan de implementación progresivo

Cada fase deja todo funcionando. Producción no cambia hasta la fase 7, y cada paso estructural sigue N 3.13 (auditoría →
propuesta → aprobación → `core/renombrar.py` con etiqueta, simulación, respaldo y `UNDO.sh`).

| fase | qué | prueba de salida | ¿toca producción? |
|---|---|---|---|
| **0** | Decisiones D1–D9 (§6) | acta en este documento | no |
| **1** | Contrato: esquema de `curso.yml` ampliado (nivel, duración, requisitos, `quiz`, rutas) y de `catalogo.json`; corregir `temario.py`, `enlazar.py` y `publicar-web.py` para que usen `core/env.py` | `core/suites.py` y el validador sin empeorar; esquema publicado en `core/` | no |
| **2** | Ganancia rápida en Quarto: perfil `html` por defecto y PDF/DOCX en un perfil `documentos` con caché | el render de la familia baja de unos 47 min; los PDF no cambian byte a byte (`SOURCE_DATE_EPOCH`) | sí, pero sin cambiar el contenido |
| **3** | Prototipo de la plataforma en Astro en la rama `wip/` de `web`, con identidad «Laboratorio abierto» y 3 pilotos: **Metodología** (con ediciones), **Python** (con código y PDF) y la revista **methodica** | construcción en menos de 2 min; Lighthouse ≥ 90 en accesibilidad y rendimiento a 375 px; claro y oscuro; vista previa en Netlify | no (vista previa) |
| **4** | `simuladores` como repo propio (sale de `docencia` con su historia) más un adaptador web con 2 modelos (IS-LM y TCL) | `main.py verificar` igual que antes; `divulgacion` renderiza una pieza con `SIMULADORES_DIR`; el simulador corre a 375 px | no |
| **5** | Migración de contenidos: unos 30 apuntes reales de los pubs → `docencia/contenido`; los unos 130 esqueletos se retiran porque los temas ya están en `curso.yml`; los unos 55 artículos se quedan en su revista | ningún contenido sin destino; cada lección con exactamente una fuente | no |
| **6** | Todos los cursos y revistas en la plataforma; `scripts-quarto` y `page-counter` apuntan a las fuentes nuevas | paridad de las unas 149 URL; los consumidores de `_pubs` en verde | no |
| **7** | Cambio de sitio: Netlify publica la plataforma; los 11 dominios de los pubs pasan a redirecciones; el `_site` anterior queda etiquetado para volver atrás | `comparar-produccion.py` y la prueba de rutas en producción; plan de vuelta probado | **sí** |
| **8** | Divulgación: `catalogo.json` y enlace de vuelta; fase B (Classroom) si el autor la quiere | el vídeo aparece en la lección de su tema | sí |

Las fases 2 y 4 no dependen de la 3 y pueden avanzar en paralelo.

## 6. Decisiones del autor

| id | pregunta | recomendación | por qué |
|---|---|---|---|
| D1 | ¿Motor del sitio? | **Astro como plataforma y Quarto/LuaLaTeX como compiladores** (opción A); la B (todo Quarto, optimizado) queda como alternativa | el lector de cursos y la interactividad son naturales en A; los documentos siguen en Quarto |
| D2 | ¿Los 11 pubs? | **Se conservan como repos y nombres, pero se publican dentro del sitio único como «revistas»**, con redirecciones desde sus dominios | lectores en un solo sitio, un tema en vez de 12 y 12 builds menos; cada revista conserva identidad y color |
| D3 | ¿Dónde viven las lecciones? | **`docencia/contenido`**, junto al `curso.yml` | ya es la fuente del currículo; separar lección y temario repetiría la dispersión |
| D4 | ¿Simuladores? | **Repo propio `simuladores`** (L3), con adaptador web Pyodide; el escritorio sigue igual | dos consumidores (`docencia`, `divulgacion`) más la web; ciclo propio; solo numpy |
| D5 | ¿Funciones con cuenta (entregas, notas)? | **Fase B, mediante Google Classroom** por dictado; nada de backend propio por ahora | los datos de estudiantes no entran en los repos (regla 8); un sitio estático no los custodia |
| D6 | ¿`_site` versionado (decisión del 2026-09-22)? | Con Astro, **Netlify construye el sitio** y solo los PDF compilados se versionan (o van como artefactos) | el sitio se reconstruye en segundos; lo caro de rehacer son los PDF |
| D7 | ¿`divulgacion`? | **Independiente**; publica `catalogo.json` y la plataforma lo lee | ciclo y dependencias de producción de vídeo; no es contenido web |
| D8 | ¿Tema por hardlinks (decisión del 2026-10-08)? | Se retira al llegar la fase 7: con un solo sitio no hay nada que propagar | hasta entonces se respeta tal cual |
| D9 | ¿Nombre de la plataforma? | El autor lo elige; propuesta: mantener «Edison Achalma» como marca y, si quiere un nombre, uno propio que no sea de la familia Qillqa (ni Qillqa, ni Tiqsi, ni Unancha) | evitar la confusión con Qillqa que el encargo pide evitar |

La licencia única (D9 del diagnóstico de documentación) sigue abierta y conviene cerrarla antes de la fase 7.

## 7. Límite honesto

- Las cifras de tiempo de la plataforma (menos de 2 min) son una estimación para unas 500 páginas en Astro; se miden en la fase 3 antes de
  comprometerlas.
- El progreso sin cuenta vive en el navegador del alumno: no pasa de un dispositivo a otro.
- Los simuladores en Pyodide cargan unos 10 MB la primera vez; la fase 4 mide si es aceptable en móvil o si conviene precalcular escenarios en
  JSON para la vista ligera.
- Las 850 evaluaciones existen sobre todo como `.tex` sin transformar al estándar; publicarlas es trabajo de contenido, no de plataforma, y
  el autor decide cuáles salen con clave.
- Este diagnóstico no abrió `docencia/registro` (sensible).
