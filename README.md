# tallermax-marketing

Contenido de redes sociales de TallerMax (`tallermax.website`): las piezas, sus
imágenes y el agente que las publica en Instagram.

El código del producto vive en otro repositorio (`Tallermax`). Aquí no hay
nada que se despliegue al servidor.

## Cómo fluye una publicación

1. Las imágenes de la pieza van a `piezas/<id>/`, y la pieza entra a la cola
   de la página de vista previa con estado `borrador`.
2. Se revisa en esa página y se aprueba o se pide cambio.
3. El agente de la nube publica lo aprobado cuya hora ya llegó, y anota el
   enlace de la publicación en la misma pieza.

**Nada sale sin aprobación.** El agente ignora cualquier pieza que no esté
aprobada, por buena que parezca.

## Estructura

```
piezas/
  2026-10-20-1315-el-rayon-que-ya-estaba/
    01.jpg 02.jpg …   en orden; la primera es la portada. El texto, la fecha
                      y el estado están en la cola, no aquí
anuncios/             el piloto de la campaña de Meta: reglas, tope y cómo se configura
investigacion/        horarios, anuncios, la competencia y por qué elegir Tallermax
scripts/              publicar.py (Instagram) · anuncios.py (campaña de Meta) y sus pruebas
vista-previa/         la página de aprobación
```

## Reglas de las imágenes

Las pone la API de Instagram, no nosotros:

* **Sólo JPEG.** Ni PNG ni WebP: la API los rechaza.
* **Proporción entre 4:5 y 1.91:1.** Usamos **1080 × 1350 (4:5)**, la que más
  pantalla ocupa en el feed.
* **8 MB como máximo** por imagen.
* **Hasta 10 imágenes por carrusel.** Instagram recorta todas según la
  primera, así que todas van del mismo tamaño.
* **Tienen que estar en una URL pública**: Instagram las descarga desde ahí.

Y una nuestra, desde el 25 de octubre: **quien ve la pieza por primera vez
sabe qué es Tallermax antes de ver una función.** La portada de cada carrusel
lleva la firma (`.firma` en `diseno/marca.css`: logo + «Sistema de gestión para
talleres mecánicos»). Los reels la llevan arriba en todas las escenas menos la
última (la pone `diseno/video/reel.js`). Y las dos primeras líneas del texto,
las que se ven sin tocar «más», dicen qué es Tallermax.

## Lo que NO va en este repositorio

El token de Instagram. Vive como variable de entorno `IG_TOKEN` en el entorno
de nube del agente, y en ningún otro sitio.

## La página de vista previa

Publicada en https://claude.ai/artifact/9HCNYBHQWVF2v8XwVDc9vE (privada: sólo
la cuenta dueña y quien ella invite). El código está en `vista-previa/`.

La cola vive en la **base de datos de esa página**, en la colección `piezas`,
y no en este repositorio: el navegador de la página no puede leer GitHub. Cada
pieza es un documento cuyo id es su carpeta (`2026-10-20-1315-slug`) con:

| Campo | Qué es |
|---|---|
| `titulo`, `tipo` | nombre interno; `carrusel`, `foto` o `reel` |
| `fecha` | `AAAA-MM-DDTHH:MM` en hora de Chile, nunca UTC |
| `texto` | el texto de la publicación |
| `imagenes` | rutas `piezas/<id>/01.jpg`… en este repo, en orden |
| `imagenesSha` | el SHA-256 de cada una, en el mismo orden |
| `diapositivas` / `guion` | lo que dice cada imagen, o los planos del reel |
| `estado` | `borrador` → `aprobada` / `cambios` → `publicada` / `error` |
| `huellaAprobada` | lo que se aprobó (ver abajo) |
| `comentario`, `revisadoPor`, `revisadoEn` | la última revisión |
| `enlace`, `publicadaEn`, `error` | los escribe el publicador |

**La huella.** Al aprobar, la página guarda el SHA-256 de
`JSON.stringify([fecha, tipo, texto, imagenes, imagenesSha])`. El publicador
la recalcula, comprueba que cada JPEG que baja de GitHub tiene el SHA-256 que
dice `imagenesSha`, y **no publica si algo no coincide**: si alguien toca el
texto, la hora o una imagen después de aprobar —aunque la imagen conserve su
nombre—, la aprobación deja de valer sola. Por eso, **al regenerar imágenes hay
que actualizar `imagenesSha` en la cola**. En Python es
`json.dumps([...], ensure_ascii=False, separators=(",", ":"))`.

## Cómo se hacen las imágenes

`diseno/` tiene un HTML por pieza; cada `<section class="slide">` es una
imagen de 1080 × 1350. `diseno/renderizar.sh archivo:id-de-pieza` las convierte
en JPEG con el Chromium del contenedor `backend` de Tallermax (que tiene que
estar levantado) y las deja en `piezas/<id>/`. Falla si una tipografía no carga
o si un texto invade el pie, en vez de entregar una imagen mal hecha.

Las tipografías (Archivo, Inter, JetBrains Mono, todas OFL) están en
`diseno/fuentes/` para que las imágenes salgan iguales en cualquier máquina.
La paleta es la de la aplicación.
