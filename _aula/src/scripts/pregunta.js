// src/scripts/pregunta.js — corrige en el navegador un formulario de src/components/pregunta-cerrada.astro y muestra su
// devolución: correcto o no, la respuesta correcta, el error común de la opción elegida si es un distractor que lo trae
// (`retro`) y la explicación. Todo va en la región `role="status"` de la pregunta, que el lector de pantalla anuncia.
import { corregir, textoCorrecto } from '../lib/quiz.mjs';

function datosDe(form) {
  try {
    return JSON.parse(form.dataset.quiz || '{}');
  } catch {
    return {};
  }
}

/** Limpia la devolución (otra vuelta de la misma pregunta). */
export function reiniciar(form) {
  form.reset();
  form.classList.remove('bien', 'mal', 'comprobada');
  form.querySelectorAll('label.es-correcta, label.elegida-mal').forEach((l) => l.classList.remove('es-correcta', 'elegida-mal'));
  const res = form.querySelector('[data-resultado]');
  if (res) res.textContent = '';
  form.querySelectorAll('[data-retro], [data-explicacion]').forEach((el) => { el.hidden = true; });
}

/**
 * Corrige el formulario y pinta la devolución. Devuelve 'bien', 'mal' o null si aún no hay una respuesta que corregir
 * (vacía o, en una numérica, algo que no es número: entonces solo se dice qué falta).
 */
export function comprobar(form) {
  const p = datosDe(form);
  const dato = new FormData(form).values().next().value;
  const { estado, retro } = corregir(p, dato);
  const res = form.querySelector('[data-resultado]');
  if (estado === 'vacia') {
    if (res) res.textContent = 'Elige o escribe una respuesta antes de comprobar.';
    return null;
  }
  if (estado === 'no-numero') {
    if (res) res.textContent = 'Escribe un número (puedes usar coma o punto decimal).';
    return null;
  }
  const bien = estado === 'bien';
  form.classList.add('comprobada');
  form.classList.toggle('bien', bien);
  form.classList.toggle('mal', !bien);
  form.querySelectorAll('label[data-opcion]').forEach((l) => {
    const op = l.dataset.opcion;
    const esCorrecta = p.tipo === 'opcion' ? Number(op) === p.correcta : op === String(Boolean(p.respuesta));
    l.classList.toggle('es-correcta', esCorrecta);
    l.classList.toggle('elegida-mal', !bien && op === String(dato));
  });
  const caja = form.querySelector('[data-retro]');
  if (caja) {
    caja.hidden = !retro;
    const t = caja.querySelector('[data-retro-texto]');
    if (t) t.textContent = retro || '';
  }
  // El texto del estado va al final: así el lector de pantalla anuncia la devolución completa de una vez.
  if (res) res.textContent = bien ? 'Correcto.' : `No es correcta. La respuesta es: ${textoCorrecto(p)}.`;
  const exp = form.querySelector('[data-explicacion]');
  if (exp) exp.hidden = false;
  return estado;
}
