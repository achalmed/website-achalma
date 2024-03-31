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






# Modelos ADRL

## Teoría

Una vez que hemos analizado diversas técnicas de series de tiempo, el problema consiste en seleccionar el modelo correcto. La Figura \ref{TimeSeries_Models} muestra un esquema o diagrama de cómo podríamos proceder para seleccionar el modelo correcto.
\begin{figure}
  \centering
    \includegraphics[width = 1.0 \textwidth]{TimeSeries_Models}
  \caption{ Method selection for time series data. OLS: Ordinary least squares; VAR: Vector autoregressive; ARDL: Autoregressive distributed lags; ECM: Error correction models, retomado de: Shrestha y Bhatta (2018) }
  \label{TimeSeries_Models}
\end{figure}

En este caso incorporaremos a los modelos autogregressive distributed lag models (ARDL, por sus siglas en inglés). En estos casos el procedimiento de Johansen no podría aplicarse directamennte cuando las variables incluidas son de un orden mixto o cuando simplemente todas no son estacionarias. Un modelo ARDL está basado en procedimientos de MCO.

Este tipo de modelos toma suficientes rezagos para capturar el mecanismo generador de datos. También es posible llegar a una especificación del mecanismo corrector de errores a partir de una trasformación lineal del ARDL. 

Consideremos la siguiente ecuación:
$$
    Y_t = \alpha + \delta X_t + \gamma Z_t + U_t
    \label{Eq_ARDL}
$$

Dada la ecuación (\ref{Eq_ARDL}) podemos establecer su forma de mecanismo corrector de errores en forma ARDL dada por:
\begin{eqnarray*}
    \Delta Y_t & = & \alpha + \sum_{i = 1}^p \beta_i \Delta Y_{t-i} + \sum_{i = 1}^p \delta_i \Delta X_{t-i} + \sum_{i = 1}^p \gamma_i \Delta Z_{t-i} \\ 
    &  & + \lambda_1 Y_{t-1} + \lambda_2 X_{t-1} + \lambda_3 Z_{t-1} + U_t
\end{eqnarray*}

Donde los coeficientes $\beta_i$, $\delta_i$, $\gamma_i$ representan la dinámica de corto plazo y las $\lambda$'s la dinámica de largo plazo.

La hipótesis nula ($H_0$) es que las $\lambda_1 + \lambda_2 + \lambda_3 = 0$, es decir, que no existe relación de largo plazo.

En la práctica estimamos una especificación con rezafos distribuidos:
$$
    Y_t = \alpha + \sum_{i = 1}^p \beta_i Y_{t-i} + \sum_{i = 1}^p \delta_i X_{t-i} + \sum_{i = 1}^p \gamma_i Z_{t-i} + U_t
$$

Además de verificar si las series involucradas son estacionarias y decidir el número de reagos $p$ mediante criterios de información.

## Ejemplo
