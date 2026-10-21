// src/lib/marca.mjs — la marca de los 12 sitios (docs/decisiones.md §1.16): un ícono de aplicación (squircle con un
// degradado sutil del acento y el monograma del pub en blanco) y el nombre en Inter con la firma «por Edison Achalma».
// Los trazos vienen de marca.generado.mjs (scripts/marca.py). Aquí se componen:
// - en la página, con variables CSS (marca.astro), para que el color siga al data-acento;
// - en archivos (favicon.svg, PNG 32/180 e imagen Open Graph), con los colores resueltos desde los tokens, porque un
//   archivo suelto no conoce las variables de la página.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { MARCA } from './marca.generado.mjs';
import { AULA_DIR } from './rutas.mjs';

const CAP = 1490; // altura de mayúscula de Inter (unidades de fuente)

/** Transformación del monograma dentro de la caja 0–100 del ícono: centrado y a un 36 % de altura de mayúscula. */
export function colocarMonograma(sitio) {
  const m = MARCA.sitios[sitio]?.monograma;
  if (!m) throw new Error(`marca: no hay monograma para «${sitio}» (python3 scripts/marca.py --aplicar)`);
  const [x0, , x1] = m.caja;
  let s = 36 / CAP;
  if ((x1 - x0) * s > 62) s = 62 / (x1 - x0);
  const tx = 50 - (s * (x0 + x1)) / 2;
  const ty = 50 + (s * CAP) / 2;
  return { d: m.d, transform: `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(5)})` };
}

export const SQUIRCLE = MARCA.squircle;

// ── Colores resueltos desde los tokens (solo para los archivos) ─────────────────────────────────────────────────
let tokens = null;
function leerTokens() {
  if (tokens) return tokens;
  tokens = {};
  for (const f of ['paleta.generado.css', 'tokens.css']) {
    const css = readFileSync(join(AULA_DIR, 'src', 'styles', f), 'utf8');
    for (const m of css.matchAll(/--([\w-]+):\s*([^;]+);/g)) if (!(m[1] in tokens)) tokens[m[1]] = m[2].trim();
  }
  return tokens;
}
/** Valor hex de un token (sigue var(--x) hasta un hex). */
export function hex(nombre) {
  const t = leerTokens();
  let v = t[nombre];
  for (let i = 0; v && i < 6 && v.startsWith('var('); i++) v = t[v.slice(6, -1).split(',')[0].trim()];
  if (!v || !/^#[0-9a-f]{6}$/i.test(v)) throw new Error(`marca: el token --${nombre} no es un hex (${v})`);
  return v.toUpperCase();
}
const mezclar = (a, b, p) => '#' + [1, 3, 5].map((i) => Math.round(parseInt(a.slice(i, i + 2), 16) * p + parseInt(b.slice(i, i + 2), 16) * (1 - p)).toString(16).padStart(2, '0')).join('').toUpperCase();

export function coloresDe(acento) {
  const c = hex(`lab-${acento}`);
  const o = hex(`lab-${acento}-o`);
  return { acento: c, acentoOscuro: o, alto: mezclar(c, '#FFFFFF', 0.82), bajo: mezclar(c, '#000000', 0.78), blanco: hex('lab-blanco') };
}

/** El ícono como archivo SVG: squircle (o cuadrado lleno, para apple-touch-icon) con los colores fijos. */
export function svgIcono(sitio, acento, { cuadrado = false } = {}) {
  const k = coloresDe(acento);
  const m = colocarMonograma(sitio);
  const forma = cuadrado ? '<rect width="100" height="100"/>' : `<path d="${SQUIRCLE}"/>`;
  const relleno = (f) => forma.replace('/>', ` fill="${f}"/>`);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs>` +
    `<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${k.alto}"/><stop offset="1" stop-color="${k.bajo}"/></linearGradient>` +
    `<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${k.blanco}" stop-opacity=".22"/><stop offset=".5" stop-color="${k.blanco}" stop-opacity="0"/></linearGradient>` +
    `</defs>${relleno('url(#a)')}${relleno('url(#b)')}<path d="${m.d}" transform="${m.transform}" fill="${k.blanco}"/></svg>`;
}

/** Imagen Open Graph (1200 × 630): fondo grafito con trama de puntos, el ícono, el nombre, el área y la firma. */
export function svgOg(sitio, acento) {
  const s = MARCA.sitios[sitio];
  const k = coloresDe(acento);
  const fondo = hex('lab-fondo-o'), texto = hex('lab-texto-o'), texto2 = hex('lab-texto-2-o'), tenue = hex('lab-tenue-o'), linea = hex('lab-linea-o');
  const m = colocarMonograma(sitio);
  const linea1 = (t, x, y, px, color, max = 1008) => {
    let esc = px / MARCA.eme;
    if (t.avance * esc > max) esc = max / t.avance;
    return `<path d="${t.d}" transform="translate(${x} ${y}) scale(${esc.toFixed(5)})" fill="${color}"/>`;
  };
  const derecha = (t, xd, y, px, color) => linea1(t, (xd - t.avance * (px / MARCA.eme)).toFixed(1), y, px, color);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs>` +
    `<pattern id="p" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="${texto}" fill-opacity=".07"/></pattern>` +
    `<radialGradient id="h" cx=".85" cy="0" r=".75"><stop offset="0" stop-color="${k.acento}" stop-opacity=".45"/><stop offset="1" stop-color="${k.acento}" stop-opacity="0"/></radialGradient>` +
    `<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${k.alto}"/><stop offset="1" stop-color="${k.bajo}"/></linearGradient>` +
    `<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${k.blanco}" stop-opacity=".22"/><stop offset=".5" stop-color="${k.blanco}" stop-opacity="0"/></linearGradient>` +
    `</defs><rect width="1200" height="630" fill="${fondo}"/><rect width="1200" height="630" fill="url(#p)"/><rect width="1200" height="630" fill="url(#h)"/>` +
    `<g transform="translate(96 92) scale(1.44)"><path d="${SQUIRCLE}" fill="url(#a)"/><path d="${SQUIRCLE}" fill="url(#b)"/><path d="${m.d}" transform="${m.transform}" fill="${k.blanco}"/></g>` +
    linea1(s.nombre, 96, 390, 88, texto) +
    (s.area ? linea1(s.area, 98, 452, 34, texto2) : '') +
    `<rect x="96" y="508" width="1008" height="1" fill="${linea}"/>` +
    linea1(MARCA.firma, 98, 562, 26, tenue) +
    derecha(s.dominio, 1104, 562, 26, k.acentoOscuro) +
    `</svg>`;
}
