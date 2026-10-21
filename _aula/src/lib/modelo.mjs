// src/lib/modelo.mjs — el modelo de un pub: lo que la vitrina publica, armado desde las fuentes.
//
// Reglas (docs/decisiones.md §1.3–§1.5):
// - Un curso vive en el pub de su PRIMER `area` (docencia/config/areas.yml); las áreas siguientes lo listan.
// - Una lección publicada es un post del pub con destino `leccion` en mapa-lecciones.csv, sin `draft: true`
//   y con su HTML en _site/. Si su tema existe en curso.yml, ocupa ese tema; si no, va a «lecturas
//   complementarias» del curso. Los posts con destino `revisar` ya publicados también van ahí.
// - El blog del pub son sus posts con destino `blog` publicados.
// - Una edición (dictado.yml) pertenece al pub donde vive alguno de sus cursos; una edición legado sin
//   cursos hereda el pub de otra edición con la misma materia web.

import { existsSync, readdirSync } from 'node:fs';
import { basename, join, relative } from 'node:path';
import * as F from './fuentes.mjs';
import { RUTAS, INDEX_DIR } from './rutas.mjs';
import { extraer } from './contenido.mjs';
import { figuraUtil, huella, imagenDeclarada, miniatura } from './imagenes.mjs';
import { MARCA } from './marca.generado.mjs';

export const ETIQUETAS = {
  tipo: { asignatura: 'Asignatura', herramienta: 'Herramienta', taller: 'Taller', nivelacion: 'Nivelación' },
  estado: { activo: 'Activo', borrador: 'En construcción', archivado: 'Archivado' },
  nivel: { pregrado: 'Pregrado', posgrado: 'Posgrado', preuniversitario: 'Preuniversitario' },
  material: { slides: 'Diapositivas', practice: 'Práctica', evaluation: 'Evaluación', homework: 'Tarea', readings: 'Lecturas' },
};
const etiqueta = (grupo, v) => ETIQUETAS[grupo]?.[v] ?? (v ? String(v).charAt(0).toUpperCase() + String(v).slice(1) : '');

const PALABRAS_MENORES = new Set(['y', 'e', 'de', 'del', 'la', 'el']);
/** Nombre visible derivado de la carpeta (numerus-scriptum → Numerus Scriptum). */
export function nombreDePub(carpeta, vitrina = {}) {
  const fijo = vitrina?.pubs?.[carpeta]?.nombre;
  if (fijo) return fijo;
  return carpeta.split('-').map((w, i) => (i > 0 && PALABRAS_MENORES.has(w) ? w : w[0].toUpperCase() + w.slice(1))).join(' ');
}

/** Slug estable de un post: sin fecha ni número de serie (2021-06-21-05-iteraciones → iteraciones). */
export function slugDePost(carpeta) {
  // kebab-case ASCII (normativa 2.3): sin tildes ni eñes, para que la URL nueva no dependa de cómo se codifique
  return carpeta.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace(/^\d{2,3}-/, '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase();
}

/** Las descripciones de relleno de los esqueletos («Estructura estándar 00–09…») no se publican. */
function descripcionUtil(d) {
  if (!d || /Estructura estándar/i.test(d)) return null;
  return String(d).replace(/\*\*(.+?)\*\*/g, '$1').trim();
}

const ORDEN_CONFIANZA = { alta: 0, media: 1, baja: 2, ninguna: 3 };
const EXT_FUERA = /\.(tex|md|qmd|yml|yaml|log|aux)$/i;

const memo = new Map();

export function modelo(pubId) {
  if (!memo.has(pubId)) memo.set(pubId, construir(pubId));
  return memo.get(pubId);
}

function construir(pubId) {
  const registro = F.registroPubs();
  const reg = registro.pubs.find((p) => p.carpeta === pubId);
  if (!reg) throw new Error(`PUB=${pubId} no está en web/_pubs/pubs.yml (válidos: ${registro.pubs.map((p) => p.carpeta).join(', ')})`);
  const vit = F.vitrina();
  const presentacion = vit?.pubs?.[pubId] ?? {};
  const areas = F.areas();
  const area = areas.find((a) => a.pub === pubId) ?? null;
  const casaDeArea = Object.fromEntries(areas.map((a) => [a.id, a.pub]));
  const dirPub = join(RUTAS.pubs, pubId);
  const siteRoot = join(dirPub, '_site');
  const dominio = new URL(reg.url);
  const avisos = [];

  // «La familia» (pie): los 11 pubs de pubs.yml y el hub, con su área (areas.yml), su acento y su colofón (vitrina.yml →
  // scripts/marca.py → marca.generado.mjs).
  const areaDePub = Object.fromEntries(areas.filter((a) => a.pub).map((a) => [a.pub, a.nombre]));
  for (const p of registro.pubs) {
    if (MARCA.sitios[p.carpeta]?.letras !== vit?.pubs?.[p.carpeta]?.monograma) {
      throw new Error(`${p.carpeta}: el monograma de config/vitrina.yml no coincide con marca.generado.mjs; corre python3 scripts/marca.py --aplicar`);
    }
  }
  const red = [
    ...registro.pubs.map((p) => ({
      id: p.carpeta, nombre: nombreDePub(p.carpeta, vit), url: p.url, tema: p.tema,
      area: areaDePub[p.carpeta] ?? p.tema, acento: vit?.pubs?.[p.carpeta]?.acento ?? 'revista', marca: p.carpeta,
      actual: p.carpeta === pubId,
    })),
    {
      id: registro.hub.carpeta, nombre: vit?.hub?.nombre ?? registro.autor.nombre, url: registro.hub.url, tema: vit?.hub?.area ?? '',
      area: vit?.hub?.area ?? '', acento: vit?.hub?.acento ?? 'tinta', marca: 'hub', actual: false, hub: true,
    },
  ];
  const pub = {
    id: pubId,
    nombre: nombreDePub(pubId, vit),
    url: reg.url,
    tema: reg.tema,
    descripcion: reg.descripcion,
    acento: presentacion.acento ?? 'revista',
    area: area ? { id: area.id, nombre: area.nombre } : null,
    autor: registro.autor,
    hub: registro.hub,
    licencia: registro.licencia_contenido,
  };

  // ── Cursos del pub ────────────────────────────────────────────────────────
  const todos = F.cursos();
  const cursos = [];
  for (const c of todos) {
    const lista = Array.isArray(c.area) ? c.area : c.area ? [c.area] : [];
    const casa = casaDeArea[lista[0]] ?? null;
    const vive = casa === pubId;
    const listado = !vive && lista.slice(1).some((a) => casaDeArea[a] === pubId);
    if (!vive && !listado) continue;
    const unidades = (c.unidades ?? []).map((u) => ({
      id: u.id,
      titulo: u.titulo,
      temas: (u.temas ?? []).map((t) => ({ id: String(t.id), titulo: t.titulo, leccion: null })),
    }));
    const regCasa = registro.pubs.find((p) => p.carpeta === casa);
    cursos.push({
      id: c.id,
      titulo: c.titulo,
      descripcion: descripcionUtil(c.descripcion),
      tipo: c.tipo, tipoEtiqueta: etiqueta('tipo', c.tipo),
      estado: c.estado, estadoEtiqueta: etiqueta('estado', c.estado),
      nivel: c.nivel, nivelEtiqueta: etiqueta('nivel', c.nivel),
      prerrequisitos: c.prerrequisitos ?? [],
      bibliografia: (c.bibliografia ?? []).map((b) => ({ titulo: b.titulo, autor: b.autor, calibre_id: b.calibre_id ?? null })),
      vive, casa, casaNombre: casa ? nombreDePub(casa, vit) : null,
      urlCasa: !vive && regCasa ? new URL(`cursos/${c.id}/`, regCasa.url).href : null,
      url: `/cursos/${c.id}/`,
      unidades,
      nTemas: unidades.reduce((s, u) => s + u.temas.length, 0),
      lecciones: [],
      complementarias: [],
      ediciones: [],
      modelos: [],
    });
  }
  const cursoPorId = new Map(cursos.map((c) => [c.id, c]));

  // ── Posts publicados del pub (mapa-lecciones.csv) ─────────────────────────
  const filas = F.mapaLecciones().filter((f) => f.pub === pubId);
  const posts = [];
  for (const f of filas) {
    const qmd = join(f._abs, 'index.qmd');
    if (!existsSync(qmd)) { avisos.push(`el mapa cita un post que no existe: ${f.ruta_post}`); continue; }
    const fm = F.frontmatter(qmd) ?? {};
    if (fm.draft === true || String(fm.draft) === 'true') continue; // borrador: no se publica
    const rel = relative(dirPub, f._abs).split('\\').join('/');
    const html = join(siteRoot, rel, 'index.html');
    if (!existsSync(html)) { avisos.push(`publicado sin HTML en _site: ${rel}`); continue; }
    if (f.draft !== 'false') avisos.push(`el mapa marca draft=${f.draft} pero el post está publicado: ${rel}`);
    posts.push({ fila: f, fm, rel, html, rutaVieja: `/${rel}/`, carpeta: basename(f._abs) });
  }

  const lecciones = [];
  const blog = [];
  const slugsBlog = new Set();
  for (const p of posts) {
    const { fila: f, fm } = p;
    const comun = {
      titulo: String(fm.title ?? f.titulo_post).replace(/`([^`]+)`/g, '$1'),
      descripcion: typeof fm.description === 'string' ? fm.description.trim() : null,
      fecha: fm.date ? String(fm.date).slice(0, 10) : f.fecha,
      categorias: Array.isArray(fm.categories) ? fm.categories : [],
      quiz: Array.isArray(fm.quiz) ? fm.quiz : null,
      rutaVieja: p.rutaVieja,
      html: p.html,
      dirSite: join(siteRoot, p.rel),
      confianza: f.confianza,
      imagenPropia: imagenDeclarada(fm.image, f._abs, dirPub),
    };
    if (f.destino === 'blog') {
      let slug = slugDePost(p.carpeta);
      if (slugsBlog.has(slug)) slug = p.carpeta;
      slugsBlog.add(slug);
      blog.push({ ...comun, slug, url: `/blog/${slug}/`, curso: f.curso || null });
    } else if (f.destino === 'leccion' || f.destino === 'revisar') {
      const curso = cursoPorId.get(f.curso);
      if (!curso || !curso.vive) {
        avisos.push(`lección de un curso que no vive en ${pubId} (${f.curso || 'sin curso'}): ${p.rel}`);
        continue;
      }
      const slug = slugDePost(p.carpeta);
      lecciones.push({ ...comun, slug, curso: curso.id, temaId: f.destino === 'leccion' ? f.tema_id || null : null, destino: f.destino, url: `/cursos/${curso.id}/${slug}/` });
    }
  }

  // Mapa de URL viejas → nuevas (para reescribir enlaces entre posts y para _redirects).
  const mapaUrls = new Map([...lecciones, ...blog].map((x) => [x.rutaVieja, x.url]));

  // Extracción del contenido (HTML de Quarto → cuerpo limpio).
  const recursos = [];
  const sinResolver = [];
  let anclasReparadas = 0;
  for (const x of [...lecciones, ...blog]) {
    const e = extraer({ html: x.html, siteRoot, rutaVieja: x.rutaVieja, rutaNueva: x.url, dominio, mapaUrls });
    Object.assign(x, { cuerpo: e.html, indice: e.indice, secciones: e.secciones, palabras: e.palabras, minutos: e.minutos, hayMatematicas: e.hayMatematicas, figuras: e.figuras });
    recursos.push(...e.recursos);
    anclasReparadas += e.anclasReparadas;
    sinResolver.push(...e.sinResolver.map((s) => ({ ...s, pagina: x.url })));
    for (const formato of ['pdf', 'docx']) {
      const src = join(x.dirSite, `index.${formato}`);
      if (F.esArchivo(src)) {
        x[formato] = { url: `${x.url}index.${formato}`, bytes: F.tamano(src) };
        recursos.push({ src, dest: `${x.url}index.${formato}` });
      } else x[formato] = null;
    }
    // Las figuras en PDF que Quarto compila para el documento (index_files/figure-pdf/) también están publicadas en el
    // sitio viejo: viajan con el post para que la redirección de su carpeta no deje ninguna URL sin destino.
    const figurasPdf = join(x.dirSite, 'index_files', 'figure-pdf');
    if (existsSync(figurasPdf)) {
      for (const n of readdirSync(figurasPdf)) recursos.push({ src: join(figurasPdf, n), dest: `${x.url}index_files/figure-pdf/${n}` });
    }
    delete x.html;
  }

  // Miniaturas de las tarjetas (src/lib/imagenes.mjs): la imagen propia del post, si ningún otro post del pub la
  // comparte; si no, la primera figura útil del cuerpo; si no, ninguna (la tarjeta muestra el índice del texto).
  const usos = new Map();
  for (const x of [...lecciones, ...blog]) if (x.imagenPropia) usos.set(huella(x.imagenPropia), (usos.get(huella(x.imagenPropia)) ?? 0) + 1);
  const miniaturas = new Map();
  for (const x of [...lecciones, ...blog]) {
    const propia = x.imagenPropia && usos.get(huella(x.imagenPropia)) === 1 ? x.imagenPropia : null;
    const figura = propia ? null : x.figuras.find(figuraUtil) ?? null;
    x.imagen = propia ? miniatura(propia, 'portada') : figura ? miniatura(figura, 'figura') : null;
    if (x.imagen) miniaturas.set(x.imagen.url, x.imagen);
    delete x.imagenPropia;
    delete x.figuras;
  }

  // Lecciones en el temario de su curso.
  for (const l of lecciones) {
    const curso = cursoPorId.get(l.curso);
    let tema = null, unidad = null;
    if (l.temaId) {
      for (const u of curso.unidades) {
        const t = u.temas.find((t) => t.id === l.temaId);
        if (t) { tema = t; unidad = u; break; }
      }
      if (!tema) avisos.push(`tema ${l.temaId} no existe en ${curso.id}/curso.yml: ${l.rutaVieja}`);
      else if (tema.leccion) { avisos.push(`tema ${curso.id} ${l.temaId} ya tiene lección; esta va a complementarias: ${l.rutaVieja}`); tema = null; unidad = null; }
    }
    if (tema) {
      tema.leccion = { slug: l.slug, url: l.url, titulo: l.titulo };
      l.tema = { id: tema.id, titulo: tema.titulo };
      l.unidad = { id: unidad.id, titulo: unidad.titulo };
    } else {
      l.tema = null;
      l.unidad = null;
      curso.complementarias.push(l);
    }
  }
  for (const c of cursos) {
    const enTemario = [];
    for (const u of c.unidades) for (const t of u.temas) if (t.leccion) enTemario.push(lecciones.find((l) => l.url === t.leccion.url));
    c.complementarias.sort((a, b) => (a.fecha || '').localeCompare(b.fecha || '') || a.slug.localeCompare(b.slug));
    c.lecciones = [...enTemario, ...c.complementarias];
    c.lecciones.forEach((l, i) => {
      l.orden = i;
      l.anterior = c.lecciones[i - 1] ? { url: c.lecciones[i - 1].url, titulo: c.lecciones[i - 1].titulo } : null;
      l.siguiente = c.lecciones[i + 1] ? { url: c.lecciones[i + 1].url, titulo: c.lecciones[i + 1].titulo } : null;
    });
    c.nPublicadas = enTemario.length;
    c.nLecciones = c.lecciones.length;
    c.primera = c.lecciones[0]?.url ?? null;
  }
  blog.sort((a, b) => (b.fecha || '').localeCompare(a.fecha || ''));

  // ── Ediciones (dictados) ──────────────────────────────────────────────────
  const dictados = F.dictados();
  const materiaDePub = new Map();
  for (const d of dictados) {
    if ((d.cursos ?? []).some((id) => cursoPorId.get(id)?.vive) && d.web?.materia) materiaDePub.set(d.web.materia, pubId);
  }
  const ediciones = [];
  for (const d of dictados) {
    const propios = (d.cursos ?? []).filter((id) => cursoPorId.get(id)?.vive);
    const heredada = !(d.cursos ?? []).length && d.web?.materia && materiaDePub.get(d.web.materia) === pubId;
    if (!propios.length && !heredada) continue;
    const dirWeb = d.web ? join(RUTAS.cursosWeb, d.web.materia, d.web.edicion) : null;
    const fmEd = dirWeb && existsSync(join(dirWeb, 'index.qmd')) ? F.frontmatter(join(dirWeb, 'index.qmd')) : {};
    const url = `/ediciones/${d.id}/`;
    const sesiones = (d.sesiones ?? []).map((s) => {
      const dirS = dirWeb ? join(dirWeb, s.web) : null;
      const fmS = dirS && existsSync(join(dirS, 'index.qmd')) ? F.frontmatter(join(dirS, 'index.qmd')) : {};
      const dirPubl = join(d._dir, 'publicacion', s.web);
      const materiales = [];
      const vistos = new Set();
      for (const base of [dirPubl, dirS].filter((x) => x && existsSync(x))) {
        for (const tipo of ['slides', 'practice', 'evaluation', 'homework', 'resources/readings']) {
          const dir = join(base, tipo);
          if (!existsSync(dir)) continue;
          for (const nombre of readdirSync(dir).sort()) {
            const src = join(dir, nombre);
            if (nombre.startsWith('.') || nombre.startsWith('_') || EXT_FUERA.test(nombre) || !F.esArchivo(src)) continue;
            const clave = basename(tipo) + '/' + nombre;
            if (vistos.has(clave)) continue;
            vistos.add(clave);
            const dest = `${url}${s.web}/${clave}`;
            recursos.push({ src, dest });
            materiales.push({ tipo: basename(tipo), tipoEtiqueta: etiqueta('material', basename(tipo)), nombre, url: dest, bytes: F.tamano(src), ext: (nombre.split('.').pop() || '').toLowerCase() });
          }
        }
      }
      return {
        orden: s.orden,
        titulo: s.titulo ?? fmS?.title ?? s.web,
        fecha: fmS?.date ? String(fmS.date).slice(0, 10) : null,
        curso: s.curso ? { id: s.curso, titulo: cursoPorId.get(s.curso)?.titulo ?? s.curso } : null,
        materiales,
      };
    });
    const ed = {
      id: d.id,
      url,
      titulo: d.titulo ?? fmEd?.title ?? d.id,
      periodo: d.periodo,
      institucion: d.institucion,
      estado: d.estado,
      legado: !!d.legado,
      nota: d.nota ?? null,
      descripcion: d.descripcion ?? fmEd?.description ?? null,
      cursos: propios.map((id) => ({ id, titulo: cursoPorId.get(id).titulo, url: cursoPorId.get(id).url })),
      urlHub: d.web ? new URL(`cursos/${d.web.materia}/${d.web.edicion}/`, registro.hub.url).href : null,
      sesiones,
      nMateriales: sesiones.reduce((s, x) => s + x.materiales.length, 0),
    };
    ediciones.push(ed);
    for (const id of propios) cursoPorId.get(id).ediciones.push({ id: ed.id, url: ed.url, titulo: ed.titulo, periodo: ed.periodo, estado: ed.estado, nSesiones: sesiones.filter((s) => !s.curso || s.curso.id === id).length });
  }
  ediciones.sort((a, b) => String(b.periodo).localeCompare(String(a.periodo)));

  // ── Laboratorio (simuladores/catalogo.json) ───────────────────────────────
  for (const m of F.catalogoSimuladores()) {
    for (const ref of m.cursos ?? []) {
      const c = cursoPorId.get(ref.curso);
      if (c && c.vive) c.modelos.push({ id: m.id, ref: m.ref, titulo: m.titulo, tema: ref.tema, nivel: m.nivel, pregunta: m.ficha?.pregunta ?? null, disciplina: m.disciplina });
    }
  }

  // ── Portada: lección en curso y cursos destacados ─────────────────────────
  const destacadaFija = presentacion.leccion_destacada;
  let enCurso = null;
  if (destacadaFija) {
    const l = lecciones.find((x) => `${x.curso}/${x.slug}` === destacadaFija);
    if (l) enCurso = { origen: 'leccion', item: l };
    else avisos.push(`config/vitrina.yml: leccion_destacada ${destacadaFija} no está publicada`);
  }
  if (!enCurso) {
    const candidatas = lecciones
      .filter((l) => l.tema && l.secciones.length >= 3)
      .sort((a, b) => (ORDEN_CONFIANZA[a.confianza] ?? 9) - (ORDEN_CONFIANZA[b.confianza] ?? 9) || a.orden - b.orden);
    const conCodigo = candidatas.find((l) => l.secciones.filter((s) => s.codigo).length >= 3);
    const l = conCodigo ?? candidatas[0];
    if (l) enCurso = { origen: 'leccion', item: l };
  }
  if (!enCurso) {
    const a = blog.find((b) => b.secciones.length >= 3);
    if (a) enCurso = { origen: 'blog', item: a };
  }

  const propios = cursos.filter((c) => c.vive);
  const destacados = [...propios]
    .sort((a, b) => b.nLecciones - a.nLecciones || (a.estado === 'activo' ? -1 : 0) - (b.estado === 'activo' ? -1 : 0) || b.nTemas - a.nTemas)
    .slice(0, 3);

  // Advertencias sobre la calidad del currículo (para el informe; no bloquean).
  for (const c of propios) {
    if (!c.unidades.length) avisos.push(`curso sin unidades en curso.yml: ${c.id}`);
    const sinTilde = c.unidades.flatMap((u) => u.temas).filter((t) => /cion(es)?\b|\b(Metodo|Tecnicas|Analisis|Que|Tamano|Diseno)\b/.test(t.titulo)).length;
    if (sinTilde) avisos.push(`${c.id}: ${sinTilde} títulos de tema sin tildes en curso.yml`);
  }

  return {
    pub, red, cursos, propios, destacados, lecciones, blog, ediciones, enCurso,
    recursos: dedupe(recursos),
    miniaturas: [...miniaturas.values()],
    redirecciones: [...lecciones, ...blog].map((x) => ({ desde: x.rutaVieja, hacia: x.url })),
    avisos, sinResolver, anclasReparadas,
    totales: {
      cursos: propios.length,
      listados: cursos.length - propios.length,
      temas: propios.reduce((s, c) => s + c.nTemas, 0),
      lecciones: lecciones.filter((l) => l.tema).length,
      complementarias: lecciones.filter((l) => !l.tema).length,
      articulos: blog.length,
      ediciones: ediciones.length,
    },
  };
}

function dedupe(recursos) {
  const vistos = new Map();
  for (const r of recursos) if (!vistos.has(r.dest)) vistos.set(r.dest, r);
  return [...vistos.values()];
}

export { INDEX_DIR };
