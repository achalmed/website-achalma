---
# documentmode: jou  # Modo de documento: Can be jou (journal), man (manuscript), stu (student), or doc (document)
    # - man (Manuscrito): Similar al formato .docx
    # - jou (Revista): Un formato pulido de dos columnas similar a muchas revistas APA.
    # - doc (Documento): Similar al predeterminado LaTex artículos.
    # - stu (Estudiante): Formateado para trabajos de estudiantes
# MODO ESTUDIANTE (STU)
# course: Metodología (EDUC 5101)
# professor: Dr. Edison Achalma Mendoza
# duedate: 01/23/2022
# MODO REVISTA (JOU)
# journal: The American Economic Review # Econometrica, The American Economic Review, Revista de Economía, Revista de la CEPAL
# volume: 2025, Vol. 131, No. 2, 10--60
copyrightnotice: 2019
copyrightext: All rights reserved
# image: featured.png
title: Guía de Git Cómo trabajar en equipo en proyectos
subtitle: Aprende a usar Git para controlar versiones, colaborar con otros desarrolladores y mantener tu código organizado.
shorttitle: "Editar"
abstract: |
  Primer parrafo de abstrac
keywords: [keyword1, keyword2]
categories:
  - Operating System
  - GitHub
tags:
  - Git
  - GitHub
  - Colaboración
  - DesarrolloDeSoftware
  - GitBasics
  - GitAdvanced
  - GitTips
  - OpenSource

# Nota del Autor
author-note:
  status-changes: 
    # Ejemplo: [Nombre del autor] está ahora en [afiliación].
    affiliation-change: ~
    # Ejemplo: [Nombre del autor] ha fallecido.
    deceased: ~
  # Las divulgaciones se condensan en un párrafo, pero puede iniciar un campo con dos saltos de línea para separarlas: \n\nNew 
  disclosures:
    # Ejemplo: Este estudio se registró en X (Identificador Y).
    study-registration: ~
    # Reconozca y cite los datos/materiales que se van a compartir.
    data-sharing: ~
    # Ejemplo: Este artículo se basa en datos publicados en [Referencia].
    # Ejemplo: Este artículo se basa en la disertación realizada por [cita].
    related-report: ~
    # Ejemplo: [Nombre del autor] ha sido consultor remunerado de la Corporación X, que ha financiado este estudio.
    conflict-of-interest: El autor no tiene conflictos de interés que revelar.
    # Ejemplo: Este estudio ha contado con el apoyo de la subvención [Número de subvención] de [Fuente de financiación].
    financial-support: ~
    # Ejemplo: Los autores agradecen a [Persona] por [Motivo].
    gratitude: ~
    # Ejemplo. Dado que los autores contribuyen por igual, el orden de autoría se determinó mediante el lanzamiento de una moneda al aire.
    authorship-agreements: ~

description: '' # Texto que se muestra debajo de las etiquetas, no en la página del listado
# links:
# - icon: pin-map-fill
#   name: Collection of maps
#   url: /project/2024-06-16-ccd-sips #./../talk/2021-03-16-xaringan-deploy-demo/
# - icon: github
#   icon_pack: fab
#   name: R-Ladies template files
#   url: https://github.com/spcanelon/RLadies-xaringan-template
eval: false # true(predeterminado): evaluar celda de código, false: no evaluar la celda de código
# Google Scholar
# bibliography: mybibliography.bib
citation:
  type: article-journal
  author:
    - Edison Achalma
  pdf-url: https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-de-git-y-github/index.pdf
date: "02/16/2023"
draft: false # Modo de borrador (false = final, true = borrador)
---









# Comandos ADB para Conectar y Instalar en Windows

## Versión de Microsoft Windows: 10.0.22000.282

(c) Microsoft Corporation. Todos los derechos reservados.

## Cambio de directorio a la ubicación de `ADB`

```sh
C:\Users\achalmaedison>cd "C:\Users\achalmaedison\Downloads\ADB"
```

## Conexión con ADB

```sh
C:\Users\achalmaedison\Downloads\ADB>adb connect 127.0.0.1:58526
```

**Salida esperada:**

```sh
Ya conectado a 127.0.0.1:58526
```

## Instalación de Instagram APK

```sh
C:\Users\achalmaedison\Downloads\ADB>adb install Instagram.apk
```

**Salida esperada:**

```sh
Realizando Instalación en Streaming
Instalación Exitosa
```

Este es un ejemplo de cómo utilizar los comandos ADB en un entorno Windows.

## Descarga de ADB

Puedes descargar ADB desde el siguiente enlace:

[Plataforma de herramientas de Android](https://developer.android.com/studio/releases/platform-tools)

## Configuración

1. Configurar el subsistema de Android.
2. Activar el modo desarrollador.
3. Copiar la dirección IP del dispositivo.
4. Abrir **CMD** como administrador.
5. Navegar a la carpeta `platform-tools` ubicada en `C:\platform-tools`:

```sh
cd C:\platform-tools
```

## Comandos para conexión e instalación de aplicaciones

Conectar el dispositivo:

```sh
adb connect 127.0.0.1:58526
```

Instalar aplicaciones:

```sh
adb install gmail.apk
```

```sh
adb install facebook-354-0-0-22-110.apk
```

**Nota:** Si los comandos no funcionan, intenta reiniciar el sistema.

## Ejemplo de salida esperada

```sh
Microsoft Windows [Version 10.0.22000.527]
(c) Microsoft Corporation. All rights reserved.
```

```sh
C:\platform-tools>adb connect 172.28.22.78
* daemon not running; starting now at tcp:5037
* daemon started successfully
connected to 172.28.22.78:5555
```

```sh
C:\platform-tools>adb install termux-app_v0.118.0+github-debug_arm64-v8a.apk
Performing Streamed Install
Success
```

```sh
C:\platform-tools>
```


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2017-05-21-comandos-de-informacion-windows/index.pdf) [Comandos De Informacion Windows](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2017-05-21-comandos-de-informacion-windows)
2. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2019-06-19-adb/index.pdf) [Adb](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2019-06-19-adb)
3. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-08-17-limpieza-y-optimizacion-de-pc/index.pdf) [Limpieza Y Optimizacion De Pc](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-08-17-limpieza-y-optimizacion-de-pc)
4. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11/index.pdf) [Usando Apk En Windown 11](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2021-10-21-usando-apk-en-windown-11)
5. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-05-12-gestionar-versiones-de-jdk-en-kubuntu/index.pdf) [Gestionar Versiones De Jdk En Kubuntu](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-05-12-gestionar-versiones-de-jdk-en-kubuntu)
6. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-07-21-instalar-tor-browser/index.pdf) [Instalar Tor Browser](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-07-21-instalar-tor-browser)
7. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-08-14-crear-enlaces-duros-o-hard-link-en-linux/index.pdf) [Crear Enlaces Duros O Hard Link En Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-08-14-crear-enlaces-duros-o-hard-link-en-linux)
8. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim/index.pdf) [Comandos Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2022-09-27-comandos-vim)
9. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-de-git-y-github/index.pdf) [Guia De Git Y Github](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-02-16-guia-de-git-y-github)
10. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux/index.pdf) [00 Primeros Pasos En Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-05-02-00-primeros-pasos-en-linux)
11. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux/index.pdf) [01 Introduccion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-17-01-introduccion-linux)
12. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux/index.pdf) [02 Distribuciones Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-18-02-distribuciones-linux)
13. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux/index.pdf) [03 Instalacion Linux](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-19-03-instalacion-linux)
14. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes/index.pdf) [04 Administracion Particiones Volumenes](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-06-20-04-administracion-particiones-volumenes)
15. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim/index.pdf) [Atajos De Teclado Y Comandos Para Usar Vim](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2023-07-01-atajos-de-teclado-y-comandos-para-usar-vim)
16. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2024-07-15-instalando-specitify/index.pdf) [Instalando Specitify](https://achalmaedison.netlify.app/tecnologia-seguridad/operating-system/2024-07-15-instalando-specitify)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

