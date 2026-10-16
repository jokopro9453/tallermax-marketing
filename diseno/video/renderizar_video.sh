#!/usr/bin/env bash
#
# Genera un reel MP4 (1080 × 1920, 30 fps, H.264 + pista de audio silenciosa).
#
#     diseno/video/renderizar_video.sh fundadores videos/2026-10-17-fundadores.mp4
#     diseno/video/renderizar_video.sh fundadores /tmp/muestras --tiempos 1.5,8,14
#
# Los cuadros los saca el Chromium del contenedor `backend` de Tallermax (que
# tiene que estar levantado) y el MP4 lo arma un ffmpeg completo en contenedor:
# el ffmpeg de Fedora no trae H.264. Con --tiempos deja sólo los JPEG.

set -euo pipefail

VIDEO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISENO="$(dirname "$VIDEO")"
TALLERMAX="${TALLERMAX:-$HOME/TALLERPROYECT}"
nombre="$1"; destino="$2"; shift 2

docker_() {
  if docker info >/dev/null 2>&1; then docker "$@"
  else sg docker -c "docker $(printf '%q ' "$@")"; fi
}
compose() { (cd "$TALLERMAX" && docker_ compose "$@"); }

compose exec -T backend sh -c 'rm -rf /tmp/dvid && mkdir -p /tmp/dvid' < /dev/null
compose cp "$DISENO/video" backend:/tmp/dvid/video >/dev/null
compose cp "$DISENO/fuentes" backend:/tmp/dvid/fuentes >/dev/null
compose exec -T backend sh -c '
  ln -sfn /app/node_modules /tmp/dvid/video/node_modules
  node /tmp/dvid/video/renderizar_video.mjs "/tmp/dvid/video/$0.html" /tmp/dvid/cuadros "$@"
' "$nombre" "$@" < /dev/null

trabajo="$(mktemp -d)"
trap 'rm -rf "$trabajo"' EXIT
compose cp backend:/tmp/dvid/cuadros "$trabajo/cuadros" >/dev/null
compose exec -T backend rm -rf /tmp/dvid < /dev/null

if [ "${1:-}" = "--tiempos" ]; then
  mkdir -p "$destino"; cp "$trabajo"/cuadros/*.jpg "$destino"/; ls "$destino"; exit 0
fi

mkdir -p "$(dirname "$destino")"
docker_ run --rm -v "$trabajo:/w:z" --entrypoint /ffmpeg mwader/static-ffmpeg:7.1 -v error -y \
  -framerate 30 -i /w/cuadros/%05d.jpg -f lavfi -i anullsrc=r=48000:cl=stereo -shortest \
  -vf scale=in_range=pc:out_range=tv,format=yuv420p -color_range tv \
  -c:v libx264 -preset slow -crf 19 -profile:v high -r 30 \
  -c:a aac -b:a 128k -movflags +faststart /w/salida.mp4
cp "$trabajo/salida.mp4" "$destino"
ls -la "$destino"
