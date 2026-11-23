// src/lib/espaciado.mjs — el calendario del repaso espaciado de un curso, sin DOM ni almacenamiento (decisiones §1.25).
// Lo usa src/scripts/repaso.js, que lo guarda en el localStorage del visitante; lo prueban scripts/prueba-repaso.mjs.
//
// Cajas de Leitner con intervalos que crecen: cada acierto seguido pasa la pregunta a la caja siguiente y la aleja
// INTERVALOS[caja - 1] días; un fallo la devuelve a la caja 0 y vuelve hoy mismo, al final de la vuelta, hasta acertarla
// (y entonces, mañana). Por qué así:
//   - El intervalo que mejor retiene crece con el plazo hasta la prueba, y para plazos de 6 meses o más es de al menos
//     un mes; los intervalos que crecen rinden igual o mejor que los fijos (Cepeda et al., 2006, p. 366).
//   - Medido contra ese plazo, el intervalo óptimo baja del 20-40 % (una semana) al 5-10 % (un año); para 35 y 70 días,
//     11 y 21 días (Cepeda et al., 2008, pp. 1095 y 1099). Un semestre son unos 120 días: el techo de 30 queda en ese
//     orden y los primeros pasos (1, 3, 7) sostienen las semanas de clase.
//   - Probarse y repartir la práctica son las dos técnicas más eficaces (Dunlosky, 2013, p. 13); probarse con
//     devolución hasta recordar cada pregunta al menos una vez, y volver a acertarla otro día (p. 14); estudiar en bloques breves repartidos en la semana, con lo nuevo y lo anterior (p. 15);
//     intercalar temas distintos (p. 16): la vuelta alterna las sesiones del curso.
// Las cifras exactas (1, 3, 7, 14, 30 y diez nuevas por día) son decisión de diseño, no de las obras.

export const VERSION = 1;
export const INTERVALOS = [1, 3, 7, 14, 30];   // días hasta la próxima vuelta tras el 1.º, 2.º… acierto seguido
export const CAJA_AFIANZADA = 4;                // desde aquí la pregunta vuelve a dos semanas o más
export const MAX_NUEVAS = 10;                   // preguntas nuevas por día: bloques breves, no un atracón

const ISO = /^\d{4}-\d{2}-\d{2}$/;

/** La fecha local del visitante (no la de UTC: a las 21 h en Lima ya sería mañana) como AAAA-MM-DD. */
export function fechaLocal(d = new Date()) {
  const dos = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${dos(d.getMonth() + 1)}-${dos(d.getDate())}`;
}

/** AAAA-MM-DD más n días (aritmética de calendario, sin husos ni horario de verano). */
export function sumarDias(iso, n) {
  const [a, m, d] = iso.split('-').map(Number);
  const f = new Date(Date.UTC(a, m - 1, d + n));
  return f.toISOString().slice(0, 10);
}

/** Días de a a b (b − a). */
export function diasEntre(a, b) {
  const t = (iso) => { const [x, y, z] = iso.split('-').map(Number); return Date.UTC(x, y - 1, z); };
  return Math.round((t(b) - t(a)) / 86_400_000);
}

/** El estado guardado, saneado: lo que no tenga la forma esperada se descarta (otra versión, datos rotos). */
export function normalizar(crudo) {
  const estado = { v: VERSION, preguntas: {}, sesiones: null };
  if (!crudo || typeof crudo !== 'object' || crudo.v !== VERSION) return estado;
  for (const [id, x] of Object.entries(crudo.preguntas ?? {})) {
    if (!x || typeof x !== 'object' || !ISO.test(x.proxima ?? '')) continue;
    const caja = Number.isInteger(x.caja) ? Math.min(Math.max(x.caja, 0), INTERVALOS.length) : 0;
    estado.preguntas[id] = {
      caja, proxima: x.proxima, ultima: ISO.test(x.ultima ?? '') ? x.ultima : null,
      aciertos: Number.isInteger(x.aciertos) ? x.aciertos : 0, fallos: Number.isInteger(x.fallos) ? x.fallos : 0,
    };
  }
  if (Array.isArray(crudo.sesiones)) estado.sesiones = crudo.sesiones.filter((s) => typeof s === 'string');
  return estado;
}

/** Anota una respuesta de hoy y programa la próxima vuelta. Devuelve la entrada nueva (y la deja en `estado`). */
export function registrar(estado, id, bien, hoy) {
  const prev = estado.preguntas[id] ?? { caja: 0, aciertos: 0, fallos: 0 };
  const caja = bien ? Math.min(prev.caja + 1, INTERVALOS.length) : 0;
  const entrada = {
    caja,
    proxima: bien ? sumarDias(hoy, INTERVALOS[caja - 1]) : hoy,
    ultima: hoy,
    aciertos: prev.aciertos + (bien ? 1 : 0),
    fallos: prev.fallos + (bien ? 0 : 1),
  };
  estado.preguntas[id] = entrada;
  return entrada;
}

/** Ordena alternando las sesiones (s01, s02, s03, s01, …), conservando el orden dentro de cada una. */
export function intercalar(items) {
  const grupos = new Map();
  for (const it of items) {
    if (!grupos.has(it.sesion)) grupos.set(it.sesion, []);
    grupos.get(it.sesion).push(it);
  }
  const colas = [...grupos.values()];
  const out = [];
  for (let i = 0; out.length < items.length; i++) for (const c of colas) if (i < c.length) out.push(c[i]);
  return out;
}

/** Las preguntas del curso que el visitante repasa (las de las sesiones que eligió; todas, si no eligió). */
export function elegidas(estado, preguntas) {
  const s = estado.sesiones;
  return Array.isArray(s) ? preguntas.filter((p) => s.includes(p.sesion)) : preguntas;
}

/**
 * La vuelta de hoy: primero las que vencen (la más atrasada primero), después hasta `maxNuevas` que nunca vio, en el
 * orden del curso; cada grupo, intercalado por sesión. `preguntas`: [{ id, sesion, … }].
 */
export function vueltaDeHoy(estado, preguntas, hoy, { maxNuevas = MAX_NUEVAS } = {}) {
  const lista = elegidas(estado, preguntas);
  const vencidas = lista
    .filter((p) => estado.preguntas[p.id] && estado.preguntas[p.id].proxima <= hoy)
    .sort((a, b) => (estado.preguntas[a.id].proxima < estado.preguntas[b.id].proxima ? -1 : estado.preguntas[a.id].proxima > estado.preguntas[b.id].proxima ? 1 : 0));
  const nuevas = lista.filter((p) => !estado.preguntas[p.id]);
  return { vencidas: intercalar(vencidas), nuevas: intercalar(nuevas.slice(0, Math.max(0, maxNuevas))), nuevasRestantes: Math.max(0, nuevas.length - maxNuevas) };
}

/** Cuántas vuelven cada día de los próximos `dias` (desde mañana) y cuántas más adelante. */
export function calendario(estado, preguntas, hoy, dias = 14) {
  const lista = elegidas(estado, preguntas);
  const cuenta = new Map();
  let despues = 0;
  for (const p of lista) {
    const e = estado.preguntas[p.id];
    if (!e || e.proxima <= hoy) continue;
    const d = diasEntre(hoy, e.proxima);
    if (d <= dias) cuenta.set(e.proxima, (cuenta.get(e.proxima) ?? 0) + 1);
    else despues++;
  }
  const filas = [...cuenta.entries()].sort(([a], [b]) => (a < b ? -1 : 1)).map(([fecha, n]) => ({ fecha, n, en: diasEntre(hoy, fecha) }));
  return { filas, despues };
}

/** El estado de las preguntas elegidas: sin ver, aprendiendo (vencen pronto o se fallaron) y afianzadas. */
export function resumen(estado, preguntas) {
  const lista = elegidas(estado, preguntas);
  let nuevas = 0, aprendiendo = 0, afianzadas = 0;
  for (const p of lista) {
    const e = estado.preguntas[p.id];
    if (!e) nuevas++;
    else if (e.caja >= CAJA_AFIANZADA) afianzadas++;
    else aprendiendo++;
  }
  return { total: lista.length, nuevas, aprendiendo, afianzadas };
}
