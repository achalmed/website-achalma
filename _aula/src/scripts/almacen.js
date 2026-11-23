// src/scripts/almacen.js — progreso y preferencias del visitante en su navegador (localStorage).
// Todo acceso va envuelto en try/catch: en una ventana privada, con el almacenamiento bloqueado o en una
// captura previa, la página funciona igual y simplemente no recuerda nada (decisiones §1.6).

const pub = () => document.documentElement.dataset.pub || 'aula';
const clave = () => `aula:${pub()}:completadas`;

function leer(k, defecto) {
  try {
    const v = localStorage.getItem(k);
    return v == null ? defecto : JSON.parse(v);
  } catch {
    return defecto;
  }
}
function escribir(k, valor) {
  try {
    localStorage.setItem(k, JSON.stringify(valor));
    return true;
  } catch {
    return false;
  }
}

/** { "curso/slug": "AAAA-MM-DD" } */
export function completadas() {
  const v = leer(clave(), {});
  return v && typeof v === 'object' ? v : {};
}
export function marcar(id, hecho) {
  const v = completadas();
  if (hecho) v[id] = new Date().toISOString().slice(0, 10);
  else delete v[id];
  escribir(clave(), v);
  document.dispatchEvent(new CustomEvent('aula:progreso', { detail: { id, hecho } }));
  return v;
}
/** Sustituye todo el progreso del pub (lo usa la sincronización con el aula con cuenta, src/scripts/aula-api.js). */
export function reemplazarCompletadas(v) {
  const ok = escribir(clave(), v && typeof v === 'object' ? v : {});
  document.dispatchEvent(new CustomEvent('aula:progreso', { detail: { sincronizado: true } }));
  return ok;
}
/** El calendario del repaso espaciado de un curso (`aula:<pub>:repaso:<curso>`, decisiones §1.25): solo los id de las
 *  preguntas con su caja y sus fechas; nada personal y nada que salga del navegador (no se sincroniza con el aula). */
export const claveRepaso = (curso) => `aula:${pub()}:repaso:${curso}`;
export function leerRepaso(curso) {
  return leer(claveRepaso(curso), null);
}
export function guardarRepaso(curso, estado) {
  return escribir(claveRepaso(curso), estado);
}
export function borrarRepaso(curso) {
  try {
    localStorage.removeItem(claveRepaso(curso));
    return true;
  } catch {
    return false;
  }
}
/** Si este navegador deja guardar (en una ventana privada o con el almacenamiento bloqueado, no). */
export function sePuedeGuardar() {
  try {
    const k = 'aula:prueba';
    localStorage.setItem(k, '1');
    localStorage.removeItem(k);
    return true;
  } catch {
    return false;
  }
}

export function preferencia(nombre, defecto) {
  return leer(`aula:${nombre}`, defecto);
}
export function guardarPreferencia(nombre, valor) {
  return escribir(`aula:${nombre}`, valor);
}

/** Pinta las celdas de retícula y los contadores de progreso de la página. */
export function pintarProgreso(raiz = document) {
  const hechas = completadas();
  raiz.querySelectorAll('[data-leccion]').forEach((el) => {
    el.classList.toggle('hecha', Boolean(hechas[el.dataset.leccion]));
  });
  raiz.querySelectorAll('[data-progreso-curso]').forEach((el) => {
    const ids = (el.dataset.progresoCurso || '').split(' ').filter(Boolean);
    const n = ids.filter((id) => hechas[id]).length;
    const texto = el.querySelector('[data-progreso-texto]');
    const barra = el.querySelector('[data-progreso-barra]');
    el.hidden = n === 0 && el.hasAttribute('data-ocultar-sin-progreso');
    if (texto) texto.textContent = n === 0 ? 'Aún no completas ninguna lección.' : `Completaste ${n} de ${ids.length} ${ids.length === 1 ? 'lección' : 'lecciones'}.`;
    if (barra) barra.style.setProperty('--avance', ids.length ? n / ids.length : 0);
  });
}
