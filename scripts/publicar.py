#!/usr/bin/env python3
"""Publica en Instagram una pieza aprobada de la cola: carrusel, foto o reel.

    python3 scripts/publicar.py <pieza.json> [--simular] [--ahora AAAA-MM-DDTHH:MM]

<pieza.json> es el documento de la colección `piezas` tal como lo guarda
ArtifactData con `out_dir` (sólo los campos; el id es el nombre del archivo).

Antes de tocar Instagram comprueba, y se niega a seguir si algo falla:
  1. que la pieza esté `aprobada` y que su hora (de Chile) ya haya llegado;
  2. que la huella de aprobación coincida con lo que hay ahora en la pieza;
  3. que cada JPEG que baja de GitHub tenga el SHA-256 de `imagenesSha`;
  4. que no esté ya publicada (por si una pasada anterior se cortó a medias).

Con --simular hace todo eso y lee la cuenta, pero no publica nada.

El token NO pasa por aquí: en la nube, un "network secret" del entorno agrega
`Authorization: Bearer …` a toda petición hacia graph.instagram.com. Para
probar en local se puede poner IG_TOKEN en el entorno.

Escribe en stdout UNA línea JSON con el resultado:
  {"ok": true, "id": ..., "enlace": ..., "media_id": ..., "ya_estaba": bool}
  {"ok": false, "id": ..., "error": "...", "reintentable": bool}
Sale con 0 si publicó (o simuló bien) y con 1 si no.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API = "https://graph.instagram.com/v25.0"
REPO = "jokopro9453/tallermax-marketing"
RAIZ = Path(__file__).resolve().parent.parent
# Todo se descarga y se verifica desde raw.githubusercontent.com, que es lo que la
# red del entorno en la nube deja pasar (cdn.jsdelivr.net da 403 desde ahí).
# A Instagram, en cambio, los videos se le entregan por jsDelivr: GitHub los sirve
# como application/octet-stream e Instagram pide video/mp4.
# Las dos direcciones van FIJADAS al commit, no a `main`: así lo que se verifica y
# lo que baja Instagram es el mismo objeto de git, y jsDelivr no puede entregar
# una versión vieja de caché (a una rama la guarda hasta 12 horas).
CRUDO = "https://raw.githubusercontent.com/{repo}/{commit}/"
CDN = "https://cdn.jsdelivr.net/gh/{repo}@{commit}/"
ZONA = ZoneInfo("America/Santiago")
LIMITE_TEXTO = 2200
LIMITE_HASHTAGS = 30
LIMITE_IMAGENES = 10


class Rechazo(Exception):
    """La pieza no se publica. `reintentable` dice si vale la pena volver a intentar."""

    def __init__(self, mensaje: str, reintentable: bool = False) -> None:
        super().__init__(mensaje)
        self.reintentable = reintentable


def huella(p: dict) -> str:
    """La misma que calcula la página: sha256 de JSON.stringify([...])."""

    def lista(x: object) -> list:
        return x if isinstance(x, list) else []

    datos = [p.get("fecha") or "", p.get("tipo") or "", p.get("texto") or "", lista(p.get("imagenes")), lista(p.get("imagenesSha"))]
    texto = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def ahora_chile() -> str:
    return datetime.now(ZONA).strftime("%Y-%m-%dT%H:%M")


def pedir(metodo: str, url: str, datos: dict | None = None) -> dict:
    cuerpo = urllib.parse.urlencode(datos).encode() if datos is not None else None
    req = urllib.request.Request(url, data=cuerpo, method=metodo)
    token = os.environ.get("IG_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read()).get("error", {})
        except (ValueError, AttributeError):
            err = {}
        codigo = err.get("code")
        if codigo == 190:
            raise Rechazo("Instagram rechazó el token: falta, venció o fue revocado. Hay que generar uno "
                          "nuevo y reemplazar el network secret del entorno tallermax-marketing.") from None
        if codigo in (4, 17, 32, 613) or e.code == 429:
            raise Rechazo(f"Instagram pide esperar (límite de uso): {err.get('message', e.reason)}", True) from None
        raise Rechazo(f"Instagram respondió {e.code}: {err.get('message', e.reason)}", e.code >= 500) from None
    except urllib.error.URLError as e:
        raise Rechazo(f"No se pudo conectar con {urllib.parse.urlparse(url).netloc}: {e.reason}", True) from None


def validar(p: dict, ahora: str) -> list[str]:
    if p.get("estado") != "aprobada":
        raise Rechazo(f"La pieza está «{p.get('estado')}», no «aprobada».")
    fecha = p.get("fecha") or ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", fecha):
        raise Rechazo(f"Fecha inválida: {fecha!r}")
    if fecha > ahora:
        raise Rechazo(f"Todavía no es su hora ({fecha}; en Chile son las {ahora}).", True)
    if p.get("huellaAprobada") != huella(p):
        raise Rechazo("La pieza cambió después de aprobarse (la huella no coincide). Hay que volver a aprobarla.")
    tipo = p.get("tipo")
    if tipo not in ("carrusel", "foto", "reel"):
        raise Rechazo(f"El publicador no sabe publicar «{tipo}».")
    imagenes, shas = p.get("imagenes") or [], p.get("imagenesSha") or []
    if len(imagenes) != len(shas):
        raise Rechazo("`imagenes` e `imagenesSha` no tienen el mismo largo.")
    if tipo == "foto" and len(imagenes) != 1:
        raise Rechazo("Una foto lleva exactamente una imagen.")
    if tipo == "reel" and (len(imagenes) != 1 or not imagenes[0].lower().endswith(".mp4")):
        raise Rechazo("Un reel lleva exactamente un video .mp4 en `imagenes`.")
    if tipo == "carrusel" and not 2 <= len(imagenes) <= LIMITE_IMAGENES:
        raise Rechazo(f"Un carrusel lleva entre 2 y {LIMITE_IMAGENES} imágenes; esta tiene {len(imagenes)}.")
    texto = p.get("texto") or ""
    if len(texto) > LIMITE_TEXTO:
        raise Rechazo(f"El texto tiene {len(texto)} caracteres; el máximo es {LIMITE_TEXTO}.")
    if len(re.findall(r"#\w+", texto)) > LIMITE_HASHTAGS:
        raise Rechazo(f"Más de {LIMITE_HASHTAGS} hashtags.")
    return imagenes


def commit_actual() -> str:
    """El commit del clon (en la nube, el último de main). Si no hay git, `main`."""
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RAIZ, capture_output=True, text=True, check=True, timeout=10)
        commit = r.stdout.strip()
        return commit if re.fullmatch(r"[0-9a-f]{40}", commit) else "main"
    except (OSError, subprocess.SubprocessError):
        return "main"


def verificar_imagenes(imagenes: list[str], shas: list[str]) -> list[str]:
    """Baja cada archivo de GitHub, comprueba que sea el que se aprobó y devuelve
    la dirección que se le da a Instagram."""
    commit = commit_actual()
    crudo, cdn = CRUDO.format(repo=REPO, commit=commit), CDN.format(repo=REPO, commit=commit)
    urls = []
    for ruta, sha in zip(imagenes, shas):
        if not re.fullmatch(r"piezas/[\w.-]+/[\w.-]+\.(jpe?g|mp4)", ruta, re.IGNORECASE):
            raise Rechazo(f"Ruta de imagen no permitida: {ruta!r}")
        es_video = ruta.lower().endswith(".mp4")
        url = crudo + ruta
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                datos = r.read()
        except urllib.error.URLError as e:
            raise Rechazo(f"No se pudo bajar {ruta}: {e}", True) from None
        if es_video and datos[4:8] != b"ftyp":
            raise Rechazo(f"{ruta} no es un MP4.")
        if not es_video and datos[:3] != b"\xff\xd8\xff":
            raise Rechazo(f"{ruta} no es un JPEG.")
        real = hashlib.sha256(datos).hexdigest()
        if real != sha:
            raise Rechazo(f"{ruta} no es la imagen que se aprobó (SHA-256 distinto). ¿Se regeneró sin "
                          "actualizar imagenesSha, o falta hacer push?")
        urls.append(cdn + ruta if es_video else url)
    return urls


def esperar_contenedor(cid: str, intentos: int = 30, pausa: float = 3) -> None:
    """Espera a que Instagram procese el contenedor. Un video tarda bastante más."""
    for _ in range(intentos):
        estado = pedir("GET", f"{API}/{cid}?fields=status_code").get("status_code")
        if estado == "FINISHED":
            return
        if estado in ("ERROR", "EXPIRED"):
            raise Rechazo(f"Instagram no pudo procesar el contenedor {cid} ({estado}).", True)
        time.sleep(pausa)
    raise Rechazo(f"El contenedor {cid} no terminó de procesarse a tiempo.", True)


def ya_publicada(ig: str, texto: str) -> dict | None:
    recientes = pedir("GET", f"{API}/{ig}/media?fields=id,caption,permalink&limit=15").get("data", [])
    return next((m for m in recientes if (m.get("caption") or "").strip() == texto.strip()), None)


def publicar(p: dict, simular: bool, ahora: str) -> dict:
    imagenes = validar(p, ahora)
    urls = verificar_imagenes(imagenes, p.get("imagenesSha") or [])
    yo = pedir("GET", f"{API}/me?fields=user_id,username")
    ig = yo.get("user_id")
    if not ig:
        raise Rechazo("Instagram no devolvió la cuenta (¿falta el network secret en el entorno?).")

    previa = ya_publicada(ig, p.get("texto") or "")
    if previa:
        return {"ok": True, "ya_estaba": True, "media_id": previa["id"], "enlace": previa.get("permalink")}
    if simular:
        return {"ok": True, "simulado": True, "cuenta": yo.get("username"), "imagenes": len(urls)}

    texto = p.get("texto") or ""
    if p["tipo"] == "reel":
        contenedor = pedir("POST", f"{API}/{ig}/media", {
            "media_type": "REELS", "video_url": urls[0], "caption": texto, "share_to_feed": "true",
            "thumb_offset": str(int(p.get("portadaMs") or 0)),
        })["id"]
        esperar_contenedor(contenedor, intentos=40, pausa=8)
    elif p["tipo"] == "foto":
        contenedor = pedir("POST", f"{API}/{ig}/media", {"image_url": urls[0], "caption": texto})["id"]
    else:
        hijos = [pedir("POST", f"{API}/{ig}/media", {"image_url": u, "is_carousel_item": "true"})["id"] for u in urls]
        for h in hijos:
            esperar_contenedor(h)
        contenedor = pedir("POST", f"{API}/{ig}/media",
                           {"media_type": "CAROUSEL", "children": ",".join(hijos), "caption": texto})["id"]
    esperar_contenedor(contenedor)
    media = pedir("POST", f"{API}/{ig}/media_publish", {"creation_id": contenedor})["id"]
    enlace = pedir("GET", f"{API}/{media}?fields=permalink").get("permalink")
    return {"ok": True, "ya_estaba": False, "media_id": media, "enlace": enlace}


def main() -> int:
    args = sys.argv[1:]
    simular = "--simular" in args
    ahora = ahora_chile()
    if "--ahora" in args:
        ahora = args[args.index("--ahora") + 1]
    archivos = [a for a in args if a.endswith(".json")]
    if len(archivos) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    ruta = Path(archivos[0])
    pid = ruta.stem
    try:
        pieza = json.loads(ruta.read_text(encoding="utf-8"))
        resultado = {"id": pid, **publicar(pieza, simular, ahora)}
        codigo = 0
    except Rechazo as e:
        resultado = {"id": pid, "ok": False, "error": str(e), "reintentable": e.reintentable}
        codigo = 1
    print(json.dumps(resultado, ensure_ascii=False))
    return codigo


if __name__ == "__main__":
    sys.exit(main())
