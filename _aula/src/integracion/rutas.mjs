// src/integracion/rutas.mjs — las rutas dinámicas del aula se registran aquí (injectRoute) en lugar de vivir en
// carpetas con corchetes bajo src/pages/: la norma del ecosistema pide nombres en kebab-case (normativa 2.3–2.4) y la
// sintaxis [param] de Astro solo hace falta en el patrón, no en el nombre del archivo. Las URL publicadas no cambian.
const RUTAS = [
  ['/blog/[slug]', './src/rutas/blog-entrada.astro'],
  ['/cursos/[curso]', './src/rutas/curso.astro'],
  ['/cursos/[curso]/[leccion]', './src/rutas/leccion.astro'],
  ['/ediciones/[id]', './src/rutas/edicion.astro'],
  ['/[demo]/autoevaluacion', './src/rutas/demo-autoevaluacion.astro'],
];

export default function rutas() {
  return {
    name: 'aula-rutas',
    hooks: {
      'astro:config:setup': ({ injectRoute }) => {
        for (const [pattern, entrypoint] of RUTAS) injectRoute({ pattern, entrypoint });
      },
    },
  };
}
