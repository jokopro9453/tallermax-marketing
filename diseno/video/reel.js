// Motor de los reels: cada <section class="esc" data-dur="3.5"> es una escena a
// pantalla completa. Dentro, todo elemento con data-in="0.4" entra (aparece y
// sube) a esos segundos de empezada la escena y se queda hasta el final.
//
//   data-anim="escala" | "izq"   otra forma de entrar (por defecto, sube)
//   data-contar="143931"         cuenta en pesos hasta ese número
//   data-escribir="KLTR42"       se escribe a data-vel letras por segundo
//
// Expone window.render(t) y window.DURACION para renderizar_video.mjs.
(() => {
  const FUNDIDO = 0.35;
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const sale = (x) => 1 - Math.pow(1 - x, 3);
  const escenas = [...document.querySelectorAll('.esc')];
  let t0 = 0;
  for (const e of escenas) { e._inicio = t0; e._dur = Number(e.dataset.dur); t0 += e._dur; }
  const DURACION = t0;
  const pesos = (n) => '$' + Math.round(n).toLocaleString('es-CL');

  function render(t) {
    escenas.forEach((e, i) => {
      const local = t - e._inicio;
      const entra = i === 0 ? 1 : clamp(local / FUNDIDO);
      const salir = i === escenas.length - 1 ? 0 : clamp((local - (e._dur - FUNDIDO)) / FUNDIDO);
      const vis = local >= -0.001 && local <= e._dur + 0.001 ? entra * (1 - salir) : 0;
      e.style.opacity = vis;
      e.style.visibility = vis > 0.001 ? 'visible' : 'hidden';
      if (vis <= 0.001) return;
      e.querySelectorAll('[data-in]').forEach((el) => {
        const p = sale(clamp((local - Number(el.dataset.in)) / 0.5));
        const anim = el.dataset.anim;
        el.style.opacity = p;
        el.style.transform = anim === 'escala' ? `scale(${0.85 + 0.15 * p})` : anim === 'izq' ? `translateX(${(1 - p) * -60}px)` : `translateY(${(1 - p) * 60}px)`;
      });
      e.querySelectorAll('[data-contar]').forEach((el) => {
        const desde = Number(el.dataset.desde || 0.6);
        el.textContent = pesos(Number(el.dataset.contar) * sale(clamp((local - desde) / 1.2)));
      });
      e.querySelectorAll('[data-escribir]').forEach((el) => {
        const txt = el.dataset.escribir, vel = Number(el.dataset.vel || 5), desde = Number(el.dataset.desde || 0.5);
        el.textContent = txt.slice(0, Math.floor(clamp((local - desde) * vel, 0, txt.length)));
      });
      e.querySelectorAll('[data-pulso]').forEach((el) => {
        el.style.transform = `scale(${1 + 0.03 * Math.sin(Math.max(0, local - 1) * 5)})`;
      });
    });
  }
  window.render = render;
  window.DURACION = DURACION;
  render(0);
})();
