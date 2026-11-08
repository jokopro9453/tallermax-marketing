#!/usr/bin/env python3
"""Transcribe cada frase grabada y dice cuándo empieza y termina cada palabra.

    python3 subtitulos.py <carpeta-con-01.wav…> <cantidad-de-escenas> <salida.json> [guion.json]

Escribe una lista con una entrada por escena: la lista de palabras de su frase
({"p": palabra, "a": inicio, "b": fin}, en segundos desde que empieza la frase),
o una lista vacía si la escena no tiene voz. reel.js las pone en pantalla.

Usa faster-whisper con el modelo `small` en CPU. Whisper no conoce la marca, así
que lo que oye como «Taller Max» se corrige a «Tallermax».

Con guion.json (una frase por escena, lo que se pidió decir) cada palabra que
Whisper oyó parecida a la del guion se escribe como en el guion, con el tiempo
que oyó. Donde Joaquín dijo otra cosa, queda lo que dijo.
"""

import json
import re
import unicodedata
from difflib import SequenceMatcher
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

CORRECCIONES = [(re.compile(r"^taller\s*max", re.I), "Tallermax"), (re.compile(r"^quilpu[eé]", re.I), "Quilpué")]
CONTEXTO = "Tallermax, sistema para talleres mecánicos en Quilpué. Patente, rayón, constancia, WhatsApp."


def corregir(palabras: list[dict]) -> list[dict]:
    """Junta «Taller» + «Max» en una palabra y aplica las correcciones de marca."""
    out: list[dict] = []
    for w in palabras:
        if out and out[-1]["p"].lower() == "taller" and w["p"].lower().strip(".,") == "max":
            out[-1] = {"p": "Tallermax" + w["p"][3:], "a": out[-1]["a"], "b": w["b"]}
            continue
        for patron, bien in CORRECCIONES:
            w["p"] = patron.sub(bien, w["p"])
        out.append(w)
    return out


def _base(p: str) -> str:
    sin_tilde = unicodedata.normalize("NFD", p.lower())
    return "".join(c for c in sin_tilde if c.isalnum())


def con_guion(oidas: list[dict], frase: str) -> list[dict]:
    """Pone la ortografía del guion sobre los tiempos de lo oído."""
    dichas = frase.split()
    a, b = [_base(w["p"]) for w in oidas], [_base(p) for p in dichas]
    out: list[dict] = []
    calce = SequenceMatcher(None, a, b, autojunk=False)
    # Si la frase entera calza casi toda, una palabra cambiada por otra es un error
    # de oído («pelo» por «dedo», «7» por «siete»), no algo que dijo distinto.
    casi_igual = calce.ratio() >= 0.8
    for op, i1, i2, j1, j2 in calce.get_opcodes():
        if op == "equal" or (op == "replace" and casi_igual and i2 - i1 == j2 - j1):
            out += [{**oidas[i], "p": dichas[j]} for i, j in zip(range(i1, i2), range(j1, j2))]
        elif op == "replace" and i2 > i1 and SequenceMatcher(None, " ".join(a[i1:i2]), " ".join(b[j1:j2])).ratio() >= 0.6:
            # Lo oído se parece al guion: sus palabras, repartidas en el mismo tramo.
            ini, fin, n = oidas[i1]["a"], oidas[i2 - 1]["b"], j2 - j1
            paso = (fin - ini) / n
            out += [{"p": dichas[j1 + k], "a": round(ini + k * paso, 2), "b": round(ini + (k + 1) * paso, 2)} for k in range(n)]
        elif op != "insert":
            out += oidas[i1:i2]  # dijo otra cosa: queda lo que dijo
    return out


def leer(wav: Path) -> np.ndarray:
    """El audio a 16 kHz mono, decodificado con el ffmpeg del sistema (el PyAV
    que trae faster-whisper cambia de interfaz entre versiones)."""
    crudo = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                           check=True, capture_output=True).stdout
    return np.frombuffer(crudo, dtype=np.float32)


def main() -> int:
    carpeta, escenas, salida = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
    guion = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8")) if len(sys.argv) > 4 else []
    modelo = WhisperModel("small", device="cpu", compute_type="int8")
    resultado = []
    for i in range(1, escenas + 1):
        wav = carpeta / f"{i:02d}.wav"
        if not wav.exists():
            resultado.append([])
            continue
        segmentos, _ = modelo.transcribe(leer(wav), language="es", word_timestamps=True, initial_prompt=CONTEXTO,
                                         vad_filter=False, beam_size=5)
        palabras = [{"p": w.word.strip(), "a": round(w.start, 2), "b": round(w.end, 2)}
                    for s in segmentos for w in (s.words or []) if w.word.strip()]
        palabras = corregir(palabras)
        if i <= len(guion) and guion[i - 1]:
            palabras = con_guion(palabras, guion[i - 1])
        resultado.append(palabras)
        print(f"escena {i:02d}: {' '.join(w['p'] for w in palabras)}")
    salida.write_text(json.dumps(resultado, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
