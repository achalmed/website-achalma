// src/lib/marca.mjs — el colofón de los 12 sitios (docs/decisiones.md §1.18): el monograma del sitio en Petrona dentro de
// un cuadrado de doble filete, en el acento del sitio, como el sello de una editorial universitaria o de una revista.
// Dos variantes del mismo signo: «filete» (trazo y letras en el acento sobre el papel; cabecera, pie, familia, tarjetas)
// y «lleno» (cuadrado en el acento, letras y filete interior en el color del papel; favicon e ícono de pantalla de inicio,
// donde un filete fino no se vería). Los trazos vienen de marca.generado.mjs (scripts/marca.py). Se compone:
// - en la página, con variables CSS (marca.astro), para que el color siga al data-acento y al tema;
// - en archivos (favicon.svg, PNG 32/180 e imagen Open Graph), con los colores resueltos desde los tokens.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { MARCA } from './marca.generado.mjs';
import { AULA_DIR } from './rutas.mjs';

const CAP = 641; // altura de mayúscula de Petrona (unidades de fuente, eme = 1000)

/** Geometría del sello en una caja de 0 a 100: filete exterior, filete interior y el monograma centrado. */
export const SELLO = {
  exterior: { x: 3, y: 3, lado: 94, trazo: 3 },
  interior: { x: 10, y: 10, lado: 80, trazo: 1.2 },
};

/** Transformación del monograma: altura de mayúscula del 40 % de la caja, sin pasar del 64 % de ancho. */
export function colocarMonograma(sitio) {
  const m = MARCA.sitios[sitio]?.monograma;
  if (!m) throw new Error(`marca: no hay monograma para «${sitio}» (python3 scripts/marca.py --aplicar)`);
  const [x0, , x1] = m.caja;
  let s = 40 / CAP;
  if ((x1 - x0) * s > 64) s = 64 / (x1 - x0);
  const tx = 50 - (s * (x0 + x1)) / 2;
  const ty = 50 + (s * CAP) / 2;
  return { d: m.d, transform: `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(5)})` };
}

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

function cuadros(colorFilete, rellenoExterior = 'none') {
  const { exterior: e, interior: i } = SELLO;
  return `<rect x="${e.x}" y="${e.y}" width="${e.lado}" height="${e.lado}" fill="${rellenoExterior}" stroke="${colorFilete}" stroke-width="${e.trazo}"/>` +
    `<rect x="${i.x}" y="${i.y}" width="${i.lado}" height="${i.lado}" fill="none" stroke="${colorFilete}" stroke-width="${i.trazo}"/>`;
}

/** El sello como archivo SVG. «lleno»: cuadrado en el acento con letras y filete interior en el papel. */
export function svgSello(sitio, acento, { variante = 'lleno', cuadrado = false } = {}) {
  const ac = hex(`lab-${acento}`), papel = hex('spc-bg');
  const m = colocarMonograma(sitio);
  if (variante === 'lleno') {
    const i = SELLO.interior;
    const fondo = cuadrado ? `<rect width="100" height="100" fill="${ac}"/>` : `<rect x="1" y="1" width="98" height="98" fill="${ac}"/>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">${fondo}` +
      `<rect x="${i.x}" y="${i.y}" width="${i.lado}" height="${i.lado}" fill="none" stroke="${papel}" stroke-opacity=".55" stroke-width="2"/>` +
      `<path d="${m.d}" transform="${m.transform}" fill="${papel}"/></svg>`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">${cuadros(ac, papel)}<path d="${m.d}" transform="${m.transform}" fill="${ac}"/></svg>`;
}

/** Imagen Open Graph (1200 × 630): papel con retícula milimetrada tenue, el sello, el nombre en Petrona, el área y la firma. */
export function svgOg(sitio, acento) {
  const s = MARCA.sitios[sitio];
  const ac = hex(`lab-${acento}`), papel = hex('spc-bg'), tinta = hex('spc-primary'), tinta2 = hex('spc-primary-light'), tenue = hex('spc-text-muted'), linea = hex('spc-border-strong');
  const m = colocarMonograma(sitio);
  const linea1 = (t, x, y, px, color, max = 1008) => {
    let esc = px / t.eme;
    if (t.avance * esc > max) esc = max / t.avance;
    return `<path d="${t.d}" transform="translate(${x} ${y}) scale(${esc.toFixed(5)})" fill="${color}"/>`;
  };
  const derecha = (t, xd, y, px, color) => linea1(t, (xd - t.avance * (px / t.eme)).toFixed(1), y, px, color);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs>` +
    `<pattern id="mm" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0V12H0" fill="none" stroke="${ac}" stroke-opacity=".07" stroke-width="1"/></pattern>` +
    `<pattern id="cm" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0V60H0" fill="none" stroke="${ac}" stroke-opacity=".14" stroke-width="1"/></pattern>` +
    `</defs><rect width="1200" height="630" fill="${papel}"/><rect width="1200" height="630" fill="url(#mm)"/><rect width="1200" height="630" fill="url(#cm)"/>` +
    `<g transform="translate(96 84) scale(1.5)">${cuadros(ac, papel)}<path d="${m.d}" transform="${m.transform}" fill="${ac}"/></g>` +
    linea1(s.nombre, 96, 392, 96, tinta) +
    (s.area ? linea1(s.area, 98, 456, 38, tinta2) : '') +
    `<rect x="96" y="508" width="1008" height="1.5" fill="${linea}"/>` +
    linea1(MARCA.firma, 98, 562, 28, tenue) +
    derecha(s.dominio, 1104, 562, 28, ac) +
    `</svg>`;
}
