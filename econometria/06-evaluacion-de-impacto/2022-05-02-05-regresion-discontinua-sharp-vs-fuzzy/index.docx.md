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
copyrightnotice: 2022
copyrightext: All rights reserved
# image: featured.png
title: Regresión Discontinua Sharp vs Fuzzy
subtitle: Diferencias y Similitudes
shorttitle: "Regresión Discontinua Sharp vs Fuzzy"
abstract: |
  Este abstract será actualizado una vez que se complete el contenido final del artículo.
keywords: [keyword1, keyword2]
categories:
  -  Evaluacion Impacto
  - Regresión Discontinua
  - Análisis de Datos
tags:
  - Regresión Discontinua Sharp
  - Regresión Discontinua Fuzzy
  - Supuestos de Identificación

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
  pdf-url: https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-02-05-regresion-discontinua-sharp-vs-fuzzy/index.pdf
date: "05/02/2022"
draft: true  # Modo de borrador (false = final, true = borrador)
---









Este artículo está actualmente en proceso de edición, y todas las secciones serán ampliadas y refinadas en futuras revisiones.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-04-01-introduccion-a-la-evaluacion-de-impacto/index.pdf) [01 Introduccion A La Evaluacion De Impacto](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-04-01-introduccion-a-la-evaluacion-de-impacto)
2. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-11-02-introduccion-a-los-experimentos-aleatorios/index.pdf) [02 Introduccion A Los Experimentos Aleatorios](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-11-02-introduccion-a-los-experimentos-aleatorios)
3. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-18-03-modelo-de-emparejamiento/index.pdf) [03 Modelo De Emparejamiento](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-18-03-modelo-de-emparejamiento)
4. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-25-04-regresion-discontinua-rd/index.pdf) [04 Regresion Discontinua Rd](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-04-25-04-regresion-discontinua-rd)
5. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-02-05-regresion-discontinua-sharp-vs-fuzzy/index.pdf) [05 Regresion Discontinua Sharp Vs Fuzzy](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-02-05-regresion-discontinua-sharp-vs-fuzzy)
6. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-09-06-analizando-papers-con-rdd-usando-stata-y-r/index.pdf) [06 Analizando Papers Con Rdd Usando Stata Y R](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-09-06-analizando-papers-con-rdd-usando-stata-y-r)
7. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-16-07-metodo-de-control-sintetico-mcs/index.pdf) [07 Metodo De Control Sintetico Mcs](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2022-05-16-07-metodo-de-control-sintetico-mcs)
8. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2024-03-31-por-editar/index.pdf) [Por Editar](https://achalmaedison.netlify.app/econometria/06-evaluacion-de-impacto/2024-03-31-por-editar)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

