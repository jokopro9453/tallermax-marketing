# Voz en off de los reels: la graba Joaquín

Desde el 6 de noviembre los reels nuevos llevan la voz de Joaquín: una sola
voz, la del que hizo Tallermax, contando lo que se ve en pantalla. Ningún
servicio de voces suena tan creíble como «lo hice yo, acá en Quilpué».

Se graba **un archivo por escena**. Claude limpia el audio, alarga cada escena
lo que haga falta para que la frase quepa, le pone **subtítulos palabra por
palabra** (la mayoría ve los reels sin sonido) y arma el reel:

```bash
diseno/video/reel_con_voz.sh ingreso diseno/video/voz/ingreso piezas/<id>/reel.mp4
```

Lo que se pidió decir está en `diseno/video/voz/<reel>/guion.json`: los
subtítulos usan su ortografía donde lo que Whisper oyó se le parece, y lo que
Joaquín dijo de verdad donde cambió una frase.

## Cómo grabar (10 minutos por reel)

1. **Un lugar sin eco.** Lo mejor es un clóset con ropa o un auto estacionado
   con las ventanas cerradas. Lo peor, una cocina o un baño. Nada de ruido de
   fondo: ni radio, ni compresor, ni la tele.
2. **La Grabadora de voz del Samsung**, no una nota de voz de WhatsApp (la
   comprime y suena a teléfono). En sus ajustes: *Calidad de grabación → Alta*,
   y el modo **Estándar** (no «Entrevista» ni «Voz a texto»). Modo avión, para
   que no entre una llamada.
3. **El celular a un palmo de la boca**, un poco hacia el lado, para que las
   «p» y las «b» no golpeen el micrófono.
4. **Un archivo por escena**, llamado con su número: `01`, `02`, `03`… Si te
   equivocas, borra y graba esa de nuevo. Deja un segundo de silencio antes y
   después: lo corto yo.
5. **Cómo hablar:** como si se lo contaras a un mecánico amigo, no como
   locutor de radio. Con una sonrisa (se nota en la voz), un poco más lento de
   lo normal y sin leer «de corrido». Si una palabra no te sale natural,
   cámbiala por la tuya.
6. **Escúchala una vez antes de mandarla.** Si te suena rara, es normal: todos
   oímos nuestra voz grabada así. Fíjate sólo en que se entienda y no tenga ruido.

**Para mandármelas:** adjúntalas en el chat con el clip 📎 (el micrófono del
chat convierte la voz en texto y el audio se pierde). Si la app no deja
adjuntar audio, súbelas a GitHub en `diseno/video/voz/<reel>/` → *Add file →
Upload files*.

## Reel 1 · «Ingreso con fotos» (`ingreso`, 7 escenas)

El anuncio que trajo las conversaciones en la campaña de noviembre, ahora con voz.
Gancho: la situación que todo mecánico conoce.

| Archivo | Lo que dices | (En pantalla) |
|---|---|---|
| `01` | ¿Te ha pasado? Le entregas el auto al cliente y te dice: «oiga, ese rayón no estaba». | ¿Te ha pasado? «Ese rayón no estaba.» |
| `02` | Y ahí es tu palabra contra la suya. Sin pruebas, o pierdes la discusión… o pierdes al cliente. | Y es tu palabra contra la suya. |
| `03` | Con Tallermax, cuando recibes el auto, le sacas una foto por cada lado. Frente, atrás y los dos costados. | Al recibirlo, foto a las 4 caras. |
| `04` | Si viene con un daño, lo marcas con el dedo, ahí mismo en la foto. | Marcas los daños con el dedo. |
| `05` | Y al cliente le llega una constancia al correo, con las fotos… | Y la evidencia le llega a su correo. |
| `06` | …antes de que se vaya del taller. Con fecha y hora. Nada que discutir. | Antes de que se vaya. |
| `07` | Soy Joaquín, y hice Tallermax acá en Quilpué. Pruébalo gratis siete días: escríbenos por WhatsApp. | Logo · Pruébalo gratis 7 días |

## Reel 2 · «El rayón de $80.000» (`rayon80`, 6 escenas, nuevo)

Gancho: la cifra primero. Es la misma cuenta del carrusel del 14 de noviembre.

| Archivo | Lo que dices | (En pantalla) |
|---|---|---|
| `01` | Ochenta mil pesos. Eso cuesta repintar una puerta que tú no rayaste. | $80.000 · Repintar una puerta que tú no rayaste. |
| `02` | Porque si no tienes una foto, es tu palabra contra la del cliente. Y o lo pagas tú, o lo pierdes. | Sin una foto, lo pagas tú. |
| `03` | Con Tallermax, cuando recibes el auto, le sacas una foto por cada lado, desde el celular. | Foto a las 4 caras al recibirlo. |
| `04` | Y antes de que se vaya, al cliente le llega la constancia al correo, con las fotos. | La constancia, en su correo. |
| `05` | Un solo reclamo que te ahorras paga más de dos meses de Tallermax. | Un rayón $80.000 · Tallermax $35.700 al mes |
| `06` | Soy Joaquín, de Quilpué. Pruébalo gratis siete días: escríbenos por WhatsApp. | Logo · Pruébalo gratis 7 días |

## Reel 3 · «¿Qué le hiciste la otra vez?» (`cobro`, 5 escenas)

El reel de patente y cobro del 2 de noviembre, ahora con voz. Gancho: la
pregunta que el mecánico se hace cuando vuelve un cliente.

| Archivo | Lo que dices | (En pantalla) |
|---|---|---|
| `01` | ¿Qué le hiciste a este auto la otra vez? Si tienes que buscarlo en el cuaderno, te vas a demorar. | ¿Qué le hiciste la otra vez? |
| `02` | Con Tallermax escribes la patente, y aparece todo lo que se le hizo, con fecha y valor. | Escribes la patente… (historial) |
| `03` | Agregas el trabajo de hoy, y el cobro sale solo, con el IVA calculado. | …y el cobro sale con IVA. |
| `04` | Y el comprobante sale en PDF, con el logo de tu taller. | El comprobante, en PDF con tu logo. |
| `05` | Lo hice yo, acá en Quilpué. Pruébalo gratis siete días: escríbenos por WhatsApp. | Logo · Pruébalo gratis 7 días |
