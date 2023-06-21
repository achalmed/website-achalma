---
title: Lo que debemos saber de R
subtitle: Explorando las capacidades de R y su uso en el entorno Linux
description: |
  Descubre cómo comenzar con R en el sistema operativo Linux, desde la descarga e instalación hasta la manipulación de datos para análisis. Aprende sobre las funcionalidades y ventajas que ofrece este software en el entorno Linux.
categories:
  - R
  - RStudio
tags:
  - R
  - RStudio
  - Linux
  - Manipulación-de-Datos
  - Análisis-de-Datos
citation:
  pdf-url: https://achalmaedison.netlify.app/docs/blog/posts/2023-06-10-3-debemos-saber-r/index.pdf
date: "06/11/2023"
---




# Lo que debemos saber

## Tipos de datos

En R, es fundamental comprender los diferentes tipos de datos disponibles. A continuación, exploraremos los tres tipos básicos de datos en R y cómo se utilizan en la programación.

### 1. Tipos de datos numéricos

Los datos numéricos en R se dividen en dos tipos principales:

a.  Números reales, se conoce como `double`. Estos son los números más comunes y se utilizan para representar valores decimales. Por ejemplo, 3.14 y 2.71828 son números reales en R. La precisión de los números reales en R depende de la máquina en la que se ejecuta el programa.

b.  Números enteros, se conoce como `integer`. Estos son números que no contienen decimales y se utilizan para representar valores enteros. Por ejemplo, 1, 2, -5 son ejemplos de números enteros en R. Los números enteros se utilizan cuando no se requiere precisión decimal.

### 2. Tipo de datos lógico

El tipo de dato lógico en R se conoce como `booleano`. Este tipo de dato puede tener uno de dos valores: TRUE o FALSE. Los valores booleanos se utilizan principalmente para realizar operaciones de comparación y evaluación lógica en los programas. Por ejemplo, se puede usar una expresión lógica para verificar si una condición es verdadera o falsa.

### 3. Tipo de datos carácter

El tipo de dato carácter en R se utiliza para almacenar letras `text` y símbolos `strings`. Los datos de tipo carácter se definen utilizando comillas simples ('') o comillas dobles (""). Por ejemplo,"Hola" y 'RStudio' son ejemplos de datos de tipo carácter en R. Los datos de tipo carácter se utilizan con frecuencia para almacenar texto legible por humanos, como nombres, descripciones o mensajes.

> Es importante comprender estos tipos de datos en R, ya que nos permiten manipular y realizar operaciones en los datos de manera adecuada. Cada tipo de dato tiene sus propias características y funciones asociadas que nos permiten realizar tareas específicas en la programación.

## Estructura de datos

Las estructuras de datos nos permiten organizar y manipular la información de manera eficiente. A continuación, exploraremos las principales estructuras de datos disponibles en R y cómo se utilizan en la programación.

### 1. Escalar

Un escalar es un dato individual, como un número o una palabra, que no está agrupado con otros elementos. En R, los escalares pueden ser de diferentes tipos de datos, como numéricos, lógicos o caracteres. Estos datos se utilizan cuando solo necesitamos almacenar una única observación.

### 2. Vector

Un vector es una colección ordenada de elementos del mismo tipo de dato. Puede contener números, valores lógicos o caracteres. En R, los vectores son utilizados para almacenar conjuntos de datos relacionados. Por ejemplo, podemos tener un vector de edades o un vector de nombres. Los vectores son una de las estructuras de datos más utilizadas en R y nos permiten realizar operaciones y cálculos de manera eficiente.

**Vectores**

Concatenación de elementos con **`c()`**: Se utiliza la función `c()` para concatenar elementos y crear vectores en R.



::: {.cell hash='index_cache/pdf/unnamed-chunk-1_67cbc2be760bfd13677d3709c2226bf7'}

```{.r .cell-code}
c(0.5, 0.6, 0.25) # números decimales (double)
c(9L, 10L, 11L, 12L, 13L) # números enteros (integer)
c(9:13) # secuencia de números enteros (integer sequence)
c(TRUE, FALSE, FALSE) # valores lógicos (logical)
c(1 + 0i, 2 + 4i) # números complejos (complex)
c("a", "b", "c") # caracteres (character)
```
:::



**Acciones con vectores**

1.  Asignar los vectores a nombres:

    Creamos un vector llamado "dbl" que contiene los números decimales 0.5, 0.6 y 0.25.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-2_596a48aa3ed78a702817322cb4dee413'}
    
    ```{.r .cell-code}
    dbl <- c(0.5, 0.6, 0.25)
    ```
    :::



    Creamos un vector llamado "chr" que contiene los caracteres "a", "b" y "c".



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-3_3ec49d0a4203f37bc68ba90626f1742d'}
    
    ```{.r .cell-code}
    chr <- c("a", "b", "c")
    ```
    :::



2.  Imprimir los vectores "dbl" y "chr" en la consola:

    Visualizamos en la consola el contenido del vector "dbl", que son los números decimales 0.5, 0.6 y 0.25.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-4_ce411da7dce59791fb1feeed228dc01c'}
    
    ```{.r .cell-code}
    dbl
    ```
    :::



    Visualizamos en la consola el contenido del vector "chr", que son los caracteres "a", "b" y "c".



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-5_a0e825e6a882d5ac495929d13ea71e4d'}
    
    ```{.r .cell-code}
    chr
    ```
    :::



3.  Verificar el número de elementos en "dbl" y "chr":

    Calculamos y mostramos en la consola la longitud del vector "dbl", que es 3.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-6_f90466b568201c6f0a47b2788a99e2fc'}
    
    ```{.r .cell-code}
    length(dbl)
    ```
    :::



    Calculamos y mostramos en la consola la longitud del vector "chr", que es 3.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-7_1434f6db1907c725addb23273904f918'}
    
    ```{.r .cell-code}
    length(chr)
    ```
    :::



4.  Verificar el tipo de dato de "dbl" y "chr":

    Visualizamos en la consola el tipo de dato del vector "dbl", que es "double" (números decimales).



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-8_d2ee571c303a54c548d896f9bc99a154'}
    
    ```{.r .cell-code}
    typeof(dbl)
    ```
    :::



    Visualizamos en la consola el tipo de dato del vector "chr", que es "character" (caracteres).



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-9_eee21acfda2d0a335407e7e3ab598924'}
    
    ```{.r .cell-code}
    typeof(chr)
    ```
    :::



5.  Combinar dos vectores:

    Se puede combinar el vector "dbl" consigo mismo utilizando la función "c()", creando un nuevo vector que contiene los elementos duplicados del vector original.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-10_b68003ba5c18e56d2cbb46ff41dcb1f3'}
    
    ```{.r .cell-code}
    c(dbl, dbl)
    ```
    :::



    Tambien se puede combina el vector "dbl" con el vector "chr" utilizando la función "c()", creando un nuevo vector que contiene los elementos de ambos vectores concatenados.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-11_46835486cadc0b664b8c29c77e250d2c'}
    
    ```{.r .cell-code}
    c(dbl, chr)
    ```
    :::



::: callout-note
El cambio automático del tipo de datos del vector resultante se denomina coerción. La coerción garantiza que se mantiene el mismo tipo de datos para cada elemento del vector.
:::

**Operaciones aritméticas con vectores**

1.  Definamos dos nuevos vectores numéricos llamados `a` y `b` con 4 elementos cada uno:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-12_5b69639fdd37d8c35357d7a34fca0cbb'}
    
    ```{.r .cell-code}
    a <- c(1, 2, 3, 4)
    b <- c(10, 20, 30, 40)
    ```
    :::



2.  Realizamos una multiplicación escalar de `a` por 5, lo que significa que cada elemento en `a` se multiplica por 5:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-13_ab27fd4a43b8253efdc6813d78aa7bce'}
    
    ```{.r .cell-code}
    a * 5
    ```
    :::



3.  Realizamos una multiplicación de vectores entre `a` y `b`, lo que implica multiplicar cada elemento en `a` por el elemento correspondiente en `b`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-14_c096aae91f0feced6cb651e0c409cdbf'}
    
    ```{.r .cell-code}
    a * b
    ```
    :::



4.  Creamos un nuevo vector numérico llamado `v` con longitud 5.



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-15_f4789d3198700338e413995b7ddd5aa3'}
    
    ```{.r .cell-code}
    v <- c(1.1, 1.2, 1.3, 1.4, 1.5)
    a * v
    ```
    :::



::: callout-note
Las operaciones aritméticas de los vectores se realizan por elementos. si dos vectores no tienen la misma longitud, el vector más corto se reciclará para que coincida con el más largo (en este caso, se vuelve a utilizar el primer elemento de a).
:::

### 3. Matriz

Una matriz es una estructura bidimensional que contiene elementos organizados en filas y columnas. Todos los elementos de una matriz deben ser del mismo tipo de dato. Las matrices son útiles para almacenar datos tabulares, como una tabla de datos con variables en filas y observaciones en columnas. En R, podemos realizar operaciones matriciales y manipular los datos de manera eficiente utilizando esta estructura.

**Matrices**

1.  Combinamos los vectores `a` y `b`, definidas anteriormente, por columnas utilizando la función `cbind()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-16_0573e07eefe01df7dbd1251db287f01a'}
    
    ```{.r .cell-code}
    A <- cbind(a, b)
    A
    ```
    :::



    Esta opción combina los vectores `a` y `b` por columnas, creando una matriz `A` donde los elementos de `a` forman la primera columna y los elementos de `b` forman la segunda columna.

2.  Combinamos los vectores `a` y `b` por filas utilizando la función `rbind()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-17_6434c09b7516746837a7df467f91ab18'}
    
    ```{.r .cell-code}
    B <- rbind(a, b)
    B
    ```
    :::



    En esta opción, los vectores `a` y `b` se combinan por filas para crear una matriz `B`. Los elementos de `a` forman la primera fila y los elementos de `b` forman la segunda fila.

3.  Creamos una matriz a partir de los elementos de vector `a` utilizando la función `matrix()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-18_b2840e1b43c8c19523fdd21c3c96b66e'}
    
    ```{.r .cell-code}
    A <- matrix(a, ncol = 2, nrow = 2)
    A
    ```
    :::



    Aquí se utiliza la función `matrix()` para crear una matriz `A` a partir de los elementos del vector `a`. Se especifica que la matriz tendrá 2 columnas y 2 filas. Los argumentos nrow y ncol indican el número de filas y el número de columnas de que consta la matriz resultante.

4.  Para 4 elementos y ncol =2 la matriz sólo puede tener 2 filas. Por lo tanto no es necesario especificar ambos argumentos



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-19_2cafe0d6d014e676eb73cda832e64c39'}
    
    ```{.r .cell-code}
    A <- matrix(a, ncol = 2)
    A
    ```
    :::



    En esta variante, se crea una matriz `A` con 2 columnas y se ajusta automáticamente el número de filas según la longitud del vector `a`.

5.  Por defecto la matriz se rellena columna a columna (R trata internamente un objeto matriz como vector columna). si la matriz debe rellenarse fila a fila se requiere el argumento `byrow = TRUE`



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-20_a4900d0ac914718e52dd7a95dd53f623'}
    
    ```{.r .cell-code}
    B <- matrix(a, ncol = 2, byrow = TRUE)
    B
    ```
    :::



    En esta opción, se crea una matriz `B` con 2 columnas y se especifica que los elementos del vector `a` se distribuirán por filas `byrow = TRUE`, es decir, los primeros elementos de `a` formarán la primera fila, los siguientes elementos formarán la segunda fila, y así sucesivamente.

**Acciones con matrices**

1.  Verificamos el número de filas de la matriz `A` utilizando la función `nrow()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-21_0b160dbb3e557609bf3c2856f916ecb4'}
    
    ```{.r .cell-code}
    nrow(A)
    ```
    :::



    Esta línea de código devuelve el número de filas de la matriz `A`.

2.  Verificamos el número de columnas de la matriz `A` utilizando la función `ncol()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-22_99dbfe38745d99a9a2597f429a91e10c'}
    
    ```{.r .cell-code}
    ncol(A)
    ```
    :::



    Aquí se obtiene el número de columnas de la matriz `A`.

3.  Verificamos la dimensión (número de filas y columnas) de la matriz `A` utilizando la función `dim()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-23_d7a82385053ad7d50a8ccc4dec6ff6db'}
    
    ```{.r .cell-code}
    dim(A)
    ```
    :::



    Esta línea de código devuelve la dimensión de la matriz `A` en formato `[nrow, ncol]`.

4.  Combinamos dos matrices `A` por columnas utilizando la función `cbind()` y almacenamos el resultado en `D.wide`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-24_1bf40aa117ef50d77fb3ac170d3be1f1'}
    
    ```{.r .cell-code}
    D.wide <- cbind(A, A)
    D.wide
    ```
    :::



    En esta línea se crea una nueva matriz `D.wide` que combina las matrices `A` y `A` por columnas.

5.  Combinamos dos matrices `A` por filas utilizando la función `rbind()` y almacenamos el resultado en `D.long`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-25_36b942bc9163658776f67670ba19a1d2'}
    
    ```{.r .cell-code}
    D.long <- rbind(A, A)
    D.long
    ```
    :::



    Aquí se crea una nueva matriz `D.long` que combina las matrices `A` y `A` por filas.

6.  Combinamos las matrices `D.wide` y `D.long` por columnas utilizando la función `cbind()` y almacenamos el resultado en `D`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-26_a5bcacf951fdf501b7b09a60c1c7d867'}
    
    ```{.r .cell-code}
    # D <- cbind(D.wide, D.long)
    ```
    :::



    En esta línea se crea una nueva matriz `D` que combina las matrices `D.wide` y `D.long` por columnas.

**Operaciones aritméticas con matrices**

1.  Suma de la matriz `B` consigo misma utilizando el operador `+`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-27_31c8b4d575bf1395f1343cd5867571c2'}
    
    ```{.r .cell-code}
    B + B
    ```
    :::



    Esta línea de código realiza la suma de la matriz `B` con ella misma.

2.  Multiplicación escalar de la matriz `B` por 2 utilizando el operador `*`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-28_d4bbadb2eefa3037ac710ade0150b77d'}
    
    ```{.r .cell-code}
    B * 2
    ```
    :::



    Aquí se realiza la multiplicación de cada elemento de la matriz `B` por 2.

3.  Multiplicación elemento a elemento de la matriz `B` consigo misma y almacenar el resultado en `a`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-29_346e0bf991db225659c6b6a2cf65d0fd'}
    
    ```{.r .cell-code}
    a <- B * B
    a
    ```
    :::



    En esta línea se realiza la multiplicación elemento a elemento de la matriz `B` con ella misma, y el resultado se almacena en la matriz `a`.

4.  Multiplicación de matrices utilizando el operador `%*%`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-30_64f2588a8b95fc7e78472df9375b289d'}
    
    ```{.r .cell-code}
    C <- B %*% B
    C
    ```
    :::



    Aquí se realiza la multiplicación de matrices entre la matriz `B` y ella misma, y el resultado se almacena en la matriz `C`.

**Otras operaciones con matrices:**

1.  Transposición de la matriz `D.wide` utilizando la función `t()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-31_262ff495713ecd15e9425967c6b6fe60'}
    
    ```{.r .cell-code}
    t(D.wide)
    ```
    :::



    Esta línea de código transpone la matriz `D.wide`, es decir, intercambia las filas por columnas y viceversa.

2.  Cálculo del determinante de la matriz `B` utilizando la función `det()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-32_9843836078ef74c6a33decb361f4e045'}
    
    ```{.r .cell-code}
    det(B)
    ```
    :::



    Aquí se calcula el determinante de la matriz `B`.

3.  Cálculo de la inversa de la matriz `B` utilizando la función `solve()` (solo si el determinante es diferente de 0):



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-33_edca7fcf882e0fae570b9ef85f84a3cd'}
    
    ```{.r .cell-code}
    solve(B)
    ```
    :::



    En esta línea se calcula la inversa de la matriz `B`, siempre y cuando el determinante sea diferente de 0.

4.  Cálculo de los valores propios (eigenvalues) de una matriz cuadrada y simétrica utilizando la función `eigen()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-34_19a90baec43973578038f9f2c35012b6'}
    
    ```{.r .cell-code}
    eigen(B)
    ```
    :::



    Aquí se calculan los valores propios de la matriz `B`. Esta operación solo es aplicable a matrices cuadradas y simétricas.

### 4. Data frame

Un data frame es una estructura similar a una matriz, pero más flexible. Puede contener columnas con diferentes tipos de datos, lo que lo hace ideal para almacenar conjuntos de datos heterogéneos. Los data frames son muy utilizados en el análisis de datos, ya que nos permiten manipular y explorar datos de manera eficiente. Podemos realizar operaciones de filtrado, selección y transformación en los data frames para obtener información significativa.

**Creación del data frame:**

1.  Creamos vectores con diferentes tipos de datos, como números decimales (`dbl`), números enteros (`int`), valores lógicos (`lgl`) y caracteres (`chr`):



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-35_e92e4800e5034b0b5f3e816d89ffd6a8'}
    
    ```{.r .cell-code}
    dbl <- c(0.5, 0.6, 0.25, 1.2, 0.333) # números decimales (double)
    int <- c(9L, 10L, 11L, 12L, 13L) # números enteros (integer)
    lgl <- c(TRUE, FALSE, FALSE, TRUE, TRUE) # valores lógicos (logical)
    chr <- c("a", "b", "c", "d", "e") # caracteres (character)
    ```
    :::



    Cada vector tiene elementos que representan valores de su respectivo tipo de dato.

2.  Utilizamos la función `data.frame()` para combinar los vectores en un data frame llamado `df`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-36_e3c623fb12aa0dae8a316eaa111bbde8'}
    
    ```{.r .cell-code}
    df <- data.frame(dbl, int, lgl, chr)
    ```
    :::



    El data frame `df` se crea utilizando los vectores `dbl`, `int`, `lgl` y `chr` como columnas.

3.  Mostamos el contenido del data frame en la consola:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-37_d42c63f8a5875493961ce6a25a468798'}
    
    ```{.r .cell-code}
    df
    ```
    :::



    Esto imprime el contenido del data frame `df`.

**Acciones con data frames:**

1.  Verificamos el número de filas del data frame utilizando la función `nrow()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-38_abb6992cced97339def5aabdb071f1e6'}
    
    ```{.r .cell-code}
    nrow(df)
    ```
    :::



    Esta línea de código devuelve el número de filas en el data frame `df`.

2.  Verificamos el número de columnas del data frame utilizando la función `ncol()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-39_5fcba0fad38a3366f3c0fb4a16b28306'}
    
    ```{.r .cell-code}
    ncol(df)
    ```
    :::



    Aquí se obtiene el número de columnas en el data frame `df`.

3.  Verificamos la dimensión (número de filas y columnas) del data frame utilizando la función `dim()`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-40_621e82a7f33edc0737765e79ac41693c'}
    
    ```{.r .cell-code}
    dim(df)
    ```
    :::



    Esta línea de código devuelve la dimensión del data frame `df` en formato `[nrow, ncol]`, es decir, el número de filas y columnas que tiene el data frame.

### 5. Lista

Una lista es una estructura de datos genérica que puede contener diferentes objetos, como vectores, matrices, data frames o incluso otras listas. A diferencia de las otras estructuras, las listas no tienen restricciones en cuanto a los tipos de datos o la longitud de los componentes individuales. Las listas son muy flexibles y se utilizan cuando necesitamos almacenar objetos de diferentes tipos o estructuras complejas.

**Creación de la lista**

1.  Creamos una variable `a` que contiene un **escalar** de tipo entero (`1L`):



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-41_349da934741a2662bffe4bec2174360c'}
    
    ```{.r .cell-code}
    a <- 1L
    ```
    :::



2.  Creamos un **vector numérico** `dbl` con 5 elementos:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-42_b66d52c246f3c77b566d7ffbc388c55f'}
    
    ```{.r .cell-code}
    dbl <- c(0.5, 0.6, 0.25, 1.2, 0.333)
    ```
    :::



3.  Creamos un **vector de caracteres** `chr` con 3 elementos:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-43_165f4570893b5c2c07643ac9873a981d'}
    
    ```{.r .cell-code}
    chr <- c("a", "b", "c")
    ```
    :::



4.  Creamos un vector `v` con 4 elementos de tipo numérico:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-44_b1bc2bcf94471da78760646a923b91f0'}
    
    ```{.r .cell-code}
    v <- c(1.1, 1.2, 1.3, 1.4)
    ```
    :::



5.  Creamos una matriz `mat` de tamaño 2x2 a partir del vector `v`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-45_eb345f12fdcf6e5b39e619b3831ee3df'}
    
    ```{.r .cell-code}
    mat <- matrix(v, ncol = 2)
    ```
    :::



    La matriz `mat` tiene 2 columnas y los elementos del vector `v` se llenan por columnas.

6.  Creamos una lista `l` que contiene los elementos `a`, `dbl`, `chr` y `mat`:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-46_f3b87f59610c04362564c29d698a85b8'}
    
    ```{.r .cell-code}
    l <- list(a, dbl, chr, mat)
    ```
    :::



    La lista `l` contiene estos elementos en ese orden.

7.  Finalmente, visualizamos el contenido de la lista en la consola:



    ::: {.cell hash='index_cache/pdf/unnamed-chunk-47_5f8bb300937c4624ab6065663fae9621'}
    
    ```{.r .cell-code}
    l
    ```
    :::



    Esto imprime el contenido de la lista `l`.

> Es importante comprender estas estructuras de datos en R, ya que nos permiten organizar y manipular la información de manera efectiva. Cada estructura tiene sus propias características y funciones asociadas que nos facilitan el trabajo con los datos en la programación.
