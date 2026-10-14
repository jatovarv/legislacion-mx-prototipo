#!/usr/bin/env python3
"""Extrae las versiones de un artículo del PDF «Historia del texto del artículo» de la SCJN (00_historia.pdf)
POR COORDENADAS con pdfplumber, no por el flujo lineal de texto.

Uso: python3 extraer_historia_scjn_pdf.py Art_073_00_historia.pdf 73.raw.json

Diseño del PDF: dos columnas. Izquierda (x < 145): etiqueta de versión
("Texto original D.O.F. 05 de febrero de 1917" / "Texto derivado de la reforma
publicada en el D.O.F. 31 de diciembre de 1974"). Derecha (x >= 145): texto.
Cada etiqueta marca, por su coordenada vertical, dónde empieza una versión.
"""
import json, re, sys
import pdfplumber

PDF = sys.argv[1]
OUT = sys.argv[2]
SPLIT_X = 130
MESES = {m: i + 1 for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"])}

def lineas(words, tol=3):
    """Agrupa palabras en líneas por coordenada 'top'."""
    words = sorted(words, key=lambda w: (round(w["top"]), w["x0"]))
    out = []
    for w in words:
        if out and abs(w["top"] - out[-1]["top"]) <= tol:
            out[-1]["words"].append(w)
        else:
            out.append({"top": w["top"], "bottom": w["bottom"], "words": [w]})
    for l in out:
        l["words"].sort(key=lambda w: w["x0"])
        l["text"] = " ".join(w["text"] for w in l["words"])
        l["x0"] = l["words"][0]["x0"]
        l["x1"] = l["words"][-1]["x1"]
    return out

# 1) Recorre páginas y construye una lista global de líneas de texto y de etiquetas
etiquetas = []   # (page, top, texto_etiqueta)
texto_lineas = []  # dict(page, top, bottom, x0, text)
with pdfplumber.open(PDF) as pdf:
    w0 = pdf.pages[0].extract_words(keep_blank_chars=False, use_text_flow=False, x_tolerance=1.5)
    art_x = min((w["x0"] for w in w0 if 100 < w["top"] < 725 and w["text"].startswith("Art")), default=136)
    if art_x > 170:
        SPLIT_X = 170  # columna izquierda más ancha (p. ej. Art. 35, donde el cuerpo arranca en x=182.6)
    for pi, page in enumerate(pdf.pages):
        words = page.extract_words(keep_blank_chars=False, use_text_flow=False, x_tolerance=1.5)
        izq = [w for w in words if w["x0"] < SPLIT_X and w["top"] < 725 and (w["top"] > 100 or w["x0"] < 130)]
        # cuerpo: fuera del encabezado corrido (top 49/65) y del pie (número de página y correo, top >= 734)
        der = [w for w in words if w["x0"] >= SPLIT_X and 100 < w["top"] < 725]
        for l in lineas(izq):
            l["page"] = pi + 1
            etiquetas.append(l)
        for l in lineas(der):
            l["page"] = pi + 1
            texto_lineas.append(l)

# 2) Agrupa las líneas de etiqueta en bloques: cada etiqueta empieza con "Texto" y puede
#    continuar en las líneas siguientes, incluso en la página siguiente.
bloques = []
for l in etiquetas:
    t = l["text"]
    if t == ",":
        continue  # coma espuria del encabezado corrido (top negativo) en los PDF grandes
    # Inicio de etiqueta: "Texto ..." o una primera línea corrupta por sobreimpresión (p. ej. "RETFeOxRtMo AdDeOri vPaRdIMoE"
    # en el Art. 73, pág. 426) seguida de "de la reforma": se detecta por la mezcla de mayúsculas/minúsculas sin vocal clara.
    corrupta = bool(re.match(r"^[A-Za-z]{6,}\s+[A-Za-z]{5,}(\s+[A-Za-z]{5,})?$", t)) and sum(c.isupper() for c in t) >= 6 and sum(c.islower() for c in t) >= 4 and not t.startswith("Texto")
    if t.startswith("Texto") or corrupta:
        if corrupta: print("AVISO: etiqueta con primera línea corrupta por sobreimpresión, pág.", l["page"], repr(t), "-> se toma como 'Texto derivado'", file=sys.stderr)
        bloques.append({"page": l["page"], "top": l["top"], "lineas": ["Texto derivado" if corrupta else t], "corrupta": corrupta})
    elif bloques:
        bloques[-1]["lineas"].append(t)   # continuación (puede venir en la página siguiente)
    else:
        print("AVISO etiqueta suelta:", l["page"], round(l["top"]), t, file=sys.stderr)

versiones = []
for b in bloques:
    full = " ".join(b["lineas"])
    m = re.search(r"(?:D\.?O\.?F\.?\s+)?(?:el\s+)?(\d{1,2})\s+de\s+([a-zñ]+)\s+(?:de\s+)?(\d{4})", full, re.I)
    if not m:
        print("AVISO etiqueta sin fecha:", full, file=sys.stderr); continue
    d, mes, y = int(m.group(1)), MESES[m.group(2).lower()], int(m.group(3))
    tipo = "original" if full.startswith("Texto original") else ("fe_de_erratas" if "fe de erratas" in full else ("aclaracion" if "aclaración" in full or "aclaracion" in full else "reforma"))
    versiones.append({"etiqueta_scjn": full, "tipo": tipo, "publicacion": f"{y:04d}-{mes:02d}-{d:02d}", "page": b["page"], "top": b["top"], "lineas": [],
                      **({"etiqueta_corrupta": True} if b.get("corrupta") else {})})
if versiones and versiones[-1]["etiqueta_scjn"].startswith("Texto vigente"):
    versiones[-1]["tipo"] = "vigente"

# 3) Asigna cada línea de texto a su versión. Frontera real: la primera línea de arranque del artículo
#    («Art. N.-», o una anotación/nota de editor que la precede inmediatamente) situada a partir de ~12 pt por
#    encima de la etiqueta. Así el cuerpo de una versión puede continuar por debajo de la etiqueta siguiente
#    (PDF largos) y las anotaciones previas al arranque quedan en la versión correcta.
ARRANQUE = re.compile(r"^Art(?:ículo|\.)\s*\d+[oa]?\.?-?")
PREVIO = re.compile(r"^(\(?(REFORMAD|ADICIONAD|DEROGAD|REUBICAD|N\. DE E\.|F\. DE E\.)|\[N\. DE E\.|[A-ZÁÉÍÓÚÑ0-9 ,.;:()\[\]'\"-]{30,}$)")
texto_lineas.sort(key=lambda l: (l["page"], l["top"]))
fronteras = []   # índice de la línea de cuerpo donde empieza cada versión
for v in versiones:
    desde = (v["page"], v["top"] - 12)
    cand = None
    for i, l in enumerate(texto_lineas):
        if (l["page"], l["top"]) < desde: continue
        if ARRANQUE.match(l["text"].strip()):
            cand = i
            # retrocede sobre anotaciones/notas de editor contiguas que preceden al arranque
            j = i - 1
            while j >= 0 and (texto_lineas[j]["page"], texto_lineas[j]["top"]) >= desde and PREVIO.match(texto_lineas[j]["text"].strip()):
                cand = j; j -= 1
            break
    if cand is None:
        print("AVISO: sin arranque de artículo tras la etiqueta", v["etiqueta_scjn"], file=sys.stderr)
        cand = next((i for i, l in enumerate(texto_lineas) if (l["page"], l["top"]) >= desde), len(texto_lineas))
    fronteras.append(cand)
for n_v, v in enumerate(versiones):
    ini = fronteras[n_v]; fin = fronteras[n_v + 1] if n_v + 1 < len(versiones) else len(texto_lineas)
    if fin < ini: fin = ini
    v["lineas"] = texto_lineas[ini:fin]

# 4) Convierte líneas en párrafos: salto de párrafo si el hueco vertical supera 1.45 veces el interlineado,
#    o si la línea es una anotación editorial entre paréntesis en mayúsculas (se guarda aparte).
MARGEN_DERECHO = max(l["x1"] for l in texto_lineas)
# Anotaciones editoriales de la SCJN: una o varias expresiones entre paréntesis, en mayúsculas,
# que ocupan la línea completa, p. ej. "(ADICIONADO, D.O.F. 7 DE ABRIL DE 2000) (F. DE E., D.O.F. 12 DE ABRIL DE 2000)".
ANOTACION = re.compile(r"^(\(?(REFORMAD|ADICIONAD|DEROGAD|REUBICAD|N\. DE E\.|F\. DE E\.)[^)]*\)\s*)+$")
INICIO_ANOT = re.compile(r"^\((REFORMAD|ADICIONAD|DEROGAD|REUBICAD|N\. DE E\.|F\. DE E\.)")
def parrafos_de(lineas_v):
    pars, notas, cur, prev, pend = [], [], [], None, None
    corch = None
    for l in lineas_v:
        t = l["text"].strip()
        if corch is not None:                     # nota [N. DE E. ...] que continúa
            corch += " " + t
            if corch.count("[") <= corch.count("]"):
                notas.append(corch); corch = None
            prev = l; continue
        if t.startswith("[N. DE E.") and t.count("[") > t.count("]"):
            if cur: pars.append(" ".join(cur)); cur = []
            corch = t; prev = l; continue
        if t.startswith("[N. DE E.") and t.endswith("]"):
            if cur: pars.append(" ".join(cur)); cur = []
            notas.append(t); prev = l; continue
        if pend is not None:                      # anotación que continúa en la línea siguiente
            pend += " " + t
            if pend.count("(") == pend.count(")"):
                notas.append(pend); pend = None
            prev = l; continue
        if INICIO_ANOT.match(t) or (ANOTACION.match(t) and t == t.upper()):  # anotación editorial de la SCJN: no es texto del artículo
            if cur: pars.append(" ".join(cur)); cur = []
            if not t.startswith("("): t = "(" + t
            if t.count("(") == t.count(")"): notas.append(t)
            else: pend = t
            prev = l; continue
        salto = False
        if prev is not None and cur:
            if l["page"] != prev["page"]:
                # cambio de página: nuevo párrafo si la última línea de la página anterior quedó corta
                # (no llegó al margen derecho) y terminó en signo de cierre.
                salto = prev["x1"] < MARGEN_DERECHO - 25 and bool(re.search(r"[.;:]$", prev["text"].strip()))
            else:
                salto = (l["top"] - prev["top"]) > 1.45 * 12.2
        if salto and cur:
            pars.append(" ".join(cur)); cur = []
        cur.append(t); prev = l
    if cur: pars.append(" ".join(cur))
    pars = [re.sub(r"\s+", " ", p).strip() for p in pars]
    # Notas de editor de la SCJN sin paréntesis ("N. DE E. PARA CONSULTAR LA VERSIÓN CORREGIDA ..."):
    # párrafos íntegramente en mayúsculas que empiezan con "N. DE E." no son texto del artículo.
    editor = [p for p in pars if p.startswith("N. DE E.") and p == p.upper()]
    for p in editor:
        notas.insert(0, p); pars.remove(p)
        print("AVISO: nota de editor (N. DE E.) separada del texto", file=sys.stderr)
    # Caso especial (versión 14-08-2001): la SCJN deja "Art. 4o.- (DEROGADO PRIMER PARRAFO, ...)" como
    # marcador del párrafo derogado. Se pasa a notas y el prefijo "Art. 4o.-" se antepone al primer párrafo
    # subsistente, que es como lo presenta el texto consolidado de la Cámara de Diputados.
    if pars and re.match(r"^Art\. 4o\.- \(DEROGADO[^)]*\)$", pars[0]):
        notas.insert(0, pars[0][len("Art. 4o.- "):])
        pars = ["Art. 4o.- " + pars[1]] + pars[2:]
        print("AVISO: marcador de párrafo derogado convertido en nota (versión con DEROGADO PRIMER PARRAFO)", file=sys.stderr)
    return pars, notas

def es_mayusculas(t):
    return len(t) >= 20 and t == t.upper() and re.search(r"[A-ZÁÉÍÓÚÑ]{3}", t) is not None

for v in versiones:
    # líneas de nota de editor (mayúsculas) antes del arranque «Art. N.-» -> notas; y cola en mayúsculas al final -> notas
    ls = v["lineas"]
    k = next((i for i, l in enumerate(ls) if ARRANQUE.match(l["text"].strip())), None)
    pre = []
    if k:
        pre = [l["text"].strip() for l in ls[:k] if es_mayusculas(l["text"].strip()) or l["text"].strip().startswith("[N. DE E.") or ANOTACION.match(l["text"].strip())]
        resto = [l for l in ls[:k] if l["text"].strip() not in pre]
        if resto:
            print("AVISO: texto no identificado antes del arranque:", v["publicacion"], [l["text"][:50] for l in resto], file=sys.stderr)
        ls = resto + ls[k:]
    cola = []
    while ls and es_mayusculas(ls[-1]["text"].strip()) and not ANOTACION.match(ls[-1]["text"].strip()):
        cola.insert(0, ls.pop()["text"].strip())
    v["lineas"] = ls
    pars, notas = parrafos_de(v["lineas"])
    # fracción/inciso derogado: la SCJN escribe «II.- (REFORMADA [N. DE E. DEROGADA], D.O.F. 8 DE OCTUBRE DE 1974)».
    # Se conserva el numeral con la mención «(Derogada)» y la anotación completa pasa a notas.
    RX_DEROG = re.compile(r"^((?:[IVXLC]{1,7}(?:-[A-Z])?|\d+[oaª]|[A-Z]|[a-z]\))[.)]?-?)\s*(\((?:REFORMAD[AO]|ADICIONAD[AO]|DEROGAD[AO])\s*\[N\. DE E\. DEROGAD[AO]\][^)]*\)|\(DEROGAD[AO][^)]*\))\s*$")
    # línea de fracción derogada pegada a la fracción siguiente por un corte de página: se separa primero
    RX_DEROG_INLINE = re.compile(r"^((?:[IVXLC]{1,7}(?:-[A-Z])?|\d+[oaª]|[A-Z]|[a-z]\))[.)]?-?)\s*(\((?:REFORMAD[AO]|ADICIONAD[AO]|DEROGAD[AO])\s*\[N\. DE E\. DEROGAD[AO]\][^)]*\)|\(DEROGAD[AO][^)]*\))\s+(?=(?:[IVXLC]{1,7}(?:-[A-Z])?|\d+[oaª]|[A-Z]|[a-z]\))[.)]-?\s)")
    nuevos = []
    for par in pars:
        m = RX_DEROG_INLINE.match(par)
        if m:
            nuevos.append(m.group(1) + " " + m.group(2)); nuevos.append(par[m.end():])
        else:
            nuevos.append(par)
    pars = nuevos
    for i, par in enumerate(pars):
        m = RX_DEROG.match(par)
        if m:
            notas.append(m.group(2)); pars[i] = m.group(1) + " (Derogada)"
    if pre:
        pre_s = re.sub(r"\s+", " ", " ".join(pre))
        if not pre_s.startswith("(") and pre_s.endswith(")") and re.match(r"^(REFORMAD|ADICIONAD|DEROGAD|REUBICAD)", pre_s):
            pre_s = "(" + pre_s
        notas.insert(0, pre_s)
    if cola: notas.append("[cola de nota de editor] " + re.sub(r"\s+", " ", " ".join(cola)))
    v["parrafos"], v["notas"] = pars, notas
    v["texto"] = "\n\n".join(pars)
    del v["lineas"]

json.dump(versiones, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"{len(versiones)} versiones extraídas")
for v in versiones:
    print(f"  {v['publicacion']}  pág. {v['page']:>2}  {len(v['parrafos']):>2} párrafos  {len(v['texto']):>5} chars  notas: {len(v['notas'])}")
