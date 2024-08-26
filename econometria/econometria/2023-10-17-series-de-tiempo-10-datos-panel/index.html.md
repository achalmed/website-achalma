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









# Modelos de Datos Panel

## Motivación

Denotemos con $Y_{it}$  el componente o individuo $i$, $i = 1, 2, \ldots, N$ en el tiempo $t$, $t = 1, 2, \ldots, T$. Típicamente las series de tiempo en forma de panel se caracterizan por ser de dimensión de individuos corta y de dimensión temporar larga. 

En general, escribiremos:
$$
    Y_{it} = \alpha_i + \beta_i X_{it} + U_{it}
$$

Donde $\alpha_i$ es un efecto fijo especificado como:
$$
    \alpha_i = \beta_0 + \gamma_i Z_i
$$

## Pruebas de Raíces Unitarias en Panel

Las pruebas de raíces unitarias para panel suelen ser usadas  principalmente en casos macroeconómicos. De forma similar al caso de series univariadas, asumiremos una forma de AR(1) para una serie en panel:
$$
    \Delta Y_{it} = \mu_i + \rho_i Y_{i t-1} + \sum_{i = 1}^{k_i} \varphi_{ij} \Delta Y_{i t-j} + \varepsilon_{it}
    \label{eq_AR_Panel}
$$

Donde $i = 1, \ldots, N$, $t = 1, \ldots, T$ y $\varepsilon_{it}$ es una v.a. iid que cumple con:
\begin{eqnarray*}
    \mathbb{E}[\varepsilon_{it}] & = & 0 \\
    \mathbb{E}[\varepsilon_{it}^2] & = & \sigma^2_i < \infty \\
    \mathbb{E}[\varepsilon_{it}^4] & < & \infty 
\end{eqnarray*}

Al igual que en el caso univariado, en este tipo de pruebas buscamos identificar cuando las series son I(1) y cuando I(0). Pasra tal efecto, la prueba de raíz unitaria que utilizaremos está basada en una prueba  Dickey-Fuller Aumentada en la cual la hipótesis nula ($H_0$) es que todas las series en el panel son no estacionarias, es decir, son I(1). Es decir,
$$
    H_0 : \rho_i = 0
$$

Por su parte, en el caso de la hipótesis nula tenndremos dos:
\begin{itemize}
    \item $H_1^A :$ Todas las series son I(0) -- caso homogéneo, o
    
    \item $H_1^B :$ Al menos una de las series es I(0) -- caso heterogéneo
\end{itemize}

## Panel VAR

En esta sección extenderemos el caso del modelo VAR(p) a uno en forma panel. En este caso asumimos que las viables exogenas son los $p$ rezagos de las $k$ variables endogenas. Consideremos el siguiente caso de un modelo panel VAR con efectos fijos --ciertamente es posible hacer estimaciones con efectos aleatorios, no obstante requiere de supuestos adicionales que no contemplamos en estas notas --, el cual es la forma más común de estimación:
$$
    \mathbf{Y}_{it} = \mu_i + \sum_{l = 1}^p \mathbf{A}_l \mathbf{Y}_{i t - l} + \mathbf{B} \mathbf{X}_{it} + \varepsilon_{it}
    \label{eq_PVAR}
$$

Donde $\mathbf{Y}_{it}$ es un vector de variables endogenas estacionarias para la unidad de corte transversal $i$ en el tiempo $t$, $\mathbf{X}_{it}$ es una matriz que contiene varaibles exógenas, y $\varepsilon_{it}$ es un término de error que cumple con:
\begin{eqnarray*}
    \mathbb{E}[\varepsilon_{it}] & = & 0 \\
    Var[\varepsilon_{it}] & = & \Sigma_\varepsilon
\end{eqnarray*}

Donde $\Sigma_\varepsilon$ es una matriz definida positiva.

Para el porceso de estimación la ecuación (\ref{eq_PVAR}) se modifica en su versión en diferencias para quedar como:
$$
    \Delta \mathbf{Y}_{it} = \sum_{l = 1}^p \mathbf{A}_l \Delta \mathbf{Y}_{i t - l} + \mathbf{B} \Delta \mathbf{X}_{it} + \Delta \varepsilon_{it}
    \label{eq_Dinamic_PVAR}
$$

La ecuación (\ref{eq_Dinamic_PVAR}) se estima por un GMM.

## Cointegración







