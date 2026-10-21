#!/usr/bin/env node
// scripts/enlaces.mjs — busca enlaces internos rotos en el sitio construido de un pub.
// Uso: node scripts/enlaces.mjs dist/methodica   (o: npm run enlaces -- dist/methodica)
// Revisa href, src y data de cada HTML: la ruta debe existir en dist (archivo, o carpeta con index.html) y,
// si lleva #fragmento, ese id debe existir en la página de destino. Los enlaces externos no se revisan.
// Sale con 1 si hay alguno roto.

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, posix, relative, resolve } from 'node:path';
import * as cheerio from 'cheerio';

const raiz = resolve(process.argv[2] || '');
if (!process.argv[2] || !existsSync(raiz)) {
  console.error('Uso: node scripts/enlaces.mjs dist/<pub>');
  process.exit(2);
}

const html = [];
(function recorrer(d) {
  for (const n of readdirSync(d)) {
    const r = join(d, n);
    if (statSync(r).isDirectory()) recorrer(r);
    else if (n.endsWith('.html')) html.push(r);
  }
})(raiz);

const ids = new Map();
const idsDe = (archivo) => {
  if (!ids.has(archivo)) {
    const $ = cheerio.load(readFileSync(archivo, 'utf8'));
    ids.set(archivo, new Set($('[id]').map((_, e) => $(e).attr('id')).get()));
  }
  return ids.get(archivo);
};
const destino = (ruta) => {
  const f = join(raiz, ruta);
  if (existsSync(f) && statSync(f).isFile()) return f;
  if (existsSync(join(f, 'index.html'))) return join(f, 'index.html');
  return null;
};

const rotos = [];
let revisados = 0;
for (const archivo of html) {
  const $ = cheerio.load(readFileSync(archivo, 'utf8'));
  const urlPagina = '/' + relative(raiz, archivo).split('\\').join('/');
  for (const [sel, attr] of [['a[href]', 'href'], ['[src]', 'src'], ['link[href]', 'href'], ['object[data]', 'data']]) {
    $(sel).each((_, el) => {
      const v = $(el).attr(attr);
      if (!v || /^(https?:|mailto:|tel:|data:|javascript:|\/\/)/i.test(v)) return;
      revisados++;
      const [ruta, frag] = v.split('#');
      let abs;
      try { abs = decodeURI(ruta ? posix.resolve(posix.dirname(urlPagina), ruta.split('?')[0]) : urlPagina); } catch { abs = ruta; }
      const f = ruta ? destino(abs) : archivo;
      if (!f) { rotos.push({ pagina: urlPagina, enlace: v, motivo: 'no existe' }); return; }
      if (frag && f.endsWith('.html') && !idsDe(f).has(decodeURIComponent(frag))) rotos.push({ pagina: urlPagina, enlace: v, motivo: 'fragmento sin id' });
    });
  }
}

console.log(`enlaces: ${html.length} páginas, ${revisados} enlaces internos revisados, ${rotos.length} rotos`);
for (const r of rotos) console.log(`  ${r.pagina}  →  ${r.enlace}  (${r.motivo})`);
process.exit(rotos.length ? 1 : 0);
