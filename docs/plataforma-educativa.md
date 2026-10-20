---
tipo: doc
titulo: "Plataforma educativa: diagnóstico y arquitectura objetivo (los 11 pubs como aulas)"
estado: borrador
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

### 2.1 La web hoy (`web`, repo `website-achalma`)

| sección | fuentes | observación |
|---|---|---|
| Inicio, About, Contact, Appointment | 4 `.qmd` | presentación estática; la portada no muestra lo que el autor hace |
| Cursos | 70 `.qmd` y 30 `.md`, 100 MB | 31 fichas, 8 en `draft`; 22 con sílabo generado desde `curso.yml`; solo Metodología (2025-1, 2026-1) y `pre_economia` tienen sesiones |
| Publications, Datos (observatorio de `datafw`), Blog (6 posts) | — | funcionan; el observatorio es un archivo autocontenido generado |
| «More» | 11 enlaces | los pubs, cada uno en su dominio |

La identidad es el design system «Quiet Laboratory» (`assets/scss/`, tokens `$lab-*`): papel `#FBFBF8`, tinta `#101820`, azul `#0F5CA8`,
verde `#2F7D5D` y rótulos en monoespaciada. Es sobria y coherente, y se conserva. Su debilidad es la experiencia: tarjetas grises sin
imagen ni progreso y nada interactivo en la portada.

### 2.2 Los 11 pubs (985 MB)

| pub | tema | posts | esqueletos | naturaleza |
|---|---|---|---|---|
| epsilon-y-beta | Econometría | 49 | 45 | ~92 % lecciones (01–07 por nivel) y 2 investigaciones |
| numerus-scriptum | Programación | 80 | 56 | ~87 % lecciones (python, r, stata, matlab, ofimática) y guías sueltas |
| aequilibria | Macroeconomía | 13 | 11 | serie 01–11 de macroeconomía I y 2 artículos |
| optimums | Microeconomía | 14 | 7 | micro I y organización industrial (apuntes reales) |
| pecunia-fluxus | Finanzas | 9 | 7 | finanzas I y finanzas internacionales |
| axiomata | Matemática | 2 | 0 | apuntes escaneados y 1 artículo |
| chaska | Linux y seguridad | 32 | 13 | tutoriales seriados (i3wm, Linux) |
| methodica | Metodología | 7 | 0 | guías (Quarto, Zotero) |
| dialectica-y-mercado | Filosofía | 9 | 0 | ensayos |
| actus-mercator | Gestión | 5 | 0 | casos (planes de negocio) |
| res-publica | Gestión pública | 3 | 0 | artículos breves |

Totales y características comunes:

- **Contenido:** de los 223 posts, unos 160 tienen forma de lección y unos 130 son esqueletos; unos 30 son apuntes reales y unos 55, blog.
- **Enlace con el currículo:** cada post lleva `curso:` con un id que `curso.yml` resuelve por `alias`.
- **Peso:** unos 417 MB son `.git` embebidos; `assets/` (4,1 MB) se repite 11 veces.
- **Formatos y código:** solo 17 posts tienen código, y todos están congelados. Todos los posts declaran salida HTML, PDF (apaquarto, LuaLaTeX) y DOCX.
- **URL publicadas:** 89 (los borradores no se publican).

### 2.3 `docencia`

Tiene el modelo de datos que la plataforma necesita:

- **`curso.yml`:** unidades, temas con `archivo` y `recursos`, `bibliografia[].calibre_id`, `datasets[].clave`, `banco_examenes`, `tipo`, `area`.
- **Sesiones y dictados:** sesiones tipadas (`clase`, `laboratorio`, `taller`, `evaluacion`) y `dictado.yml` por cada edición real.
- **Volumen:** 52 cursos, 303 unidades, 1 952 temas, **18 notas escritas**, 67 sesiones y unos 850 `.tex` de evaluación.
- **Marcos LaTeX propios:**
  - `classes/` (`academic-base`, `academic-exam`, `academic-report`, `academic-beamer`);
  - `themes/academic` (Beamer);
  - `templates/` (12 tipos de examen, 8 de presentación, 4 de informe);
  - `scaffolds/sesion/` (`deck.tex` Beamer y `deck.qmd` reveal.js).

Hechos que deciden dónde va cada cosa:

- **Visibilidad.** `docencia` (`CampusTeX-Research`) es **público**. Su contenido (`contenido/`, `Academic_Class`) es **privado** y guarda los exámenes con
  sus claves. Los 11 pubs son **públicos**. Ninguna clave ni examen inédito puede pasar a un pub.
- **Lo sensible.** `docencia/registro` (estudiantes y notas) es sensible (regla 8) y no se toca.
- **Diapositivas.** Las de clase **no dependen de `escritura`**. `docencia` tiene su Beamer y su reveal.js; `escritura` tiene `lamina.cls` y
  `presentacion.cls` para defensas, ponencias y conferencias, y `docencia` solo toma de ella el esquema del guion. Son dos marcos con funciones
  distintas. Ambos usan la capa de diseño `sistema-editorial` (§2.7).
- **Rutas.** `temario.py`, `enlazar.py` y `publicar-web.py` deducen `~/Documents` en lugar de usar `core/env.py` (N 5.1).

### 2.4 Duplicaciones

| tema | dónde aparece hoy | casa única |
|---|---|---|
| Metodología, APA, monografías | `sistema-apa`, `monografias/s03`, web 2025-1 y 2026-1, 7 posts de methodica | currículo en `docencia`; lecciones y ediciones en **methodica** |
| Python | 18 notas en `docencia`, 14 posts, ficha web | currículo en `docencia`; las 18 notas pasan a **numerus-scriptum** y se funden con sus 14 posts tema por tema |
| Excel y Power BI | 20 talleres en `docencia`, 20 posts, ficha | currículo en `docencia`; lecciones en **numerus-scriptum** |
| Econometría | `econometria-i/ii`, `-con-python`, `-r-y-python`, 50 páginas de epsilon-y-beta, ficha | currículo en `docencia` (los temas que solo están en el pub entran en `curso.yml`); lecciones en **epsilon-y-beta** |
| Macro y micro | `curso.yml`, series de aequilibria y optimums | ídem, en **aequilibria** y **optimums** |
| Solo en la web | álgebra lineal, cálculo, optimización, SQL, Power BI, preuniversitarias | alta en `curso.yml` (o mapeo a `matematicas-i/ii/iii`) antes de migrar |

### 2.5 `simuladores` (hoy `docencia/simuladores`, 5,5 MB)

- **Modelos:** 115 de macro en 12 niveles y 23 de estadística, más animaciones Manim. Cada uno es un `base.Modelo` con su `Ficha`, que lleva las fuentes verificadas contra el PDF de Calibre.
- **Dependencias:** los modelos usan **solo `numpy`**; matplotlib está únicamente en la aplicación de escritorio. Por eso pueden correr en el navegador con Pyodide sin
  reescribirse. El nivel 12 lee series del BCRP desde `datafw` (`DATAFW_DIR`) y tiene un snapshot de respaldo.
- **Consumidores:** `docencia` (29 recursos `tipo: simulador`) y `divulgacion` (`lib/simuladores.py`, que usa `m.verificaciones` y las curvas).

### 2.6 `divulgacion`

Es un estudio de producción de vídeo corto (9 piezas en borrador, Manim, canal «achalmaedison»), **no un archivo de documentos**:

- lee simuladores, `datafw`, Calibre y los `curso.yml`;
- cada pieza declara `curriculo: [{curso, tema}]`;
- deja sus productos en `$VIDEOS_DIR/divulgacion/`;
- todavía no publica nada.

Sigue independiente. Lo que falta es el «enlace de vuelta»: un catálogo que los pubs leen para mostrar el vídeo en la lección de su tema.

### 2.7 Los marcos LaTeX y su capa de diseño

| proyecto | qué es | ejemplo |
|---|---|---|
| `sistema-editorial` | **capa de diseño**, no un marco: tipografías, colores y maquetas en YAML que generan `.tex` de configuración | `temas/docencia.yml` → `docencia/config/palette.tex` |
| `docencia/classes` | marco de **docencia**: exámenes, sílabos, rúbricas, decks Beamer | `academic-exam` |
| `escritura/classes` | marco de **producción académica**: tesis, artículos, informes, láminas de exposición | `lamina.cls` |
| `marco_documental` (en `sgdp`) | marco de **documentos oficiales** del despacho | oficios, informes |

Son tres marcos de clases, uno por dominio, que comparten una misma capa de diseño. La plataforma no los cambia: publica sus PDF.

### 2.8 El uso real de Quarto y el costo del render

Tiempos del render completo (registro de la ola 6): pubs 2 800 s y hub entre 320 y 530 s, unos **47 min** en total. Casi no hay código que ejecutar, así que el
tiempo se va en apaquarto: **un PDF con LuaLaTeX y un DOCX por cada post en cada render**, en 12 proyectos.

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
aula (repo nuevo)     el CÓDIGO de la plataforma: componentes Astro,   un paquete versionado que los 12 sitios
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
| `curso.yml` (currículo), `rutas.yml` nuevo, `dictado.yml` | el texto de las lecciones (18 notas, más lo escrito en los posts) | `simuladores/` con su historia | `web/cursos` (su contenido va a methodica y al 12.º sitio) |
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

Hoy el tema de los 12 sitios se reparte con hardlinks (decisión del 2026-10-08). Con la plataforma, el código vive en el repo nuevo **`aula`**
(el nombre lo elige el autor) y cada pub fija una versión del paquete, igual que fija la versión de una librería. Un pub queda reducido a su
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

El campo `area` de los 52 `curso.yml` tiene hoy 20 valores. Mezcla áreas (`macroeconomia`, `finanzas`) con nombres de herramientas (`python`, `stata`,
`eviews`) y tiene grafías dobles (`math` y `matematicas`). Propuesta: un **vocabulario cerrado de 12 áreas**, una por sitio. El área decide el pub
de cada curso; un curso vive en un pub y puede listarse en otros.

| sitio | área normalizada | cursos | cambio respecto de hoy |
|---|---|---|---|
| aequilibria | Macroeconomía | macroeconomia-i, -ii, -dinamica, crecimiento-economico, economia-monetaria, comercio-internacional, economia-computacional | ninguno |
| optimums | Microeconomía | microeconomia-i, -ii, organizacion-industrial, economia-del-desarrollo, economia-recursos-naturales-ambientales | sale microeconometria-aplicada |
| epsilon-y-beta | Estadística y econometría | estadistica, estadistica-para-economistas, econometria-i, -ii, **microeconometria-aplicada**, **econometria-con-python**, **econometria-r-y-python**, **indicadores-de-pobreza-enaho** | se renombra el área; entran 4 cursos (hoy en micro, python y stata) |
| axiomata | Matemáticas | matematicas-i, -ii, -iii, investigacion-operativa | `math` → `matematicas`; álgebra lineal, cálculo y optimización de la web se mapean a estos o se dan de alta |
| pecunia-fluxus | Finanzas | finanzas-i, -ii, -iii | ninguno |
| actus-mercator | Gestión empresarial y proyectos | formulacion-de-proyectos, evaluacion-privada-de-proyectos, investigacion-de-mercados | sale evaluación social |
| res-publica | Gestión y economía pública | economia-publica, **evaluacion-social-de-proyectos** | entra evaluación social (inversión pública) |
| dialectica-y-mercado | Filosofía, historia y economía política | economia-politica, filosofia-politica, historia-economica | `filosofia` y `economia` se unen |
| methodica | Metodología de la investigación | ensayo, monografias, seminario-de-investigacion, sistema-apa, más las ediciones de Metodología de `web/cursos` | ninguno |
| numerus-scriptum | Programación y software | python, r, stata, eviews, spss, gretl, excel, latex, git, geogebra, conceptos-de-programacion; Power BI y SQL (alta) | 9 valores de herramienta se unen en uno |
| chaska | **Sistemas y seguridad** | **bash** (sale de herramientas), más Linux y ciberseguridad (altas desde sus series) | **área nueva**: hoy chaska no tiene ningún curso en el currículo |
| **12.º sitio** (nombre por decidir; p. ej. *Propaedeutica*) | Preuniversitario y nivelación | curso-0, pre_algebra, pre_aritmetica, pre_economia, más los libros de `11 Book` | **sitio nuevo**: otro público (escolares y postulantes) con otro lenguaje; mezclarlo con cursos universitarios confunde a los dos |

Así, 10 de los 11 pubs ya casan con un área del currículo, `chaska` gana la suya y preuniversitario recibe un sitio. Las categorías actuales
del hub (Ciencia de Datos, Economía, Gestión, Investigación, Preuniversitario) desaparecen con `web/cursos`. Esta normalización resuelve
también la decisión D4 pendiente del diagnóstico de simuladores (vocabulario de áreas).

## 6. Plan de implementación

Cada fase deja todo funcionando. Los sitios en producción no cambian hasta la fase 7, y cada paso estructural sigue N 3.13 (auditoría,
propuesta, aprobación, `core/renombrar.py` con etiqueta, simulación, respaldo y `UNDO.sh`).

| fase | qué | prueba de salida | ¿producción? |
|---|---|---|---|
| **1. Currículo** (**hecha** 2026-10-20: vocabulario de 12 áreas en `docencia/config/areas.yml`, 29 cursos normalizados, `validate.sh` lo exige, altas de MATLAB y Linux, título de Matemáticas I; las rutas por `core/env.py` ya estaban; los campos nuevos de `curso.yml` y `rutas.yml` pasan a la fase 4, donde los fija el generador que los lee) | vocabulario de 12 áreas; mover los 5 cursos; altas que faltan (Linux, ciberseguridad, Power BI, SQL, temas que solo están en los pubs); esquema de `curso.yml` ampliado (nivel, duración, requisitos, `pub`), `rutas.yml`; scripts de `docencia` a `core/env.py` | cada curso con un área válida y un pub; validador sin empeorar | no |
| **2. Render rápido** (independiente) | en los 12 sitios Quarto actuales, perfil `html` por defecto y PDF/DOCX en el perfil `documentos` con caché | de unos 47 min a pocos minutos; PDF idénticos byte a byte (`SOURCE_DATE_EPOCH`) | sí, sin cambiar contenido |
| **3. `simuladores`** (**hecha** 2026-10-20: repo propio con 64 commits de historia, `SIMULADORES_DIR`, `main.py catalogo` → `catalogo.json` con 138 modelos, verificaciones idénticas; respaldo y `UNDO.sh` en `$RESPALDOS_DIR/renombres/2026-10-20-docencia-simuladores-a-simuladores/`; alta en `workspace.yml`, remoto y adaptador web pendientes) | repo propio con su historia; `SIMULADORES_DIR`; adaptador web con IS-LM y TCL | `main.py verificar` igual; `divulgacion` renderiza una pieza; el simulador corre a 375 px | no |
| **4. `aula` (vitrina)** | repo nuevo; paquete Astro con la identidad «Laboratorio abierto»; generador `curso.yml` → pub; piloto **methodica** (tiene ediciones reales) | build en segundos; Lighthouse ≥ 90 a 375 px; claro y oscuro; vista previa en Netlify | no (vista previa) |
| **5. Contenido** | por pub: generar la estructura, emparejar los esqueletos con sus temas, llevar las 18 notas y las ediciones de `web/cursos`; los artículos quedan como blog del área | cada tema con exactamente una lección; ningún contenido sin casa; redirección para cada URL vieja | no |
| **6. `aula` (API)** | FastAPI + PostgreSQL: cuentas, clases, tareas, entregas, notas, anuncios, exámenes calificados; política de privacidad; respaldo cifrado | pruebas de la API; un dictado real de prueba con cuentas ficticias | no |
| **7. Cambio** | los 11 pubs (más el 12.º) publican la plataforma uno por uno, empezando por methodica; `web/cursos` → 301; se retiran los hardlinks | prueba de las unas 149 URL (200 o 301 a un destino 200); `comparar-produccion.py`; vuelta atrás probada | **sí** |
| **8. Integraciones** | `divulgacion` publica su `catalogo.json`; los vídeos aparecen por tema | el vídeo aparece en la lección de su tema | sí |

Las fases 2 y 3 no dependen de las demás. La 2 alivia hoy mismo el problema de los 47 min.

## 7. Decisiones abiertas

| id | pregunta | recomendación |
|---|---|---|
| ~~B1~~ | ¿Dónde vive la API del aula? | **decidido (A9)**: en la laptop, con Docker y Tailscale Funnel; con la laptop apagada el aula no responde (la vitrina sigue en Netlify) y el enlace no cambia. Si algún día hace falta disponibilidad continua, la misma receta Docker sube a un VPS sin cambios |
| B2 | ¿Dominio propio? Los 12 `*.netlify.app` son dominios distintos: una sesión iniciada en aequilibria no vale en optimums | un dominio propio con subdominios (`aequilibria.<dominio>`…) permite una sola sesión para los 12; sin él, se inicia sesión en cada sitio con la misma cuenta |
| B3 | ¿12.º sitio para preuniversitario y nivelación? | sí (§5); el autor elige el nombre |
| B4 | ¿Nombre del repo de la plataforma? | el autor elige; que no sea de la familia Qillqa (Qillqa, Tiqsi, Unancha) para no confundirlas |
| B5 | ¿`_site` versionado (decisión del 2026-09-22)? | con Astro, Netlify construye el sitio y solo se versionan los PDF compilados |
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
