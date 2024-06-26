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









# Modelos multivariados de volatilidad: $M - ARCH$ y $M - GARCH$

\chapter{Cointegración}

Hasta ahora en el curso hemos usado el supuesto de que las series son estacionarias para el conjunto de técnicas $ARMA(p,q)$ y $VAR(p)$. No obstante, dado que relajamos el supuesto de estacionariedad (incluyendo la estacionariedad en varianza) y que establecimos una serie de pruebas para determinar cuando una serie es estadísticamente estacionaria, ahora podemos plantear una técnica llamada Cointegración. Para esta técnica consideraremos sólo series que son $I(1)$ y reconoceremos que se originó con los trabajos de Engle y Granger (1987), Stock (1987) y Johansen (1988).

## Definición y propiedades del proceso de cointegración

Cointegración puede ser caracterizada o definida en palabras sencillas como que dos o más variables tienen una relación común estable en el largo plazo. Es decir, estas no suelen tomar caminos o trayectorias diferentes, excepto por periodos de tiempo transitorios y eventuales. A continuación, utilizaremos la definición de Engle y Grnager (1984) de cointegración.

Sea $\mathbf{Y}$ un vector de k-series de tiempo, decimos que los elementos en $\mathbf{Y}$ están cointegrados en un orden (d, c), es decir, $\mathbf{Y} \sim CI(d, c)$, si todos los elementos de $\mathbf{Y}$ son series integradas de orden d, I(d), y si existe al menos una combinación lineal no trivial $\mathbf{Z}$ de esas variables que es de orden I(d - c), donde $d \geq c > 0$, si y sólo si:
$$
    \boldsymbol{\beta}_i' \mathbf{Y}_t = \mathbf{Y}_{it} \sim I(d-c)
$$

Donde $i = 1, 2, \ldots, r$ y $r < k$.

A los diferentes vectores $\boldsymbol{\beta}_i$ se les denomina como vectores de cointegración. El rango de la matriz de vectores de cointegración $r$ es el número de vectores de cointegración linealmente independientes. En general diremos que los vectores de la matriz de cointegración $\boldsymbol{\beta}$ tendrá la forma de:
$$
    \boldsymbol{\beta}' \mathbf{Y}_t = \mathbf{Z}_t
$$

Antes de continuar hagamos algunas observaciones. Si todas las variables de $\mathbf{Y}$ son I(1) y $0 \leq r < k$, diremos que las series no cointegran si $r = 0$. Si esto pasa, entonces, como demostraremos más adelante, la mejor opción será estimar un modelo VAR(p) en diferencias. Adicionalmente, asumiremos que $c = d = 1$, por lo que la relación de cointegración, en su caso, generará combinaciones lineales $\mathbf{Z}$ estacionarias.

## Cointegración para modelos de más de una ecuación o para modelos basados en Vectores Autoregresivos

Sean $Y_1, Y_2, \ldots, Y_k$ son series que forman $\mathbf{Y}$ y que todas son I(1), entonces los siguientes casos son posibles:
\begin{enumerate}
    \item Si $r = 1$ entonces se trata de un caso de cointegración de Granger.
    \item Si $r \geq 1$ entonces se trata de un caso de cointegración múltiple de Johansen.
\end{enumerate}

Por lo anterior, en este curso analizaremos el caso de Cointegración de Johansen. Ahora plantearemos la forma de estimar el proceso de cointgración. El primer paso para ello es determinar un modelo VAR(p) con las k-series no estacionarias (series en niveles). Alegimos el valor de $p$ mediante el uso de los criterios de información. De esta forma tendremos una especificación similar a:
$$
    \mathbf{Y}_t = \sum_{j=1}^p \mathbf{A}_j \mathbf{Y}_{t-j} + \mathbf{D}_t + \mathbf{U}_t
    \label{VAR_CI}
$$

Donde $\mathbf{U}_t$ es un término de error k-dimensional puramente aleatorio; $\mathbf{D}_t$ contiene los compeoentes deterministicos de constante y tendencia, y $\mathbf{A}_i$, $i = 1, 2, \ldots, p$, son matrices de $k \times k$ coeficientes. Notemos que el VAR(p) involucrado en este caso, a diferencia del VAR anteriormente estudiado, puede incluir un término de tendencia. Esto en razón de que hemos relajado el concepto de estacionariedad.

Si reescribimos la ecuación (\ref{VAR_CI}) en su forma de Vector Corrector de Errores (VEC, por sus siglas en inglés) tenemos:
\begin{eqnarray}
    \mathbf{Y}_t - \mathbf{Y}_{t-1} & = & \Delta \mathbf{Y}_t \nonumber \\
    & = & \sum_{j=1}^p \mathbf{A}_j \mathbf{Y}_{t-j} + \mathbf{D}_t - \mathbf{Y}_{t-1} + \mathbf{U}_t \nonumber \\
    & = & (\mathbf{A}_1 - \mathbf{I}) \mathbf{Y}_{t-1} + \mathbf{A}_2 \mathbf{Y}_{t-2} + \ldots + \mathbf{A}_p \mathbf{Y}_{t-p} + \mathbf{D}_t + \mathbf{U}_t \nonumber \\
    & = & \left( \sum_{j=1}^{p} \mathbf{A}_j - \mathbf{I} \right) \mathbf{Y}_{t-1} + \sum_{j=1}^{p-1} \mathbf{A}^*_j \Delta \mathbf{Y}_{t-j} + \mathbf{D}_t \mathbf{U}_t \nonumber \\
    & = & - \left( \mathbf{I} - \sum_{j=1}^{p} \mathbf{A}_j \right) \mathbf{Y}_{t-1} + \sum_{j=1}^{p-1} \mathbf{A}^*_j \Delta \mathbf{Y}_{t-j} + \mathbf{D}_t \mathbf{U}_t \nonumber \\
    \Delta \mathbf{Y}_t & = & - \Pi \mathbf{Y}_{t-1} + \sum_{j=1}^{p-1} \mathbf{A}^*_j \Delta \mathbf{Y}_{t-j} + \mathbf{D}_t + \mathbf{U}_t
    \label{VAR_VEC}
\end{eqnarray}

Donde $\mathbf{A}_j^* = - \sum_{i=j+1}^p \mathbf{A}_i$, $i = 1, 2, \ldots, p-1$, y la matriz $\Pi$ representa todas las relaciones de largo plazo entre las variables, por lo que la matriz es de rango completo $k \times k$. Por lo tanto, tenemos que dicha matriz en la ecuación (\ref{VAR_VEC}) se puede factorizar como:
$$
    \Pi_{(k \times k)} = \Gamma_{(k \times r)} \boldsymbol{\beta}_{(r \times k)}'
    \label{Pi_Matrix}
$$

Donde $\boldsymbol{\beta}_{(r \times k)}' \mathbf{Y}_{t-1}$ son $r$ combinaciones linealmente independientes que son estacionarias.

Dada la ecuación (\ref{VAR_VEC}) podemos establecer la aproximación de Johansen (1988) que se realiza mediante una estimación por Máxima Verosimilitud de la ecuación:
$$
    \Delta \mathbf{Y}_t + \Gamma \boldsymbol{\beta}' \mathbf{Y}_{t-1} = \sum_{j=1}^{p-1} \mathbf{A}^*_j \Delta \mathbf{Y}_{t-j} + \mathbf{D}_t + \mathbf{U}_t
$$

Donde una vez estimado el sistema:
$$
    \boldsymbol{\beta} = [v_1, v_2, \ldots, v_r]
$$

Cada $v_i$, $i = 1, 2, \ldots, r$, es un vector propio que asociado a los $r$ valores propios positivos, mismos que estás asociados con la prueba de hipótesis de cointegración. Dicha hipótesis está basada en dos estadísticas con las que se determina el rango $r$ de $\Pi$:
\begin{enumerate}
    \item Prueba de Traza:
    
    $H_0 :$ Existen al menos $r$ valores propios positivos o Existen al menos $r$ relaciones de largo plazo estacionarias.
    
    \item Prueba del valor propio máximo o $\lambda_{max}$:
    
    $H_0 :$ Existen $r$ valores propios positivos o Existen $r$ relaciones de largo plazo estacionarias.
\end{enumerate}

## Ejemplo de cointegración

Para ejemplificar el procedimiento de cointegración utilizaremos las series de INPC, Tipo de Cambio, rendimiento de los Cetes a 28 días, IGAE e Índice de Producción Industrial de Estados Unidos. Quizá el marco teórico de la relación entre las variables no sea del todo correcta, pero dejando de lado ese problema estimaremos si las 5 series cointegran.

En el Scrip Clase 17 de la capeta de GoogleDrive se encuentra el desarrollo de este ejemplo. Por principio, probaremos que todas las series son I(1), lo cual es cierto (ver Scrip para mayores detalles). En la Figura (\ref{G_Cointegracion}) se muestran las series en niveles y en diferencias, con lo cual ilustramos como es viable que las series sean I(1).
\begin{figure}
  \centering
    \includegraphics[width = 1.0\textwidth]{G_Cointegracion}
  \caption{Series en niveles (logatirmos) y en diferencias logarítmicas para la prueba de Cointegración.}
  \label{G_Cointegracion}
\end{figure}

Posteriormente, determinamos cuál es el orden adecuado de un VAR(p) en niveles. En el Cuadro (\ref{Select_VAR_VEC}) mostramos los resultados de los criterios de información para determinar el número de rezagos óptimos, el cual resultó en $p = 3$ para los criterios AIC y FPE, $p = 2$ para el criterio HQ y $p = 1$ para el citerio SC. Por lo tanto decidiremos utilizar un VAR(3) con tendencia y constante.
\begin{table}
\centering
\begin{tabular}{| c | c | c | c | c |}
\hline
    Rezagos & AIC & HQ & SC & FPE \\
\hline
    1 & -4.606707e+01 & -4.585260e+01 & -4.553568e+01 & 9.848467e-21 \\
    2 & -4.643287e+01 & -4.606521e+01 & -4.552191e+01 & 6.834064e-21 \\
    3 & -4.647783e+01 & -4.595697e+01 & -4.518730e+01 & 6.539757e-21 \\
    4 & -4.645834e+01 & -4.578428e+01 & -4.478824e+01 & 6.679778e-21 \\
    \vdots & \vdots & \vdots & \vdots & \vdots \\
\hline
    \multicolumn{5}{ l }{Nota: Se reporta el valor de los criterios de información.} \\
\end{tabular}
\caption{Criterios de información para diferentes especificaciones de modelos VAR(p) con término constante y tendencia de la series $LINPC_t$, $LTC_t$, $LCETE28_t$, $LIGAE_t$ y $LIPI_t$.}
\label{Select_VAR_VEC}
\end{table}

El mismo número de rezagos los utilizaremos para probar la Cointegración ya sea por una estadística de la Traza o por una de el máximo valor propio. En el Scrip llamado Clase 18 que se encuentra en la carpeta de GoogleDrive se ubican todos los resultados citados acontinuación. Derivado de la exploración de los resultados sólo matraremos uno de los caso en que las series cointegran y sólo para el caso de la prueba de la traza. En el Cuadro (\ref{Traza_Test}) reportamos los resultados del Test de Cointegración para un modelo con 3 rezagos.
\begin{table}
\centering
\begin{tabular}{| c | c | c | c | c |}
\hline
    r $\leq$ & Estadística & 10\% & 5\% & 1\% \\
\hline
    4 & 3.38 & 10.49 & 12.25 & 16.26 \\
    3 & 17.09 & 22.76 & 25.32 & 30.45 \\
    2 & 31.66 & 39.06 & 42.44 & 48.45 \\
    1 & 56.88 & 59.14 & 62.99 & 70.05 \\
    0 & 89.69 & 83.20 & 87.31 & 96.58 \\
\hline
\end{tabular}
\caption{Criterios de información para diferentes especificaciones de modelos VAR(p) con tendencia de la series $LINPC_t$, $LTC_t$, $LCETE28_t$, $LIGAE_t$ y $LIPI_t$.}
\label{Traza_Test}
\end{table}

Los resutados del Cuadro (\ref{Traza_Test}) indican que acptamos la hipótesis nula para el caso de $r \leq 1$ al $5\%$, por lo que podemos concluir que existe evidencia estadística para probar que existen al menos 1 vector de cointegración. Por lo que dicho vector es:
$$
    \boldsymbol{\beta} = \left[ 
    \begin{matrix}
    1.00000000 \\
    0.151162436 \\
    -0.042650912 \\
    0.163804862 \\
    0.229295743 \\
    -0.004350646 \\
    \end{matrix} \right]
$$

Donde el vector esta normalizado para la serie $LINPC_t$, por lo que concluímos que la relación de largo plazo que encontramos cointegra estará dada por:
\begin{eqnarray*}
    LINPC_t & = & -0.151162436 LTC_t + 0.042650912 LCETE28_t \\
    &  & - 0.163804862 LIGAE_t - 0.229295743 LIPI_t \\
    &  & + 0.004350646 t
\end{eqnarray*}

Considerando lo anterior, podemos determinar $\hat{U}_t$ para esta ecuación de cointegración. En la Figura (\ref{G_U_Cointegration}) mostramos los residuales estimados. Derivado de la impección visual parecería que estos no son estacionarios, condición que debería ser cierta. De esta forma, una prueba deseable es aplicar todas la pruebas de raíces unitarias a esta serie para mostrar que es I(0). En el Scrip llamado Clase 18 en la carpeta de GoogleDrive se muestran algunas pruebas sobre esta serie y se encuentra que es posible que no sea estacionaria.
\begin{figure}
  \centering
    \includegraphics[width = 1.0\textwidth]{G_U_Cointegration}
  \caption{Residuales estimados de la ecuación de cointegración.}
  \label{G_U_Cointegration}
\end{figure}
