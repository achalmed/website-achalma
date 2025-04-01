---
title: Combinando Hojas de Excel
subtitle: VBA
shorttitle: "Combinar Hojas de Excel"
description: |
  Accede al [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-05-31-combinando-hojas-de-excel-con-vba/index.pdf) completo aquí.
abstract: |
  | This article introduces a simple VBA macro designed to merge all sheets from multiple Excel files into a single workbook. The macro automates the process of data consolidation, which is particularly useful for repetitive tasks in econometrics or any field requiring data aggregation from various sources. The method involves opening each file in read-only mode, copying all sheets to a target workbook, and then closing the source workbook to proceed to the next file in the directory.
keywords: [VBA, Excel, Data Automation, Macros, Consolidation]
categories:
  - Ofimatica
  - Programación
  - Excel
  - VBA
tags:
  - Automatización
  - Macros
  - VBA Scripting
  - Data Merging
  - Office Efficiency
  - Automation Techniques
  - Spreadsheet Management
citation:
  pdf-url: https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-05-31-combinando-hojas-de-excel-con-vba/index.pdf
date: "05/31/2023"
draft: false  # Modo de borrador (false = final, true = borrador)
---












SEPARAR HOJAS DE EXCEL EN DOCUMENTOS INDIVIDUALES
Seguramente en cualquier ocasion les han pedido que deben separar un documento en excel, el cual contiene varias hojas, ya que por facilidad de visualización y trabajo el documento se debe tener de esta manera, pero al final debemos tener documentos individuales para ser enviados por separado o simplemente para darle otro tratamiento.
En este articulo aprenderemos a separar ese documento el cual contiene varias hojas y dejarlo en documentos individuales. Para ello solamente debemos ingresar al modo desarrollador en excel y copiar unas lineas de codigo y ejecutar y se realizara automaticamente la separacion.
Se deben seguir los siguientes pasos:

1- Creamos una carpeta donde vamos a guardar el documento el cual vamos a separar.
2- Abrimos el documento y pulsamos las teclas `alt+F11`.
3- De esta manera se abrirá el modo desarrollador, en la parte izquierda encontramos un icono que dice ver código. damos clic en el y se abrirá una ventana para insertar el código. Copiamos y pegamos el siguiente fragmento de código:

```
Sub Splitbook()
'Updateby20140612
Dim xPath As String
xPath = Application.ActiveWorkbook.Path
Application.ScreenUpdating = False
Application.DisplayAlerts = False
For Each xWs In ThisWorkbook.Sheets
    xWs.Copy
    Application.ActiveWorkbook.SaveAs Filename:=xPath & "\" & xWs.Name & ".xlsx"
    Application.ActiveWorkbook.Close False
Next
Application.DisplayAlerts = True
Application.ScreenUpdating = True
End Sub
```

4- Damos clic en el icono **Ejecutar Sub** el cual lo encontramos en la barra superior con un icono triangular.
5- Inmediatamente se ejecutará el código y vamos a visualizar la carpeta, encontrando las hojas ya separadas en documentos individuales.

De esta manera se habrá solucionado esa tarea que tal vez puede resultar tediosa si no conocemos mucho del modo desarrollador en excel.


# Publicaciones Similares

Si te interesó este artículo, te recomendamos que explores otros blogs y recursos relacionados que pueden ampliar tus conocimientos. Aquí te dejo algunas sugerencias:


1. [01 Introduccion Al Lenguaje Y Editor Vba](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-05-01-introduccion-al-lenguaje-y-editor-vba) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-05-01-introduccion-al-lenguaje-y-editor-vba/index.pdf)
2. [02 Grabar Y Modificar](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-12-02-grabar-y-modificar) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-12-02-grabar-y-modificar/index.pdf)
3. [03 Procedimientos](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-19-03-procedimientos) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-19-03-procedimientos/index.pdf)
4. [04 Funciones En Vba](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-26-04-funciones-en-vba) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2022-12-26-04-funciones-en-vba/index.pdf)
5. [05 Funciones Condicionales Estructuras Condicionales](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-02-05-funciones-condicionales-estructuras-condicionales) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-02-05-funciones-condicionales-estructuras-condicionales/index.pdf)
6. [06 Funciones Iterativas Estructuras Repetitivas O Bucles](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-09-06-funciones-iterativas-estructuras-repetitivas-o-bucles) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-09-06-funciones-iterativas-estructuras-repetitivas-o-bucles/index.pdf)
7. [07 Formularios](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-16-07-formularios) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-16-07-formularios/index.pdf)
8. [08 Eventos](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-23-08-eventos) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-01-23-08-eventos/index.pdf)
9. [Combinando Hojas De Excel Con Vba](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-05-31-combinando-hojas-de-excel-con-vba) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2023-05-31-combinando-hojas-de-excel-con-vba/index.pdf)
10. [Por Editar](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2024-03-31-por-editar) Lee sin conexión [PDF](https://achalmaedison.netlify.app/herramientas-oficina/ofimatica/2024-03-31-por-editar/index.pdf)


Esperamos que encuentres estas publicaciones igualmente interesantes y útiles. ¡Disfruta de la lectura!

