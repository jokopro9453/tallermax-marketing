# Voz en off de los reels: la graba Joaquín

Desde el 6 de noviembre los reels nuevos llevan la voz de Joaquín: una sola
voz, la del que hizo Tallermax, contando lo que se ve en pantalla. Ningún
servicio de voces suena tan creíble como «lo hice yo, acá en Quilpué».

Se graba **un archivo por escena**. Claude limpia el audio, alarga cada escena
lo que haga falta para que la frase quepa y arma el reel:

```bash
diseno/video/reel_con_voz.sh ingreso diseno/video/voz/ingreso piezas/<id>/reel.mp4
```

## Cómo grabar (10 minutos)

1. **Un lugar sin eco.** Lo mejor es un clóset con ropa o un auto estacionado
   con las ventanas cerradas. Lo peor, una cocina o un baño. Nada de ruido de
   fondo: ni radio, ni compresor, ni la tele.
2. **La app de grabadora del celular**, no una nota de voz de WhatsApp (la
   comprime y suena a teléfono). Modo avión, para que no entre una llamada.
3. **El celular a un palmo de la boca**, un poco hacia el lado, para que las
   «p» y las «b» no golpeen el micrófono.
4. **Un archivo por escena**, llamado con su número: `01`, `02`, `03`… Si te
   equivocas, borra y graba esa de nuevo. Deja un segundo de silencio antes y
   después: lo corto yo.
5. **Cómo hablar:** como si se lo contaras a un mecánico amigo, no como
   locutor de radio. Con una sonrisa (se nota en la voz), un poco más lento de
   lo normal y sin leer «de corrido». Si una palabra no te sale natural,
   cámbiala por la tuya: el texto en pantalla no tiene que ser idéntico.
6. **Escúchala una vez antes de mandarla.** Si te suena rara, es normal: todos
   oímos nuestra voz grabada así. Fíjate sólo en que se entienda y no tenga ruido.

**Para mandármelas:** adjúntalas en el chat. Si la app no te deja adjuntar
audio, súbelas a GitHub: el repositorio → carpeta `diseno/video/voz/<reel>/`
→ *Add file → Upload files*.

## Reel «Ingreso con fotos» (`diseno/video/ingreso.html`)

El primero con voz. Cada frase va con su escena: entre paréntesis, lo que se
ve en pantalla mientras hablas.

| Archivo | Lo que dices | (En pantalla) |
|---|---|---|
| `01` | ¿Te ha pasado? Le entregas el auto al cliente y te dice: «oiga, ese rayón no estaba». | ¿Te ha pasado? «Ese rayón no estaba.» |
| `02` | Y ahí es tu palabra contra la suya. Sin pruebas, o pierdes la discusión… o pierdes al cliente. | Y es tu palabra contra la suya. |
| `03` | Con Tallermax, cuando recibes el auto, le sacas una foto por cada lado. Frente, atrás y los dos costados. | Al recibirlo, foto a las 4 caras. |
| `04` | Si viene con un daño, lo marcas con el dedo, ahí mismo en la foto. | Marcas los daños con el dedo. |
| `05` | Y al cliente le llega una constancia al correo, con las fotos… | Y la evidencia le llega a su correo. |
| `06` | …antes de que se vaya del taller. Con fecha y hora. Nada que discutir. | Antes de que se vaya. |
| `07` | Soy Joaquín, y hice Tallermax acá en Quilpué. Pruébalo gratis siete días: escríbenos por WhatsApp. | Logo · Pruébalo gratis 7 días |

Dura unos 35 segundos con la voz (sin voz eran 28): las escenas se alargan
solas lo que haga falta.
