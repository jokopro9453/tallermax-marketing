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

  // Que ninguna escena se meta debajo de la firma ni baje a la franja donde
  // Instagram pone el nombre y el texto. Se mide al final de cada escena, con
  // todo ya entrado. Sólo los bloques de primer nivel: lo de dentro lo recortan ellos.
  const choques = await p.evaluate(() => {
    const firma = document.querySelector('.firma');
    const arriba = firma ? firma.getBoundingClientRect().bottom + 16 : 280;
    const escenas = [...document.querySelectorAll('.esc')];
    const out = [];
    escenas.forEach((e, i) => {
      if (e._inicio === undefined) return;
      window.render(e._inicio + e._dur - 0.4);
      for (const el of e.children) {
        const r = el.getBoundingClientRect();
        if (!r.height) continue;
        const quien = `escena ${i + 1}, «${el.textContent.trim().replace(/\s+/g, ' ').slice(0, 32)}»`;
        if (firma && i < escenas.length - 1 && r.top < arriba) out.push(`${quien} sube hasta y=${Math.round(r.top)} y choca con la firma`);
        if (r.bottom > 1920 - 400) out.push(`${quien} baja hasta y=${Math.round(r.bottom)}`);
      }
    });
    return out;
  });
  if (choques.length) throw new Error(`Se sale de la zona segura:\n  ${choques.join('\n  ')}`);

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
