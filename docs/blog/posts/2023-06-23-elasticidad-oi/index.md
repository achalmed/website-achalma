---
title: Elasticidad
subtitle: Expl
description: |
  Descub
categories:
  - Organización industrial
  - Economía y Negocios
tags:
  - OrganizaciónIndustrial
date: "06/23/2023"
draft: true
---


Elasticidad precio de la demanda

::: {.cell}
``` {.python .cell-code}
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

# Fijar el estado aleatorio para reproducibilidad
np.random.seed(19680801)

# Crear datos aleatorios
xdata = np.random.random([2, 10])

# Dividir los datos en dos partes
xdata1 = xdata[0, :]
xdata2 = xdata[1, :]

# Ordenar los datos para obtener curvas limpias
xdata1.sort()
xdata2.sort()

# Crear algunos puntos de datos y
ydata1 = xdata1 ** 2
ydata2 = 1 - xdata2 ** 3

# Graficar los datos
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(xdata1, ydata1, color='tab:blue')
ax.plot(xdata2, ydata2, color='tab:orange')

# Crear los eventos que marcan los puntos de datos en el eje x
xevents1 = EventCollection(xdata1, color='tab:blue', linelength=0.05)
xevents2 = EventCollection(xdata2, color='tab:orange', linelength=0.05)

# Crear los eventos que marcan los puntos de datos en el eje y
yevents1 = EventCollection(ydata1, color='tab:blue', linelength=0.05, orientation='vertical')
yevents2 = EventCollection(ydata2, color='tab:orange', linelength=0.05, orientation='vertical')

# Agregar los eventos al eje
ax.add_collection(xevents1)
ax.add_collection(xevents2)
ax.add_collection(yevents1)
ax.add_collection(yevents2)

# Establecer los límites
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

ax.set_title('Gráfico de línea con puntos de datos')

# Mostrar la gráfica
plt.show()
```
:::


1.  
$$
\eta _{XP_y} = \frac{\frac {X_f^d - X_i^d}{X_i}}{\frac {P_f^d - P_i^d}{P_i^d}}
$$

$$
= \frac{\frac{\Delta X^d}{X_i^d}}{\frac{\Delta P_x^d}{P_i^d}}
$$

$$
\frac{\Delta X^d P_i^d}{\Delta P_x^d X_i^d}
$$ {#eq-1}

2.  

$$
\eta _{PX^d} = \frac{\partial X^d P_x}{\partial P_x X^d}
$$ {#eq-2}

3.  

$$
\eta _{PX^d} = \frac{\partial \ln(\mathrm X)}{\partial  \ln(\mathrm P_x)}
$$ {#eq-3}

4.   
$$
\eta _{PX^d} = \frac{\Delta \% X^d}{\Delta \% P_x}
$$ {#eq-4}

1.  

$$
\eta_{PX^d} = m_{ip} \frac{P_i^d}{X^d}
$$ {#eq-5}

Ejemplo

$$
X^d = \frac{P_y P_z I^{0.2} N}{2 P_x}
$$

Aplicando la fórmula @eq-2

$$ 
\eta _{PX^d} = \frac{\partial \mathrm{X}}{\partial \mathrm{P_x}} \frac{\mathrm{P_x}}{\mathrm{X^d}} 
$$

$$
= - \frac{P_y P_z I^{0.2} N}{2 (P_x)^2} \frac{\mathrm{P_x}}{\mathrm{X^d} }
$$

reemplazamos $x^d$ con su valor 
$$
= - \frac{P_y P_z I^{0.2} N}{2 (P_x)^2} \frac{\mathrm{P_x}}{\frac{P_y P_z I^{0.2} N}{2 P_x} }
$$

ordenando y resolviendo

$$
= - \frac{2 P_y P_z (P_x)^2 I^{0.2} N}{2 P_y P_z (P_x)^2 I^{0.2} N} = -1
$$

interpretación

Si el $P_x$ aumenta en 1% entonces $X^d$ disminuye en 1%.

