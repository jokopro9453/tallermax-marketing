#!/usr/bin/env python3
"""Edita un video grabado con el celular y lo deja listo para Instagram.

    python3 editar_toma.py <toma.mp4> <salida.mp4> --trabajo <carpeta> --firma <firma.png>
        --cierre <cierre.mp4> [--guion guion.txt] [--insertos insertos.json] [--musica pista.mp3] [--sin-cortes]

Lo lanza editar_toma.sh, que prepara el entorno. Hace, en orden:

1. **Voz.** Quita el zumbido grave, reduce el ruido con RNNoise (una red
   neuronal entrenada con voz grabada), baja las «s» silbantes, saca el barro
   de los medios, le da presencia a la voz, la comprime y la deja en -16 LUFS,
   el volumen al que Instagram no le baja.
2. **Cortes.** Transcribe con faster-whisper y se queda sólo con lo hablado:
   saca los silencios largos y, cuando Joaquín se equivoca, hace una pausa y
   repite la frase, bota la toma mala y deja la última.
3. **Imagen.** Lleva el video a 1080 × 1920 vertical (recortando, nunca
   estirando) y a 30 cuadros, con la firma de Tallermax arriba y subtítulos
   palabra por palabra, con la que se está diciendo en amarillo.
4. **Insertos.** Si se le pasan, pone clips encima (por ejemplo la pantalla del
   teléfono) cuando se dice una frase, sin cortar la voz.
5. **Música.** Si se le pasa una pista, la pone de fondo y la baja sola cada
   vez que Joaquín habla, para que nunca tape la voz.
6. **Cierre.** Pega al final la tarjeta con el logo y «Pruébalo gratis 7 días».

Escribe en stdout UNA línea JSON con lo que hizo: duración, cortes, tomas
botadas y la transcripción final.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from subtitulos import con_guion, corregir, leer  # noqa: E402

AQUI = Path(__file__).resolve().parent
RNNOISE = AQUI / "rnnoise" / "somnolent-hogwash.rnnn"
FUENTES = AQUI.parent / "fuentes"
ANCHO, ALTO, FPS = 1080, 1920, 30

# La cadena de la voz. Cada filtro, en el orden en que suena:
VOZ = ",".join([
    "highpass=f=80",                                  # golpes de mesa, motor, viento
    f"arnndn=m='{RNNOISE}':mix=0.9",                  # ruido de fondo (red neuronal)
    "afftdn=nf=-30:tn=1",                             # lo que quede de ruido parejo
    "deesser=i=0.35:m=0.5:f=0.5",                     # «s» silbantes
    "equalizer=f=250:t=q:w=1.2:g=-2.5",               # barro de pieza chica
    "equalizer=f=3500:t=q:w=1.0:g=2.5",               # presencia: que se entienda
    "acompressor=threshold=-22dB:ratio=3:attack=8:release=150:makeup=2",
])
HUECO = 0.45    # silencio que corta una frase de la siguiente
ANTES = 0.12    # aire que se deja antes de cada frase
DESPUES = 0.22  # y después
PAUSA_DE_ERROR = 1.0  # la pausa que hace Joaquín antes de repetir una frase


def correr(*cmd: str) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def duracion(archivo: Path) -> float:
    return float(correr("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(archivo)))


def es_hdr(archivo: Path) -> bool:
    t = correr("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
               "-of", "csv=p=0", str(archivo)).strip()
    return t in ("smpte2084", "arib-std-b67")


def _norm(p: str) -> str:
    s = unicodedata.normalize("NFD", p.lower())
    return "".join(c for c in s if c.isalnum())


# ── 1. Voz ───────────────────────────────────────────────────────────────────


def limpiar_voz(toma: Path, salida: Path) -> None:
    """La voz limpia y en -16 LUFS, en dos pasadas (la primera mide)."""
    crudo = salida.with_name("voz-cruda.wav")
    correr("ffmpeg", "-v", "error", "-y", "-i", str(toma), "-vn", "-ac", "1", "-ar", "48000", "-af", VOZ, str(crudo))
    medida = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(crudo), "-af",
                             "loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True, check=True).stderr
    m = json.loads(medida[medida.rindex("{"):medida.rindex("}") + 1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    correr("ffmpeg", "-v", "error", "-y", "-i", str(crudo), "-af", f"{ln},alimiter=limit=0.89,aresample=48000",
           "-ac", "1", str(salida))


# ── 2. Cortes ────────────────────────────────────────────────────────────────


def palabras_de(voz: Path, guion: str | None) -> list[dict]:
    from faster_whisper import WhisperModel
    modelo = WhisperModel("small", device="cpu", compute_type="int8")
    contexto = "Tallermax, sistema para talleres mecánicos en Quilpué. Patente, rayón, constancia, WhatsApp."
    segs, _ = modelo.transcribe(leer(voz), language="es", word_timestamps=True, initial_prompt=contexto,
                                vad_filter=True, beam_size=5)
    palabras = corregir([{"p": w.word.strip(), "a": round(w.start, 2), "b": round(w.end, 2)}
                         for s in segs for w in (s.words or []) if w.word.strip()])
    return con_guion(palabras, guion) if guion else palabras


def frases(palabras: list[dict]) -> list[list[dict]]:
    """Agrupa las palabras en frases: un silencio de más de HUECO las separa."""
    out: list[list[dict]] = []
    for w in palabras:
        if out and w["a"] - out[-1][-1]["b"] <= HUECO:
            out[-1].append(w)
        else:
            out.append([w])
    return out


def es_repeticion(mala: list[dict], buena: list[dict]) -> bool:
    """¿La frase `buena` vuelve a decir lo que `mala` empezó a decir?"""
    a = [_norm(w["p"]) for w in mala]
    b = [_norm(w["p"]) for w in buena][: len(a) + 2]
    if len(a) < 2 or len(b) < 2:
        return False
    # Basta con que arranque igual: la toma mala suele quedar a medias.
    n = min(len(a), len(b), 6)
    return SequenceMatcher(None, a[:n], b[:n], autojunk=False).ratio() >= 0.7


def elegir(fr: list[list[dict]]) -> tuple[list[list[dict]], list[str]]:
    """Bota cada frase que se repite más adelante después de una pausa."""
    botadas: list[str] = []
    quedan: list[list[dict]] = []
    for i, f in enumerate(fr):
        siguientes = fr[i + 1:i + 4]
        pausa = fr[i + 1][0]["a"] - f[-1]["b"] if i + 1 < len(fr) else 0
        if pausa >= PAUSA_DE_ERROR and any(es_repeticion(f, s) for s in siguientes):
            botadas.append(" ".join(w["p"] for w in f))
            continue
        quedan.append(f)
    return quedan, botadas


def tramos(fr: list[list[dict]], largo: float) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for f in fr:
        a, b = max(0.0, f[0]["a"] - ANTES), min(largo, f[-1]["b"] + DESPUES)
        if out and a <= out[-1][1] + 0.05:
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
    return out


def remapear(fr: list[list[dict]], tr: list[tuple[float, float]]) -> list[dict]:
    """Las palabras con su tiempo en el video ya cortado."""
    out, base = [], 0.0
    inicio = [0.0]
    for a, b in tr:
        base += b - a
        inicio.append(base)
    for f in fr:
        for w in f:
            k = next(i for i, (a, b) in enumerate(tr) if a - 0.01 <= w["a"] <= b + 0.01)
            d = inicio[k] - tr[k][0]
            out.append({"p": w["p"], "a": round(w["a"] + d, 2), "b": round(w["b"] + d, 2)})
    return out


# ── 3. Subtítulos ────────────────────────────────────────────────────────────


def _t(s: float) -> str:
    h, r = divmod(max(s, 0), 3600)
    m, r = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{r:05.2f}"


def ass(palabras: list[dict]) -> str:
    """Subtítulos ASS: de a pocas palabras, la que se dice en amarillo. Mismo
    corte que reel.js: hasta 4 palabras, o antes en un punto o una coma."""
    grupos, actual = [], []
    for k, w in enumerate(palabras):
        actual.append(w)
        fin = re.search(r"[.;:?!…»]$", w["p"]) or (w["p"].endswith(",") and len(actual) >= 2)
        if fin or len(actual) == 4 or k == len(palabras) - 1:
            grupos.append(actual)
            actual = []
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {ANCHO}
PlayResY: {ALTO}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter,66,&H00FFFFFF,&H00FFFFFF,&H38181312,&H38181312,-1,0,0,0,100,100,0,0,3,14,0,2,80,80,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lineas = []
    for gi, g in enumerate(grupos):
        hasta = min(g[-1]["b"] + 0.35, grupos[gi + 1][0]["a"] if gi + 1 < len(grupos) else 1e9)
        for wi, w in enumerate(g):
            a = w["a"] if wi else g[0]["a"]
            b = g[wi + 1]["a"] if wi + 1 < len(g) else hasta
            if b <= a:
                continue
            texto = " ".join(("{\\c&H3DC5FF&}" + x["p"] + "{\\c&HFFFFFF&}") if xi == wi else x["p"]
                             for xi, x in enumerate(g))
            lineas.append(f"Dialogue: 0,{_t(a)},{_t(b)},Sub,,0,0,0,,{texto}")
    return cab + "\n".join(lineas) + "\n"


# ── 4 y 5. Video final ───────────────────────────────────────────────────────


def buscar(palabras: list[dict], frase: str) -> float | None:
    objetivo = [_norm(x) for x in frase.split()]
    dichas = [_norm(w["p"]) for w in palabras]
    for i in range(len(dichas) - len(objetivo) + 1):
        if SequenceMatcher(None, dichas[i:i + len(objetivo)], objetivo).ratio() >= 0.8:
            return palabras[i]["a"]
    return None


def armar(toma: Path, voz: Path, tr: list[tuple[float, float]], subs: Path, firma: Path, cierre: Path,
          insertos: list[dict], palabras: list[dict], salida: Path, trabajo: Path, musica: Path | None) -> list[dict]:
    hdr = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv," if es_hdr(toma) else ""
    cuadro = (f"{hdr}scale={ANCHO}:{ALTO}:force_original_aspect_ratio=increase,crop={ANCHO}:{ALTO},"
              f"fps={FPS},format=yuv420p")
    partes = [f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];[1:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]"
              for i, (a, b) in enumerate(tr)]
    une = "".join(f"[v{i}][a{i}]" for i in range(len(tr))) + f"concat=n={len(tr)}:v=1:a=1[vc][ac]"
    filtro = ";".join(partes) + ";" + une + f";[vc]{cuadro}[base]"
    entradas = ["-i", str(toma), "-i", str(voz), "-loop", "1", "-i", str(firma)]
    actual, usados = "base", []
    for k, ins in enumerate(insertos):
        desde = buscar(palabras, ins["frase"])
        if desde is None:
            usados.append({**ins, "puesto": False})
            continue
        largo = float(ins.get("dur", min(4.0, duracion(Path(ins["archivo"])))))
        entradas += ["-i", ins["archivo"]]
        n = 3 + k
        filtro += (f";[{n}:v]trim=0:{largo:.2f},setpts=PTS-STARTPTS+{desde:.2f}/TB,scale={ANCHO}:{ALTO}:"
                   f"force_original_aspect_ratio=increase,crop={ANCHO}:{ALTO},fps={FPS},format=yuv420p[i{k}];"
                   f"[{actual}][i{k}]overlay=eof_action=pass:enable='between(t,{desde:.2f},{desde + largo:.2f})'[o{k}]")
        actual = f"o{k}"
        usados.append({**ins, "puesto": True, "desde": desde, "dur": largo})
    audio = "ac"
    if musica:
        entradas += ["-stream_loop", "-1", "-i", str(musica)]
        n = 3 + len(insertos)
        # La música a un cuarto del volumen, y se agacha (comprime) cada vez que hay voz.
        filtro += (f";[ac]asplit=2[voz1][llave];[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.25[mus];"
                   "[mus][llave]sidechaincompress=threshold=0.02:ratio=10:attack=30:release=500[agachada];"
                   "[voz1][agachada]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[am]")
        audio = "am"
    subs_esc = str(subs).replace("\\", "/").replace(":", "\\:")
    filtro += (f";[{actual}][2:v]overlay=0:0:shortest=1[conf];"
               f"[conf]subtitles='{subs_esc}':fontsdir='{FUENTES}'[vf]")
    cuerpo = trabajo / "cuerpo.mp4"
    correr("ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", filtro, "-map", "[vf]", "-map", f"[{audio}]",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", str(cuerpo))
    lista = trabajo / "lista.txt"
    lista.write_text(f"file '{cuerpo}'\nfile '{cierre}'\n")
    correr("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy",
           "-movflags", "+faststart", str(salida))
    return usados


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("toma", type=Path)
    p.add_argument("salida", type=Path)
    p.add_argument("--trabajo", type=Path, required=True)
    p.add_argument("--firma", type=Path, required=True)
    p.add_argument("--cierre", type=Path, required=True)
    p.add_argument("--guion", type=Path, help="lo que se pidió decir: los subtítulos usan su ortografía")
    p.add_argument("--insertos", type=Path, help='JSON: [{"archivo": "pantalla.mp4", "frase": "cuatro fotos", "dur": 3}]')
    p.add_argument("--musica", type=Path, help="pista de fondo (sólo con licencia para usarla en anuncios)")
    p.add_argument("--sin-cortes", action="store_true", help="no sacar silencios ni tomas repetidas")
    a = p.parse_args()
    a.trabajo.mkdir(parents=True, exist_ok=True)

    voz = a.trabajo / "voz.wav"
    limpiar_voz(a.toma, voz)
    guion = a.guion.read_text(encoding="utf-8") if a.guion else None
    palabras = palabras_de(voz, guion)
    if not palabras:
        print(json.dumps({"ok": False, "error": "No se oye nada que transcribir en la toma."}, ensure_ascii=False))
        return 1
    largo = duracion(voz)
    fr = frases(palabras)
    if a.sin_cortes:
        quedan, botadas, tr = fr, [], [(0.0, largo)]
    else:
        quedan, botadas = elegir(fr)
        tr = tramos(quedan, largo)
    finales = remapear(quedan, tr)
    subs = a.trabajo / "subtitulos.ass"
    subs.write_text(ass(finales), encoding="utf-8")
    insertos = json.loads(a.insertos.read_text(encoding="utf-8")) if a.insertos else []
    usados = armar(a.toma, voz, tr, subs, a.firma, a.cierre, insertos, finales, a.salida, a.trabajo, a.musica)
    print(json.dumps({
        "ok": True, "salida": str(a.salida), "duracion_toma": round(largo, 1), "duracion_final": round(duracion(a.salida), 1),
        "tramos": len(tr), "tomas_botadas": botadas, "insertos": usados,
        "texto": " ".join(w["p"] for w in finales),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
