---
tipo: doc
forma: explicacion
titulo: "Diagnóstico de la web, los pubs, docencia, simuladores y divulgación (2026-10-20)"
estado: hecho
---
# Diagnóstico de la plataforma educativa (instantánea del 2026-10-20)

> Foto en solo lectura que fundó `../plataforma-educativa.md`; no se corrige: lo vigente está allí y en `../decisiones.md`.


### 1 La web hoy (`web`, repo `website-achalma`)

| sección | fuentes | observación |
|---|---|---|
| Inicio, About, Contact, Appointment | 4 `.qmd` | presentación estática; la portada no muestra lo que el autor hace |
| Cursos | 70 `.qmd` y 30 `.md`, 100 MB | 31 fichas, 8 en `draft`; 22 con sílabo generado desde `curso.yml`; solo Metodología (2025-1, 2026-1) y `pre_economia` tienen sesiones |
| Publications, Datos (observatorio de `datafw`), Blog (6 posts) | — | funcionan; el observatorio es un archivo autocontenido generado |
| «More» | 11 enlaces | los pubs, cada uno en su dominio |

La identidad es el design system «Quiet Laboratory» (`assets/scss/`, tokens `$lab-*`): papel `#FBFBF8`, tinta `#101820`, azul `#0F5CA8`,
verde `#2F7D5D` y rótulos en monoespaciada. Es sobria y coherente, y se conserva. Su debilidad es la experiencia: tarjetas grises sin
imagen ni progreso y nada interactivo en la portada.

### 2 Los 11 pubs (985 MB)

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

### 3 `docencia`

Tiene el modelo de datos que la plataforma necesita:

- **`curso.yml`:** unidades, temas con `archivo` y `recursos`, `bibliografia[].calibre_id`, `datasets[].clave`, `banco_examenes`, `tipo`, `area`.
- **Sesiones y dictados:** sesiones tipadas (`clase`, `laboratorio`, `taller`, `evaluacion`) y `dictado.yml` por cada edición real.
- **Volumen:** 52 cursos, 303 unidades, 1 952 temas, **muy pocas notas escritas** (casi todas en `python/02-contenido`), 67 sesiones y unos 850 `.tex` de evaluación.
- **Marcos LaTeX propios:**
  - `classes/` (`academic-base`, `academic-exam`, `academic-report`, `academic-beamer`);
  - `docencia/themes/academic` (Beamer);
  - `templates/` (12 tipos de examen, 8 de presentación, 4 de informe);
  - `docencia/scaffolds/sesion/` (`deck.tex` Beamer y `deck.qmd` reveal.js).

Hechos que deciden dónde va cada cosa:

- **Visibilidad.** `docencia` (`CampusTeX-Research`) es **público**. Su contenido (`contenido/`, `Academic_Class`) es **privado** y guarda los exámenes con
  sus claves. Los 11 pubs son **públicos**. Ninguna clave ni examen inédito puede pasar a un pub.
- **Lo sensible.** `docencia/registro` (estudiantes y notas) es sensible (regla 8) y no se toca.
- **Diapositivas.** Las de clase **no dependen de `escritura`**. `docencia` tiene su Beamer y su reveal.js; `escritura` tiene `lamina.cls` y
  `presentacion.cls` para defensas, ponencias y conferencias, y `docencia` solo toma de ella el esquema del guion. Son dos marcos con funciones
  distintas. Ambos usan la capa de diseño `sistema-editorial` (§2.7).
- **Rutas.** `temario.py`, `enlazar.py` y `publicar-web.py` deducen `~/Documents` en lugar de usar `core/env.py` (N 5.1).

### 4 Duplicaciones

| tema | dónde aparece hoy | casa única |
|---|---|---|
| Metodología, APA, monografías | `sistema-apa`, `monografias/s03`, web 2025-1 y 2026-1, 7 posts de methodica | currículo en `docencia`; lecciones y ediciones en **methodica** |
| Python | notas de `python/02-contenido`, 14 posts, ficha web | currículo en `docencia`; esas notas pasan a **numerus-scriptum** y se funden con sus 14 posts tema por tema |
| Excel y Power BI | 20 talleres en `docencia`, 20 posts, ficha | currículo en `docencia`; lecciones en **numerus-scriptum** |
| Econometría | `econometria-i/ii`, `-con-python`, `-r-y-python`, 50 páginas de epsilon-y-beta, ficha | currículo en `docencia` (los temas que solo están en el pub entran en `curso.yml`); lecciones en **epsilon-y-beta** |
| Macro y micro | `curso.yml`, series de aequilibria y optimums | ídem, en **aequilibria** y **optimums** |
| Solo en la web | álgebra lineal, cálculo, optimización, SQL, Power BI, preuniversitarias | alta en `curso.yml` (o mapeo a `matematicas-i/ii/iii`) antes de migrar |

### 5 `simuladores` (hoy `docencia/simuladores`, 5,5 MB)

- **Modelos:** 115 de macro en 12 niveles y 23 de estadística, más animaciones Manim. Cada uno es un `base.Modelo` con su `Ficha`, que lleva las fuentes verificadas contra el PDF de Calibre.
- **Dependencias:** los modelos usan **solo `numpy`**; matplotlib está únicamente en la aplicación de escritorio. Por eso pueden correr en el navegador con Pyodide sin
  reescribirse. El nivel 12 lee series del BCRP desde `datafw` (`DATAFW_DIR`) y tiene un snapshot de respaldo.
- **Consumidores:** `docencia` (29 recursos `tipo: simulador`) y `divulgacion` (`divulgacion/lib/simuladores.py`, que usa `m.verificaciones` y las curvas).

### 6 `divulgacion`

Es un estudio de producción de vídeo corto (9 piezas en borrador, Manim, canal «achalmaedison»), **no un archivo de documentos**:

- lee simuladores, `datafw`, Calibre y los `curso.yml`;
- cada pieza declara `curriculo: [{curso, tema}]`;
- deja sus productos en `$VIDEOS_DIR/divulgacion/`;
- todavía no publica nada.

Sigue independiente. Lo que falta es el «enlace de vuelta»: un catálogo que los pubs leen para mostrar el vídeo en la lección de su tema.

### 7 Los marcos LaTeX y su capa de diseño

| proyecto | qué es | ejemplo |
|---|---|---|
| `sistema-editorial` | **capa de diseño**, no un marco: tipografías, colores y maquetas en YAML que generan `.tex` de configuración | `sistema-editorial/temas/docencia.yml` → `docencia/config/palette.tex` |
| `docencia/classes` | marco de **docencia**: exámenes, sílabos, rúbricas, decks Beamer | `academic-exam` |
| `escritura/classes` | marco de **producción académica**: tesis, artículos, informes, láminas de exposición | `lamina.cls` |
| `marco_documental` (en `sgdp`) | marco de **documentos oficiales** del despacho | oficios, informes |

Son tres marcos de clases, uno por dominio, que comparten una misma capa de diseño. La plataforma no los cambia: publica sus PDF.

### 8 El uso real de Quarto y el costo del render

Tiempos del render completo (registro de la ola 6): pubs 2 800 s y hub entre 320 y 530 s, unos **47 min** en total. Casi no hay código que ejecutar, así que el
tiempo se va en apaquarto: **un PDF con LuaLaTeX y un DOCX por cada post en cada render**, en 12 proyectos.
