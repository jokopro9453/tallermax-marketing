#!/usr/bin/env bash
#
# Genera los JPEG de las piezas y los deja en piezas/<id>/.
#
#     diseno/renderizar.sh rayon:2026-10-20-1315-el-rayon-que-ya-estaba [...]
#
# Usa el Chromium del contenedor `backend` de Tallermax (el host es inmutable y
# ahí no se instala nada), así que esa pila tiene que estar levantada. Se le
# copia diseno/ a /tmp, se renderiza ahí y se traen las imágenes de vuelta.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TALLERMAX="${TALLERMAX:-$HOME/TALLERPROYECT}"
[ $# -gt 0 ] || { sed -n '3,9p' "$0"; exit 2; }

docker_() {
  if docker info >/dev/null 2>&1; then docker "$@"
  else sg docker -c "docker $(printf '%q ' "$@")"; fi
}
compose() { (cd "$TALLERMAX" && docker_ compose "$@"); }

compose exec -T backend rm -rf /tmp/diseno < /dev/null
compose cp "$RAIZ/diseno" backend:/tmp/diseno >/dev/null
compose exec -T backend sh -c '
  ln -sfn /app/node_modules /tmp/diseno/node_modules
  node /tmp/diseno/renderizar.mjs /tmp/diseno "$@"
' sh "$@" < /dev/null

for encargo in "$@"; do
  id="${encargo#*:}"
  rm -rf "$RAIZ/piezas/$id"
  mkdir -p "$RAIZ/piezas"
  compose cp "backend:/tmp/diseno/salida/$id" "$RAIZ/piezas/$id" >/dev/null
done
compose exec -T backend rm -rf /tmp/diseno < /dev/null

ls -la "$RAIZ"/piezas/*/
