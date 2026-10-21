// src/lib/contenido.mjs — extrae el cuerpo de una lección o un artículo del HTML que Quarto ya renderizó.
//
// Decisión §1.2 (docs/decisiones.md): se lee `_site/<post>/index.html` (fidelidad máxima: matemáticas,
// código con sus salidas, figuras) y se toma solo el contenido principal (`main#quarto-document-content`).
// Se quitan el bloque de título de Quarto, el apéndice, los estilos y scripts incrustados y el bloque
// «Publicaciones similares» que cada pub añade al final; las matemáticas se componen aquí con KaTeX, y las
// rutas relativas se resuelven: los recursos del post se copian junto a la página nueva y los enlaces a
// otros posts se reescriben a su URL nueva.

import * as cheerio from 'cheerio';
import katex from 'katex';
import { existsSync, readFileSync } from 'node:fs';
import { join, posix } from 'node:path';
import { esArchivo } from './fuentes.mjs';
import { icono } from './iconos.mjs';

// Ancho visible aproximado de un trozo de TeX, en caracteres: cada comando cuenta como uno; llaves, subíndices y
// espacios no cuentan. Alcanza para decidir si una ecuación cabe en un celular (unos 26 caracteres a 17 px).
function anchoTex(t) {
  return t.replace(/\\(left|right|big|Big|bigg|Bigg|,|;|:|!|quad|qquad)\b/g, '')
    .replace(/\\[a-zA-Z]+/g, 'x').replace(/[{}_^\s]/g, '').length;
}

const RELACIONES = ['\\approx', '\\equiv', '\\leq', '\\geq', '\\le', '\\ge', '='];

/** Versión partida de una ecuación larga: `LHS = t1 + t2 \\ + t3 …` en un `aligned` alineado tras la relación, con
 *  cortes solo en sumas y restas del nivel superior. null si no hace falta o no se puede (sin relación, ya alineada,
 *  cabe en el celular, o no hay dónde cortar). */
export function partirEcuacion(tex, anchoMax = 26) {
  if (/\\\\|\\begin\{|\\tag\b/.test(tex) || anchoTex(tex) <= anchoMax + 2) return null;
  let prof = 0, rel = null, cortes = [];
  for (let i = 0; i < tex.length; i++) {
    const c = tex[i];
    if (c === '\\') {
      const m = tex.slice(i).match(/^\\([a-zA-Z]+|.)/);
      const cmd = m[1];
      if (cmd === 'left') prof++;
      else if (cmd === 'right') prof--;
      else if (prof === 0 && !rel) {
        const r = RELACIONES.find((x) => x.slice(1) === cmd);
        if (r) rel = { i, fin: i + m[0].length, sig: r };
      }
      i += m[0].length - 1;
      continue;
    }
    if (c === '{') prof++;
    else if (c === '}') prof--;
    else if (prof === 0 && c === '=' && !rel) rel = { i, fin: i + 1, sig: '=' };
    else if (prof === 0 && rel && (c === '+' || c === '-')) {
      const antes = tex.slice(rel.fin, i).trimEnd();
      if (antes && !/[=+\-*/(,^_{]$|\\(cdot|times)$/.test(antes)) cortes.push(i);
    }
  }
  if (!rel || !cortes.length) return null;
  const izq = tex.slice(0, rel.i).trim();
  const der = tex.slice(rel.fin);
  const trozos = [];
  let desde = 0;
  for (const c of cortes.map((x) => x - rel.fin)) { trozos.push(der.slice(desde, c).trim()); desde = c; }
  trozos.push(der.slice(desde).trim());
  const presupuesto = Math.max(14, anchoMax - anchoTex(izq) - 1);
  const lineas = [];
  for (const t of trozos) {
    const ultima = lineas[lineas.length - 1];
    if (ultima && anchoTex(ultima + t) <= presupuesto) lineas[lineas.length - 1] = `${ultima} ${t}`;
    else lineas.push(t);
  }
  if (lineas.length < 2) return null;
  return `\\begin{aligned}${izq} ${rel.sig}{} &${lineas[0]} \\\\ ${lineas.slice(1).map((l) => `&{} ${l}`).join(' \\\\ ')}\\end{aligned}`;
}

const PROTOCOLOS_FUERA = /^(mailto:|tel:|data:|javascript:)/i;

/**
 * @param {object} o
 * @param {string} o.html        ruta del index.html renderizado
 * @param {string} o.siteRoot    carpeta _site del pub
 * @param {string} o.rutaVieja   ruta URL vieja del post, con / final (p. ej. /python/2021-…/)
 * @param {string} o.rutaNueva   ruta URL nueva, con / final
 * @param {URL}    o.dominio     URL pública del pub (para reconocer enlaces absolutos al propio sitio)
 * @param {Map<string,string>} o.mapaUrls  ruta vieja → ruta nueva de todos los posts publicados
 */
export function extraer(o) {
  const $ = cheerio.load(readFileSync(o.html, 'utf8'));
  const main = $('main#quarto-document-content').first();
  const recursos = [];
  const sinResolver = [];
  const figuras = [];

  // 1. Lo que no es contenido.
  // Las notas al pie y la bibliografía viven en el apéndice de Quarto: se rescatan antes de quitarlo.
  const apendice = main.find('#quarto-appendix');
  const notas = apendice.find('section#footnotes, #refs, section.quarto-appendix-contents#quarto-bibliography').clone();
  main.find('style, script, noscript, link, #title-block-header, .quarto-title-block, #quarto-appendix, nav#TOC, .code-copy-button, #particles-js, .quarto-alternate-formats').remove();
  if (notas.length) main.append(notas);
  main.contents().filter((_, n) => n.type === 'comment').remove();
  main.find('*').contents().filter((_, n) => n.type === 'comment').remove();
  main.find('section').each((_, s) => {
    const h = $(s).children('h1,h2,h3').first().clone();
    h.find('.header-section-number').remove();
    if (/^\s*publicaciones similares\s*$/i.test(h.text())) $(s).remove();
  });

  // 2. Matemáticas: KaTeX en la construcción, sin JS en el navegador.
  //    a) Un párrafo cuyo único contenido es una fórmula en línea es, de hecho, una ecuación: se muestra como bloque
  //       (si no, el navegador la corta donde cae, sin alinear; pasaba en epsilon-y-beta, 2026-10-21).
  main.find('p').each((_, p) => {
    const $p = $(p);
    const hijos = $p.contents().filter((_, n) => !(n.type === 'text' && !n.data.trim()));
    if (hijos.length === 1 && $(hijos[0]).is('span.math.inline')) $(hijos[0]).removeClass('inline').addClass('display');
  });
  //    b) Una ecuación de bloque larga con un signo de relación lleva además una versión partida en varias líneas,
  //       alineada justo después de ese signo, que solo se ve en pantallas angostas (contenido.css: .ec-angosta).
  let hayMatematicas = false;
  const opciones = (display) => ({ displayMode: display, throwOnError: false, output: 'htmlAndMathml', strict: 'ignore' });
  main.find('span.math').each((_, el) => {
    const $el = $(el);
    const display = $el.hasClass('display');
    let tex = $el.text().trim();
    tex = tex.replace(/^\\\(|\\\)$/g, '').replace(/^\\\[|\\\]$/g, '');
    try {
      const ancha = katex.renderToString(tex, opciones(display));
      const partida = display ? partirEcuacion(tex) : null;
      $el.replaceWith(partida
        ? `<div class="ec-larga"><div class="ec-ancha">${ancha}</div><div class="ec-angosta">${katex.renderToString(partida, opciones(true))}</div></div>`
        : ancha);
      hayMatematicas = true;
    } catch {
      /* se deja el texto fuente */
    }
  });

  // 3. Encabezados un nivel abajo: el h1 de la página es el título.
  for (let n = 5; n >= 1; n--) main.find(`h${n}`).each((_, el) => { el.name = `h${n + 1}`; });

  // 4. Código: fuera los anclajes vacíos de número de línea (enlaces sin texto) y, sobre cada bloque, una cabecera
  //    discreta con el lenguaje y el botón de copiar (nace oculto: lo activa el lector si hay JS y portapapeles).
  main.find('pre code a:empty').remove();
  main.find('pre.number-lines, pre.numberSource').removeClass('number-lines numberSource');
  const NO_LENGUA = new Set(['sourceCode', 'code-with-copy', 'cell-code', 'numberSource', 'number-lines', 'code-annotation-code']);
  const CONSOLA = /^(bash|sh|shell|zsh|console|powershell|ps1|cmd|bat|fish)$/i;
  main.find('div.sourceCode').each((_, el) => {
    const $b = $(el);
    const pre = $b.children('pre').first();
    if (!pre.length || $b.children('.codigo-barra').length) return;
    const lengua = (pre.attr('class') || '').split(/\s+/).find((c) => c && !NO_LENGUA.has(c)) || 'código';
    const ic = icono(CONSOLA.test(lengua) ? 'terminal' : 'code', { tamano: 14 });
    pre.before(`<div class="codigo-barra"><span class="codigo-lengua">${ic}${lengua}</span><button type="button" class="codigo-copiar" data-copiar hidden>${icono('copy', { tamano: 14 })}<span>Copiar</span></button></div>`);
  });

  // 5. Rutas.
  const resolverRef = (valor) => {
    if (!valor || valor.startsWith('#') || PROTOCOLOS_FUERA.test(valor)) return { tipo: 'igual' };
    let ruta = valor;
    if (/^https?:\/\//i.test(valor)) {
      let u;
      try { u = new URL(valor); } catch { return { tipo: 'igual' }; }
      if (u.host !== o.dominio.host) return { tipo: 'igual' };
      ruta = u.pathname + u.hash;
    }
    const [sinHash, hash = ''] = ruta.split('#');
    const sinQuery = sinHash.split('?')[0];
    let abs;
    try { abs = decodeURIComponent(posix.resolve(o.rutaVieja, sinQuery)); } catch { abs = posix.resolve(o.rutaVieja, sinQuery); }
    const anc = hash ? `#${hash}` : '';
    // a) otro post publicado → su URL nueva
    const dir = abs.endsWith('/index.html') ? abs.slice(0, -'index.html'.length) : abs.replace(/\/?$/, '/');
    if (o.mapaUrls.has(dir)) return { tipo: 'nueva', valor: o.mapaUrls.get(dir) + anc };
    const padre = posix.dirname(abs) + '/';
    if (padre !== o.rutaVieja && o.mapaUrls.has(padre) && /\.(pdf|docx)$/i.test(abs)) {
      // PDF o DOCX de otro post publicado: se sirve junto a su página nueva
      return { tipo: 'nueva', valor: o.mapaUrls.get(padre) + posix.basename(abs) };
    }
    const archivo = join(o.siteRoot, abs);
    if (esArchivo(archivo)) {
      if (abs.startsWith(o.rutaVieja)) {
        // recurso propio del post: se copia junto a la página nueva y la referencia relativa no cambia
        const rel = abs.slice(o.rutaVieja.length);
        recursos.push({ src: archivo, dest: o.rutaNueva + rel });
        return { tipo: 'nueva', valor: encodeURI(o.rutaNueva + rel) + anc, archivo };
      }
      // recurso compartido del sitio: se copia con la misma ruta absoluta
      recursos.push({ src: archivo, dest: abs });
      return { tipo: 'nueva', valor: encodeURI(abs) + anc };
    }
    if (existsSync(join(archivo, 'index.html'))) {
      // página del sitio viejo que la vitrina no publica (p. ej. una sección): se enlaza el sitio vivo
      return { tipo: 'nueva', valor: new URL(dir.slice(1), o.dominio).href + anc };
    }
    return { tipo: 'roto', abs };
  };

  for (const [sel, attr] of [['[src]', 'src'], ['[href]', 'href'], ['object[data]', 'data'], ['[poster]', 'poster']]) {
    main.find(sel).each((_, el) => {
      const $el = $(el);
      const r = resolverRef($el.attr(attr));
      if (r.tipo === 'nueva') {
        $el.attr(attr, r.valor);
        if (el.name === 'img' && r.archivo) figuras.push(r.archivo); // candidatas a miniatura (src/lib/imagenes.mjs)
      }
      else if (r.tipo === 'roto') {
        sinResolver.push({ ref: $el.attr(attr), abs: r.abs });
        if (el.name === 'a') $el.replaceWith(`<span class="enlace-sin-destino" title="Enlace sin destino en el sitio original">${$el.html() ?? ''}</span>`);
      }
    });
  }
  // Anclas internas: algunos posts traen un índice escrito a mano con anclas al estilo de GitHub
  // (#1-conceptos…) que no coinciden con los id de Quarto (conceptos…); ya estaban rotas en el sitio
  // Quarto. Se reparan cuando el id sin el número existe; si no, se informan.
  const ids = new Set(main.find('[id]').map((_, e) => $(e).attr('id')).get());
  let anclasReparadas = 0;
  main.find('a[href^="#"]').each((_, el) => {
    const $el = $(el);
    let frag = $el.attr('href').slice(1);
    try { frag = decodeURIComponent(frag); } catch { /* se deja tal cual */ }
    if (!frag || ids.has(frag)) return;
    const compacto = (x) => x.replace(/^\d+(-\d+)*-/, '').replace(/[^\p{L}\p{N}]/gu, '').toLowerCase();
    const bueno = [...ids].find((id) => compacto(id) === compacto(frag));
    if (bueno) { $el.attr('href', `#${bueno}`); anclasReparadas++; }
    else {
      sinResolver.push({ ref: `#${frag}`, abs: '(ancla sin sección en la página)' });
      $el.replaceWith(`<span class="enlace-sin-destino" title="Enlace sin destino en el sitio original">${$el.html() ?? ''}</span>`);
    }
  });

  // Figuras: carga diferida (arriba siempre está el título, que es la primera pintura) y tablas en un contenedor que se
  // desplaza solo él, para que la tabla conserve su ancho natural sin desbordar a 375 px.
  main.find('img').each((_, el) => {
    const $el = $(el);
    if (!$el.attr('loading')) $el.attr('loading', 'lazy');
    if (!$el.attr('decoding')) $el.attr('decoding', 'async');
  });
  main.find('table').each((_, el) => {
    const $el = $(el);
    // Los anchos fijos de Pandoc (colgroup) obligan a la tabla a no caber en un celular: el navegador reparte mejor.
    $el.children('colgroup').remove();
    // Cinco columnas o más: en el celular va compacta (contenido.css) para caber sin desplazarse.
    const columnas = Math.max(0, ...$el.find('tr').map((_, tr) => $(tr).children('th,td').length).get());
    // El marco lleva el borde redondeado; dentro, .tabla es lo que se desliza (así el desvanecido no borra el borde).
    if (!$el.parent().hasClass('tabla')) $el.wrap(`<div class="tabla-marco${columnas >= 5 ? ' tabla-densa' : ''}"><div class="tabla"></div></div>`);
  });
  // Pie de figura y de tabla al estilo APA 7: el rótulo («Tabla 1») en su línea y el título debajo.
  main.find('figcaption, caption').each((_, el) => {
    const $el = $(el);
    if ($el.find('.rotulo').length) return;
    const m = ($el.html() || '').match(/^\s*((?:Tabla|Figura|Cuadro|Gráfico|Gráfica|Listado|Ecuación|Table|Figure)(?:&nbsp;|\s)+[\w.-]+)\s*[:.]\s*/u);
    if (m) $el.html(`<span class="rotulo">${m[1].replace(/&nbsp;/g, ' ')}</span> <span class="titulo-float">${($el.html() || '').slice(m[0].length)}</span>`);
  });

  // Enlaces externos: sin dar acceso a la página de origen.
  main.find('a[href^="http"]').attr('rel', 'noopener');

  // 6. Índice de la página (secciones de primer y segundo nivel).
  const indice = [];
  main.find('section.level1, section.level2').each((_, s) => {
    const $s = $(s);
    const id = $s.attr('id');
    const h = $s.children('h2,h3').first().clone();
    if (!id || !h.length) return;
    const num = h.find('.header-section-number').text().trim();
    h.find('.header-section-number').remove();
    indice.push({ id, texto: h.text().trim(), numero: num, nivel: $s.hasClass('level1') ? 2 : 3 });
  });

  // 7. Muestra para la portada: cada sección de primer nivel con su primer párrafo y, si la tiene, su primera
  //    celda de código corta (las lecciones se publican sin salidas: no se muestran ni se inventan).
  const secciones = [];
  main.find('section.level1').each((_, s) => {
    const $s = $(s);
    const h = $s.children('h2').first().clone();
    const numero = h.find('.header-section-number').text().trim();
    h.find('.header-section-number').remove();
    const p = $s.find('p').filter((_, x) => $(x).text().trim().length > 80).first().text().trim().replace(/\s+/g, ' ');
    const code = $s.find('div.sourceCode pre code').filter((_, x) => $(x).text().split('\n').length <= 9).first();
    if (h.text().trim() && p) {
      secciones.push({
        id: $s.attr('id'),
        numero,
        titulo: h.text().trim(),
        parrafo: p.length > 300 ? p.slice(0, 297).replace(/\s+\S*$/, '') + '…' : p,
        codigo: code.length ? code.html() : null,
      });
    }
  });

  // 8. Tiempo de lectura: prosa a 200 palabras por minuto y código a 30 líneas por minuto.
  const copia = main.clone();
  const lineasCodigo = copia.find('pre').text().split('\n').length;
  copia.find('pre, .katex-mathml').remove();
  const palabras = copia.text().split(/\s+/).filter(Boolean).length;
  const minutos = Math.max(1, Math.ceil(palabras / 200 + lineasCodigo / 30));

  return { html: main.html() ?? '', anclasReparadas, indice, secciones, palabras, minutos, hayMatematicas, recursos, sinResolver, figuras };
}
