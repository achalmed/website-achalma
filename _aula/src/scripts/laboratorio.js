// src/scripts/laboratorio.js — la página /laboratorio/<id>/ en el navegador: deslizadores, escenarios, «Restablecer»,
// figura y resultados. El cálculo lo hace el trabajador (laboratorio-trabajador.js) con Pyodide; aquí solo se dibuja,
// con el mismo grafico-lab.mjs que pintó la figura inicial en el build. Sin JavaScript o sin red la página conserva esa
// figura (los valores por defecto) y lo dice.
import { graficoSvg, leyendaHtml, anotacionHtml, fmt, fmtParametro, matHtml, textoHtml } from '../lib/grafico-lab.mjs';

const raiz = document.querySelector('[data-lab]');
if (raiz) iniciar(raiz);

function iniciar(raiz) {
  const datos = JSON.parse(raiz.querySelector('script[type="application/json"]').textContent);
  const figura = raiz.querySelector('[data-lab-figura]');
  const leyenda = raiz.querySelector('[data-lab-leyenda]');
  const anotacion = raiz.querySelector('[data-lab-anotacion]');
  const tabla = raiz.querySelector('[data-lab-resultados]');
  const estado = raiz.querySelector('[data-lab-estado]');
  const tiempos = raiz.querySelector('[data-lab-tiempos]');
  const aviso = raiz.querySelector('[data-lab-aviso]');
  const lectura = raiz.querySelector('[data-lab-lectura]');
  const entradas = [...raiz.querySelectorAll('input[type="range"][data-param]')];
  const botones = [...raiz.querySelectorAll('[data-escenario], [data-restablecer]')];
  const defecto = Object.fromEntries(datos.parametros.map((p) => [p.nombre, p.valor]));
  let ultimo = datos.inicial;

  const dibujar = (d) => {
    ultimo = d;
    const ancho = Math.round(figura.clientWidth) || 640;
    figura.innerHTML = graficoSvg(d.curvas, { ancho, xlabel: datos.xlabel, ylabel: datos.ylabel, titulo: datos.titulo, id: 'lab' });
    leyenda.innerHTML = leyendaHtml(d.curvas);
    anotacion.innerHTML = anotacionHtml(d.curvas.anotacion);
    anotacion.hidden = !d.curvas.anotacion;
    if (tabla) tabla.innerHTML = d.resultados.map(([k, v]) => `<tr><th scope="row">${matHtml(k)}</th><td class="dato">${escapar(fmt(v))}</td></tr>`).join('');
  };
  // La figura del build se dibujó a 640 px: aquí se rehace al ancho real (y en cada cambio de tamaño).
  dibujar(ultimo);
  let anchoPrevio = figura.clientWidth;
  new ResizeObserver(() => { if (Math.abs(figura.clientWidth - anchoPrevio) > 4) { anchoPrevio = figura.clientWidth; dibujar(ultimo); } }).observe(figura);

  const valores = () => Object.fromEntries(entradas.map((e) => [e.dataset.param, Number(e.value)]));
  const mostrarValor = (e) => {
    const p = datos.parametros.find((x) => x.nombre === e.dataset.param);
    const texto = fmtParametro(e.value, p.paso, p.unidad);
    raiz.querySelector(`[data-valor="${e.dataset.param}"]`).textContent = texto;
    e.setAttribute('aria-valuetext', texto);
  };

  // ── El trabajador ──────────────────────────────────────────────────────────────────────────────────────────────
  let trabajador = null, listo = false, enCurso = false, pendiente = null, idPedido = 0, tInicio = 0;
  const FASES = { pyodide: 'Cargando Python (Pyodide)…', numpy: 'Cargando numpy…', modelo: 'Cargando el modelo…' };
  const fallar = (motivo) => {
    estado.dataset.estado = 'error';
    estado.textContent = `No se pudo cargar el cálculo en el navegador (${motivo}). La figura muestra el modelo con sus valores por defecto.`;
    trabajador?.terminate();
  };
  const pedir = () => {
    if (!listo) return;
    if (enCurso) { pendiente = true; return; }
    enCurso = true; pendiente = false;
    trabajador.postMessage({ tipo: 'calcular', id: ++idPedido, valores: valores() });
  };
  const arrancar = () => {
    tInicio = performance.now();
    try {
      trabajador = new Worker(new URL('./laboratorio-trabajador.js', import.meta.url));
    } catch (err) { fallar('este navegador no admite trabajadores'); return; }
    const reloj = setTimeout(() => { if (!listo) fallar('tardó demasiado; revisa la conexión'); }, 90000);
    trabajador.onerror = () => { clearTimeout(reloj); fallar('error al cargar Pyodide'); };
    trabajador.onmessage = ({ data: m }) => {
      if (m.tipo === 'avance') estado.textContent = FASES[m.fase] ?? estado.textContent;
      else if (m.tipo === 'listo') {
        clearTimeout(reloj);
        listo = true;
        raiz.dataset.listo = '';
        raiz.dataset.msCarga = String(Math.round(performance.now() - tInicio));
        entradas.forEach((e) => { e.disabled = false; });
        botones.forEach((b) => { b.disabled = false; });
        estado.dataset.estado = 'listo';
        estado.textContent = 'Listo: mueve un parámetro. El cálculo corre en tu navegador con el mismo código Python del laboratorio.';
        pedir();
      } else if (m.tipo === 'resultado') {
        enCurso = false;
        dibujar(m.datos);
        raiz.dataset.msCalculo = String(m.ms);
        tiempos.textContent = `Primera carga ${fmt(Number(raiz.dataset.msCarga) / 1000)} s · último cálculo ${m.ms} ms`;
        if (pendiente) pedir();
      } else if (m.tipo === 'error') {
        enCurso = false;
        if (!listo) { clearTimeout(reloj); fallar(m.mensaje); } else estado.textContent = `El modelo no pudo calcular con estos valores: ${m.mensaje}`;
      }
    };
    trabajador.postMessage({
      tipo: 'iniciar', pyodide: datos.pyodide, base: new URL(datos.base, location.href).href,
      archivos: datos.archivos, disciplina: datos.disciplina, modulo: datos.modulo,
    });
  };

  // ── Controles ──────────────────────────────────────────────────────────────────────────────────────────────────
  entradas.forEach((e) => {
    mostrarValor(e);
    e.addEventListener('input', () => { mostrarValor(e); pedir(); });
  });
  const poner = (cambios, texto) => {
    entradas.forEach((e) => { e.value = String(cambios[e.dataset.param] ?? defecto[e.dataset.param]); mostrarValor(e); });
    pedir();
    if (aviso) aviso.textContent = texto;
  };
  raiz.querySelector('[data-restablecer]')?.addEventListener('click', () => {
    poner({}, 'Parámetros restablecidos a sus valores por defecto.');
    if (lectura) lectura.hidden = true;
    raiz.querySelectorAll('[data-escenario]').forEach((b) => b.setAttribute('aria-pressed', 'false'));
  });
  raiz.querySelectorAll('[data-escenario]').forEach((b) => b.addEventListener('click', () => {
    const esc = datos.escenarios.find((x) => x.nombre === b.dataset.escenario);
    poner(esc.cambios, `Escenario aplicado: ${esc.descripcion}.`);
    raiz.querySelectorAll('[data-escenario]').forEach((o) => o.setAttribute('aria-pressed', String(o === b)));
    if (lectura) {
      lectura.hidden = false;
      lectura.querySelector('[data-lectura-titulo]').innerHTML = textoHtml(esc.descripcion);
      lectura.querySelector('[data-lectura-texto]').innerHTML = textoHtml(esc.lectura);
      lectura.querySelector('[data-lectura-cadena]').innerHTML = (esc.cadena || []).map((c) => `<li>${textoHtml(c)}</li>`).join('');
    }
  }));

  // Pyodide se pide solo en esta página y después de pintarla: no compite con la primera vista.
  // (con plazo: en una pestaña de fondo requestIdleCallback puede no llegar nunca)
  const cuando = (f) => (window.requestIdleCallback ? requestIdleCallback(f, { timeout: 1500 }) : setTimeout(f, 200));
  if (document.readyState === 'complete') cuando(arrancar); else addEventListener('load', () => cuando(arrancar), { once: true });
}

function escapar(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
