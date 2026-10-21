// /buscar.json — el índice de la paleta de comandos (⌘K): cursos, lecciones, artículos y ediciones del pub, con lo
// mínimo para buscar y abrir. Se genera en el build desde el modelo; la paleta lo pide la primera vez que se abre.
import { datos } from '../lib/datos.mjs';

export function GET() {
  const { propios, blog, ediciones } = datos();
  const items = [
    ...propios.map((c) => ({ t: 'curso', titulo: c.titulo, contexto: [c.tipoEtiqueta, `${c.nPublicadas} de ${c.nTemas} temas con lección`].join(' · '), url: c.url })),
    ...propios.flatMap((c) => c.lecciones.map((l) => ({ t: 'leccion', titulo: l.titulo, contexto: l.tema ? `${c.titulo} · tema ${l.tema.id}` : `${c.titulo} · lectura complementaria`, url: l.url }))),
    ...blog.map((b) => ({ t: 'articulo', titulo: b.titulo, contexto: `${b.fecha} · ${b.minutos} min`, url: b.url })),
    ...ediciones.map((e) => ({ t: 'edicion', titulo: e.titulo, contexto: `${e.periodo} · ${e.sesiones.length} sesiones`, url: e.url })),
  ];
  return new Response(JSON.stringify(items), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
}
