#!/usr/bin/env node
// scripts/tokens.mjs — genera src/styles/paleta.generado.css desde la paleta del hub.
//
// Fuente: web/assets/scss/00-settings/_palette-light.scss y _palette-dark.scss («Quiet Laboratory»), los
// mismos valores crudos `$spc-*` que usan los 12 sitios Quarto. Aquí solo se publican como propiedades CSS
// `--spc-*`; los roles (`--papel`, `--tinta`, `--acento`…) se asignan a mano en src/styles/tokens.css.
// Simula por defecto (imprime lo que escribiría); `--aplicar` escribe.

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { RUTAS, AULA_DIR } from '../src/lib/rutas.mjs';

const aplicar = process.argv.includes('--aplicar');
const salida = join(AULA_DIR, 'src', 'styles', 'paleta.generado.css');

function leerPaleta(archivo) {
  const ruta = join(RUTAS.paletas, archivo);
  const pares = [];
  for (const linea of readFileSync(ruta, 'utf8').split('\n')) {
    const m = linea.match(/^\$(spc-[\w-]+):\s*(#[0-9A-Fa-f]{3,8})\s*!default;\s*(?:\/\/\s*(.*))?$/);
    if (m) pares.push({ nombre: m[1], valor: m[2].toUpperCase(), nota: m[3]?.trim() ?? '' });
  }
  if (!pares.length) throw new Error(`sin colores en ${ruta}`);
  return pares;
}

const claro = leerPaleta('_palette-light.scss');
const oscuro = leerPaleta('_palette-dark.scss');
const linea = (p) => `  --${p.nombre}: ${p.valor};${p.nota ? ` /* ${p.nota} */` : ''}`;
const css = `/* GENERADO por scripts/tokens.mjs desde web/assets/scss/00-settings/_palette-{light,dark}.scss; no editar.
   Valores crudos de «Quiet Laboratory» (hub). Los roles se asignan en tokens.css. */
:root {
${claro.map(linea).join('\n')}
${oscuro.map(linea).join('\n')}
}
`;

const actual = existsSync(salida) ? readFileSync(salida, 'utf8') : '';
if (actual === css) {
  console.log('tokens: paleta.generado.css al día');
} else if (aplicar) {
  writeFileSync(salida, css);
  console.log(`tokens: escrito ${salida} (${claro.length} claros, ${oscuro.length} oscuros)`);
} else {
  console.log(`tokens: simulación; escribiría ${salida} (${claro.length} + ${oscuro.length} colores). Usa --aplicar.`);
}
