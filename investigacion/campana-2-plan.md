# Campaña 2: qué aprendimos de la primera y cómo armar la siguiente

Investigación del 13 de noviembre de 2026, el día en que terminó la campaña
«TMX · Talleres fundadores». Junta tres cosas: los números de esa campaña, las
guías de `.claude/skills/ads` y `.claude/skills/ad-creative`, y lo que se
encontró en la web sobre anuncios de Meta en 2026.

Como en las otras investigaciones, separa **lo que se midió**, **lo que dicen
las fuentes** (casi todas son proveedores que venden algo: sus cifras se citan
como lo que dicen, no como hechos) y **lo que deducimos** (hipótesis que la
campaña 2 tiene que confirmar).

> **Decidido el 13 de noviembre:** $70.000 con IVA y partida el lunes 30 de
> noviembre. La configuración exacta, los textos y la lista de pendientes están
> en `anuncios/campana-2.md`. De las 2 conversaciones de la campaña 1, una era
> un revendedor de autos (probó y no le servía) y la otra dejó de contestar:
> **ninguna fue de un taller mecánico.**

---

## 1. Resumen

1. **La campaña 1 costó $27.481 y trajo 2 conversaciones: $13.740 cada una.**
   Es caro. Para que los anuncios se paguen, cada conversación debería costar
   **$7.500 o menos** (la cuenta está en la sección 5).
2. **El anuncio barato de mostrar no fue el problema.** Mostrar el anuncio mil
   veces costó unos $1.700, que es poco. Lo que falló fue lo que vino después:
   **sólo 4 de cada 1.000 personas tocaron el anuncio, y sólo 3 de cada 100 que
   tocaron escribieron.**
3. **Hay dos fugas, y cada una tiene su arreglo:**
   * *Pocos se detienen* → los anuncios eran texto animado, sin una persona ni
     un taller de verdad. Se parecen a publicidad, y la gente la salta. Lo que
     más recomiendan las fuentes para una marca nueva es **el fundador hablando
     a la cámara**.
   * *Casi nadie escribe* → el chat se abre y la persona no sabe qué decir, o se
     arrepiente. Se arregla con **preguntas listas para tocar**, una bienvenida
     que repita la oferta del anuncio y **respuesta en minutos**.
4. **Con este presupuesto, Meta no alcanza a aprender.** Meta necesita unas 50
   conversaciones a la semana por conjunto para optimizar; tuvimos 2 en dos
   semanas. No se arregla con trucos de configuración: se arregla con **menos
   anuncios, mejores, y un embudo que no pierda gente**.
5. **Pausamos dos anuncios demasiado pronto.** Con el costo que tuvo el
   «ganador», gastar $4.000 sin conversaciones pasa 6 de cada 10 veces por
   pura mala suerte. No sabemos si «Evidencia por correo» y «Tu sistema hoy»
   eran malos. En la campaña 2 los anuncios se juzgan primero por **cuánta
   gente los toca**, que se sabe en pocos días, y no por conversaciones.
6. **Los anuncios no pueden ser el canal principal todavía.** En las 4 comunas
   hay cientos de miles de personas de 28 a 60 años y, como mucho, uno o dos
   mil dueños de taller. Los primeros clientes de un software como éste casi
   siempre salen de **contacto directo del fundador**: visitas, conocidos,
   recomendaciones. Los anuncios apoyan eso; no lo reemplazan.

---

## 2. Lo que se midió en la campaña 1

Del 1 al 13 de noviembre (el piloto leyó la cuenta cada día a las 09:15).

| | Gasto | Veces mostrado | Personas | Toques | Conversaciones |
|---|---|---|---|---|---|
| Ingreso con fotos | $18.260 | 12.386 | 7.238 | 51 | **2** |
| Evidencia por correo (pausado el 5–6 nov) | $5.069 | 2.122 | 1.670 | 11 | 0 |
| Tu sistema hoy (pausado el 7 nov) | $4.152 | 1.750 | 1.347 | 6 | 0 |
| **Total** | **$27.481** | 16.258 | — | **68** | **2** |

De ahí salen cuatro números:

| Qué mide | Campaña 1 | Referencia | Lectura |
|---|---|---|---|
| Costo por mil veces mostrado | **$1.690** | — | Barato. La subasta no es el problema. |
| Toques por cada 100 veces mostrado | **0,42 %** | 1,0–1,5 % es lo normal en B2B; menos de 0,8 % es mala señal (guía `meta-decision-system`) | **Malo.** El anuncio no detiene a la gente correcta. |
| Conversaciones por cada 100 toques | **2,9 %** | Los proveedores hablan de 25 % o más de respuesta al primer mensaje | **Muy malo**, con una salvedad: «toques» incluye «me gusta» y visitas al perfil, no sólo el botón de WhatsApp. |
| Veces que cada persona vio «Ingreso con fotos» | 1,7 | Hasta 2,5 es sano | No hubo saturación. |

Dos hechos más:

* **Las 2 conversaciones llegaron en la primera semana** (con $5.427 gastados
  en «Ingreso con fotos»). En la segunda semana ese anuncio gastó otros $12.800
  y no trajo ninguna. Con tan pocos casos no se puede saber si se agotó o si fue
  azar.
* **La cuenta de Instagram tiene 12 seguidores** y las 20 publicaciones juntan
  entre 2 y 8 «me gusta» cada una, sin comentarios. El contenido orgánico
  todavía no llega a nadie por sí solo: sirve como vitrina cuando alguien entra
  al perfil desde un anuncio o desde un WhatsApp, no como canal.

**Lo que falta saber (y sólo Joaquín lo sabe):** qué pasó con esas 2
conversaciones. ¿Alguna llegó a la prueba de 7 días? ¿Alguna pagó? Sin eso, el
único costo que conocemos es el de la conversación, que es el que menos importa.

---

## 3. Lo que dicen las fuentes

### Cómo funciona Meta en 2026

* **El anuncio es la segmentación.** Meta retiró la mayoría de los intereses en
  enero de 2026 ([Jon Loomer](https://www.jonloomer.com/qvt/detailed-targeting-announcement/),
  [Social Media Today](https://www.socialmediatoday.com/news/meta-removes-more-detailed-ad-targeting-options-facebook-instagram/757856/)).
  Lo que queda es público amplio y que el anuncio mismo llame a su gente: la
  palabra «taller mecánico» en el primer segundo y en el titular funciona como
  filtro para la persona y como señal para el algoritmo (guía
  `meta-andromeda-playbook`).
* **Los anuncios muy parecidos cuentan como uno solo.** Meta agrupa los que
  juzga similares y les reparte menos. Tres reels de texto animado con el mismo
  estilo son, para Meta, casi el mismo anuncio. La variedad tiene que ser de
  **formato y de idea**, no de redacción.
* **Presupuesto chico: todo junto.** Las fuentes coinciden en un solo conjunto
  de anuncios y pocos anuncios, porque repartir es la forma más rápida de que
  ninguno aprenda ([Stackmatix](https://www.stackmatix.com/blog/how-much-to-run-ads-on-facebook),
  [Vizup](https://www.tryvizup.com/blog/meta-ads-minimum-budget-requirements-2026)).
  La guía `meta-decision-system` da la cuenta: los anuncios activos no deberían
  ser más que *(presupuesto diario × 14) ÷ (2 × costo objetivo)*.
* **No tocar lo que corre.** Editar un anuncio o cambiar el presupuesto más de
  un 20 % reinicia el aprendizaje. Lo nuevo se agrega al lado.
* **El texto largo ayuda.** En 2026 los textos largos le dan a Meta más
  contexto para decidir a quién mostrarle el anuncio (guía
  `meta-andromeda-playbook`; es la opinión de quienes la escribieron, no un dato
  de Meta).

### Qué formato hacer

La guía `meta-creative-formats` ordena 51 formatos según si sirven para llegar
a gente nueva o sólo para convencer a quien ya nos vio:

* **Arriba de todo, el contenido del fundador:** «el primer ganador confiable a
  cualquier nivel de producción. Cuenta por qué lo hiciste». Una agencia reporta
  que los anuncios con el fundador le ganan al contenido de marca en costo y en
  toques ([MHI](https://mhigrowthengine.com/blog/founder-led-vs-brand-content-2026/);
  son datos de tiendas en línea, no de software para talleres).
* **Las imágenes fijas baratas suelen ganarle al video pulido**, y se hacen en
  una hora. La regla que proponen: validar la idea como imagen y recién después
  hacer el video ([Stackmatix](https://stackmatix.com/blog/facebook-video-vs-image-ads-performance)).
* **Los carruseles están casi al fondo** como anuncio («rara vez valen el
  esfuerzo»). Sirven en el perfil, no para pagar por ellos.
* **Las fuentes se contradicen sobre cuánto pulir.** Unas dicen que lo crudo
  gana; otras, que los subtítulos y la edición suben el rendimiento. El estudio
  más grande (550.000 anuncios, [Motion](https://motionapp.com/library/research/creative-benchmarks-2026/trends-are-not-universal))
  concluye que **no hay formato universal y que sólo 1 de cada 20 anuncios
  gana de verdad**. Hay que probar en la cuenta propia.

### Anuncios que llevan a WhatsApp

* **Donde más gente se pierde es justo después del toque:** abren el chat, no
  saben qué decir y lo cierran ([Infobip](https://www.infobip.com/blog/click-to-whatsapp-ads),
  [eGrow](https://www.egrow.com/en/blog/click-to-whatsapp-ads-the-complete-guide-to-driving-sales-from-meta-to-whatsapp-2026)).
* **Lo que recomiendan casi todos:**
  1. **Preguntas listas para tocar** en vez de un mensaje que hay que enviar.
     Ojo: una guía dice que se puede usar el mensaje escrito *o* las preguntas,
     no las dos cosas. No está confirmado con Meta; se ve al crear el anuncio.
  2. Que la bienvenida **repita la oferta del anuncio** (no «¿en qué te
     ayudo?»).
  3. **Responder en minutos.** Los mensajes a quien llega de un anuncio son
     gratis durante 72 horas ([Mercately](https://blog.mercately.com/nuevos-precios-whatsapp-api-octubre-2026/));
     con la app gratuita de WhatsApp Business, como la que usa Joaquín, no hay
     cobro por mensaje.
* **Formulario o WhatsApp:** las fuentes no se ponen de acuerdo en cuál sale
  más barato ([Wati](https://www.wati.io/en/blog/click-to-whatsapp-ads-vs-lead-form-ads-roas/),
  [Stackmatix](https://www.stackmatix.com/blog/meta-ads-whatsapp-lead-generation)).
  Coinciden en que el formulario trae más contactos y de peor calidad, y en que
  hay que comparar por **cliente**, no por contacto. Si se usa formulario, que
  sea de «mayor intención» y con una o dos preguntas que filtren (guía
  `meta-decision-system`).

### Cómo se consiguen los primeros clientes de un software

No hay estudios sobre vender software a talleres en Chile. Lo que hay son
encuestas de fundadores: la mayoría consiguió sus primeros 10 clientes **por
contacto directo y por su red de conocidos**, y los anuncios funcionaron después
de tener el mensaje probado y algún cliente que mostrar
([Saas Hero](https://www.saashero.net/strategy/early-b2b-saas-marketing-strategy/),
[Cut the SaaS](https://cut-the-saas.com/guides/first-100-customers)). Calza con
lo que ya sabíamos del rubro: el mecánico adopta la herramienta «cuando la ve
funcionando» (Pitz, en `competencia-y-por-que-tallermax.md`).

### Lo que se buscó y no se encontró

* Cuánto cuesta una conversación de WhatsApp o mostrar mil anuncios **en
  Chile**. Nuestro propio dato ($1.690 por mil) es mejor que cualquier fuente.
* Si rinde más Facebook o Instagram para **dueños de negocio de más de 40
  años**. Se ve en el Administrador de anuncios, en el desglose por ubicación.
* Cuánto cuesta el clic de «software taller mecánico» en Google en Chile. Se ve
  gratis en el Planificador de palabras clave.
* Si sigue existiendo algún interés o comportamiento de «dueño de negocio».
  Algunas cuentas tienen una opción nueva, «Describe tu público»; hay que
  mirar si la nuestra la tiene.

---

## 4. Por qué pasó lo que pasó (lo que deducimos)

1. **Los tres anuncios eran el mismo anuncio.** Mismo fondo, misma tipografía,
   texto animado, sin voz y sin personas. Meta no tuvo tres ideas para probar:
   tuvo una. Y esa una se ve como publicidad desde el primer cuadro.
2. **El gancho hablaba del sistema antes que de la persona.** «¿Te ha pasado?»
   sí funcionó (es el del anuncio que trajo las 2 conversaciones). «Tu sistema
   hoy» y «La evidencia le llega a su correo» parten desde el producto.
3. **El salto a WhatsApp es grande para alguien que nos vio 20 segundos.**
   Escribirle a un desconocido es un compromiso. Y Meta tenía encendidas sus
   propias preguntas generadas con IA, que no elegimos nosotros.
4. **El anuncio le llegó sobre todo a gente que no tiene taller.** Con 7.000
   personas alcanzadas y uno o dos mil dueños de taller en toda la zona, la
   mayoría de lo gastado se fue en mostrarlo a quien no le sirve. No hay forma
   de evitarlo del todo; se reduce con un anuncio que diga «taller mecánico» de
   entrada y, sobre todo, **no dependiendo sólo de los anuncios**.
5. **Nadie nos conoce todavía.** Sin un solo taller que diga «yo lo uso», el
   anuncio pide confianza a cambio de nada. El primer testimonio vale más que
   cualquier cambio de configuración.

---

## 5. La meta: cuánto puede costar una conversación

Un taller paga $30.000 + IVA al mes. Si se queda un año, son $360.000.

| Supuesto | Valor | De dónde sale |
|---|---|---|
| Lo máximo que conviene gastar por cliente | **$60.000** | Dos meses de lo que paga. Decisión conservadora. |
| De cada 2 conversaciones, 1 llega a la prueba | 50 % | **Supuesto.** Hay que medirlo. |
| De cada 4 pruebas, 1 paga | 25 % | **Supuesto.** Las fuentes dan 10–20 % para software nuevo; la puesta en marcha en persona debería subirlo. |
| **Costo objetivo por conversación** | **$7.500** | $60.000 × 25 % × 50 % |

La campaña 1 estuvo en **$13.740**: casi el doble. Si el porcentaje de toques
sube de 0,42 % a 1 % y de cada 100 toques escriben 10 en vez de 3, la
conversación baja a cerca de **$1.700**. No hace falta tanto: basta con
arreglar bien una de las dos fugas.

---

## 6. El plan de la campaña 2

### Antes de gastar un peso (2 semanas de preparación)

Cuatro condiciones. Si falta una, se espera.

1. **Un video de Joaquín hablando a la cámara**, grabado con el celular en un
   taller o frente a un auto (30–40 segundos). Es el formato que más recomiendan
   las fuentes y el único que no hemos probado. Guion en la sección 7.
2. **Los reels con voz y subtítulos** ya guionados: «Ingreso con fotos» y «El
   rayón de $80.000» (`guiones/voz-en-off.md`).
3. **El WhatsApp probado de punta a punta.** Joaquín toca la vista previa del
   anuncio en su propio teléfono y comprueba: que abre WhatsApp Business, qué
   se ve, que la bienvenida automática repite la oferta y que las respuestas
   rápidas están cargadas (`guiones/whatsapp-ventas.md`).
4. **Algo real que mostrar:** una foto o una frase de un taller que lo esté
   probando (aunque sea el primero), o un video de la pantalla del teléfono
   registrando un auto de verdad. Sin inventar nada.

### La estructura

| | |
|---|---|
| Campañas | **Una sola**, `TMX · Rayón` (el prefijo `TMX` lo necesita el piloto) |
| Objetivo | Interacción → WhatsApp → maximizar conversaciones. Es lo que ya funciona técnicamente; lo que cambia son los anuncios y el chat. |
| Conjuntos | **Uno.** Las 4 comunas +17 km, 28–60 años, sin intereses, ubicaciones automáticas. |
| Presupuesto | Total, con fecha de término. **Lo decide Joaquín** (ver abajo). |
| Horario | Sólo cuando Joaquín puede contestar en minutos. Si no puede a las 13:00, ese bloque se saca. |
| Mensaje | **Preguntas elegidas por nosotros**, no las de IA de Meta: «¿Cuánto cuesta?», «¿Cómo es la prueba gratis?», «Quiero probarlo en mi taller». |
| Anuncios | **Tres, de tres formatos distintos**, con la misma idea (el rayón): |

**Los tres anuncios**

| # | Formato | Primer segundo | Por qué |
|---|---|---|---|
| A | **Joaquín a la cámara** | «Si tienes un taller mecánico en Quilpué, Villa Alemana, Viña o Valparaíso, mira esto.» | El formato mejor rankeado para una marca nueva. Nombra al público y la zona. |
| B | **Reel «El rayón de $80.000»** con su voz y subtítulos | «Ochenta mil pesos. Eso cuesta repintar una puerta que tú no rayaste.» | La cifra primero. Reutiliza la idea que sí trajo conversaciones. |
| C | **Imagen fija** | Titular: «Taller mecánico: ¿y si el cliente dice que el rayón no estaba?» | Barata, se hace en una hora y las imágenes suelen ganar en toques. |

Los tres llevan **texto largo** que empieza con «Para talleres mecánicos de…»,
cuenta el reclamo del rayón, explica la prueba de 7 días armada con su logo y
termina con el precio de fundador.

**Presupuesto: dos opciones**

| | Gasto en anuncios | Con IVA | Al día (18 días con horario) | Anuncios que puede sostener |
|---|---|---|---|---|
| **Igual que la campaña 1** | $29.400 | $35.000 | $1.630 | 2 (A y B) |
| **El doble** | $58.800 | $70.000 | $3.270 | 3 (A, B y C) |

La cuenta de la guía: *anuncios = (gasto diario × 14) ÷ (2 × $7.500)*. Con
$1.630 al día salen 1,5: alcanza para dos anuncios apenas. No se recomienda
gastar más de $70.000 hasta que algún anuncio demuestre un costo por
conversación bajo $7.500.

### Cómo se decide durante la campaña

El piloto sigue leyendo todos los días, pero con reglas nuevas:

1. **Días 1–4: no se toca nada.**
2. **Día 5: primera lectura, por toques.** Un anuncio con menos de 0,5 % de
   toques después de 1.500 veces mostrado no está deteniendo a nadie: se
   reemplaza por otro gancho. Esto se sabe con $2.500 gastados, no con $15.000.
3. **Conversaciones: se juzga recién con $15.000 gastados en ese anuncio** (dos
   veces el costo objetivo). Antes de eso, cero conversaciones no prueba nada.
4. **Nunca se pausa sin tener el reemplazo listo.** El reemplazo es otro gancho
   de la misma idea, no una edición del anuncio que ya corre.
5. **Freno general:** si la campaña gasta $22.500 (tres veces el objetivo) sin
   ninguna conversación, se pausa entera y se revisa el chat antes que los
   anuncios.

### Qué se mide (y dónde)

| Qué | Dónde | Quién |
|---|---|---|
| Toques y costo por anuncio | Administrador de anuncios | El piloto, cada día |
| Conversaciones | Administrador de anuncios | El piloto |
| **De cada conversación: ¿tenía taller? ¿pidió la prueba? ¿pagó?** | Página de prospectos | **Joaquín**, al cerrar cada chat |
| Por dónde llegó | Primera pregunta: «¿Dónde nos viste?» | Joaquín |

La tercera fila es la que decide si hay campaña 3.

### Lo que va en paralelo y no cuesta plata

Es lo que con más probabilidad trae los primeros clientes:

1. **Visitar 5 talleres por semana** de la lista de prospectos, con el teléfono
   en la mano: registrar un auto con fotos delante del dueño. Dos minutos.
2. **Pedirle a cada persona que lo prueba que nos presente a otro taller.** Un
   mes gratis por cada taller que llegue recomendado y se quede.
3. **El primer testimonio.** Una foto del taller y una frase con nombre. Entra
   al anuncio C y a la bienvenida del WhatsApp apenas exista.
4. **Mensajes directos y grupos de Facebook** (`guiones/difusion-personal.md`).
5. **Mirar la Biblioteca de anuncios de Meta** (es gratis, con la sesión
   iniciada): buscar «Bujía», «Mi Taller», «Appli-Car» y «GestionCar» y anotar
   qué anuncios llevan más de un mes activos. Si siguen activos, les funcionan.

### Lo que NO se hace en la campaña 2

* Más de un conjunto de anuncios, o probar públicos. El presupuesto no da.
* Carruseles como anuncio.
* Formulario en vez de WhatsApp. Queda como **plan B**: si con las preguntas
  listas y Joaquín respondiendo rápido siguen escribiendo menos de 10 de cada
  100 que tocan, la campaña 3 prueba un formulario de dos preguntas.
* Google Ads. Vale la pena mirar primero, gratis, cuánta gente busca «software
  taller mecánico» en Chile. Quien busca eso ya quiere comprar; si hay volumen,
  es un mejor uso del dinero que ampliar Meta.
* Herramientas pagadas de anuncios con IA.

---

## 7. Guion del anuncio A (Joaquín a la cámara)

Celular en vertical, a la altura de los ojos, con luz de día. De fondo, un
taller o un auto con el capó abierto. Sin leer: decirlo como se lo diría a un
conocido. 30 a 40 segundos.

> Si tienes un taller mecánico en Quilpué, Villa Alemana, Viña o Valparaíso,
> esto es para ti.
>
> Soy Joaquín. Hice un sistema para talleres porque vi lo mismo muchas veces:
> entregas el auto y el cliente te dice «ese rayón no estaba». Y sin una foto,
> terminas pagándolo tú.
>
> Con Tallermax, cuando recibes el auto le sacas cuatro fotos con el celular, y
> al cliente le llega la constancia a su correo antes de irse.
>
> Estoy buscando los primeros cinco talleres de la zona. Te lo dejo armado hoy,
> con tu logo, y lo pruebas siete días gratis. Escríbeme por WhatsApp.

Mientras habla, mostrar una vez el teléfono con la pantalla de las cuatro fotos.
Los subtítulos los pone el sistema de reels.

---

## 8. Hechos, hipótesis y lo que falta

**Hechos (medidos en nuestra cuenta)**
* $27.481 gastados, 2 conversaciones, 68 toques, 16.258 veces mostrado.
* Las 2 conversaciones vinieron del anuncio del rayón, en la primera semana.
* 12 seguidores en Instagram; ninguna publicación pasa de 8 «me gusta».

**Hipótesis (la campaña 2 las confirma o las bota)**
* Un video del fundador sube los toques por sobre 0,8 %.
* Las preguntas listas para tocar y la respuesta rápida suben a 10 de cada 100
  los toques que terminan en conversación.
* La mitad de las conversaciones llega a la prueba y 1 de cada 4 pruebas paga.
* El contacto directo trae clientes más baratos que los anuncios.

**Lo que falta**
* Si el sitio `tallermax.website` tiene el píxel de Meta instalado (no se pudo
  revisar desde la nube). Sin él no se puede volver a mostrarle anuncios a
  quien visitó la página.
* El desglose por ubicación (Facebook o Instagram, feed o reels) y por edad de
  la campaña 1. Está en el Administrador de anuncios y dice dónde está la
  gente que sí tocó.
* Cuánta gente busca «software taller mecánico» en Google en Chile.

---

## Fuentes

Guías del repositorio (de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)):
`.claude/skills/ads/references/meta-decision-system.md`,
`meta-andromeda-playbook.md` y
`.claude/skills/ad-creative/references/meta-creative-formats.md`,
`hook-system.md`, `static-ad-templates.md`.

Meta en 2026:
* [Jon Loomer — retiro de la segmentación detallada](https://www.jonloomer.com/qvt/detailed-targeting-announcement/)
* [Social Media Today — Meta retira más opciones](https://www.socialmediatoday.com/news/meta-removes-more-detailed-ad-targeting-options-facebook-instagram/757856/)
* [MediaPost — Meta consolida opciones](https://www.mediapost.com/publications/article/408262/meta-further-consolidates-ad-targeting-options.html)
* [Stackmatix — presupuesto mínimo](https://www.stackmatix.com/blog/how-much-to-run-ads-on-facebook)
* [Vizup — mínimos y reglas de entrega 2026](https://www.tryvizup.com/blog/meta-ads-minimum-budget-requirements-2026)
* [Cropink — presupuesto mínimo](https://cropink.com/minimum-budget-for-facebook-ads)

Formatos:
* [Motion — 550.000 anuncios, «las tendencias no son universales»](https://motionapp.com/library/research/creative-benchmarks-2026/trends-are-not-universal)
* [MHI — fundador contra contenido de marca](https://mhigrowthengine.com/blog/founder-led-vs-brand-content-2026/)
* [Stackmatix — video contra imagen](https://stackmatix.com/blog/facebook-video-vs-image-ads-performance)
* [Adstellar — anuncios del fundador](https://www.adstellar.ai/blog/founder-led-ads)
* [Growthspree — video para software B2B](https://www.growthspreeofficial.com/blogs/meta-video-ads-b2b-saas-2026)

Anuncios a WhatsApp (proveedores):
* [Infobip](https://www.infobip.com/blog/click-to-whatsapp-ads)
* [eGrow](https://www.egrow.com/en/blog/click-to-whatsapp-ads-the-complete-guide-to-driving-sales-from-meta-to-whatsapp-2026)
* [Clickatell](https://www.clickatell.com/help-center/whatsapp/marketing-commerce/what-are-best-practices-for-ads-that-click-to-whatsapp/)
* [Wati — WhatsApp contra formulario](https://www.wati.io/en/blog/click-to-whatsapp-ads-vs-lead-form-ads-roas/)
* [Stackmatix — contactos por WhatsApp](https://www.stackmatix.com/blog/meta-ads-whatsapp-lead-generation)
* [Mercately — precios de WhatsApp desde octubre de 2026](https://blog.mercately.com/nuevos-precios-whatsapp-api-octubre-2026/)
* [Chattigo — cobro por mensaje](https://blog.chattigo.com/whatsapp-business/cuanto-cobra-whatsapp-business-por-mensaje)

Primeros clientes:
* [Saas Hero — marketing de software B2B en etapa temprana](https://www.saashero.net/strategy/early-b2b-saas-marketing-strategy/)
* [Cut the SaaS — los primeros 100 clientes](https://cut-the-saas.com/guides/first-100-customers)
