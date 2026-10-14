// Exporta el logo a PNG y la hoja de conceptos a JPEG. Corre en el contenedor
// backend (trae Chromium). Lo lanza exportar.sh.
//
//   node exportar.mjs <carpeta diseno/logo>

import puppeteer from 'puppeteer-core';
import { mkdirSync, readFileSync } from 'node:fs';

const [dir] = process.argv.slice(2);
const png = `${dir}/png`;
mkdirSync(png, { recursive: true });

const navegador = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files'],
});

// Un SVG centrado en un lienzo cuadrado. `fondo` null = transparente.
async function cuadrado(pagina, svg, lado, destino, { fondo = null, margen = 0 } = {}) {
  const contenido = readFileSync(`${dir}/svg/${svg}`, 'utf8');
  const interior = lado - 2 * margen;
  await pagina.setViewport({ width: lado, height: lado, deviceScaleFactor: 1 });
  await pagina.setContent(`<html><body style="margin:0;background:${fondo ?? 'transparent'};display:grid;place-items:center;width:${lado}px;height:${lado}px">
    <div style="width:${interior}px;height:${interior}px">${contenido.replace('<svg ', '<svg style="width:100%;height:100%" ')}</div></body></html>`);
  await pagina.screenshot({ path: `${png}/${destino}`, omitBackground: fondo === null });
}

try {
  const p = await navegador.newPage();
  for (const lado of [16, 32, 48, 180, 192, 512, 1024]) {
    await cuadrado(p, 'tallermax-icono.svg', lado, `tallermax-icono-${lado}.png`);
  }
  // Foto de perfil: Instagram la recorta en círculo, así que la marca va con aire.
  await cuadrado(p, 'tallermax-icono.svg', 1080, 'perfil-instagram.png', { fondo: '#121318', margen: 250 });

  // El logo horizontal a 4x, transparente, para documentos y la landing.
  for (const v of ['tallermax-horizontal', 'tallermax-horizontal-sobre-oscuro', 'tallermax-horizontal-negro', 'tallermax-horizontal-blanco']) {
    const contenido = readFileSync(`${dir}/svg/${v}.svg`, 'utf8');
    const [, w, h] = contenido.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
    await p.setViewport({ width: Math.ceil(w), height: Math.ceil(h), deviceScaleFactor: 4 });
    await p.setContent(`<html><body style="margin:0;background:transparent">${contenido}</body></html>`);
    await p.screenshot({ path: `${png}/${v}@4x.png`, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }

  await p.setViewport({ width: 1800, height: 1000, deviceScaleFactor: 1 });
  await p.goto(`file://${dir}/hoja.html`, { waitUntil: 'networkidle0' });
  await p.evaluate(() => document.fonts.ready);
  const hoja = await p.$('.hoja');
  await hoja.screenshot({ path: `${dir}/hoja-conceptos.jpg`, type: 'jpeg', quality: 92 });
  console.log('listo');
} finally {
  await navegador.close();
}
