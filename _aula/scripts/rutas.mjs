// scripts/rutas.mjs — prueba de rutas antes del cambio de un pub a la vitrina (fase 7 de web/docs/plataforma-educativa.md).
// Para cada archivo que el sitio Quarto publica hoy (páginas .html, .pdf y .docx de su _site/), exige que la vitrina
// lo sirva tal cual o que una regla de dist/<pub>/_redirects lo lleve (301) a un archivo que exista en dist/<pub>/.
// Así ninguna URL publicada se pierde al cambiar `publish` del pub. Solo lee; no escribe nada.
// Uso: node scripts/rutas.mjs <pub>          (p. ej. methodica; lee web/_pubs/<pub>/_site y dist/<pub>)
// Salida: 0 todas las rutas viven · 1 alguna se pierde (la lista sale por pantalla) · 2 uso incorrecto.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { INDEX_DIR } from '../src/lib/rutas.mjs';

const pub = process.argv[2];
const viejo = pub && join(INDEX_DIR, '_pubs', pub, '_site');
const nuevo = pub && new URL(`../dist/${pub}/`, import.meta.url).pathname;
if (!pub || !existsSync(viejo) || !existsSync(nuevo)) {
  console.error('Uso: node scripts/rutas.mjs <pub>   (hace falta web/_pubs/<pub>/_site y dist/<pub>: PUB=<pub> npm run build)');
  process.exit(2);
}

// Lo que el sitio Quarto publica y alguien puede tener enlazado: páginas y documentos (no site_libs ni estilos).
const IGNORAR = /^(site_libs|assets|_extensions)\/|^(search\.json|sitemap\.xml|robots\.txt|listings\.json)$/;
const publicados = [];
(function recorrer(d) {
  for (const n of readdirSync(d)) {
    const f = join(d, n);
    if (statSync(f).isDirectory()) recorrer(f);
    else {
      const rel = relative(viejo, f).split('\\').join('/');
      if (!IGNORAR.test(rel) && /\.(html|pdf|docx)$/.test(rel)) publicados.push('/' + rel);
    }
  }
})(viejo);

// Reglas de _redirects (origen destino estado); `*` al final del origen y `:splat` en el destino, como Netlify.
const reglas = existsSync(join(nuevo, '_redirects'))
  ? readFileSync(join(nuevo, '_redirects'), 'utf8').split('\n').map((l) => l.trim())
      .filter((l) => l && !l.startsWith('#')).map((l) => l.split(/\s+/))
  : [];

const sirve = (ruta) => {
  const r = decodeURI(ruta);
  const f = join(nuevo, r);
  if (existsSync(f) && statSync(f).isFile()) return true;
  return existsSync(join(f, 'index.html'));
};
const redirige = (ruta) => {
  for (const [desde, hacia] of reglas) {
    let destino = null;
    if (desde.endsWith('/*') && ruta.startsWith(desde.slice(0, -1))) destino = hacia.replace(':splat', ruta.slice(desde.length - 1));
    else if (desde === ruta) destino = hacia;
    if (destino !== null) return destino;
  }
  return null;
};

const perdidas = [];
let directas = 0, redirigidas = 0;
for (const ruta of publicados) {
  // la portada de una página vale igual con su carpeta: /x/index.html ⇔ /x/
  if (sirve(ruta)) { directas++; continue; }
  const d = redirige(ruta);
  if (d && sirve(d)) { redirigidas++; continue; }
  perdidas.push(d ? `${ruta}  →  ${d} (no existe)` : `${ruta}  (sin página ni redirección)`);
}
console.log(`rutas de ${pub}: ${publicados.length} publicadas · ${directas} directas · ${redirigidas} redirigidas · ${perdidas.length} perdidas`);
for (const p of perdidas) console.log('  ✖ ' + p);
process.exit(perdidas.length ? 1 : 0);
