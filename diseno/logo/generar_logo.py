"""Genera los SVG del logo de Tallermax con el texto convertido a trazos.

    docker run --rm -v "$PWD/diseno:/d:z" python:3.12-slim \
        sh -c "pip install -q fonttools && python /d/logo/generar_logo.py"

El texto sale de Inter (OFL) a peso 800, convertido a curvas: el SVG no
depende de que quien lo abra tenga la tipografía.
"""

from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

AQUI = Path(__file__).parent
INDIGO, GRAFITO, BLANCO, AMARILLO = "#4F46E5", "#121318", "#FFFFFF", "#FFC53D"

fuente = instantiateVariableFont(TTFont(AQUI.parent / "fuentes" / "Inter.ttf"), {"wght": 800, "opsz": 32})
glifos, cmap, upm = fuente.getGlyphSet(), fuente.getBestCmap(), fuente["head"].unitsPerEm
X_HEIGHT = fuente["OS/2"].sxHeight / upm


def texto(s: str, tam: float, x: float, base: float, tracking: float = -0.03) -> tuple[str, float]:
    """Path SVG de `s` con la línea base en `base`. Devuelve (d, ancho)."""
    escala, avance, partes = tam / upm, 0.0, []
    for ch in s:
        g = cmap[ord(ch)]
        pen = SVGPathPen(glifos)
        glifos[g].draw(TransformPen(pen, (escala, 0, 0, -escala, x + avance, base)))
        partes.append(pen.getCommands())
        avance += fuente["hmtx"][g][0] * escala + tracking * tam
    return " ".join(partes), avance - tracking * tam


# Hexágono con la punta arriba, de esquinas redondeadas (el trazo del mismo
# color redondea las puntas). Es una tuerca vista de frente.
HEX = "M32 6.5 L54.08 19.25 L54.08 44.75 L32 57.5 L9.92 44.75 L9.92 19.25 Z"


def marca_a(fondo: str, figura: str) -> str:
    """A · Tuerca con la T: la T de Tallermax recortada en una tuerca."""
    # La T es UNA forma, con sólo las esquinas de fuera redondeadas: con dos
    # rectángulos superpuestos, sus esquinas dejaban una muesca en la unión.
    t = ("M21.1 20 H42.9 Q44.5 20 44.5 21.6 V25.4 Q44.5 27 42.9 27 H35.5 V43.9 Q35.5 45.5 33.9 45.5 "
         "H30.1 Q28.5 45.5 28.5 43.9 V27 H21.1 Q19.5 27 19.5 25.4 V21.6 Q19.5 20 21.1 20 Z")
    return (f'<path d="{HEX}" fill="{fondo}" stroke="{fondo}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="{t}" fill="{figura}"/>')


def marca_b(linea: str, visto: str) -> str:
    """B · Tuerca con visto bueno: el trabajo terminado."""
    return (f'<path d="{HEX}" fill="none" stroke="{linea}" stroke-width="6.5" stroke-linejoin="round"/>'
            f'<path d="M22.5 32.5 L29.5 39.5 L42 25.5" fill="none" stroke="{visto}" stroke-width="6" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def marca_c(fondo: str, letras: str) -> str:
    """C · Monograma «tm» en un ícono de app."""
    d, ancho = texto("tm", 31, 0, 0, -0.04)
    return (f'<rect x="4" y="4" width="56" height="56" rx="15" fill="{fondo}"/>'
            f'<path transform="translate({32 - ancho / 2:.2f} {32 + X_HEIGHT * 31 / 2:.2f})" d="{d}" fill="{letras}"/>')


def svg(ancho: float, alto: float, cuerpo: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.2f} {alto:.2f}" '
            f'width="{ancho:.0f}" height="{alto:.0f}">{cuerpo}</svg>\n')


def horizontal(marca: str, color_texto: str) -> str:
    """Ícono de 64 + «tallermax» con el ojo de la x centrado en el ícono."""
    tam = 40
    base = 32 + X_HEIGHT * tam / 2
    d, ancho = texto("tallermax", tam, 64 + 16, base)
    return svg(64 + 16 + ancho + 2, 64, f'{marca}<path d="{d}" fill="{color_texto}"/>')


salida = AQUI / "svg"
salida.mkdir(exist_ok=True)
archivos = {
    # Recomendado (A) — juego completo
    "tallermax-icono.svg": svg(64, 64, marca_a(INDIGO, BLANCO)),
    "tallermax-icono-blanco.svg": svg(64, 64, marca_a(BLANCO, GRAFITO)),
    "tallermax-icono-negro.svg": svg(64, 64, marca_a(GRAFITO, BLANCO)),
    "tallermax-horizontal.svg": horizontal(marca_a(INDIGO, BLANCO), GRAFITO),
    "tallermax-horizontal-sobre-oscuro.svg": horizontal(marca_a(INDIGO, BLANCO), BLANCO),
    "tallermax-horizontal-negro.svg": horizontal(marca_a(GRAFITO, BLANCO), GRAFITO),
    "tallermax-horizontal-blanco.svg": horizontal(marca_a(BLANCO, GRAFITO), BLANCO),
    # Alternativas, para la hoja de conceptos
    "concepto-b-icono.svg": svg(64, 64, marca_b(INDIGO, GRAFITO)),
    "concepto-b-icono-oscuro.svg": svg(64, 64, marca_b(INDIGO, BLANCO)),
    "concepto-b-horizontal.svg": horizontal(marca_b(INDIGO, GRAFITO), GRAFITO),
    "concepto-c-icono.svg": svg(64, 64, marca_c(INDIGO, BLANCO)),
    "concepto-c-horizontal.svg": horizontal(marca_c(INDIGO, BLANCO), GRAFITO),
}
for nombre, contenido in archivos.items():
    (salida / nombre).write_text(contenido, encoding="utf-8")
print(f"{len(archivos)} SVG en {salida}")
