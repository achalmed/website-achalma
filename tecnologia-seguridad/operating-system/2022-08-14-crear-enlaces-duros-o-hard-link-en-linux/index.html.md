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
title: Guía de Git Cómo trabajar en equipo en proyectos
subtitle: Aprende a usar Git para controlar versiones, colaborar con otros desarrolladores y mantener tu código organizado.
shorttitle: "Editar"
abstract: |
  Primer parrafo de abstrac
keywords: [keyword1, keyword2]
categories:
  - Operating System
  - GitHub
tags:
  - Git
  - GitHub
  - Colaboración
  - DesarrolloDeSoftware
  - GitBasics
  - GitAdvanced
  - GitTips
  - OpenSource

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
  pdf-url: https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-de-git-y-github/index.pdf
date: "02/16/2023"
draft: false  # Modo de borrador (false = final, true = borrador)
---









## Cómo Crear un Enlace Duro (Hard Link) en Linux

## Introducción

Los **enlaces duros o hard link** asocian dos o más ficheros compartiendo el mismo **inodo**, esto hace que cada **enlace duro** sea una copia exacta del resto de los ficheros enlazados, tanto en los datos como en los permisos, propietario, grupo, etc. Cuando se modifica uno de los enlaces o el fichero original, los cambios afectan al resto de los enlaces.

> **Nota:** Los **enlaces duros** no pueden hacerse contra directorios y tampoco fuera del propio sistema de ficheros.

En sistemas linux también existen los enlaces simbolicos, también conocidos como **enlaces blandos** o **Symlinks**. 

## Características principales de los enlaces duros

- Solo se pueden hacer entre ficheros. No se pueden hacer entre directorios.
- No se pueden hacer entre distintos sistemas de ficheros.
- Comparten el número de inodo
- Si se borra el fichero original la información no se pierde.
- Son copias exactas del fichero original. Los cambios aplicados a uno de ellos o al fichero original, afectan a todos.

## Creando un enlace duro (hard link)

La sintaxis genérica para crear un **enlace duro** es la siguiente:

```bash
ln TARGET LINK_NAME
```

- **TARGET**: Nombre del archivo existente al que le crearemos el **enlace duro**.
- **LINK_NAME**: Nombre del **enlace duro**.

Veamos un ejemplo:

```bash
ln test.txt enlace-duro-a-test.txt
```

Si listamos ambos archivos con el comando `ls -li`, 

```bash
ls -li
```

Observamos que ambos comparten el mismo inodo
```bash
786433 -rw-r--r-- 2 achalma achalma 0 jun 21 21:27 enlace-duro-a-test.txt
786433 -rw-r--r-- 2 achalma achalma 0 jun 21 21:27 test.txt
```

Se observa en la primera columna que ambos, archivo y enlace, comparten el mismo número de inodo (**786433**). La tercera columna indica cuantos **enlaces duros** tiene el fichero, en este caso **2**, el archivo original más el enlace.

Si modificamos uno de ellos, los cambios afectan a todos. Por ejemplo, vamos a conceder permiso de ejecución al propietario en el archivo `test.txt` y veamos que pasa con el enlace:

```bash
chmod u+x test.txt
```

Si volvemos a listar ambos archivos vemos que el cambio ha afectado a ambos, al fichero original y al enlace:

```bash
$ ls -li
786433 -rwxr--r-- 2 achalma achalma 0 jun 21 21:27 enlace-duro-a-test.txt
786433 -rwxr--r-- 2 achalma achalma 0 jun 21 21:27 test.txt
```

Si editásemos el archivo o el enlace, los cambios realizados en el contenido afectarían a ambos.
## Generar varios

Para crear 35 enlaces duros de `_metadata.yml` puedes usar un simple bucle `for` en la terminal de Linux:

```bash
for i in {1..35}; do ln _metadata.yml "_metadata$i.yml"; done
```

Este comando hace lo siguiente:

1. `for i in {1..35}`: Esto establece un bucle que itera desde 1 hasta 35.
2. `ln _metadata.yml "_metadata$i.yml"`: Dentro del bucle, se ejecuta el comando `ln` para crear un enlace duro de `_metadata.yml` con el nombre `_metadataX.yml`, donde `X` es el valor actual de `i` en el bucle.

Finalmente, se generarán los 35 enlaces duros.



# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2017-05-21-comandos-de-informacion-windows/index.pdf) [Comandos De Informacion Windows](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2017-05-21-comandos-de-informacion-windows)
2. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2019-06-19-adb/index.pdf) [Adb](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2019-06-19-adb)
3. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-08-17-limpieza-y-optimizacion-de-pc/index.pdf) [Limpieza Y Optimizacion De Pc](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-08-17-limpieza-y-optimizacion-de-pc)
4. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11/index.pdf) [Usando Apk En Windown 11](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11)
5. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-05-12-gestionar-versiones-de-jdk-en-kubuntu/index.pdf) [Gestionar Versiones De Jdk En Kubuntu](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-05-12-gestionar-versiones-de-jdk-en-kubuntu)
6. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-07-21-instalar-tor-browser/index.pdf) [Instalar Tor Browser](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-07-21-instalar-tor-browser)
7. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-08-14-crear-enlaces-duros-o-hard-link-en-linux/index.pdf) [Crear Enlaces Duros O Hard Link En Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-08-14-crear-enlaces-duros-o-hard-link-en-linux)
8. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim/index.pdf) [Comandos Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim)
9. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-de-git-y-github/index.pdf) [Guia De Git Y Github](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-de-git-y-github)
10. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux/index.pdf) [00 Primeros Pasos En Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux)
11. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux/index.pdf) [01 Introduccion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux)
12. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux/index.pdf) [02 Distribuciones Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux)
13. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux/index.pdf) [03 Instalacion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux)
14. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes/index.pdf) [04 Administracion Particiones Volumenes](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes)
15. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim/index.pdf) [Atajos De Teclado Y Comandos Para Usar Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim)
16. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2024-07-15-instalando-specitify/index.pdf) [Instalando Specitify](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2024-07-15-instalando-specitify)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

