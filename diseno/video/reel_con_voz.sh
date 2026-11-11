#!/usr/bin/env bash
#
# Reel con voz en off: una grabación por escena, y cada escena dura lo que su frase.
#
#     diseno/video/reel_con_voz.sh ingreso diseno/video/voz/ingreso piezas/<id>/reel.mp4
#
# La carpeta de voz trae un archivo por escena, numerado como la escena: 01.m4a,
# 02.m4a… (sirve cualquier formato que lea ffmpeg: m4a, mp3, ogg, wav, opus). Una
# escena sin archivo va sin voz. Cada frase se limpia (ruido de fondo, graves de
# la mesa, silencios del principio y del final), entra 0,3 s después de que
# empieza su escena y la escena se alarga si la frase no cabe en su data-dur.
# Al final todo se lleva a -16 LUFS, el volumen al que Instagram no le baja.
#
# Lleva subtítulos palabra por palabra: subtitulos.py transcribe cada frase con
# faster-whisper (la primera vez instala un entorno de Python y baja el modelo,
# unos 460 MB, desde huggingface.co). Si la carpeta de voz trae guion.json (lo
# que se pidió decir, una frase por escena), los subtítulos usan su ortografía.
# Con SIN_SUBTITULOS=1 se arma sin ellos.
#
# A diferencia de renderizar_video.sh, éste no usa Docker: corre donde haya
# node, Chromium y un ffmpeg con libx264 (el contenedor de la nube de Claude los
# trae). Chromium sale de CHROMIUM_PATH, o de /opt/pw-browsers/chromium.

set -euo pipefail

VIDEO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISENO="$(dirname "$VIDEO")"
nombre="$1"; voz="$2"; destino="$3"
ENTRA=0.3    # segundos desde que empieza la escena hasta que empieza a hablar
RESPIRO=0.45 # segundos de silencio después de la frase, antes del fundido
CIERRE=1.2   # en la última escena, el logo y el botón se quedan esto más

[ -f "$VIDEO/$nombre.html" ] || { echo "No existe diseno/video/$nombre.html" >&2; exit 1; }
[ -d "$voz" ] || { echo "No existe la carpeta de voz $voz" >&2; exit 1; }
export CHROMIUM_PATH="${CHROMIUM_PATH:-/opt/pw-browsers/chromium}"

trabajo="$(mktemp -d)"
trap 'rm -rf "$trabajo"' EXIT
cp -r "$VIDEO" "$trabajo/video"; cp -r "$DISENO/fuentes" "$DISENO/capturas" "$trabajo/"

# puppeteer-core, una vez, en una carpeta de caché fuera del repositorio.
modulos="${XDG_CACHE_HOME:-$HOME/.cache}/tallermax-video"
if [ ! -d "$modulos/node_modules/puppeteer-core" ]; then
  mkdir -p "$modulos"
  (cd "$modulos" && PUPPETEER_SKIP_DOWNLOAD=1 npm install --silent --no-save puppeteer-core@23.11.1)
fi
ln -sfn "$modulos/node_modules" "$trabajo/video/node_modules"

escenas=$(grep -c 'class="esc' "$VIDEO/$nombre.html")
mkdir -p "$trabajo/voz"
duraciones=()
for i in $(seq 1 "$escenas"); do
  n=$(printf '%02d' "$i")
  origen=$(find "$voz" -maxdepth 1 -type f -name "$n.*" | head -1)
  if [ -z "$origen" ]; then duraciones+=(0); continue; fi
  ffmpeg -v error -y -i "$origen" -ac 1 -ar 48000 -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-25,\
silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,\
silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,\
acompressor=threshold=-20dB:ratio=3:attack=5:release=120" "$trabajo/voz/$n.wav"
  largo=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$trabajo/voz/$n.wav")
  extra=0; [ "$i" -eq "$escenas" ] && extra=$CIERRE
  duraciones+=("$(echo "$ENTRA + $largo + $RESPIRO + $extra" | bc -l)")
  printf 'escena %s: frase de %.1f s\n' "$n" "$largo"
done
sobran=$(find "$voz" -maxdepth 1 -type f -name '[0-9][0-9].*' | sed 's#.*/##; s#\..*##' | awk -v m="$escenas" '$1+0 > m' | sort -u | tr '\n' ' ')
[ -z "$sobran" ] || { echo "Hay grabaciones para escenas que no existen: $sobran(el reel tiene $escenas)" >&2; exit 1; }

subtitulos=()
if [ "${SIN_SUBTITULOS:-0}" != 1 ]; then
  if [ ! -x "$modulos/venv/bin/python" ] || ! "$modulos/venv/bin/python" -c 'import faster_whisper' 2>/dev/null; then
    python3 -m venv "$modulos/venv"
    "$modulos/venv/bin/pip" install --quiet faster-whisper==1.1.1 requests
  fi
  HF_HOME="$modulos/hf" HF_HUB_DISABLE_XET=1 "$modulos/venv/bin/python" -I "$VIDEO/subtitulos.py" \
    "$trabajo/voz" "$escenas" "$trabajo/subtitulos.json" $( [ -f "$voz/guion.json" ] && echo "$voz/guion.json" )
  subtitulos=(--subtitulos "$trabajo/subtitulos.json" --entra "$ENTRA")
fi

node "$trabajo/video/renderizar_video.mjs" "$trabajo/video/$nombre.html" "$trabajo/cuadros" \
  --voz "$(IFS=,; echo "${duraciones[*]}")" "${subtitulos[@]}"

# Cada frase en su lugar, todas juntas en una pista del largo del video.
total=$(python3 -c "import json,sys; e=json.load(open(sys.argv[1])); print(e[-1]['inicio']+e[-1]['dur'])" "$trabajo/cuadros/escenas.json")
entradas=(); filtros=""; k=0
for i in $(seq 1 "$escenas"); do
  n=$(printf '%02d' "$i")
  [ -f "$trabajo/voz/$n.wav" ] || continue
  ms=$(python3 -c "import json,sys; print(round((json.load(open(sys.argv[1]))[int(sys.argv[2])]['inicio'] + float(sys.argv[3])) * 1000))" \
    "$trabajo/cuadros/escenas.json" "$((i - 1))" "$ENTRA")
  entradas+=(-i "$trabajo/voz/$n.wav")
  filtros+="[$k:a]adelay=${ms}:all=1[v$k];"; k=$((k + 1))
done
[ "$k" -gt 0 ] || { echo "La carpeta $voz no tiene ninguna grabación 01.*, 02.*…" >&2; exit 1; }
mezcla=$(for j in $(seq 0 $((k - 1))); do printf '[v%d]' "$j"; done)
ffmpeg -v error -y "${entradas[@]}" -filter_complex \
  "${filtros}${mezcla}amix=inputs=$k:normalize=0,apad,atrim=0:$total,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]" \
  -map '[a]' -ac 2 "$trabajo/voz.wav"

mkdir -p "$(dirname "$destino")"
ffmpeg -v error -y -framerate 30 -i "$trabajo/cuadros/%05d.jpg" -i "$trabajo/voz.wav" -shortest \
  -vf scale=in_range=pc:out_range=tv,format=yuv420p -color_range tv \
  -c:v libx264 -preset slow -crf 19 -profile:v high -r 30 \
  -c:a aac -b:a 160k -movflags +faststart "$destino"
printf '%s · %.1f s\n' "$destino" "$total"
