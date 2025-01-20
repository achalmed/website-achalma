---
title: Linux Primeros Pasos
subtitle: Una guía para principiantes en Linux
shorttitle: "Editar"
description: |
  Accede al [PDF](https://achalmaedison.netlify.app/blog/posts/2021-07-14-comandos-blogdown/index.pdf) completo aquí. Actualizar enlace
abstract: |
  | Primer parrafo de abstrac
keywords: [keyword1, keyword2]
categories:
  - Informática
  - Sistemas Operativos
tags:
  - Linux
  - Principiantes
  - OpenSource
  - Comandos
citation:
  pdf-url: https://achalmaedison.netlify.app/docs/blog/posts/2023-05-02-linux-primeros-pasos/index.pdf
date: "05/02/2023"
draft: false  # Modo de borrador (false = final, true = borrador)
---





# LINUX primeros pasos como usuario

SISTEMAS OPERATIVOS

SISTEMA OPERATIVO es el conjunto de programas que proporciona los mecanismos y reglas básicas de funcionamiento para acceder a los recursos del ordenador de forma adecuada, especialmente a todos los dispositivos periféricos.

- **MS-DOS**
- **WINDOWS**
- **Mac-OS**
- **UNIX** (Grandes máquinas) ------  **LINUX** (PCs)

Tipos de programas:

- **Programas de Control**: Gestión de software y hardware, p.e. colas de impresión, etc.
- **Utilidades del sistema**: editores de texto, compiladores, gestión de correo, etc.

ORIGEN Y DESARROLLO DE LINUX

- Creado por **Linus Torvalds** en 1991. Inspirado en **UNIX**.
- Sistema **multiusuario** y **multitarea**.
- Desarrollado por miles de programadores en la red.
- Filosofía **GNU**. Libre distribución bajo **GPL** (General Public License).
- No garantizado. Flexible, estable y barato.
- Al principio no era fácil de usar, porque estaba pensado para programadores.
- Cada vez se desarrollan más aplicaciones y utilidades pensando en usuarios no programadores, para facilitar el uso de INTERNET y competir con WINDOWS.

**Distribuciones**: Núcleo (**Kernel**) de Linux +  Aplicaciones y Utilidades para un grupo específico de usuarios

- Algunas distribuciones son gratuitas y otras no.
- Algunas de las distribuciones están mantenidas por empresas comerciales (ej. RedHat, Fedora, openSUSE, Ubuntu), y otras son mantenidas por una comunidad de programadores (ej. Debian).
- Normalmente se obtiene una distribución descargándola de Internet.
- Distribuciones mas usadas:
  - **Debian**
  - **Slackware**
  - **SUSE**
  - **Caldera**
  - **Red Hat Enterprise Linux**(comercial)
  - **Fedora Project** (basada en RedHat)
  - **Mandriva** (basada en RedHat)
  - **Ubuntu** (basada en Debian)
  - **Guadalinex** (basado en Debian, promovido por la Junta de Andalucía)

PRIMEROS PASOS

**ARRANQUE DEL SISTEMA**

- **LILO o GRUB:** programa que se encarga de arrancar el S.O. deseado por el usuario cuando coexisten Windows y Linux

**INICIO DE UNA SESIÓN DE USUARIO**

- **Login**:Nombre del usuario.
- **Password**: Contraseña secreta de acceso privado de cada usuario. (Sólo aparecen asteriscos cuando se teclea)

**ELECCIÓN DE PASSWORDS**

La utilización de passwords está hoy en día extendida a muchos aspectos de la vida cotidiana, no sólo a la utilización de máquinas compartidas.

La elección de un **password seguro** es tanto más crucial cuanto mayor sea la importancia de lo que "protege": cuentas bancarias, messenger, cuenta de e-mail, reserva de biletes de tren, etc.

Passwords no seguros pueden ser averiguados por programas especializados en un tiempo inferior a 1 segundo (por ejemplo para una palabra de diccionario) o en pocas horas (passwords de hasta 6 caracteres formados por letras mayúsculas, minúsculas y números).

Variantes del tipo sustituir A por 4 , la E por un 3, o la I por un 1 están ya incorporadas en los crackers.

Recomendación para passwords importantes:

- Utilizar passwords cuanto más largos mejor, al menos de 6 caracteres (mejor 8)
- Utilizar letras mayúsculas, minúsculas, números y caracteres especiales  como **! " $ % & / ( ) = ? ¿**
- El tiempo para crackear un password así con 8 caracteres es de 39 años !!!

Lo que NO debes hacer con un password:

- Apuntarlo en un post-it y pegarlo en la pantalla
- Decírselo a cualquiera
- Usar palabras de un diccionario, ni siquiera concatenadas (megustaminovio)
- Usar passwords de menos de 6 caracteres
- Llevar las claves de tarjetas y los passwords de las cuentas bancarias por internet en la cartera, o en una agenda en el bolso.

**EL PROBLEMA DE LOS BUENOS PASSWORDS ES ACORDARSE DE ELLOS: aqui tienes un truco**

Piensa en una frase y utiliza las iniciales de las palabras, mezcladas con números y algún signo, de forma que  puedas recordarla.

Ejemplos:

**E95faP+L**

(El 95 fui a Paris y Londres)

**Uiv+q%p**

(Una imagen vale más que 100 palabras)

**2+2s4!**

(dos más dos son cuatro!)

**$90%pa**

(somos 90 por ciento pura agua)

**VaLy$l**

(Vente conmigo a Lepe y serás lepera)

Puedes crear tus propias reglas personales: elegir las segundas letras, tomar las dos primeras ...

**CAMBIO DEL PASSWORD DE USUARIO**

1. Elegir una contraseña nueva atendiendo a las recomendaciones anteriores.
2. Abrir un Emulador de Terminal desde el panel.
3. Teclear en la Linea de Comandos del terminal una de los siguientes instrucciones:

- **passwd** (para instalaciones locales de Linux)
- **yppasswd** (para instalaciones de Linux con sistema de archivos compartidos)

5. Teclear la contraseña actual.  (No se visualiza)
6. Teclear la nueva contraseña.  (No se visualiza)
7. Confirmar la nueva contraseña. (No se visualiza)
8. Salir del terminal con la instrucción **exit**

**SALIDA DE LA SESIÓN**

- Sesión Failsafe:  tecleando  **exit**
- Sesiones en entorno de ventanas:  eligiendo **Terminar** en el **Menú de Inicio**.

**CIERRE DEL SISTEMA**

- Eligiendo **Apagar** o **Reiniciar** en el **Menú Sistema**

SISTEMA MULTIUSUARIO

- LINUX  puede tener habilitados muchos usuarios.
- Pueden trabajar simultáneamente a través de la red.
- Cada usuario tiene una **cuota de disco** duro, una cantidad máxima de disco que puede usar.
- Hay un superusuario llamado  **root**  que actua como administrador del sistema y que dispone de permisos PARA TODO. Son funciones exclusivas del  **root**:

- Habilitar y deshabilitar usuarios.
- Cambiar contraseñas de otros usuarios.
- Asignar o modificar las cuotas de disco.
- Decidir qué aplicaciones y utilidades puede usar cada usuario.
- Organizar a los usuarios por grupos.
- Instalar o desinstalar programas.

**Nota:** Es muy importante reservar el usuario **root** exclusivamente para labores de administración del sistema, incluso cuando se instale un sistema LINUX particular, es decir, que vaya a ser utilizado por un único usuario. Debe tenerse en cuenta que, debido a que el **root** dispone de TODOS LOS PERMISOS, un error puede resultar catastrófico. Por ello se debe dar de alta, al menos, un usuario "corriente" y trabajar habitualmente con esa cuenta. Utilizar la cuenta del **root** sólo para administración, instalación de nuevo software, etc.

**NUNCA** utilices la cuenta del **root** para acceder a Internet. Y esmérate con su password.

MODOS DE TRABAJO

- **Modo de comandos**: El usuario se comunica con el ordenador mediante la **Linea de Comandos** de un terminal o de un emulador de terminal. Estos comandos o instrucciones pueden ser interpretados por el sistema usando diferentes programas denominados **Shell**. (Lo usaremos sólo esporádicamente).

- **Modo gráfico**: El usuario se comunica con el ordenador  mediante un **Interfaz Gráfico de Usuario** (**GUI**) que se encarga de interpretar las diferentes acciones realizadas con el teclado o con el ratón sobre diferentes objetos gráficos como **iconos**, **botones**, **ventanas**,  **menús**, **barras de desplazamiento** (**scroll**), **lineas separadoras**, etc.
- En UNIX, el GUI habitual es el sistema **X Window** que está formado fundamentalmente por dos programas:
- **Servidor X** (**X Server**): programa que dibuja en la pantalla los objetos gráficos
- **Gestor de Ventanas** (**Window Manager**): los más usados son  **GNOME** y  **KDE**.

SISTEMA DE ARCHIVOS Y CARPETAS

**NOMBRES DE FICHEROS Y DIRECTORIOS**

**Archivos o Ficheros** (**Files**) : Reglas para los nombres

- De 1 a  255 caracteres. Se pueden usar todos menos el     \***\*/\*\***      aunque ...
- No es recomendable usar caracteres como       **=   ^   ~   '   "   `   \*   ;   -   ?   [ ] ( ) ! & > <**
- Pueden aparecer sólo números
- Se distinguen mayúsculas y minúsculas: README no es lo mismo que ReaDme
- IMPORTANTE: Si se van a compartir archivos con WINDOWS no se debe usar esa distinción
- Los nombres de archivos pueden, aunque no es necesario, llevar una extensión o sufijo (lo que aparece al final del nombre, después de un punto) :    **Nombre.extension**
- Las extensiones sirven principalmente a título orientativo. Algunos programas reconocen determinadas extensiones y las aceptan "por defecto":

- **txt** para archivos de texto
- **htm**  y **html** para archivos de hipertexto (formato usual de las páginas de Internet)
- **png**,  **tif**,  **jpg** y **gif** para archivos de imagenes en distintos formatos
- **f**  y  **f90** para archivos fuente en lenguaje Fortran
- **m**  archivos conteniendo programas MATLAB
- etc.

**Carpetas o Directorios** (**Folder** o **Directory**)

- Tipo especial de fichero que contiene a su vez otros ficheros y/o subcarpetas.
- Mismas reglas para los nombres que los ficheros.
- Las carpetas no suelen tener extensiones.

**ESTRUCTURA DEL SISTEMA DE FICHEROS**

El sistema de archivos es, más o menos, "la forma de organizar la información almacenada en el disco duro". La mayoría de los sistemas operativos posee su propio sistema de archivos. El sistema de archivos nativo de Linux es el **EXT2**. Normalmente, los sistemas operativos proveen los mecanismos para crear, mover, renombrar y eliminar tanto archivos como directorios.

La estructura de directorios suele ser jerárquica, ramificada o "en árbol":

La estructura de directorios que sigue Linux es similar a la de cualquier sistema UNIX. La estructura del sistema de archivos NO está ligada de forma directa a la estructura de hardware. A diferencia de Windows, es independiente del número de discos duros, disqueteras o CDROMs. No hay una "unidad" para cada unidad física de disco o partición como en Windows (**A:\*\*, **C:\*\*, etc.), sino que todos los discos duros o de red se montan bajo un sistema de directorios en árbol, y algunos de esos directorios enlazan con estas unidades físicas de disco. IMPORTANTE: Las barras en Linux al igual que en cualquier UNIX son inclinadas hacia la derecha, como se puede ver más abajo (ese es el motivo de que en internet sean inclinadas hacia la derecha, ya que nació bajo UNIX).

- Estructura jerárquica de árbol invertido:

- Desde una **carpeta raiz**, denotada por  / , "cuelgan" otros archivos y/o carpetas.
- De cada subcarpeta pueden "colgar" a su vez otros archivos y/o carpetas.
- etc

- "Colgar" significa  "estar contenido en"
- Todos los archivos y/o carpetas están  finalmente colgados de la carpeta raíz  /
- Carpeta "**padre**" de una carpeta es aquella que la contiene y está en el nivel inmediatamente superior de la estructura de árbol.

La ubicación de un fichero en la estructura de archivos se denota mediante su **path** ó **ruta**: se trata de una cadena de caracteres que incluye todo el "camino" de directorios que llevan desde el directorio raiz (  /  ) hasta el fichero considerado. Se separa un directorio del siguiente de nuevo mediante el caracter especial   /   .

Ejemplo: el path  **/usr/local/bin/readme.txt**  indica la ubicación del fichero de nombre  **readme.txt**  que cuelga de la carpeta  **bin**  que a su vez cuelga de la carpeta  **local**  que a su vez cuelga de la carpeta  **usr**  que cuelga de la raiz del sistema de archivos   /  .

**ALGUNOS DIRECTORIOS IMPORTANTES**

Los directorios principales que podemos encontrar en cualquier sistema Linux son:

Directorio

Descripción

**/**

Es la raíz del sistema de directorios. Aquí se monta la partición principal Linux EXT.

**/etc**

Contiene los archivos de configuración de la mayoría de los programas.

**/home**

Contiene los archivos personales de los usuarios.

**/bin**

Contiene comandos básicos y muchos programas.

**/dev**

Contiene archivos simbólicos que representan partes del hardware, tales como discos duros, memoria...

**/mnt**

Contiene subdirectorios donde se montan (se enlaza con) otras particiones de disco duro, CDROMs, etc.

**/tmp**

Ficheros temporales o de recursos de programas.

**/usr**

Programas y librerías instalados con la distribución

**/usr/local**

Programas y librerías instalados por el administrador

**/sbin**

Comandosadministrativos

**/lib**

Librerías varias y módulos ("trozos") del kernel

**/var**

Datos varios como archivos de log (registro de actividad) de programas, bases de datos, contenidos del servidor web, copias de seguridad...

**/proc**

Información temporal sobre los procesos del sistema (explicaremos esto más en profundidad posteriormente).

**OTROS CONCEPTOS RELACIONADOS CON DIRECTORIOS:**

- **Directorio** o **Carpeta de trabajo (Working Directory)**: es, en cada momento, el directorio en que se está trabajando. Cualquier fichero que el S.O. tenga que buscar, lo hará en primer lugar en dicho directorio.
- **Ruta** **(Path) de un fichero**: secuencia de directorios, separados por el símbolo **/**,  que se ha de recorrer en la estructura de árbol para llegar a un fichero determinado.

- **Path absoluto**: muestra toda la ruta desde la raiz del sistema de ficheros **/**
- **Path relativo**: muestra la ruta desde el directorio de trabajo.  Puede empezar en:

- una subdirectorio del directorio de trabajo,  si el camino es descendente
- **. .**  si el camino comienza de forma ascendente

- **.**   denota el directorio de trabajo
- **. .**  denota el directorio padre del directorio de trabajo

- **Directorio o carpeta personal** de un usuario (**home directory**): es el que contiene los ficheros de un usuario del sistema. Cada usuario tiene su propio directorio personal. Frecuentemente, los directorios personales cuelgan del directorio **/home**, es decir, son de la forma **/home/usuario**. Cuando se empieza una sesión en un sistema Linux, de forma automática se elige el **home directory** como **working directory**.

**PUNTOS DE MONTAJE DE DISPOSITIVOS:**

En Linux, los distintos dispositivos conectados al ordenador forman parte del sistema de archivos, de manera que, una vez montados, para el usuario son como una carpeta más del sistema de ficheros. Habitualmente se montan en **/mnt**  
Por ejemplo, la **disquetera** suele ser  **/mnt/floppy**    y el  **CDROM**   suele ser   **/mnt/cdrom**

**SISTEMAS DE ARCHIVOS COMPARTIDOS Yellow Pages**

Este sistema permite que un conjunto de máquinas con sistemas Linux  conectadas en red compartan un sistema de archivos común. Esto permite que todos los usuarios de esas máquinas dispongan de todos sus archivos en todas las máquinas. En este caso, el sistema de archivos suele estar físicamente en una de las máquinas. Un usuario puede, así, acceder a cualquiera de las máquinas con el mismo login y el mismo password.

Cuando se usa el servicio yellow pages (páginas amarillas), para cambiar el password de un usuario es necesario utilizar el comando **yppasswd**  en lugar de passwd.

PROPIEDAD, PERMISOS Y DERECHOS DE ACCESO A CARPETAS Y FICHEROS

Al ser Linux un sistema multiusuario, es preciso que esté definido de quién es cada cosa (carpetas y ficheros) y qué derechos de acceso tiene cada usuario.

Cada usuario es propietario, en general, de todos los ficheros y subdirectorios que cuelgan de su directorio personal: puede crear, modificar y borrar en él todo lo que quiera. Ningún otro usuario (excepto el root) puede acceder a los ficheros de otro, ni siquiera verlos.

En Linux, cada fichero y carpeta tiene un **propietario** (**owner**). El propietario es el que define los permisos de acceso de otros usuarios a sus ficheros. Para ello, el conjunto de usuarios de una máquina se entiende dividido en tres grupos:

- el mismo propietario (**owner**)
- el grupo de usuarios al que pertenece el propietario (**group**)
- el resto del mundo (**world**)

Dichos permisos, a su vez, son de tres tipos:

- de lectura (**read**)
- de escritura (**write**)
- de ejecución (**execute**)

Los permisos de acceso a un fichero sólo los puede cambiar el propietario y el (todopoderoso) **root**. En general, cada usuario puede leer en el resto de directorios del sistema de ficheros, excepto en la del root y en las de los otros usuarios.

- Los ficheros y carpetas del sistema son propiedad del root
- Los ficheros y carpetas de programas instalados son propiedad del  root
- El  root tiene todos los permisos sobre todos los ficheros de todos los usuarios.

EL GESTOR DE VENTANAS KDE

**PANTALLA KDE:**

**Panel de KDE:**

- Menú de inicio de aplicaciones
- Escritorios virtuales
- Directorio Personal
- Lista de ventanas abiertas
- Emulador de Terminal
- Editores sencillos: Kedit, Kwrite

**Ventanas:**

- Barra de títulos:

- Icono de aplicación (Manipulación de ventanas)
- Fijación de ventana
- Minimizar, maximizar y cerrar
- Barra de menús
- Barra de herramientas

**Konqueror: Gestor gráfico de archivos (File Manager):**

- Navegar por la estructura de directorios
- Crear y borrar carpetas
- Copiar y mover carpetas
- Cambiar nombre a ficheros y carpetas
- Abrir y borrar ficheros
- Ver y modificar las propiedades de ficheros y carpetas

**Konsole: Emulador de terminal**

Se usa para trabajar con el Sistema Operativo en modo de comandos, es decir para introducir directamente instrucciones UNIX al sistema. Las instrucciones se escriben en la Línea de Comandos, después del **prompt** del usuario.

**ALGUNOS COMANDOS:**

**clear**

limpia la pantalla

**date**

devuelve la fecha y hora actuales

**cal**

muestra el calendario

**history**

muestra la historia de los últimos comandos usados

**man comando**

Muestra la página del manual correspondiente al comando

**more file**

Si **file** es un fichero de texto, lo muestra de página en página. Se pasa página con la barra espaciadora. Se termina con **q**

**ls**

muestra el contenido del directorio de trabajo

**ls -l**

muestra el contenido del directorio de trabajo en forma de lista, incluyendo información extra

**ls -a**

muestra el contenido del directorio de trabajo incluídos los ficheros ocultos

**ls dir**

ejecuta **ls** sobre el directorio **dir** - se pueden usar opciones: **ls -la dir**

**pwd**

muestra el nombre del directorio de trabajo (print working directory)

**df**

muestra el espacio libre y usado en los discos

**du -sk dir**

muestra la cantidad de espacio de disco usada por el directorio **dir** (y todo lo que hay dentro)

**du -Sk dir**

lo mismo, pero especificando por subdirectorios

**mkdir name**

crea un directorio de nombre **name** (make directory) - si **name** no incluye un **path**, el directorio se crea en el directorio de trabajo

**rm fich**

borra el fichero **fich** (remove)

**rmdir direc**

borra el directorio  **dir** (tiene que estar vacío)

**rm -i fich**

antes de borrar el fichero **fich**, pide confirmación (modo interactivo)

**cp fich dir**

crea una copia del fichero **fich** en el directorio **dir**

**cp fich1 fich2**

crea una copia del fichero **fich1** y le pone el nombre **fich2**

**mv fich dir**

"mueve" el fichero **fich**  al directorio **dir**

**mv fich1 fich2**

"mueve" el fichero **fich1**  al fichero **fich2** (es decir, lo cambia de nombre) (**fich2** puede también incluir un **path**; en ese caso también lo cambia de sitio)

**cd**

cambia el directorio de trabajo al directorio personal (home)

**cd dir**

cambia el directorio de trabajo al directorio **dir**

**cd ..**

cambia el directorio de trabajo al "padre" del actual

**ps**

proporciona información sobre los procesos activos del usuario

**ps aux**

proporciona información sobre todos los procesos activos en el sistema

**kill -9 PID**

elimina el proceso con número de identificación PID

**gzip fich**

crea un fichero de nombre **fich.gz**, comprimido de **fich**

**gunzip fich.gz**

descomprime el fichero **fich.gz**

**tar**

condensa directorios en un sólo fichero y viceversa

**tar -cf file.tar direc**

crea el fichero **file.tar** con el contenido del directorio **direc**

**tar -cvf file.tar direc**

lo mismo, pero con explicaciones (v==verbose)

**tar -xf file.tar**

extrae los ficheros de **file.tar**

**tar -xvf file.tar**

los mismo, pero con explicaciones

**exit**

finaliza la sesión de trabajo; en un terminal, cierra el terminal.

**PERSONALIZACIÓN DE LAS CUENTAS:**

- el fichero de configuración **.bashrc**
- definición o modificación de comandos: **alias**
- variable de entorno **PATH**: definición de los caminos de búsqueda
- ejecución de un fichero de configuración: **source**

**MODIFICACIÓN DEL FICHERO DE CONFIGURACIÓN .bahsrc PARA EL ACENTO ^ EN MATLAB:**

- En el directorio personal, editar el fichero oculto **.bashrc**
- Añadir, al final, la orden: **setxkbmap -variant nodeadkeys**



# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [Usando Apk En Windown 11](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11/index.pdf)
2. [Comandos Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim/index.pdf)
3. [Guia Git](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-git) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-git/index.pdf)
4. [00 Primeros Pasos En Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux/index.pdf)
5. [01 Introduccion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux/index.pdf)
6. [02 Distribuciones Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux/index.pdf)
7. [03 Instalacion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux/index.pdf)
8. [04 Administracion Particiones Volumenes](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes/index.pdf)
9. [Atajos De Teclado Y Comandos Para Usar Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim) Lee sin conexión 📚 [PDF](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

