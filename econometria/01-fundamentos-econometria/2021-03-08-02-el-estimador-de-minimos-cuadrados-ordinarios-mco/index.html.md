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
# journal: Psychological Review
# volume: 2025, Vol. 131, No. 2, 10--60
copyrightnotice: 2021
copyrightext: All rights reserved
# image: featured.png
title: Estimador de Mínimos Cuadrados Ordinarios
subtitle: Métodos y Aplicaciones
shorttitle: "Estimador MCO"
abstract: |
  Este abstract será actualizado una vez que se complete el contenido final del artículo.
keywords: [keyword1, keyword2]
categories:
  -  Fundamentos Econometria
  - Econometría  
  - Métodos Estadísticos
tags:
  - Mínimos Cuadrados  
  - Estimación Paramétrica  
  - Análisis de Datos

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
  pdf-url: https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-08-02-el-estimador-de-minimos-cuadrados-ordinarios-mco/index.pdf
date: "03/08/2021"
draft: true  # Modo de borrador (false = final, true = borrador)
---












Este artículo está actualmente en proceso de edición, y todas las secciones serán ampliadas y refinadas en futuras revisiones.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [01 Modelo Clasico De Regresion Lineal](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-01-01-modelo-clasico-de-regresion-lineal) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-01-01-modelo-clasico-de-regresion-lineal/index.pdf)
2. [02 El Estimador De Minimos Cuadrados Ordinarios Mco](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-08-02-el-estimador-de-minimos-cuadrados-ordinarios-mco) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-08-02-el-estimador-de-minimos-cuadrados-ordinarios-mco/index.pdf)
3. [03 Algebra Y Geometria De Mco](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-15-03-algebra-y-geometria-de-mco) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-15-03-algebra-y-geometria-de-mco/index.pdf)
4. [04 Propiedades En Muestras Finitas Del Estimador Mco](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-22-04-propiedades-en-muestras-finitas-del-estimador-mco) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-22-04-propiedades-en-muestras-finitas-del-estimador-mco/index.pdf)
5. [05 Propiedades En Muestras Infinitas Del Estimador Mco](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-29-05-propiedades-en-muestras-infinitas-del-estimador-mco) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-03-29-05-propiedades-en-muestras-infinitas-del-estimador-mco/index.pdf)
6. [06 El Trade Off Sesgo Varianza](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-04-10-06-el-trade-off-sesgo-varianza) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-04-10-06-el-trade-off-sesgo-varianza/index.pdf)
7. [07 Bondad De Ajuste](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-04-19-07-bondad-de-ajuste) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-04-19-07-bondad-de-ajuste/index.pdf)
8. [08 Multicolinealidad](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-04-26-08-multicolinealidad) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-04-26-08-multicolinealidad/index.pdf)
9. [09 Inferencia](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-03-09-inferencia) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-03-09-inferencia/index.pdf)
10. [10 El Modelo General De Regresion Lineal Permitiendo Heterocedasticidad En Los Errores](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-10-10-el-modelo-general-de-regresion-lineal-permitiendo-heterocedasticidad-en-los-errores) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-10-10-el-modelo-general-de-regresion-lineal-permitiendo-heterocedasticidad-en-los-errores/index.pdf)
11. [11 Problemas De Endogeneidad](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-17-11-problemas-de-endogeneidad) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-17-11-problemas-de-endogeneidad/index.pdf)
12. [12 Perturbaciones No Esfericas](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-24-12-perturbaciones-no-esfericas) Lee sin conexión [PDF](https://achalmaedison.netlify.app/econometria/01-fundamentos-econometria/2021-05-24-12-perturbaciones-no-esfericas/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

