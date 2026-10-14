# tallermax-marketing

Contenido de redes sociales de TallerMax (`tallermax.website`): las piezas, sus
imágenes y el agente que las publica en Instagram.

El código del producto vive en otro repositorio (`Tallermax`). Aquí no hay
nada que se despliegue al servidor.

## Cómo fluye una publicación

1. Se prepara la pieza en `piezas/` con estado `borrador`.
2. Se revisa en la página de vista previa y se aprueba o se pide cambio.
3. El agente de la nube publica lo aprobado cuya hora ya llegó, y anota el
   enlace de la publicación en la misma pieza.

**Nada sale sin aprobación.** El agente ignora cualquier pieza que no esté
aprobada, por buena que parezca.

## Estructura

```
piezas/
  2026-10-21-1300-ingreso-con-fotos/
    pieza.json        tipo, texto, fecha y hora (America/Santiago), estado
    01.jpg 02.jpg …   en orden; la primera es la portada
investigacion/        en qué se basan los horarios y los anuncios
scripts/              publicar.py (pendiente)
vista-previa/         la página de aprobación (pendiente)
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

## Lo que NO va en este repositorio

El token de Instagram. Vive como variable de entorno `IG_TOKEN` en el entorno
de nube del agente, y en ningún otro sitio.
