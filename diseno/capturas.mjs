// Capturas REALES de Tallermax para las piezas, con la cuenta del taller de
// pruebas (datos ficticios). Corre dentro del contenedor backend, que ve la
// aplicación en http://frontend:3001. Lo lanza capturas.sh.
//
//   node capturas.mjs <carpeta-salida>
//
// Necesita TALLER_EMAIL y TALLER_PASSWORD en el entorno. Sólo navega y
// fotografía: nunca envía un formulario salvo el de entrar.

import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';

const BASE = process.env.WEB ?? 'http://frontend:3001';
const [salida] = process.argv.slice(2);
const { TALLER_EMAIL: email, TALLER_PASSWORD: clave } = process.env;
if (!salida || !email || !clave) {
  console.error('Uso: TALLER_EMAIL=… TALLER_PASSWORD=… node capturas.mjs <carpeta>');
  process.exit(2);
}
mkdirSync(salida, { recursive: true });

const navegador = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'],
});

const ir = async (pagina, ruta) => {
  await pagina.goto(BASE + ruta, { waitUntil: 'networkidle0', timeout: 120_000 });
  await pagina.evaluate(() => document.fonts.ready);
};

try {
  const pagina = await navegador.newPage();
  await pagina.setViewport({ width: 1280, height: 800, deviceScaleFactor: 2 });
  await ir(pagina, '/login');
  await pagina.type('input[name="email"]', email);
  await pagina.type('input[name="password"]', clave);
  await Promise.all([
    pagina.waitForNavigation({ waitUntil: 'networkidle0', timeout: 120_000 }),
    pagina.$eval('input[name="password"]', (el) => el.form.requestSubmit()),
  ]);
  if (new URL(pagina.url()).pathname.startsWith('/login')) throw new Error('No se pudo entrar: revisa las credenciales.');

  // La primera orden del listado, para su detalle.
  await ir(pagina, '/ordenes');
  const orden = await pagina.$$eval('a[href^="/ordenes/"]', (as) =>
    as.map((a) => a.getAttribute('href')).find((h) => /^\/ordenes\/\d+$/.test(h)));

  const tomas = [
    ['escritorio-portada', '/', 1280, 800],
    ['escritorio-ordenes', '/ordenes', 1280, 800],
    ['escritorio-orden', orden, 1280, 800],
    ['escritorio-metricas', '/metricas', 1280, 800],
    ['telefono-portada', '/', 390, 844],
    ['telefono-orden', orden, 390, 844],
    ['telefono-vehiculos', '/vehiculos', 390, 844],
  ];
  for (const [nombre, ruta, ancho, alto] of tomas) {
    if (!ruta) { console.log(`${nombre}: sin ruta, se omite`); continue; }
    await pagina.setViewport({ width: ancho, height: alto, deviceScaleFactor: 2 });
    await ir(pagina, ruta);
    await pagina.screenshot({ path: `${salida}/${nombre}.png` });
    console.log(`${nombre}: ${ruta}`);
  }
} finally {
  await navegador.close();
}
