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
copyrightnotice: 2025
copyrightext: All rights reserved
# image: featured.png
title: Editar
subtitle: Editar
shorttitle: "Editar"
abstract: |
  Descubre cómo crear tu propio sitio web estático con Blogdown, una herramienta poderosa que combina R Markdown y Hugo. Aprende a usar comandos sencillos para personalizar, construir y alojar tu sitio web de manera fácil y rápida. ¡Comienza tu proyecto web hoy mismo!
keywords: [keyword1, keyword2]
categories:
  - Iwm
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

description: '' # Texto que se muestra debajo de las etiquetas, no en la página del listado
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
  pdf-url: https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-18-personalizando-de-i3wm/index.pdf
date: "02/18/2020"
draft: true  # Modo de borrador (false = final, true = borrador)
---










1. Introducción a la personalización en i3wm
## Importancia de la personalización en un entorno de trabajo
## Ventajas de personalizar i3wm según tus preferencias

1. Configuración básica de i3wm
## Localización y estructura del archivo de configuración
## Ajustes iniciales recomendados
## Modificación de atajos de teclado y comandos

1. Temas visuales en i3wm
## Utilización de gestores de temas (theme managers)
## Cambio de colores y apariencia de la barra de estado
## Personalización de los bordes y estilos de las ventanas

1. Fondos de pantalla y lock screens
## Establecimiento de fondos de pantalla en i3wm
## Configuración de lock screens para mayor seguridad y personalización

1. Barra de estado personalizada
## Selección de barra de estado (status bar) adecuada para tus necesidades
## Configuración de información y widgets en la barra de estado
## Uso de programas externos para mostrar datos adicionales

1. Personalización avanzada con scripts y programas externos
## Automatización de tareas con scripts personalizados
## Integración de programas externos para funciones específicas

1. Gestión de ventanas mejorada
## Uso de aplicaciones externas para añadir funcionalidades
## Configuración de reglas específicas para ventanas

1. Compartir y descubrir configuraciones personalizadas
## Recursos en línea para encontrar y compartir configuraciones de i3wm
## Consideraciones al importar configuraciones de otros usuarios

1. Recursos adicionales y consejos útiles
## Herramientas y programas recomendados para la personalización en i3wm
## Comunidades y foros en línea para obtener soporte y compartir ideas



# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-15-introduccion-a-i3wm/index.pdf) [Introduccion A I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-15-introduccion-a-i3wm)
2. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-16-guia-de-instalacion-y-configuracion-de-i3wm/index.pdf) [Guia De Instalacion Y Configuracion De I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-16-guia-de-instalacion-y-configuracion-de-i3wm)
3. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-17-atajos-de-teclado-y-comandos-esenciales-de-i3wm/index.pdf) [Atajos De Teclado Y Comandos Esenciales De I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-17-atajos-de-teclado-y-comandos-esenciales-de-i3wm)
4. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-18-personalizando-de-i3wm/index.pdf) [Personalizando De I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-18-personalizando-de-i3wm)
5. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-18-trabajando-con-ventanas-en-i3wm/index.pdf) [Trabajando Con Ventanas En I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-18-trabajando-con-ventanas-en-i3wm)
6. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-19-aumenta-tu-productividad-con-i3wm/index.pdf) [Aumenta Tu Productividad Con I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-19-aumenta-tu-productividad-con-i3wm)
7. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-20-i3wm-vs-otros-gestores-de-ventanas/index.pdf) [I3wm Vs Otros Gestores De Ventanas](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-20-i3wm-vs-otros-gestores-de-ventanas)
8. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-21-integracion-de-i3wm-en-tu-entorno-de-trabajo/index.pdf) [Integracion De I3wm En Tu Entorno De Trabajo](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-21-integracion-de-i3wm-en-tu-entorno-de-trabajo)
9. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-22-casos-de-uso-avanzados-de-i3wm/index.pdf) [Casos De Uso Avanzados De I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-22-casos-de-uso-avanzados-de-i3wm)
10. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-23-solucion-de-problemas-comunes-en-i3wm/index.pdf) [Solucion De Problemas Comunes En I3wm](https://achalmaedison.netlify.app/tecnologia-seguridad/i3wm/2020-02-23-solucion-de-problemas-comunes-en-i3wm)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

