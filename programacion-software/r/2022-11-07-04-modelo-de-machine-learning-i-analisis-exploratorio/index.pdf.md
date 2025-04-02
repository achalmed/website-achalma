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
title: Análisis Exploratorio en Machine Learning
subtitle: Componentes Principales y Agrupamiento
shorttitle: "Análisis Expl ML"
abstract: |
  Este abstract será actualizado una vez que se complete el contenido final del artículo.
keywords: [keyword1, keyword2]
categories:
  - R
  - Machine Learning  
  - Análisis de Datos  
  - Estadística Multivariada
tags:
  - PCA  
  - Cluster Analysis  
  - K-means  
  - Hierarchical Clustering  
  - Outliers

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
  pdf-url: https://achalmaedison.netlify.app/programacion-software/r/2022-11-07-04-modelo-de-machine-learning-i-analisis-exploratorio/index.pdf
date: "11/07/2022"
draft: true  # Modo de borrador (false = final, true = borrador)
---









Este artículo está actualmente en proceso de edición, y todas las secciones serán ampliadas y refinadas en futuras revisiones.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2020-06-10-011-instalacion-de-r/index.pdf) [011 Instalacion De R](https://achalmaedison.netlify.app/programacion-software/r/2020-06-10-011-instalacion-de-r)
2. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2020-06-10-012-que-ofrece-r/index.pdf) [012 Que Ofrece R](https://achalmaedison.netlify.app/programacion-software/r/2020-06-10-012-que-ofrece-r)
3. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2020-06-10-013-lo-que-debemos-saber-de-r/index.pdf) [013 Lo Que Debemos Saber De R](https://achalmaedison.netlify.app/programacion-software/r/2020-06-10-013-lo-que-debemos-saber-de-r)
4. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2021-03-027-01-introduccion-al-programa/index.pdf) [2021 03 027 01 Introduccion Al Programa](https://achalmaedison.netlify.app/programacion-software/r/2021-03-027-01-introduccion-al-programa)
5. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2021-04-05-02-manipulacion-de-datos/index.pdf) [02 Manipulacion De Datos](https://achalmaedison.netlify.app/programacion-software/r/2021-04-05-02-manipulacion-de-datos)
6. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2021-04-12-03-visualizacion-de-datos/index.pdf) [03 Visualizacion De Datos](https://achalmaedison.netlify.app/programacion-software/r/2021-04-12-03-visualizacion-de-datos)
7. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2022-11-07-04-modelo-de-machine-learning-i-analisis-exploratorio/index.pdf) [04 Modelo De Machine Learning I Analisis Exploratorio](https://achalmaedison.netlify.app/programacion-software/r/2022-11-07-04-modelo-de-machine-learning-i-analisis-exploratorio)
8. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2022-11-14-05-modelo-de-machine-learning-ii-modelo-de-clasificacion/index.pdf) [05 Modelo De Machine Learning Ii Modelo De Clasificacion](https://achalmaedison.netlify.app/programacion-software/r/2022-11-14-05-modelo-de-machine-learning-ii-modelo-de-clasificacion)
9. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2022-11-21-06-modelo-de-machine-learning-iii-modelo-de-regresion/index.pdf) [06 Modelo De Machine Learning Iii Modelo De Regresion](https://achalmaedison.netlify.app/programacion-software/r/2022-11-21-06-modelo-de-machine-learning-iii-modelo-de-regresion)
10. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/programacion-software/r/2022-11-28-07-modelo-de-machine-learning-iv-tex-mining/index.pdf) [07 Modelo De Machine Learning Iv Tex Mining](https://achalmaedison.netlify.app/programacion-software/r/2022-11-28-07-modelo-de-machine-learning-iv-tex-mining)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

