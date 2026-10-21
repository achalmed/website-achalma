// src/lib/datos.mjs — el modelo del pub que se está construyendo (PUB=<carpeta> npm run build).
import { modelo } from './modelo.mjs';

export function pubActual() {
  const pub = process.env.PUB;
  if (!pub) throw new Error('Falta PUB: PUB=methodica npm run build (carpeta de web/_pubs/pubs.yml).');
  return pub;
}
export const datos = () => modelo(pubActual());

const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
/** 2021-06-21 → «21 de junio de 2021». */
export function fechaLarga(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || '');
  return m ? `${Number(m[3])} de ${MESES[Number(m[2]) - 1]} de ${m[1]}` : '';
}
/** Tamaño legible: 1 234 567 → «1,2 MB». */
export function peso(bytes) {
  if (!bytes) return '';
  const u = ['B', 'KB', 'MB', 'GB'];
  let i = 0, v = bytes;
  while (v >= 1024 && i < u.length - 1) { v /= 1024; i++; }
  return `${v.toLocaleString('es-PE', { maximumFractionDigits: v < 10 && i > 0 ? 1 : 0 })} ${u[i]}`;
}
export const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;
