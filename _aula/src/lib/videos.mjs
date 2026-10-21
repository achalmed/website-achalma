// src/lib/videos.mjs — los vídeos de divulgacion en las lecciones (fase 8 del plan, decisiones §1.21).
//
// Contrato: divulgacion/catalogo.json → piezas[] con `curriculo: [{curso, tema}]` y `publicaciones: [{red, fecha, url}]`.
// Una pieza aparece en la lección de su tema solo si tiene al menos una publicación con url. YouTube se incrusta con
// youtube-nocookie y solo al pulsar (nada se pide a YouTube antes); TikTok, Facebook y lo demás van como enlace simple.
// Funciones puras: las usan el modelo del pub (src/lib/modelo.mjs), la página de demostración y su prueba.

const RED = { youtube: 'YouTube', tiktok: 'TikTok', facebook: 'Facebook', instagram: 'Instagram', x: 'X', twitter: 'X' };

/** Id de un vídeo de YouTube (watch?v=, youtu.be/, /shorts/, /embed/, /live/); null si la url no es de YouTube. */
export function idYoutube(url) {
  let u;
  try { u = new URL(url); } catch { return null; }
  const host = u.hostname.replace(/^www\.|^m\./, '');
  let id = null;
  if (host === 'youtu.be') id = u.pathname.split('/')[1];
  else if (host === 'youtube.com' || host === 'youtube-nocookie.com') {
    if (u.pathname === '/watch') id = u.searchParams.get('v');
    else {
      const m = /^\/(shorts|embed|live)\/([^/?#]+)/.exec(u.pathname);
      if (m) id = m[2];
    }
  }
  return id && /^[A-Za-z0-9_-]{6,20}$/.test(id) ? id : null;
}

/** Una publicación normalizada: { red, nombreRed, url, fecha, youtube: id|null, incrustar: url|null }. */
export function publicacion(p) {
  if (!p || typeof p.url !== 'string' || !/^https:\/\//.test(p.url)) return null;
  const yt = idYoutube(p.url);
  const red = String(p.red ?? (yt ? 'youtube' : '')).toLowerCase();
  return {
    red,
    nombreRed: RED[red] ?? (red ? red.charAt(0).toUpperCase() + red.slice(1) : new URL(p.url).hostname),
    url: p.url,
    fecha: p.fecha ? String(p.fecha).slice(0, 10) : null,
    youtube: yt,
    incrustar: yt ? `https://www.youtube-nocookie.com/embed/${yt}?rel=0` : null,
  };
}

/** Las piezas publicadas de un tema de un curso, con sus publicaciones normalizadas (las que tienen url). */
export function videosDelTema(piezas, curso, tema) {
  const salida = [];
  for (const pz of piezas ?? []) {
    const toca = (pz.curriculo ?? []).some((c) => c.curso === curso && String(c.tema) === String(tema));
    if (!toca) continue;
    const pubs = (pz.publicaciones ?? []).map(publicacion).filter(Boolean)
      .sort((a, b) => Number(Boolean(b.youtube)) - Number(Boolean(a.youtube)) || String(a.fecha).localeCompare(String(b.fecha)));
    if (!pubs.length) continue;
    salida.push({
      id: pz.id,
      titulo: pz.titulo,
      descripcion: pz.descripcion ?? null,
      principal: pubs[0],
      otras: pubs.slice(1),
    });
  }
  return salida;
}
