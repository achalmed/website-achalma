---
title: Finanzas
subtitle: Análisis de mercados financieros, inversión y estrategias económicas. Publicaciones sobre valoración de activos, teoría de portafolio, gestión de riesgos y economía financiera aplicada.
listing:
  - id: ultimas-entradas
    contents: 
      - "posts/*/index.qmd"
      - "finanzas-internacionales/*/index.qmd"
    type: default # (table, default)
    sort: 
      - "date desc"
      - "title desc"
    date-format: short
    # sort-ui: false
    filter-ui: false
    fields: [title, author, categories, date, image, reading-time]
    image-placeholder: sidebar.jpg
    image-align: right
   # page-size: 5
    categories: false # (numbered, unnumbered, cloud, false)
    feed: true
    
# page-layout: full
# margin-header: signup.html
# title-block-banner: "#EDF3F9"
# title-block-banner-color: body
# css: index.css

citation: false
toc: false
search: false
comments: false
draft: false  # Modo de borrador solo esta pagina (false = final, true = borrador)
format: 
  html: 
    page-layout: full
title-block-banner: false

header-includes: >
  <link rel="stylesheet" href="../assets/listing-default.css">
resources:
  - ../assets/listing-default.css
# include-after-body: ../assets/silvia/subscribe.html
---




<script data-name="BMC-Widget" data-cfasync="false" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="achalmaedison" data-description="Support me on Buy me a coffee!" data-message="¡Apóyame con un café! ☕✨
Si disfrutas mis blogs y artículos sobre economía, finanzas y análisis de datos, tu apoyo me ayudará a seguir creando contenido de calidad. ¡Gracias por contribuir a este espacio de aprendizaje! 🚀📚" data-color="#FF5F5F" data-position="Right" data-x_margin="18" data-y_margin="18"></script>