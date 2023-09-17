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




# Otros Modelos de Series de Tiempo No lineales


## Modelos de cambio de régimen

En años recientes, los modelos de serie de tiempo han sido incorporados en análisis de la existencia de diferentes estados que son generados por procesos estocásticos subyacentes. En esta sección del curso revisaremos algunos modelos de cambio de regimen. Restringimos nuestra revisión a modelos que asuman que la dinámica de las series puede ser descrito por modelos del tipo AR y dejamos fuera procesos del tipo MA.

En general distinguimos que existen dos tipos de modelos:
\begin{enumerate}
    \item Modelos caracterizados por una variable observable, por lo que tenemos certeza de los régimanes en cada uno de los momentos.
    
    \item Modelos en los que el régimen no puede ser observado por una variable, pero si conocemos el proceso estocástico subyacente. 
\end{enumerate}

### Regímenes determinados por información observable

En estos casos asumimos que el régimen ocurren en un momento $t$ y puede ser determinado por una variable observable. Este modelo es conocido como el modelo autoregresivo con umbral (TAR, Threshold Autoregressive model). En este caso también diremos que cuando el régimen está determinado por la información de la misma serie será llamdao Self-Exciting TAR (SETAR).

Veámos un ejemplo. Supongamos que existe un umbral, $c$, para el régimen que esta determinado por $q_t = y_{t-1}$ y que el estado de la naturaleza nos permite establecer dos estados o regímenes:
$$
    y_t = 
    \begin{cases}
        \phi_{01} + \phi_{11} y_{t-1} + \varepsilon_t \text{ si } y_{t-1} \leq c \\
        \phi_{02} + \phi_{12} y_{t-1} + \varepsilon_t \text{ si } y_{t-1} > c 
    \end{cases}
$$

Donde asumiremos que $\varepsilon_t$ es i.i.d y que cumple con:
\begin{equation*}
    \mathbb{E}[\varepsilon_t | \Omega_{t-1}] = 0
\end{equation*}

Donde $\Omega_{t-1} = \{ y_{t-1}, y_{t-2}, \ldots \}$. Existe una variante de este modelo que suaviza la transición entre regímenes conocido como Smooth Transition AR (STAR) y puede ser especificado en su modalidad de dos regémenes como:
$$
    y_t = (\phi_{01} + \phi_{11} y_{t-1}) (1 - G(y_{t-1}; \gamma, c)) + (\phi_{02} + \phi_{12} y_{t-1}) G(y_{t-1}; \gamma, c) + \varepsilon_t
$$

Donde $G(y_{t-1}; \gamma, c)$ es una función de distribución de probabilidad que suviza la transición entre regímenes. La práctica común es suponer que está tiene una forma logística:
$$
    G(y_{t-1}; \gamma, c) = \frac{1}{1 + e^{-\gamma (y_{t-1} - c)}}
$$

Es posible hacer estensiones de lo anterior a modelos de orden superior dando como resultado:
$$
    y_t = 
    \begin{cases}
        \phi_{01} + \phi_{11} y_{t-1} + \phi_{21} y_{t-2} + \ldots + \phi_{p_1 1} y_{t-p_1} + \varepsilon_t \text{ si } y_{t-1} \leq c \\
        \phi_{02} + \phi_{12} y_{t-1} + \phi_{22} y_{t-2} + \ldots + \phi_{p_2 2} y_{t-p_2} + \varepsilon_t \text{ si } y_{t-1} > c 
    \end{cases}
$$

En el segundo caso:
\begin{eqnarray*}
    y_t & = & (\phi_{01} + \phi_{11} y_{t-1} + \phi_{21} y_{t-2} + \ldots + \phi_{p_1 1} y_{t-p_1}) (1 - G(y_{t-1}; \gamma, c)) \\
    &  & + (\phi_{02} + \phi_{12} y_{t-1} + \phi_{22} y_{t-2} + \ldots + \phi_{p_2 2} y_{t-p_2}) G(y_{t-1}; \gamma, c) \\
    &  & + \varepsilon_t
\end{eqnarray*}

De igual forma que en el caso de los modelos ARIMA y VAR, el número de rrezagos utilizados es determinado mediennte el uso de criterios de información como el de Akaike:
$$
    AIC(p_1, p_2) = n_1 ln(\hat{\sigma}^2_1) + n_2 ln(\hat{\sigma}^2_2) + 2(p_1 + 1) + 2(p_2 + 1)
$$

Los modelos SETAR y STAR generan procesos estacionarios siempre que cumplan ciertas condiciones. En estas notas nos enfocaremos únicamente en el modelo SETAR el cual genera en un proceso estacionario cuando:
\begin{enumerate}
    \item $\phi_{11} < 1$, $\phi_{12} < 1$, $\phi_{11} \cdot \phi_{12} < 1$
    
    \item $\phi_{11} = 1$, $\phi_{12} < 1$, $\phi_{01} > 0$
    
    \item $\phi_{11} < 1$, $\phi_{12} = 1$, $\phi_{02} < 0$
    
    \item $\phi_{11} = 1$, $\phi_{12} = 1$, $\phi_{02} < 0 < \phi_{01}$
    
    \item $\phi_{11} \cdot \phi_{12} = 1$, $\phi_{11} < 0$, $\phi_{02} + \phi_{12} \cdot \phi_{01} > 0$
\end{enumerate}

Finalmente, en ocasiones podemos estar interesados en modelos donde los regímenes sean más de 2, es decir, digamos $m$ umbrales bajo un modelo SETAR o STAR. Por ejemplo, en el caso de un modelo SETAR podemos verificar que $m$ regímnes implican $m + 1$ umbrales: $c_0, c_1, \ldots, c_m$. En cuyo caso:
\begin{equation*}
    -\infty = c_0 < c_1 < \ldots < c_{m-1} < c_m = \infty
\end{equation*}

Así, tendríamos ecuaciones:
$$
    y_t = \phi_{0j} + \phi_{ij} y_{t-1} + \varepsilon_t \text{ si } c_{j-1} < y_{t-1} < c_j
$$

Para $j = 1, 2, \ldots, m$. De forma similar podemos recomponer el modelo STAR.

### Regímenes determinados por variables no observables

Este tipo de modelosmasume que el regímen ocurre en el momento $t$ y que no puede ser observado, ya que este es determinado por un proceso no observable, el cual denotamos como $s_t$. En el caso de dos regímenes, $s_t$ puede ser asumido como que toma 2 valores: 1 y 2, por ejemplo. Supongamos que el proceso subyacente tiene una forma del tipo AR(1) dado por:
$$
    y_t = 
    \begin{cases}
        \phi_{01} + \phi_{11} y_{t-1} + \varepsilon_t \text{ si } s_t = 1 \\
        \phi_{02} + \phi_{12} y_{t-1} + \varepsilon_t \text{ si } s_t = 2
    \end{cases}
    \label{eq_swching_obs}
$$

O en un formato más corto de notación:
$$
    y_t = \phi_{0 s_t} + \phi_{1 s_t} y_{t-1} + \varepsilon_t
$$

Para complementar el modelo, las propiedades del proceso $s_t$ necesitan ser especificadas. El modelo más popular dentro de esta familia es el propuesto por James Hamilton en 1989 el cual es conocido como Markov Switching Model (MSM), en el cual el proceso $s_t$ se asume como un proceso de Markov de primer orden. Esto implica que el regímen actula $s_t$ sólo dependen del período $s_{t-1}$. 

Así, el modelo es completado mediante la definición de las probabilidades de transición para moverse del un estado a otro:
\begin{eqnarray*}
    \mathbb{P}(s_t = 1 | s_{t-1} = 1) & = & p_{11} \\
    \mathbb{P}(s_t = 2 | s_{t-1} = 1) & = & p_{12} \\
    \mathbb{P}(s_t = 1 | s_{t-1} = 2) & = & p_{21} \\
    \mathbb{P}(s_t = 2 | s_{t-1} = 2) & = & p_{22} 
\end{eqnarray*}

Así, $p_{ij}$ es igual a la probabilidad de que la cadena de Markov pase del estado $i$ en el momento $t-1$ al estdo $j$ en el tiempo $t$. En todo caso asumiremos que $p_{ij} > 0$ y que:
\begin{eqnarray*}
    p_{11} + p_{12} = 1 \\
    p_{21} + p_{22} = 1 
\end{eqnarray*}

Otro tipo de probabilidades a analizar son las probabilidades incondicionales de $\mathbb{P}(s_t = i)$, $i = 1, 2$. Usando la teoría ergódica de la cadenas de Markov, estas probabilidades están dadas por:
\begin{eqnarray*}
    \mathbb{P}(s_t = 1) & = & \frac{1 - p_{22}}{2 - p_{11} - p_{22}} \\ 
    \mathbb{P}(s_t = 2) & = & \frac{1 - p_{11}}{2 - p_{11} - p_{22}}
\end{eqnarray*}

Un caso más general es el de múltiples regímenes en el cual $s_t$ puede tomar cualquier valor $m > 2$, $m \in \mathbb{N}$. Este modelo se puede escribir como:
$$
    y_t = \phi_{0j} + \phi_{1j} y_{t-1} + \varepsilon_t \text{ si } s_t = j \text{, para } j = 1, 2, \ldots, m
$$

Donde las probabilidades de transición estarán dadas por:
$$
    p_{ij} = \mathbb{P}(s_t = j | s_{t-1} = i) \text{ para } i , j = 1, 2, \ldots, m
$$

Donde la ecuación anterior satisface que $p_{ij} > 0$, $\forall i, j = = 1, 2, \ldots, m$ y que:
\begin{equation*}
    \sum_{j=1}^m p_{ij} = 1 \text{ para } i = 1, 2, \ldots, m
\end{equation*}

Finalmente, plantearemos el procedimiento empiríco seguido para la estimación de este tipo de modelos:
\begin{enumerate}
    \item Estimar un proceso AR(p)
    
    \item Probar una hipótesis nula de no linealidad de acurdo con alguno de los modelos SERAR, STAR o MSM
    
    \item Estimar lo parámetros
    
    \item Evluar los resultados del modelo
    
    \item Ajustar, en su caso, la estimación o modelo
    
    \item Pronósticar o realizar análisis impluso-respuesta
\end{enumerate}
