// src/integracion/recursos.mjs — integración de Astro que completa el sitio de un pub al terminar el build:
// 1. copia los recursos que las páginas citan (figuras de los posts, PDF y DOCX de Quarto, materiales de
//    las ediciones) desde sus fuentes, que solo se leen;
// 2. escribe `_redirects` (formato de Netlify) con una redirección 301 por cada URL vieja del pub;
// 3. escribe las miniaturas de las tarjetas (640 × 400, WebP) con sharp (src/lib/imagenes.mjs, decisiones §1.17);
// 4. escribe el colofón del pub como archivos: favicon.svg, favicon-32.png, apple-touch-icon.png (180) y og.png
//    (1200 × 630), desde src/lib/marca.mjs (decisiones §1.18);
// 5. deja un informe del modelo (cifras, avisos de los datos de origen) en .cache/informe-<pub>.json.

import { copyFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import { svgOg, svgSello } from '../lib/marca.mjs';
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
        // Miniaturas: recorte a 16:10; la foto propia busca la zona con más detalle y la figura se centra sobre blanco
        // (las gráficas de Quarto tienen fondo transparente o blanco).
        for (const im of m.miniaturas) {
          const destino = join(salida, im.url);
          await mkdir(dirname(destino), { recursive: true });
          let t = sharp(im.src, { limitInputPixels: 1e8 }).rotate();
          if (im.origen === 'figura') t = t.flatten({ background: { r: 255, g: 255, b: 255 } });
          await t.resize(im.ancho, im.alto, { fit: 'cover', position: im.origen === 'figura' ? 'centre' : 'attention' })
            .webp({ quality: 72, effort: 5 }).toFile(destino);
        }
        // Colofón del pub como archivos.
        const sello = svgSello(pub, m.pub.acento);
        await writeFile(join(salida, 'favicon.svg'), sello);
        await sharp(Buffer.from(sello), { density: 300 }).resize(32, 32).png().toFile(join(salida, 'favicon-32.png'));
        await sharp(Buffer.from(svgSello(pub, m.pub.acento, { cuadrado: true })), { density: 300 }).resize(180, 180).png().toFile(join(salida, 'apple-touch-icon.png'));
        await sharp(Buffer.from(svgOg(pub, m.pub.acento))).png({ compressionLevel: 9 }).toFile(join(salida, 'og.png'));
        const lineas = [
          `# _redirects — GENERADO por aula (src/integracion/recursos.mjs); no editar.`,
          `# Cada post del sitio Quarto de ${pub} lleva a su página nueva; los archivos del post (PDF, DOCX, figuras) también.`,
          // Netlify compara la regla con la ruta codificada (%C3%B3): una ruta vieja con tildes va también codificada.
          ...m.redirecciones.flatMap((r) => [...new Set([r.desde, encodeURI(r.desde)])].map((d) => `${d}*  ${r.hacia}:splat  301`)),
        ];
        await writeFile(join(salida, '_redirects'), lineas.join('\n') + '\n');
        await mkdir(join(AULA_DIR, '.cache'), { recursive: true });
        await writeFile(
          join(AULA_DIR, '.cache', `informe-${pub}.json`),
          JSON.stringify({ pub, totales: m.totales, recursos: m.recursos.length, miniaturas: m.miniaturas.length, redirecciones: m.redirecciones.length, avisos: m.avisos, anclasReparadas: m.anclasReparadas, sinResolver: m.sinResolver }, null, 2),
        );
        logger.info(`${m.recursos.length} recursos copiados, ${m.miniaturas.length} miniaturas, ${m.redirecciones.length} redirecciones; ${m.avisos.length} avisos de datos (.cache/informe-${pub}.json)`);
      },
    },
  };
}
