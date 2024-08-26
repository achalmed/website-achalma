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









# Procesos No Estacionarios

## Definición y formas de No Estacionariedad

Hasta ahora hemos planteado una serie de ténicas de regresión que aplican sólo a procesos o series estacionarias. En esta sección relajaremos la definición de estacionariedad y plantearemos pruebas para determinar cuando una serie es estacionaria bajo tres diferentes especificiones: (1) estacionariedad al rededor de una tendencia determinística; (2) estacionariedad al rededor de una media, y (3) estacionariedad al rededor del cero.

A continuación discutiremos cómo es posible que una serie sea estacionaria al rededor de una tendencia determinística. Diremos que una tendencia es determinística si ésta puede ser aproximada o modelada por un polinomio en función de $t$, la cual incluye posibles transformaciones logarítmicas.

Bajo este enfoque, el proceso está lejos de cumplir con la defición de estacionariedad que hemos establecido en capítulos previos, pero relajaremos el supuesto y reconoceremos que una serie puede ser estacionaria en varianza bajo una tendencia determinística. Así, diremos que la serie será descrita por una ecuación dada por:
$$
    Y_t = \sum^m_{j = 0} \delta_j t^j + X_t
    \label{Y_Trend}
$$

Donde $X_t$ es un proceso $ARMA(p, q)$ con media cero, que se puede ver como:
$$
    \alpha(L) X_t = \beta(L) U_t
$$

Entonces, los momentos y variaza de la ecuación (\ref{Y_Trend}) estaran dados por:
$$
    \mathbb{E}[Y_t] = \sum^m_{j = 0} \delta_j t^j = \mu_t
    \label{E_Trend}
$$

Dada la ecuación (\ref{E_Trend}) podemos plantear la siguiente ecuación de covarainzas:
\begin{eqnarray}
    \mathbb{E}[(Y_t - \mu_t) \cdot (Y_{t+\tau} - \mu_{t+\tau})] & = & \mathbb{E}[X_t \cdot X_{t+\tau}] \nonumber \\
    & = & \gamma_X(\tau)
    \label{Cov_Trend}
\end{eqnarray}

Utilizando el resultado de la ecuación (\ref{Cov_Trend}) podemos establecer que:
$$
    \mathbb{E}[(Y_t - \mu_t)^2] = \mathbb{E}[X_t^2] = \sigma_X^2
    \label{Var_Trend}
$$

Así, las ecuaciones (\ref{E_Trend}) y (\ref{Var_Trend}) significan que el proceso descrito por la ecuación (\ref{Y_Trend}) es estacionario pero en varianza. De esta forma a partir de este momento diremos que una serie será estacionaria al rededor de una tendencia determinística si cumple con las condiciones establecidas en las ecuaciones (\ref{Y_Trend}), (\ref{E_Trend}) y (\ref{Var_Trend}).

Dicho lo anterior estudiaremos el concepto de raíz unitaria de un proceso estocástico o de una serie de tiempo. Partamos de platear que un proceso AR(1) tiene raíz unitaria cuando el cual el coeficiente $a_1 = 1$, es decir:
$$
    Y_t = Y_{t-1} + U_t
    \label{UR_1}
$$

Donde $U_t$ es un proceso pueramente aleatorio con media cero, varianza constante y autocovarianza cero (0), al cual nos referiremos simplemente como ruido blanco. Supongamos ahora que incluímos un término constante en la ecuación (\ref{UR_1}), de forma que tenemos:
$$
    Y_t = \delta + Y_{t-1} + U_t
    \label{UR_2}
$$

Tomando a la ecuación (\ref{UR_2}) y suponiendo que existe un valor inicial $Y_0$ de la serie podemos plantear la sguiente secuencia de expresiones:
\begin{eqnarray*}
    Y_1 & = & \delta + Y_0 + U_1 \\
    Y_2 & = & \delta + Y_1 + U_2 \\
    & = & \delta + (\delta + Y_0 + U_1) + U_2 \\
    & = & 2 \times \delta + Y_0 + U_1 + U_2
\end{eqnarray*}

Si repitieramos la sustitución sucesiva anterior hasta el momento $t$ encontrariamos que la ecuación de la solución general que describe a un $AR(1)$ con término constante que tiene raíz unitaria es de la forma:
$$
    Y_t = t \delta + Y_0 + \sum_{i=1}^t U_i
    \label{UR_3}
$$

La ecuación (\ref{UR_3}) es equivalente a la ecuación (\ref{Y_Trend}). A la ecuación (\ref{UR_3}) también se le conoce como proceso con Drift o con término constante, indistintamente, ya que el componente de Drift suele asociarse a la posibilidad de incorporar el efecto de los residuales pasados, lo cual es posible simplemente agregando una constante.s

Si revisamos el comportamiento de sus momentos y varianza de la ecuación (\ref{UR_3}) encontramos que:
\begin{eqnarray*}
    \mathbb{E}[Y_t] & = & Y_0 + \delta t = \mu_t \\
    Var[Y_t] & = & t \sigma^2 = \gamma(0, t) \\
    Cov(Y_t, Y_{t+\tau}) & = & (t - \tau) \sigma^2 = \gamma(t, \tau)
\end{eqnarray*}

De esta forma, la ecuación (\ref{UR_3}) no describe un proceso estacionario, sólo podría ser estacionario si $t = 1$, en cualquier otro caso sería no estacionario en varianza. Ahora hagamos un resumen y acordemos notación que se utilizará en esta sección. Supongamos un proceso o serie de tiempo que es decrito por la siguiente ecuación:
$$
    Y_t = \delta + Y_{t-1} + X_t
    \label{UR_4}
$$

Donde $X_t$ es un $ARMA(p, q)$ con media cero. Si definimos a $\Delta Y_t = Y_t - Y_{t-1}$, entonces la ecuación (\ref{UR_4}) la podemos escribir como:
$$
    \Delta Y_t = \delta + X_t
    \label{UR_5}
$$

A la ecuación (\ref{UR_5}) la denominaremos como un proceso estacionario en diferencias o simplemente como un proceso integrado. Así utilizaremos la siguiente definición.

Sea un proceso estocástico $Y$, decimos que este es integrado de orden $d$, $I(d)$, si este puede transformarse a uno estacionacionario, que sea invertible, mediante la diferenciación del mismo $d$-veces, es decir:
$$
    (1 - L)^d Y_t = \delta + X_t
    \label{UR_6}
$$

Donde $X_t$ es un proceso $ARMA(p, q)$. De lo cual se infiere que en la ecuación (\ref{UR_6}) $Y_t$ será una $ARIMA(p, d, q)$, el cual contiene $d$ raíces unitarias. A estos procesos también se les conoce como procesos con tendencia estocástica.

Dada la discusión annterior, a continuación platearemos un resumen de cuales son los dos casos a los cuales nos referiremos como procesos que no son estacionarios en media, pero que si lo son en varianza. Estos casos son:
\begin{eqnarray}
    Y_t & = & Y_0 + \delta t + U_t \\
    Y_t & = & Y_0 + \delta + \sum_{i = 1}^t U_t
\end{eqnarray}

Ambos casos no son estacionarios en media, pero si lo son en varianza. De ambos podemos decir que los choques o innovaciones del término de error tienen un efecto transitorio en el primero, pero permanentes en el segundo.

## Pruebas de Raíces Unitarias

En esta sección plantearemos una serie de pruebas estadísticas para determinar cuando una serie puede ser estacionaria bajo tres posibles casos: (1) estacionariedad al rededor de una tendencia determinística; (2) estacionariedad al rededor de una media, y (3) estacionariedad al rededor del cero.

## Dickey - Fuller (DF)

Partamos de una forma del proceso $Y_t$ dada por:
$$
    Y_t = \sum_{j = 0}^m \delta_j t^j + X_t
    \label{UR_DF_G}
$$

Donde $X_t$ es un $ARMA(p, q)$ con media cero. Esta prueba asume que $m = 1$, por lo que utilizaremos un modelo del tipo:
$$
    Y_t = \alpha + \delta t + \rho Y_{t-1} + U_t
    \label{UR_DF}
$$

Si, el $AR(1)$ planteado tiene raíz unitaria, es decir, $\rho = 1$, entonces tendríamos:
\begin{eqnarray*}
    Y_t & = & \alpha + \delta t + Y_{t-1} + U_t \\
    \Delta Y_t & = & \alpha + \delta t + U_t
\end{eqnarray*}

De esta forma, para determinar si una serie tiene raíz unitaria basta con probar la hipótesis nula de que $H_0 : \rho = 1$, junto con las diferentes combinaciones que impliquen restricciones respecto a $\delta$ y $\alpha$.

En resumen, la prueba DF consiste en asumir un modelo general dado por la ecuación (\ref{UR_DF}) y probar tres especificaciones distintas que serían válidas bajo $H_0 : \rho = 1$:
\begin{enumerate}
    \item Modelo A: con intercepto y tendencia:
    \begin{equation*}
        \Delta Y_t = \alpha + \delta t + \beta Y_{t-1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \beta = \rho - 1 = 0$ contra $H_a : \beta < 0$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario al rededor de una tendencia determinística.
    
    \item Modelo B: con intercepto:
    \begin{equation*}
        \Delta Y_t = \alpha + \beta Y_{t-1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \beta = \rho - 1 = 0$ contra $H_a : \beta < 0$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario al rededor de una constante.
    
    \item Modelo C: sin intercepto y tendencia:
    \begin{equation*}
        \Delta Y_t = \beta Y_{t-1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \beta = \rho - 1 = 0$ contra $H_a : \beta < 0$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario sin considerar una constante o una tendencia determinística, es decir, es un proceso puramente aleatorio.
\end{enumerate}

### Dickey - Fuller Aumentada (ADF)

A diferencia de un modelo AR(1) para el caso de una prueba DF como en la ecuación (\ref{UR_DF}), en una prueba ADF se asume que el proceso es un AR(p) de la forma (por simplicidad hemos omitido el término constante y el término de tendencia determinística):
$$
    Y_t = a_1 Y_{t-1} + a_2 Y_{t-2} + \ldots + a_p Y_{t-p} + U_t
    \label{UR_ADF}
$$

Haciendo una sustitución de términos similar a las que hemos planteado en otras secciones podemos reexpresar la ecuación (\ref{UR_ADF}) en su versión en diferencias siguiendo el proceso:
$$
    Y_t = \rho Y_{t-1} + \theta_1 \Delta Y_{t-1} + \theta_2 \Delta Y_{t-2} + \ldots + + \theta_{p-1} \Delta Y_{t-p+1} + U_t 
$$

Donde $\rho = \theta_0 = \sum_{j = 1}^p a_j$, $\theta_i = - \sum_{j = i + 1}^p a_j$, $i = 1, 2, \ldots, p-1$. Así, si el proceso AR(p) tiene raíz unitaria entonces ceremos que:
\begin{eqnarray*}
    1 - a_1 - a_2 - \ldots - a_p & = & 0 \\
    \rho & = & 1
\end{eqnarray*}

De donde podemos establecer que el modelo general de una prueba ADF será:
$$
    \Delta Y_{t-1} = \alpha + \beta t + (\rho - 1) Y_{t-1} + \theta_1 \Delta Y_{t-1} + \theta_2 \Delta Y_{t-2} + \ldots + \theta_k \Delta Y_{t-k} + U_t
$$

Donde $U_t$ es un proceso puramente aleatorio y $k$ es elegido de tal manera que los residuales sean un proceso puramente aleatorio. En resumen, la prueba DF consiste en asumir un modelo general dado por la ecuación (\ref{UR_ADF}), que incluya constante y tendencia, y probar tres especificaciones distintas que serían válidas bajo $H_0 : \rho = 1$:
\begin{enumerate}
    \item Modelo A: con intercepto y tendencia:
    \begin{equation*}
        \Delta Y_t = \alpha + \delta t + \beta Y_{t-1} + \theta_1 \Delta Y_{t-1} + \theta_2 \Delta Y_{t-2} + \ldots + \theta_{p-1} \Delta Y_{t-p+1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \beta = \rho - 1 = 0$ contra $H_a : \beta < 0$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario al rededor de una tendencia determinística.
    
    \item Modelo B: con intercepto:
    \begin{equation*}
        \Delta Y_t = \alpha + \beta Y_{t-1} + \theta_1 \Delta Y_{t-1} + \theta_2 \Delta Y_{t-2} + \ldots + \theta_{p-1} \Delta Y_{t-p+1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \beta = \rho - 1 = 0$ contra $H_a : \beta < 0$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario al rededor de una constante.
    
    \item Modelo C: sin intercepto y tendencia:
    \begin{equation*}
        \Delta Y_t = \beta Y_{t-1} + \theta_1 \Delta Y_{t-1} + \theta_2 \Delta Y_{t-2} + \ldots + \theta_{p-1} \Delta Y_{t-p+1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \beta = \rho - 1 = 0$ contra $H_a : \beta < 0$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario sin considerar una constante o una tendencia determinística, es decir, es un proceso puramente aleatorio.
\end{enumerate}

### Phillips - Perron (PP)

Una tercera prueba es la de PP, la cual también está basada en una AR(1) dado por la ecuación:
$$
    Y_t = d \eta + \rho Y_{t-1} + U_t
    \label{UR_PP}
$$

Donde $d$ incluye a cualquiera de los componentes determinísticos como constante y tendencia. Al igual que los casos pasados, la hipótesis a probar era $H_0 : \rho = 1$ contra la alternativa $H_a : \abs{\rho} < 1$, y asumimos una estructura MA(q) es el término de error de la forma $U_t = \psi(L) \varepsilon_t = \psi_0 \varepsilon_t + \psi_1 \varepsilon_{t-1} + \ldots + \psi_p \varepsilon_{t-p}$, con $\varepsilon_t$ es un ruido blanco con media cero y varianza $\sigma^2$. En este modelo se elige el valor $p$ que hace que el componente sea un MA(p). Las tablas estadísticas de PP para esta prueba pueden utilizar una estadística $Z_\tau$ o $Z_\rho$, las cuales se pueden emplear indistintamente.

En resumen, la prueba PP consiste en asumir un modelo general dado por la ecuación (\ref{UR_PP}) y probar dos especificaciones distintas que serían válidas bajo $H_0 : \rho = 1$, ambas considerando un compenente Drift:
\begin{enumerate}
    \item Modelo A: con intercepto y tendencia:
    \begin{equation*}
        Y_t = \alpha + \delta t + \rho Y_{t-1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \rho = 1$ contra $H_a : \abs{\rho} < 1$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario al rededor de una tendencia determinística.
    
    \item Modelo B: con intercepto:
    \begin{equation*}
        Y_t = \alpha + \rho Y_{t-1} + U_t
    \end{equation*}
    Buscamos probar si $H_0 : \rho = 1$ contra $H_a : \abs{\rho} < 1$, por lo que es una prueba de una cola. Otra forma de decirlo, es probamos si el proceso tiene raíz unitaria contra si el proceso es estacionario al rededor de una constante.
\end{enumerate}

### Kwiatkowsky - Phillips - Schmidt - Shin (KPSS)

La prueba KPSS considera que el proceso es estacionario bajo la hipótesis nula, lo cual hace una diferencia respecto de las anteriores pruebas. El modelo considerado es:
$$
    Y_t = \delta t + \xi_t + U_t
$$

Donde $U_t$ es un proceso estacionario y $\xi_t$ es un ruido blanco descrito por la forma: $\xi_t = \xi_{t-1} + \varepsilon_t$, donde $\varepsilon_t$ es un proceso normalmente distribuido con media cero y varianza $\sigma^2_\varepsilon$.

Así, bajo la hipótesis nula $H_0 : \sigma^2_\varepsilon = 0$, $\xi$ se vuelve una constante y el proceso puede tener una tendencia estacionaria. Dado el planteamiento de la prueba, los valores críticos al 95\% son: 
\begin{enumerate}
    \item 0.146, para un modelo con tendencia
    \item 0.463, para un modelo con constante
\end{enumerate}

### Ejemplo con aplicación de todas las pruebas de raíces unitarias

A continuación, mostraremos como ejemplo la aplicación de las pruebas de raíces unitarias a la serie de Tipo de Cambio en forma logaritmica y de diferencias logaritmicas. Asumamos que determinamos el valor de los rezagos de la prueba con el criterio de $p = int\{ 4 (T/100)^{1/4} \}$. En la práctica, existen otras formas de determinar el valor de $p$, como el criterio de AIC, pero es decisión del investigador cual usar.

En el Cuadro (\ref{Result_UR}) mostramos los resultados de aplicar las pruebas de raíces unitarias a la serie $LTC_t$, considerando $p = int \{ 4 (234/100)^{(1/4)} \} = 4$ para aquellas pruebas que requieren de rezagos: ADF, PP y KPSS. Los raultados para todos los modelos se ubican en el Scrip Clase 16 en el GitHub.
\begin{table}
\centering
\begin{tabular}{|c | c | c | c | c |}
\hline
    Variable & Dickey-Fuller & DF Aumentada & Phillips-Perron & KPSS \\
\hline
    $LTC_t$ & -2.534(A)* & -2.534(A)* & -2.4971(A)* & 0.5095(A) \\
    $\Delta LTC_t$ & -11.6643(C) & -6.5746(C) & -11.6183(C) & 0.0611(B)* \\
\hline
    \multicolumn{5}{ l }{Nota: (1) Entre parentésis se indica el modelo utilizado que es aquel más} \\
    \multicolumn{5}{ l }{probable de ser aceptado. (2) * Indica el rechazo de $H_0$ al 5\%. Los valo-} \\
    \multicolumn{5}{ l }{res criticos para los modelos A, B y C para las pruebas DF y ADF son:} \\
    \multicolumn{5}{ l }{-3.43, -2.88 y -1.95, respectivamente. Los valores criticos para prueba PP} \\
    \multicolumn{5}{ l }{son: -3.430186 y -2.873954, y los valores criticos para prueba KPSS son:} \\
    \multicolumn{5}{ l }{0.146 y 0.463, para los modelos A y B, respectivamente.}
\end{tabular}
\caption{Pruebas de Raíces Unitarias para la serie $LTC_t$ utilizando 4 rezagos.}
\label{Result_UR}
\end{table}

