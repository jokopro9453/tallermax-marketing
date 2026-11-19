#!/usr/bin/env bash
#
# Edita un video grabado con el celular (Joaquín a la cámara, o la pantalla del
# teléfono) y lo deja listo para Instagram y para los anuncios.
#
#     diseno/video/editar_toma.sh toma.mp4 piezas/<id>/reel.mp4 [--guion guion.txt] [--insertos insertos.json] [--musica pista.mp3] [--sin-cortes]
#
# Limpia la voz, corta silencios y tomas repetidas, recorta a 1080 × 1920, pone
# la firma arriba, subtítulos palabra por palabra y la tarjeta de cierre. Los
# detalles están arriba de editar_toma.py. --guion es un texto con lo que se
# pidió decir (los subtítulos usan su ortografía); --insertos, una lista de
# clips para poner encima cuando se dice una frase:
#     [{"archivo": "pantalla.mp4", "frase": "cuatro fotos", "dur": 3}]
# --musica, una pista de fondo que baja sola cuando se habla (sólo pistas con
# licencia para anuncios: la biblioteca de audio de YouTube o la de Meta).
#
# Corre donde haya node, Chromium y ffmpeg con libx264 y libass (el contenedor
# de la nube de Claude los trae). Usa la misma caché que reel_con_voz.sh.

set -euo pipefail

VIDEO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISENO="$(dirname "$VIDEO")"
toma="$(realpath "$1")"; salida="$(realpath -m "$2")"; shift 2
export CHROMIUM_PATH="${CHROMIUM_PATH:-/opt/pw-browsers/chromium}"
modulos="${XDG_CACHE_HOME:-$HOME/.cache}/tallermax-video"

if [ ! -d "$modulos/node_modules/puppeteer-core" ]; then
  mkdir -p "$modulos"
  (cd "$modulos" && PUPPETEER_SKIP_DOWNLOAD=1 npm install --silent --no-save puppeteer-core@23.11.1)
fi
if [ ! -x "$modulos/venv/bin/python" ] || ! "$modulos/venv/bin/python" -c 'import faster_whisper' 2>/dev/null; then
  python3 -m venv "$modulos/venv"
  "$modulos/venv/bin/pip" install --quiet faster-whisper==1.1.1 requests
fi

trabajo="$(mktemp -d)"
trap 'rm -rf "$trabajo"' EXIT
cp -r "$VIDEO" "$trabajo/video"; cp -r "$DISENO/fuentes" "$DISENO/capturas" "$trabajo/"
ln -sfn "$modulos/node_modules" "$trabajo/video/node_modules"

# La firma (PNG transparente) y la tarjeta de cierre (3,6 s, sin sonido).
node "$trabajo/video/capas.mjs" "$trabajo/video/firma.html" "$trabajo/firma.png"
node "$trabajo/video/renderizar_video.mjs" "$trabajo/video/cierre.html" "$trabajo/cierre" >/dev/null
ffmpeg -v error -y -framerate 30 -i "$trabajo/cierre/%05d.jpg" -f lavfi -i anullsrc=r=48000:cl=stereo -shortest \
  -vf scale=in_range=pc:out_range=tv,format=yuv420p -color_range tv \
  -c:v libx264 -preset slow -crf 19 -profile:v high -r 30 -c:a aac -b:a 160k "$trabajo/cierre.mp4"

mkdir -p "$(dirname "$salida")"
HF_HOME="$modulos/hf" HF_HUB_DISABLE_XET=1 "$modulos/venv/bin/python" -I "$VIDEO/editar_toma.py" "$toma" "$salida" \
  --trabajo "$trabajo/edicion" --firma "$trabajo/firma.png" --cierre "$trabajo/cierre.mp4" "$@"
