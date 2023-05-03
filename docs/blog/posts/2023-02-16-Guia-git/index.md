---
title: Guía de Git Cómo trabajar en equipo en proyectos de desarrollo de software
subtitle: Aprende a usar Git para controlar versiones, colaborar con otros desarrolladores y mantener tu código organizado.guia completa
description: |
  Esta guía detallada de Git te enseñará todo lo que necesitas saber para empezar a trabajar en equipo en proyectos de desarrollo de software. Desde la instalación hasta la colaboración con otros desarrolladores, esta guía te proporcionará las herramientas necesarias para mantener tu código organizado y siempre actualizado.
categories:
  - Desarrollo de software
  - Control de versiones
  - Trabajo en equipo
tags:
  - Git
  - GitHub
  - colaboración
  - desarrollo de software
author: Edison Achalma Mendoza
date: "02/16/2023"
date-modified: "today"
draft: false
---



Achalma Edison.
¿Necesitas aprender algunos comandos de [GIT](https://git-scm.com/) básicos? Has venido al lugar correcto. Sigue leyendo para descubrir nuestra práctica hoja de trucos que puedes utilizar como referencia diaria.

¡Empecemos!

# Introducción

Los sistemas de control de versiones como Git son imprescindibles para las prácticas recomendadas del desarrollo de software moderno. El control de versiones le permite realizar un seguimiento de su software a nivel de fuente. Puede rastrear cambios, volver a etapas anteriores y producir ramificaciones para crear versiones alternativas de archivos y directorios.

Los archivos de muchos proyectos de software se mantienen en repositorios de Git y las plataformas como GitHub, GitLab y Bitbucket facilitan el intercambio y la colaboración en proyectos de desarrollo de software.

En esta guía, mostraremos cómo instalar y configurar Git en un servidor de Ubuntu 20.04. Abordaremos la instalación del software de dos formas diferentes: a través del [administrador de paquetes integrado](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-18-04#installing-git-with-default-packages) y a través de la [fuente](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-20-04#installing-git-from-source). Cada uno de estos enfoques ofrece sus propios beneficios, dependiendo de sus necesidades específicas.

# Entendiendo cómo funciona GIT

GIT es el SCV (sistema de control de versiones) de código abierto [más utilizado](https://www.g2.com/categories/version-control-systems?utf8=%E2%9C%93&order=g2_score) que te permite rastrear los cambios realizados en los archivos. Las empresas y los programadores suelen utilizar el GIT para colaborar en el desarrollo de software y aplicaciones.

Un proyecto GIT consta de tres secciones principales: **el directorio de trabajo, el área de preparación y el directorio git.**

El directorio de trabajo es donde se agregan, borran y editan los archivos. Luego, los cambios son preparados (indexados) en el área de preparación. Después de que confirmes tus cambios, la instantánea de los cambios se guardará en el directorio git.

Todo el mundo puede usar GIT ya que está disponible para [Linux](https://git-scm.com/book/es/v2), [Windows](https://gitforwindows.org/), [Mac](https://git-scm.com/download/mac) y [Solaris](https://www.opencsw.org/packages/git/). El software puede tener una fuerte curva de aprendizaje, pero hay muchos [tutoriales](https://www.hostinger.es/tutoriales/instalar-git-en-distintos-sistemas-operativos) disponibles para ayudarte.

# Comandos de GIT básicos

Aquí hay algunos comandos básicos de GIT que debes conocer:

1. `git init`: Inicializa un nuevo repositorio de Git en la carpeta actual.
2. `git clone [url]`: Clona un repositorio existente a la carpeta actual.
3. `git add [file]`: Agrega un archivo al área de stage (preparación) para ser incluido en el próximo commit.
4. `git commit -m "[message]"`: Realiza un commit (guarda un punto de referencia) con un mensaje describiendo los cambios realizados.
5. `git status`: Muestra el estado actual del repositorio, incluyendo los archivos modificados y los que están pendientes de commit.
6. `git log`: Muestra un historial de todos los commits realizados en el repositorio.
7. `git diff`: Muestra las diferencias entre los cambios realizados y el último commit.
8. `git branch`: Muestra una lista de todas las ramas existentes en el repositorio.
9. `git checkout [branch]`: Cambia a una rama específica.
10. `git merge [branch]`: Combina los cambios de una rama específica con la rama actual.
11. `git config --global user.email "achalmaedison@outlook.com"`
12. `git config --global user.name "achalmed"`

Estos son solo algunos de los comandos básicos de Git, hay muchos otros comandos avanzados disponibles para realizar tareas más complejas como trabajar con ramas remotas y manejar conflictos.

# Instalar y Configurar Git en Ubuntu 20.04

- [Git](https://www.digitalocean.com/community/tags/git)
- [Open Source](https://www.digitalocean.com/community/tags/open-source)
- [Ubuntu](https://www.digitalocean.com/community/tags/ubuntu)

By [Lisa Tagliaferri](https://www.digitalocean.com/community/users/ltagliaferri)

## Instalación de Git con paquetes predeterminados

La opción de instalar con paquetes predeterminados es recomendable si quiere activar y ejecutar con Git rápidamente, si prefiere una versión estable ampliamente utilizada o si no busca las funciones más recientes disponibles. Si busca la versión más reciente, debería ir directamente a la sección sobre la [instalación desde la fuente](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-20-04#installing-git-from-source).

Es probable que Git ya esté instalado en el servidor Ubuntu 20.04. Puede confirmar que ese es el caso de su servidor con el siguiente comando:

`git --version`

Si obtiene un resultado similar al siguiente, significa que Git ya está instalado.

Output
git version 2.25.1  

De ser así, puede pasar a la [configuración de Git](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-20-04#setting-up-git), o bien si necesita una versión más actualizada, puede leer la siguiente sección sobre [cómo instalar desde la fuente](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-20-04#installing-git-from-source).

Sin embargo, si no obtuvo como resultado un número de versión de Git, puede instalarlo con el administrador de paquetes predeterminado APT de Ubuntu.

1. Abre una terminal.
2. Ejecuta el siguiente comando para actualizar la lista de paquetes disponibles: `sudo apt update`
3. Instala Git usando el siguiente comando: `sudo apt install git`
4. Verifica la instalación de Git ejecutando el comando `git --version`

Una vez que Git esté instalado, puedes configurarlo para que se adapte a tus necesidades. Para configurar Git en Ubuntu, sigue estos pasos:

1. Establece tu nombre de usuario en Git utilizando el comando `git config --global user.name "Your Name"`
2. Establece tu dirección de correo electrónico en Git utilizando el comando `git config --global user.email "your.email@example.com"`
3. Para verificar la configuración actual de Git, utiliza el comando `git config --list`

Es recomendable usar un editor de texto para escribir los mensajes de commit, para esto se puede configurar con el siguiente comando `git config --global core.editor "nano"` o `git config --global core.editor "vi"` o el editor de tu preferencia.

## Instalación de Git desde la fuente

Si busca un método más flexible para instalar Git, puede optar por compilar el software desde la fuente, lo cual explicaremos en esta sección. Esto toma más tiempo y no se mantendrá en su administrador de paquetes, pero le permitirá descargar la versión más reciente y le brindará mayor control sobre las opciones que incluya si quiere personalizarlo.

Verifique la versión de Git que está instalada actualmente en el servidor:
`git --version`

Si Git está instalado, obtendrá un resultado similar al siguiente:

Output
git version 2.25.1

Antes de comenzar, debe instalar el software necesario para Git. Todo se encuentra disponible en los repositorios predeterminados, de modo que podemos actualizar nuestro índice local de paquetes y luego instalar los paquetes pertinentes.
`sudo apt update`  

`sudo apt install libz-dev libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext cmake gcc`  

Tras haber instalado las dependencias necesarias, cree un directorio temporal y vaya a él. Aquí es donde descargaremos nuestro tarball de Git.
`mkdir tmp`

`cd /tmp`

Desde el [sitio web del proyecto Git](https://git-scm.com/), podemos navegar a la lista de tarball disponible en [https://mirrors.edge.kernel.org/pub/software/scm/git/](https://mirrors.edge.kernel.org/pub/software/scm/git/) y descargar la versión que quiera utilizar. En el momento de escribir este artículo, la versión más reciente es 2.26.2, así que descargaremos esa versión para nuestra demostración. Utilizaremos curl y enviaremos el archivo que descarguemos a git.tar.gz.
`curl -o git.tar.gz https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.26.2.tar.gz`  

Descomprima el archivo tarball:

`tar -zxf git.tar.gz`

A continuación, vaya al nuevo directorio de Git:
`cd git-*`  

Ahora, podrá crear el paquete e instalarlo escribiendo estos dos comandos:
`make prefix=/usr/local all`

`sudo make prefix=/usr/local install`  

Ahora, sustituya el proceso de shell para que se utilice la versión de Git que acabamos de instalar:
`exec bash`  

Una vez completado esto, puede estar seguro de que su instalación se realizó correctamente comprobando la versión.
`git --version`

Output

git version 2.26.2

Con Git instalado correctamente, ahora puede finalizar su configuración.

## Configuración de Git

Una vez que esté satisfecho con la versión de Git, debería configurar Git de modo que los mensajes de confirmación que genere contengan la información correcta y lo respalden a medida que compile su proyecto de software.

Esta configuración es posible si aplicamos el comando git config. Específicamente, debemos proporcionar nuestro nombre y nuestra dirección de correo electrónico debido a que Git inserta esta información en cada confirmación que hacemos. Podemos añadir esta información escribiendo lo siguiente:
`git config --global user.name "Your Name"`

For example: `git config --global user.name "achalmed"`

`git config --global user.email "youremail@domain.com"`

`git config --global user.email "achalmaedison@outlook.com"`

Podemos ver todos los elementos de configuración creados escribiendo lo siguiente:
`git config --list`

Output

user.name=Your Name
user.email=youremail@domain.com
...

La información que ingresa se almacena en el archivo de configuración de Git. Tendrá la opción de editarlo manualmente con el editor de texto que prefiera (en este tutorial utilizaremos nano) como se muestra a continuación:
`nano ~/.gitconfig`  

~/.gitconfig contents

[user]
name = Your Name
email = youremail@domain.com

Para salir del editor de texto pulse CTRL y X, luego Y y, a continuación, ENTER.

Existen muchas otras opciones que puede configurar, pero estas son las dos esenciales que se necesitan. Si omite este paso, probablemente verá mensajes de advertencia cuando realice una confirmación con Git. Esto implica un mayor trabajo para usted, pues tendrá que revisar las confirmaciones que haya realizado con la información corregida.

## Conclusión

De esta manera, deberá tener Git instalado y listo para utilizarlo en su sistema.

# Cómo Obtener y Configurar tus Claves SSH para Git y GitHub

Recortado de: [https://www.freecodecamp.org/espanol/news/como-obtener-y-configurar-tus-claves-ssh-para-git-y-github/](https://www.freecodecamp.org/espanol/news/como-obtener-y-configurar-tus-claves-ssh-para-git-y-github/)

Si usas GitHub sin configurar una clave SSH, realmente te estás perdiendo de algo genial. Piensa en todo el tiempo que pasaste introduciendo tu correo electrónico y tu contraseña en la consola cada vez que haces un commit podrías haberlo pasado programando.

Bueno, ya no más. Aquí hay una guía rápida para generar y configurar una clave SSH con GitHub para que nunca más tengas que autentificarte a la antigua.

## Comprobar si existe una clave SSH

Primero, comprueba si ya has generado las claves SSH para tu máquina. Abre una terminal e introduce el siguiente comando:

`ls -al ~/.ssh`

Si ya has generado las claves SSH, deberías ver una salida similar a esta:

-rw-------  1 usuario usuario  1766 Jul  7  2018 id_rsa
-rw-r--r--  1 usuario usuario   414 Jul  7  2018 id_rsa.pub
-rw-------  1 usuario usuario 12892 Feb  5 18:39 known_hosts

Si tus claves ya existen, pasa a la sección **Copia tu clave pública de SSH** abajo.

Si no ves ninguna salida o ese directorio no existe (obtienes un mensaje de No such file or directory), entonces ejecuta:

`mkdir $HOME/.ssh`

Luego genera un nuevo conjunto de claves con:

`ssh-keygen -t rsa -b 4096 -C achalmaedison@outlook.com`

**Enter para crear el archivo con código con el nombre default, luego pide poner una clave para el uso del archivo for example 345320

*Ahora comprueba que tus claves existen con el comando ls -al ~/.ssh y asegúrate de que la salida es similar a la anterior.*

**Nota:** Las claves SSH siempre se generan como un par de claves públicas (id_rsa.pub) y privadas (id_rsa). Es extremadamente importante que **nunca reveles tu clave privada,** y que **sólo uses tu clave pública** para cosas como la autenticación de GitHub. Puedes leer más sobre cómo funcionan los pares de claves SSH / RSA [aquí](https://www.freecodecamp.org/news/a-top-down-introduction-to-ssh-965f4fadd32e/).

## Agrega tu clave SSH a ssh-agent

ssh-agent es un programa que se inicia cuando te conectas y almacena tus claves privadas. Para que funciones correctamente, debe estar ejecutándose y tener una copia de tu clave privada.

Primero, asegúrate de que ssh-agent se está ejecutando con:

`eval "$(ssh-agent -s)"` # para Mac y Linux

o:

`eval ssh-agent -s`

`ssh-agent -s` # para Windows

Entonces, agrega tu clave privada a ssh-agent con:

`ssh-add ~/.ssh/id_rsa`

## Copia tu clave pública de SSH

A continuación, tienes que copiar tu clave pública de SSH en el portapapeles.

Para Linux o Mac, imprime el contenido de tu clave pública en la consola con:

`cat ~/.ssh/id_rsa.pub` # Linux

Sale un conjunto números y letras, si al final está el correo que registro antes debe borrar para pegar en GitHub

Luego resalta y copia la salida.

O para Windows, simplemente ejecuta:

`clip < ~/.ssh/id_rsa.pub` # Windows

## Agrega tu clave SSH pública a GitHub

Ve a la página de [configuración](https://github.com/settings/keys) de tu GitHub y haz clic en el botón "New SSH key":

Luego dale a tu clave un título reconocible y pégala en tu clave pública (id_rsa.pub):

![](GetImage%20(46).png)

Finalmente, prueba la autenticación con:

`ssh -T git@github.com`

Si has seguido todos estos pasos correctamente, deberías ver este mensaje:

Hi tu_usuario! You've successfully authenticated, but GitHub does not provide shell access.  

or

Warning: Permanently added the ECDSA host key for IP address '140.82.114.3' to the list of known hosts.

Hi achalmed! You've successfully authenticated, but GitHub does not provide shell access.

## Más información sobre SSH

Traducido del artículo - [How to Get and Configure Your Git and GitHub SSH Keys](https://www.freecodecamp.org/news/git-ssh-how-to/)

VER DCUMENTACIO [https://cli.github.com/](https://cli.github.com/)  

## CLI de github

PRIMERO INSTALAR Installing gh on Linux  

`gh auth login`

`sudo apt  install gh  # version 2.12.1+dfsg1-1`

`gh auth login`

Eligir estas opciones

? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? SSH
? Generate a new SSH key to add to your GitHub account? Yes
? Enter a passphrase for your new SSH key (Optional) ****** es 345320
? Title for your SSH key: achalmagit
? How would you like to authenticate GitHub CLI? Login with a web browser

Luego copiar el codifo en el navegador para conectar con github

! First copy your one-time code: 5DCA-FB42

Enter

Press Enter to open github.com in your browser...  

Listo usa el coigo 345320 para trabajar con repostios de github en terminal

LISTO

VER DOCUMETACION DE GIT HUB

[https://cli.github.com/](https://cli.github.com/)

# Create a Repository

## git init [project name]

`git init` creará un nuevo repositorio local GIT. Inicializa un nuevo repositorio.

`git init [project name]`

> Se hace solo una vez. Como alternativa, puedes crear un repositorio dentro de un nuevo directorio especificando el nombre del proyecto:  `git init [nombre del proyecto]`

> **Comandos en visual code.** Los archivos con U indican que no tiene seguimiento. Los archivos con A ya estan en seguimiento con git. Cuando no hay A ni U entonces los archivos ya estan en linea. La M indica Modificaciones pendientes

### Git en Visual Code

Primero configurar git – paso anterior, usar cod ssh o instalar gh y usar git hub cli

Primero creamos espacio de trabajo en la carpeta del proyecto (el nombre puede ser distinto o igual a la carpeta)

**…or create a new repository on the command line**

echo "# achalmaedison.web" >> README.md  

1. Abrir el terminar integrado de la carpeta del proyecto en VCODE
2. `git init`
3. `git add README.md`
4. `git add .`
5. `git commit -m "comienzo del proyecto"` (enviamos al repostio en línea)
6. `git branch -M main`
Una vez haya modificaciones  

Podemos agregar los archivos mod con en el comando  

7. `git add index.html` (agregar archivos individuales)
8. `git commit - m "comienzo b"`
9. `git remote add origin https://github.com/achalmed/achalmaedison.web.git`
10. `git push -u origin main` Aqui se agrega el nombre del usuario "achalmed" y la contraseña 8920[ACHAL09med]2397 se debe escribir, no copy

**…or push an existing repository from the command line**

1. `git remote add origin https://github.com/achalmed/achalmaedison.web.git`  
2. `git branch -M main`
3. `git push -u origin main`

**…or import code from another repository**

You can initialize this repository with code from a Subversion, Mercurial, or TFS project.

## git clone my_url

`git clone my_url`: se usa para copiar un repositorio. Si el repositorio está en un servidor remoto, usa: `git clone nombredeusuario@host:/path/to/repository`  

A la inversa, ejecuta el siguiente comando básico para copiar un repositorio local: `git clone /path/to/repository`

### Cómo clonar el repositorio git

Git es un popular sistema de control de versiones utilizado por muchas empresas de todo el mundo. Sin embargo, requiere que tenga una copia del repositorio git antes de poder comenzar a trabajar en él. Debe clonar un repositorio de git en su computadora de escritorio o portátil local, antes de poder comenzar a realizar cambios en él. En este artículo, veremos cómo clonar un repositorio git en Ubuntu. Puede usar estos pasos para clonar un repositorio en github, bitbucket, gitlab y otras plataformas de desarrollo populares basadas en git.

### ¿Qué es git clone?

Git clone es básicamente un comando para apuntar a un repositorio existente y hacer una copia de él, en otra ubicación. En este caso, el comando git creará un nuevo directorio, lo configurará para su uso con git y copiará archivos en él. A menos que clone un repositorio git, no podrá contribuir con cambios a él.

### Clonar un repositorio remoto

Supongamos que desea clonar un repositorio remoto desde Github, Bitbucket o cualquier otra plataforma en la nube a su máquina local.

Abra el terminal y navegue hasta la ubicación (por ejemplo, /home/ubuntu) donde desea que se copie el repositorio.

`cd /home/ubuntu/`

Cada repositorio remoto de git tendrá una URL. Inicie sesión en su plataforma de desarrollo, como Github, y anote su URL. Será del formato.

[https://git-website.com/username/repository-name](https://git-website.com/username/repository-name)

Por ejemplo, su repositorio de git (por ejemplo, demostración) tendrá las siguientes URL, dependiendo de la plataforma.

Github

[https://github.com/username/demo.git](https://github.com/username/demo.git)

Bitbucket

[https://bitbucket.com/username/demo.git](https://bitbucket.com/username/demo.git)

A veces, la URL también puede ser de la forma

ssh://username@example.com/path/to/my-project.git  

Lea también: [Cómo instalar Virtualenv en Ubuntu](https://fedingo.com/how-to-install-virtualenv-in-ubuntu/)

Anote la URL de su repositorio y utilícela en el comando git clone como se muestra a continuación.

`sudo git clone https://github.com/username/repository-name`

Reemplace el nombre de usuario con su nombre de usuario de Github y el nombre del repositorio con el nombre de su repositorio. Por ejemplo

`sudo git clone https://github.com/test_user/demo.git`

Se le pedirá su contraseña para la autenticación, después de lo cual Git descargará automáticamente la copia de su repositorio a su directorio de trabajo actual.

Lea también: [Cómo actualizar Python en Ubuntu](https://fedingo.com/how-to-upgrade-python-in-ubuntu/)

### Clonación a una carpeta específica

Este es el comando para clonar el repositorio en una carpeta específica.

`sudo git clone <repo> <directory>`

Por ejemplo, supongamos que desea clonar su repositorio a la carpeta /home/developer

`sudo git clone https://github.com/test_user/demo.git /home/developer`

### Clonar superficialmente un repositorio

Si necesita clonar un repositorio grande con un gran historial de confirmaciones, puede llevar mucho tiempo. En tales casos, puede hacer un clon superficial donde puede especificar las últimas n confirmaciones que desea clonar. Será mucho más rápido y ocupará muy poco espacio en su sistema.

Aquí está la sintaxis para el clon superficial, donde n es el número de confirmaciones más recientes que desea clonar.

`sudo git clone -depth=n <repo>`

Lea también: [VPS vs alojamiento compartido: comparación en profundidad](https://fedingo.com/vps-vs-shared-hosting-in-depth-comparison/)

Aquí está el comando para clonar la última confirmación de 1 de su repositorio.

`sudo git clone -depth=1 https://github.com/test_user/demo.git`

Del mismo modo, aquí está el comando para clonar las últimas 10 confirmaciones de su repositorio.

`sudo git clone -depth=10 https://github.com/test_user/demo.git`

Clonar una rama de Git

Si solo desea clonar una rama específica (por ejemplo, trabajar) y no todo el repositorio, use la opción -branch en git clone.

`git clone -branch working https://github.com/test_user/demo.git`

Eso es todo. Como puede ver, es muy fácil clonar un repositorio git en Ubuntu.

From <[https://fedingo.com/how-to-clone-git-repository-in-ubuntu/?msclkid=98a3c8fbbcd911ec855d68473f662007](https://fedingo.com/how-to-clone-git-repository-in-ubuntu/?msclkid=98a3c8fbbcd911ec855d68473f662007)>

### Utilizar Git y Github para subir proyectos

`git clone https://github.com/achalmed/P-1-Thesis-economic-growth-poverty.git`

Recortado de: [https://www.redeszone.net/2013/06/08/utilizar-git-y-github-para-subir-proyectos-desde-ubuntu-ii/?msclkid=e54919b4be0411ec84047adbcd737726](https://www.redeszone.net/2013/06/08/utilizar-git-y-github-para-subir-proyectos-desde-ubuntu-ii/?msclkid=e54919b4be0411ec84047adbcd737726)

En [este artículo anterior](https://www.redeszone.net/2013/06/07/utilizar-git-y-github-desde-ubuntu-i/) **os hemos hecho una pequeña introducción a Git y GitHub en Ubuntu. Os hemos enseñado cómo instalarlo, identificarnos y a la vez identificarnos en GitHub.**

En ese artículo vamos a enseñar cómo podemos subir un proyecto desde el PC a GitHub para comenzar a gestionarlo desde allí. También os enseñaremos a utilizar los principales comandos para utilizarlo a través del terminal de Linux.

**Crear un nuevo repositorio**

En primer lugar debemos crear un nuevo repositorio desde la web de GitHub. Creamos un nuevo desde la página **«New Project«.*
![](Pasted%20image%2020230128185950.png)

Introduciremos el nombre del repositorio, una descripción y seleccionaremos si queremos que el repositorio sea público o privado (como privado habrá que pagar una suscripción). Una vez rellenado pulsamos sobre «Create Repository» y ya tenemos creado nuestro repositorio.

**Subir un proyecto**

Para subir un proyecto en primer lugar debemos crear nuestro proyecto Git de forma local en nuestro PC. Para ello debemos situarnos sobre la ruta del proyecto desde un terminal mediante el siguiente comando.

`cd ruta/al/archivo`  

Una vez situados allí debemos teclear el comando para crear un proyecto Git.

`git init`  

Veremos que el programa nos devuelve una línea de confirmación.

Ahora debemos añadir los archivos correspondientes a Git. Para ello debemos teclear una de las siguientes funciones dependiendo si queremos añadir únicamente un archivo o añadir todos los existentes en el proyecto.

`git add .` (añade todos los archivos existentes en la carpeta al proyecto Git)  

`git add nombredelarchivo.extension` (solo añade al proyecto el archivo especificado)  

Todos los cambios que se vayan realizando en nuestro proyecto deben ser identificados por un comentario. Añadimos el comentario mediante:

`git commit -m 'comentario'`  

Y ya podemos proceder a subir el proyecto a GitHub. Para ello debemos teclear en el terminal:

`git remote add origin git@github.com:achalmed/achalmaedison.web.git`

Debemos cambiar nick por nuestro nombre de usuario en GitHub y repositorio.git por el nombre del repositorio que hemos creado anteriormente. Pulsamos enter y ya podemos subir el proyecto mediante:

`git push -u origin master`  

Ya tenemos el proyecto subido en nuestra cuenta de GitHub. Podemos comprobarlo accediendo a la página del proyecto.

![](Pasted%20image%2020230128190024.png)

En caso de que en el paso anterior ocurra un error denominado: «fatal: remote origin already exists» debemos teclear:

`git remote rm origin`  

Y a continuación volver a realizar el proceso anterior.

# Observe your Repository

## git status

`git status` muestra la lista de los archivos que se han cambiado junto con los archivos que están por ser preparados o confirmados.

`git status -s` lista archivos sin sincronizar.

> Checa el estatus del repositorio actual.  List new or modified files not yet committed: `git status`

## git diff

- `git diff`  Show the changes to files not yet staged, se usa para hacer una lista de todos los conflictos.

- `git diff --base <file-name>` Para poder ver conflictos con respecto al archivo base

- `git diff <source-branch> <target-branch>`  se usa para ver los conflictos que hay entre ramas antes de fusionarlas:

- `git diff --cached`  Show the changes to staged files

- `git diff HEAD` Show all staged and unstaged file changes

- `git diff commit1 commit2` Show the changes between two commit ids

> Muestra las diferencias de los cambios hechos y que no han sido añadidos a un commit

## git blame [file]

`git blame [file]` List the change dates and authors for a file.

## git show

- `git show` se usa para mostrar información sobre cualquier objeto git.

- `git show [commit]:[file]` Show the file changes for a commit id and/or file.

## git log

`git log` : Muestra la lista de cambios hechos (commits), cuántas copias hay en respostorio, número de commits, show full change history.

`git log -p [file/directory]` : Show change history for file/directory including diffs.

`git log --oneline`

`git log --oneline --decorate --all --graph --since=2018-12-04`

> - git log se usa para ver el historial del repositorio listando ciertos detalles de la confirmación. Al ejecutar el comando se obtiene una salida como ésta:  commit 15f4b6c44b3c8344caasdac9e4be13246e21sadw Author: Alex Hunter [<alexh@gmail.com](mailto:%3Calexh@gmail.com)> Date:   Mon Oct 1 12:56:29 2016 -0600

### Ejemplos

achalmaubuntu@DESKTOP-ACHI23E:~/Documents/GitHub/achalmed$ git log
commit 8668f30bf15bb2b60d7a56ac0b41fc1d66f43afe (HEAD -> main)
Author: achalmed <achalmaedison@outlook.com>
Date:   Sat Apr 16 22:41:20 2022 -0500
    actualizando pefil

# Working with Branches

## git branch

- `git branch` List all local branches, se usa para listar, crear o borrar ramas. si quieres listar todas las ramas presentes en el repositorio.

- `git branch -av` List all branches, local and remote

- `git checkout [my_branch]` Switch to a branch, my_branch, and update working directory  

- `git branch [new_branch_name]` Create a new branch called new_branch  

- `git branch -d [branch_name]` Delete the branch called my_branch,  Si quieres borrar una rama

- `git branch –a`

> Muestra la lista de las ramas creadas

### Creando ramas (sirven para pruebas de version, etc)

1. `git branch [Rama2]` (Creación de una nueva rama basada en la rama actual)
2. `git log --oneline` (me indica todos los commit de la rama)
3. `git branch` (indica las ramas del proyecto e indica en que rama me encuentro)

*movernos a otra rama para hacer las modificaciones

4. `git checkout Rama2` (se movió mi flujo de trabajo a otra rama) por ejemplo esta rama puede ser rama de prueba

Una vez hecho las modificaciones de prueba  

5. `git add .` (agregamos los archivos modificados) AGREGANDO CAMBIOS
6. `git commit - m "saludos agrado a la rama de prueba"`
7. `git log --oneline` (me indica todos los commit de la rama nueva)

*Regresando a la rama Master o main

8. `git checkout [master]` (OJO LAS MODIFICACIONES HECHAS NO ESTAN AQUI)

OJO PARA NOTAR LOS CAMBIOS EN LOS ARCHIVOS MINIMIZAR EL CONSALA DE GIT

Para enviar finalmente los archivos al repositorio online se debe tipear:

9. `git push origin [Rama2]` : también puede ser main (es la rama, Enviar al GitHub)

## git checkout [file]

- `git checkout [file]` crea ramas y te ayuda a navegar entre ellas. Por ejemplo, el siguiente comando crea una nueva y automáticamente se cambia a ella:

command `git checkout -b [branch-name]`  

- Para cambiar de una rama a otra, sólo usa:

`git checkout [branch-name]`  

Merge branch_a into branch_b

- `git checkout [branch_b]`
- `git merge [branch_a]`

> Creación de una nueva rama y ubicación dentro de esa rama. Solucionar conflictos de … con Visual Code es más sencillo

### Fusionando ramas

PRIMERO debemos estar en la rama MASTER antes de hacer la fusión

1. `git checkout [master]`
2. `git merge [Rama2]`

## git rebase branch_name

`git rebase branch_name`: Alcanzar los cambios de un branch

## git tag [nombre_tag]  

- `git checkout [nombre_tag]`

- `git tag [nombre_tag]` Tag the current commit, creación de una etiqueta con el texto v0.0.1 (indica la version v0.0.1)

- `git tag [nombre_tag]/commit_SHA1` Creación de un tag a un commit en especifico  

Se puede acceder al commit donde se encuentra un tag mediante este comando

> `git tag` TAGS (INDICAN LAS VERSIONES DE UN PROYECTO). marca commits específicos. Los desarrolladores lo usan para marcar puntos de lanzamiento como v1.0 y v2.0.  `git tag 1.1.0 [instert-commitID-here]`

### Ejemplos

1. `git tag [26-03-2022v1] -m "Version 1 del proyecto"` (creando una version), por ejemplo sirve para descargar.

2. `git push --tags` (subimos las versiones a línea)

## git config

`git config --global alias.lodag‘log --oneline --decorate --all --graph’`  Agregar un alias  

`git config --global --get-regexp alias`  Ver la lista de alias creados  

`git config --global --unset alias.trololo`  Quitar un alias

- `git config` puede ser usado para establecer una configuración específica de usuario, como el email, nombre de usuario y tipo de formato, etc. Por ejemplo, el siguiente comando se usa para establecer un email:

`git config --global user.email tuemail@ejemplo.com`

- La opción -global le dice a GIT que vas a usar ese correo electrónico para todos los repositorios locales. Si quieres utilizar diferentes correos electrónicos para diferentes repositorios, usa el siguiente comando:

`git config --local user.email tuemail@ejemplo.com`

# Make a change

## git add [file]

- `git add -u`

- `git add [file]` Stages the file, ready for commit, se usa para agregar archivos al área de preparación. Por ejemplo, el siguiente comando de Git básico indexará el archivo temp.txt:

`git add <temp.txt>`  

- `git add .`  Stage all changed files, ready for commit,

> Con el nombre del archivo se registra dicho cambio en el caso de alguna creación, con el punto (.) se preparan todos los cambios realizados en el proyecto actual.  Lista de cambios preparados para subir en el siguiente commit.  (sincroniza todos los archivos)

### Ejemplos

`git add [index.html]` (agregamos unos de los archivos por ejemplo el index.html)

`git add` -actualiza todos tus cambios

1) Al modificar un/unos archivo/s:

`git branch` : para saber el rama actual

`git add .` Esto añade todos los archivos al repositorio local (no al web)

o sino también

`git add nombreDelArchivo` Esto añade solamente el archivo indicado al repositorio local.

2) Luego... se genera un commit para confirmar todos los archivos modificados agregando un mensaje que brinde una idea de lo que se modificó en el/los dichos archivo/s

`git commit -m "aquí el mensaje"`

3) Para enviar finalmente los archivos al repositorio online se debe tipear:

`git push origin [master]` : también puede ser main (es la rama)

Apendice A)

Si se quiere ir verificando el estado de la transacción luego de cada instrucción, puede tipear el siguiente comando:

`git status`

From <[https://github.com/cristian87dev/comandos-git/blob/master/Para%20subir%20cambios%20al%20servidor%20github.txt](https://github.com/cristian87dev/comandos-git/blob/master/Para%20subir%20cambios%20al%20servidor%20github.txt)>

## git commit

- `git commit` creará una instantánea de los cambios y la guardará en el directorio git.

- `git commit –m “El mensaje que acompaña al commit va aquí”`  

Ten en cuenta que los cambios confirmados no llegarán al repositorio remoto.

- `git commit -am “commit message”`  Commit all your tracked files to versioned history, agrega y envía

> Genera un archivo de los cambios realizados en el proyecto, en el archivo que se mostrará se agrega una descripción del cambio realizado. (toma una captura o crea una version)

### Ejemplos

`git commit -m "Comienzo del proyecto"`

`git commit -am "párrafo y tamaño fuente"` (agrega y envía )

## git add . && git commit -m "Cambionumeros"

`git add . && git commit -m "Cambionumeros"`

### Descripción

`git add . && git commit -m "Cambionumeros"` Add y commit en una sola línea

## git merge branch_name

`git merge branch_name`

### Descripción

Para este paso suponemos un ejemplo Tenemos el branchdevelop y feature, y queremos integrar la rama feature a develop por lo que debemos hacer los siguientes pasos:  

1. Ubicarse en la rama develop mediante el comando:

`gitcheckoutdevelop`  

2. Ingresar el comando  

`gitmergefeature`

> `git merge` se usa para fusionar una rama con otra rama activa: `git merge [branch-name]`

## git revert –m 1 SHA1_merge

`git revert –m 1 SHA1_merge`

### Descripción

Revierte un merge, especificando el SHA1 del merge que se quiere revertir

## git revert HEAD

`git revert HEAD`  

`git revert --no-commit HEAD`  

`git revert --no-commit HEAD~1`  

`git revert --continue`

### Descripción

Revierte un commit hecho sobre la rama actual  

Revertir dos o más commit junto al mismo comando de revert para ser tomados en cuenta como uno solo

## git reset

`git reset SHA_1_commit/[branch_name]`  

`git reset --soft SHA_1_commit/[branch_name]`  

`git reset --hard SHA_1_commit/[branch_nam]`

### Descripción

Regresar a una rama anterior, quita los cambios y los deja fuera del área de preparación  

Regresa a un commit o rama anterior, y deja los cambios hechos en el commit que se va a quitar listos en el área de preparación  

Regresa a un commit o rama anterior, y deja en blanco el área de preparación y el directorio de trabajo  

`766abcd`, es el identificador del commit al que deseamos regresar. Esta operación, si lo hacemos desde  una rama, no afectará a otras, de modo que puedes hacer diferentes commit a partir de ese punto, sin que se modifiquen otras ramas  del proyecto.

> `git reset` sirve para resetear el index y el directorio de trabajo al último estado de confirmación.

`git reset - -hard HEAD`  

> El conocimiento y el uso de log con sus diferente posibilidades, nos permitirá manejar acertadamente, la creación de ramas, los movimientos entre ellas y los avances y retrocesos entre commits.

### Regresar a un commit anterior en Git

Recortado de: [https://frankgalandev.com/regresando-a-un-commit-anterior-en-git/](https://frankgalandev.com/regresando-a-un-commit-anterior-en-git/)

Muchas veces, nos damos cuenta de que necesitamos regresar en el tiempo  a un punto de nuestro proyecto, para ello el comando checkout nos permite  regresar a un commit anterior en Git,  de esta manera:

Primero ver la estructura de los últimos commit con este comando

`git log --oneline`  

Su salida, será algo como esto

8674e5f commit  test3
jº44568 commit segunda parte  
55df4c2 commit de inicio.

`git checkout [766abcd]`  

Existen diferentes formas de retroceder en el tiempo a commits previos, **checkout** es una de ellas, pero también se utiliza **reset** con sus atributos **soft** o **hard**

Con una sintaxis como:

`git reset --soft` referencia del commit  

Esto nos permitirá retroceder a un commit previo, manteniendo los cambios:  

`git reset --soft [568abcj]`  

Si queremos deshacer solo el ultimo:  

`git reset --soft HEAD~`  

Si lo que se desea es eliminar permanentemente los cambios realizado después de un commit  específico, el comando a usar es:  

`git reset --hard [789abcd]` (regresar a una version, el codigo es el ultimo commit que queremos mantener)

Si queremos eliminar los cambios después del último commit lo que hacemos es usar el atributo hard del comando reset, pero dirigiéndolo al apuntador especial HEAD.

`git reset --hard HEAD~`  

para descartar los cambios antes de retornar a un commit, se utiliza el comando stash

`git commit stash`

# Synchronize

##

`git fetch` le permite al usuario buscar todos los objetos de un repositorio remoto que actualmente no se encuentran en el directorio de trabajo local.

`git fetch origin`

## git pull

`git pull` fusiona todos los cambios que se han hecho en el repositorio remoto con el directorio de trabajo local (actualizar las ediciones de línea en el repostorio local).
`git pull`

### Ejemplos

1) Para obtener los cambios desde el repositorio github.com debe tipear:

`git pull --rebase`

o tambien

`git pull origin [master]`

## git remote add NAME_REPO URL

`git remote add NAME_REPO URL`  

`git remote`  

`git remote –v`

### Descripción

- `git remote` te permite ver todos los repositorios remotos. El siguiente comando listará todas las conexiones junto con sus URLs: `git remote -v`  

- Para conectar el repositorio local a un servidor remoto, usa este comando: `git remote add origin [host-or-remoteURL]`  

- Por otro lado, el siguiente comando borrará una conexión a un repositorio remoto especificado: `git remote [nombre-del-repositorio]`

### Ejemplos

Adición de un repositorio  

Listado de los repositorios

## git push --set-upstream NAME_REPO master

`git push --set-upstream NAME_REPO master`  

`git push NAME_REPO BRANCH_NAME`  

`git push REMOTE --all git push REMOTE --tags`

### Descripción

- `git push` se usa para enviar confirmaciones locales a la rama maestra del repositorio remoto. Aquí está la estructura básica del código: `git push  origin [master]`  

- Reemplaza [master] con la rama en la que quieres enviar los cambios cuando no quieras enviarlos a la rama maestra.

### Ejemplos

Subir cambios de un Proyecto a gitLab  

3) Para enviar finalmente los archivos al repositorio online se debe tipear:

`git push origin [master]` : también puede ser main (es la rama)

# Finally

## git command --help

`git command --help`

`git command --help` When in doubt, use git help

## git stash

`git stash` guardará momentáneamente los cambios que no están listos para ser confirmados. De esta manera, pudes volver al proyecto más tarde.

## git ls-tree

`git ls-tree`

`git ls-tree HEAD`

### Descripción

- `git ls-tree` te permite ver un objeto de árbol junto con el nombre y modo de cada ítem, y el valor blob de SHA-1. Si quieres ver el HEAD, usa:

`git ls-tree HEAD`

## git cat-file

`git cat-file`: se usa para ver la información de tipo y tamaño de un objeto del repositorio. Usa la opción -p junto con el valor SHA-1 del objeto para ver la información de un objeto específico.

### Ejemplos

`git cat-file –p d670460b4b4aece5915caf5c68d12f560a9fe3e4`

## git grep

`git grep`: le permite al usuario buscar frases y palabras específicas en los árboles de confirmación, el directorio de trabajo y en el área de preparación. Para buscar por [www.hostinger.com](http://www.hostinger.com/) en todos los archivos, usa:

`git grep “www.hostinger.com”`

## gitk

`gitk`: muestra la interfaz gráfica para un repositorio local.

## git instaweb

`git instaweb`: te permite explorar tu repositorio local en la interfaz GitWeb. Por ejemplo:

`git instaweb –http=webrick`

## git gc

`git gc`:  limpiará archivos innecesarios y optimizará el repositorio local.

## git archive

`git archive`: le permite al usuario crear archivos zip o tar que contengan los constituyentes de un solo árbol de repositorio.

### Ejemplos

`git archive - -format=tar master`

## git prune

`git prune`: elimina los objetos que no tengan ningún apuntador entrante.

## git fsck

`git fsck`: realiza una comprobación de integridad del sistema de archivos git e identifica cualquier objeto corrupto

## git rebase

`git rebase`: se usa para aplicar ciertos cambios de una rama en otra.

### Ejemplos

`git rebase master`

## git rm

`git rm`

### Borrar archivos/carpetas del repositorio

Para borrar archivos o carpetas también «arriba» en nuestro respositorio (bitbucket, github…) se usa el comando «rm» de git siguiendo los siguientes pasos.

`git add -u` : actualiza todos los cambios

`git commit -m "elimino archivos innecesarios"`

3) Para enviar finalmente los archivos al repositorio online se debe tipear:

`git push origin master` : también puede ser main (es la rama)

1.A Si quieres eliminar un archivo:

`git rm miarchivo.php`

1.B. Si quieres eliminar una carpeta:

`git rm -r micarpeta`

2. Creamos el commit

`git commit -m "elimino archivos innecesarios"`

3. Subimos los cambios al repositorio

`git push`

# Hoja de trucos de los comandos de GIT en .pdf

Si estás empezando con GIT, puede ser difícil recordar incluso los comandos básicos. Por eso, hemos preparado una hoja de trucos de GIT para ayudarte a dominar el software. Guarda el archivo en tus dispositivos o imprímelo para tenerlo siempre listo cuando tengas que recordar los comandos de GIT.

[Descargar (tamaño: 1.2 MB)](https://cdn.hostinger.com/tutorials/pdf/Git-Cheat-Sheet-EN.pdf)

# Conclusión

Aprender los comandos básicos de GIT será de gran ayuda para los desarrolladores, ya que pueden controlar fácilmente el código fuente de los proyectos. Puede que te lleve algo de tiempo recordarlos todos, por eso nuestra hoja de trucos de GIT podría resultarte útil.

¡Practica estos comandos de GIT y aprovecha al máximo tus habilidades en desarrollo! ¡Buena suerte!

El autor  

Gustavo B.

Gustavo es un apasionado por la creación de sitios web. Se enfoca en la aplicación de estrategias SEO en Hostinger para España y Latinoamérica, así como la creación de contenidos de alto nivel. Cuando no está aplicando nuevos trucos en WordPress lo puedes encontrar tocando la guitarra, viajando o tomando un curso online.  

[Más de Gustavo B.](https://www.hostinger.es/tutoriales/author/gustavohostinger)
