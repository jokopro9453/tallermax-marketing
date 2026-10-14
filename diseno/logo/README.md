# Logo de Tallermax

**La T en la tuerca.** La inicial de la marca recortada en una tuerca vista
de frente: el objeto más reconocible de un taller. Índigo `#4F46E5` y blanco.
El nombre va en minúsculas, Inter 800, **convertido a trazos**: los SVG se ven
igual en cualquier equipo, tenga o no la tipografía.

## Qué archivo usar

| Dónde | Archivo |
|---|---|
| Landing, fondo claro | `svg/tallermax-horizontal.svg` |
| Landing, fondo oscuro | `svg/tallermax-horizontal-sobre-oscuro.svg` |
| Sobre fondo índigo o una foto | `svg/tallermax-horizontal-blanco.svg` |
| Impreso en un color (timbre, factura) | `svg/tallermax-horizontal-negro.svg` |
| Sólo el ícono | `svg/tallermax-icono.svg` (+ `-blanco`, `-negro`) |
| Favicon | `png/favicon.ico` |
| Ícono de app / Apple / Android | `png/tallermax-icono-180.png`, `-192`, `-512` |
| Foto de perfil de Instagram | `png/perfil-instagram.png` |
| Documentos (Word, presentaciones) | `png/tallermax-horizontal@4x.png` |

En Next.js basta con copiar `favicon.ico` a `src/app/favicon.ico` y
`tallermax-icono-180.png` como `src/app/apple-icon.png`.

## Reglas

* **No poner la versión índigo sobre fondo índigo**: se usa la blanca.
* **Aire alrededor**: al menos la mitad del ancho del ícono libre por cada lado.
* **Tamaño mínimo**: ícono de 16 px; logo horizontal de 96 px de ancho.
* **No** estirar, rotar, cambiar los colores, ponerle sombras ni reescribir
  el nombre con otra tipografía.

## Cómo se regenera

`diseno/logo/exportar.sh` rehace todo: SVG, PNG, favicon y la hoja de
conceptos. Las formas están en `generar_logo.py`.
