// src/lib/quiz.mjs — la corrección de una pregunta cerrada del formato `quiz:` (docs/decisiones.md §1.7), sin DOM: la usan
// la autoevaluación de una lección y el repaso espaciado del curso (src/scripts/pregunta.js), y sus pruebas
// (scripts/prueba-quiz.mjs). La clave del ítem NO se calcula aquí: llega ya resuelta en el `quiz:` (de la lección o de
// `docencia/scripts/alineamiento.py exportar --formato quiz`, la única fuente del banco).

export const TIPOS = ['opcion', 'vf', 'numerica'];

/** Número escrito por el estudiante: admite coma o punto decimal y espacios de millar. NaN si no es número. */
export function numero(s) {
  const t = String(s ?? '').trim().replace(/\s/g, '').replace(',', '.');
  return t === '' ? NaN : Number(t);
}

/** La pregunta se puede mostrar y corregir sola. */
export function valida(p) {
  if (!p || !p.enunciado || !TIPOS.includes(p.tipo)) return false;
  if (p.tipo === 'opcion') return Array.isArray(p.opciones) && p.opciones.length >= 2 && Number.isInteger(p.correcta) && p.correcta >= 0 && p.correcta < p.opciones.length;
  if (p.tipo === 'vf') return typeof p.respuesta === 'boolean';
  return Number.isFinite(Number(p.respuesta));
}

/** La respuesta correcta en palabras. */
export function textoCorrecto(p) {
  if (p.tipo === 'opcion') return String(p.opciones?.[p.correcta] ?? '');
  if (p.tipo === 'vf') return p.respuesta ? 'Verdadero' : 'Falso';
  return `${p.respuesta}${p.unidad ? ` ${p.unidad}` : ''}`;
}

/** El error común de cada opción (alineado con `opciones`; null en la correcta o si no se escribió). */
export function retroDe(p, j) {
  if (p.tipo !== 'opcion' || !Array.isArray(p.retro) || j === p.correcta) return null;
  const r = p.retro[j];
  return typeof r === 'string' && r.trim() ? r.trim() : null;
}

/**
 * Corrige la respuesta `dato` (el valor del formulario: índice de la opción, «true»/«false» o el número escrito).
 * Devuelve { estado: 'vacia' | 'no-numero' | 'bien' | 'mal', retro }: `retro` es el error común que delata la opción
 * elegida cuando es un distractor que lo tiene (null en lo demás).
 */
export function corregir(p, dato) {
  if (dato == null || String(dato).trim() === '') return { estado: 'vacia', retro: null };
  if (p.tipo === 'numerica') {
    const v = numero(dato);
    if (Number.isNaN(v)) return { estado: 'no-numero', retro: null };
    const bien = Math.abs(v - Number(p.respuesta)) <= Number(p.tolerancia || 0) + 1e-12;
    return { estado: bien ? 'bien' : 'mal', retro: null };
  }
  if (p.tipo === 'vf') {
    const bien = String(dato) === String(Boolean(p.respuesta));
    return { estado: bien ? 'bien' : 'mal', retro: null };
  }
  const j = Number(dato);
  const bien = j === p.correcta;
  return { estado: bien ? 'bien' : 'mal', retro: bien ? null : retroDe(p, j) };
}
