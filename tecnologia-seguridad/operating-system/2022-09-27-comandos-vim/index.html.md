---
title: Comandos básicos de Vim para mejorar tu flujo de trabajo
subtitle: Aprende a utilizar los comandos esenciales de Vim para ser más productivo en tu programación.
shorttitle: "Editar"
description: |
  Accede al [PDF](https://achalmaedison.netlify.app/blog/posts/2021-07-14-comandos-blogdown/index.pdf) completo aquí. Actualizar enlace
abstract: |
  | Primer parrafo de abstrac
keywords: [keyword1, keyword2]
categories:
  - Programación
tags:
  - Vim
  - EditorDeTexto
  - Comandos
  - Programación
citation:
  pdf-url: https://achalmaedison.netlify.app/docs/blog/posts/2022-09-27-comandos-vim/index.pdf
date: "09/27/2022"
draft: false  # Modo de borrador (false = final, true = borrador)
---





Vim es un editor de texto muy poderoso utilizado en sistemas Linux y Unix. A continuación, se presentan algunos de los comandos y combinaciones de teclas más utilizados en Vim:

1. Modos de Vim:

    - Modo de comandos: el modo predeterminado de Vim, en el que se pueden ingresar comandos para editar el texto. Para activar el modo comando en Vim, debes presionar la tecla "Esc". Esto te llevará al modo comando desde cualquier otro modo en el que te encuentres, como el modo insertar o el modo de reemplazo. Una vez que estés en el modo comando, puedes utilizar una variedad de comandos y combinaciones de teclas para navegar, editar y guardar tus archivos. Para salir de Vim, puedes ingresar el comando ":q" seguido de Enter. Si has realizado cambios y deseas guardarlos antes de salir, utiliza el comando ":wq" para escribir y guardar los cambios y salir de Vim.

    - Modo de inserción: el modo en el que se puede ingresar texto normal.
    - Modo de visualización: el modo utilizado para seleccionar y manipular bloques de texto.
2. Comandos de movimiento de cursor:

    - h: mueve el cursor una posición a la izquierda.
    - j: mueve el cursor una posición hacia abajo.
    - k: mueve el cursor una posición hacia arriba.
    - l: mueve el cursor una posición a la derecha.
    - 0: mueve el cursor al inicio de la línea.
    - $: mueve el cursor al final de la línea.
    - w: mueve el cursor a la siguiente palabra.
    - b: mueve el cursor a la palabra anterior.
    - gg: mueve el cursor al inicio del archivo.
    - G: mueve el cursor al final del archivo.
    - :numero: mueve el cursor a la línea con el número especificado.
3. Comandos de edición:

    - i: entra en el modo de inserción antes del cursor.
    - a: entra en el modo de inserción después del cursor.
    - o: inserta una nueva línea debajo del cursor y entra en el modo de inserción.
    - d: elimina el texto seleccionado.
    - y: copia el texto seleccionado.
    - p: pega el texto copiado o eliminado después del cursor.
    - u: deshace la última acción.
    - Ctrl+r: rehace la última acción.
    - :w: guarda el archivo.
    - :q: sale de Vim.
    - :q!: sale de Vim sin guardar los cambios.
4. Comandos de búsqueda y reemplazo:

    - /: busca el texto especificado hacia adelante.
    - ?: busca el texto especificado hacia atrás.
    - n: busca la siguiente ocurrencia del texto especificado.
    - N: busca la ocurrencia anterior del texto especificado.
    - :s/old/new/g: reemplaza la primera ocurrencia de "old" con "new" en la línea actual.
    - :s/old/new/gc: reemplaza todas las ocurrencias de "old" con "new" en la línea actual y pide confirmación antes de cada reemplazo.

Estos son solo algunos de los comandos y combinaciones de teclas más utilizados en Vim. Hay muchos más disponibles, y la lista completa se puede encontrar en la documentación de Vim.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [Usando Apk En Windown 11](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11/index.pdf)
2. [Comandos Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim/index.pdf)
3. [Guia Git](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-git) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-git/index.pdf)
4. [00 Primeros Pasos En Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux/index.pdf)
5. [01 Introduccion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux/index.pdf)
6. [02 Distribuciones Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux/index.pdf)
7. [03 Instalacion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux/index.pdf)
8. [04 Administracion Particiones Volumenes](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes/index.pdf)
9. [Atajos De Teclado Y Comandos Para Usar Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

