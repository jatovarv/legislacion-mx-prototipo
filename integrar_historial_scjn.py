#!/usr/bin/env python3
"""Integra versiones_separadas.json (separador SCJN, PR #7, corrido en Colab) en cpeum.json.

Uso: python3 integrar_historial_scjn.py . /ruta/versiones_separadas.json   (escribe docs/reporte_integracion_historial.json)

Reglas:
- Arts. 1o. y 4o. (golden cases) no se tocan.
- Entradas "desconocido" (PDF sin número de artículo en la ruta) se ignoran y se reportan.
- Art. duplicado: se conserva la entrada con más versiones (la otra es un fragmento del mismo PDF).
- Artículo numerado con 0 versiones: la SCJN no publica cronología (sin reformas desde 1917) y
  el consolidado de la Cámara lo confirma ("Artículo original DOF 05-02-1917"); queda con su
  única versión = texto original = texto vigente ya cargado, estado "verificado" sólo si el
  consolidado lo marca sin reforma; si no coincide, se deja en "vigente" y se reporta.
- Versión con fecha null: NO se inventa. publicacion = null, vigencia_desde = null,
  estado de la versión "fecha_pendiente"; se guarda fecha_sugerida (única fecha citada en las
  notas de esa versión dentro de la ventana entre vecinas) como pista para el cotejo manual.
- vigencia: regla general "al día siguiente de la publicación" con vigencia_verificada=false
  (salvo el texto original: 1917-05-01, verificada). vigencia_hasta = día anterior a la
  siguiente versión fechada; si la siguiente no tiene fecha, null + nota.
- Cotejo: la última versión de la SCJN debe coincidir con el texto vigente del consolidado
  (ya en cpeum.json). Si coincide -> estado "verificado"; si no -> "historial_parcial" y se
  reporta la discrepancia (puede ser reforma posterior al PDF de la SCJN o diferencia de
  extracción). En ambos casos el texto vigente mostrado sigue siendo el del consolidado.
- dof_url: no se asigna (requiere la cronología oficial por artículo; pendiente).
"""
import collections, datetime as dt, json, pathlib, re, sys

SCRATCH = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path(sys.argv[1])
SEP = json.load(open(sys.argv[2] if len(sys.argv) > 2 else REPO / "versiones_separadas.json", encoding="utf-8"))  # salida del separador (Drive: /MyDrive/CPEUM_SCJN_Historial/versiones_separadas.json)
data = json.loads((REPO / "cpeum.json").read_text(encoding="utf-8"))
CONSOL = {k: {"fechas_dof": sorted({f"{y}-{m}-{d}" for d, m, y in __import__("re").findall(r"(\d{2})-(\d{2})-(\d{4})", " ".join(a["versiones"][-1].get("notas_camara", [])))})} for k, a in data["articulos"].items()}  # fechas DOF citadas por la Cámara
MES = {m: i + 1 for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                        "septiembre", "octubre", "noviembre", "diciembre"])}
CAMBIO_CAPITULO = "2011-06-10"

def norm(s): return re.sub(r"\s+", " ", s).strip()
def comparable(s):
    """Normalización SÓLO para el cotejo (no modifica los textos guardados)."""
    s = norm(s)
    s = re.sub(r"\((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD|F\. DE E\.|N\. DE E\.)[^)]*\)", " ", s, flags=re.I)   # anotaciones SCJN
    s = re.sub(r"\[N\. DE E\.[^\]]*\]", " ", s, flags=re.I)
    s = re.sub(r"^Art(?:ículo|\.)\s*(\d+[oa]?)\.?-?\s*", r"Artículo \1 ", s)                                   # «Art. 5o.-» == «Artículo 5o.»
    s = s.replace("–", "-").replace("—", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\(?Párrafo [a-zé ]+\.? ?(?:Se deroga|Derogado)\.?\)?", " ", s)                                 # marcadores Cámara
    s = re.sub(r"\(Se deroga\)|\bSe deroga\.?|\bDerogad[ao]\b\.?", " ", s, flags=re.I)
    s = re.sub(r"\(sic(?: DOF [\d\- ]+)?\)", " ", s, flags=re.I)                                                # marcas (sic), incl. «28-12- 1982»
    s = re.sub(r"\bREPUBLICADA DEROGACI[OÓ]N D\.? ?O\.? ?F\.? \d{1,2} DE [A-ZÁÉÍÓÚ]+ DE \d{4}", " ", s, flags=re.I)
    s = s.replace("º", "o")
    s = re.sub(r"(\b(?:[IVXLC]{1,7}(?:-[A-Z])?(?: Bis)?|[A-Z]|[a-z]|\d+[oa]?)[.)]+)\s*-\s*", r"\1 ", s)    # «I.-», «a).-», «A.-», «XXIII Bis.-», «1.-» == sin guion
    s = re.sub(r"(\w)\s+-\s*(\w)", r"\1-\2", s)                                                               # «exclusivismos - atenderá» == «exclusivismos-atenderá»
    s = s.replace("aquéllos", "aquellos").replace("aquéllas", "aquellas").replace("éste", "este").replace("ésta", "esta")
    s = re.sub(r"[.,;:()\[\]]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()
def dia(iso, k): return (dt.date.fromisoformat(iso) + dt.timedelta(days=k)).isoformat()
def fechas_en_notas(notas):
    out = collections.Counter()
    for n in notas:
        for d, m, y in re.findall(r"(\d{1,2}) DE ([A-ZÁÉÍÓÚ]+) DE (\d{4})", n.upper()):
            mm = MES.get(m.lower())
            if mm: out[f"{y}-{mm:02d}-{int(d):02d}"] += 1
    return out
RESIDUO_SCJN = [
    re.compile(r"\s*\[N\. DE E\.[^\]]*\]"),                                   # [N. DE E. ...] entre corchetes
    re.compile(r"\s*\((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD|F\. DE E\.|N\. DE E\.)[^)]*\)"),  # anotación en línea
    re.compile(r"(?m)^\s*N\. DE E\.[^\n]*$"),                                   # nota de editor en su propia línea
]
def limpiar_residuos(texto, notas):
    """Retira anotaciones de la SCJN que quedaron dentro del cuerpo y las pasa a notas. No toca palabras del texto."""
    # restos del encabezado partido por corte de página: fragmento de fecha ("15 de", "el 20 de diciembre de 2019") o coma suelta al inicio
    texto = re.sub(r"^\s*(?:el )?\d{1,2} de(?: [a-záéíóú]+)?(?: de)?(?: \d{4})?\s*\n+", "", texto)
    texto = re.sub(r"^\s*,\s*\n+", "", texto)
    texto = re.sub(r"^\s*(?:el )?\d{1,2} de(?: [a-záéíóú]+)?(?: de)?(?: \d{4})?\s*\n+", "", texto)
    # anotación que perdió su paréntesis de apertura: "REFORMADO PRIMER PÁRRAFO, D.O.F. 6 DE JUNIO DE 2019)"
    for m in re.finditer(r"(?:^|\s)((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD)[A-ZÁÉÍÓÚ ,.\[\]]*?D\.O\.F\. \d{1,2} DE [A-ZÁÉÍÓÚ]+ DE \d{4}\))", texto):
        notas.append("(" + norm(m.group(1)))
    texto = re.sub(r"(?:^|\s)(?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD)[A-ZÁÉÍÓÚ ,.\[\]]*?D\.O\.F\. \d{1,2} DE [A-ZÁÉÍÓÚ]+ DE \d{4}\)", " ", texto)
    texto = re.sub(r"(?:^|\s)(?:VISUALIZA DENTRO DE LA CRONOLOG[ÍI]A[^\n]*\.)", " ", texto)
    # fragmento de fecha + espacio + "Art." en la misma línea ("el 6 de junio de 2019  Art. 35.-")
    texto = re.sub(r"^\s*(?:el )?\d{1,2} de(?: [a-záéíóú]+)?(?: de)?(?: \d{4})?\s+(?=Art)", "", texto)
    # nota de editor en mayúsculas al inicio, cortada antes de "N. DE E." (continuación de la nota del encabezado)
    m0 = re.match(r"^([A-ZÁÉÍÓÚÑ0-9 ,.;:()\[\]'\"\-]{40,}?[.\]])\s*\n+", texto)
    if m0 and m0.group(1) == m0.group(1).upper():
        notas.append(norm(m0.group(1))); texto = texto[m0.end():]
    # anotación anidada partida en varias líneas: "IX.- (REFORMADA [N. DE E.\nDEROGADA], D.O.F. 8 DE OCTUBRE DE 1974)"
    for m in re.finditer(r"\((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD)[^()]*?\[N\. DE E\.[^\]]*\][^()]*?\)", texto, flags=re.S):
        notas.append(norm(m.group(0)))
    texto = re.sub(r"\((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD)[^()]*?\[N\. DE E\.[^\]]*\][^()]*?\)", "", texto, flags=re.S)
    texto = re.sub(r"\((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD)[A-ZÁÉÍÓÚ ,]*\[N\. DE E\.\s*$", "", texto, flags=re.M)  # resto sin cierre
    for rx in RESIDUO_SCJN:
        for m in rx.finditer(texto):
            notas.append(norm(m.group(0)))
        texto = rx.sub("", texto)
    texto = re.sub(r"[ \t]+\n", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"^\s*(?:el )?\d{1,2} de(?: [a-záéíóú]+)?(?: de)?(?: \d{4})?\s*\n+", "", texto.strip())
    return texto.strip()

def capitulo_de(num):
    def visitar(nodo, camino):
        camino = camino + [nodo]
        r = nodo.get("articulos")
        if r and r["desde"] <= num <= r["hasta"]: return camino
        for h in nodo.get("hijos", []):
            x = visitar(h, camino)
            if x: return x
    for t in data["estructura"]:
        x = visitar(t, [])
        if x: return x[-1].get("subtitulo") or x[-1]["nombre"]

# --- agrupa la salida del separador por número ---
por_num, desconocidos = {}, 0
for a in SEP:
    n = str(a["numero"])
    if not n.isdigit(): desconocidos += 1; continue
    if n in por_num and len(por_num[n]["versiones"]) >= len(a["versiones"]): continue
    por_num[n] = a
print(f"entradas 'desconocido' ignoradas: {desconocidos}; artículos numerados: {len(por_num)}")

reporte = {"verificado": [], "sin_reforma": [], "historial_parcial": [], "fecha_pendiente": [], "sin_cronologia_pero_con_reforma": []}
for n in range(1, 137):
    k = str(n)
    art = data["articulos"][k]
    if art.get("estado") == "verificado" and art.get("nota", "").startswith("Golden case"):
        continue
    vigente_consol = art["versiones"][-1]["texto"]            # texto vigente del consolidado (ya limpio)
    cap_actual = capitulo_de(n)
    entrada = por_num.get(k)
    sv = entrada["versiones"] if entrada else []
    # Colab rellenó los artículos sin cronología con un marcador {"fecha_dof": "1917-02-05", "texto": "Texto original de 1917"}:
    # no es texto del artículo; se trata como "sin cronología SCJN".
    if sv and all("tipo" not in v for v in sv):
        sv = []

    if not sv:  # sin cronología SCJN
        fechas_cam = CONSOL[k]["fechas_dof"]
        if not fechas_cam or fechas_cam == ["1917-02-05"]:
            v = art["versiones"][0]
            v.update({"id": "v1", "etiqueta": "Original (vigente)", "tipo": "original", "publicacion": "1917-02-05",
                      "vigencia_desde": "1917-05-01", "vigencia_hasta": None, "vigencia_verificada": True,
                      "vigencia_nota": "Texto original de 1917 sin reformas (la SCJN no publica cronología para este artículo; el consolidado de la Cámara lo marca «Artículo original DOF 05-02-1917»). En vigor desde el 1o. de mayo de 1917.",
                      "dof_url": "https://www.dof.gob.mx/Constitucion1917/constitucion_1917.pdf", "dof_etiqueta": "Ver texto original en el DOF"})
            v.pop("fuente_url", None); v.pop("fuente_etiqueta", None)
            art["estado"] = "verificado"
            art["nota"] = "Artículo sin reformas desde 1917: texto original = texto vigente, cotejado con el consolidado de la Cámara de Diputados (última reforma DOF 07-10-2026)."
            reporte["sin_reforma"].append(n)
        else:
            reporte["sin_cronologia_pero_con_reforma"].append((n, fechas_cam))
        continue

    def es_version_completa(txt):
        t = re.sub(r"^[\s,]+", "", txt)
        t = re.sub(r"^\s*(?:el )?\d{1,2} de(?: [a-záéíóú]+)?(?: de)?(?: \d{4})?\s*\n+", "", t)
        t = re.sub(r"^\s*\[N\. DE E\.[^\]]*\]\s*", "", t)
        t = re.sub(r"^\s*(?:\(?(?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD)[^)]*\)\s*)+", "", t)
        return bool(re.match(rf"^Art(?:ículo|\.)\s*{n}[oa]?\.?", t))
    incompletas = [v["orden"] for v in sv if not es_version_completa(v["texto"])]
    if len(incompletas) > 1:
        # el PDF de la SCJN de este artículo está organizado por fracciones/apartados (encabezado repetido por fragmento):
        # el separador por encabezados no produce versiones del artículo completo. No se integra; se reporta.
        art["estado"] = "historial_parcial"
        art["nota"] = (f"El PDF «Historia del texto» de la SCJN de este artículo está organizado por fragmentos (fracciones o apartados), no por "
                       f"versiones íntegras del artículo: {len(incompletas)} de {len(sv)} cortes no empiezan con «Artículo {n}». El historial requiere "
                       "un separador específico; por ahora se muestra sólo el texto vigente del consolidado de la Cámara de Diputados.")
        art["versiones"][-1].update({"id": "vig", "etiqueta": "Vigente (consolidado Cámara de Diputados)", "tipo": "vigente"})
        art["fuente_historial"] = "SCJN (00_historia.pdf) — estructura por fragmentos; pendiente"
        reporte["historial_parcial"].append((n, "estructura por fragmentos", f"{len(incompletas)}/{len(sv)}"))
        continue
    versiones = []
    for i, v in enumerate(sv):
        f = v["fecha_dof"]
        nv = {"id": f"v{i+1}", "tipo": v["tipo"]}
        if f:
            nv["etiqueta"] = ("Original" if v["tipo"] == "original" else
                              f"Fe de erratas DOF {f[8:]}-{f[5:7]}-{f[:4]}" if v["tipo"] == "fe_de_erratas" else
                              f"Aclaración DOF {f[8:]}-{f[5:7]}-{f[:4]}" if v["tipo"] == "aclaracion" else
                              f"Reforma DOF {f[8:]}-{f[5:7]}-{f[:4]}")
            nv["publicacion"] = f
            if v["tipo"] == "original":
                nv["vigencia_desde"] = "1917-05-01"; nv["vigencia_verificada"] = True
                nv["vigencia_nota"] = "Artículo 1o. transitorio de la Constitución de 1917: entró en vigor el 1o. de mayo de 1917."
            else:
                nv["vigencia_desde"] = dia(f, 1); nv["vigencia_verificada"] = False
                nv["vigencia_nota"] = "Regla general (al día siguiente de su publicación); pendiente de cotejo con los transitorios del decreto."
        else:
            prev = max((x["fecha_dof"] for x in sv[:i] if x["fecha_dof"]), default=None)
            nxt = min((x["fecha_dof"] for x in sv[i+1:] if x["fecha_dof"]), default=None)
            cand = [c for c in fechas_en_notas(v["notas_scjn"]) if (prev is None or c > prev) and (nxt is None or c < nxt)]
            nv.update({"etiqueta": "Reforma (fecha pendiente de cotejo)", "publicacion": None, "vigencia_desde": None,
                       "vigencia_verificada": False, "fecha_pendiente": True,
                       "fecha_sugerida": cand[0] if len(cand) == 1 else None,
                       "vigencia_nota": ("La fecha de publicación no pudo leerse del PDF de la SCJN (quedó partida por un corte de página). "
                                         + (f"Pista: las notas de esta versión citan una sola fecha dentro de la ventana {prev}–{nxt}: {cand[0]}; " if len(cand) == 1 else f"Ventana entre versiones vecinas: {prev}–{nxt}; ")
                                         + "confirmar contra el PDF de la SCJN antes de fijarla.")})
            reporte["fecha_pendiente"].append((n, i + 1, cand[0] if len(cand) == 1 else None))
        ref = nv.get("publicacion") or nv.get("fecha_sugerida") or "9999"
        nv["capitulo"] = (("De las Garantías Individuales" if ref < CAMBIO_CAPITULO else cap_actual) if n <= 29 else cap_actual)
        notas = list(v["notas_scjn"])
        cuerpo = limpiar_residuos(v["texto"], notas)
        if re.match(rf"^{n}[oa]?\.-\s", cuerpo):
            cuerpo = "Art. " + cuerpo   # el «Art.» del encabezado quedó en la página anterior
            notas.append("[integración: prefijo «Art.» restituido, perdido por corte de página]")
        nv["texto"] = cuerpo
        nv["notas_scjn"] = notas
        nv["encabezado_scjn"] = v["encabezado_scjn"]
        versiones.append(nv)
    # vigencia_hasta
    for a, b in zip(versiones, versiones[1:]):
        if a["vigencia_desde"] and b["vigencia_desde"]:
            h = dia(b["vigencia_desde"], -1)
            if h < a["vigencia_desde"]:
                h = a["vigencia_desde"]; a["vigencia_nota"] += " Texto intermedio: el siguiente decreto entró en vigor el mismo día."
            a["vigencia_hasta"] = h
        else:
            a["vigencia_hasta"] = None
            if b["vigencia_desde"] is None: a["vigencia_nota"] += " Fin de vigencia indeterminado: la versión siguiente no tiene fecha confirmada."
    versiones[-1]["vigencia_hasta"] = None
    versiones[-1]["etiqueta"] = "Vigente" + (f" (post {versiones[-1]['publicacion'][8:]}-{versiones[-1]['publicacion'][5:7]}-{versiones[-1]['publicacion'][:4]})" if versiones[-1].get("publicacion") else "")

    coincide = comparable(versiones[-1]["texto"]) == comparable(vigente_consol)
    if coincide:
        art["estado"] = "verificado"
        art["nota"] = ("Historial extraído del PDF «Historia del texto del artículo» de la SCJN; la versión vigente coincide con el texto consolidado "
                       "de la Cámara de Diputados (última reforma DOF 07-10-2026). Fechas de entrada en vigor por regla general, pendientes de cotejo con cada decreto.")
        versiones[-1]["texto"] = vigente_consol  # prefijo «Artículo N.» como el consolidado
        reporte["verificado"].append(n)
    else:
        art["estado"] = "historial_parcial"
        art["nota"] = ("Historial extraído del PDF de la SCJN, pero su última versión NO coincide con el texto consolidado de la Cámara de Diputados "
                       "(última reforma DOF 07-10-2026): puede haber una reforma posterior al PDF o una diferencia de extracción. "
                       "Se muestra como vigente el texto del consolidado; el historial queda pendiente de cotejo.")
        vig = art["versiones"][-1]
        vig.update({"id": f"v{len(versiones)+1}", "etiqueta": "Vigente (consolidado Cámara de Diputados)", "tipo": "vigente",
                    "vigencia_nota": "Texto del consolidado de la Cámara; no procede del PDF de la SCJN. " + vig.get("vigencia_nota", "")})
        if versiones[-1]["vigencia_desde"] and vig["vigencia_desde"] and vig["vigencia_desde"] > versiones[-1]["vigencia_desde"]:
            versiones[-1]["vigencia_hasta"] = dia(vig["vigencia_desde"], -1)
        versiones[-1]["etiqueta"] = versiones[-1]["etiqueta"].replace("Vigente", "Última versión SCJN")
        versiones.append(vig)
        reporte["historial_parcial"].append((n, versiones[-2].get("publicacion"), art["versiones"][-1]["publicacion"]))
    art["versiones"] = versiones
    art["fuente_historial"] = "SCJN, Historia del texto del artículo (00_historia.pdf), separado con separar_versiones_scjn.py (PR #7) en Colab; Drive: /MyDrive/CPEUM_SCJN_Historial/versiones_separadas.json"

data["norma"]["aviso"] = ("Prototipo de demostración. Textos vigentes cotejados con el consolidado de la Cámara de Diputados (última reforma DOF 07-10-2026); "
                          "historial de versiones extraído de la compilación de la SCJN. Las fechas de entrada en vigor marcadas «por cotejar» siguen la regla general "
                          "y las versiones con fecha pendiente no han podido fecharse con certeza. No constituye texto oficial.")
(REPO / "cpeum.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
json.dump(reporte, open(REPO / "docs/reporte_integracion_historial.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
est = collections.Counter(a["estado"] for a in data["articulos"].values())
print("estados:", dict(est))
print("verificados con historial:", len(reporte["verificado"]), "| sin reforma:", reporte["sin_reforma"])
print("historial_parcial:", reporte["historial_parcial"])
print("fecha_pendiente:", reporte["fecha_pendiente"])
print("sin cronología pero con reforma:", reporte["sin_cronologia_pero_con_reforma"])
print("total versiones:", sum(len(a["versiones"]) for a in data["articulos"].values()))
