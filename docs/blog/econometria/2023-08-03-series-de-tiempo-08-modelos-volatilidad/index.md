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



# Modelos Univariados y Multivariados de Volatilidad

## Modelos ARCH y GARCH Univariados

Estos modelos de Heterocedásticidad Condicional Autoregresiva (ARCH, por sus siglas en inglés) y modelos Heterocedásticidad Condicional Autoregresiva Generalizados (GARCH, por sus siglas en inglés) tienen la característica de modelar situaciones como las que ilustra la Figutra \ref{G_ARCH_Return}. Es decir: 1) existen zonas donde la variación de los datos es mayor y zonas donde la variación es más estable--a estas situaciones se les conoce como de variabilidad por clúster--, y 2) los datos corresponden a innformación de alta frecuencia.
\begin{figure}
  \centering
    \includegraphics[width = 1.0 \textwidth]{G_ARCH_Return}
  \caption{ Rendimientos (diferenccias logarítmicas) de tres acciones seleccionadas: Apple, Pfizer, Tesla, enero 2011 a noviembre de 2020}
  \label{G_ARCH_Return}
\end{figure}

Para plantear el modelo supongamos --por simplicidad-- que hemos construido y estimado un modelo AR(1). Es decir, asumamos que el proceso subyacente para la media condicional está dada por:
$$
    X_t = a_0 + a_1 X_{t-1} + U_t
$$

Donde $\abs{a_1} < 1$ para garantizar la convergencia del proceso en el largo plazo, en el cual:
\begin{eqnarray*}
    \mathbb{E}[X_t] & = & \frac{a_0 }{1 - a_1} = \mu \\
    Var[X_t] & = & \frac{\sigma^2}{1 - a_1^2}
\end{eqnarray*}

Ahora, supongamos que este tipo de modelos pueden ser extendidos y generalizados a un modelo ARMA(p, q), que incluya otras variables exogénas. Denotemos a como $\mathbf{Z}_t$ al conjunto que incluye los componentes AR, MA y variables exogénas que pueden explicar a $X_t$ de forma que el proceso estará dado por:
$$
    X_t = \mathbf{Z}_t \boldsymbol{\beta} + U_t
$$

Donde $U_t$ es un proceso estacionario que representa el error asociado a un proceso ARMA(p, q) y donde siguen diendo válidos los supuestos:
\begin{eqnarray*}
    \mathbb{E}[U_t] & = & 0 \\
    Var[U_t^2] & = & \sigma^2
\end{eqnarray*}

No obstante, en este caso podemos suponer que existe autocorrelación en el término de error que puede ser capturada por un porceso similar a uno de medias móviles (MA) dado por:
$$
    U_t^2 = \gamma_0 + \gamma_1 U_{t-1}^2 + \gamma_2 U_{t-2}^2 + \ldots + \gamma_q U_{t-q}^2 + \nu_t
$$

Donde $\nu_t$ es un ruido blanco y $U_{t-i} = X_{t-i} - \mathbf{Z}_{t-i} \boldsymbol{\beta}$, $i = 1, 2 ,\ldots $. Si bien los procesos son estacionarios por los supuestos antes enunciados, la varianza condicional estará dada por:
\begin{eqnarray*}
    \sigma^2_{t | t-1} & = & Var[ U_t | \Omega_{t-1} ] \\
    & = & \mathbb{E}[ U^2_t | \Omega_{t-1} ]
\end{eqnarray*}

Donde $\Omega_{t-1} = \{U_{t-1}, U_{t-2}, \ldots \}$ es el conjunto de toda la información pasada de $U_t$ y observada hasta el momento $t-1$, por lo que:
\begin{equation*}
    U_t | \Omega_{t-1} \sim \mathbb{D}(0, \sigma^2_{t | t-1})
\end{equation*}

Así, de forma similar a un proceso MA(q) podemos decir que la varianza condicional tendrá efectos ARCH de orden $q$ (ARCH(q)) cuando:
$$
    \sigma^2_{t | t-1} = \gamma_0 + \gamma_1 U_{t-1}^2 + \gamma_2 U_{t-2}^2 + \ldots + \gamma_q U_{t-q}^2
    \label{ARCH_Effect}
$$

Donde $\mathbb{E}[\nu_t] = 0$ y $\gamma_0$ y $\gamma_i \geq 0$, para $i = 1, 2, \ldots, q-1$ y  $\gamma_q > 0$. Estas condiciones son necesarias para garantizar que la varianza sea positiva. En general, la varianza condicional se expresa de la forma $\sigma^2_{t | t-1}$, no obstante, para facilitar la notación, nos referiremos en cada caso a esta simplemente como $\sigma^2_{t}$.

Podemos generalizar está situación si asumimos a la varianza condicional como dependiente de lo valores de la varianza rezagados, es decir, como si fuera un proceso AR de orden $p$ para la varianza y juntandolo con la ecuación (\ref{ARCH_Effect}). Bollerslev (1986) y Taylor (1986) generalizaron el problema de heterocedásticidad condicional. El modelo se conoce como GARCH(p, q), el cual se especifica como:
$$
    \sigma^2_t = \gamma_0 + \gamma_1 U_{t-1}^2 + \gamma_2 U_{t-2}^2 + \ldots + \gamma_q U_{t-q}^2 + \beta_1 \sigma^2_{t-1} + \beta_2 \sigma^2_{t-2} + \ldots + \beta_p \sigma^2_{t-p}
    \label{GARCH_Effect}
$$

Donde las condiciones de no negatividad son que $\gamma_0 > 0$, $\gamma_i \geq 0$, $i = 1, 2, \ldots, q-1$, $\beta_j \geq 0$, $j = 1, 2, \ldots, p-1$, $\gamma_q > 0$ y $\beta_p > 0$. Además, otra condición de convergencia es que:
\begin{equation*}
    \gamma_1 + \ldots + \gamma_q + \beta_1 + \ldots + \beta_p < 1
\end{equation*}

Usando el operador rezago $L$ en la ecuación (\ref{GARCH_Effect}) podemos obtener:
$$
    \sigma^2_t = \gamma_0 + \alpha(L) U_t^2 + \beta(L) \sigma^2_t
    \label{GARCH_Effect_L}
$$

De donde podemos establecer:
$$
    \sigma^2_t = \frac{\gamma_0}{1 - \beta(L)} + \frac{\alpha(L)}{1 - \beta(L)} U_t^2 
$$

Por lo que la ecuación (\ref{GARCH_Effect}) del GARCH(p, q) representa un ARCH($\infty$):
$$
    \sigma^2_t = \frac{a_0}{1 - b_1 - b_2 - \ldots - b_p} + \sum_{i = 1}^\infty U_{t-i}^2 
$$

## Modelos ARCH y GARCH Multivariados

De forma similar a los modelo univariados, los modelos multivariados de heterocedásticidad condicional asumen una estructura de la media condicional. En este caso, descrita por un VAR(p) cuyo proceso estocástico $\mathbf{X}$ es estacionario de dimensión $k$. De esta forma la expresión reducida del modelo o el proceso VAR(p) estará dado por:
$$
    \mathbf{X}_t = \mathbf{\delta} + A_1 \mathbf{X}_{t-1} + A_2 \mathbf{X}_{t-2} + \ldots + A_p \mathbf{X}_{t-p} + \mathbf{U}_{t}
$$

Donde cada uno de las $A_i$, $i = 1, 2, \ldots, p$, son matrices cuadradas de dimensión $k$ y $\mathbf{U}_t$ representa un vector de dimensión $k \times 1$ con los residuales en el momento del tiempo $t$ que son un proceso pueramente aleatorio. También se incorpora un vector de términos constantes denominado como $\mathbf{\delta}$, el cual es de dimensión $k \times 1$ --es este caso también es posible incorporar procesos determinas adicionales--.

Así, suponemos que el término de error tendra estructura de vector:
\begin{equation*}
    \mathbf{U}_t = 
    \begin{bmatrix}
    U_{1t} \\ U_{2t} \\ \vdots \\ U_{Kt}
    \end{bmatrix}
\end{equation*}

De forma que diremos que:
\begin{equation*}
    \mathbf{U}_t | \Omega_{t-1} \sim (0, \Sigma_{t | t-1})
\end{equation*}

Dicho lo anterior, entonces, el mode ARCH(q) multivariado será descrito por:
$$
    Vech(\Sigma_{t | t-1}) = \boldsymbol{\gamma}_0 + \Gamma_1 Vech(\mathbf{U}_{t-1} \mathbf{U}_{t-1}') + \ldots + \Gamma_q Vech(\mathbf{U}_{t-q} \mathbf{U}_{t-q}')
    \label{M_ARCH}
$$

Donde $Vech$ es un operador que apila en un vector la parte superior de la matriz a la cual se le aplique, $\boldsymbol{\gamma}_0$ es un vector de cosntantes, $\Gamma_i$, $i = 1, 2, \ldots$ son matrices de coeficientes asociados a la estimación.

Para ilustrar la ecuación (\ref{M_ARCH}), tomemos un ejemplo de $K = 2$, de esta forma tenemos que un M-ARCH(1) será:
\begin{equation*}
    \Sigma_{t | t-1} = 
    \begin{bmatrix}
    \sigma^2_{1, t | t-1} & \sigma_{12, t | t-1} \\ \sigma_{21, t | t-1} & \sigma^2_{2, t | t-1}
    \end{bmatrix} = 
    \begin{bmatrix}
    \sigma_{11, t} & \sigma_{12, t} \\ \sigma_{21, t} & \sigma_{22, t}
    \end{bmatrix} =
    \Sigma_{t}
\end{equation*}

Donde hemos simplificado la notación de la varianzas y la condición de que están en función de $t-1$. Así,
\begin{equation*}
    Vech(\Sigma_{t}) = 
    Vech \begin{bmatrix}
    \sigma_{11, t} & \sigma_{12, t} \\ \sigma_{21, t} & \sigma_{22, t}
    \end{bmatrix} =
    \begin{bmatrix}
    \sigma_{11, t} \\ \sigma_{12, t} \\ \sigma_{22, t}
    \end{bmatrix}
\end{equation*}

De esta forma, podemos establecer el modelo M-ARCH(1) con $K = 2$ será de la forma:
\begin{equation*}
    \begin{bmatrix}
    \sigma_{11, t} \\ \sigma_{12, t} \\ \sigma_{22, t}
    \end{bmatrix} =
    \begin{bmatrix}
    \gamma_{10} \\ \gamma_{20} \\ \gamma_{30}
    \end{bmatrix} +
    \begin{bmatrix}
    \gamma_{11} & \gamma_{12} & \gamma_{13} \\ \gamma_{21} & \gamma_{22} & \gamma_{23} \\ \gamma_{31} & \gamma_{32} & \gamma_{33}
    \end{bmatrix} 
    \begin{bmatrix}
    U^2_{1, t-1} \\ U_{1, t-1} U_{2, t-1} \\ U^2_{2, t-1}
    \end{bmatrix}
\end{equation*}

Como notarán este tipo de procedimientos implica la estimación de muchos paramétros. En este circunstacia, se suelen estimar modelos restringidos para reducir el número de coeficientes estimados. por ejemplo, podríamos querer estimar un caso como:
\begin{equation*}
    \begin{bmatrix}
    \sigma_{11, t} \\ \sigma_{12, t} \\ \sigma_{22, t}
    \end{bmatrix} =
    \begin{bmatrix}
    \gamma_{10} \\ \gamma_{20} \\ \gamma_{30}
    \end{bmatrix} +
    \begin{bmatrix}
    \gamma_{11} & 0 & 0 \\ 0 & \gamma_{22} & 0 \\ 0 & 0 & \gamma_{33}
    \end{bmatrix} 
    \begin{bmatrix}
    U^2_{1, t-1} \\ U_{1, t-1} U_{2, t-1} \\ U^2_{2, t-1}
    \end{bmatrix}
\end{equation*}

Finalmente y de forma analóga al caso univariado, podemos plantear un modelo M-GARCH(p, q) como:
$$
    Vech(\Sigma_{t | t-1}) = \boldsymbol{\gamma}_0 + \sum_{j = 1}^q \Gamma_j Vech(\mathbf{U}_{t-j} \mathbf{U}_{t-j}') + \sum_{m = 1}^p \mathbf{G}_m Vech(\Sigma_{t-m | t-m-1})
    \label{M_GARCH}
$$

Donde cada una de las $\mathbf{G}_m$ es una matriz de coeficientes. Para ilustrar este caso retomemos el ejemplo anterior pera ahora para un modelo M-GARCH(1, 1) con $K = 2$ de formaque tendríamos:
\begin{equation*}
    \begin{bmatrix}
    \sigma_{11, t} \\ \sigma_{12, t} \\ \sigma_{22, t}
    \end{bmatrix} =
    \begin{bmatrix}
    \gamma_{10} \\ \gamma_{20} \\ \gamma_{30}
    \end{bmatrix} +
    \begin{bmatrix}
    \gamma_{11} & \gamma_{12} & \gamma_{13} \\ \gamma_{21} & \gamma_{22} & \gamma_{23} \\ \gamma_{31} & \gamma_{32} & \gamma_{33}
    \end{bmatrix} 
    \begin{bmatrix}
    U^2_{1, t-1} \\ U_{1, t-1} U_{2, t-1} \\ U^2_{2, t-1}
    \end{bmatrix} +
    \begin{bmatrix}
    g_{11} & g_{12} & g_{13} \\ g_{21} & g_{22} & g_{23} \\ g_{31} & g_{32} & g_{33}
    \end{bmatrix} 
    \begin{bmatrix}
    \sigma_{11, t-1} \\ \sigma_{12, t-1} \\ \sigma_{22, t-1}
    \end{bmatrix}
\end{equation*}

## Pruebas para detectar efectos ARCH

La prueba que mostraremos es conocida como una ARCH-LM, la cual está basada en una regresión de los residuales estimados de un modelo VAR(p) o cualquier otra estimación que deseemos probar, con el objeto de determinar si existen efectos ARCH --esta prueba se puede simplificar para el caso univariado--.

Partamos de platear:
$$
    Vech(\hat{\mathbf{U}}_t \hat{\mathbf{U}}_t') = \mathbf{B}_0 + \mathbf{B}_1 Vech(\hat{\mathbf{U}}_{t-1} \hat{\mathbf{U}}_{t-1}') + \ldots + \mathbf{B}_q Vech(\hat{\mathbf{U}}_{t-q} \hat{\mathbf{U}}_{t-q}') + \varepsilon_t
    \label{ARCH-LM}
$$

Dada la estimación en la ecuación (\ref{ARCH-LM}), plantemos la estructura de hipótesis dada por:
\begin{eqnarray*}
    H_0 & : & \mathbf{B}_1 = \mathbf{B}_2 = \ldots = \mathbf{B}_q = 0 \\
    H_a & : & No H_0    
\end{eqnarray*}

La estadística de prueba será determinada por:
$$
    LM_{M-ARCH} = \frac{1}{2} T K (K + 1) - Traza \left( \hat{\Sigma}_{ARCH} \hat{\Sigma}^{-1}_{0} \right) \sim \chi^2_{[q K^2 (K + 1)^2 / 4]}
$$

Donde la matriz $\hat{\Sigma}_{ARCH}$ es calcula de acuerdo con la ecuación (\ref{ARCH-LM}) y la matriz $\hat{\Sigma}_{0}$ sin considerar una estructura dada para los errores.
