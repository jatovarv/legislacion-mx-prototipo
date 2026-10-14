# Reporte del Grupo A — Artículos con historial por cotejar (Arts. 2, 10, 20, 22, 82, 116 y 122)

## 1. Resumen ejecutivo

De los **7 artículos del Grupo A** diagnosticados previamente en `docs/diagnostico-15-articulos-historial-por-cotejar.md`, la inspección directa por coordenadas (`extraer_historia_scjn_pdf.py`) de sus archivos `00_historia.pdf` en `CPEUM_SCJN_Historial/cpeum_scjn.zip` demostró que el grupo se divide en dos subconjuntos:

1. **4 artículos cuyo PDF de la SCJN SÍ está actualizado hasta la última reforma y se cierran como `verificado` en este PR (`Arts. 2, 10, 20 y 22`):**
   - El PDF de la SCJN no estaba desactualizado: contenía todas las reformas hasta la versión vigente inclusive, pero el separador lineal (`separar_versiones_scjn.py`) había dejado de cortar en una versión intermedia porque las etiquetas de la columna izquierda escribían `DOF` sin puntos (Art. 2), anteponían `Texto vigente derivado de la reforma…` (Art. 10), omitían las siglas `D.O.F.` (`Texto vigente 15 de septiembre de 2024`, Art. 20) o quedaban partidas por un salto de página entre `Texto derivado de la reforma` y `publicada en el D.O.F. …` (Art. 22).
   - Al extraer por coordenadas con `extraer_historia_scjn_pdf.py`, se recuperan todas las versiones intermedias y vigentes con sus fechas legibles en el PDF, y la última versión de la SCJN coincide íntegramente (`comparable() == True`) con el texto vigente del consolidado de la Cámara de Diputados.

2. **3 artículos cuyo PDF de la SCJN es anterior a la reforma `DOF 07-10-2026` y permanecen en `historial_parcial` pendientes de PDF actualizado (`Arts. 82, 116 y 122`):**
   - El PDF de la SCJN llega hasta el `01-04-2025` (Art. 82) o hasta el `02-06-2026` (Arts. 116 y 122), mientras que el texto vigente del consolidado de la Cámara de Diputados incorpora la reforma publicada en el **DOF 07-10-2026**.
   - **No falta ninguna reforma intermedia** entre la última versión del PDF de la SCJN (`01-04-2025` / `02-06-2026`) y la reforma vigente de la Cámara (`07-10-2026`). La única reforma ausente en el PDF de la SCJN es precisamente el decreto vigente del `07-10-2026`, cuyo texto consolidado oficial ya obra como última versión de cada uno de estos tres artículos en `cpeum.json`.

---

## 2. Tabla comparativa de los 7 artículos del Grupo A

| Artículo | Última fecha SCJN (separador lineal previo) | Última fecha real en PDF SCJN (`00_historia.pdf`) | Fecha del texto vigente (Cámara) | Reformas posteriores al corte lineal (según `notas_camara`) | ¿PDF SCJN actualizado? | Estado resultante |
|---:|---|---|---|---|---|---|
| **Art. 2o.** | `2015-05-22` (`v3` fusionada) | **`2024-09-30`** (`v7`, 7 versiones en PDF) | `2024-09-30` | `29-01-2016`, `06-06-2019`, `09-08-2019`, `30-09-2024` (todas presentes en el PDF SCJN) | **Sí** (`Titulo_Primero/Art_002/00_historia.pdf`) | **`verificado`** (cerrado) |
| **Art. 10** | `1971-10-22` (`v2` fusionada) | **`2019-03-26`** (`v3`, 3 versiones en PDF) | `2019-03-26` | `26-03-2019` (presente en el PDF SCJN) | **Sí** (`Titulo_Primero/Art_010/00_historia.pdf`) | **`verificado`** (cerrado) |
| **Art. 20** | `2011-07-14` (`v9` fusionada) | **`2024-09-15`** (`v10`, 10 versiones en PDF) | `2024-09-15` | `15-09-2024` (presente en el PDF SCJN; nota Cámara cita `29-01-2016` sólo en transitorio de reforma previa) | **Sí** (`Titulo_Primero/Art_020/00_historia.pdf`) | **`verificado`** (cerrado) |
| **Art. 22** | `2015-05-27` (`v6` fusionada) | **`2019-03-14`** (`v8`, 8 versiones en PDF) | `2019-03-14` | `18-06-2008` (fusionada en `v5`) y `14-03-2019` (fusionada en `v6`; ambas presentes en el PDF SCJN) | **Sí** (`Titulo_Primero/Art_022/00_historia.pdf`) | **`verificado`** (cerrado) |
| **Art. 82** | `2025-04-01` (`v11`) | `2025-04-01` (`v11`, 11 versiones en PDF) | `2026-10-07` | **Ninguna intermedia**; sólo falta en el PDF SCJN la reforma vigente `DOF 07-10-2026` (fracc. I) | **No** (anterior a `DOF 07-10-2026`) | `historial_parcial` (pendiente de PDF SCJN) |
| **Art. 116** | `2026-06-02` (`v21`) | `2026-06-02` (`22` versiones en PDF) | `2026-10-07` | **Ninguna intermedia**; sólo falta en el PDF SCJN la reforma vigente `DOF 07-10-2026` (fracc. I, párrafos quinto y sexto) | **No** (anterior a `DOF 07-10-2026`) | `historial_parcial` (pendiente de PDF SCJN) |
| **Art. 122** | `2026-06-02` (`v20`) | `2026-06-02` (`21` versiones en PDF) | `2026-10-07` | **Ninguna intermedia**; sólo falta en el PDF SCJN la reforma vigente `DOF 07-10-2026` (Apartado A, fracc. III, párrafos segundo y tercero) | **No** (anterior a `DOF 07-10-2026`) | `historial_parcial` (pendiente de PDF SCJN) |

---

## 3. Detalle por artículo

### 3.1. Artículos cerrados como `verificado` (`Arts. 2, 10, 20 y 22`)

#### Artículo 2o. (`Titulo_Primero/Art_002/00_historia.pdf`)
- **Fechas en el PDF de la SCJN (7 versiones):**
  1. `v1`: `1917-02-05` — `Texto original D.O.F. 05 de febrero de 1917`
  2. `v2`: `2001-08-14` — `Texto derivado de la reforma publicada en el D.O.F. 14 de agosto de 2001`
  3. `v3`: `2015-05-22` — `Texto derivado de la reforma publicada en el D.O.F. 22 de mayo de 2015`
  4. `v4`: `2016-01-29` — `Texto derivado de la reforma publicada en el DOF 29 de enero de 2016`
  5. `v5`: `2019-06-06` — `Texto derivado de la reforma publicada en el DOF 06 de junio de 2019`
  6. `v6`: `2019-08-09` — `Texto derivado de la reforma publicada en el DOF 09 de agosto de 2019`
  7. `v7`: `2024-09-30` — `Texto vigente DOF 30 de septiembre de 2024`
- **Cotejo contra Cámara (`2024-09-30`):** Coincidencia íntegra (`comparable() == True`, 68 párrafos; única diferencia de estilo: `Art. 2o.-` frente a `Artículo 2o.`). Cerrado como `verificado`.

#### Artículo 10 (`Titulo_Primero/Art_010/00_historia.pdf`)
- **Fechas en el PDF de la SCJN (3 versiones):**
  1. `v1`: `1917-02-05` — `Texto original D.O.F. 05 de febrero de 1917`
  2. `v2`: `1971-10-22` — `Texto derivado de la reforma publicada en el D.O.F. 22 de octubre de 1971`
  3. `v3`: `2019-03-26` — `Texto vigente derivado de la reforma publicada en el D.O.F. 26 de marzo de 2019`
- **Cotejo contra Cámara (`2019-03-26`):** Coincidencia íntegra (`comparable() == True`, 1 párrafo; única diferencia de estilo: `Art. 10.-` frente a `Artículo 10.`). Cerrado como `verificado`.

#### Artículo 20 (`Titulo_Primero/Art_020/00_historia.pdf`)
- **Fechas en el PDF de la SCJN (10 versiones):**
  1. `v1`: `1917-02-05` — `Texto original D.O.F. 05 de febrero de 1917` (no rigió por sí solo; corregido por fe de erratas `06-02-1917`)
  2. `v2`: `1917-02-06` — `Texto derivado de la fe de erratas publicada en el D.O.F. 06 de febrero de 1917`
  3. `v3`: `1948-12-02` — `Texto derivado de la reforma publicada en el D.O.F. 02 de diciembre de 1948`
  4. `v4`: `1985-01-14` — `Texto derivado de la reforma publicada en el D.O.F. 14 de enero de 1985`
  5. `v5`: `1993-09-03` — `Texto derivado de la reforma publicada en el D.O.F. 03 de septiembre de 1993`
  6. `v6`: `1996-07-03` — `Texto derivado de la reforma publicada en el D.O.F. 03 de julio de 1996`
  7. `v7`: `2000-09-21` — `Texto derivado de la reforma publicada en el D.O.F. 21 de septiembre de 2000`
  8. `v8`: `2008-06-18` — `Texto derivado de la reforma publicada en el D.O.F. 18 de junio de 2008`
  9. `v9`: `2011-07-14` — `Texto derivado de la reforma publicada en el D.O.F. 14 de julio de 2011`
  10. `v10`: `2024-09-15` — `Texto vigente 15 de septiembre de 2024`
- **Nota sobre la fecha `29-01-2016` en `notas_camara`:** La nota al pie de la Cámara (`Artículo reformado DOF 18-06-2008. Fe de erratas DOF 29-01-2016` / transitorios de la reforma previa al sistema penal acusatorio) corresponde al texto pre-reforma de 2008 que la SCJN conserva en nota de editor (`N. DE E. PARA CONSULTAR LA VERSIÓN CORREGIDA DE ESTE TEXTO ANTERIOR A LA REFORMA DE 18 DE JUNIO DE 2008…`). No constituye una versión posterior al `14-07-2011`.
- **Cotejo contra Cámara (`2024-09-15`):** Coincidencia íntegra (`comparable() == True`, 40 párrafos; única diferencia de estilo: `Art. 20.-` frente a `Artículo 20.`). Cerrado como `verificado`.

#### Artículo 22 (`Titulo_Primero/Art_022/00_historia.pdf`)
- **Fechas en el PDF de la SCJN (8 versiones):**
  1. `v1`: `1917-02-05` — `Texto original D.O.F. 05 de febrero de 1917`
  2. `v2`: `1982-12-28` — `Texto derivado de la reforma publicada en el D.O.F. 28 de diciembre de 1982`
  3. `v3`: `1996-07-03` — `Texto derivado de la reforma publicada en el D.O.F. 03 de julio de 1996`
  4. `v4`: `1999-03-08` — `Texto derivado de la reforma publicada en el D.O.F. 08 de marzo de 1999`
  5. `v5`: `2005-12-09` — `Texto derivado de la reforma publicada en el D.O.F. 09 de diciembre de 2005`
  6. `v6`: `2008-06-18` — `Texto derivado de la reforma publicada en el D.O.F. 18 de junio de 2008`
  7. `v7`: `2015-05-27` — `Texto derivado de la reforma publicada en el D.O.F. 27 de mayo de 2015`
  8. `v8`: `2019-03-14` — `Texto vigente publicado en el D.O.F. 14 de marzo de 2019`
- **Cotejo contra Cámara (`2019-03-14`):** Coincidencia íntegra (`comparable() == True`, 5 párrafos; única diferencia de estilo: `Art. 22.-` frente a `Artículo 22.`). Cerrado como `verificado`.

---

### 3.2. Artículos pendientes de PDF actualizado de la SCJN (`Arts. 82, 116 y 122`)

En estos tres artículos, el archivo `00_historia.pdf` de la SCJN fue generado antes del decreto publicado en el **DOF 07-10-2026** (reforma constitucional en materia de nacionalidad mexicana por nacimiento y prohibición de adquirir o invocar otra nacionalidad para personas titulares de los poderes ejecutivos federal y locales).

#### Artículo 82 (`Titulo_Tercero/Art_082/00_historia.pdf`)
- **Última fecha SCJN (`00_historia.pdf`):** `2025-04-01` (`v11`, `Texto vigente D.O.F. 01 de abril de 2025`).
- **Fecha del texto vigente de la Cámara:** `2026-10-07` (`v12`, `DOF 07-10-2026`).
- **Reformas intermedias faltantes según `notas_camara`:** **Ninguna.** Las 11 versiones del PDF de la SCJN (`1917-02-05`, `1927-01-22`, `1943-01-08`, `1974-10-08`, `1993-08-20`, `1994-07-01`, `2007-06-19`, `2014-02-10`, `2016-01-29`, `2024-09-30` y `2025-04-01`) cubren la totalidad de las reformas previas al `07-10-2026` citadas por la Cámara (`notas_camara` cita además la `Fe de erratas al párrafo primero DOF 06-02-1917`).
- **Fuente exacta del cambio entre `v11` (`01-04-2025`) y `v12` (`07-10-2026`):**
  - Nota de la Cámara en la fracción I: `Fracción reformada DOF 22-01-1927, 01-07-1994, 07-10-2026`.
  - El decreto `DOF 07-10-2026` reforma el primer párrafo de la fracción I y adiciona los párrafos segundo y tercero de dicha fracción (texto íntegro ya cargado en `v12` a partir del consolidado oficial de la Cámara de Diputados). Las fracciones II a VIII son idénticas entre `v11` (SCJN `01-04-2025`) y `v12` (Cámara `07-10-2026`).

#### Artículo 116 (`Titulo_Quinto/Art_116/00_historia.pdf`)
- **Última fecha SCJN (`00_historia.pdf`):** `2026-06-02` (`Texto vigente D.O.F. 02 de junio de 2026`, 22 bloques en el PDF de la SCJN).
- **Fecha del texto vigente de la Cámara:** `2026-10-07` (`DOF 07-10-2026`).
- **Reformas intermedias faltantes según `notas_camara`:** **Ninguna.** Al extraer por coordenadas las 22 versiones del PDF de la SCJN (`1917-02-05` a `2026-06-02`, incluyendo `2007-11-13` y la separación de `2015-05-27` y `2019-12-20`), están presentes todas las reformas previas al `07-10-2026` citadas en `notas_camara`.
- **Fuente exacta del cambio entre la última versión SCJN (`02-06-2026`) y la versión vigente de la Cámara (`07-10-2026`):**
  - Notas de la Cámara en la fracción I: `Párrafo reformado DOF 02-12-2024, 07-10-2026` y `Párrafo adicionado DOF 07-10-2026`.
  - El decreto `DOF 07-10-2026` reforma el quinto párrafo de la fracción I (`Sólo podrá ser gobernador o gobernadora constitucional de un Estado un ciudadano o ciudadana mexicana por nacimiento que no tenga ni adquiera otra nacionalidad…`) y adiciona un sexto párrafo a la fracción I (`Quien ejerza el cargo no podrá adquirir ni solicitar otra nacionalidad…`). Todo el resto del artículo (fracciones II a X) coincide entre la versión SCJN del `02-06-2026` y el texto vigente de la Cámara del `07-10-2026` (salvo el punto y coma final `disposiciones reglamentarias; y` en la fracc. VI).

#### Artículo 122 (`Titulo_Quinto/Art_122/00_historia.pdf`)
- **Última fecha SCJN (`00_historia.pdf`):** `2026-06-02` (`Texto vigente D.O.F. 02 de junio de 2026`, 21 bloques en el PDF de la SCJN).
- **Fecha del texto vigente de la Cámara:** `2026-10-07` (`DOF 07-10-2026`).
- **Reformas intermedias faltantes según `notas_camara`:** **Ninguna.** Al extraer por coordenadas las 21 versiones del PDF de la SCJN (`1917-02-05` a `2026-06-02`, incluyendo la separación de `2012-08-09` y `2013-12-27` y la fecha legible `2020-12-18`), están presentes todas las reformas previas al `07-10-2026` citadas en `notas_camara`.
- **Fuente exacta del cambio entre la última versión SCJN (`02-06-2026`) y la versión vigente de la Cámara (`07-10-2026`):**
  - Notas de la Cámara en el Apartado A, fracción III: `Párrafo reformado DOF 07-10-2026` y `Párrafo adicionado DOF 07-10-2026`.
  - El decreto `DOF 07-10-2026` reforma el segundo párrafo de la fracción III del Apartado A (`La Constitución Política de la Ciudad de México establecerá las facultades del Jefe o Jefa de Gobierno…`) y adiciona un tercer párrafo a dicha fracción (`Quien ejerza el cargo no podrá adquirir ni solicitar otra nacionalidad…`). Todo el resto del artículo coincide íntegramente entre la versión SCJN del `02-06-2026` y el texto vigente de la Cámara del `07-10-2026`.

---

## 4. Conclusión y propuesta sobre los 3 artículos restantes (Arts. 82, 116 y 122)

1. Conforme a la regla 3 del encargo (*«Si el PDF de la SCJN no está actualizado, marca como pendiente de PDF»*), los **Arts. 82, 116 y 122** se mantienen en `"estado": "historial_parcial"` con nota explícita de que su PDF de la SCJN concluye en `01-04-2025` (Art. 82) y `02-06-2026` (Arts. 116 y 122), pendiente de la actualización del PDF de la SCJN para el decreto `DOF 07-10-2026`.
2. **Propuesta de cierre sin inventar texto (regla 4):** Dado que en los tres artículos **no falta ninguna reforma intermedia** entre la última versión del PDF de la SCJN (`01-04-2025` en Art. 82; `02-06-2026` en Arts. 116 y 122) y el decreto vigente (`DOF 07-10-2026`), y que el texto vigente íntegro de la reforma `DOF 07-10-2026` ya está incorporado en `cpeum.json` a partir de la fuente oficial autorizada (consolidado de la Cámara de Diputados, con cita exacta de sus notas de reforma), la serie histórica de los tres artículos está materialmente completa de `1917-02-05` a `2026-10-07`. Si el Coordinador autoriza dar por suficiente el texto consolidado de la Cámara para la versión del `07-10-2026` sin esperar a que la SCJN regenere los tres PDFs con ese último bloque, los Arts. 82, 116 y 122 pueden pasarse directamente a `"estado": "verificado"` sin modificar una sola palabra normativa.
