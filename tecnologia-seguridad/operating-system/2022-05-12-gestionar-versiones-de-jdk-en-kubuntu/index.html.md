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
copyrightnotice: 2022
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
draft: false  # Modo de borrador (false = final, true = borrador)
---









  
Gestionar varias versiones de JDK en Kubuntu (o cualquier distribución basada en Ubuntu) puede hacerse de varias maneras, aquí te describo algunas de las más comunes:

  

1. Usando update-alternatives para gestionar versiones JDK:

- Listar versiones instaladas:
    
    bash
    
    ```bash
    sudo update-alternatives --config java
    ```
    
    Esto te mostrará las versiones de Java disponibles y te permitirá elegir una como predeterminada.
    
- Instalar una nueva versión de JDK:
    
    - Puedes instalar diferentes versiones de OpenJDK usando apt:
        
        bash
        
        ```bash
        sudo apt update
        sudo apt install openjdk-8-jdk openjdk-11-jdk openjdk-17-jdk  # O cualquier otra versión que desees
        ```
        
    - Para Oracle JDK, generalmente necesitas añadir un PPA o descargarlo manualmente debido a las licencias:
        
        bash
        
        ```bash
        sudo add-apt-repository ppa:linuxuprising/java
        sudo apt update
        sudo apt install oracle-java11-installer  # Asegúrate de reemplazar 11 con la versión que quieras
        ```
        
- Configurar la versión predeterminada: Después de instalar, usa update-alternatives para elegir la versión predeterminada:
    
    bash
    
    ```bash
    sudo update-alternatives --config java
    sudo update-alternatives --config javac
    ```
    

  

2. Usando SDKMAN! para gestionar múltiples JDKs:

- Instalar SDKMAN!:
    
    bash
    
    ```bash
    curl -s "https://get.sdkman.io" | bash
    source "$HOME/.sdkman/bin/sdkman-init.sh"
    ```
    
- Listar versiones disponibles de JDK:
    
    bash
    
    ```bash
    sdk list java
    ```
    
- Instalar una versión específica:
    
    bash
    
    ```bash
    sdk install java <version-id>
    ```
    
    Donde <version-id> es el identificador de la versión que deseas instalar, como 8.0.265-zulu, 17.0.1-tem, etc.
    
- Cambiar entre versiones:
    
    bash
    
    ```bash
    sdk use java <version-id>
    ```
    
- Establecer una versión como predeterminada:
    
    bash
    
    ```bash
    sdk default java <version-id>
    ```
    
- Eliminar una versión:
    
    bash
    
    ```bash
    sdk uninstall java <version-id>
    ```
    
- Actualizar una versión: SDKMAN! puede manejar actualizaciones automáticamente, pero para actualizar manualmente:
    
    bash
    
    ```bash
    sdk upgrade java
    ```
    

  

3. Eliminar versiones de JDK:

- Eliminar con apt:
    
    bash
    
    ```bash
    sudo apt remove openjdk-8-jdk  # Reemplaza 8 con la versión que quieras eliminar
    ```
    
- Eliminar con SDKMAN!: Usa el comando mencionado anteriormente para desinstalar versiones.
    

  

Consideraciones:

- JAVA_HOME: Después de cambiar la versión de Java, asegúrate de actualizar la variable de entorno JAVA_HOME o usa SDKMAN! que puede manejar esto automáticamente.
    
- Compatibilidad de aplicaciones: Algunas aplicaciones pueden requerir una versión específica de Java. Asegúrate de probar después de cambiar la versión predeterminada.
    
- Actualizaciones de seguridad: Mantén tus JDKs actualizados para aplicaciones críticas debido a las actualizaciones de seguridad.
    

  

Estas herramientas y comandos te permitirán gestionar tus versiones de JDK en Kubuntu de manera eficiente, aunque para tareas más complejas o si tienes muchas versiones, SDKMAN! puede ser tu mejor aliado.


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

