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
