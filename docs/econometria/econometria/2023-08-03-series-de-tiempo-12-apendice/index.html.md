---
title: Notas de Clase Series de Tiempo
subtitle: Descubre cómo seleccionar hardware, descargar la imagen ISO y preparar los medios de instalación. Exploraremos opciones para probar o instalar Linux en tu equipo.
description: |
  Únete a esta emocionante serie de introducción a Linux, donde te guiaré a través de los pasos para descargar e instalar GNU/Linux en tu equipo. Aprenderás a seleccionar el hardware adecuado, descargar la imagen ISO de tu distribución preferida y preparar los medios de instalación. Además, exploraremos diferentes opciones para probar o instalar Linux. ¡Embárcate en esta aventura y descubre el poder de GNU/Linux!
categories:
  - Informática
  - Tecnología
  - Sistemas Operativos
  - Linux
tags:
  - Linux
  - OpenSource
  - GNU/Linux
  - SistemasOperativos
  - DistribucionesLinux
  - DescargaDeLinux
  - InstalaciónDeLinux
  - Hardware
  - ImagenISO
date: "08/27/2023"
---






# Apendice I 

## Estimador de Mínimos Cuadrados Ordinarios y el análisis clásico de regresión 

El estimador de Mínimos Cuadrados Ordinarios (MCO) es el estimador básico en econometría o, propiamente dicho, en el análisis de regresión. Esta sección cubre las propiedades finitas del estimador de MCO, mismas que son validas para cualquier tamaño de muestra dado. El material cubierto es totalmente estándar.  

Cualquier estudio econométrico inicia con un conjunto de proposiciones sobre algún fenómeno de la economía. Algunos ejemplos familiares son las ecuaciones de demanda, las funciones de producción y algunos otros modelos macroeconómicos. Así, la investigación empírica provee las estimaciones de los parámetros desconocidos en el modelo. La teoría especifica un conjunto de relaciones determinísticas sobre las variables. 

Dichas relaciones sulen estudiarse mediante el análisis de regresión múltiple, el cual permite el estudio de la relación entre una _variable dependiente_ y otras más denominadas _variables independientes_. En adelante, en general diremos que la forma de representar la relación entre la variable dependiente y las variables independientes, tendrá la siguiente notación:
\begin{eqnarray}
    y & = & f(x_1, x_2, \ldots , x_K) + \varepsilon \nonumber \\
    & = & x_1\beta_1 + x_2\beta_2 + \ldots + x_K\beta_K + \varepsilon
\end{eqnarray}

donde $y$ es la variable dependiente o _explicada_, el conjunto de variables dado por $x_1$, $x_2$, ..., $x_K$ son las variables independientes o _explicativas_ y de la teoría tomamos la especificación descrita por $f(x_1, x_2, \ldots, x_K)$. Esta función es comúnmente llamada la _ecuación de regresión poblacional_ de $y$ en $x_1$, $x_2$, ..., $x_K$. El término $\varepsilon$ es una _perturbación_ aleatoria o error de estimación. 

Este error existe por varias razones, principalmente, porque no esperamos capturar toda la influencia que existe o determina a una varaible económica en un modelo simplista como el que generalmente se formula en el análisis de regresión. Digamos, entonces, que existe un conjunto de información no observable que permite la existencia del término de error. Por ejemplo, existe una clara dificultad para obtener medidas razonables de cualidades como habilidades o capcidades de aprendizaje de un conjunto de individuos a los cuales, quizá, queremos medir su productividad. Por lo tanto, sólo podemos medir el efecto de aquellas variables o información que es cuantificable. El resto de la información la conoceremos como aquella que no es observable. Así, el término de error existe a razón de dicha información.

Implícitamente, estamos suponiendo que cada una de las observaciones en una muestra dada por $\{y_i, x_{i1}, x_{i2}, \ldots, x_{iK} \}$, para $i = 1, \ldots, n$, fue generada por un proceso subyacente descrito por:
$$
    y_i = x_{i1}\beta_1 + x_{i2}\beta_2 + \ldots + x_{iK}\beta_K + \varepsilon_i
$$

Es decir, el valor observado de $y_i$ es igual a la suma de dos partes: una parte determinística, $x_{i1}\beta_1 + x_{i2}\beta_2 + \ldots + x_{iK}\beta_K$, y una parte aleatoria, $\varepsilon_i$. Dicho esto, el objetivo del análisis de regresión radica en estimar los parámetros desconocidos del modelo ($\beta_1$, $\beta_2$, $\ldots$, $\beta_K$), validar la proposiciones teóricas usando los datos disponibles y predecir el valor de la variable $y_i$ mediante el uso del modelo estimado. 

Sea $\mathbf{X}_k$ el vector columna de $n$ observaciones de la variable $x_k$, donde $k = 1, \ldots, K$, y que colocado en una matriz da por resultado un arreglo $\mathbf{X}$ de tamaño $n \times K$. Es decir, cada una de las columnas de la siguiente matriz representa todas las observaciones de cada una de las variables:
$$
    \left[ 
    \begin{array}{c c c c}
    \mathbf{X}_1 & \mathbf{X}_2 & \ldots & \mathbf{X}_K 
    \end{array} 
    \right]
    = 
    \left[ 
    \begin{array}{c c c c}
    x_{11} & x_{12} & \ldots & x_{1K}\\
    x_{21} & x_{22} & \ldots & x_{2K}\\
    x_{31} & x_{32} & \ldots & x_{3K}\\
    \vdots & \vdots & \ldots & \vdots\\
    x_{n1} & x_{n2} & \ldots & x_{nK}\\
    \end{array} 
    \right]
$$

En la mayoría de las veces vamos a asumir que existe una columna compuesta del número 1 (uno) en todas sus entradas, tal que, el paramétro $\beta_1$ es un término constante en el modelo. De esta forma la matriz anteriormente mostrada se puede ver como:
$$
    \left[ 
    \begin{array}{c c c c}
    \mathbf{1} & \mathbf{X}_2 & \ldots & \mathbf{X}_K 
    \end{array} 
    \right]
    = 
    \left[ 
    \begin{array}{c c c c}
    1 & x_{12} & \ldots & x_{1K}\\
    1 & x_{22} & \ldots & x_{2K}\\
    1 & x_{32} & \ldots & x_{3K}\\
    \vdots & \vdots & \ldots & \vdots\\
    1 & x_{n2} & \ldots & x_{nK}\\
    \end{array} 
    \right]
$$

Adicionalmente, denotaremos a $\mathbf{Y}$ como un vector columna de $n$ observaciones ($y_1$, $y_2$, $\ldots$, $y_n$, en forma de columna), y a $\boldsymbol{\varepsilon}$ como el vector columna de $n$ perturbaciones ($\varepsilon_1$, $\varepsilon_2$, $\ldots$, $\varepsilon_n$, en forma de columna). El modelo descrito en la ecuaci\'on (1) se puede escribir en su forma general como:
$$
{\bf{Y}} = {\bf {X}}_1\beta_1 + {\bf{X}}_2\beta_2 + \ldots + {\bf{X}}_K\beta_K + {\boldsymbol{\varepsilon}}
$$
\\

Ecuación que podemos rescribir como:
$$
\mathbf{Y} 
=
\left[ 
\begin{array}{c c c c}
\mathbf{X}_1 & \mathbf{X}_2 & \ldots & \mathbf{X}_K 
\end{array} 
\right]
\left[ 
\begin{array}{c}
\beta_1 \\
\beta_2 \\
\vdots \\
\beta_K 
\end{array} 
\right]
+
\
\boldsymbol{\varepsilon}
= 
\boldsymbol{X\beta} + \boldsymbol{\varepsilon}
$$

Adicionalmente, de ahora en delante diremos que la regresión lineal dada por $y_i = x_{i1}\beta_1 + x_{i2}\beta_2 + \ldots + x_{iK}\beta_K + \varepsilon_i$, se podrá escribir como:
$$
y_i = (x_{i1}, x_{i2}, \ldots, x_{iK})(\beta_1, \beta_2, \ldots, \beta_K)' + \varepsilon = \mathbf{X}'_i \boldsymbol{\beta} + \varepsilon_i
$$

Así, los parámetros desconocidos, $\boldsymbol{\beta}$, de la relación estocástica dada por $y_i = \mathbf{X}'_i \boldsymbol{\beta} + \varepsilon_i$ son el objeto de la estimación. En este sentido distingamos que $\boldsymbol{\beta}$ y $\varepsilon_i$ son, respectivamente, el conjumto de los parámetros y el término de error de la población, y que, por lo tanto, denotaremos a las estimaciones relsultantes de una muestra como $\hat{\boldsymbol{\beta}}$ y $e_i$. Es decir, siempre que no podamos adquirir o conocer la iformación de todos los elementos de la población, nuestras aproximaciones muestrales se denotarán de forma distinta a las que refieran a la población. 

Así, los principios de \textit{regresión poblacional} y \textit{regresión muestral} están dados por las fórmulas $E[y_i|\mathbf{X}_i] = \mathbf{X}'_i\boldsymbol{\beta}$ y $\hat{y}_i = \mathbf{X}'_i\hat{\boldsymbol{\beta}}$, respectivamente. Donde $\hat{y}_i$ es el estimador de $E[y_i|\mathbf{X}_i]$.

Por su parte, el término de error asociado será:
$$
\varepsilon_i = y_i - {\bf{X}}'_i \boldsymbol{\beta}
$$

si hablamos del caso poblacional o,
$$
e_i = y_i - {\bf{X}}'_i \hat{\boldsymbol{\beta}}
$$

cuando hagamos referencia al caso muestral. Es decir, nuestro estimador de  $\varepsilon_i$ es $e_i$. De lo dicho hasta ahora podemos escribir:
$$
y_i = \mathbf{X}'_i \boldsymbol{\beta} + \varepsilon_i = \mathbf{X}'_i \hat{\boldsymbol{\beta}} + e_i
$$

Intuitivamente, la ecuación (36) significa que siempre que poseamos una muestra de los elementos de la población, podremos explicar una parte de la variable dependiente, no su totalidad. En este sentido, el análisis de regresión consiste en un proceso de ajuste a la variable dependiente. Está es la idea que da origen al $R^2$ y otras medidas de bondad de ajuste, mismas que más adelante en el curso analizaremos.

Regresando a la discusión central de esta sección, el método de MCO, en consecuencia, resulta en encontrar la combinación de parámetros $\hat\beta$ que permita minimizar la suma de los residuales al cuadrado dada por:
$$
\sum^{n}_{i=1}{e^2_i} = \sum^{n}_{i=1}{(y_i - {\bf X}'_i\hat{\boldsymbol{\beta}})^2}
$$

donde $\hat{\boldsymbol{\beta}}$ denota el vector de estimadores $\hat{\beta}_1$, $\ldots$, $\hat{\beta}_K$. En términos matriciales, dado que $(e_1, e_2, \ldots, e_n)'(e_1, e_2, \ldots, e_n) = {\mathbf{e'e}}$, el problema del método de MCO consiste en:
$$
Minimizar_{\hat{\boldsymbol \beta}} S(\hat{\boldsymbol \beta}) = Minimizar_{\hat{\boldsymbol \beta}} \mathbf{e'e} 
$$

$$
= Minimizar_{\hat{\boldsymbol \beta}} (\mathbf{Y}-\mathbf{X}\hat{\boldsymbol \beta})'(\mathbf{Y}-\mathbf{X}\hat{\boldsymbol \beta})
$$

Expandiendo la expresión $\mathbf{e'e}$ obtenemos:
$$
\mathbf{e'e} = \mathbf{Y'Y} - 2 \mathbf{Y'X} \hat{\boldsymbol \beta} + \hat{\boldsymbol \beta}' \mathbf{X'X}\hat{\boldsymbol \beta}
$$

De esta forma obtenemos que las condiciones necesarias de un mínimo son:
$$
\frac{\partial S(\hat{\boldsymbol \beta})}{\partial \hat{\boldsymbol \beta}} = -2{\bf{X'Y}} + 2{\bf{X'X}} \hat{\boldsymbol{\beta}} = \bf{0}
$$

De ecuación anterior obtenemos para la solución del problema del mínimo a las ecuaciones siguientes conocidas como \textit{ecuaciones normales} dadas por:
$$
\bf{X'X}\hat{\boldsymbol \beta} = \bf{X'Y}
$$

Notemos que dichas ecuaciones normales son en realidad un sistema de ecuaciones de $K$ variables o incógnitas. Por un lado, recordemos que $\mathbf X$ es una matriz de dimensión $n \times K$, con lo cual $\mathbf X'$ es de dimensión $K \times n$. Así, el producto $\mathbf{X'X}$ dará como resultado una matriz cuadrada de dimensión $K \times K$. Por otro lado, sabemos que $\mathbf Y$ es un vector de tamaño $n \times 1$, con lo cual el producto $\mathbf{X'Y}$ da como resultado un vector de dimención $K \times 1$. En conclusión, el sistema de ecuaciones normales consiste en $K$ ecuaciones con $K$ incógnitas ($\hat{\beta}_1, \ldots, \hat{\beta}_K$). Ante este hecho, existen múltiples formas mediante las cuales se puede solucionar dicho sistema, sin embargo en nuesto caso seguiremos el siguiente procedimiento.

Si la inversa de la matriz $\mathbf{X'X}$ existe (recuerde que el procedimiento de MCO tradicional supone que $\mathbf{X}$ es de rango completo), la solución esta dada por la siguiente expresión:
$$
\hat{\boldsymbol \beta} = (\mathbf{X'X})^{-1}\mathbf{X'Y}
$$

Esta expresión, a pesar de ser en apariencia compleja se puede ver como un conjunto de sumas. En general hemos supuesto que nuestra regresión a estimar esta descrita por la eccuación: $y_i = x_{i1}\beta_1 + x_{i2}\beta_2 + \ldots + x_{iK}\beta_K + \varepsilon_i$, de esta forma tenemos $K$ variables independientes es nuestra regresión. 

Ahora bien, si denotamos a $\mathbf{X}_k$ como el vector columna formado por todas las observaciones de la muestra ($i = 1, 2, \ldots, n$) para la variable $k$, podemos decir que la matriz $\mathbf X$ que contiene todas las variable independientes se forma por la concatenación de cada uno de los $K$ vectores columna. Dicho esto, podemos ver que las matrices $\mathbf{X}$ y $\mathbf{X'}$ se pueden expresar como:

\[
\mathbf{X} = 
\left[ \begin{array}{ccccc}
x_{11} & x_{12} & x_{13} & \ldots & x_{1K} \\
x_{21} & x_{22} & x_{23} & \ldots & x_{2K} \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
x_{n1} & x_{n2} & x_{n3} & \ldots & x_{nK}
\end{array} \right] =
\left[ \begin{array}{ccccc}
\mathbf{X}_1 & \mathbf{X}_2& \mathbf{X}_3 & \ldots & \mathbf{X}_K
\end{array} \right]
\]

\[
\bf{X'} = 
\left[ \begin{array}{ccccc}
x_{11} & x_{21} & x_{31} & \ldots & x_{n1} \\
x_{12} & x_{22} & x_{32} & \ldots & x_{n2} \\
x_{13} & x_{23} & x_{33} & \ldots & x_{n3} \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
x_{1K} & x_{2K} & x_{3K} & \ldots & x_{nK}
\end{array} \right] =
\left[ \begin{array}{c}
\mathbf{X}_1' \\
\mathbf{X}_2'\\
\mathbf{X}_3'\\
\vdots \\
\mathbf{X}_K'
\end{array} \right]
\]\\

Si suponemos que nuestra regresión tiene una constante, la especificación sería: $y_i = \beta_1 + x_{i2}\beta_2 + \ldots + x_{iK}\beta_K + \varepsilon_i$, con unas matrices $\mathbf X$ y $\mathbf X'$ dadas:
\[
\mathbf{X} = 
\left[ \begin{array}{ccccc}
1 & x_{12} & x_{13} & \ldots & x_{1K} \\
1 & x_{22} & x_{23} & \ldots & x_{2K} \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
1 & x_{n2} & x_{n3} & \ldots & x_{nK}
\end{array} \right] =
\left[ \begin{array}{ccccc}
\mathbf{1_n} & \mathbf{X}_2& \mathbf{X}_3 & \ldots & \mathbf{X}_K
\end{array} \right]
\]

\[
\bf{X'} = 
\left[ \begin{array}{ccccc}
1 & 1 & 1 & \ldots & 1 \\
x_{12} & x_{22} & x_{32} & \ldots & x_{n2} \\
x_{13} & x_{23} & x_{33} & \ldots & x_{n3} \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
x_{1K} & x_{2K} & x_{3K} & \ldots & x_{nK}
\end{array} \right] =
\left[ \begin{array}{c}
\mathbf{1_n}' \\
\mathbf{X}_2'\\
\mathbf{X}_3'\\
\vdots \\
\mathbf{X}_K'
\end{array} \right]
\]\\

Donde $\mathbf{1_n}$ es un vector columna compuesto de 1's (unos). Retomando (14), desarrollemos cada uno de los casos anteriores, así obtenemos lo siguiente para el caso general:
\[
\mathbf{X'X} = 
\left[ \begin{array}{c}
\mathbf{X}_1' \\
\mathbf{X}_2' \\
\mathbf{X}_3'\\
\vdots \\
\mathbf{X}_K'
\end{array} \right]
\left[ \begin{array}{ccccc}
\mathbf{X}_1 & \mathbf{X}_2 & \mathbf{X}_3 & \ldots & \mathbf{X}_K
\end{array} \right]
\]

\[ 
\left[ \begin{array}{ccccc}
\mathbf{X}_1'\bf{X}_1 & \mathbf{X}_1'\mathbf{X}_2 & \mathbf{X}_1'\mathbf{X}_3 & \ldots & \mathbf{X}_1'\mathbf{X}_K \\
\mathbf{X}_2'\mathbf{X}_1 & \mathbf{X}_2'\mathbf{X}_2 & \mathbf{X}_2'\mathbf{X}_3 & \ldots & \mathbf{X}_2'\mathbf{X}_K \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
\mathbf{X}_K'\mathbf{X}_1 & \mathbf{X}_K'\mathbf{X}_2 & \mathbf{X}_K'\mathbf{X}_3 & \ldots & \mathbf{X}_K'\mathbf{X}_K
\end{array} \right]
\]\\

Por lo tanto, obtenemos que:

\[
\mathbf{X'X} =
\left[ \begin{array}{ccccc}
\sum^{n}_{i=1}{x_{i1}^2} & \sum^{n}_{i=1}{x_{i1}x_{i2}} & \sum^{n}_{i=1}{x_{i1}x_{i3}} & \ldots & \sum^{n}_{i=1}{x_{i1}x_{iK}}\\
\sum^{n}_{i=1}{x_{i2}x_{i1}} & \sum^{n}_{i=1}{x^{2}_{i2}} & \sum^{n}_{i=1}{x_{i2}x_{i3}} & \ldots & \sum^{n}_{i=1}{x_{i2}x_{iK}}\\
\sum^{n}_{i=1}{x_{i3}x_{i1}} & \sum^{n}_{i=1}{x_{i3}x_{i2}} & \sum^{n}_{i=1}{x^2_{i3}} & \ldots & \sum^{n}_{i=1}{x_{i3}x_{iK}}\\
\vdots & \vdots & \vdots & \vdots & \vdots \\
\sum^{n}_{i=1}{x_{iK}x_{i1}} & \sum^{n}_{i=1}{x_{iK}x_{i2}} & \sum^{n}_{i=1}{x_{iK}x_{i3}} & \ldots & \sum^{n}_{i=1}{x^2_{iK}}
\end{array} \right]
\]\\

Por otro lado, cuando supongamos que existe un término constante:

\[
\mathbf{X'X} =
\left[ \begin{array}{ccccc}
n & \sum^{n}_{i=1}{x_{i2}} & \sum^{n}_{i=1}{x_{i3}} & \ldots & \sum^{n}_{i=1}{x_{iK}}\\
\sum^{n}_{i=1}{x_{i2}} & \sum^{n}_{i=1}{x^{2}_{i2}} & \sum^{n}_{i=1}{x_{i2}x_{i3}} & \ldots & \sum^{n}_{i=1}{x_{i2}x_{iK}}\\
\sum^{n}_{i=1}{x_{i3}} & \sum^{n}_{i=1}{x_{i3}x_{i2}} & \sum^{n}_{i=1}{x^2_{i3}} & \ldots & \sum^{n}_{i=1}{x_{i3}x_{iK}}\\
\vdots & \vdots & \vdots & \vdots & \vdots \\
\sum^{n}_{i=1}{x_{iK}} & \sum^{n}_{i=1}{x_{iK}x_{i2}} & \sum^{n}_{i=1}{x_{iK}x_{i3}} & \ldots & \sum^{n}_{i=1}{x^2_{iK}}
\end{array} \right]
\]\\

Adicionalmente, el producto $\mathbf{X'Y}$, en el caso general, se puede expresar como:

\[
\mathbf{X'Y} 
= 
\left[ \begin{array}{c}
\mathbf{X}_1' \\
\mathbf{X}_2' \\
\mathbf{X}_3'\\
\vdots \\
\mathbf{X}_K'
\end{array} \right] \mathbf{Y}
= 
\left[ \begin{array}{c}
\mathbf{X}_1'\mathbf{Y}\\
\mathbf{X}_2'\mathbf{Y}\\
\mathbf{X}_3'\mathbf{Y}\\
\vdots\\
\mathbf{X}_K'\mathbf{Y}
\end{array} \right]
=
\left[ \begin{array}{c}
\sum^{n}_{i=1}{x_{i1}y_{i}}\\
\sum^{n}_{i=1}{x_{i2}y_{i}}\\
\sum^{n}_{i=1}{x_{i3}y_{i}}\\
\vdots\\
\sum^{n}_{i=1}{x_{iK}y_{i}}
\end{array} \right]
\]\\

Si el modelo supone la existencia de un término constante, dicho producto se expresa como:

\[
\mathbf{X'Y} 
= 
\left[ \begin{array}{c}
\mathbf{1_n}' \\
\mathbf{X}_2' \\
\mathbf{X}_3'\\
\vdots \\
\mathbf{X}_K'
\end{array} \right] \mathbf{Y}
= 
\left[ \begin{array}{c}
\mathbf{1_n}'\mathbf{Y}\\
\mathbf{X}_2'\mathbf{Y}\\
\mathbf{X}_3'\mathbf{Y}\\
\vdots\\
\mathbf{X}_K'\mathbf{Y}
\end{array} \right]
=
\left[ \begin{array}{c}
\sum^{n}_{i=1}{y_{i}}\\
\sum^{n}_{i=1}{x_{i2}y_{i}}\\
\sum^{n}_{i=1}{x_{i3}y_{i}}\\
\vdots\\
\sum^{n}_{i=1}{x_{iK}y_{i}}
\end{array} \right]
\]\\

Finalmente, para que esta solución dada para el procedimiento de MCO sea un mínimo debemos buscar las condiciones de segundo orden:
$$
\frac{\partial^2 S(\hat{\boldsymbol \beta})}{\partial \hat{\boldsymbol \beta} \partial \hat{\boldsymbol \beta'}} = 2 \mathbf{X'X}
$$

donde la matriz $\mathbf{X'X}$ debe ser positiva definida para que la solución de MCO sea un mínimo. Sea $q = \mathbf{c'X'Xc}$ para algún vector $\mathbf{c}$ distinto de cero. Entonces:

\[
q = \mathbf{v'v} = \sum_{i=1}^{n}{v_i^2} \textrm{, donde } \mathbf{v = Xc}
\]\\

Así, $q$ es positivo. Si $\mathbf v$ fuera cero, entonces existe una combinación lineal de las columnas de $\mathbf X$ que da como resultado cero, lo cual contradice el supuesto de que $\mathbf X$ es de rango completo. En todos los casos, si $\mathbf X$ es de rango completo, entonces la solución del método de MCO, $\hat{\boldsymbol{\beta}}$, es la única que mínimiza la suma de los residuales al cuadrado. 

Finalmente, no debemos perder de vista que lo aqui espresado tiene un objeto, mostrar como este procedimiento de MCO es valido cuando suponemos regresiones del tipo:
$$
y_t = \beta_0 + y_{t-1}\beta_1 + \ldots + y_{t-\tau}\beta_\tau + \varepsilon_t
$$

Donde $t = 0, 1, 2, \ldots, T$ es un índice del tiempo, la variable dependiente es $y_t$ y las variables independientes son la misma variable independiente, pero en forma rezagada. Así, podemos definir un vector columna $\mathbf{Y}_{t-k}$ el vector columna de $T$ observaciones de la variable dependiente rezagada $k$ veces, donde $k = 1, \ldots, \tau$, y que colocado en una matriz da por resultado un arreglo $\mathbf{X}$ de tamaño $T-\tau \times \tau+1$. 

## Estimación por el método de Máxima Verosimilitud (MV)

Ahora analicemos otro método de estimación que tiene más uso en series de tiempo: MV. Iniciemos con algo de notación. La función de densidad de probabilidad de una variable aleatoria $y$, condicional en un conjunto de parámetros, $\boldsymbol{\theta}$, la denotaremos como $f(y|\boldsymbol{\theta})$. Dicha función identifica el mecanismo generador de datos subyacente a la muestra observable y al mismo tiempo prove una descripción matemática de los datos que el proceso generará.

Por otro lado, la función de densidad conjunta de n observaciones \textit{independientes e idénticamente distribuidas} (i.i.d) está dada por el siguiente producto de las funciones de densidad individuales:
$$
f(y_1, y_2, \ldots, y_n |\boldsymbol{\theta}) = \prod_{i=1}^n f(y_i|\boldsymbol{\theta}) = L(\boldsymbol{\theta} | \boldsymbol{y})
$$

A esta función de densidad conjunta se le conoce como \textbf{Función de Verosimilitud}, la cual se define como una función del vector de parámetros, $\boldsymbol{\theta}$, donde $\boldsymbol{y}$ indica la familia de observaciones en la muestra de datos. Notemos que la función de densidad conjunta la hemos escrito como una función de los datos observados condicional en los parámetros a estimar. Sin embargo, por otro lado también hemos dicho que la función de verosimilitud, aquella que es ídentica a la función de densidad conjunta, es una función de los parámetros condicional en los datos observados. Aunque ambas funciones son la misma cabe hace enfasís de que en la segunda buscamos aquellos parámetros que máximizan la función de verosimilitud condicional en los datos observados.

Ahora bien, el procedimiento de máxima verosimilitud, por simplicidad, se estima aplicando la función logarítmo natural a $L(\boldsymbol{\theta} | \boldsymbol{y})$. Derivado de que la función logarítmo natural es monótona, ésta preserva el orden y con ello el valorque máximiza a la función. De esta forma escribiremos que la función será:
$$
ln(L(\boldsymbol{\theta} | \boldsymbol{y})) = ln(\prod_{i=1}^n f(y_i|\boldsymbol{\theta})) = \sum_{i = 1}^{n} ln(f(y_i|\boldsymbol{\theta}))
$$

Así, por simplicidad diremos que denotaremos a el logarítmo de la función de densidad conjunta como:
$$
ln(L(\boldsymbol{\theta} | \boldsymbol{y})) = l(\boldsymbol{\theta} | \boldsymbol{y})
$$

Dicho lo anterior, el objetivo de esta sección es mostrar el procedimiento de estimación de Máxima Verosimilitud aplicado a una regresión lineal. Retomemos la idea de que en nuestra ecuación de regresión lineal: $y_i = \mathbf{X}_i'\boldsymbol \beta + \varepsilon_i$ para $i = 1, \ldots, n$, el término de error $\varepsilon_i$ se distribuye como una normal con media cero y varianza constante, $\sigma^2$:
\[
\varepsilon_i \sim \mathbf{N}(0, \sigma^2)
\]

Asimismo, en genral hemos dicho que, visto como vector, el término de error tiene una distribución de la forma:
\[
\boldsymbol \varepsilon \sim \mathbf{N}(\mathbf{0}, \sigma^2 \mathbf{I}_n)
\]

Obsérvese que la forma de la varianza del término de error: $Var[\boldsymbol \varepsilon | \mathbf X] =  \sigma^2 \mathbf{I}_n$, implica que la distribución de cada una de las $\varepsilon_i$ es independiente, de tel forma que la función de densidad esta dada por:
\[
f(\varepsilon_i | \boldsymbol \theta) = \frac{1}{\sqrt{2 \pi \sigma^2}}e^{-\frac{1}{2} \frac{(\varepsilon_i - 0)^2}{\sigma^2}}
\]

Sustituyendo la definición del término de error obetenemos la siguiente expresión:
$$
f(\varepsilon_i | \boldsymbol \theta) = \frac{1}{\sqrt{2 \pi \sigma^2}}e^{-\frac{1}{2} \frac{(\mathbf{X}_i'\boldsymbol \beta - y_i)^2}{\sigma^2}}
$$

Donde el vector $\boldsymbol \theta$ se compone de el vector $\boldsymbol \beta$ y $\sigma^2$.

Por lo tanto, la función de verosimilitud asociada a este caso está dada por la siguiente expresión:
$$
L(\boldsymbol{\theta} | \boldsymbol{\varepsilon}) = \prod_{i=1}^n f(\varepsilon_i|\boldsymbol{\theta}) = \prod_{i=1}^n\frac{1}{\sqrt{2 \pi \sigma^2}}e^{-\frac{1}{2} \frac{(\mathbf{X}_i'\boldsymbol \beta - y_i)^2}{\sigma^2}}
$$

Esta última ecuación, en su forma logarítmica, se puede expresar como:
\begin{eqnarray}
l(\boldsymbol{\theta} | \boldsymbol{\varepsilon}) 
& = &
\sum_{i=1}^n{ \left[ ln(1) - ln(\sqrt{2 \pi \sigma^2}) - \frac{1}{2} \frac{(y_i - \mathbf{X}_i'\boldsymbol \beta)^2}{\sigma^2} \right]} \nonumber \\
 & = &
\sum_{i=1}^n{ \left[- \frac{1}{2}ln(2 \pi \sigma^2) - \frac{1}{2} \frac{(y_i - \mathbf{X}_i'\boldsymbol \beta)^2}{\sigma^2} \right]} \nonumber \\
 & = &
- \frac{1}{2} \sum_{i=1}^n{ \left[ln(2 \pi \sigma^2) + \frac{(y_i - \mathbf{X}_i'\boldsymbol \beta)^2}{\sigma^2} \right]} \nonumber \\
 & = &
- \frac{1}{2} \left[ \sum_{i=1}^n{ \left[ln(2 \pi \sigma^2) \right]} + \sum_{i=1}^n{ \left[\frac{(y_i - \mathbf{X}_i'\boldsymbol \beta)^2}{\sigma^2} \right]} \right] \nonumber \\\nonumber \\
 & = &
- \frac{1}{2} \left[ n \times ln(2 \pi \sigma^2) + \frac{1}{\sigma^2} \sum_{i=1}^n{ \left[(y_i - \mathbf{X}_i'\boldsymbol \beta)^2\right]} \right] \nonumber \\
 & = &
- \frac{n}{2}ln(2 \pi \sigma^2) - \frac{1}{2 \sigma^2} \boldsymbol \varepsilon' \boldsymbol \varepsilon \nonumber \\
 & = &
- \frac{n}{2}ln(2 \pi \sigma^2) - \frac{1}{2 \sigma^2} (\mathbf{Y} - \mathbf{X} \boldsymbol \beta)'(\mathbf{Y} - \mathbf{X} \boldsymbol \beta) \nonumber \\
 & = &
- \frac{n}{2}ln(2 \pi \sigma^2) - \frac{1}{2 \sigma^2} (\mathbf{Y'Y} - 2\mathbf{Y'X} \boldsymbol \beta + \boldsymbol \beta' \mathbf{X'X} \boldsymbol \beta)
\end{eqnarray}

Establecida la función de verosimilitud, el siguiente paso consisten en la estimación de los parámetros. Para tal efecto debemos determinar las condiciones de primer orden, quedando de la siguiente forma:
$$
\frac{\partial l(\boldsymbol{\theta} | \boldsymbol{\varepsilon})}{\partial \hat{\boldsymbol \beta}} = -2{\mathbf{X'Y}} + 2{\mathbf{X'X}} \hat{\boldsymbol{\beta}} = \mathbf{0}
$$

$$
\frac{\partial l(\boldsymbol{\theta} | \boldsymbol{\varepsilon})}{\partial \hat{\sigma}^2} = - \frac{n}{2 \sigma^2} + \frac{1}{2 (\sigma^2)^2} (\mathbf{Y} - \mathbf{X} \hat{\boldsymbol \beta})'(\mathbf{Y} - \mathbf{X} \hat{\boldsymbol \beta}) = \bf{0}
$$

De las dos ecuaciones anteriores podemos deducir las fórmulas de nuestros estimadores de Máxima Verosimilitud:
$$
\hat{\boldsymbol{\beta}} = (\mathbf{X'X})^{-1}\mathbf{X'Y}
$$

$$
\hat{\sigma}^2 = \frac{\mathbf{e'e}}{n}
$$

El procedimiento de de máxima verosimilitud es el más atractivo de los demás procedimientos de estimación, ya que sus propiedades asíntoticas son que: 

\textit{Un estimador es asíntoticamente eficiente si éste es consistente, asíntoticamente distribuido de forma normal y posee una matriz de varianza y covarianza que no es más grande que la matrix de varianzas y covarianzas asociadas a cualquier otro estimador.}

Si se asume que la función de densidad conjunta cumple con las condiones de regularidad (que la primer derivada del logarítmo de la función de verosimilitud es continua en todo punto, y que las condiciones de primer órden y segundo órden son conocidas), podemos enunciar el suiguente:

\textbf{Teorema. Propiedades de un Estimador de Máxima Verosimilitud}. Bajo condiciones de regularidad, el estimador de máxima verosimilitud posee las siguientes propiedades asíntoticas:

\begin{enumerate}
\item Consistencia: $plim \hat{\boldsymbol{\theta}} = \boldsymbol{\theta}_0$ 
\item Normalidad asíntotica: $\hat{\boldsymbol{\theta}} \sim N[\boldsymbol{\theta}_0, I(\boldsymbol{\theta}_0)^{-1}]$, donde
\[
I(\boldsymbol{\theta}_0) = -E_0[\partial^2 ln(L)/\partial \boldsymbol{\theta}_0 \partial \boldsymbol{\theta}'_0]
\]
\item Eficiencia asíntotica: $\hat{\boldsymbol{\theta}}$ es asíntoticamente eficiente y alcanza la cota inferior de Cramér-Rao.
\item Invarianza. El estimador de máxima verosimilitud de $\boldsymbol{\gamma}_0 = c(\boldsymbol{\theta}_0)$ es $c(\hat{\boldsymbol{\theta}})$ si $c(\boldsymbol{\theta}_0)$ es una función continúa y diferenciable.
\end{enumerate}

## Métricas de bondad de ajuste

El criterio que dio origen a los estimadores de MCO consiste en el valor m\'inimo para la suma del cuadrado de todos los residuales. Esta suma es, por otro lado, una medida de ajuste de la l\'inea de regresi\'on a los datos. Sin embargo, esta medida puede ser facilmente alterada y, por lo tanto, rescalada por una simple multiplicaci\'on de los residuales por cualquier valor. Recordemos que el valor de los residuales esta basado en los valores de $\bf{X}$, as\'i podr\'iamos pregntarnos por cuanto de la variaci\'on de $\bf{Y}$ es explicada por la varaci\'on de $\bf{X}$.

De la Figura 1 podemos afirmar que la variaci\'on total de la variable dependiente $\bf{Y}$ se puede descomponer en dos partes, es decir, la variaci\'on total de $\bf{Y}$ se puede expresar como la suma dada por:

$$SST = \sum^{n}_{i=1}{(y_i - \bar{y})^2} $$

Dada la deficnici\'on de regresi\'on tenemos que $\bf{Y} = \bf{X} \hat{\boldsymbol{\beta}} + \bf{e} = \hat{\bf{Y}}  + \bf{e}$. Es decir, $y_i = \hat{y}_i + e_i = {\bf{X}}_i \hat{\boldsymbol{\beta}} + e_i$. De donde podemos inferir que:

$$ y_i - \bar{y} = \hat{y}_i - \bar{y} + e_i = ({\bf{X}}_i - \bar{\bf{X}}_i )\hat{\boldsymbol{\beta}} + e_i $$

Se definimos $\bf{M^0}$ como una matriz saca promedios (con las propiedad de ser idempotente y simetrica) y definida como:

$$
\bf{M^0}= 
\left[ \begin{array}{ccccc}
1 & 0 & 0 & \ldots & 0 \\
0 & 1 & 0 & \ldots & 0 \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
0 & 0 & 0 & \ldots & 1
\end{array} \right] 
-
\left[ \begin{array}{ccccc}
1 & 1 & 1 & \ldots & 1 \\
1 & 1 & 1 & \ldots & 1 \\
\vdots & \vdots & \vdots & \vdots & \vdots \\
1 & 1 & 1 & \ldots & 1
\end{array} \right] 
$$
$$=
\bf{I}_n 
-
\left[ \begin{array}{c}
1  \\
1 \\
\vdots \\
1 
\end{array} \right]  
\left[ \begin{array}{ccccc}
1 & 1 & 1 & \ldots & 1 \\
\end{array} \right] 
=
\bf{I}_n - i'i
$$

De tal forma que para cualquier vector o matriz, $\bf{W}$, sucede que: $\bf{M^0}\bf{W}= \bf{W} - \bar{\bf{W}}$, por ello le llammos matriz saca promedios. Regresando a nuestra discusi\'on, podemos escribir que:

$$\bf{Y} - \bar{\bf{Y}} = \bf{M^0Y} = \bf{M^0X} \hat{\boldsymbol{\beta}} + \bf{M^0e}$$

Recordemos que si $\bf{M^0}$ extrae los promedios, estonces $\bf{M^0e} = e$. As\'i podemos verificar que el producto $\bf{Y'M^0}\bf{M^0Y}$ es igual a:

$$SST = ({\bf{Y}} - \bar{\bf{Y}})'({\bf{Y}} - \bar{\bf{Y}}) = \sum^{n}_{i=1}{(y_i - {\bar{y}})^2} = \bf{Y'M^0Y}$$

$$\bf{Y'M^0Y} = Y'(\bf{M^0X} \hat{\boldsymbol{\beta}} + \bf{M^0e}) = (\bf{X} \hat{\boldsymbol{\beta}} + \bf{e})'(\bf{M^0X} \hat{\boldsymbol{\beta}} + \bf{M^0e})$$
$$= (\hat{\boldsymbol{\beta}}' \bf{X'} + \bf{e'})(\bf{M^0X} \hat{\boldsymbol{\beta}} + \bf{M^0e}) $$
$$= \hat{\boldsymbol{\beta}}' \bf{X'}\bf{M^0X} \hat{\boldsymbol{\beta}} + \hat{\boldsymbol{\beta}}' \bf{X'}\bf{M^0e} + \bf{e'}\bf{M^0X} \hat{\boldsymbol{\beta}} + \bf{e'}\bf{M^0e}$$

Finlamente, como recordaran de clases pasadas, dijimos que s\'olo cuando nuestra regresi\'on inclui constante la suma de residuales $\sum^{n}_{i=1}{e_i} = 0$. De esta forma, el promedio de residuales  $(\sum^{n}_{i=1}{e_i})/n = 0$. Es decir,  que nuestra matriz saca promedio multiplicada por el vector de residuales es igual a $\bf{M^0e} = e - \bar{e} = e$. As\'i:

$$\bf{Y'M^0Y} = \hat{\boldsymbol{\beta}}' \bf{X'}\bf{M^0X} \hat{\boldsymbol{\beta}} + \hat{\boldsymbol{\beta}}' \bf{X'}\bf{e} + \bf{e'}\bf{X} \hat{\boldsymbol{\beta}} + \bf{e'}\bf{e}$$

Por otro lado, sabemos que la soluci\'on por el m\'etodo de MCO garantiza que el producto de $\bf{X'e} = \bf{e'X} = 0$.

$$SST = \bf{Y'M^0Y} = \hat{\boldsymbol{\beta}}' \bf{X'}\bf{M^0X} \hat{\boldsymbol{\beta}} + \bf{e'}\bf{e}$$
$$SST = SSR + SSE$$

O en palabras, la variavilidad total de $\bf{Y}$ se puede descomponer en dos: la variavilidad originada por la regresi\'on y la variavilidad que no puede ser explicada, es decir, la del t\'ermino de error.

Dicho esto, porponemos el siguiente coeficiente de bondad de ajuste a los datos, el cual suele concerse como $R^2$:

$$R^2 = \frac{SSR}{SST} = \frac{SST - SSE}{SST} = 1 - \frac{SSE}{SST}$$

En f\'ormula:

$$R^2 = 1 - \frac{\bf{e'e}}{\bf{Y'M^0Y}}$$

Por \'ultimo el $R^2$ ajustado solo es: 

$$R^2 = 1 - \frac{{\bf{e'e}}/(n-K)}{{\bf{Y'M^0Y}}/(n-1)}$$

## Pruebas de Hipótesis

El An\'alisis de Regresi\'on se suele usar con mucha frecuencia para los siguientes prop\'ositos: la estimaci\'on y predicci\'on, y para probar alg\'un tipo de hip\'otesis. La estimaci\'on y predicci\'on se analizar\'a con mayor detalle al final de esta clase y el sesiones futuras. Por lo que respecta a las pruebas de hip\'otesis estableceremos los siguiente.

Recordemos que nuestro modelo general de regresi\'on est\'a dado por la siguiente expresi\'on:

$${\bf Y} = {\bf X}{\boldsymbol \beta} + {\boldsymbol \varepsilon}$$

Ahora consideremos un ejemplo, supongamos que desea plantear una regresi\'on del tipo logar\'itmica con el objeto de determinar la demanda de tabaco. As\'i, establece la siguiente relaci\'on:

$$ln(Q_{Tabaco}) = \beta_0 + \beta_1 ln(P_{Tabaco}) + \beta_2 ln(P_{Alcohol}) + \beta_3 ln(Ingreso) + \varepsilon$$

Donde $Q_{Tabaco}$ es la cantidad de tabaco demandada, y $P_{Tabaco}$ y $P_{Alcohol}$ son el precio del tabaco y del aocohol, respectivamente. Suponga, adicionalmente, que sospecha que el tabaco y el alcohol guardan una relaci\'on de complementariedad, por lo que espera que los param\'etros asociados a las variables de precios de ambos tengan el mismo signo (-). Asimismo, suponga que estas variables son las \'unicas relevantes para este caso y el resto de la informaci\'on es no observable o no medible.

Supongamos, quiz\'a de forma absurda, que el tabaco y el alcohol exhiben una el\'asticidad unitaria, por lo que decide plantear la siguiente hip\'otesis:

$$H_0: \beta_1 = 1 \medspace y \medspace \beta_2 = 1$$

$$H_1: No \medspace H_0$$

La hip\'otesis nula es equivalente a escribir el siguiente sistema de ecuaciones:

$$0 \beta_0 + 1 \beta_1 + 0 \beta_2 + 0 \beta_3 = 1$$
$$0 \beta_0 + 0 \beta_1 + 1 \beta_2 + 0 \beta_3 = 1$$

El cual podemos escribir como:

\[
\left(
\begin{array}{c c c c}
0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 \\
\end{array}
\right)
\left(
\begin{array}{c}
\beta_0 \\
\beta_1 \\
\beta_2 \\
\beta_3 \\
\end{array}
\right)
=
\left(
\begin{array}{c}
1 \\
1 \\
\end{array}
\right)
\]

En forma reducida:

$${\bf R} {\boldsymbol \beta} = q$$

Con lo cual la hip\'otesis original se puede escribir como:

$$H_0: {\bf R} {\boldsymbol \beta} = q$$

$$H_1: {\bf R} {\boldsymbol \beta} \ne q$$

Observemos que podemos afirmar que la hip\'otesis tiene dos restricciones. Regresando a nuestro caso general:

$${\bf Y} = {\bf X}{\boldsymbol \beta} + {\boldsymbol \varepsilon}$$

Por analog\'ia podr\'iamos escribir un conjunto de ``J'' restricciones como:

$$r_{10} \beta_0 + r_{11} \beta_1 + \ldots + r_{1K} \beta_K = q_1$$
$$r_{20} \beta_0 + r_{21} \beta_1 + \ldots + r_{2K} \beta_K = q_2$$
$$\vdots$$
$$r_{J0} \beta_0 + r_{J1} \beta_1 + \ldots + r_{JK} \beta_K = q_J$$

Sistema que se puede escribir en forma matricial como:

\[
\left(
\begin{array}{c c c c}
r_{10} & r_{11} & \ldots & r_{1K} \\
r_{20} & r_{21} & \ldots & r_{2K} \\
\vdots & \vdots & \ldots & \vdots \\
r_{J0} & r_{J1} & \ldots & r_{JK} \\
\end{array}
\right)
\left(
\begin{array}{c}
\beta_0 \\
\beta_1 \\
\vdots \\
\beta_3 \\
\end{array}
\right)
=
\left(
\begin{array}{c}
q_1 \\
q_2 \\
\vdots \\
q_J \\
\end{array}
\right)
\]

De esta forma podemos, finalmente, escribir una hip\'otesis general:

$$H_0: {\bf R} {\boldsymbol \beta} = q$$

$$H_1: No \medspace H_0$$

Dicho lol anterior, el restante argumento versa sobre c\'omo hacer uso de estas restricciones conjuntas.

\subsection{Prueba F}

Cuando deseamos evaluar una hip\'otesis con m\'as de una restricci\'on se debe ocupar la prueba F. La cual se puede escribir como:

$$F_{[J, n-K]} = \frac{({\bf R}{\boldsymbol \beta} - {\bf q})' [s^2 {\bf R} ({\bf X'X})^{-1} {\bf R}'] ({\bf R}{\boldsymbol \beta} - {\bf q})}{J}$$

Esta estad\'istica se distribuye como una F de Fisher con $J$ y $n-K$ grados de libertad.

\subsection{Prueba t}

Cuando deseamos evaluar una hip\'otesis con solo una restricci\'on se debe ocupar la prueba t. La cual se puede escribir como:

$$t_{[n-K, \alpha/2]} = ({\bf R}{\boldsymbol \beta} - {\bf q})' [s^2 {\bf R} ({\bf X'X})^{-1} {\bf R}'] ({\bf R}{\boldsymbol \beta} - {\bf q})$$

Esta estad\'istica se distribuye como una t con $n-K$ grados de libertad.
