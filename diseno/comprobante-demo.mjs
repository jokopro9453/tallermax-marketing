// Un comprobante REAL de Tallermax —sale de la misma función que imprime los de
// verdad, backend/src/modules/ordenes/plantilla-pdf.ts— con datos de ejemplo
// limpios: taller, cliente y patente inventados. No toca la base de datos.
//
// Corre en el contenedor backend con tsx, para usar el código fuente y no una
// copia compilada que puede estar atrasada:
//   node --import tsx comprobante-demo.mjs <salida.png>

import puppeteer from 'puppeteer-core';

const { plantillaOrden } = await import('/app/src/modules/ordenes/plantilla-pdf.ts');

const item = (n, tipo, descripcion, precioUnitario, cantidad) =>
  ({ id: `i${n}`, tipo, repuestoId: null, descripcion, precioUnitario, cantidad, subtotal: precioUnitario * cantidad });
const items = [
  item(1, 'MANO_OBRA', 'Cambio de pastillas de freno delanteras', 35000, 1),
  item(2, 'MANO_OBRA', 'Alineación y balanceo', 25000, 1),
  item(3, 'REPUESTO', 'Pastillas de freno delanteras', 28990, 1),
  item(4, 'REPUESTO', 'Aceite 10W-40 (litro)', 7990, 4),
];
const subtotal = items.reduce((s, i) => s + i.subtotal, 0);

const orden = {
  id: '7c41e0a2-0000-4000-8000-000000000000',
  vehiculoId: 'v1', fecha: '2026-10-20T12:42:00.000Z', kilometraje: 84310, abono: 0,
  observaciones: 'Ruido al frenar. Se revisa también el nivel de líquido de frenos.',
  estado: 'TERMINADA', terminadaAt: '2026-10-20T19:10:00.000Z',
  constanciaEnviadaAt: null, entregaAvisadaAt: null,
  subtotal, totalNeto: subtotal, editable: false,
  encargado: { id: 'u1', nombre: 'Pedro Soto' }, version: 1, items,
  vehiculo: { id: 'v1', patente: 'KLTR42', marca: 'Toyota', modelo: 'Hilux', anio: 2019 },
  cliente: { id: 'c1', rut: '12345678-5', nombre: 'Juan Pérez' },
};
const taller = { nombre: 'Taller de Ejemplo', logo: null, rut: null, direccion: null, telefono: null, correo: null };

const [salida] = process.argv.slice(2);
const navegador = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'],
});
try {
  const pagina = await navegador.newPage();
  await pagina.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2 });
  await pagina.setContent(plantillaOrden(orden, taller), { waitUntil: 'networkidle0' });
  await pagina.screenshot({ path: salida, fullPage: false });
  console.log(`comprobante: ${salida}`);
} finally {
  await navegador.close();
}
