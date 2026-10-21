// src/scripts/laboratorio-trabajador.js — el trabajador (Web Worker) del laboratorio: carga Pyodide y numpy desde
// jsDelivr, escribe en su sistema de archivos los .py mínimos del modelo (los lista simuladores/navegador.json; el build
// los copia a /laboratorio/py/) e importa el MISMO `MODELO` que usa el escritorio. Corre fuera del hilo principal para
// que la página no se congele mientras Python arranca (decisiones §1.20).
//
// Mensajes: entra {tipo:'iniciar', pyodide, base, archivos, disciplina, modulo} y {tipo:'calcular', id, valores};
// sale {tipo:'avance', fase}, {tipo:'listo', ms}, {tipo:'resultado', id, datos, ms} o {tipo:'error', mensaje}.

let calcular = null;

async function iniciar({ pyodide: urlPyodide, base, archivos, disciplina, modulo }) {
  const t0 = performance.now();
  self.postMessage({ tipo: 'avance', fase: 'pyodide' });
  importScripts(`${urlPyodide}pyodide.js`);
  // stdout/stderr y los avisos de carga de paquetes no van a la consola: la página informa por su cuenta.
  const silencio = () => {};
  const py = await self.loadPyodide({ indexURL: urlPyodide, stdout: silencio, stderr: silencio });
  self.postMessage({ tipo: 'avance', fase: 'numpy' });
  await py.loadPackage('numpy', { messageCallback: silencio, errorCallback: silencio });
  self.postMessage({ tipo: 'avance', fase: 'modelo' });
  const textos = await Promise.all(archivos.map(async (a) => {
    const r = await fetch(new URL(a, base));
    if (!r.ok) throw new Error(`no se pudo leer ${a} (${r.status})`);
    return [a, await r.text()];
  }));
  for (const [a, texto] of textos) {
    const ruta = `/lab/${a}`;
    py.FS.mkdirTree(ruta.slice(0, ruta.lastIndexOf('/')));
    py.FS.writeFile(ruta, texto);
  }
  py.globals.set('_disciplina', disciplina);
  py.globals.set('_modulo', modulo);
  py.runPython(`
import importlib, sys
sys.path[:0] = ['/lab/' + _disciplina, '/lab']
import navegador
navegador.preparar()
_MODELO = importlib.import_module(_modulo).MODELO
_calcular = lambda s: navegador.calcular_json(_MODELO, s)
`);
  calcular = py.globals.get('_calcular');
  self.postMessage({ tipo: 'listo', ms: Math.round(performance.now() - t0) });
}

self.onmessage = async (e) => {
  const m = e.data;
  try {
    if (m.tipo === 'iniciar') await iniciar(m);
    else if (m.tipo === 'calcular' && calcular) {
      const t0 = performance.now();
      const datos = JSON.parse(calcular(JSON.stringify(m.valores ?? {})));
      self.postMessage({ tipo: 'resultado', id: m.id, datos, ms: Math.round(performance.now() - t0) });
    }
  } catch (err) {
    self.postMessage({ tipo: 'error', mensaje: String(err?.message ?? err).split('\n').slice(-3).join(' ') });
  }
};
