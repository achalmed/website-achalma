#!/usr/bin/env node
// scripts/prueba-videos.mjs — prueba de src/lib/videos.mjs con los datos de muestra de src/demo/videos-ejemplo.json y con
// el catálogo real de divulgacion (hoy sin publicaciones: ninguna lección debe mostrar vídeos). Sale 1 si algo falla.
//   node scripts/prueba-videos.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { idYoutube, publicacion, videosDelTema } from '../src/lib/videos.mjs';
import { RUTAS } from '../src/lib/rutas.mjs';

const ejemplo = JSON.parse(readFileSync(new URL('../src/demo/videos-ejemplo.json', import.meta.url), 'utf8'));

test('reconoce las formas de url de YouTube', () => {
  for (const u of ['https://www.youtube.com/watch?v=aqz-KE-bpKQ', 'https://youtu.be/aqz-KE-bpKQ', 'https://youtube.com/shorts/aqz-KE-bpKQ', 'https://m.youtube.com/watch?v=aqz-KE-bpKQ&t=3']) {
    assert.equal(idYoutube(u), 'aqz-KE-bpKQ', u);
  }
  assert.equal(idYoutube('https://www.tiktok.com/@x/video/1'), null);
  assert.equal(idYoutube('no es url'), null);
});

test('YouTube se incrusta con youtube-nocookie; lo demás es enlace', () => {
  assert.equal(publicacion({ red: 'youtube', url: 'https://youtu.be/aqz-KE-bpKQ' }).incrustar, 'https://www.youtube-nocookie.com/embed/aqz-KE-bpKQ?rel=0');
  assert.equal(publicacion({ red: 'tiktok', url: 'https://www.tiktok.com/@x/video/1' }).incrustar, null);
  assert.equal(publicacion({ red: 'youtube', url: '' }), null);
  assert.equal(publicacion({ red: 'youtube', url: 'http://youtu.be/aqz-KE-bpKQ' }), null, 'solo https');
});

test('una pieza aparece solo si tiene publicación con url, y YouTube va primero', () => {
  const v = videosDelTema(ejemplo.piezas, 'curso-ejemplo', '1.1');
  assert.deepEqual(v.map((x) => x.id), ['eco-900-ejemplo-youtube', 'dat-901-ejemplo-facebook']);
  assert.equal(v[0].principal.red, 'youtube');
  assert.deepEqual(v[0].otras.map((o) => o.nombreRed), ['TikTok']);
  assert.equal(v[1].principal.incrustar, null);
  assert.deepEqual(videosDelTema(ejemplo.piezas, 'curso-ejemplo', '9.9'), []);
  assert.deepEqual(videosDelTema(ejemplo.piezas, 'otro-curso', '1.1'), []);
});

test('el catálogo real de divulgacion no muestra vídeos mientras no haya publicaciones', { skip: !existsSync(RUTAS.catalogoDivulgacion) }, () => {
  const piezas = JSON.parse(readFileSync(RUTAS.catalogoDivulgacion, 'utf8')).piezas;
  const publicadas = piezas.filter((p) => (p.publicaciones ?? []).some((x) => x.url));
  for (const p of piezas) for (const c of p.curriculo ?? []) {
    const v = videosDelTema(piezas, c.curso, c.tema);
    assert.equal(v.length, publicadas.filter((q) => (q.curriculo ?? []).some((d) => d.curso === c.curso && String(d.tema) === String(c.tema))).length);
  }
});
