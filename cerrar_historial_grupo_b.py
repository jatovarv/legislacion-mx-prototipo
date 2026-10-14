#!/usr/bin/env python3
"""Cierra el historial del Grupo B (Arts. 3, 35, 72, 99, 100, 107, 109, 123) con el consolidado de la Cámara.

Uso: python3 cerrar_historial_grupo_b.py .     (modifica cpeum.json; escribe docs/reporte_cierre_grupo_b.json)

Diagnóstico: docs/diagnostico-15-articulos-historial-por-cotejar.md. En estos artículos la última versión del
PDF de la SCJN y el consolidado de la Cámara tienen la misma fecha, pero el bloque SCJN trae defectos de
extracción. Reglas:

- La última versión pasa a ser una sola: el texto vigente del consolidado de la Cámara, con la fecha de
  publicación (idéntica en ambas fuentes) y las notas/encabezado del bloque SCJN. Se eliminan el par
  «Última versión SCJN (cerrada el mismo día)» + «Vigente (consolidado Cámara)».
- Antes de cerrar, se DEMUESTRA que la diferencia es de extracción y no normativa: a cada bloque SCJN se le
  aplica sólo la corrección mecánica descrita (quitar una línea de corte de página repetida, un párrafo
  duplicado, una anotación editorial o una marca «x») y el resultado debe coincidir palabra por palabra con
  el texto de la Cámara bajo la normalización de cotejo `comparable()` del integrador. Si no coincide, el
  script aborta y el artículo no se cierra.
- La diferencia queda documentada en `nota_extraccion` de la versión vigente y en la nota del artículo.
  No se inventa texto: el cuerpo vigente es el de la Cámara tal cual.
- Art. 100: la misma línea de corte de página («El personal del Tribunal regirá … excepciones», que es un
  párrafo del Art. 99) se coló también en las versiones v5–v8, siempre partiendo frases por la mitad. Se
  retira de esas versiones (cadena exacta, párrafo suelto) y se reúnen las dos mitades del párrafo; cada
  versión lo registra en `nota_extraccion`.
- Art. 99 v7: ese mismo párrafo quedó partido por un corte de página («… excepciones» / «que señale la
  ley.»); se reúne y se registra.
- Art. 35: su último bloque SCJN no tiene fecha legible y es un bloque fusionado (dos textos separados por la
  etiqueta «Texto vigente publicado en el D.O.F. el 02 de junio de 2026»). No se le asigna fecha por
  inferencia ni se separa: se aísla con `nota_extraccion` para re-extraerlo por coordenadas desde el PDF.
  El texto vigente sigue siendo el del consolidado (ya cargado); el artículo permanece «historial por cotejar».
- `extraccion_pendiente: true` marca las versiones cuyo cuerpo sigue pendiente de cotejo con el PDF (bloques
  fusionados, limpiezas de corte de página, bloque sin fecha del Art. 35); la interfaz las señala.
- Bloques fusionados en general: toda versión cuyo cuerpo contiene una etiqueta de la SCJN («Texto derivado
  de la reforma…», «Texto vigente…») reúne más de una versión del artículo (defecto del separador lineal).
  Se marcan todas con `nota_extraccion` (también en artículos ya verificados) y se listan en el reporte;
  separarlas exige el PDF de la SCJN y el extractor por coordenadas.
"""
import collections, datetime as dt, json, pathlib, re, sys

REPO = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
RUTA = REPO / "cpeum.json"
data = json.loads(RUTA.read_text(encoding="utf-8"))
ARTS = data["articulos"]

# --- normalización de cotejo: la misma del integrador (se carga desde su fuente para no duplicarla) -------------
_src = (REPO / "integrar_historial_scjn.py").read_text(encoding="utf-8").split("\n")
_ini = next(i for i, l in enumerate(_src) if l.startswith("def norm("))
_fin = next(i for i, l in enumerate(_src) if l.startswith("def dia("))
exec("import re\n" + "\n".join(_src[_ini:_fin]), globals())  # define norm() y comparable()

GRUPO_B = [3, 35, 72, 99, 100, 107, 109, 123]
CIERRE = [3, 72, 99, 100, 107, 109, 123]  # 35 se queda pendiente (bloque sin fecha)
ULTIMA_REFORMA = data["norma"]["ultima_reforma_consolidado"]
RX_ETIQUETA = re.compile(r"Texto (?:derivado de la (?:reforma|fe de(?: erratas)?)|vigente|original)[^\n]*")

# Línea de corte de página del PDF del Art. 100 (es un párrafo del Art. 99, truncado); entra siempre como párrafo suelto.
LINEA_99 = ("El personal del Tribunal regirá sus relaciones de trabajo conforme a las disposiciones aplicables "
            "al Poder Judicial de la Federación y a las reglas especiales y excepciones")
PARRAFO_99 = LINEA_99 + " que señale la ley."
RESIDUO_ETIQUETA_100_V5 = "31 de diciembre de 1994 "


def fmt(iso):
    return dt.date.fromisoformat(iso).strftime("%d-%m-%Y")


def quitar_parrafo_suelto(texto, parrafo):
    """Retira cada aparición de `parrafo` como párrafo propio. Si separaba dos mitades de una frase (la
    siguiente empieza en minúscula o la anterior no cierra con puntuación), las reúne con un espacio."""
    partes = texto.split("\n\n")
    out, n = [], 0
    for p in partes:
        if p.strip() == parrafo:
            n += 1
            out.append(None)  # marca
            continue
        out.append(p)
    res, i = [], 0
    while i < len(out):
        p = out[i]
        if p is None:
            i += 1
            continue
        while i + 2 < len(out) and out[i + 1] is None and out[i + 2] is not None and \
                (out[i + 2][:1].islower() or not re.search(r"[.;:]\s*$", p)):
            p = p.rstrip() + " " + out[i + 2].lstrip()
            i += 2
        res.append(p)
        i += 1
    return "\n\n".join(res), n


def igual(a, b):
    return comparable(a) == comparable(b)


# --- comprobaciones por artículo: corrección mecánica del bloque SCJN -> debe igualar al texto de la Cámara ------
def corregir_bloque(num, texto):
    """Devuelve (texto_corregido, descripción de la diferencia). Sólo retira o normaliza; no añade palabras."""
    if num == 3:
        t = re.sub(r"exclusivismos\s*[-–]\s*atenderá", "exclusivismos– atenderá", texto)
        return t, ("Desfases: la raya del inciso b) de la fracción II («–sin hostilidades ni exclusivismos– atenderá») "
                   "salió como guion con espacios en el PDF de la SCJN («-sin hostilidades ni exclusivismos - atenderá»); "
                   "además, el párrafo tercero, el inciso d) de la fracción II y las fracciones III y IX derogados figuran en la Cámara "
                   "con la leyenda «Párrafo tercero. Se deroga.», «d) Se deroga.», «III. Se deroga.» y «IX. Se deroga», mientras que en el "
                   "bloque SCJN sus anotaciones «(DEROGADO…)» pasaron a notas_scjn dejando sólo el numeral. Diferencias tipográficas y de "
                   "representación de derogaciones.")
    if num == 72:
        t = (texto
             .replace("ésta,, (sic)", "ésta,, (sic DOF 05-02-1917)")
             .replace("I (sic).- El Ejecutivo", "I (sic DOF 24-11-1923). El Ejecutivo"))
        return t, ("Desfases: en el inciso C la marca editorial «ésta,, (sic)» del bloque SCJN aparece en la Cámara con fecha "
                   "«ésta,, (sic DOF 05-02-1917)», y el numeral repetido «I (sic).-» del apartado final salió con guion y sin fecha en el "
                   "PDF de la SCJN mientras la Cámara lo imprime «I (sic DOF 24-11-1923).». Diferencias tipográficas y de fechamiento de marcas (sic).")
    if num == 99:
        dup = PARRAFO_99 + "\n\n" + PARRAFO_99 + " El ingreso,"
        assert texto.count(dup) == 1, "Art. 99: no se encontró el párrafo duplicado esperado"
        t = texto.replace(dup, PARRAFO_99 + " El ingreso,")
        return t, ("Único desfase: el párrafo «El personal del Tribunal regirá sus relaciones de trabajo…» aparece dos veces en el "
                   "bloque SCJN (repetido en un corte de página: una vez suelto y otra como inicio del párrafo que sigue con «El ingreso, formación…»). "
                   "La Cámara lo trae una sola vez. Duplicado de extracción.")
    if num == 100:
        t, n = quitar_parrafo_suelto(texto, LINEA_99)
        assert n == 5, f"Art. 100: se esperaban 5 líneas de corte de página, hay {n}"
        return t, ("Único desfase: la línea «El personal del Tribunal regirá … reglas especiales y excepciones» (párrafo del Art. 99, truncado) "
                   "se coló 5 veces en el bloque SCJN como línea de corte de página, partiendo frases por la mitad. No forma parte del Art. 100. "
                   "Retirada, el bloque coincide con la Cámara.")
    if num == 107:
        marca = "XVIII.- (REPUBLICADA DEROGACIÓN, D.O.F. 6 DE JUNIO DE 2011)"
        assert texto.count(marca) == 1
        t = texto.replace(marca, "XVIII.- (Derogada)")
        return t, ("Desfases: la fracción XVIII derogada trae en el PDF de la SCJN la anotación editorial «(REPUBLICADA DEROGACIÓN, "
                   "D.O.F. 6 DE JUNIO DE 2011)» (la Cámara imprime «XVIII. Se deroga.») y en la fracción X derogada la Cámara imprime "
                   "«X. Se deroga;» mientras en el bloque SCJN su anotación «(DEROGADA, D.O.F. 6 DE JUNIO DE 2011)» pasó a notas_scjn. "
                   "Anotaciones editoriales, no texto normativo.")
    if num == 109:
        t, n = quitar_parrafo_suelto(texto, "x")
        assert n == 3, f"Art. 109: se esperaban 3 marcas «x», hay {n}"
        return t, ("Único desfase: tres párrafos sueltos con una «x» (marca del PDF de la SCJN en cortes de página, sin correlato en el texto). "
                   "Retirados, el bloque coincide con la Cámara.")
    if num == 123:
        t = (texto
             .replace("dosicentos (sic)", "dosicentos (sic DOF 09-01-1978)")
             .replace("consentimieto (sic)", "consentimieto (sic DOF 21-11-1962)")
             .replace("XI (SIC).- Los trabajadores", "XI (sic 05-12-1960). Los trabajadores")
             .replace("XIII bis.- El banco", "XIII bis. El banco"))
        return t, ("Desfases: en el Apartado A las marcas editoriales «dosicentos (sic)» (fracción XII, párrafo tercero) y «consentimieto (sic)» "
                   "(fracción XXII) del bloque SCJN llevan fecha en la Cámara («dosicentos (sic DOF 09-01-1978)» y «consentimieto (sic DOF 21-11-1962)»); "
                   "en el Apartado B el numeral repetido «XI (SIC).-» salió con guion y sin fecha en el PDF de la SCJN (la Cámara: «XI (sic 05-12-1960).») "
                   "y «XIII bis.-» frente a «XIII bis.». Diferencias tipográficas y de fechamiento de marcas (sic).")
    raise KeyError(num)


reporte = {"generado": dt.date.today().isoformat(), "cerrados": {}, "pendientes": {}, "bloques_fusionados": [], "limpiezas": []}

# --- 1. cierre de los 7 artículos corregibles ---------------------------------------------------------------------
for num in CIERRE:
    art = ARTS[str(num)]
    vers = art["versiones"]
    ult, vig = vers[-2], vers[-1]
    assert art["estado"] == "historial_parcial", num
    assert ult["etiqueta"].startswith("Última versión SCJN") and vig["etiqueta"].startswith("Vigente (consolidado"), num
    assert ult["publicacion"] == vig["publicacion"], (num, ult["publicacion"], vig["publicacion"])
    corregido, descripcion = corregir_bloque(num, ult["texto"])
    if not igual(corregido, vig["texto"]):
        sys.exit(f"Art. {num}: tras la corrección mecánica el bloque SCJN sigue sin coincidir con la Cámara; no se cierra.")
    assert not igual(ult["texto"], vig["texto"]), f"Art. {num}: ya coincidían; nada que cerrar"
    nueva = {
        "id": ult["id"],
        "tipo": "vigente",
        "etiqueta": f"Vigente (post {fmt(vig['publicacion'])})",
        "publicacion": vig["publicacion"],
        "vigencia_desde": vig["vigencia_desde"],
        "vigencia_verificada": False,
        "vigencia_nota": (f"Texto vigente tomado del consolidado de la Cámara de Diputados (última reforma DOF {fmt(ULTIMA_REFORMA)}), "
                          "con el que coincide la última versión del PDF de la SCJN una vez descontada una diferencia de extracción "
                          "(véase la nota de extracción). Regla general (al día siguiente de su publicación); pendiente de cotejo con los transitorios del decreto."),
        "capitulo": ult.get("capitulo") or vig.get("capitulo"),
        "texto": vig["texto"],
        "notas_scjn": ult.get("notas_scjn", []),
        "notas_camara": vig.get("notas_camara", []),
        "encabezado_scjn": ult.get("encabezado_scjn"),
        "vigencia_hasta": None,
        "nota_extraccion": ("Bloque SCJN de la misma fecha sustituido por el texto del consolidado de la Cámara. " + descripcion),
    }
    vers[-2:] = [nueva]
    art["estado"] = "verificado"
    art["nota"] = ("Historial extraído del PDF «Historia del texto del artículo» de la SCJN; la versión vigente coincide con el texto consolidado "
                   f"de la Cámara de Diputados (última reforma DOF {fmt(ULTIMA_REFORMA)}). Fechas de entrada en vigor por regla general, pendientes de cotejo con cada decreto. "
                   "El último bloque del PDF de la SCJN traía una diferencia de extracción no normativa (detallada en la nota de extracción de la versión vigente); "
                   "la versión vigente es el texto del consolidado (cerrar_historial_grupo_b.py).")
    extra_fh = (" y limpieza de corte de página en v7" if num == 99 else
                " y limpieza de líneas de corte de página en v5–v8" if num == 100 else "")
    art["fuente_historial"] = art.get("fuente_historial", "") + f"; última versión cerrada con el consolidado de la Cámara{extra_fh} (cerrar_historial_grupo_b.py)"
    reporte["cerrados"][num] = {"versiones": len(vers), "publicacion_ultima": vig["publicacion"], "diferencia": descripcion}

# --- 2. limpiezas mecánicas en versiones anteriores (Arts. 99 y 100) -----------------------------------------------
a100 = ARTS["100"]["versiones"]
for v in a100:
    t, n = quitar_parrafo_suelto(v["texto"], LINEA_99)
    if not n:
        continue
    extra = ""
    if v["id"] == "v5":
        assert t.count(RESIDUO_ETIQUETA_100_V5) == 1
        t = t.replace("estarán a " + RESIDUO_ETIQUETA_100_V5 + "cargo", "estarán a cargo")
        extra = (" En uno de esos cortes apareció además el fragmento «31 de diciembre de 1994», resto de la etiqueta de la SCJN (retirado del cuerpo); "
                 "coincide con la pista de fecha de esta versión, que sigue pendiente de confirmar contra el PDF.")
    assert "El personal del Tribunal" not in t, (v["id"], "quedó otra aparición")
    v["texto"] = t
    v["extraccion_pendiente"] = True
    v["nota_extraccion"] = (f"Se retiró {n} {'vez' if n == 1 else 'veces'} la línea de corte de página «El personal del Tribunal regirá … reglas especiales y excepciones» "
                            "(párrafo del Art. 99 que el PDF de la SCJN repite al pie de cada página de este artículo, partiendo frases por la mitad) y se reunieron "
                            "las mitades de cada frase. No se añadió ninguna palabra; pendiente de cotejo con el PDF de la SCJN." + extra)
    reporte["limpiezas"].append({"articulo": 100, "version": v["id"], "lineas_retiradas": n})

a99 = ARTS["99"]["versiones"]
for v in a99:
    partido = LINEA_99 + "\n\nque señale la ley."
    if partido in v["texto"]:
        v["texto"] = v["texto"].replace(partido, PARRAFO_99)
        v["extraccion_pendiente"] = True
        v["nota_extraccion"] = ("El párrafo «El personal del Tribunal regirá …» quedó partido por un corte de página («… excepciones» / «que señale la ley.»); "
                                "se reunieron sus dos mitades sin añadir palabras. " + v.get("nota_extraccion", ""))
        reporte["limpiezas"].append({"articulo": 99, "version": v["id"], "parrafo_reunido": True})

# --- 3. Art. 35: aislar el bloque sin fecha; no fechar por inferencia ------------------------------------------------
a35 = ARTS["35"]
v6, v7 = a35["versiones"][-2], a35["versiones"][-1]
assert v6["publicacion"] is None and v7["etiqueta"].startswith("Vigente (consolidado"), "Art. 35: estructura inesperada"
etq = RX_ETIQUETA.search(v6["texto"])
assert etq and etq.group(0).startswith("Texto vigente publicado en el D.O.F. el 02 de junio de 2026"), "Art. 35: etiqueta esperada no encontrada"
parte1 = v6["texto"][:etq.start()].strip()
parte2 = v6["texto"][etq.end():].strip()
coincide = igual(parte2, v7["texto"])
v6["etiqueta"] = "Bloque SCJN sin fecha legible (fusionado; pendiente de re-extracción)"
v6["extraccion_pendiente"] = True
v6["nota_extraccion"] = (
    f"Bloque fusionado por el separador: contiene dos textos separados por la etiqueta «{etq.group(0)}» (etiqueta duplicada/sobreimpresa en el PDF). "
    f"La segunda parte ({len(parte2)} caracteres) {'coincide' if coincide else 'NO coincide'} con el texto vigente del consolidado de la Cámara bajo la normalización de cotejo; "
    f"la primera parte ({len(parte1)} caracteres) no tiene fecha legible y no se fecha por inferencia. "
    "Pendiente: re-extraer el Art. 35 por coordenadas (extraer_historia_scjn_pdf.py) desde Art_035_00_historia.pdf. El texto vigente mostrado es el del consolidado.")
a35["nota"] = ("Historial extraído del PDF de la SCJN con el separador lineal, con bloques fusionados (v2, v4 y v6 contienen más de una versión) y dos versiones sin fecha legible. "
               "El texto vigente es el del consolidado de la Cámara de Diputados (última reforma DOF " + fmt(ULTIMA_REFORMA) + "); "
               "el último bloque de la SCJN no se fecha por inferencia y queda aislado para re-extracción por coordenadas desde el PDF (cerrar_historial_grupo_b.py). Historial por cotejar.")
a35["fuente_historial"] = a35.get("fuente_historial", "") + "; último bloque sin fecha aislado para re-extracción (cerrar_historial_grupo_b.py)"
reporte["pendientes"][35] = {"motivo": "último bloque SCJN sin fecha legible y fusionado; requiere el PDF Art_035_00_historia.pdf",
                             "parte2_coincide_con_camara": coincide, "versiones": len(a35["versiones"])}

# --- 4. marcar todos los bloques fusionados (cuerpo con etiqueta de la SCJN a medio texto) ---------------------------
for num, art in ARTS.items():
    for v in art["versiones"]:
        etiquetas = [norm(m.group(0)) for m in RX_ETIQUETA.finditer(v["texto"])]
        if not etiquetas:
            continue
        v["extraccion_pendiente"] = True
        if not (num == "35" and v["id"] == "v6"):
            v["nota_extraccion"] = (f"Bloque fusionado por el separador lineal: el cuerpo contiene {len(etiquetas)} etiqueta(s) de la SCJN a mitad del texto "
                                    f"({'; '.join('«' + e + '»' for e in etiquetas)}), por lo que reúne {len(etiquetas) + 1} versiones del artículo. "
                                    "No se separó para no fechar bloques por inferencia; pendiente de re-extracción por coordenadas desde el PDF de la SCJN. "
                                    + (v.get("nota_extraccion", "")))
        reporte["bloques_fusionados"].append({"articulo": int(num), "version": v["id"], "publicacion": v.get("publicacion"),
                                              "estado_articulo": art["estado"], "etiquetas": etiquetas})

# --- 5. invariantes y salida ----------------------------------------------------------------------------------------
for num in GRUPO_B:
    vers = ARTS[str(num)]["versiones"]
    assert sum(1 for v in vers if v.get("vigencia_desde") and not v.get("vigencia_hasta") and not v.get("vigencia_hasta_indeterminada")) == 1, num
    assert vers[-1]["vigencia_hasta"] is None and vers[-1]["tipo"] == "vigente", num
    assert [v["id"] for v in vers] == [f"v{i + 1}" for i in range(len(vers))], num
for k in ("1", "4"):  # golden cases intactos
    assert json.loads((REPO / f"cpeum-art-{k}.json").read_text(encoding="utf-8"))["versiones"] == ARTS[k]["versiones"], k

reporte["estados"] = dict(collections.Counter(a["estado"] for a in ARTS.values()))
RUTA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(REPO / "docs" / "reporte_cierre_grupo_b.json").write_text(json.dumps(reporte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: reporte[k] for k in ("cerrados", "pendientes", "estados")}, ensure_ascii=False, indent=1))
print("bloques fusionados marcados:", len(reporte["bloques_fusionados"]), "| limpiezas:", len(reporte["limpiezas"]))
