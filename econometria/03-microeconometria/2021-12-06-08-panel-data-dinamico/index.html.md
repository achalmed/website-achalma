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
copyrightnotice: 2021
copyrightext: All rights reserved
# image: featured.png
title: Modelos de Panel Data Dinámico
subtitle: Métodos de Estimación y Corrección de Sesgos en Series Temporales
shorttitle: "Panel Data Dinámico"
abstract: |
  Este abstract será actualizado una vez que se complete el contenido final del artículo.
keywords: [keyword1, keyword2]
categories:
  -  Microeconometria
  - Econometría Aplicada
  - Análisis de Datos
tags:
  - Estimación por Método Generalizado de Momentos
  - Sesgo de Nickell
  - Variables instrumentales

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
  pdf-url: https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-12-06-08-panel-data-dinamico/index.pdf
date: "12/06/2021"
draft: true  # Modo de borrador (false = final, true = borrador)
---












Este artículo está actualmente en proceso de edición, y todas las secciones serán ampliadas y refinadas en futuras revisiones.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [01 Modelos De Eleccion Discreta Probit Y Logit](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-10-18-01-modelos-de-eleccion-discreta-probit-y-logit) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-10-18-01-modelos-de-eleccion-discreta-probit-y-logit/index.pdf)
2. [02 Modelos Fraccionados](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-10-25-02-modelos-fraccionados) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-10-25-02-modelos-fraccionados/index.pdf)
3. [03 Modelos Multinomiales Y Ordenados](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-01-03-modelos-multinomiales-y-ordenados) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-01-03-modelos-multinomiales-y-ordenados/index.pdf)
4. [04 Modelos Con Variables Censuradas Y Truncadas](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-08-04-modelos-con-variables-censuradas-y-truncadas) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-08-04-modelos-con-variables-censuradas-y-truncadas/index.pdf)
5. [05 Sesgo De Seleccion](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-15-05-sesgo-de-seleccion) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-15-05-sesgo-de-seleccion/index.pdf)
6. [06 Modelos De Ecuaciones Simultaneas](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-22-06-modelos-de-ecuaciones-simultaneas) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-22-06-modelos-de-ecuaciones-simultaneas/index.pdf)
7. [07 Panel Data Estatico](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-29-07-panel-data-estatico) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-11-29-07-panel-data-estatico/index.pdf)
8. [08 Panel Data Dinamico](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-12-06-08-panel-data-dinamico) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-12-06-08-panel-data-dinamico/index.pdf)
9. [09 ](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-12-13-09-) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/03-microeconometria/2021-12-13-09-/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

