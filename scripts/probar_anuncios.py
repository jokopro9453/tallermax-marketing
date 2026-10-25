#!/usr/bin/env python3
"""Pruebas de scripts/anuncios.py contra escenarios falsos. No toca Meta.

    python3 scripts/probar_anuncios.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "anuncios.py"
CUENTA = "act_111"


def anuncio(id_: str, gasto: int, conv: int, creado: str = "2026-10-27T09:00:00-0300", estado: str = "ACTIVE"):
    return ({"id": id_, "name": f"Anuncio {id_}", "status": estado, "effective_status": estado, "created_time": creado},
            {"ad_id": id_, "spend": str(gasto), "impressions": "1000", "reach": "800", "clicks": "20",
             "actions": [{"action_type": "onsite_conversion.messaging_conversation_started_7d", "value": str(conv)}] if conv else []})


def escenario(campanas: list[dict], moneda: str = "CLP", limite: str = "35000") -> dict:
    get = {CUENTA: {"name": "Tallermax", "currency": moneda, "account_status": 1, "amount_spent": "0", "spend_cap": limite},
           f"{CUENTA}/campaigns": {"data": []}}
    for c in campanas:
        get[f"{CUENTA}/campaigns"]["data"].append({
            "id": c["id"], "name": c.get("nombre", "TMX · Talleres fundadores"), "status": c.get("estado", "ACTIVE"),
            "effective_status": c.get("estado", "ACTIVE"), "objective": "OUTCOME_ENGAGEMENT",
            "lifetime_budget": c.get("total", "35000"), "daily_budget": c.get("diario"),
            "start_time": "2026-10-27T00:00:00-0300", "stop_time": "2026-11-13T23:59:00-0300"})
        get[f"{c['id']}/adsets"] = {"data": [{"id": c["id"] + "9", "name": "Gran Valparaíso"}]}
        get[f"{c['id']}/ads"] = {"data": [a for a, _ in c["anuncios"]]}
        get[f"{c['id']}/insights"] = {"data": [r for _, r in c["anuncios"]]}
    return {"get": get}


def correr(esc: dict, *args: str) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(esc, f)
    r = subprocess.run([sys.executable, str(SCRIPT), *args, "--cuenta", CUENTA, "--falso", f.name],
                       capture_output=True, text=True, check=False)
    Path(f.name).unlink()
    return json.loads(r.stdout)


def pausados(s: dict) -> list[str]:
    return [a["id"] for a in s.get("acciones", [])]


CASOS = []


def caso(fn):
    CASOS.append(fn)
    return fn


@caso
def sin_conversaciones_se_pausa():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 6000, 0), anuncio("11", 5000, 3)]}]), "revisar", "--hoy", "2026-10-31")
    assert pausados(s) == ["10"], s
    assert s["_posts"] == [], "sin --aplicar no debe tocar Meta"


@caso
def aplicar_pausa_de_verdad():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 6000, 0), anuncio("11", 5000, 3)]}]), "revisar", "--aplicar", "--hoy", "2026-10-31")
    assert s["_posts"] == [["10", {"status": "PAUSED"}]], s["_posts"]
    assert s["ok"] and s["acciones"][0]["aplicada"]


@caso
def antes_de_tiempo_no_se_juzga():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 6000, 0), anuncio("11", 5000, 3)]}]), "revisar", "--hoy", "2026-10-29")
    assert pausados(s) == [], s


@caso
def poco_gasto_no_se_juzga():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 3000, 0), anuncio("11", 5000, 3)]}]), "revisar", "--hoy", "2026-11-02")
    assert pausados(s) == [], s


@caso
def caro_frente_al_mejor_se_pausa():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 9000, 2), anuncio("11", 6000, 4)]}]), "revisar", "--hoy", "2026-11-01")
    assert pausados(s) == ["10"], s
    assert s["costo_conversacion"] == 2500


@caso
def parecido_al_mejor_sigue():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 8000, 3), anuncio("11", 6000, 4)]}]), "revisar", "--hoy", "2026-11-01")
    assert pausados(s) == [], s


@caso
def nunca_deja_la_campana_vacia():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 5000, 0)]}]), "revisar", "--hoy", "2026-11-01")
    assert pausados(s) == [], s


@caso
def dos_malos_y_uno_nuevo():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 4500, 0), anuncio("11", 4200, 0),
                                                    anuncio("12", 500, 1, creado="2026-10-31T09:00:00-0300")]}]),
               "revisar", "--hoy", "2026-11-01")
    assert sorted(pausados(s)) == ["10", "11"], s
    assert any("un solo anuncio" in a for a in s["alertas"]), s["alertas"]


@caso
def campana_sin_resultados_se_pausa_entera():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 4500, 0), anuncio("11", 4200, 0)]}]), "revisar", "--hoy", "2026-11-01")
    # 8.700 gastados sin una conversación: pasa el umbral de la campaña
    assert s["acciones"][0]["tipo"] == "pausar_campana", s


@caso
def presupuesto_diario_pausa_campana():
    s = correr(escenario([{"id": "1", "total": None, "diario": "5000", "anuncios": [anuncio("10", 100, 0)]}]), "revisar", "--hoy", "2026-10-28")
    assert s["acciones"][0]["tipo"] == "pausar_campana" and "diario" in s["acciones"][0]["motivo"], s


@caso
def presupuesto_sobre_el_tope_pausa_campana():
    s = correr(escenario([{"id": "1", "total": "50000", "anuncios": [anuncio("10", 100, 0)]}]), "revisar", "--hoy", "2026-10-28")
    assert s["acciones"][0]["tipo"] == "pausar_campana" and "tope" in s["acciones"][0]["motivo"], s


@caso
def gasto_en_el_tope_pausa_todo():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 20000, 6), anuncio("11", 15000, 2)]}]), "revisar", "--hoy", "2026-11-10")
    assert [a["tipo"] for a in s["acciones"]] == ["pausar_campana"], s


@caso
def pasada_la_fecha_pausa_todo():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 2000, 1)]}]), "revisar", "--hoy", "2026-11-14")
    assert s["acciones"][0]["tipo"] == "pausar_campana", s


@caso
def campanas_ajenas_ni_se_miran():
    esc = escenario([{"id": "1", "anuncios": [anuncio("10", 2000, 1)]},
                     {"id": "2", "nombre": "Otra campaña", "total": "900000", "anuncios": [anuncio("20", 50000, 0)]}])
    s = correr(esc, "revisar", "--aplicar", "--hoy", "2026-11-01")
    assert [c["id"] for c in s["campanas"]] == ["1"] and s["_posts"] == [], s


@caso
def campana_pausada_no_se_toca():
    s = correr(escenario([{"id": "1", "estado": "PAUSED", "total": "90000", "anuncios": [anuncio("10", 9000, 0)]}]), "revisar", "--aplicar", "--hoy", "2026-11-01")
    assert s["_posts"] == [], s


@caso
def moneda_distinta_se_niega():
    s = correr(escenario([{"id": "1", "anuncios": []}], moneda="USD"), "revisar")
    assert not s["ok"] and "USD" in s["error"], s


@caso
def sin_limite_de_gasto_avisa():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 100, 0)]}], limite="0"), "revisar", "--hoy", "2026-10-28")
    assert any("límite de gasto" in a for a in s["alertas"]), s


@caso
def rechazado_avisa():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 0, 0, estado="DISAPPROVED"), anuncio("11", 100, 0)]}]), "revisar", "--hoy", "2026-10-28")
    assert any("DISAPPROVED" in a for a in s["alertas"]), s


@caso
def activar_propio():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 100, 0, estado="PAUSED"), anuncio("11", 100, 0)]}]), "activar", "10", "--hoy", "2026-10-30")
    assert s["ok"] and s["_posts"] == [["10", {"status": "ACTIVE"}]], s


@caso
def activar_ajeno_se_niega():
    esc = escenario([{"id": "1", "anuncios": [anuncio("10", 100, 0)]},
                     {"id": "2", "nombre": "Otra campaña", "anuncios": [anuncio("20", 0, 0, estado="PAUSED")]}])
    s = correr(esc, "activar", "20", "--hoy", "2026-10-30")
    assert not s["ok"] and s["_posts"] == [], s


@caso
def activar_sobre_el_tope_se_niega():
    s = correr(escenario([{"id": "1", "total": "60000", "anuncios": [anuncio("10", 100, 0, estado="PAUSED")]}]), "activar", "10", "--hoy", "2026-10-30")
    assert not s["ok"] and s["_posts"] == [], s


@caso
def activar_pasada_la_fecha_se_niega():
    s = correr(escenario([{"id": "1", "anuncios": [anuncio("10", 100, 0, estado="PAUSED")]}]), "activar", "10", "--hoy", "2026-11-20")
    assert not s["ok"] and s["_posts"] == [], s


def escenario_cuentas(cuentas: list[dict], permisos: list[str]) -> dict:
    return {"get": {"me/adaccounts": {"data": cuentas},
                    "me/permissions": {"data": [{"permission": p, "status": "granted"} for p in permisos]}}}


@caso
def cuentas_lista_las_que_ve():
    s = correr(escenario_cuentas([{"id": CUENTA, "name": "Tallermax", "currency": "CLP", "account_status": 1,
                                   "amount_spent": "12000", "spend_cap": "35000"}],
                                 ["ads_management", "ads_read", "public_profile"]), "cuentas")
    assert s["ok"] and s["cuentas"][0]["id"] == CUENTA and s["cuentas"][0]["limite_de_gasto"] == 35000, s
    assert s["alertas"] == [] and s["_posts"] == [], s


@caso
def cuentas_avisa_permisos_de_mas_y_de_menos():
    s = correr(escenario_cuentas([{"id": CUENTA, "currency": "CLP"}], ["ads_read", "business_management"]), "cuentas")
    assert not s["ok"], s
    assert any("faltan" in a and "ads_management" in a for a in s["alertas"]), s
    assert any("de más" in a and "business_management" in a for a in s["alertas"]), s


@caso
def cuentas_sin_ninguna_falla():
    s = correr(escenario_cuentas([], ["ads_management", "ads_read"]), "cuentas")
    assert not s["ok"] and any("ninguna cuenta" in a for a in s["alertas"]), s


if __name__ == "__main__":
    fallas = 0
    for fn in CASOS:
        try:
            fn()
            print(f"ok    {fn.__name__}")
        except AssertionError as e:
            fallas += 1
            print(f"FALLA {fn.__name__}: {e}")
    print(f"\n{len(CASOS) - fallas}/{len(CASOS)} bien")
    sys.exit(1 if fallas else 0)
