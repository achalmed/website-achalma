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
title: Factores que influyen en el rendimiento académico de la serie 100 y 200
subtitle: Procesamiento de datos
shorttitle: "Editar"
abstract: |
  Primer parrafo de abstrac
keywords: [keyword1, keyword2]
categories:
  - Estadistica
tags:
  - Estadística

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
    - Marilin Argumedo 
    - Felix Bermudo
    - Margoth Gómez
    - Luz Guitierrez 
  pdf-url: https://achalmaedison.netlify.app/docs/blog/posts/2018-12-26-factores-influyen-rendimiento-academico/index.pdf
date: "12/26/2018"
draft: false  # Modo de borrador (false = final, true = borrador)
---












# Introducción

En el presente estudio, se busca evaluar las variables internas y externas que impactan en el rendimiento académico de los alumnos de las series 100 y 200 de la escuela de Economía. Con el fin de llevar a cabo esta evaluación, se aplicó una encuesta escrita a 174 estudiantes universitarios pertenecientes a dichas series.

Dentro de las variables evaluadas se encuentran tanto aspectos cuantitativos como cualitativos, tales como el índice académico, sexo, edad, horas de estudio, frecuencia de visita a la biblioteca, entre otros. Estas variables nos proporcionaron datos suficientes para analizar el desempeño y rendimiento académico de los estudiantes, permitiéndonos así llegar a conclusiones certeras respecto a las hipótesis planteadas.

Los resultados de esta investigación son de gran importancia para comprender los factores que influyen en el rendimiento académico de los estudiantes de las series 100 y 200, y contribuirán a la generación de estrategias y recomendaciones para mejorar dicho rendimiento.

Estudiantes

# El rendimiento académico de las series 100 y 200 (2018-II)

## Observación

### Objetivos:

El objetivo de este trabajo es evaluar el desempeño de los alumnos en relación a diversas variables, tales como sexo, serie, índice académico, número de cursos matriculados, horas de estudio, frecuencia de visita a la biblioteca y uso de redes sociales.

## Planteamiento del problema

Este trabajo se propone responder a las siguientes interrogantes:

-   ¿Cómo afecta el número de cursos matriculados al rendimiento académico?
-   ¿Cómo influyen las horas de estudio en el índice académico?
-   ¿Cuál es la proporción de rendimiento académico entre hombres y mujeres?
-   ¿Cómo se ve afectado el rendimiento académico por la frecuencia de uso de la biblioteca?
-   ¿Qué impacto tiene la frecuencia de uso de las redes sociales en el rendimiento académico?

## Hipótesis

Con el fin de analizar, comparar y evaluar las variables que influyen en el rendimiento académico, planteamos las siguientes posibles respuestas:

-   Se espera que la serie 100 presente una mayor proporción de alumnos aprobados.
-   A medida que se disminuye el número de cursos matriculados, se espera que el índice académico aprobatorio supere el 50%.
-   Se espera que a mayor cantidad de horas de estudio, exista una mayor probabilidad de obtener un mejor rendimiento académico.
-   Se presume que un menor uso de la biblioteca se asociará con una mayor probabilidad de desaprobación.
-   Se espera que las mujeres representen una proporción más alta en el rendimiento académico.

## Trabajo de campo y resultados

A continuación se presentan los datos recopilados durante el trabajo de campo y los resultados obtenidos:

- Número total de alumnos: $N = 174$
- Media poblacional: $\mu = 11.5458$
- Desviación estándar poblacional: $\sigma = 4.10$

Se realizó una muestra piloto con los primeros 20 estudiantes, de la cual se obtuvieron los siguientes datos:

- Tamaño de la muestra: $n = 20$
- Desviación estándar de la muestra: $s = 1.842081989$
- Media de la muestra: $x = 10.8185$

Utilizando los datos y considerando un nivel de confianza del 95% y un margen de error de 0.6, se determinó el tamaño necesario para una muestra representativa mediante la fórmula:

$$
n = \frac{{N \cdot Z^2 \cdot \sigma^2}}{{(N-1) \cdot e^2 + Z^2 \cdot \sigma^2}}
$$

Sustituyendo los valores en la fórmula, se obtuvo:

$$
n = \frac{{174 \cdot 1.96^2 \cdot 1.842081989^2}}{{173 \cdot 0.6^2 + 1.96^2 \cdot 1.842081989^2}}
$$

El resultado obtenido fue $n \approx 30.1158088$, lo cual indica que se requieren 30 datos aleatorios para tener una muestra representativa.

A partir de la muestra de 30 datos, se realizaron las siguientes estimaciones:

- Estimación de la media poblacional: $\hat{u} = 10.720333$
- Estimación de la desviación estándar poblacional: $\hat{\sigma} = 2.325168861$

Estas estimaciones proporcionan información sobre los valores promedio y la variabilidad de la población a partir de la muestra seleccionada.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [Estadigrafos](https://achalmaedison.netlify.app/econometria/estadistica/2018-05-16-estadigrafos) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/estadistica/2018-05-16-estadigrafos/index.pdf)
2. [Factores Que Influyen Rendimiento Academico](https://achalmaedison.netlify.app/econometria/estadistica/2018-12-26-factores-que-influyen-rendimiento-academico) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/estadistica/2018-12-26-factores-que-influyen-rendimiento-academico/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

