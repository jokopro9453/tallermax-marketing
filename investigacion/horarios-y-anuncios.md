# Horarios de publicación y anuncios de Meta

Investigación del 14 de octubre de 2026. Para quien prepara las piezas y para
el agente que las publica.

Separa siempre **lo que dicen los estudios** de **lo que deducimos para
TallerMax**. Lo segundo es una hipótesis que se confirma con las estadísticas
de la propia cuenta, no un dato.

---

## 1. Cuándo publicar

### Lo que dicen los estudios

* **Globales (millones de publicaciones).** Coinciden en los días hábiles de
  mitad de semana y en contra de viernes y sábado. No coinciden en la hora:
  - Buffer, con 9,6 millones de publicaciones: los mejores huecos son jueves 9:00,
    miércoles 12:00 y miércoles 18:00. El mejor día es el miércoles.
  - Sprout Social: de martes a jueves, en franjas de mediodía y tarde.
  - Later, con más de 6 millones: madrugada (5:00) y lunes.
* **Chile.** Las guías locales repiten dos bloques: **mediodía (12:00–14:30)**
  y **noche (19:00–22:30)** de lunes a viernes, con martes y miércoles como los
  más fuertes. Para los reels marcan de noche (20:00–23:00), y para las
  historias, temprano (8:00–10:00) y al cierre del día. Ninguna cita una
  metodología propia: casi todas adaptan los estudios globales.

**Conclusión honesta:** los estudios generales no saben nada de mecánicos. Sirven
como punto de partida y nada más.

### Lo que deducimos para el público de TallerMax

El dueño de un taller trabaja con las manos, más o menos de 8:30 a 18:30, y
no mira el teléfono con grasa en los dedos. Lo mira:

| Momento | Por qué | Formato |
|---|---|---|
| **8:00–8:45**, antes de abrir | café y teléfono | historias |
| **13:00–14:30**, almuerzo | la pausa más segura del día | carruseles y fotos |
| **20:30–22:00**, en la casa | tiempo largo, ve videos | reels |
| **Sábado 10:00–12:00** | muchos talleres trabajan medio día | carrusel ligero |

**Calendario de partida:**

* **Martes y jueves, 13:15**: carrusel (educativo o demo).
* **Miércoles, 21:00**: reel (dolor o demo).
* **Domingo, 20:00**: una pieza opcional. El dueño planifica la semana, y es
  justo cuando piensa en «ordenar el taller».
* Historias diarias a las 8:15, cuando haya material.

**Cómo se corrige:** después de 4 semanas (unas 12 publicaciones), se miran en
las estadísticas de la cuenta, en *Seguidores → Momentos más activos*, las
horas de actividad del público real, y se mueve el calendario. El agente puede
leer esas estadísticas con la API si se le da el permiso de *insights*.

**Ojo con la hora de Chile:** hasta el primer domingo de abril es UTC−3; después,
UTC−4. Las piezas guardan su hora en `America/Santiago`, nunca en UTC, para
que el cambio no las corra.

---

## 2. Cómo hacer que los anuncios lleguen a talleres de verdad

### Lo que cambió en Meta (y que invalida las guías antiguas)

* Entre diciembre de 2025 y enero de 2026, Meta **retiró una gran cantidad de
  intereses** de la segmentación detallada, sin publicar la lista completa, y
  **eliminó las exclusiones por interés**.
* Lo que queda de segmentación detallada funciona, para la mayoría de los
  objetivos, como **sugerencia**: Meta puede ampliarla a quien crea que va a
  responder. Para objetivos de conversión, la ampliación va siempre activada.
* No hay ninguna fuente que diga si siguen existiendo intereses como «dueños de
  pequeñas empresas» o «taller mecánico». **Hay que comprobarlo en el propio
  Administrador de anuncios**, que marca en rojo los intereses retirados.

En la práctica, **ya no se puede «elegir» a los mecánicos con casillas.** Lo
que filtra al público ahora son estas cuatro cosas, en este orden:

### a) La pieza misma es la segmentación

Meta muestra el anuncio a quien se detiene a mirarlo. Si el primer segundo
dice **«Si tienes un taller mecánico…»**, con un taller real, una orden de
trabajo y una patente, los que se quedan son mecánicos, y el algoritmo aprende
a buscar más como ellos.

* Nombrar al público en la primera frase y en el primer cuadro.
* Usar las palabras del oficio: patente, OT, repuestos, «el cliente que dice
  que el rayón no estaba».
* Nada de imágenes de banco con un mecánico sonriente: delatan publicidad y
  atraen a cualquiera.

### b) Audiencias propias (lo más preciso que existe)

1. **Quienes vieron el 50 % o más de un reel orgánico.** Si el reel trata de
   órdenes de trabajo, quien lo ve hasta la mitad casi seguro es del rubro. Es
   **el motivo principal para publicar orgánico antes de pagar**.
2. **Quienes interactuaron con la cuenta** de Instagram o con la página de
   Facebook en los últimos 90 días.
3. **Visitantes de la landing**, para lo que la landing necesita el **píxel de
   Meta**. Conviene instalarlo ya, aunque los anuncios empiecen más tarde, porque
   la audiencia se va llenando desde el día en que se instala.
4. **Lista de clientes**, con los talleres que ya usan TallerMax, para crear una
   **audiencia similar al 1 %** en Chile. Con pocos talleres en la lista queda
   pobre: sirve desde unos cientos de contactos.
   - Sólo con datos de contactos que hayan dado su permiso. **No subir listas
     raspadas de internet**: la nueva ley chilena de protección de datos
     personales (Ley 21.719) entra en vigencia en diciembre de 2026.

### c) Geografía, en lugar de intereses

Los talleres se agrupan. En vez de «todo Chile», probar círculos de pocos
kilómetros alrededor de los **barrios de talleres y repuestos**. En Santiago,
el eje de 10 de Julio y Avenida Matta es el más conocido; en regiones, el
equivalente de cada ciudad. El que vive cerca sin tener taller se filtra con
el punto (a).

* Edad: 25–65 años. Sin filtrar por sexo.
* **Incluir Facebook**, no sólo Instagram: el público de más de 40 años, que es
  buena parte de los dueños de taller, está más en Facebook.
* Los intereses que sigan disponibles (mecánica automotriz, repuestos,
  herramientas) se ponen como sugerencia en **un** conjunto de anuncios, y se
  compara con otro abierto (*Advantage+*) con el mismo presupuesto.

### d) El objetivo de la campaña

* **Mensajes a WhatsApp** (*click-to-WhatsApp*) con la **app gratuita de
  WhatsApp Business**. Las tarifas por mensaje de la API de WhatsApp Business no
  aplican si se contesta desde la app.
  - El chat se abre con una pregunta que filtra: *«¿Cuántas personas trabajan
    en tu taller?»*. Quien no tiene taller se cae solo.
  - La meta del chat es **agendar una demo de 10 minutos**, no «conseguir
    contactos».
* Los proveedores de *chatbots* aseguran que WhatsApp convierte 2 o 3 veces más
  que un formulario o una landing, pero son cifras de quien vende el servicio.
  **Tómalas como una hipótesis, no como un dato.**
* **Qué medir:** costo por **demo agendada** y por **taller que paga**. El costo
  por mensaje o por clic engaña: 1.000 chats pueden ser 150 talleres reales.

### Plan de prueba sugerido

1. **Semanas 1–4: sólo orgánico.** 3 piezas por semana, píxel instalado y
   audiencias creciendo.
2. **Semana 5: primera campaña.** Dos conjuntos de anuncios, uno con
   audiencias propias y uno abierto en zona de talleres, con 2 piezas cada uno
   (las 2 orgánicas que mejor funcionaron). Mínimo 7 días sin tocar, porque Meta
   necesita aprender.
3. **Presupuesto:** no encontramos datos fiables de CPM ni de costo por mensaje
   en Chile para 2026. Partir con poco, medir el costo por demo durante la
   primera semana y recién entonces decidir si se sube.

---

## Fuentes

Horarios:
* [Buffer — 9,6 M de publicaciones (sep. 2026)](https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/)
* [Sprout Social — Instagram](https://sproutsocial.com/insights/best-times-to-post-on-instagram/)
* [Later — más de 6 M de publicaciones](https://later.com/blog/best-time-to-post-on-instagram/)
* [CreatorFlow — comparativa de estudios](https://creatorflow.so/blog/best-times-post-instagram/)
* [Entel — horarios en Chile](https://ce.entel.cl/articulos/horarios-para-publicar-en-instagram)
* [Brújula Marketing — Chile 2026](https://brujulamarketing.cl/blog/mejores-horarios-publicar-redes-sociales-chile/)
* [Umarket — Chile 2026](https://umarket.cl/mejores-horas-para-publicar-en-instagram-chile/)
* [TusFollowers — Chile](https://tusfollowers.com/cl/blog/mejores-horarios-publicar-instagram-chile)

Segmentación de Meta:
* [Brandwatch — cambios de Meta en intereses](https://social-media-management-help.brandwatch.com/en/articles/13215856-meta-changes-to-detailed-targeting-interests-in-advertise)
* [The Keyword — Meta retira opciones de segmentación](https://www.thekeyword.co/news/meta-to-remove-detailed-targeting-options-in-ads-manager)
* [Conversios — Advantage+ frente a segmentación detallada](https://www.conversios.io/blog/meta-advantage-audience-vs-detailed-targeting-2026-guide/)
* [Pixelmovers — qué funciona tras el retiro](https://pixelmovers.co/blog/meta-detailed-targeting-removed-what-works-2026)
* [AsisteClick — click-to-WhatsApp (proveedor)](https://asisteclick.com/en/blog/click-to-whatsapp-ads-ctwa-conversion-2026)
* [ChatMaxima — playbook click-to-WhatsApp (proveedor)](https://chatmaxima.com/blog/2026-click-to-whatsapp-ads-playbook/)
* [Teramont — tarifas de la API de WhatsApp en Chile](https://teramont.net/es/blog/whatsapp-business-api-cobro-mensajes-servicio-2026)

API de Instagram:
* [Meta — Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
* [Meta — IG User Media](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media)
