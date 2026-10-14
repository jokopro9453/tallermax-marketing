"""favicon.ico con 16, 32 y 48 px a partir de los PNG exportados.

    docker run --rm -v "$PWD/diseno:/d:z" python:3.12-slim \
        sh -c "pip install -q pillow && python /d/logo/favicon.py"
"""

from pathlib import Path

from PIL import Image

png = Path(__file__).parent / "png"
grande = Image.open(png / "tallermax-icono-48.png")
extras = [Image.open(png / f"tallermax-icono-{n}.png") for n in (16, 32)]
grande.save(png / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=extras)
print("favicon.ico")
