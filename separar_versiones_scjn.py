#!/usr/bin/env python3
"""Separa en versiones el historial de cada artículo de la CPEUM extraído de los PDF
«Historia del texto del artículo» de la SCJN (00_historia.pdf → PyMuPDF get_text("text")).

Uso:
    python3 separar_versiones_scjn.py historial_completo.json versiones_separadas.json [--sin-validar]

Entrada:  lista de objetos con "numero" (str/int) y "texto_completo" (str).
Salida:   lista de objetos {"numero", "total_versiones", "versiones":[{...}], "avisos":[...]}.

REGLAS (documentadas; cotejadas con los PDF de los Arts. 1o. y 4o.):

1. CORTE sólo en encabezados de nivel superior de la columna izquierda de la SCJN. En el flujo
   de PyMuPDF llegan partidos en varias líneas, por eso se buscan con espacios/saltos flexibles:
     - "Texto original ... D.O.F."
     - "Texto vigente ... D.O.F."
     - "Texto derivado de la reforma publicada en el D.O.F."
     - "Texto derivado de la fe de erratas publicada en el D.O.F."
     - "Texto derivado de la aclaración publicada en el D.O.F."
   Las notas parentéticas "(REFORMADO, D.O.F. ...)" NUNCA son frontera.

2. FECHA del encabezado: normalmente sigue al "D.O.F." como "dd de mes de\naaaa". Cuando el
   encabezado cae al pie de una página, PyMuPDF imprime primero el pie/encabezado corrido de la
   página siguiente y después la fecha ("03 de febrero de\n1983"), a veces tras una nota
   parentética. Regla: si no hay fecha inmediata, se toma la PRIMERA línea de fecha suelta
   (día + mes + año, sin otro texto en la línea) que aparezca dentro de esta versión, antes del
   siguiente encabezado. Si tampoco existe, la versión se conserva con fecha null y aviso.

3. LIMPIEZA del cuerpo (sin tocar el texto jurídico):
     - se eliminan encabezado/pie corridos de la SCJN ("Constitución Política de los Estados
       Unidos Mexicanos,", "que reforma la de 5 de febrero de 1857", "Centro de Documentación y
       Análisis...", "cdaacl@scjn.gob.mx") y los números de página sueltos;
     - las notas parentéticas en mayúsculas "(REFORMADO|ADICIONADO|DEROGADO|REUBICADO|F. DE E.|
       N. DE E. ...)" se extraen a `notas_scjn` y se retiran del cuerpo (pueden ocupar varias
       líneas; se cierran al balancear paréntesis);
     - las notas de editor "N. DE E. ..." en mayúsculas, sin paréntesis, también van a notas;
     - el marcador "Art. No.- (DEROGADO PRIMER PARRAFO, ...)" pasa a notas y el prefijo
       "Art. No.-" se antepone al primer párrafo subsistente (así lo presenta el consolidado de
       la Cámara de Diputados);
     - los párrafos se reconstruyen: líneas en blanco = fin de párrafo; una línea que termina en
       guion se une sin espacio con la siguiente si ésta empieza en minúscula.

4. DEDUPLICACIÓN sólo cuando coinciden fecha Y huella (SHA-1 del cuerpo normalizado). Dos
   versiones con el mismo texto y fechas distintas se conservan (son reformas que no tocaron
   el artículo en lo sustantivo, o decretos del mismo día).

5. VALIDACIÓN: Art. 1 → exactamente 4 versiones (1917-02-05, 2001-08-14, 2006-12-04,
   2011-06-10); Art. 4 → exactamente 25. Si falla, no se escribe la salida y se imprime el
   diagnóstico (encabezados detectados y fragmentos que parecen encabezados sin coincidir).
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata

MESES = {m: i + 1 for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
     "septiembre", "octubre", "noviembre", "diciembre"])}
MESES_RE = "|".join(MESES)
S = r"[ \t\r\n]+"          # espacio flexible (incluye saltos de línea del flujo de PyMuPDF)
So = r"[ \t\r\n]*"

# Encabezados de nivel superior (columna izquierda del PDF de la SCJN).
ENCABEZADO = re.compile(
    rf"(?P<enc>Texto{S}(?:"
    rf"(?P<original>original)|"
    rf"(?P<vigente>vigente)|"
    rf"derivado{S}de{S}la{S}(?P<tipo>reforma|fe{S}de{S}erratas|aclaraci[oó]n){S}publicad[ao]{S}en{S}el"
    rf"){So}D{So}\.{So}O{So}\.{So}F{So}\.?)"
    rf"(?P<fecha>{So}(?P<d>\d{{1,2}}){S}de{S}(?P<m>{MESES_RE}){S}de{S}(?P<y>\d{{4}}))?",
    re.IGNORECASE,
)
# Línea de fecha suelta: "03 de febrero de\n1983" o "03 de febrero de 1983" sola en su(s) línea(s).
FECHA_SUELTA = re.compile(
    rf"(?m)^[ \t]*(?P<d>\d{{1,2}})[ \t]+de[ \t]+(?P<m>{MESES_RE})[ \t]+de[ \t]*\n?[ \t]*(?P<y>\d{{4}})[ \t]*$",
    re.IGNORECASE,
)
# Anotaciones editoriales de la SCJN (van a notas_scjn)
NOTA_INICIO = re.compile(r"^\((?:REFORMAD|ADICIONAD|DEROGAD|REUBICAD|N\.\s*DE\s*E\.|F\.\s*DE\s*E\.)", re.IGNORECASE)
NOTA_EDITOR = re.compile(r"^N\.\s*DE\s*E\.\s")
MARCADOR_DEROGADO = re.compile(r"^(Art(?:ículo|\.)\s+\d+[oa]?\.?-?)\s*(\((?:DEROGAD)[^)]*\))\s*$", re.IGNORECASE)
# Ruido de encabezado/pie corrido y numeración de página
RUIDO = [
    re.compile(r"^Constitución Política de los Estados Unidos Mexicanos,?$"),
    re.compile(r"^que reforma la de 5 de febrero de 1857$"),
    re.compile(r"^Centro de Documentación y Análisis, Archivos y Compilación de Leyes$"),
    re.compile(r"^cdaacl@scjn\.gob\.mx$"),
    re.compile(r"^\d{1,3}$"),
]
POSIBLE_ENCABEZADO = re.compile(r"Texto\s+\w+|publicad[ao]\s+en\s+el\s+D", re.IGNORECASE)


def iso(d, m, y):
    return f"{int(y):04d}-{MESES[m.lower()]:02d}-{int(d):02d}"


def norm(s):
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip()


def huella(texto):
    return hashlib.sha1(norm(texto).lower().encode("utf-8")).hexdigest()[:16]


def limpiar_cuerpo(bruto, numero):
    """Devuelve (texto_juridico, notas_scjn, fecha_suelta_o_None)."""
    lineas = [l.rstrip() for l in bruto.split("\n")]
    # 1) fecha suelta (para encabezados cuya fecha quedó tras el corte de página)
    fecha_suelta = None
    m = FECHA_SUELTA.search(bruto)
    if m:
        fecha_suelta = iso(m.group("d"), m.group("m"), m.group("y"))
        # retira esas líneas del cuerpo
        bruto2 = bruto[:m.start()] + bruto[m.end():]
        lineas = [l.rstrip() for l in bruto2.split("\n")]

    notas, parrafos, cur, pend, editor = [], [], [], None, False
    def cerrar():
        nonlocal cur
        if cur:
            parrafos.append(" ".join(cur)); cur = []
    for raw in lineas:
        t = raw.strip()
        if pend is not None:                       # nota parentética que continúa
            pend += " " + t
            if pend.count("(") <= pend.count(")"):
                notas.append(norm(pend)); pend = None
            continue
        if not t:
            cerrar(); continue
        if any(r.match(t) for r in RUIDO):
            continue
        md = MARCADOR_DEROGADO.match(t)
        if md:                                     # "Art. 4o.- (DEROGADO PRIMER PARRAFO, ...)"
            cerrar(); notas.append(md.group(2)); parrafos.append(("__PREFIJO__", md.group(1))); continue
        if NOTA_INICIO.match(t):
            cerrar()
            if t.count("(") <= t.count(")"): notas.append(norm(t))
            else: pend = t
            continue
        if NOTA_EDITOR.match(t) and t == t.upper():
            cerrar(); notas.append(norm(t)); editor = True; continue
        if editor and t == t.upper() and re.search(r"[A-ZÁÉÍÓÚÑ]{3}", t):
            notas[-1] = norm(notas[-1] + " " + t); continue   # continuación de la nota de editor (líneas en mayúsculas)
        editor = False
        if cur and cur[-1].endswith("-") and re.match(r"^[a-záéíóúñ]", t):
            cur[-1] = cur[-1] + t                  # palabra partida con guion
        else:
            cur.append(t)
    cerrar()
    if pend is not None:
        notas.append(norm(pend))
    # notas de editor en mayúsculas que quedaron como párrafo
    limpios = []
    prefijo = None
    for p in parrafos:
        if isinstance(p, tuple):
            prefijo = p[1]; continue
        if NOTA_EDITOR.match(p) and p == p.upper():
            notas.append(norm(p)); continue
        p = norm(p)
        if prefijo and not re.match(r"^Art(ículo|\.)\s", p):
            p = prefijo + " " + p; prefijo = None
        limpios.append(p)
    return "\n\n".join(limpios), notas, fecha_suelta


def separar(texto, numero):
    """Corta el texto completo de un artículo en versiones. Devuelve (versiones, avisos, diagnostico)."""
    encs = list(ENCABEZADO.finditer(texto))
    avisos, diag = [], {"encabezados": [], "sospechosos": []}
    versiones = []
    for i, m in enumerate(encs):
        fin = encs[i + 1].start() if i + 1 < len(encs) else len(texto)
        if m.group("original"): tipo = "original"
        elif m.group("vigente"): tipo = "vigente"
        else:
            t = norm(m.group("tipo")).lower()
            tipo = "fe_de_erratas" if "erratas" in t else ("aclaracion" if "aclar" in t else "reforma")
        fecha = iso(m.group("d"), m.group("m"), m.group("y")) if m.group("fecha") else None
        cuerpo_bruto = texto[m.end():fin]
        cuerpo, notas, fecha_suelta = limpiar_cuerpo(cuerpo_bruto, numero)
        origen_fecha = "encabezado"
        if fecha is None and fecha_suelta:
            fecha, origen_fecha = fecha_suelta, "fecha suelta tras corte de página"
        elif fecha is None:
            origen_fecha = "no encontrada"
            avisos.append(f"encabezado #{i+1} ({tipo}) sin fecha; se conserva con fecha null")
        versiones.append({
            "orden": i + 1, "tipo": tipo, "fecha_dof": fecha, "origen_fecha": origen_fecha,
            "encabezado_scjn": norm(m.group("enc") + (m.group("fecha") or "")),
            "texto": cuerpo, "notas_scjn": notas, "huella": huella(cuerpo),
        })
        diag["encabezados"].append({"orden": i + 1, "tipo": tipo, "fecha": fecha, "origen": origen_fecha})
    # fragmentos que parecen encabezado pero no coincidieron
    cubiertos = [(m.start(), m.end()) for m in encs]
    for s in POSIBLE_ENCABEZADO.finditer(texto):
        if not any(a <= s.start() < b for a, b in cubiertos):
            diag["sospechosos"].append(norm(texto[s.start(): s.start() + 120]))
    # deduplicación: fecha + huella
    vistos, dedup = set(), []
    for v in versiones:
        k = (v["fecha_dof"], v["huella"])
        if k in vistos:
            avisos.append(f"versión duplicada eliminada: {v['fecha_dof']} ({v['tipo']})"); continue
        vistos.add(k); dedup.append(v)
    return dedup, avisos, diag


ESPERADO = {
    "1": ["1917-02-05", "2001-08-14", "2006-12-04", "2011-06-10"],
    "4": 25,
}


def validar(resultados):
    ok = True
    por_num = {str(r["numero"]).lstrip("0") or "0": r for r in resultados}
    for num, esp in ESPERADO.items():
        r = por_num.get(num)
        if r is None:
            print(f"VALIDACIÓN: el Art. {num} no está en la entrada; no se puede validar"); ok = False; continue
        fechas = [v["fecha_dof"] for v in r["versiones"]]
        n_esp = len(esp) if isinstance(esp, list) else esp
        cumple = len(fechas) == n_esp and (not isinstance(esp, list) or fechas == esp)
        print(f"VALIDACIÓN Art. {num}: {len(fechas)} versiones (esperadas {n_esp}) -> {'OK' if cumple else 'FALLA'}")
        print("   fechas:", ", ".join(f or "null" for f in fechas))
        if r["avisos"]: print("   avisos:", "; ".join(r["avisos"]))
        if not cumple:
            ok = False
            print("   encabezados detectados:")
            for e in r["diagnostico"]["encabezados"]: print("     ", e)
            if r["diagnostico"]["sospechosos"]:
                print("   fragmentos que parecen encabezado y NO coincidieron:")
                for s in r["diagnostico"]["sospechosos"]: print("      ·", s)
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada"); ap.add_argument("salida")
    ap.add_argument("--sin-validar", action="store_true", help="escribe la salida aunque falle la validación")
    a = ap.parse_args(argv)
    datos = json.load(open(a.entrada, encoding="utf-8"))
    resultados = []
    for art in datos:
        texto = art.get("texto_completo") or ""
        num = str(art.get("numero", "?"))
        versiones, avisos, diag = separar(texto, num)
        if not versiones: avisos.append("0 versiones detectadas")
        resultados.append({"numero": num, "total_versiones": len(versiones), "versiones": versiones,
                           "avisos": avisos, "diagnostico": diag})
    total = sum(r["total_versiones"] for r in resultados)
    print(f"{len(resultados)} artículos procesados; {total} versiones")
    sin_fecha = [(r["numero"], v["orden"]) for r in resultados for v in r["versiones"] if not v["fecha_dof"]]
    if sin_fecha: print("versiones sin fecha:", sin_fecha)
    ceros = [r["numero"] for r in resultados if r["total_versiones"] == 0]
    if ceros: print("artículos con 0 versiones:", ceros)
    ok = validar(resultados)
    if not ok and not a.sin_validar:
        print("ABORTADO: la validación de los Arts. 1 y 4 no pasó; no se escribió la salida.")
        return 1
    for r in resultados:   # el diagnóstico no va a la salida
        r.pop("diagnostico", None)
    json.dump(resultados, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Guardado: {a.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
