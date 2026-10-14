#!/usr/bin/env bash
#
# Regenera el logo entero: SVG (texto en trazos), PNG, favicon.ico y la hoja.
#
#     diseno/logo/exportar.sh
#
# Todo en contenedores (el host es inmutable): Python para los SVG y el .ico,
# y el Chromium del backend de Tallermax —que tiene que estar levantado— para
# los PNG.

set -euo pipefail

LOGO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISENO="$(dirname "$LOGO")"
TALLERMAX="${TALLERMAX:-$HOME/TALLERPROYECT}"

docker_() {
  if docker info >/dev/null 2>&1; then docker "$@"
  else sg docker -c "docker $(printf '%q ' "$@")"; fi
}
compose() { (cd "$TALLERMAX" && docker_ compose "$@"); }
python_() {
  docker_ run --rm -v "$DISENO:/d:z" python:3.12-slim \
    sh -c "pip install -q --root-user-action=ignore --disable-pip-version-check $1 && python /d/logo/$2"
}

python_ fonttools generar_logo.py

compose exec -T backend sh -c 'rm -rf /tmp/dlogo && mkdir -p /tmp/dlogo' < /dev/null
compose cp "$LOGO" backend:/tmp/dlogo/logo >/dev/null
compose cp "$DISENO/fuentes" backend:/tmp/dlogo/fuentes >/dev/null
compose exec -T backend sh -c \
  'ln -sfn /app/node_modules /tmp/dlogo/logo/node_modules && node /tmp/dlogo/logo/exportar.mjs /tmp/dlogo/logo' < /dev/null
rm -rf "$LOGO/png"
compose cp backend:/tmp/dlogo/logo/png "$LOGO/png" >/dev/null
compose cp backend:/tmp/dlogo/logo/hoja-conceptos.jpg "$LOGO/hoja-conceptos.jpg" >/dev/null
compose exec -T backend rm -rf /tmp/dlogo < /dev/null

python_ pillow favicon.py
ls "$LOGO/svg" "$LOGO/png"
