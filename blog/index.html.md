---
title: Blog Personal
subtitle: Un espacio donde comparto reflexiones, ideas y pensamientos sobre diversos temas. Desde experiencias personales hasta análisis críticos de la realidad, este blog es un reflejo de mis intereses y aprendizajes cotidianos.
listing:
  - id: ultimas-entradas
    contents: 
      - "posts/*/index.qmd"
    type: default # (table, default, table)
    sort: 
      - "date desc"
      - "title desc"
    date-format: short
    filter-ui: true
    categories: cloud # (numbered, unnumbered, cloud)
    feed: true
    fields: [image, date, title, author, reading-time]
# page-layout: full
# margin-header: signup.html
# title-block-banner: "#EDF3F9"
# title-block-banner-color: body
# css: index.css
search: false
comments: false
draft: false  # Modo de borrador solo esta pagina (false = final, true = borrador)
---
