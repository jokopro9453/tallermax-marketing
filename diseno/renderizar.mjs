// Convierte cada <section class="slide"> de un HTML de diseno/ en un JPEG de
// 1080 × 1350. Corre dentro del contenedor del backend de Tallermax, que trae
// Chromium; lo lanza renderizar.sh.
//
//   node renderizar.mjs <carpeta> <archivo>:<id-de-pieza> [...]
//
// Las imágenes quedan en <carpeta>/salida/<id-de-pieza>/01.jpg, 02.jpg…

import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';

const [carpeta, ...encargos] = process.argv.slice(2);
if (!carpeta || encargos.length === 0) {
  console.error('Uso: node renderizar.mjs <carpeta> <archivo>:<id-de-pieza> [...]');
  process.exit(2);
}

const navegador = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none', '--allow-file-access-from-files'],
});

try {
  const pagina = await navegador.newPage();
  await pagina.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
  const errores = [];
  pagina.on('requestfailed', (r) => errores.push(`${r.url()}: ${r.failure()?.errorText}`));

  for (const encargo of encargos) {
    const [archivo, id] = encargo.split(':');
    await pagina.goto(`file://${carpeta}/${archivo}.html`, { waitUntil: 'networkidle0' });
    await pagina.evaluate(() => document.fonts.ready);

    // Si una tipografía no cargó, Chromium usa otra sin decir nada y la pieza
    // sale con la letra equivocada. Mejor fallar.
    const faltan = await pagina.evaluate(() =>
      ['800 100px Archivo', '400 40px Inter', '500 26px JBM'].filter((f) => !document.fonts.check(f)));
    if (faltan.length || errores.length) {
      throw new Error(`No cargó: ${[...faltan, ...errores].join(', ')}`);
    }

    // Lo que se sale de su imagen se recorta sin avisar; se comprueba aquí.
    const desbordes = await pagina.evaluate(() => [...document.querySelectorAll('section.slide')].flatMap((s, i) => {
      const caja = s.getBoundingClientRect();
      return [...s.querySelectorAll('h1,h2,h3,p,li,dl,.caras,.correo,.pantalla')]
        .filter((el) => el.getBoundingClientRect().bottom > caja.bottom - 120 && !el.closest('.pie'))
        .map((el) => `imagen ${i + 1}: «${el.textContent.trim().slice(0, 40)}» invade el pie`);
    }));
    if (desbordes.length) throw new Error(desbordes.join('\n'));

    const laminas = await pagina.$$('section.slide');
    const destino = `${carpeta}/salida/${id}`;
    mkdirSync(destino, { recursive: true });
    for (const [i, lamina] of laminas.entries()) {
      await lamina.screenshot({ path: `${destino}/${String(i + 1).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 90 });
    }
    console.log(`${id}: ${laminas.length} imágenes`);
  }
} finally {
  await navegador.close();
}
