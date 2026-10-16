// Fotografía cuadro a cuadro un HTML de diseno/video/ que expone render(t) y
// DURACION. Corre en el contenedor backend de Tallermax (trae Chromium); lo
// lanza renderizar_video.sh, que después arma el MP4 con ffmpeg.
//
//   node renderizar_video.mjs <archivo.html> <carpeta-salida> [--fps 30] [--tiempos 1.5,6,12]
//
// Con --tiempos sólo saca esos instantes (para revisar sin generar todo).

import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';

const args = process.argv.slice(2);
const [html, salida] = args;
const opt = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const fps = Number(opt('--fps', 30));
const tiempos = opt('--tiempos', null);
mkdirSync(salida, { recursive: true });

const navegador = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none', '--allow-file-access-from-files'],
});
try {
  const p = await navegador.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const fallos = [];
  p.on('requestfailed', (r) => fallos.push(r.url()));
  p.on('pageerror', (e) => fallos.push(String(e)));
  await p.goto(`file://${html}`, { waitUntil: 'networkidle0' });
  await p.evaluate(async () => { await Promise.all([...document.fonts].map((f) => f.load())); });
  if (fallos.length) throw new Error(`No cargó: ${fallos.join(', ')}`);

  const duracion = await p.evaluate(() => window.DURACION);
  const lista = tiempos ? tiempos.split(',').map(Number) : Array.from({ length: Math.round(duracion * fps) }, (_, i) => i / fps);
  for (const [i, t] of lista.entries()) {
    await p.evaluate((x) => window.render(x), t);
    await p.screenshot({ path: `${salida}/${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
    if (i % 150 === 0) console.log(`cuadro ${i}/${lista.length}`);
  }
  console.log(`${lista.length} cuadros, ${duracion}s`);
} finally {
  await navegador.close();
}
