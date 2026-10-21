// src/lib/grafico-lab.mjs — el gráfico del laboratorio: dibuja en SVG el contrato de `Modelo.curvas` de simuladores
// (lineas, barras, puntos, equilibrio y anotacion; lo serializa simuladores/navegador.py). El mismo código corre en el
// build (la figura inicial, visible sin JavaScript) y en el navegador (cada recálculo de Pyodide), así que la figura
// estática y la interactiva son idénticas. Sin dependencias: SVG en texto, colores por los tokens de tokens.css.

/** Colores de la paleta del laboratorio (simuladores/<disciplina>/config.py) → roles del aula (tokens.css). */
const COLORES = {
  '#2E5496': 'var(--graf-1)',   // AZUL2: la curva principal
  '#9E2A2B': 'var(--graf-2)',   // ROJO: segunda serie, shocks
  '#3A7D44': 'var(--graf-3)',   // VERDE: tercera serie, población
  '#C9A227': 'var(--graf-eq)',  // DORADO: equilibrio, curva teórica
  '#B0B7C3': 'var(--graf-aux)', // GRIS: líneas auxiliares
  '#1F3864': 'var(--graf-tinta)', // AZUL: títulos y anotaciones
};
const RESPALDO = ['var(--graf-1)', 'var(--graf-2)', 'var(--graf-3)', 'var(--graf-eq)'];
export const color = (hex, i = 0) => COLORES[String(hex).toUpperCase()] ?? RESPALDO[i % RESPALDO.length];
/** Trazo discontinuo para las auxiliares; así la serie se distingue también sin color. */
const trazo = (hex) => (String(hex).toUpperCase() === '#B0B7C3' ? '5 4' : null);

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// ── Matemática de las etiquetas ($…$ al estilo mathtext) ─────────────────────────────────────────────────────────
const SIMBOLOS = {
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε', eta: 'η', theta: 'θ', kappa: 'κ', lambda: 'λ', mu: 'μ',
  nu: 'ν', pi: 'π', rho: 'ρ', sigma: 'σ', tau: 'τ', phi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω', Delta: 'Δ', Gamma: 'Γ',
  Sigma: 'Σ', Pi: 'Π', Phi: 'Φ', Omega: 'Ω', Lambda: 'Λ', Theta: 'Θ', sum: 'Σ', prod: 'Π', cdot: '·', times: '×',
  geq: '≥', leq: '≤', neq: '≠', approx: '≈', infty: '∞', to: '→', rightarrow: '→', leftarrow: '←', pm: '±', sim: '∼',
  partial: '∂', ldots: '…', cdots: '⋯', quad: ' ', qquad: '  ', ',': ' ', ';': ' ', ':': ' ', '!': '', '%': '%',
  '{': '{', '}': '}', '$': '$', '\\': ' ',
};
const ACENTOS = { bar: '̄', hat: '̂', tilde: '̃', dot: '̇', vec: '⃗' };

/** Lee un argumento {…} o un solo carácter desde i; devuelve [texto, siguiente índice]. */
function argumento(s, i) {
  while (s[i] === ' ') i++;
  if (s[i] === '{') {
    let n = 1, j = i + 1;
    while (j < s.length && n > 0) { if (s[j] === '{') n++; else if (s[j] === '}') n--; j++; }
    return [s.slice(i + 1, j - 1), j];
  }
  if (s[i] === '\\') {
    const m = /^\\([A-Za-z]+|.)/.exec(s.slice(i));
    return [m ? m[0] : '', i + (m ? m[0].length : 1)];
  }
  return [s[i] ?? '', i + 1];
}

/** Texto matemático plano (sin sub/superíndices) de un fragmento TeX sencillo. */
function plano(s) {
  return segmentos(s, true).map((x) => x.t).join('');
}

/** Fragmentos [{t, pos: 'n'|'sup'|'sub', mat}] de una cadena con $…$; fuera de $ es texto normal. */
export function segmentos(texto, todoMat = false) {
  const out = [];
  const empuja = (t, pos, mat) => {
    if (!t) return;
    const u = out[out.length - 1];
    if (u && u.pos === pos && u.mat === mat) u.t += t; else out.push({ t, pos, mat });
  };
  const partes = todoMat ? [String(texto)] : String(texto ?? '').split('$');
  partes.forEach((parte, k) => {
    const mat = todoMat || k % 2 === 1;
    if (!mat) { empuja(parte, 'n', false); return; }
    let i = 0;
    while (i < parte.length) {
      const c = parte[i];
      if (c === '\\') {
        const m = /^\\([A-Za-z]+|.)/.exec(parte.slice(i));
        const nombre = m ? m[1] : '';
        i += m ? m[0].length : 1;
        if (ACENTOS[nombre]) { const [a, j] = argumento(parte, i); i = j; empuja(plano(a) + ACENTOS[nombre], 'n', true); }
        else if (nombre === 'frac') { const [a, j] = argumento(parte, i); const [b, k2] = argumento(parte, j); i = k2; empuja(`${plano(a)}/${plano(b)}`, 'n', true); }
        else if (nombre === 'text' || nombre === 'mathrm' || nombre === 'operatorname' || nombre === 'mathbf') { const [a, j] = argumento(parte, i); i = j; empuja(a, 'n', false); }
        else if (nombre === 'sqrt') { const [a, j] = argumento(parte, i); i = j; empuja(`√${plano(a)}`, 'n', true); }
        else if (nombre === 'left' || nombre === 'right' || nombre === 'Big' || nombre === 'big') { /* tamaño: se ignora */ }
        else empuja(SIMBOLOS[nombre] ?? nombre, 'n', true);
      } else if (c === '^' || c === '_') {
        const [a, j] = argumento(parte, i + 1);
        i = j;
        empuja(plano(a), c === '^' ? 'sup' : 'sub', true);
      } else if (c === '{' || c === '}' || c === ' ') i++;   // en modo matemático los espacios no cuentan
      else { empuja(c === ',' ? ', ' : c, 'n', true); i++; }
    }
  });
  return out;
}

/** HTML de una etiqueta con $…$: cursiva para la matemática, <sub>/<sup> para los índices. */
// La barra combinante (U+0304) cae fuera de su letra en varias fuentes de interfaz: en HTML va como sobrerrayado.
const sobrerrayar = (h) => h.replace(/(\p{L})\u0304/gu, '<span style="text-decoration:overline">$1</span>');
/** Texto llano en HTML (sin interpretar $): solo escapa y corrige la barra combinante (X̄). */
export const textoHtml = (s) => sobrerrayar(esc(s ?? ''));

export function matHtml(texto) {
  return segmentos(texto).map(({ t, pos, mat }) => {
    let h = sobrerrayar(esc(t));
    if (mat && /[A-Za-zα-ωΑ-Ω]/.test(t) && pos === 'n') h = `<i>${h}</i>`;
    if (pos === 'sup') h = `<sup>${h}</sup>`;
    if (pos === 'sub') h = `<sub>${h}</sub>`;
    return h;
  }).join('');
}

/** Texto plano (para aria-label y <title>). */
export const matPlano = (texto) => segmentos(texto).map((s) => s.t).join('');

/** <tspan> de SVG de una etiqueta con $…$. */
function matSvg(texto) {
  return segmentos(texto).map(({ t, pos, mat }) => {
    const estilo = mat && pos === 'n' && /[A-Za-zα-ω]/.test(t) ? ' font-style="italic"' : '';
    if (pos === 'n') return `<tspan${estilo}>${esc(t)}</tspan>`;
    const dy = pos === 'sup' ? '-0.45em' : '0.3em';
    const vuelta = pos === 'sup' ? '0.45em' : '-0.3em';
    return `<tspan dy="${dy}" font-size="0.72em">${esc(t)}</tspan><tspan dy="${vuelta}">​</tspan>`;
  }).join('');
}

// ── Números ────────────────────────────────────────────────────────────────────────────────────────────────────
/** Formato del laboratorio (base.fmt) con la convención es-PE: miles con coma, decimales con punto. */
export function fmt(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return '—';
  if (typeof v !== 'number') return String(v);
  const a = Math.abs(v);
  const d = a >= 1000 ? 1 : a >= 10 ? 1 : a >= 1 ? 2 : 3;
  return v.toLocaleString('es-PE', { minimumFractionDigits: d, maximumFractionDigits: d });
}

/** Valor de un parámetro con los decimales de su paso (n = 10, c1 = 0.60, G = 200 u.m.). */
export function fmtParametro(v, paso, unidad = '') {
  const d = Math.max(0, Math.min(4, -Math.floor(Math.log10(paso || 1) + 1e-9)));
  const texto = Number(v).toLocaleString('es-PE', { minimumFractionDigits: d, maximumFractionDigits: d });
  return unidad ? `${texto} ${unidad}` : texto;
}

function marcas(min, max, n = 5) {
  if (!(max > min)) { const d = Math.abs(min) || 1; min -= d / 2; max += d / 2; }
  const bruto = (max - min) / n;
  const pot = 10 ** Math.floor(Math.log10(bruto));
  const paso = [1, 2, 2.5, 5, 10].map((f) => f * pot).find((p) => p >= bruto) ?? 10 * pot;
  const ini = Math.ceil(min / paso - 1e-9) * paso;
  const out = [];
  for (let v = ini; v <= max + paso * 1e-6; v += paso) out.push(Math.abs(v) < paso * 1e-9 ? 0 : v);
  return { marcas: out, paso };
}
function rotulo(v, paso) {
  let dec = 0;                                   // los decimales que el paso necesita (2,5 → 1; 0,25 → 2)
  while (dec < 6 && Math.abs(Math.round(paso * 10 ** dec) - paso * 10 ** dec) > 1e-6 * 10 ** dec) dec++;
  const a = Math.abs(v);
  if (a >= 1e6) return v.toExponential(1).replace('e+', 'e');
  return v.toLocaleString('es-PE', { minimumFractionDigits: dec, maximumFractionDigits: dec });
}

/** Símbolo del eje para el equilibrio: «Producto ($Y$)» → «Y*» (como graficos._simbolo de simuladores). */
function simbolo(etiqueta) {
  const m = /\(([^()]*)\)/.exec(etiqueta || '');
  if (!m) return '';
  const s = m[1].trim().replace(/^\$|\$$/g, '');
  if (s.length > 0 && s.length <= 3 && s !== '%' && !s.includes('^') && !s.includes('*')) return `${plano(s)}*`;
  return '';
}

/** Rango [min, max] de los datos de un eje, sin nulos ni infinitos. */
function rango(valores) {
  let lo = Infinity, hi = -Infinity;
  for (const v of valores) if (typeof v === 'number' && Number.isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; }
  return lo === Infinity ? [0, 1] : [lo, hi];
}

/**
 * SVG de las curvas de un modelo.
 * @param {object} curvas  `curvas` de navegador.calcular (lineas, barras, puntos, equilibrio, anotacion)
 * @param {object} op      { ancho, alto, xlabel, ylabel, titulo, descripcion, id }
 */
export function graficoSvg(curvas, op = {}) {
  const ancho = Math.max(280, Math.round(op.ancho ?? 640));
  const alto = Math.round(op.alto ?? Math.max(260, Math.min(420, ancho * 0.62)));
  const estrecho = ancho < 460;
  const m = { izq: estrecho ? 46 : 58, der: 22, arr: 14, aba: op.xlabel ? 46 : 30 };   // a la derecha cabe el último rótulo
  const W = ancho - m.izq - m.der, H = alto - m.arr - m.aba;
  const id = op.id ?? 'g';
  const lineas = curvas.lineas ?? [];
  const barras = curvas.barras ?? null;
  const puntos = curvas.puntos ?? [];
  const eq = curvas.equilibrio ?? null;

  let xs = [], ys = [];
  for (const l of lineas) { xs.push(...l.x); ys.push(...l.y); }
  for (const p of puntos) { xs.push(p.x); ys.push(p.y); }
  if (eq) { xs.push(eq.x); ys.push(eq.y); }
  let xmin, xmax;
  if (barras) {
    xmin = -0.5; xmax = barras.categorias.length - 0.5;
    ys.push(...barras.valores, 0);
  } else [xmin, xmax] = rango(xs);
  let [ymin, ymax] = rango(ys);
  if (!(xmax > xmin)) { xmin -= 0.5; xmax += 0.5; }
  if (!(ymax > ymin)) { const d = Math.abs(ymin) || 1; ymin -= d * 0.1; ymax += d * 0.1; }
  const py = (ymax - ymin) * 0.06;
  ymin -= barras && ymin >= 0 ? 0 : py; ymax += py;
  if (barras && ymin > 0) ymin = 0;
  const X = (v) => m.izq + ((v - xmin) / (xmax - xmin)) * W;
  const Y = (v) => m.arr + (1 - (v - ymin) / (ymax - ymin)) * H;
  const r = (v) => Math.round(v * 10) / 10;

  const partes = [];
  partes.push(`<svg class="grafico-lab" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${ancho} ${alto}" width="${ancho}" height="${alto}" role="img" aria-labelledby="${id}-t ${id}-d">`);
  partes.push(`<title id="${id}-t">${esc(matPlano(op.titulo ?? 'Gráfico del modelo'))}</title>`);
  partes.push(`<desc id="${id}-d">${esc(op.descripcion ?? describir(curvas, op))}</desc>`);
  partes.push(`<defs><clipPath id="${id}-c"><rect x="${m.izq}" y="${m.arr}" width="${W}" height="${H}"/></clipPath></defs>`);

  // Retícula y ejes
  const ty = marcas(ymin, ymax, Math.max(3, Math.round(H / 60)));
  partes.push('<g class="g-reticula">');
  for (const v of ty.marcas) partes.push(`<line x1="${m.izq}" x2="${m.izq + W}" y1="${r(Y(v))}" y2="${r(Y(v))}"/>`);
  let tx = null;
  if (!barras) {
    tx = marcas(xmin, xmax, Math.max(3, Math.round(W / (estrecho ? 70 : 90))));
    for (const v of tx.marcas) partes.push(`<line y1="${m.arr}" y2="${m.arr + H}" x1="${r(X(v))}" x2="${r(X(v))}"/>`);
  }
  partes.push('</g>');
  if (ymin < 0 && ymax > 0) partes.push(`<line class="g-cero" x1="${m.izq}" x2="${m.izq + W}" y1="${r(Y(0))}" y2="${r(Y(0))}"/>`);
  partes.push(`<g class="g-ejes"><line x1="${m.izq}" x2="${m.izq + W}" y1="${m.arr + H}" y2="${m.arr + H}"/><line x1="${m.izq}" x2="${m.izq}" y1="${m.arr}" y2="${m.arr + H}"/></g>`);
  partes.push('<g class="g-rotulos">');
  for (const v of ty.marcas) partes.push(`<text x="${m.izq - 6}" y="${r(Y(v))}" text-anchor="end" dominant-baseline="middle">${esc(rotulo(v, ty.paso))}</text>`);
  if (tx) for (const v of tx.marcas) partes.push(`<text x="${r(X(v))}" y="${m.arr + H + 16}" text-anchor="middle">${esc(rotulo(v, tx.paso))}</text>`);
  if (barras) {
    const paso = Math.max(1, Math.ceil((barras.categorias.length * (estrecho ? 46 : 64)) / W));
    barras.categorias.forEach((c, i) => {
      if (i % paso) return;
      const t = matPlano(c);
      partes.push(`<text x="${r(X(i))}" y="${m.arr + H + 16}" text-anchor="middle">${esc(t.length > 14 ? t.slice(0, 13) + '…' : t)}</text>`);
    });
  }
  partes.push('</g>');
  if (op.xlabel) partes.push(`<text class="g-eje-titulo" x="${m.izq + W / 2}" y="${alto - 8}" text-anchor="middle">${matSvg(op.xlabel)}</text>`);
  if (op.ylabel) partes.push(`<text class="g-eje-titulo" transform="translate(12 ${m.arr + H / 2}) rotate(-90)" text-anchor="middle">${matSvg(op.ylabel)}</text>`);

  // Datos
  partes.push(`<g clip-path="url(#${id}-c)">`);
  if (barras) {
    const bw = (W / barras.categorias.length) * 0.62;
    barras.valores.forEach((v, i) => {
      if (typeof v !== 'number') return;
      const y0 = Y(Math.max(0, Math.min(v, ymax))), y1 = Y(Math.min(0, Math.max(v, ymin)));
      partes.push(`<rect class="g-barra" x="${r(X(i) - bw / 2)}" y="${r(y0)}" width="${r(bw)}" height="${r(Math.max(0.5, y1 - y0))}" style="fill:${color(barras.colores[i], i)}"/>`);
    });
  }
  lineas.forEach((l, i) => {
    let d = '', abierto = false;
    const n = l.x.length;
    const paso = Math.max(1, Math.floor(n / (W * 1.5)));   // a lo sumo ~1,5 puntos por píxel; el último siempre
    for (let k = 0; k < n; k = k + paso < n || k === n - 1 ? k + paso : n - 1) {
      const x = l.x[k], y = l.y[k];
      if (typeof x !== 'number' || typeof y !== 'number') { abierto = false; continue; }
      d += `${abierto ? 'L' : 'M'}${r(X(x))} ${r(Y(y))}`;
      abierto = true;
    }
    const dash = trazo(l.color);
    partes.push(`<path class="g-linea" d="${d}" style="stroke:${color(l.color, i)}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`);
  });
  partes.push('</g>');

  // Puntos y equilibrio, con su rótulo dentro del área
  const ponerRotulo = (x, y, texto) => {
    const derecha = X(x) > m.izq + W * 0.62;
    const yy = Math.max(m.arr + 12, Math.min(m.arr + H - 6, Y(y) - 9));
    const xx = derecha ? X(x) - 8 : X(x) + 8;
    return `<text class="g-punto-rotulo" x="${r(xx)}" y="${r(yy)}" text-anchor="${derecha ? 'end' : 'start'}">${matSvg(texto)}</text>`;
  };
  for (const p of puntos) {
    if (typeof p.x !== 'number' || typeof p.y !== 'number') continue;
    partes.push(`<circle class="g-punto" cx="${r(X(p.x))}" cy="${r(Y(p.y))}" r="4"/>`);
    if (p.etiqueta) partes.push(ponerRotulo(p.x, p.y, p.etiqueta));
  }
  if (eq && typeof eq.x === 'number' && typeof eq.y === 'number') {
    partes.push(`<circle class="g-equilibrio" cx="${r(X(eq.x))}" cy="${r(Y(eq.y))}" r="5.5"/>`);
    const sx = simbolo(op.xlabel), sy = simbolo(op.ylabel);
    partes.push(ponerRotulo(eq.x, eq.y, `(${sx ? sx + ' = ' : ''}${fmt(eq.x)}, ${sy ? sy + ' = ' : ''}${fmt(eq.y)})`));
  }
  partes.push('</svg>');
  return partes.join('');
}

/** Descripción textual del gráfico (para lectores de pantalla). */
export function describir(curvas, op = {}) {
  const t = [];
  const series = (curvas.lineas ?? []).map((l) => matPlano(l.etiqueta));
  if (series.length) t.push(`Curvas: ${series.join('; ')}.`);
  if (curvas.barras) t.push(`Barras: ${curvas.barras.categorias.map((c, i) => `${matPlano(c)} ${fmt(curvas.barras.valores[i])}`).join('; ')}.`);
  if (curvas.equilibrio) {
    const sx = simbolo(op.xlabel) || 'x', sy = simbolo(op.ylabel) || 'y';
    t.push(`Equilibrio en ${sx} = ${fmt(curvas.equilibrio.x)}, ${sy} = ${fmt(curvas.equilibrio.y)}.`);
  }
  for (const p of curvas.puntos ?? []) if (p.etiqueta) t.push(`${matPlano(p.etiqueta)}.`);
  if (op.xlabel || op.ylabel) t.push(`Eje horizontal: ${matPlano(op.xlabel || '—')}; eje vertical: ${matPlano(op.ylabel || '—')}.`);
  return t.join(' ');
}

/** Leyenda en HTML (debajo de la figura: se acomoda a 375 px). */
export function leyendaHtml(curvas) {
  const items = (curvas.lineas ?? []).map((l, i) => {
    const dash = trazo(l.color);
    return `<li><svg aria-hidden="true" width="22" height="10" viewBox="0 0 22 10"><line x1="1" x2="21" y1="5" y2="5" style="stroke:${color(l.color, i)}"${dash ? ` stroke-dasharray="${dash}"` : ''}/></svg><span>${matHtml(l.etiqueta)}</span></li>`;
  });
  if (curvas.equilibrio) items.push('<li><svg aria-hidden="true" width="22" height="10" viewBox="0 0 22 10"><circle class="g-equilibrio" cx="11" cy="5" r="4"/></svg><span>equilibrio</span></li>');
  return items.join('');
}

/** La anotación del modelo (texto con saltos de línea y $…$) en HTML. */
export const anotacionHtml = (texto) => (texto ? String(texto).split('\n').map(matHtml).join('<br>') : '');
