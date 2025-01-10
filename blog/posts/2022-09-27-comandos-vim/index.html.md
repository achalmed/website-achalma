---
title: Comandos básicos de Vim para mejorar tu flujo de trabajo
subtitle: Aprende a utilizar los comandos esenciales de Vim para ser más productivo en tu programación.
description: |
  En este artículo encontrarás una guía completa de los comandos básicos de Vim, uno de los editores de texto más populares en el mundo de la programación. Desde cómo abrir y cerrar archivos, hasta cómo buscar y reemplazar texto, aprenderás a utilizar Vim para mejorar tu flujo de trabajo y ser más eficiente en tu programación.
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
