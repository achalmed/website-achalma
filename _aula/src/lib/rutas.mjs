// src/lib/rutas.mjs — rutas de las fuentes del aula, equivalentes a core/env.py.
//
// La raíz del ecosistema es la carpeta que contiene core/env.py (el mismo marcador que usa core/env.py).
// Cada carpeta puede fijarse por variable de entorno con el mismo nombre que en core/env.py
// (DOCS_ROOT, CLASS_DIR, INDEX_DIR, SIMULADORES_DIR); si no, se deriva de la raíz como allí. DIVULGACION_DIR aún no está
// en core/env.py: se deriva igual (<raíz>/divulgacion) y admite la misma variable.
// Nada de este módulo escribe: el aula solo lee sus fuentes.

import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const MARCADOR = join('core', 'env.py');

function buscarRaiz() {
  if (process.env.DOCS_ROOT) return resolve(process.env.DOCS_ROOT);
  // Se sube desde la carpeta del proyecto (cwd) y, de respaldo, desde este archivo.
  for (const inicio of [process.cwd(), dirname(fileURLToPath(import.meta.url))]) {
    let d = resolve(inicio);
    while (true) {
      if (existsSync(join(d, MARCADOR))) return d;
      const padre = dirname(d);
      if (padre === d) break;
      d = padre;
    }
  }
  throw new Error('No se encontró la raíz del ecosistema (carpeta con core/env.py); fija DOCS_ROOT.');
}

const v = (nombre, defecto) => (process.env[nombre] ? resolve(process.env[nombre]) : defecto);

export const DOCS_ROOT = buscarRaiz();
export const CLASS_DIR = v('CLASS_DIR', join(DOCS_ROOT, 'docencia'));
export const INDEX_DIR = v('INDEX_DIR', join(DOCS_ROOT, 'web'));
export const SIMULADORES_DIR = v('SIMULADORES_DIR', join(DOCS_ROOT, 'simuladores'));
export const DIVULGACION_DIR = v('DIVULGACION_DIR', join(DOCS_ROOT, 'divulgacion'));

/** Carpeta del proyecto aula: la primera, subiendo desde cwd, con el package.json de «aula».
 *  (No se deriva de import.meta.url: en el build este módulo vive dentro de un chunk de dist.) */
function buscarAula() {
  if (process.env.AULA_DIR) return resolve(process.env.AULA_DIR);
  let d = resolve(process.cwd());
  while (true) {
    const pj = join(d, 'package.json');
    if (existsSync(pj) && /"name":\s*"aula"/.test(readFileSync(pj, 'utf8'))) return d;
    const padre = dirname(d);
    if (padre === d) break;
    d = padre;
  }
  return resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
}
export const AULA_DIR = buscarAula();

export const RUTAS = {
  areas: join(CLASS_DIR, 'config', 'areas.yml'),
  cursos: join(CLASS_DIR, 'contenido', 'cursos'),
  dictados: join(CLASS_DIR, 'contenido', 'dictados'),
  mapaLecciones: join(CLASS_DIR, 'contenido', 'migracion', 'mapa-lecciones.csv'),
  pubs: join(INDEX_DIR, '_pubs'),
  pubsYml: join(INDEX_DIR, '_pubs', 'pubs.yml'),
  cursosWeb: join(INDEX_DIR, 'cursos'),
  paletas: join(INDEX_DIR, 'assets', 'scss', '00-settings'),
  catalogoSimuladores: join(SIMULADORES_DIR, 'catalogo.json'),
  navegadorSimuladores: join(SIMULADORES_DIR, 'navegador.json'),
  catalogoDivulgacion: join(DIVULGACION_DIR, 'catalogo.json'),
  vitrina: join(AULA_DIR, 'config', 'vitrina.yml'),
};
