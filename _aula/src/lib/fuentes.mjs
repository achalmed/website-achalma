// src/lib/fuentes.mjs — lectura (solo lectura) de las fuentes del aula.
//
// docencia: config/areas.yml, contenido/cursos/*/curso.yml, contenido/dictados/*/dictado.yml,
//           contenido/migracion/mapa-lecciones.csv
// web:      _pubs/pubs.yml, _pubs/<pub>/**/index.qmd (frontmatter) y su _site/ ya renderizado,
//           cursos/<materia>/<edicion>/ (páginas y materiales de las ediciones, hasta la fase 5)
// simuladores: catalogo.json
// aula:     config/vitrina.yml (presentación de cada pub: acento y nombre visible)

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { load } from 'js-yaml';
import { RUTAS, DOCS_ROOT } from './rutas.mjs';

const leer = (ruta) => readFileSync(ruta, 'utf8');
export const yaml = (ruta) => load(leer(ruta));

/** Frontmatter YAML de un .qmd o .md (null si no tiene). */
export function frontmatter(ruta) {
  const texto = leer(ruta);
  const m = texto.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  try {
    return load(m[1]) ?? {};
  } catch (e) {
    return { _error: String(e.message || e) };
  }
}

/** CSV separado por punto y coma, con comillas dobles (RFC 4180). */
export function csv(ruta, sep = ';') {
  const texto = leer(ruta).replace(/^﻿/, '');
  const filas = [];
  let fila = [], campo = '', comillas = false;
  for (let i = 0; i < texto.length; i++) {
    const c = texto[i];
    if (comillas) {
      if (c === '"') {
        if (texto[i + 1] === '"') { campo += '"'; i++; } else comillas = false;
      } else campo += c;
    } else if (c === '"') comillas = true;
    else if (c === sep) { fila.push(campo); campo = ''; }
    else if (c === '\n') { fila.push(campo.replace(/\r$/, '')); filas.push(fila); fila = []; campo = ''; }
    else campo += c;
  }
  if (campo || fila.length) { fila.push(campo); filas.push(fila); }
  const [cab, ...resto] = filas;
  return resto.filter((f) => f.length > 1).map((f) => Object.fromEntries(cab.map((k, i) => [k, f[i] ?? ''])));
}

export function areas() {
  return yaml(RUTAS.areas).areas;
}

export function registroPubs() {
  return yaml(RUTAS.pubsYml);
}

export function vitrina() {
  return existsSync(RUTAS.vitrina) ? yaml(RUTAS.vitrina) : {};
}

export function cursos() {
  return readdirSync(RUTAS.cursos)
    .filter((d) => existsSync(join(RUTAS.cursos, d, 'curso.yml')))
    .sort()
    .map((d) => yaml(join(RUTAS.cursos, d, 'curso.yml')));
}

export function dictados() {
  if (!existsSync(RUTAS.dictados)) return [];
  return readdirSync(RUTAS.dictados)
    .filter((d) => existsSync(join(RUTAS.dictados, d, 'dictado.yml')))
    .sort()
    .map((d) => ({ ...yaml(join(RUTAS.dictados, d, 'dictado.yml')), _dir: join(RUTAS.dictados, d) }));
}

/** Filas del mapa post → lección; ruta_post viene relativa a la raíz del ecosistema. */
export function mapaLecciones() {
  return csv(RUTAS.mapaLecciones).map((f) => ({ ...f, _abs: join(DOCS_ROOT, f.ruta_post) }));
}

export function catalogoSimuladores() {
  if (!existsSync(RUTAS.catalogoSimuladores)) return [];
  return JSON.parse(leer(RUTAS.catalogoSimuladores)).modelos ?? [];
}

export function esArchivo(ruta) {
  try { return statSync(ruta).isFile(); } catch { return false; }
}

export function tamano(ruta) {
  try { return statSync(ruta).size; } catch { return 0; }
}
