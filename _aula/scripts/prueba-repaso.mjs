#!/usr/bin/env node
// scripts/prueba-repaso.mjs — pruebas de la autoevaluación y del repaso espaciado (decisiones §1.24 y §1.25):
//   - src/lib/quiz.mjs: la corrección y la retroalimentación por distractor (`retro`);
//   - src/lib/espaciado.mjs: el calendario (cajas, intervalos, vuelta de hoy, intercalado, estado guardado roto);
//   - src/lib/alineamiento.mjs: la vitrina deja fuera lo que propuso la IA sin verificar, y las preguntas del repaso
//     salen del exportador de docencia (`alineamiento.py exportar --formato quiz`), con un curso de muestra en una
//     carpeta temporal y, si está, con el banco real de econometria-i.
//   node --test scripts/prueba-repaso.mjs        (sale 1 si algo falla)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import { dump, load } from 'js-yaml';
import { corregir, retroDe, textoCorrecto, valida, numero } from '../src/lib/quiz.mjs';
import * as E from '../src/lib/espaciado.mjs';
import { aprendizajeDelCurso, publicable } from '../src/lib/alineamiento.mjs';
import { RUTAS } from '../src/lib/rutas.mjs';

// ── quiz.mjs ─────────────────────────────────────────────────────────────────────────────────────────
const opcion = {
  tipo: 'opcion', enunciado: '¿?', opciones: ['a', 'b', 'c'], correcta: 1,
  retro: ['confunde a con b', null, '  '],
};

test('corrige opción, verdadero o falso y numérica (coma o punto, tolerancia)', () => {
  assert.equal(corregir(opcion, '1').estado, 'bien');
  assert.equal(corregir(opcion, '0').estado, 'mal');
  assert.equal(corregir({ tipo: 'vf', enunciado: 'x', respuesta: false }, 'false').estado, 'bien');
  assert.equal(corregir({ tipo: 'vf', enunciado: 'x', respuesta: false }, 'true').estado, 'mal');
  const num = { tipo: 'numerica', enunciado: 'x', respuesta: 4.5, tolerancia: 0.1 };
  assert.equal(corregir(num, '4,55').estado, 'bien');
  assert.equal(corregir(num, ' 4.6 ').estado, 'bien');
  assert.equal(corregir(num, '4,7').estado, 'mal');
  assert.equal(corregir(num, 'cuatro').estado, 'no-numero');
  assert.equal(corregir(num, '').estado, 'vacia');
  assert.equal(corregir({ tipo: 'numerica', enunciado: 'x', respuesta: 3 }, '3').estado, 'bien', 'sin tolerancia es exacta');
  assert.ok(Number.isNaN(numero('')));
});

test('la retroalimentación sale solo al elegir un distractor que la trae', () => {
  assert.equal(corregir(opcion, '0').retro, 'confunde a con b');
  assert.equal(corregir(opcion, '1').retro, null, 'la correcta no lleva retro');
  assert.equal(corregir(opcion, '2').retro, null, 'retro vacía = sin retro');
  assert.equal(retroDe({ ...opcion, retro: undefined }, 0), null, 'pregunta sin retro');
  assert.equal(retroDe({ ...opcion, retro: ['x'] }, 2), null, 'retro más corta que las opciones');
  assert.equal(retroDe({ ...opcion, retro: ['x', 'no debería', null] }, 1), null, 'aunque la escriban, la correcta no muestra retro');
  assert.equal(textoCorrecto(opcion), 'b');
  assert.equal(textoCorrecto({ tipo: 'numerica', respuesta: 4.5, unidad: 'pp' }), '4.5 pp');
});

test('valida descarta lo que no se puede corregir solo', () => {
  assert.ok(valida(opcion));
  assert.ok(!valida({ ...opcion, correcta: 3 }));
  assert.ok(!valida({ ...opcion, opciones: ['solo una'], correcta: 0 }));
  assert.ok(!valida({ tipo: 'vf', enunciado: 'x', respuesta: 'sí' }));
  assert.ok(!valida({ tipo: 'abierta', enunciado: 'x', respuesta: 'texto' }));
  assert.ok(valida({ tipo: 'numerica', enunciado: 'x', respuesta: 0 }));
});

// ── espaciado.mjs ────────────────────────────────────────────────────────────────────────────────────
const P = [
  { id: 'a1', sesion: 's01' }, { id: 'a2', sesion: 's01' }, { id: 'a3', sesion: 's01' },
  { id: 'b1', sesion: 's02' }, { id: 'c1', sesion: 's03' }, { id: 'c2', sesion: 's03' },
];

test('fechas locales y aritmética de calendario', () => {
  assert.equal(E.fechaLocal(new Date(2026, 10, 23, 23, 30)), '2026-11-23', 'de noche sigue siendo hoy');
  assert.equal(E.sumarDias('2026-11-23', 8), '2026-12-01');
  assert.equal(E.sumarDias('2026-12-31', 1), '2027-01-01');
  assert.equal(E.diasEntre('2026-11-23', '2026-12-23'), 30);
});

test('cada acierto seguido aleja la pregunta 1, 3, 7, 14 y 30 días; un fallo la trae hoy', () => {
  const e = E.normalizar(null);
  let hoy = '2026-11-24';
  const vistos = [];
  for (let i = 0; i < 6; i++) {
    const x = E.registrar(e, 'a1', true, hoy);
    vistos.push(E.diasEntre(hoy, x.proxima));
    hoy = x.proxima;
  }
  assert.deepEqual(vistos, [1, 3, 7, 14, 30, 30], 'el techo es 30 días');
  const f = E.registrar(e, 'a1', false, hoy);
  assert.deepEqual([f.caja, f.proxima], [0, hoy], 'el fallo vuelve hoy, a la caja 0');
  const r = E.registrar(e, 'a1', true, hoy);
  assert.equal(r.proxima, E.sumarDias(hoy, 1), 'acertada tras fallar: mañana');
  assert.deepEqual([r.aciertos, r.fallos], [7, 1]);
});

test('la vuelta de hoy: vencidas primero (la más atrasada antes), luego nuevas con tope, intercaladas', () => {
  const e = E.normalizar(null);
  E.registrar(e, 'c1', true, '2026-11-20');   // vence el 21
  E.registrar(e, 'a2', true, '2026-11-22');   // vence el 23
  E.registrar(e, 'b1', true, '2026-11-24');   // vence el 25: hoy no
  const v = E.vueltaDeHoy(e, P, '2026-11-24', { maxNuevas: 2 });
  assert.deepEqual(v.vencidas.map((p) => p.id), ['c1', 'a2']);
  assert.deepEqual(v.nuevas.map((p) => p.id), ['a1', 'a3'], 'el tope respeta el orden del curso');
  assert.equal(v.nuevasRestantes, 1);
  const todo = E.vueltaDeHoy(E.normalizar(null), P, '2026-11-24');
  assert.deepEqual(todo.nuevas.map((p) => p.id), ['a1', 'b1', 'c1', 'a2', 'c2', 'a3'], 'alterna las sesiones');
});

test('las sesiones elegidas filtran la vuelta, el calendario y el resumen', () => {
  const e = E.normalizar(null);
  e.sesiones = ['s02'];
  assert.deepEqual(E.vueltaDeHoy(e, P, '2026-11-24').nuevas.map((p) => p.id), ['b1']);
  E.registrar(e, 'b1', true, '2026-11-24');
  E.registrar(e, 'a1', true, '2026-11-24');   // de una sesión que no se repasa: no cuenta
  assert.deepEqual(E.calendario(e, P, '2026-11-24').filas, [{ fecha: '2026-11-25', n: 1, en: 1 }]);
  assert.deepEqual(E.resumen(e, P), { total: 1, nuevas: 0, aprendiendo: 1, afianzadas: 0 });
});

test('el calendario separa los próximos días de lo que vuelve más adelante', () => {
  const e = E.normalizar(null);
  for (let i = 0; i < 5; i++) E.registrar(e, 'a1', true, '2026-11-24');   // caja 5: a 30 días
  E.registrar(e, 'a2', true, '2026-11-24');
  E.registrar(e, 'a3', true, '2026-11-24');
  const c = E.calendario(e, P, '2026-11-24', 14);
  assert.deepEqual(c.filas, [{ fecha: '2026-11-25', n: 2, en: 1 }]);
  assert.equal(c.despues, 1);
  assert.equal(E.resumen(e, P).afianzadas, 1);
});

test('un estado guardado roto o de otra versión no rompe la página', () => {
  assert.deepEqual(E.normalizar('basura'), { v: 1, preguntas: {}, sesiones: null });
  assert.deepEqual(E.normalizar({ v: 99, preguntas: { a1: { caja: 1, proxima: '2026-11-24' } } }).preguntas, {});
  const e = E.normalizar({ v: 1, preguntas: { a1: { caja: 99, proxima: '2026-11-24' }, a2: { caja: 1, proxima: 'mañana' }, a3: null }, sesiones: ['s01', 3] });
  assert.deepEqual(Object.keys(e.preguntas), ['a1']);
  assert.equal(e.preguntas.a1.caja, E.INTERVALOS.length);
  assert.deepEqual(e.sesiones, ['s01']);
});

// ── alineamiento.mjs con un curso de muestra (y el exportador de verdad) ─────────────────────────────
const python = process.env.PYTHON || 'python3';
const hayExportador = existsSync(RUTAS.alineamiento) && (() => {
  try { execFileSync(python, ['-c', 'import yaml'], { stdio: 'ignore' }); return true; } catch { return false; }
})();

function cursoDeMuestra() {
  const dir = mkdtempSync(join(tmpdir(), 'aula-repaso-'));
  writeFileSync(join(dir, 'curso.yml'), dump({ id: 'curso-muestra', titulo: 'Curso de muestra' }));
  const ses = join(dir, '03-sesiones', 's01-una-sesion');
  mkdirSync(ses, { recursive: true });
  writeFileSync(join(ses, 'sesion.yml'), dump({ titulo: 'Una sesión', resultados_aprendizaje: ['ra1'] }));
  const preguntas = [
    { id: 's01-p01', resultado: 'ra1', tipo: 'opcion', enunciado: '¿Cuál?', opciones: ['uno', 'dos', 'tres'], respuesta: 'dos',
      errores: [{ opcion: 'uno', error: 'Confunde el primero con el segundo' }], explicacion: 'Porque sí' },
    { id: 's01-p02', resultado: 'ra1', tipo: 'vf', enunciado: '¿Verdad?', respuesta: true,
      origen: { autor: 'llm', herramienta: 'chat', fecha: '2026-11-23', verificacion: 'pendiente' } },
    { id: 's01-p03', resultado: 'ra1', tipo: 'vf', enunciado: '¿Cierto?', respuesta: false,
      origen: { autor: 'llm', herramienta: 'chat', fecha: '2026-11-23', verificacion: 'verificada' } },
    { id: 's01-p04', resultado: 'ra1', tipo: 'abierta', enunciado: '¿Por qué?', respuesta: 'Texto de la puesta en común' },
    { id: 's01-p05', resultado: 'ra1', tipo: 'numerica', enunciado: '¿Cuánto?', respuesta: 'unos 4,5', valor: 4.5, tolerancia: 0.1 },
    { id: 's01-p06', resultado: 'ra1', tipo: 'abierta', enunciado: '¿Sin verificar?', respuesta: 'x',
      origen: { autor: 'llm', herramienta: 'chat', fecha: '2026-11-23' } },
  ];
  writeFileSync(join(ses, 'recuperacion.yml'), dump({ sesion: 's01-una-sesion', fuente: 'Muestra', preguntas }));
  return dir;
}

test('publicable: lo de la IA solo sale verificado (como alineamiento.py)', () => {
  assert.ok(publicable({}));
  assert.ok(publicable({ origen: { autor: 'persona' } }));
  assert.ok(publicable({ origen: { autor: 'llm', verificacion: 'verificada' } }));
  assert.ok(!publicable({ origen: { autor: 'llm', verificacion: 'pendiente' } }));
  assert.ok(!publicable({ origen: { autor: 'llm' } }), 'sin verificacion = pendiente');
});

test('la vitrina del banco deja fuera lo que propuso la IA sin verificar y no lleva claves', { skip: !hayExportador && 'sin python3 con PyYAML o sin docencia' }, () => {
  const dir = cursoDeMuestra();
  try {
    const avisos = [];
    const ap = aprendizajeDelCurso({ id: 'curso-muestra', _dir: dir }, avisos);
    const ids = ap.repaso[0].preguntas.map((p) => p.id);
    assert.deepEqual(ids, ['s01-p01', 's01-p03', 's01-p04', 's01-p05']);
    for (const p of ap.repaso[0].preguntas) {
      assert.deepEqual(Object.keys(p).filter((k) => ['respuesta', 'explicacion', 'errores', 'valor', 'origen'].includes(k)), [], `sin claves: ${p.id}`);
    }
    // El repaso: solo las cerradas publicables, del exportador, con su clave y la retro del distractor.
    assert.deepEqual(avisos, []);
    const rep = ap.repasar;
    assert.deepEqual(rep.preguntas.map((p) => p.id), ['s01-p01', 's01-p03', 's01-p05']);
    assert.deepEqual(rep.sesiones, [{ numero: 's01', titulo: 'Una sesión', n: 3 }]);
    assert.equal(rep.url, '/cursos/curso-muestra/repasar/');
    const [op, vf, num] = rep.preguntas;
    assert.equal(op.correcta, 1);
    assert.deepEqual(op.retro, ['Confunde el primero con el segundo', null, null]);
    assert.equal(corregir(op, '0').retro, 'Confunde el primero con el segundo');
    assert.equal(vf.respuesta, false);
    assert.equal(corregir(num, '4,45').estado, 'bien');
    assert.ok(rep.preguntas.every((p) => p.sesion === 's01' && valida(p)));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('un banco solo de abiertas no da página de repaso', { skip: !hayExportador && 'sin python3 con PyYAML o sin docencia' }, () => {
  const dir = cursoDeMuestra();
  try {
    const ruta = join(dir, '03-sesiones', 's01-una-sesion', 'recuperacion.yml');
    writeFileSync(ruta, dump({ sesion: 's01-una-sesion', preguntas: [{ id: 's01-p01', resultado: 'ra1', tipo: 'abierta', enunciado: '¿Por qué?', respuesta: 'x' }] }));
    const avisos = [];
    const ap = aprendizajeDelCurso({ id: 'curso-muestra', _dir: dir }, avisos);
    assert.equal(ap.repaso.length, 1);
    assert.equal(ap.repasar, null);
    assert.deepEqual(avisos, []);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('si el exportador falla, la página no se genera y queda un aviso', { skip: !hayExportador && 'sin python3 con PyYAML o sin docencia' }, () => {
  const dir = cursoDeMuestra();
  const antes = process.env.PYTHON;
  process.env.PYTHON = join(dir, 'no-existe-python');
  try {
    const avisos = [];
    const ap = aprendizajeDelCurso({ id: 'curso-muestra', _dir: dir }, avisos);
    assert.equal(ap.repasar, null);
    assert.equal(avisos.length, 1);
    assert.match(avisos[0], /sin página de repaso/);
    assert.equal(ap.repaso.length, 1, 'el banco sin claves se sigue mostrando');
  } finally {
    if (antes === undefined) delete process.env.PYTHON; else process.env.PYTHON = antes;
    rmSync(dir, { recursive: true, force: true });
  }
});

test('econometria-i: el repaso trae las mismas preguntas que el exportador del curso entero', { skip: (!hayExportador || !existsSync(join(RUTAS.cursos, 'econometria-i', 'curso.yml'))) && 'sin el banco de econometria-i' }, () => {
  const dir = join(RUTAS.cursos, 'econometria-i');
  const avisos = [];
  const ap = aprendizajeDelCurso({ id: 'econometria-i', _dir: dir }, avisos);
  const todo = load(execFileSync(python, [RUTAS.alineamiento, 'exportar', dir, '--formato', 'quiz'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] })).quiz;
  assert.deepEqual(ap.repasar.preguntas.map(({ sesion, ...q }) => q), todo, 'sesión por sesión = el curso entero');
  assert.ok(ap.repasar.preguntas.every(valida));
  assert.deepEqual(avisos.filter((a) => /repaso|exportador/.test(a)), []);
  const vitrina = new Set(ap.repaso.flatMap((r) => r.preguntas.map((p) => p.id)));
  assert.ok(ap.repasar.preguntas.every((p) => vitrina.has(p.id)), 'todo lo que se repasa está en la vitrina del banco');
});
