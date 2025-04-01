---
# documentmode: jou  # Modo de documento: Can be jou (journal), man (manuscript), stu (student), or doc (document)
# - man (Manuscrito): Similar al formato .docx
# - jou (Revista): Un formato pulido de dos columnas similar a muchas revistas APA.
# - doc (Documento): Similar al predeterminado LaTex artículos.
# - stu (Estudiante): Formateado para trabajos de estudiantes
# MODO ESTUDIANTE (STU)
# course: Metodología (EDUC 5101)
# professor: Dr. Edison Achalma Mendoza
# duedate: 01/23/2022
# MODO REVISTA (JOU)
# journal: The American Economic Review # Econometrica, The American Economic Review, Revista de Economía, Revista de la CEPAL
# volume: 2025, Vol. 131, No. 2, 10--60
copyrightnotice: 2023
copyrightext: All rights reserved
# image: featured.png
title: Editar
subtitle: Editar
shorttitle: "Editar"
abstract: |
  Este abstract será actualizado una vez que se complete el contenido final del artículo.
keywords: [keyword1, keyword2]
categories:
  - Ofimatica
  - Blogdown
  - Desarrollo Web
  - Herramientas para R
tags:
  - RStudio
  - Blogdown
  - Comandos
  - DesarrolloWeb

# Nota del Autor
author-note:
  status-changes:
    # Ejemplo: [Nombre del autor] está ahora en [afiliación].
    affiliation-change: ~
    # Ejemplo: [Nombre del autor] ha fallecido.
    deceased: ~
  # Las divulgaciones se condensan en un párrafo, pero puede iniciar un campo con dos saltos de línea para separarlas: \n\nNew
  disclosures:
    # Ejemplo: Este estudio se registró en X (Identificador Y).
    study-registration: ~
    # Reconozca y cite los datos/materiales que se van a compartir.
    data-sharing: ~
    # Ejemplo: Este artículo se basa en datos publicados en [Referencia].
    # Ejemplo: Este artículo se basa en la disertación realizada por [cita].
    related-report: ~
    # Ejemplo: [Nombre del autor] ha sido consultor remunerado de la Corporación X, que ha financiado este estudio.
    conflict-of-interest: El autor no tiene conflictos de interés que revelar.
    # Ejemplo: Este estudio ha contado con el apoyo de la subvención [Número de subvención] de [Fuente de financiación].
    financial-support: ~
    # Ejemplo: Los autores agradecen a [Persona] por [Motivo].
    gratitude: ~
    # Ejemplo. Dado que los autores contribuyen por igual, el orden de autoría se determinó mediante el lanzamiento de una moneda al aire.
    authorship-agreements: ~

description: "" # Texto que se muestra debajo de las etiquetas, no en la página del listado
# links:
# - icon: pin-map-fill
#   name: Collection of maps
#   url: /project/2024-06-16-ccd-sips #./../talk/2021-03-16-xaringan-deploy-demo/
# - icon: github
#   icon_pack: fab
#   name: R-Ladies template files
#   url: https://github.com/spcanelon/RLadies-xaringan-template
eval: false # true(predeterminado): evaluar celda de código, false: no evaluar la celda de código
# Google Scholar
# bibliography: mybibliography.bib
citation:
  type: article-journal
  author:
    - Edison Achalma
  pdf-url: https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2024-03-31-por-editar/index.pdf
date: "03/31/2024"
draft: true # Modo de borrador (false = final, true = borrador)
---












# Anchor

En LibreOffice, el "anchor" (ancla en español) de una figura se refiere al punto de referencia que determina cómo y dónde se posicionará la figura dentro del documento. Aquí te explico los tipos de anclaje disponibles y cómo afectan la disposición de tu figura:

1.  **Ancla a Párrafo (To Paragraph)**: La figura está vinculada a un párrafo específico. Si mueves el párrafo, la figura se mueve con él. Sin embargo, la posición exacta de la figura dentro del párrafo puede ajustarse manualmente.

2.  **Ancla a Carácter (To Character)**: La figura se ancla a un carácter específico dentro del texto. Esto significa que si el texto se mueve o cambia, la figura se ajustará según la posición de ese carácter.

3.  **Ancla a Página (To Page)**: La figura se fija a una posición absoluta en la página. No importa cómo se modifique el texto alrededor, la figura permanecerá en el mismo lugar de la página. Esto es útil para encabezados, pies de página, o imágenes que deben estar en una posición fija.

4.  **Ancla a Trama (To Frame)**: Si estás usando marcos (frames), puedes anclar la figura a un marco específico. La figura entonces se moverá y ajustará con el marco.

5.  **Ancla a Carácter (como una Imagen en Línea)**: Aunque es similar a "To Character", aquí la imagen actúa más como un carácter del texto, fluyendo con el texto como si fuera una letra o símbolo.

## "To Character" y "As Character"

En LibreOffice, "To Character" y "As Character" son dos formas distintas de anclar imágenes o figuras, y cada una tiene su propia manera de interactuar con el texto:

- **To Character**:

  - **Posición**: La imagen se ancla a un carácter específico en el texto, pero no actúa como un carácter. Esto significa que la imagen se posicionará cerca del carácter al que está anclada, pero no necesariamente justo en línea con el texto.

  - **Comportamiento**: Si mueves el carácter al que está anclada la imagen, la imagen se moverá con él. Sin embargo, la imagen puede estar posicionada fuera de la línea de texto, como flotando cerca de donde está el carácter.

  - **Uso**: Es útil cuando quieres que una imagen se mueva con una parte específica del texto pero no necesariamente dentro del flujo del texto.

- **As Character**:

  - **Posición**: La imagen o figura se inserta en el texto como si fuera un carácter adicional. Esto significa que se comporta exactamente como cualquier otra letra o símbolo en el documento.

  - **Comportamiento**: La imagen se alinea dentro de la línea de texto, respetando el espaciado y el formato de párrafo. Si el texto alrededor cambia, la imagen se moverá y fluirá con el texto, justo como lo haría una letra.

  - **Uso**: Es ideal para imágenes pequeñas que deben tratarse como parte del texto, como íconos, emoji o imágenes en línea que no deben interrumpir el flujo del texto.

**Diferencias Clave**:

- **Interacción con el Texto**: "As Character" inserta la imagen directamente en el flujo del texto, mientras que "To Character" ancla la imagen al texto pero permite un posicionamiento más libre fuera del flujo directo del texto.

- **Flexibilidad de Posición**: "To Character" ofrece más control sobre la posición exacta de la imagen en relación con el carácter ancla, mientras que "As Character" sigue las reglas de formato del texto.

- **Ajuste al Texto**: Con "As Character", cualquier cambio en el texto alrededor de la imagen (como rellenar, espaciado, etc.) afectará a la imagen como si fuera un carácter más. Con "To Character", la imagen puede moverse con el texto pero no se ajusta exactamente como un carácter dentro del mismo.

# Wrap

En LibreOffice, "wrap" (envoltura en español) se refiere a cómo el texto fluye alrededor de una imagen o figura. Aquí te explico las opciones de envoltura disponibles y cómo afectan la disposición del texto y la imagen en tu documento:

Tipos de Envoltura (Wrap):

1.  **None (Sin Envoltura)**:

    - El texto no fluye alrededor de la imagen. La imagen actúa como si fuera un bloque de texto, empujando el texto hacia abajo o hacia arriba dependiendo de su posición.

2.  **Before (Antes)**:

    - El texto solo fluye a la izquierda de la imagen, dejando la parte derecha libre.

3.  **After (Después)**:

    - El texto solo fluye a la derecha de la imagen, dejando la parte izquierda sin texto.

4.  **Parallel (Paralelo)**:

    - El texto fluye tanto a la izquierda como a la derecha de la imagen, creando columnas de texto a ambos lados.

5.  **Through (A través)**:

    - El texto fluye a través de la imagen como si no estuviera ahí. Esta opción es menos común y se usa cuando la imagen tiene áreas transparentes o cuando quieres que el texto pase por encima de la imagen.

6.  **Optimal (Óptimo)**:

    - LibreOffice decide automáticamente la mejor forma de envolver el texto alrededor de la imagen basándose en la forma de la imagen y el espacio disponible.

Ajustes Adicionales:

- **Contorno (Contour)**:

  - Permite que el texto siga el contorno de la imagen, en lugar de simplemente envolverla en una caja rectangular. Esto se puede ajustar manualmente para obtener un envoltorio más preciso.

- **Espaciado**:

  - Puedes ajustar el espacio entre el texto y la imagen en todas direcciones (arriba, abajo, izquierda, derecha) para controlar mejor cómo se ve la envoltura.

- Para ajustes más detallados, como el contorno o el espaciado, puedes acceder a las propiedades de la imagen a través del panel lateral de LibreOffice o mediante el diálogo de propiedades que aparece al hacer clic derecho en la imagen y seleccionar "Propiedades".

# Align Objects

En LibreOffice, "Align Objects" (Alinear Objetos) es una función que te permite organizar y posicionar varias figuras, imágenes, formas, o cualquier objeto gráfico en relación entre sí o con respecto a la página. Aquí te explico cómo funciona y las opciones disponibles:

Aliniación de Objetos:

**Opciones de Alineación**:

- **Horizontal**:

  - **Izquierda (Left)**: Alinea los objetos por su borde izquierdo.

  - **Centro (Center)**: Alinea los objetos por su centro horizontal.

  - **Derecha (Right)**: Alinea los objetos por su borde derecho.

- **Vertical**:

  - **Arriba (Top)**: Alinea los objetos por su borde superior.

  - **Centro (Center)**: Alinea los objetos por su centro vertical.

  - **Abajo (Bottom)**: Alinea los objetos por su borde inferior.

**Distribución**:

Además de la alineación, también puedes distribuir objetos para que el espacio entre ellos sea uniforme:

- **Horizontal**: Distribuye objetos uniformemente a lo largo del eje horizontal.

- **Vertical**: Distribuye objetos uniformemente a lo largo del eje vertical.

Consideraciones:

- **Anclaje**: La alineación puede verse afectada por cómo están anclados los objetos (a párrafo, carácter, página, etc.). Asegúrate de que el anclaje no interfiera con la alineación deseada.

- **Grupos**: Si los objetos están agrupados, la alineación se aplicará al grupo como si fuera un solo objeto.

- **Ajuste Manual**: A veces, después de usar la alineación automática, podrías querer hacer ajustes manuales para el posicionamiento exacto de los objetos.

# Arrange

En LibreOffice, "Arrange" (Organizar en español) se refiere a las funciones que te permiten controlar el orden de apilamiento de objetos gráficos como imágenes, formas, líneas, etc., en una página. Aquí está cómo funciona y las opciones disponibles:

Opciones de Organización:

1.  **Bring to Front (Traer al Frente)**:

    - Coloca el objeto seleccionado por encima de todos los demás objetos. Es útil cuando quieres que un objeto sea visible por completo sin estar cubierto por otros.

2.  **Bring Forward (Traer hacia Adelante)**:

    - Mueve el objeto seleccionado una posición hacia adelante en el orden de apilamiento. Si hay varios objetos, este comando moverá el objeto uno nivel por encima de su posición actual.

3.  **Send to Back (Enviar al Fondo)**:

    - Coloca el objeto seleccionado detrás de todos los demás objetos. Esto es útil cuando necesitas que un objeto esté por debajo de otros sin interferir visualmente.

4.  **Send Backward (Enviar hacia Atrás)**:

    - Mueve el objeto seleccionado una posición hacia atrás en el orden de apilamiento. Así como "Bring Forward" mueve hacia adelante una posición, esta opción hace lo contrario.

Consideraciones:

- **Visibilidad**: El orden de apilamiento afecta cómo los objetos se superponen y, por tanto, qué partes de los objetos son visibles. Un objeto en la parte superior puede ocultar porciones de objetos que están "más abajo" en el orden de apilamiento.

- **Grupos**: Si los objetos están agrupados, cualquier operación de organización se aplicará a todo el grupo como una sola unidad.

- **Interacción con el Texto**: La organización de objetos también puede cambiar cómo estos interactúan con el texto, especialmente si los objetos están anclados a diferentes elementos del documento.

- **Capas**: Aunque LibreOffice no tiene un sistema de capas como en programas de diseño gráfico avanzado, las funciones de organizar sirven para manejar una pseudo-capas a través del orden de apilamiento.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [01 Introduccion Al Lenguaje Y Editor Vba](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-05-01-introduccion-al-lenguaje-y-editor-vba) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-05-01-introduccion-al-lenguaje-y-editor-vba/index.pdf)
2. [02 Grabar Y Modificar](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-12-02-grabar-y-modificar) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-12-02-grabar-y-modificar/index.pdf)
3. [03 Procedimientos](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-19-03-procedimientos) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-19-03-procedimientos/index.pdf)
4. [04 Funciones En Vba](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-26-04-funciones-en-vba) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-26-04-funciones-en-vba/index.pdf)
5. [05 Funciones Condicionales Estructuras Condicionales](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-02-05-funciones-condicionales-estructuras-condicionales) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-02-05-funciones-condicionales-estructuras-condicionales/index.pdf)
6. [06 Funciones Iterativas Estructuras Repetitivas O Bucles](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-09-06-funciones-iterativas-estructuras-repetitivas-o-bucles) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-09-06-funciones-iterativas-estructuras-repetitivas-o-bucles/index.pdf)
7. [07 Formularios](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-16-07-formularios) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-16-07-formularios/index.pdf)
8. [08 Eventos](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-23-08-eventos) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-23-08-eventos/index.pdf)
9. [Combinando Hojas De Excel Con Vba](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-05-31-combinando-hojas-de-excel-con-vba) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-05-31-combinando-hojas-de-excel-con-vba/index.pdf)
10. [Por Editar](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2024-03-31-por-editar) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2024-03-31-por-editar/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

