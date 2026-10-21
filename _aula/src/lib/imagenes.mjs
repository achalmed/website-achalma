// src/lib/imagenes.mjs — la imagen de la tarjeta de una lección o un artículo (docs/decisiones.md §1.17).
//
// Orden: 1) la imagen propia del post (`image:` de su frontmatter), si no es la misma que comparten otros posts del pub
// (la foto genérica de la serie no distingue a nadie); 2) la primera figura del cuerpo con tamaño y proporción de
// tarjeta; 3) ninguna: la tarjeta muestra el índice del texto. La miniatura (640 × 400, WebP) la escribe
// la integración de recursos al terminar el build; aquí solo se elige y se mide, sin dependencias.

import { createHash } from 'node:crypto';
import { closeSync, openSync, readFileSync, readSync } from 'node:fs';
import { isAbsolute, join, resolve } from 'node:path';
import { esArchivo } from './fuentes.mjs';

export const MINIATURA = { ancho: 640, alto: 400 };
const RASTER = /\.(jpe?g|png|webp|gif)$/i;

/** Ancho y alto de un PNG, JPEG, GIF o WebP leyendo solo su cabecera (null si no se reconoce). */
export function dimensiones(ruta) {
  let fd;
  try {
    fd = openSync(ruta, 'r');
    const b = Buffer.alloc(64 * 1024);
    const n = readSync(fd, b, 0, b.length, 0);
    if (b.readUInt32BE(0) === 0x89504e47) return { ancho: b.readUInt32BE(16), alto: b.readUInt32BE(20) };
    if (b.toString('ascii', 0, 3) === 'GIF') return { ancho: b.readUInt16LE(6), alto: b.readUInt16LE(8) };
    if (b.toString('ascii', 0, 4) === 'RIFF' && b.toString('ascii', 8, 12) === 'WEBP') {
      const tipo = b.toString('ascii', 12, 16);
      if (tipo === 'VP8X') return { ancho: 1 + b.readUIntLE(24, 3), alto: 1 + b.readUIntLE(27, 3) };
      if (tipo === 'VP8 ') return { ancho: b.readUInt16LE(26) & 0x3fff, alto: b.readUInt16LE(28) & 0x3fff };
      if (tipo === 'VP8L') { const v = b.readUInt32LE(21); return { ancho: 1 + (v & 0x3fff), alto: 1 + ((v >> 14) & 0x3fff) }; }
      return null;
    }
    if (b[0] === 0xff && b[1] === 0xd8) {
      // JPEG: se recorren los segmentos hasta el primer SOF (C0–CF salvo C4, C8 y CC).
      let i = 2;
      while (i + 9 < n) {
        if (b[i] !== 0xff) { i++; continue; }
        const m = b[i + 1];
        if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) return { ancho: b.readUInt16BE(i + 7), alto: b.readUInt16BE(i + 5) };
        i += 2 + b.readUInt16BE(i + 2);
      }
    }
    return null;
  } catch {
    return null;
  } finally {
    if (fd !== undefined) closeSync(fd);
  }
}

const huellas = new Map();
/** Huella del contenido de un archivo (memorizada por ruta). */
export function huella(ruta) {
  if (!huellas.has(ruta)) huellas.set(ruta, createHash('sha1').update(readFileSync(ruta)).digest('hex'));
  return huellas.get(ruta);
}

/** Ruta de la imagen que declara el frontmatter (`image:`), resuelta contra la carpeta del post o la raíz del pub. */
export function imagenDeclarada(valor, dirPost, dirPub) {
  if (typeof valor !== 'string' || !valor.trim() || /^https?:/i.test(valor)) return null;
  const v = valor.trim().split(/\s+#/)[0];
  const ruta = v.startsWith('/') ? join(dirPub, v) : isAbsolute(v) ? v : resolve(dirPost, v);
  return RASTER.test(ruta) && esArchivo(ruta) ? ruta : null;
}

/** Una figura sirve de miniatura si es raster, no es diminuta y su proporción cabe en una tarjeta sin mutilarla. */
export function figuraUtil(ruta) {
  if (!RASTER.test(ruta)) return false;
  const d = dimensiones(ruta);
  if (!d || d.ancho < 360 || d.alto < 200) return false;
  const p = d.ancho / d.alto;
  return p >= 0.75 && p <= 2.8;
}

/** La miniatura publicada: una por contenido, compartida si dos posts usan la misma imagen. */
export function miniatura(src, origen) {
  const h = huella(src).slice(0, 12);
  return { src, origen, url: `/miniaturas/${h}.webp`, ...MINIATURA };
}
