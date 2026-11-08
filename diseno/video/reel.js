// Motor de los reels: cada <section class="esc" data-dur="3.5"> es una escena a
// pantalla completa. Dentro, todo elemento con data-in="0.4" entra (aparece y
// sube) a esos segundos de empezada la escena y se queda hasta el final.
//
//   data-anim="escala" | "izq"   otra forma de entrar (por defecto, sube)
//   data-contar="143931"         cuenta en pesos hasta ese número
//   data-escribir="KLTR42"       se escribe a data-vel letras por segundo
//
// La FIRMA (logo + «Sistema para talleres mecánicos») se pone sola arriba y se
// ve desde el primer cuadro: quien ve tres segundos tiene que saber quién habla.
// Se apaga en la última escena, que ya trae el logo grande. Para un reel sin
// firma: <body data-sin-firma>.
//
// Expone window.render(t), window.DURACION y window.ESCENAS (inicio y duración
// de cada escena, en segundos) para renderizar_video.mjs.
(() => {
  const FUNDIDO = 0.35;
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const sale = (x) => 1 - Math.pow(1 - x, 3);
  let firma = null;
  if (!document.body.hasAttribute('data-sin-firma')) {
    firma = document.createElement('div');
    firma.className = 'firma';
    firma.innerHTML = '<svg viewBox="0 0 64 64"><path d="M32 6.5 L54.08 19.25 L54.08 44.75 L32 57.5 L9.92 44.75 L9.92 19.25 Z" fill="#4F46E5" stroke="#4F46E5" stroke-width="7" stroke-linejoin="round"/><path d="M21.1 20 H42.9 Q44.5 20 44.5 21.6 V25.4 Q44.5 27 42.9 27 H35.5 V43.9 Q35.5 45.5 33.9 45.5 H30.1 Q28.5 45.5 28.5 43.9 V27 H21.1 Q19.5 27 19.5 25.4 V21.6 Q19.5 20 21.1 20 Z" fill="#fff"/></svg><b>tallermax</b><span>Sistema para talleres mecánicos</span>';
    document.body.appendChild(firma);
  }
  const escenas = [...document.querySelectorAll('.esc')];
  // Con voz en off, renderizar_video.mjs pone en window.DURACIONES_VOZ lo que
  // necesita cada frase grabada: la escena dura eso si es más que su data-dur.
  const voz = window.DURACIONES_VOZ || [];
  let t0 = 0;
  escenas.forEach((e, i) => { e._inicio = t0; e._dur = Math.max(Number(e.dataset.dur), voz[i] || 0); t0 += e._dur; });
  const DURACION = t0;

  // Subtítulos de la voz en off: window.SUBTITULOS_VOZ trae, por escena, las
  // palabras de su frase con su tiempo desde que empieza a hablar, y la frase
  // empieza window.ENTRA_VOZ segundos después que la escena. Se muestran de a
  // pocas palabras, con la que se está diciendo en amarillo.
  const entraVoz = window.ENTRA_VOZ || 0;
  const grupos = [];
  (window.SUBTITULOS_VOZ || []).forEach((palabras, i) => {
    if (!escenas[i] || !palabras.length) return;
    const base = escenas[i]._inicio + entraVoz;
    let actual = [];
    palabras.forEach((w, k) => {
      actual.push({ p: w.p, a: base + w.a, b: base + w.b });
      const fin = /[.;:?!…»]$/.test(w.p), coma = /,$/.test(w.p) && actual.length >= 2;
      const corte = fin || coma || actual.length === 4 || k === palabras.length - 1;
      if (corte) { grupos.push(actual); actual = []; }
    });
  });
  grupos.forEach((g, k) => {
    g.desde = g[0].a;
    const sigue = grupos[k + 1];
    g.hasta = Math.min(g[g.length - 1].b + 0.35, sigue ? sigue[0].a : Infinity);
  });
  let subtitulo = null;
  if (grupos.length) {
    subtitulo = document.createElement('div');
    subtitulo.className = 'subtitulo';
    document.body.appendChild(subtitulo);
  }
  function pintarSubtitulo(t) {
    const g = grupos.find((x) => t >= x.desde && t < x.hasta);
    subtitulo.style.visibility = g ? 'visible' : 'hidden';
    if (!g) return;
    subtitulo.replaceChildren(...g.map((w) => {
      const s = document.createElement('span');
      s.textContent = w.p;
      if (t >= w.a && t < w.b + 0.05) s.className = 'ahora';
      return s;
    }));
  }

  const pesos = (n) => '$' + Math.round(n).toLocaleString('es-CL');

  function render(t) {
    escenas.forEach((e, i) => {
      const local = t - e._inicio;
      const entra = i === 0 ? 1 : clamp(local / FUNDIDO);
      const salir = i === escenas.length - 1 ? 0 : clamp((local - (e._dur - FUNDIDO)) / FUNDIDO);
      const vis = local >= -0.001 && local <= e._dur + 0.001 ? entra * (1 - salir) : 0;
      if (firma && i === escenas.length - 1) firma.style.opacity = 1 - (local >= 0 ? clamp(local / FUNDIDO) : 0);
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
  const renderEscenas = render;
  window.render = subtitulo ? (t) => { renderEscenas(t); pintarSubtitulo(t); } : render;
  window.DURACION = DURACION;
  window.ESCENAS = escenas.map((e) => ({ inicio: e._inicio, dur: e._dur }));
  render(0);
})();
