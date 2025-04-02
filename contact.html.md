---
pagetitle: Edison Achalma - Contact
# title: Send me a note
name: Contact Form
page-layout: article
format: 
  html: 
    grid:
      margin-width: 0px
      sidebar-width: 0px

header-includes: >
  <link rel="stylesheet" href="assets/contact.css">
resources:
  - assets/contact.css
---







::: {.grid}

::: {.g-col-5 #note}

# Envíame una nota {{< fa feather-pointed >}}

Puedes utilizar este formulario para contactarme sobre charlas, colaboraciones o simplemente para saludarme.

También me encanta saber si mis materiales educativos te han resultado útiles y cómo podrían mejorarse, especialmente si pudieran hacerse más accesibles. {{< bi heart-fill >}}

<a class="link-dark me-1" href="/accessibility.html" title="Accessibility commitment" target="_blank" rel="noopener">{{< fa universal-access >}}</a>
<a class="link-dark me-1" href="https://bsky.app/profile/achalmaedison.com" title="bluesky" target="_blank" rel="noopener">{{< fa brands bluesky >}}</a>
<a class="link-dark me-1" href="https://linkedin.com/in/achalmaedison" title="LinkedIn" target="_blank" rel="noopener">{{< fa brands linkedin >}}</a>
<a class="link-dark me-1" href="https://github.com/achalmed" title="github" target="_blank" rel="noopener">{{< fa brands github >}}</a>
<!-- <a class="link-dark me-1" href="https://hachyderm.io/@achalmaedison" title="mastodon" target="_blank" rel="noopener">{{< fa brands mastodon >}}</a> -->
<a class="link-dark me-1" href="https://orcid.org/0000-0001-6996-3364" title="orcid" target="_blank" rel="noopener">{{< ai orcid >}}</a>
<a class="link-dark me-1" href="https://scholar.google.com/citations?hl=en&user=LvAkIvcAAAAJ" title="Google Scholar" target="_blank"rel="noopener">{{< ai google-scholar >}}</a>
<a class="link-dark me-1" href="https://buttondown.com/achalmaedison" title="Newsletter" target="_blank" rel="noopener">{{< fa envelope >}}</a>

:::
<!-- source: https://github.com/mccarthy-m-g/tidytales/blob/main/about/index.qmd#L24-L46 -->

::: {.g-col-1}
:::

::: {.g-col-6 #form}

<form 
style="margin-top: -5em;"
action="https://formspree.io/f/mgvananz" method="POST" accept-charset="utf-8">


<label for="full-name">Full Name</label>
<input type="text" name="name" id="full-name" class="form-control" placeholder="First and Last" required>

<label for="email-address">Email Address</label>
<input type="email" name="_replyto" id="email-address" class="form-control" placeholder="your@email.here" required>

<label for="message">Message</label>
  <textarea rows="6" name="message" id="message" class="form-control" placeholder="Aenean lacinia bibendum nulla sed consectetur. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Donec ullamcorper nulla non metus auctor fringilla nullam quis risus." required></textarea>

<button type="submit" class="btn btn-primary mt-4">Send message</button>
</form>

:::

::: {.g-col-5 #buttondown}

# Suscríbete a mi boletín informativo {{< fa envelope >}}

Puede utilizar este formulario para registrarse y recibir una pequeña nota por correo electrónico cada vez que publique algo nuevo en mi sitio web.

:::

::: {.g-col-1}
:::

::: {.g-col-6 #buttondown-form}








```{=html}
<form
  style="margin-top: 4em;"
  action="https://buttondown.com/api/emails/embed-subscribe/achalmaedison"
  method="post"
  target="popupwindow"
  onsubmit="window.open('https://buttondown.com/achalmaedison?tag=website', 'popupwindow')"
  class="embeddable-buttondown-form"
>
  <label for="bd-email">Email Address</label>
  <input 
  class="form-control"
  placeholder="your@email.here" 
  type="email" name="email" id="bd-email" />
  
  <input 
  class="btn btn-primary mt-1"
  type="submit" value="Subscribe" />
  <p>
    <a href="https://buttondown.com/refer/achalmaedison" target="_blank">Powered by Buttondown.</a>
  </p>
</form>
```







:::


:::
<!-- end grid -->
