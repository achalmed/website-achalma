// src/lib/alineamiento.mjs — lo que el estudiante ve del alineamiento de un curso (docencia/docs/estandar-docencia.md §10):
// los resultados de aprendizaje con su evidencia (evaluaciones) y su actividad (sesiones), la política de IA del curso y
// de cada evaluación, la rúbrica de cada evaluación que la tenga y, por sesión, el banco de recuperación SIN claves.
//
// Fuentes (solo lectura): curso.yml → alineamiento y politica_ia; 01-diseno/rubricas/<clave>.yml (formato común de
// escritura/config/entrega/rubrica.schema.yml); 03-sesiones/sNN-*/sesion.yml y recuperacion.yml.
// Las claves del banco (`respuesta`, `explicacion`) nunca entran al modelo: de cada pregunta se copian solo los campos
// de PREGUNTA_PUBLICA; las claves se revisan en la puesta en común de la clase (y viajan en el mazo, que es aparte).
// Lo que propuso la IA y no se verificó (`origen.autor: llm` sin `verificacion: verificada`) no se muestra: la misma regla
// que `publicable()` de docencia/scripts/alineamiento.py (FLUJO_DE_CONOCIMIENTO C3.3; decisiones §1.24).

import * as F from './fuentes.mjs';

/** Vocabulario cerrado del uso de IA por evaluación: el mismo de POLITICA_IA en docencia/scripts/alineamiento.py. */
export const POLITICA_IA = {
  prohibida: { etiqueta: 'Prohibida', descripcion: 'Sin herramientas de IA generativa.' },
  apoyo: { etiqueta: 'Apoyo', descripcion: 'IA solo para ideas, dudas y revisión de lenguaje; se declara.' },
  asistida: { etiqueta: 'Asistida', descripcion: 'IA para código o borrador, verificado línea a línea; se declara cada uso.' },
  libre: { etiqueta: 'Libre', descripcion: 'Cualquier uso, declarado y verificado; quien entrega responde por todo.' },
};
/** Taxonomía SOLO (Biggs): el nivel de comprensión que pide cada resultado. */
const NIVEL_SOLO = { uniestructural: 'Uniestructural', multiestructural: 'Multiestructural', relacional: 'Relacional', abstracto_ampliado: 'Abstracto ampliado' };
const TIPO_EVALUACION = { formativa: 'Formativa', sumativa: 'Sumativa' };
const PREGUNTA_PUBLICA = ['id', 'resultado', 'tipo', 'enunciado', 'opciones'];

const numeroDe = (carpeta) => carpeta.slice(0, 3);   // s01-diseno-… → s01

/** La pregunta puede salir al estudiante: no es una propuesta de la IA pendiente de verificar (`publicable()` de
 *  docencia/scripts/alineamiento.py). */
export function publicable(p) {
  const org = p?.origen;
  return !(org && typeof org === 'object' && org.autor === 'llm' && org.verificacion !== 'verificada');
}
const publicables = (banco) => (Array.isArray(banco?.preguntas) ? banco.preguntas.filter(publicable) : []);

function rubrica(dirCurso, ruta, mide) {
  const r = F.rubricaDeCurso(dirCurso, ruta);
  if (!r || !Array.isArray(r.criterios)) return null;
  const nombres = new Map();
  for (const c of r.criterios) for (const n of c.niveles ?? []) if (n.nombre && !nombres.has(n.puntaje)) nombres.set(n.puntaje, n.nombre);
  const puntajes = [...new Set(r.criterios.flatMap((c) => (c.niveles ?? []).map((n) => n.puntaje)))].sort((a, b) => b - a);
  return {
    clave: r.clave ?? ruta.split('/').pop().replace(/\.ya?ml$/, ''),
    titulo: r.titulo,
    fuente: r.fuente ?? null,
    escala: puntajes.map((p) => ({ puntaje: p, nombre: nombres.get(p) ?? String(p) })),
    criterios: r.criterios.map((c) => ({
      clave: c.clave,
      nombre: c.nombre,
      peso: c.peso,
      resultado: mide?.[c.clave] ?? null,
      niveles: puntajes.map((p) => (c.niveles ?? []).find((n) => n.puntaje === p)?.descriptor ?? ''),
    })),
    usan: [],
  };
}

/** El alineamiento del curso para su página; null si el curso no declara nada de §10 (ni alineamiento, ni política de
 *  IA, ni bancos de recuperación). `avisos` recibe lo que no se pudo leer. */
export function aprendizajeDelCurso(curso, avisos = []) {
  const dir = curso._dir;
  const al = curso.alineamiento ?? null;
  const pia = curso.politica_ia?.regla ? curso.politica_ia : null;
  const sesiones = dir ? F.sesionesDeCurso(dir) : [];
  const conBanco = sesiones.filter((s) => publicables(s.banco).length);
  if (!al && !pia && !conBanco.length) return null;

  const tituloSesion = new Map(sesiones.map((s) => [s.carpeta, s.sesion.titulo ?? s.carpeta]));
  const resultadosDe = new Map(sesiones.map((s) => [s.carpeta, (s.sesion.resultados_aprendizaje ?? []).filter((x) => typeof x === 'string')]));
  const evaluacionesYml = al?.evaluaciones ?? [];

  // Rúbricas: una vez cada archivo, con las evaluaciones que la usan (la de réplica sirve al informe y a la ronda de pares).
  const rubricas = new Map();
  const evaluaciones = evaluacionesYml.map((e) => {
    let rub = null;
    if (e.rubrica) {
      if (!rubricas.has(e.rubrica)) {
        const clave = e.rubrica.split('/').pop().replace(/\.ya?ml$/, '');
        const r = rubrica(dir, e.rubrica, al?.rubricas?.[clave]);
        if (!r) avisos.push(`${curso.id}: la evaluación ${e.id} cita una rúbrica que no se puede leer: ${e.rubrica}`);
        rubricas.set(e.rubrica, r);
      }
      rub = rubricas.get(e.rubrica);
      rub?.usan.push(e.titulo);
    }
    const politica = POLITICA_IA[e.politica_ia] ?? null;
    if (!politica) avisos.push(`${curso.id}: la evaluación ${e.id} no declara una política de IA del vocabulario (${e.politica_ia ?? 'ninguna'})`);
    return {
      id: e.id,
      titulo: e.titulo,
      tipo: e.tipo,
      tipoEtiqueta: TIPO_EVALUACION[e.tipo] ?? e.tipo,
      peso: e.peso ?? null,
      resultados: e.resultados ?? [],
      politica: politica ? { clave: e.politica_ia, ...politica } : null,
      sesion: e.sesion ? { numero: numeroDe(e.sesion), titulo: tituloSesion.get(e.sesion) ?? e.sesion } : null,
      rubrica: rub ? { clave: rub.clave, titulo: rub.titulo } : null,
    };
  });

  const resultados = (al?.resultados ?? []).map((r) => ({
    id: r.id,
    enunciado: r.enunciado,
    nivel: r.nivel ?? null,
    nivelEtiqueta: NIVEL_SOLO[r.nivel] ?? null,
    evidencias: evaluaciones.filter((e) => e.resultados.includes(r.id)).map((e) => ({ id: e.id, titulo: e.titulo, tipoEtiqueta: e.tipoEtiqueta, peso: e.peso })),
    sesiones: sesiones.filter((s) => resultadosDe.get(s.carpeta).includes(r.id)).map((s) => ({ numero: numeroDe(s.carpeta), titulo: tituloSesion.get(s.carpeta) })),
  }));

  const repaso = conBanco.map((s) => ({
    carpeta: s.carpeta,
    numero: numeroDe(s.carpeta),
    titulo: tituloSesion.get(s.carpeta),
    resultados: resultadosDe.get(s.carpeta),
    fuente: s.banco.fuente ?? null,
    preguntas: publicables(s.banco).map((p) => Object.fromEntries(PREGUNTA_PUBLICA.filter((k) => p[k] != null).map((k) => [k, p[k]]))),
    mazo: null,   // modelo.mjs lo enlaza si alguna edición publicó practice/mazo.tsv de esta sesión
  }));

  return {
    repasar: repasoDelCurso(curso, conBanco, tituloSesion, avisos),
    alcance: al?.alcance ?? null,
    fuente: al?.fuente ?? null,
    resultados,
    evaluaciones,
    rubricas: [...rubricas.values()].filter(Boolean),
    politica: pia ? { regla: pia.regla, declaracion: pia.declaracion ?? null, datos: pia.datos ?? null, fuente: pia.fuente ?? null } : null,
    repaso,
    fuenteRepaso: conBanco[0]?.banco.fuente ?? null,
  };
}

/**
 * Las preguntas cerradas de los bancos del curso, con su clave, para el repaso espaciado de su página «Repasar»
 * (src/rutas/curso-repasar.astro; decisiones §1.25). Vienen del exportador de docencia (F.quizDeSesion), no de leer aquí
 * `respuesta`: la clave del ítem tiene un solo dueño. null si ninguna sesión tiene preguntas que se corrijan solas o si el
 * exportador no corre (entonces, un aviso y la página no se genera).
 */
function repasoDelCurso(curso, conBanco, tituloSesion, avisos) {
  const preguntas = [];
  const sesiones = [];
  for (const s of conBanco) {
    let quiz;
    try {
      quiz = F.quizDeSesion(curso._dir, s.carpeta);
    } catch (e) {
      avisos.push(`${curso.id}: sin página de repaso, el exportador del banco falló (${e.message})`);
      return null;
    }
    const delBanco = new Set(publicables(s.banco).map((p) => String(p.id)));
    const propias = quiz.filter((q) => {
      if (delBanco.has(String(q.id))) return true;
      avisos.push(`${curso.id}: el exportador dio la pregunta ${q.id}, que la vitrina no ve en ${s.carpeta}/recuperacion.yml`);
      return false;
    });
    if (!propias.length) continue;
    const numero = numeroDe(s.carpeta);
    sesiones.push({ numero, titulo: tituloSesion.get(s.carpeta), n: propias.length });
    for (const q of propias) preguntas.push({ ...q, sesion: numero });
  }
  return preguntas.length ? { preguntas, sesiones, url: `/cursos/${curso.id}/repasar/` } : null;
}
