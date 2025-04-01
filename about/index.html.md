---
title: "Edison Achalma"
subtitle: Data Scientist & Journalist
image: sidebar/vk-profile.jpg
image-alt: "Smiling woman with a tan complexion, dark eyes, and dark long wavy hair styled to one side"
about:
  template: trestles
  image-width: 14em
  image-shape: rounded
  id: hero-heading
  links:
    - text: "{{< fa universal-access >}}"
      aria-label: "Accessibility statement"
      href: accessibility.qmd
    - text: "{{< fa brands bluesky >}}"
      aria-label: "Bluesky"
      href: https://bsky.app/profile/silviacanelon.com
    - icon: linkedin
      aria-label: "LinkedIn"
      href: https://linkedin.com/in/achalmaedison
    - icon: github
      aria-label: GitHub
      href: https://github.com/achalmed
    # - icon: mastodon
    #   href: https://hachyderm.io/@achalmaedison
    - text: "{{< ai orcid >}}"
      href: https://orcid.org/0000-0001-6996-3364
    - text: "{{< ai google-scholar >}}"
      aria-label: "Google Scholar"
      href: https://scholar.google.com/citations?hl=en&user=LvAkIvcAAAAJ
    - text: "{{< fa envelope >}}"
      aria-label: Newsletter
      href: https://buttondown.com/achalmaedison
listing: 
- id: blog
  contents: 
    - "../blog/posts/*/index.qmd"
    - "../blog/posts/*/index.markdown"
  sort: date desc
  type: grid
  grid-columns: 1
  categories: false
  sort-ui: false
  filter-ui: false
  fields: [title, subtitle, image]
  max-items: 1
  image-height: "200"
- id: talk
  contents: 
    - "../talk/*/index.qmd"
    - "../talk/*/index.markdown"
  sort: date desc
  type: grid
  grid-columns: 1
  categories: false
  sort-ui: false
  filter-ui: false
  fields: [title, subtitle, image]
  max-items: 1
  image-height: "200"
- id: publication
  contents: 
    - "../publication/*/index.qmd"
    - "../publication/*/index.markdown"
  sort: date desc
  type: grid
  grid-columns: 1
  categories: false
  sort-ui: false
  filter-ui: false
  fields: [title, image]
  max-items: 1
  image-height: "200"
  image-placeholder: ../publication/featured.jpg
- id: project
  contents: 
    - "../project/*/index.qmd"
    - "../project/*/index.markdown"
  sort: date desc
  type: grid
  grid-columns: 1
  categories: false
  sort-ui: false
  filter-ui: false
  fields: [title, subtitle, image]
  max-items: 1
  image-height: "200"
format: 
  html: 
    page-layout: full

header-includes: >
  <link rel="stylesheet" href="../assets/about.css">
resources:
  - ../assets/about.css
---




::: {#hero-heading}
<div class="h1">Hey, I'm happy you're here</div>

Thanks for stopping by!

A lo largo de mi trayectoria, he adquirido experiencia en programación y seguridad informática. Estoy comprometido en la excelencia, el aprendizaje continuo, el impacto positivo y el respeto hacia los demás. Estos principios me guían en mi vida y en mi carrera, y me inspiran a alcanzar mis metas y contribuir al mundo de manera significativa. Learn more about my research interests in [publications](/publication).

Get in touch by [sending me a note](/contact.qmd)! {{< fa feather-pointed >}}

:::

## About me

::: {.grid}

::: {.g-col-6 #about-me-1}

**Economista convertido en informático, curioso por todas las intersecciones de los datos y la sociedad.**

I enjoy using [R](https://www.r-project.org/about.html) to optimize my data science workflow and have noticed it making guest appearances elsewhere in my life. I'm certified as an [RStudio Tidyverse Instructor](https://education.rstudio.com/trainers/people/canelon+silvia/) and am passionate about R education and data literacy as ways to build power in communities. Keep up with my R tinkering in my [blog](/blog) and presentations in [talks](/talk).

<ul class="fa-ul">
   <li><span class="fa-li"><i class="fa-solid fa-certificate"></i></span><a href="https://education.rstudio.com/trainers/people/canelon+silvia/">Tidyverse Instructor Certification</a> ∙ RStudio, PBC ∙ 2020</li>
</ul>

:::

::: {.g-col-6 #about-me-2}

Prior to joining the Urban Health Lab, I developed novel data mining methods to extract meaningful information from the EHR and study health outcomes and disparities in pregnant populations. I'm particularly interested in research that combines biomedical data science with open data sources in ways that prioritize health equity in communities.

<ul class="fa-ul">
   <li><span class="fa-li"><i class="fa-solid fa-certificate"></i></span><a href="https://www.med.upenn.edu/mbmi/certificate.html">Certificate in Biomedical Informatics</a> ∙ University of Pennsylvania ∙ 2019</li>
   <li><span class="fa-li"><i class="fa-solid fa-graduation-cap"></i></span>Ph.D. in Biomedical Engineering ∙ Purdue University ∙ 2018</li>
   <li><span class="fa-li"><i class="fa-solid fa-graduation-cap"></i></span>B.S. in Biomedical Engineering ∙ University of Minnesota ∙ 2012</li>
</ul>

:::

:::
<!-- end grid -->

## Lately ...

:::: {.grid}

::: {.g-col-3}
#### Blog
::: {#blog}
:::
[See all &rarr;](../blog){.about-links .subtitle}
:::

::: {.g-col-3}
#### Talks
::: {#talk}
:::
[See all &rarr;](../talk){.about-links .subtitle}
:::

::: {.g-col-3}
#### Publications
::: {#publication}
:::
[See all &rarr;](../publication){.about-links .subtitle}
:::

::: {.g-col-3}
#### Projects
::: {#project}
:::
[See all &rarr;](../project){.about-links .subtitle}
:::

::::
