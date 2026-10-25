#!/usr/bin/env python3
"""Piloto de la campaña de Meta de Tallermax: lee los resultados y pausa lo que no rinde.

    python3 scripts/anuncios.py cuentas [--falso escenario.json]
    python3 scripts/anuncios.py revisar [--cuenta act_<id>] [--aplicar] [--hoy AAAA-MM-DD] [--falso escenario.json]
    python3 scripts/anuncios.py activar <id_anuncio> [--cuenta act_<id>] [--hoy ...] [--falso ...]

`cuentas` dice qué cuentas publicitarias ve el token y con qué permisos: es lo
primero que se corre con un token nuevo. Sin --cuenta, revisar y activar usan
la `cuenta` de anuncios/campana.json.

Lo que PUEDE hacer, y nada más:
  * leer la cuenta publicitaria, sus campañas, sus anuncios y sus resultados;
  * PAUSAR un anuncio o una campaña cuyo nombre empiece con el prefijo de
    anuncios/campana.json (las demás campañas de la cuenta ni se miran);
  * ACTIVAR un anuncio de esas campañas, sólo con la orden `activar`, y sólo si
    su campaña respeta el tope y todavía no pasa su fecha de término.
Nunca crea nada ni cambia un presupuesto, una puja, un público o el límite de
gasto de la cuenta. Pausar no gasta plata: por eso es lo único que hace solo.

Las reglas (los números están en anuncios/campana.json):
  0. Barandas. Se pausa la campaña entera si tiene presupuesto diario (tiene que
     ser total, para que Meta no pueda pasarse), si su presupuesto total supera
     el tope, si lo gastado ya llegó al tope o si pasó la fecha de término.
  1. Un anuncio se juzga sólo cuando lleva `dias_minimos` días al aire y gastó
     `gasto_minimo_para_juzgar`. Antes de eso, cualquier conclusión es ruido.
  2. Se pausa si gastó eso sin una sola conversación.
  3. Se pausa si cada conversación le sale más de `multiplo_costo` veces lo que
     al mejor anuncio (que necesita `conversaciones_minimas_ganador` para valer
     como referencia).
  4. Las reglas 2 y 3 nunca dejan una campaña sin anuncios activos. Pero si la
     campaña entera gastó `gasto_sin_resultado_campana` sin una conversación, se
     pausa completa: algo está mal armado, casi siempre el WhatsApp de destino.

El token no pasa por aquí: en la nube, un "network secret" del entorno agrega
`Authorization: Bearer …` a las peticiones hacia graph.facebook.com. Para
probar en local se puede poner META_TOKEN en el entorno.

Escribe en stdout UNA línea JSON, el informe. Sale con 0 si leyó todo y cada
acción salió bien, y con 1 si no.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API = "https://graph.facebook.com/v25.0"
CONFIG = Path(__file__).resolve().parent.parent / "anuncios" / "campana.json"
ZONA = ZoneInfo("America/Santiago")
# Meta guarda los presupuestos en la unidad mínima de la moneda. El peso chileno
# no tiene centavos (factor 1); el dólar sí (factor 100). Una moneda que no esté
# aquí se rechaza en vez de adivinar su factor.
FACTOR = {"CLP": 1, "USD": 100}
CAMPOS_CAMPANA = "id,name,status,effective_status,objective,daily_budget,lifetime_budget,start_time,stop_time"
CAMPOS_ANUNCIO = "id,name,status,effective_status,created_time,adset_id"
CAMPOS_RESULTADO = "ad_id,ad_name,spend,impressions,reach,clicks,actions"
ESTADOS_CON_PROBLEMA = {"DISAPPROVED", "WITH_ISSUES"}
# Lo que el token necesita. public_profile lo concede Meta siempre.
PERMISOS_ESPERADOS = {"ads_management", "ads_read", "public_profile"}


class Fallo(Exception):
    """No se pudo leer o actuar. El mensaje va tal cual al informe."""


# ── Acceso a Meta ────────────────────────────────────────────────────────────


class ApiReal:
    def _pedir(self, metodo: str, url: str, datos: dict | None = None) -> dict:
        cuerpo = urllib.parse.urlencode(datos).encode() if datos is not None else None
        req = urllib.request.Request(url, data=cuerpo, method=metodo)
        token = os.environ.get("META_TOKEN")
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
            if not err and e.code == 403:
                raise Fallo("La red de la nube bloqueó graph.facebook.com (403 sin respuesta de Meta). Hay que "
                            "permitir ese dominio en el acceso a la red del entorno.") from None
            if err.get("code") == 190:
                raise Fallo("Meta rechazó el token: falta, venció o fue revocado. Hay que generar uno nuevo "
                            "para el usuario del sistema y reemplazar el network secret del entorno.") from None
            if err.get("code") in (4, 17, 32, 613, 80004) or e.code == 429:
                raise Fallo(f"Meta pide esperar (límite de uso): {err.get('message', e.reason)}") from None
            raise Fallo(f"Meta respondió {e.code}: {err.get('message', e.reason)}") from None
        except urllib.error.URLError as e:
            raise Fallo(f"No se pudo conectar con graph.facebook.com: {e.reason}") from None

    def get(self, ruta: str, params: dict | None = None) -> dict:
        url = ruta if ruta.startswith("https://") else f"{API}/{ruta}?{urllib.parse.urlencode(params or {})}"
        return self._pedir("GET", url)

    def post(self, ruta: str, datos: dict) -> dict:
        return self._pedir("POST", f"{API}/{ruta}", datos)


class ApiFalsa:
    """Responde con un escenario guardado ({"get": {ruta: respuesta}}) y anota los POST."""

    def __init__(self, archivo: str) -> None:
        self.escenario = json.loads(Path(archivo).read_text(encoding="utf-8"))
        self.posts: list[tuple[str, dict]] = []

    def get(self, ruta: str, params: dict | None = None) -> dict:
        respuestas = self.escenario.get("get", {})
        if ruta not in respuestas:
            raise Fallo(f"(escenario) no hay respuesta para GET {ruta}")
        return respuestas[ruta]

    def post(self, ruta: str, datos: dict) -> dict:
        self.posts.append((ruta, datos))
        return {"success": True}


def todos(api, ruta: str, params: dict) -> list[dict]:
    """Junta todas las páginas de un listado (como mucho 10: aquí hay pocas cosas)."""
    filas: list[dict] = []
    respuesta = api.get(ruta, params)
    for _ in range(10):
        filas.extend(respuesta.get("data", []))
        siguiente = (respuesta.get("paging") or {}).get("next")
        if not siguiente:
            break
        respuesta = api.get(siguiente)
    return filas


# ── Números ──────────────────────────────────────────────────────────────────


def numero(valor: object) -> float:
    try:
        return float(valor)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def conversaciones(fila: dict, tipo: str) -> int:
    return sum(int(numero(a.get("value"))) for a in fila.get("actions") or [] if a.get("action_type") == tipo)


def fecha_meta(texto: str | None) -> date | None:
    """Meta escribe '2026-10-27T10:00:00-0300'. Se lleva a la fecha de Chile."""
    if not texto:
        return None
    try:
        return datetime.strptime(texto, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONA).date()
    except ValueError:
        return None


def costo(anuncio: dict) -> float | None:
    return anuncio["gasto"] / anuncio["conversaciones"] if anuncio["conversaciones"] else None


# ── Lectura ──────────────────────────────────────────────────────────────────


def leer(api, cuenta: str, config: dict) -> dict:
    if not re.fullmatch(r"act_\d+", cuenta):
        raise Fallo(f"La cuenta tiene que ser act_ seguido de números, no {cuenta!r}.")
    datos_cuenta = api.get(cuenta, {"fields": "name,currency,account_status,amount_spent,spend_cap"})
    moneda = datos_cuenta.get("currency")
    if moneda != config["moneda"]:
        raise Fallo(f"La cuenta publicitaria está en {moneda} y anuncios/campana.json en {config['moneda']}. "
                    "Hay que poner el tope en la moneda de la cuenta antes de seguir.")
    if moneda not in FACTOR:
        raise Fallo(f"No sé cómo guarda Meta los montos en {moneda}.")
    factor = FACTOR[moneda]

    campanas = []
    for c in todos(api, f"{cuenta}/campaigns", {"fields": CAMPOS_CAMPANA, "limit": 100}):
        if not (c.get("name") or "").startswith(config["prefijo"]):
            continue
        conjuntos = todos(api, f"{c['id']}/adsets", {"fields": "id,name,daily_budget,lifetime_budget", "limit": 100})
        anuncios = todos(api, f"{c['id']}/ads", {"fields": CAMPOS_ANUNCIO, "limit": 100})
        resultados = {r.get("ad_id"): r for r in todos(api, f"{c['id']}/insights", {
            "level": "ad", "fields": CAMPOS_RESULTADO, "date_preset": "maximum", "limit": 100})}
        inicio_campana = fecha_meta(c.get("start_time"))
        filas = []
        for a in anuncios:
            r = resultados.get(a["id"], {})
            creado = fecha_meta(a.get("created_time"))
            desde = max(d for d in (creado, inicio_campana) if d) if (creado or inicio_campana) else None
            filas.append({
                "id": a["id"], "nombre": a.get("name"), "estado": a.get("effective_status"),
                "desde": desde.isoformat() if desde else None,
                "gasto": round(numero(r.get("spend"))), "impresiones": int(numero(r.get("impressions"))),
                "alcance": int(numero(r.get("reach"))), "clics": int(numero(r.get("clicks"))),
                "conversaciones": conversaciones(r, config["accion_conversacion"]),
            })
        for f in filas:
            f["costo_conversacion"] = round(costo(f)) if costo(f) is not None else None
        campanas.append({
            "id": c["id"], "nombre": c.get("name"), "estado": c.get("status"),
            "estado_efectivo": c.get("effective_status"), "objetivo": c.get("objective"),
            "presupuesto_diario": numero(c.get("daily_budget")) / factor,
            "presupuesto_total": numero(c.get("lifetime_budget")) / factor,
            "conjuntos_diario": sum(numero(s.get("daily_budget")) for s in conjuntos) / factor,
            "conjuntos_total": sum(numero(s.get("lifetime_budget")) for s in conjuntos) / factor,
            "inicio": inicio_campana.isoformat() if inicio_campana else None,
            "termino": c.get("stop_time"),
            "gasto": sum(f["gasto"] for f in filas),
            "conversaciones": sum(f["conversaciones"] for f in filas),
            "anuncios": filas,
        })
    return {
        "cuenta": {"id": cuenta, "nombre": datos_cuenta.get("name"), "moneda": moneda,
                   "estado": datos_cuenta.get("account_status"),
                   "gastado_historico": numero(datos_cuenta.get("amount_spent")) / factor,
                   "limite_de_gasto": numero(datos_cuenta.get("spend_cap")) / factor or None},
        "campanas": campanas,
    }


def cuentas(api) -> dict:
    """Las cuentas publicitarias que ve el token y sus permisos. Sólo lee."""
    filas = todos(api, "me/adaccounts", {
        "fields": "name,currency,account_status,amount_spent,spend_cap", "limit": 100})
    alertas: list[str] = []
    try:
        concedidos = sorted(p["permission"] for p in todos(api, "me/permissions", {})
                            if p.get("status") == "granted")
    except Fallo as e:
        concedidos = None
        alertas.append(f"No se pudieron leer los permisos del token: {e}")
    if concedidos is not None:
        faltan = sorted({"ads_management", "ads_read"} - set(concedidos))
        sobran = sorted(set(concedidos) - PERMISOS_ESPERADOS)
        if faltan:
            alertas.append(f"Al token le faltan permisos: {', '.join(faltan)}.")
        if sobran:
            alertas.append(f"El token tiene permisos de más: {', '.join(sobran)}. Conviene generarlo de nuevo "
                           "marcando sólo ads_management y ads_read.")
    if not filas:
        alertas.append("El token no ve ninguna cuenta publicitaria: falta asignársela al usuario del sistema "
                       "(Asignar activos → Cuentas publicitarias).")
    lista = []
    for c in filas:
        factor = FACTOR.get(c.get("currency"), 1)
        lista.append({"id": c.get("id"), "nombre": c.get("name"), "moneda": c.get("currency"),
                      "estado": c.get("account_status"),
                      "gastado_historico": numero(c.get("amount_spent")) / factor,
                      "limite_de_gasto": numero(c.get("spend_cap")) / factor or None})
    return {"ok": bool(filas) and not any(a.startswith("Al token le faltan") for a in alertas),
            "modo": "cuentas", "cuentas": lista, "permisos": concedidos, "alertas": alertas}


# ── Decisiones ───────────────────────────────────────────────────────────────


def decidir(estado: dict, config: dict, hoy: date) -> tuple[list[dict], list[str]]:
    """Qué pausar y qué avisar. No toca Meta: sólo mira el estado leído."""
    reglas, tope = config["reglas"], config["tope"]
    acciones: list[dict] = []
    alertas: list[str] = []
    fin = date.fromisoformat(config["fin"])

    if not estado["cuenta"]["limite_de_gasto"]:
        alertas.append("La cuenta publicitaria no tiene límite de gasto. Conviene ponerlo en la configuración "
                       "de pagos: es el seguro de que nada gaste más de lo previsto.")

    vivas = [c for c in estado["campanas"] if c["estado"] == "ACTIVE"]
    gasto_total = sum(c["gasto"] for c in estado["campanas"])
    if not estado["campanas"]:
        alertas.append(f"No hay ninguna campaña cuyo nombre empiece con «{config['prefijo']}».")

    for c in vivas:
        motivo = None
        if c["presupuesto_diario"] or (not c["presupuesto_total"] and c["conjuntos_diario"]):
            motivo = "tiene presupuesto diario; el plan exige un presupuesto TOTAL para que no pueda pasarse"
        elif max(c["presupuesto_total"], c["conjuntos_total"]) > tope:
            motivo = (f"su presupuesto total (${max(c['presupuesto_total'], c['conjuntos_total']):,.0f}) "
                      f"supera el tope de ${tope:,.0f}")
        elif gasto_total >= tope:
            motivo = f"lo gastado (${gasto_total:,.0f}) ya llegó al tope de ${tope:,.0f}"
        elif hoy > fin:
            motivo = f"la campaña terminaba el {config['fin']}"
        elif c["gasto"] >= reglas["gasto_sin_resultado_campana"] and c["conversaciones"] == 0:
            motivo = (f"gastó ${c['gasto']:,.0f} sin una sola conversación: algo está mal armado "
                      "(revisar el número de WhatsApp de destino y el objetivo)")
        if motivo:
            acciones.append({"tipo": "pausar_campana", "id": c["id"], "nombre": c["nombre"], "motivo": motivo})
            continue

        activos = [a for a in c["anuncios"] if a["estado"] == "ACTIVE"]
        for a in c["anuncios"]:
            if a["estado"] in ESTADOS_CON_PROBLEMA:
                alertas.append(f"El anuncio «{a['nombre']}» está {a['estado']}: Meta lo rechazó o tiene un problema.")

        maduros = [a for a in activos if a["gasto"] >= reglas["gasto_minimo_para_juzgar"]
                   and a["desde"] and (hoy - date.fromisoformat(a["desde"])).days >= reglas["dias_minimos"]]
        referencias = [a for a in activos if a["conversaciones"] >= reglas["conversaciones_minimas_ganador"]]
        mejor = min(referencias, key=costo) if referencias else None
        quedan = len(activos)
        # Primero los peores, por si sólo se puede pausar uno sin dejar la campaña vacía.
        for a in sorted(maduros, key=lambda a: float("inf") if costo(a) is None else costo(a), reverse=True):
            if a is mejor or quedan <= 1:
                continue
            if a["conversaciones"] == 0:
                motivo = f"gastó ${a['gasto']:,.0f} en {(hoy - date.fromisoformat(a['desde'])).days} días sin una conversación"
            elif mejor and costo(a) > reglas["multiplo_costo"] * costo(mejor):
                motivo = (f"cada conversación le cuesta ${costo(a):,.0f}, más de {reglas['multiplo_costo']:g} veces "
                          f"lo que a «{mejor['nombre']}» (${costo(mejor):,.0f})")
            else:
                continue
            acciones.append({"tipo": "pausar_anuncio", "id": a["id"], "nombre": a["nombre"], "motivo": motivo})
            quedan -= 1
        if activos and quedan == 1 and len(activos) > 1:
            alertas.append(f"En «{c['nombre']}» queda un solo anuncio activo.")
    return acciones, alertas


# ── Órdenes ──────────────────────────────────────────────────────────────────


def informe(estado: dict, config: dict, hoy: date) -> dict:
    gasto = sum(c["gasto"] for c in estado["campanas"])
    conv = sum(c["conversaciones"] for c in estado["campanas"])
    return {
        "fecha": hoy.isoformat(),
        "plan": {k: config[k] for k in ("nombre", "tope", "moneda", "inicio", "fin")},
        "gasto": gasto, "conversaciones": conv,
        "costo_conversacion": round(gasto / conv) if conv else None,
        "queda": max(config["tope"] - gasto, 0),
        **estado,
    }


def revisar(api, cuenta: str, config: dict, hoy: date, aplicar: bool) -> dict:
    estado = leer(api, cuenta, config)
    acciones, alertas = decidir(estado, config, hoy)
    for a in acciones:
        if not aplicar:
            a["aplicada"] = False
            continue
        try:
            api.post(a["id"], {"status": "PAUSED"})
            a["aplicada"] = True
        except Fallo as e:
            a["aplicada"], a["error"] = False, str(e)
    return {"ok": not any("error" in a for a in acciones), "modo": "aplicar" if aplicar else "simular",
            **informe(estado, config, hoy), "acciones": acciones, "alertas": alertas}


def activar(api, cuenta: str, config: dict, hoy: date, id_anuncio: str) -> dict:
    estado = leer(api, cuenta, config)
    campana = next((c for c in estado["campanas"] if any(a["id"] == id_anuncio for a in c["anuncios"])), None)
    if campana is None:
        raise Fallo(f"El anuncio {id_anuncio} no es de una campaña «{config['prefijo']}…»: no lo toco.")
    barandas = [a for a in decidir(estado, config, hoy)[0] if a["tipo"] == "pausar_campana" and a["id"] == campana["id"]]
    if barandas:
        raise Fallo(f"No activo nada en «{campana['nombre']}»: {barandas[0]['motivo']}.")
    if hoy > date.fromisoformat(config["fin"]):
        raise Fallo(f"La campaña terminaba el {config['fin']}.")
    api.post(id_anuncio, {"status": "ACTIVE"})
    return {"ok": True, "modo": "activar", "id": id_anuncio, "campana": campana["nombre"]}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("orden", choices=["cuentas", "revisar", "activar"])
    p.add_argument("id_anuncio", nargs="?")
    p.add_argument("--cuenta", help="act_<número> de la cuenta publicitaria (por omisión, la de campana.json)")
    p.add_argument("--aplicar", action="store_true", help="pausar de verdad (sin esto sólo informa)")
    p.add_argument("--hoy", help="AAAA-MM-DD, para pruebas")
    p.add_argument("--falso", help="escenario JSON en vez de Meta, para pruebas")
    args = p.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    hoy = date.fromisoformat(args.hoy) if args.hoy else datetime.now(ZONA).date()
    api = ApiFalsa(args.falso) if args.falso else ApiReal()
    cuenta = args.cuenta or config.get("cuenta")
    try:
        if args.orden == "cuentas":
            salida = cuentas(api)
        elif not cuenta:
            raise Fallo("Falta la cuenta: --cuenta act_<id>, o `cuenta` en anuncios/campana.json.")
        elif args.orden == "activar":
            if not args.id_anuncio or not args.id_anuncio.isdigit():
                raise Fallo("activar necesita el id numérico del anuncio.")
            salida = activar(api, cuenta, config, hoy, args.id_anuncio)
        else:
            salida = revisar(api, cuenta, config, hoy, args.aplicar)
    except Fallo as e:
        salida = {"ok": False, "error": str(e)}
    if isinstance(api, ApiFalsa):
        salida["_posts"] = api.posts
    print(json.dumps(salida, ensure_ascii=False))
    return 0 if salida.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
