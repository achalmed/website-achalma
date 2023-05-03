---
title: Cómo usar APK en Windows 11 una guía paso a paso
subtitle: Aprende a instalar y ejecutar aplicaciones de Android en tu PC con Windows 11
description: |
  Descubre cómo usar APK en Windows 11 para acceder a tus aplicaciones móviles favoritas desde tu PC. Esta guía paso a paso te muestra cómo instalar y ejecutar APK en Windows 11 sin problemas.
categories:
  - Tecnología
  - Informática
  - Android
tags:
  - Windows 11
  - APK
  - Instalación de aplicaciones
  - Emulador de Android
author: Edison Achalma Mendoza
date: "09/27/2022"
date-modified: "today"
draft: false
---



# Windows 11: Cómo descargar APK usando el subsistema de Windows para Android y ADB

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/install-logo-759x427.png?width=600)

Aquí se explica cómo descargar un archivo APK para instalar la aplicación de Android en su PC con Windows 11 usando el Subsistema de Windows para Android. Puede instalar Windows Subsystem para Android manualmente en su PC con Windows 11 usando su archivo Msixbundle de nuestra [guía aquí](https://nerdschalk.com/android-apps-on-windows-11-dev-channel-how-to-install-windows-subsystem-for-android-manually-with-msixbundle/) .

[Mostrar](https://nerdschalk.com/windows-11-how-to-sideload-apk-using-windows-subsystem-for-android-and-adb/#) **CONTENIDO** [](https://nerdschalk.com/windows-11-how-to-sideload-apk-using-windows-subsystem-for-android-and-adb/#)

## Paso 1: habilite el modo de desarrollador en el subsistema de Windows

Instale [el Subsistema de Windows para Android](https://nerdschalk.com/android-apps-on-windows-11-dev-channel-how-to-install-windows-subsystem-for-android-manually-with-msixbundle/) primero. Cuando haya terminado, abra la aplicación 'Subsistema de Windows para Android' en su PC. Para esto, presione la tecla de Windows y busque Subsistema de Windows para Android.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-09.png?width=800)

Haga clic en Subsistema de Windows para Android. O haga clic en Abrir.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-08.png?width=800)

En el Subsistema de Windows para Android, active el modo Desarrollador.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-10-2.png?width=800)

## Paso 2: Instale las herramientas de la plataforma SDK

Visite la página de herramientas de la plataforma SDK de Google [aquí](https://developer.android.com/studio/releases/platform-tools.html) .

Haga clic en Descargar SDK Platform-Tools para Windows.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-11.png?width=800)

Desplácese hacia abajo hasta el final y seleccione la casilla de verificación para aceptar los términos y condiciones. Luego haga clic en el botón verde para descargar las herramientas de la plataforma.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-12.png?width=700)

Se descargará en su PC un archivo zip llamado platform-tools_r31.0.3-windows (la versión puede cambiar).

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-13.png?width=700)

Para su comodidad, cree una nueva carpeta separada llamada carpeta para aplicaciones en el Explorador de Windows. Ahora, transfiera el archivo de herramientas de la plataforma a esta carpeta.

Haga clic con el botón derecho en el archivo de herramientas de la plataforma y seleccione Extraer todo.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-14.png?width=500)

Haga clic en Extraer.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-15-2.png?width=700)

El archivo será extraído. Abra la carpeta llamada herramientas de la plataforma.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-16.png?width=500)

Tendrá adb.exe y algunos otros archivos aquí.

**Relacionado:** [Cómo reiniciar el Explorador de Windows en Windows 11 y qué sucede cuando lo hace](https://nerdschalk.com/how-to-restart-windows-explorer-on-windows-11-and-what-happens-when-you-do-it/)

## Paso 3: Instale la aplicación de Android

Haga doble clic en la carpeta de herramientas de la plataforma para abrirla.

Aquí, haga clic en la barra de direcciones y escriba **cmd,** y luego presione la tecla Intro.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-20.png?width=500)

Se abrirá una ventana de comando con su ubicación establecida en la carpeta de herramientas de la plataforma. Esto es importante.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-21.png?width=800)

Ahora, tenemos la ventana del símbolo del sistema en la carpeta donde tenemos el archivo adb.exe. Es decir, nuestra carpeta de herramientas de plataforma.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-17.png?width=700)

Ahora, descargue el archivo APK de la aplicación de Android que desea instalar. Por ejemplo, si desea instalar Snapchat, busque **Snapchat APK** en Google y descargue su archivo APK desde cualquier sitio web confiable en el que confíe. Luego, cambie el nombre del archivo a algo más simple como snapchat.apk. Ahora, transfiera snapchat.apk a la carpeta de herramientas de la plataforma.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-18.png?width=700)

Ahora podemos instalar la aplicación Snapchat para Android usando snapchat.apk y adb en su PC.

Abra el Subsistema de Windows para Android y busque la IP donde se puede conectar con ADB en la opción de modo Desarrollador.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-19.png?width=800)

En la ventana del símbolo del sistema, escriba el siguiente comando y presione Entrar:

adb.exe connect (dirección IP-aquí)

Ejemplo: adb.exe conectar 127.0.0.1:12345

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-22.png?width=800)

Ahora, escriba el comando de instalación que se proporciona a continuación y luego presione Enter:

adb.exe install (apk-file-name-here.apk)

Ejemplo: adb.exe instalar Snapchat.apk

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-23.png?width=800)

La aplicación de Android ahora se instalará en su PC usando ADB y el archivo APK que proporcionó.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-24.png?width=800)

Cuando haya terminado, verá el mensaje de Éxito.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-25.png?width=800)

Puede cerrar la ventana CMD ahora.

Ahora puede abrir la aplicación de Android en su PC.

Presione la tecla de Windows y luego escriba el nombre de su aplicación. En nuestro caso, es Snapchat.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-27.png?width=800)

Así es como se ve Snapchat en Windows 11.

![](https://cdn.nerdschalk.com/wp-content/uploads/2021/10/get-android-apps-on-windows-11-dev-channel-26.jpg?width=800)

Eso es todo.

## Cargar APK automáticamente con un doble clic

Sabemos que usar un comando adb no es la forma más fácil de instalar una aplicación de Android en su PC. Afortunadamente, ahora puede hacer doble clic en un archivo APK para instalarlo. Consulta el siguiente enlace para saber cómo configurarlo.

**Leer:** [Cómo descargar APK en Windows 11 automáticamente con un doble clic](https://nerdschalk.com/how-to-sideload-apk-on-windows-11-automatically-with-a-double-click/)

Háganos saber cuál es su método favorito para cargar archivos APK en la PC.

**RELACIONADO**

- [¿Cómo deshabilitar VBS en Windows 11 y ayuda?](https://nerdschalk.com/how-to-disable-vbs-on-windows-11-and-does-it-help/)
- [Las 10 primeras cosas que hacer en Windows 11](https://nerdschalk.com/first-10-things-to-do-on-windows-11/)
- [Windows 11: Cómo crear mosaicos y widgets en vivo usted mismo](https://nerdschalk.com/windows-11-how-to-create-live-tiles-and-widgets/)
- [Cómo extender el volumen de Windows 11 o Windows 10](https://nerdschalk.com/how-to-extend-volume-windows-11-or-windows-10/)
- [Cómo usar Facetime en Windows](https://nerdschalk.com/how-to-facetime-windows-users/)  | [Androide](https://nerdschalk.com/how-to-facetime-android-users/)
- [Cómo calibrar el monitor en una PC con Windows 11](https://nerdschalk.com/how-to-calibrate-monitor-on-windows-11-pc/)
- [Cómo ejecutar juegos antiguos en Windows 11](https://nerdschalk.com/how-to-run-old-games-on-windows-11/)

[cómo](https://nerdschalk.com/tag/how-to/)[ventanas 11](https://nerdschalk.com/tag/windows-11/)

[

![](https://secure.gravatar.com/avatar/8ddaa30f5018c02bbfc30545a9a2b72a?s=96&d=retro&r=g)

](https://nerdschalk.com/author/ka1385/)

[publicado por

###### kapil malani

](https://nerdschalk.com/author/ka1385/)

Aficionado acérrimo del Liverpool FC, Kapil es un gran admirador de Batman, Android y Street Cricket. En ese orden, probablemente. Correo electrónico: kapil@theandroidsoul.com
