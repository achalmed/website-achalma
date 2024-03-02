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
  - Windows11
  - APK
  - InstalaciónDeAplicaciones
  - EmuladorDeAndroid
citation:
  pdf-url: https://achalmaedison.netlify.app/docs/blog/posts/2021-10-21-usando-apk-en-windown-11/index.pdf
date: "10/21/2022"
draft: false  # Modo de borrador (false = final, true = borrador)
---




# Windows 11: Cómo descargar APK usando el subsistema de Windows para Android y ADB

Aquí se explica cómo descargar un archivo APK para instalar la aplicación de Android en su PC con Windows 11 usando el Subsistema de Windows para Android. Puede instalar Windows Subsystem para Android manualmente en su PC con Windows 11 usando su archivo Msixbundle de nuestra [guía aquí](https://nerdschalk.com/android-apps-on-windows-11-dev-channel-how-to-install-windows-subsystem-for-android-manually-with-msixbundle/) .


## Paso 1: habilite el modo de desarrollador en el subsistema de Windows

Instale [el Subsistema de Windows para Android](https://nerdschalk.com/android-apps-on-windows-11-dev-channel-how-to-install-windows-subsystem-for-android-manually-with-msixbundle/) primero. Cuando haya terminado, abra la aplicación 'Subsistema de Windows para Android' en su PC. Para esto, presione la tecla de Windows y busque Subsistema de Windows para Android.

Haga clic en Subsistema de Windows para Android. O haga clic en Abrir.

En el Subsistema de Windows para Android, active el modo Desarrollador.

## Paso 2: Instale las herramientas de la plataforma SDK

Visite la página de herramientas de la plataforma SDK de Google [aquí](https://developer.android.com/studio/releases/platform-tools.html) .

Haga clic en Descargar SDK Platform-Tools para Windows.

Desplácese hacia abajo hasta el final y seleccione la casilla de verificación para aceptar los términos y condiciones. Luego haga clic en el botón verde para descargar las herramientas de la plataforma.

Se descargará en su PC un archivo zip llamado platform-tools_r31.0.3-windows (la versión puede cambiar).

Para su comodidad, cree una nueva carpeta separada llamada carpeta para aplicaciones en el Explorador de Windows. Ahora, transfiera el archivo de herramientas de la plataforma a esta carpeta.

Haga clic con el botón derecho en el archivo de herramientas de la plataforma y seleccione Extraer todo.

Haga clic en Extraer.

El archivo será extraído. Abra la carpeta llamada herramientas de la plataforma.

Tendrá adb.exe y algunos otros archivos aquí.


## Paso 3: Instale la aplicación de Android

Haga doble clic en la carpeta de herramientas de la plataforma para abrirla.

Aquí, haga clic en la barra de direcciones y escriba **cmd,** y luego presione la tecla Intro.

Se abrirá una ventana de comando con su ubicación establecida en la carpeta de herramientas de la plataforma. Esto es importante.

Ahora, tenemos la ventana del símbolo del sistema en la carpeta donde tenemos el archivo adb.exe. Es decir, nuestra carpeta de herramientas de plataforma.

Ahora, descargue el archivo APK de la aplicación de Android que desea instalar. Por ejemplo, si desea instalar Snapchat, busque **Snapchat APK** en Google y descargue su archivo APK desde cualquier sitio web confiable en el que confíe. Luego, cambie el nombre del archivo a algo más simple como snapchat.apk. Ahora, transfiera snapchat.apk a la carpeta de herramientas de la plataforma.

Ahora podemos instalar la aplicación Snapchat para Android usando snapchat.apk y adb en su PC.

Abra el Subsistema de Windows para Android y busque la IP donde se puede conectar con ADB en la opción de modo Desarrollador.

En la ventana del símbolo del sistema, escriba el siguiente comando y presione Entrar:

adb.exe connect (dirección IP-aquí)

Ejemplo: adb.exe conectar 127.0.0.1:12345

Ahora, escriba el comando de instalación que se proporciona a continuación y luego presione Enter:

adb.exe install (apk-file-name-here.apk)

Ejemplo: adb.exe instalar Snapchat.apk

La aplicación de Android ahora se instalará en su PC usando ADB y el archivo APK que proporcionó.

Cuando haya terminado, verá el mensaje de Éxito.

Puede cerrar la ventana CMD ahora.

Ahora puede abrir la aplicación de Android en su PC.

Presione la tecla de Windows y luego escriba el nombre de su aplicación. En nuestro caso, es Snapchat.

Así es como se ve Snapchat en Windows 11.

Eso es todo.

## Cargar APK automáticamente con un doble clic

Sabemos que usar un comando adb no es la forma más fácil de instalar una aplicación de Android en su PC. Afortunadamente, ahora puede hacer doble clic en un archivo APK para instalarlo. Consulta el siguiente enlace para saber cómo configurarlo.


