// Saca la firma de Tallermax como PNG transparente de 1080 de ancho, para
// ponerla encima de los videos grabados (editar_toma.py). Usa el mismo CSS que
// los reels animados, así que se ve igual en los dos.
//
//   node capas.mjs <firma.html> <salida.png>

import puppeteer from 'puppeteer-core';

const [html, salida] = process.argv.slice(2);
const navegador = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none', '--allow-file-access-from-files'],
});
try {
  const p = await navegador.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`file://${html}`, { waitUntil: 'networkidle0' });
  await p.evaluate(async () => { await Promise.all([...document.fonts].map((f) => f.load())); });
  // Toda la franja de arriba, con la firma en su lugar (top: 290px en reel.css).
  await p.screenshot({ path: salida, omitBackground: true, clip: { x: 0, y: 0, width: 1080, height: 420 } });
} finally {
  await navegador.close();
}
