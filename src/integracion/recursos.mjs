// src/integracion/recursos.mjs — integración de Astro que completa el sitio de un pub al terminar el build:
// 1. copia los recursos que las páginas citan (figuras de los posts, PDF y DOCX de Quarto, materiales de
//    las ediciones) desde sus fuentes, que solo se leen;
// 2. escribe `_redirects` (formato de Netlify) con una redirección 301 por cada URL vieja del pub;
// 3. deja un informe del modelo (cifras, avisos de los datos de origen) en .cache/informe-<pub>.json.

import { copyFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { modelo } from '../lib/modelo.mjs';
import { AULA_DIR } from '../lib/rutas.mjs';

export default function recursos(pub) {
  return {
    name: 'aula-recursos',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        const salida = fileURLToPath(dir);
        const m = modelo(pub);
        let bytes = 0;
        for (const r of m.recursos) {
          const destino = join(salida, decodeURI(r.dest));
          await mkdir(dirname(destino), { recursive: true });
          await copyFile(r.src, destino);
        }
        const lineas = [
          `# _redirects — GENERADO por aula (src/integracion/recursos.mjs); no editar.`,
          `# Cada post del sitio Quarto de ${pub} lleva a su página nueva; los archivos del post (PDF, DOCX, figuras) también.`,
          ...m.redirecciones.map((r) => `${r.desde}*  ${r.hacia}:splat  301`),
        ];
        await writeFile(join(salida, '_redirects'), lineas.join('\n') + '\n');
        await mkdir(join(AULA_DIR, '.cache'), { recursive: true });
        await writeFile(
          join(AULA_DIR, '.cache', `informe-${pub}.json`),
          JSON.stringify({ pub, totales: m.totales, recursos: m.recursos.length, redirecciones: m.redirecciones.length, avisos: m.avisos, anclasReparadas: m.anclasReparadas, sinResolver: m.sinResolver }, null, 2),
        );
        logger.info(`${m.recursos.length} recursos copiados, ${m.redirecciones.length} redirecciones; ${m.avisos.length} avisos de datos (.cache/informe-${pub}.json)`);
      },
    },
  };
}
