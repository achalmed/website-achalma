// astro.config.mjs — un mismo proyecto construye el sitio de un pub: PUB=methodica npm run build → dist/methodica/
import { defineConfig } from 'astro/config';
import { registroPubs } from './src/lib/fuentes.mjs';
import recursos from './src/integracion/recursos.mjs';
import rutas from './src/integracion/rutas.mjs';

const pub = process.env.PUB;
const pubs = registroPubs().pubs;
const registro = pubs.find((p) => p.carpeta === pub);
if (!registro) {
  throw new Error(`Falta PUB o no es un pub de web/_pubs/pubs.yml. Uso: PUB=methodica npm run build. Válidos: ${pubs.map((p) => p.carpeta).join(', ')}`);
}

export default defineConfig({
  site: registro.url,
  outDir: `./dist/${pub}`,
  cacheDir: `./.cache/astro-${pub}`,
  trailingSlash: 'always',
  // CSS en línea: la hoja (unos 10 KB) deja de bloquear la primera pintura en un móvil lento (decisiones §1.19).
  build: { format: 'directory', inlineStylesheets: 'always' },
  compressHTML: true,
  devToolbar: { enabled: false },
  integrations: [rutas(), recursos(pub)],
});
