// src/lib/iconos.mjs — el único juego de íconos de la vitrina: Lucide (lucide-static, versión exacta en package.json,
// licencia ISC), en línea y con un mismo trazo (1,75) para todos. Se leen los nodos de icon-nodes.json en el build; el
// navegador no descarga nada. Decisión: docs/decisiones.md §1.16.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
let NODOS = null;
const nodos = () => (NODOS ??= JSON.parse(readFileSync(require.resolve('lucide-static/icon-nodes.json'), 'utf8')));
const escapar = (v) => String(v).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

/** SVG en línea de un ícono de Lucide; decorativo (aria-hidden) salvo que se pase `titulo`. */
export function icono(nombre, { tamano = 18, clase = '', titulo = null, trazo = 1.75 } = {}) {
  const n = nodos()[nombre];
  if (!n) throw new Error(`icono: «${nombre}» no está en lucide-static`);
  const cuerpo = n.map(([tag, attrs]) => `<${tag} ${Object.entries(attrs).map(([k, v]) => `${k}="${escapar(v)}"`).join(' ')}/>`).join('');
  const accesible = titulo ? `role="img" aria-label="${escapar(titulo)}"` : 'aria-hidden="true" focusable="false"';
  return `<svg class="icono${clase ? ' ' + clase : ''}" width="${tamano}" height="${tamano}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${trazo}" stroke-linecap="round" stroke-linejoin="round" ${accesible}>${cuerpo}</svg>`;
}
