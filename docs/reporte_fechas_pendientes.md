# Reporte de resolución de 10 fechas pendientes del historial CPEUM por coordenadas de PDF

**Repositorio:** `jatovarv/legislacion-mx-prototipo`  
**Rama:** `fix/fechas-pendientes-coordenadas`  
**Método:** Extracción por coordenadas con `pdfplumber` (`extraer_historia_scjn_pdf.py`), columna izquierda (`x0 < 130`) para el encabezado de versión de la SCJN y columna derecha (`x0 >= 130`) para el texto normativo.

---

## 1. Resumen ejecutivo

Se inspeccionaron los 8 PDFs oficiales «Historia del texto» de la SCJN (`CPEUM_SCJN_Historial/cpeum_scjn.zip`) correspondientes a las **10 versiones** que tenían `fecha_pendiente: true` en `cpeum.json` (`Art. 5 v2`, `Art. 29 v3`, `Art. 41 v15`, `Art. 72 v2`, `Art. 81 v1`, `Art. 89 v6`, `Art. 89 v12`, `Art. 100 v5`, `Art. 115 v14` y `Art. 115 v18`).

En **los 10 casos (10/10)** la fecha de publicación en el DOF es **literalmente legible** en la columna izquierda (`x0 < 130`) del PDF de la SCJN:
- En **9 casos** (`Arts. 5 v2, 29 v3, 41 v15, 72 v2, 89 v6, 89 v12, 100 v5, 115 v14, 115 v18`), el separador lineal original (`separar_versiones_scjn.py`) había perdido la fecha porque la etiqueta de la columna izquierda comenzaba al final de una página (`Texto derivado de la reforma publicada en el D.O.F.`) y la fecha continuaba en las primeras líneas de la columna izquierda de la página siguiente, quedando intercalada con el texto normativo de la columna derecha en la lectura lineal de PyMuPDF. Al aislar la columna izquierda (`x0 < 130`) con `pdfplumber`, las palabras del encabezado y la fecha se leen de forma continua e inequívoca.
- En **1 caso** (`Art. 81 v1`), el encabezado completo está en la misma página (pág. 1), pero con la grafía atípica `Texto vigente D.O.F el 20 de diciembre de 2019` (sin tercer punto en `D.O.F` y con el artículo `el` antes de la fecha), que no coincidía con la expresión regular del separador lineal pero sí es leída íntegramente por `extraer_historia_scjn_pdf.py`.

Con estas 10 fechas fijadas con evidencia documental de página y coordenadas, quedan **0 versiones con `fecha_pendiente: true` o `publicacion: null`** y **0 versiones con `vigencia_hasta_indeterminada: true`** en los 136 artículos de `cpeum.json`.

| # | Artículo | Versión | Fecha fijada (`publicacion`) | Vigencia (`vigencia_desde` → `vigencia_hasta`) | PDF SCJN (`cpeum_scjn.zip`) | Página(s) | Coordenadas inicio encabezado (`x0, top`) | Coordenadas fecha (`x0, top`) | Primeras palabras del texto siguiente (`x0 >= 130`) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Art. 5** | `v2` | `1942-11-17` | `1942-11-18` → `1974-12-31` | `Titulo_Primero/Art_005/00_historia.pdf` | Págs. 1–2 | Pág. 1: `(50.76, 637.58)` | Pág. 2: `(77.16, 137.78)` a `(78.60, 162.14)` | `Art. 5o.- Nadie podrá ser obligado a prestar trabajos personales` |
| 2 | **Art. 29** | `v3` | `2007-08-02` | `2007-08-03` → `2011-06-10` | `Titulo_Primero/Art_029/00_historia.pdf` | Págs. 1–2 | Pág. 1: `(45.40, 641.23)` | Pág. 1: `(42.60, 689.83)` / Pág. 2: `(73.20, 137.83)` | `(REFORMADO, D.O.F. 2 DE AGOSTO DE 2007) Art. 29.- En los casos de invasión,` |
| 3 | **Art. 41** | `v15` | `2024-11-15` | `2024-11-16` → `2024-12-20` | `Titulo_Segundo/Art_041/00_historia.pdf` | Págs. 86–87 | Pág. 86: `(38.64, 666.98)` | Pág. 86: `(65.04, 715.70)` / Pág. 87: `(42.36, 115.10)` | `(REFORMADO PRIMER PÁRRAFO, D.O.F. 10 DE FEBRERO DE 2014) Art. 41.- El pueblo ejerce su soberanía` |
| 4 | **Art. 72** | `v2` | `1923-11-24` | `1923-11-25` → `2011-08-17` | `Titulo_Tercero/Art_072/00_historia.pdf` | Págs. 2–3 | Pág. 2: `(50.76, 627.74)` | Pág. 3: `(77.16, 137.78)` a `(78.60, 162.14)` | `Art. 72.- Todo proyecto de ley o decreto, cuya resolución` |
| 5 | **Art. 81** | `v1` | `2019-12-20` | `2019-12-21` → `null` (vigente) | `Titulo_Tercero/Art_081/00_historia.pdf` | Pág. 1 | Pág. 1: `(54.36, 289.58)` | Pág. 1: `(100.91, 301.70)` a `(78.60, 326.06)` | `(REFORMADO, D.O.F. 20 DE DICIEMBRE DE 2019) Art. 81.- La elección del presidente será directa` |
| 6 | **Art. 89** | `v6` | `1966-10-21` | `1966-10-22` → `1974-10-08` | `Titulo_Tercero/Art_089/00_historia.pdf` | Págs. 8–9 | Pág. 8: `(50.76, 636.14)` | Pág. 9: `(54.00, 137.78)` a `(87.00, 150.02)` | `Art. 89.- Las facultades y obligaciones del Presidente son las` |
| 7 | **Art. 89** | `v12` | `1994-12-31` | `1995-01-01` → `2004-04-05` | `Titulo_Tercero/Art_089/00_historia.pdf` | Págs. 19–20 | Pág. 19: `(50.76, 636.14)` | Pág. 20: `(47.76, 137.78)` a `(87.00, 150.02)` | `(REFORMADO PRIMER PÁRRAFO, D.O.F. 10 DE AGOSTO DE 1987) Art. 89.- Las facultades y obligaciones del Presidente,` |
| 8 | **Art. 100** | `v5` | `1994-12-31` | `1995-01-01` → `1999-06-11` | `Titulo_Tercero/Art_100/00_historia.pdf` | Págs. 1–2 | Pág. 1: `(50.76, 633.98)` | Pág. 2: `(47.76, 137.78)` a `(87.00, 150.02)` | `(REFORMADO, D.O.F. 31 DE DICIEMBRE DE 1994) Art. 100.- La administración, vigilancia y disciplina` |
| 9 | **Art. 115** | `v14` | `2009-08-24` | `2009-08-25` → `2014-02-10` | `Titulo_Quinto/Art_115/00_historia.pdf` | Págs. 38–39 | Pág. 38: `(45.60, 646.94)` | Pág. 38: `(51.36, 702.86)` / Pág. 39: `(65.04, 115.10)` | `(REFORMADO, D.O.F. 3 DE FEBRERO DE 1983) Art. 115.- Los Estados adoptarán, para su régimen interior,` |
| 10 | **Art. 115** | `v18` | `2020-12-18` | `2020-12-19` → `2025-04-01` | `Titulo_Quinto/Art_115/00_historia.pdf` | Págs. 62–63 | Pág. 62: `(45.60, 645.74)` | Pág. 62: `(72.00, 701.66)` / Pág. 63: `(51.48, 115.10)` | `(REFORMADO PRIMER PÁRRAFO, D.O.F. 10 DE FEBRERO DE 2014) Art. 115.- Los estados adoptarán, para su régimen interior,` |

---

## 2. Evidencia detallada por versión (página, coordenadas y `pdfplumber`)

### 2.1. Artículo 5 — `v2` (`1942-11-17`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Primero/Art_005/00_historia.pdf`
- **Páginas:** 1 y 2 (de 10)
- **Fecha fijada:** `publicacion: "1942-11-17"` (`etiqueta: "Reforma DOF 17-11-1942"`)
- **Encadenamiento de vigencia:**
  - `v1` (`1917-02-05`): `vigencia_desde: "1917-05-01"`, `vigencia_hasta: "1942-11-17"`
  - `v2` (`1942-11-17`): `vigencia_desde: "1942-11-18"`, `vigencia_hasta: "1974-12-31"` (la `v3` se publicó el `1974-12-31` y entró en vigor el `1975-01-01`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 17 de noviembre de 1942",
    "tipo": "reforma",
    "publicacion": "1942-11-17",
    "page": 1,
    "top": 637.57788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 1:** `('Texto', x0=50.76, top=637.58, x1=81.62, bottom=648.98)`, `('derivado', x0=85.68, top=637.58, x1=127.18, bottom=648.98)`, `('de', x0=55.08, top=649.70, x1=68.02, bottom=661.10)`, `('la', x0=72.12, top=649.70, x1=81.46, bottom=661.10)`, `('reforma', x0=85.56, top=649.70, x1=122.94, bottom=661.10)`, `('publicada', x0=50.40, top=661.82, x1=100.38, bottom=673.22)`, `('en', x0=107.88, top=661.82, x1=120.82, bottom=673.22)`, `('el', x0=125.16, top=661.82, x1=127.60, bottom=673.22)`, `('D.O.F.', x0=75.72, top=674.06, x1=102.24, bottom=685.46)`
  - **Pág. 2:** `('17', x0=77.16, top=137.78, x1=90.34, bottom=149.18)`, `('de', x0=94.68, top=137.78, x1=107.62, bottom=149.18)`, `('noviembre', x0=54.48, top=150.02, x1=113.38, bottom=161.42)`, `('de', x0=117.61, top=150.02, x1=127.61, bottom=161.42)`, `('1942', x0=78.60, top=162.14, x1=103.52, bottom=173.54)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 1 (`top=637.58`):** `('Art.', 150.24, 637.58)`, `('5o.-', 177.24, 637.58)`, `('Nadie', 205.92, 637.58)`, `('podrá', 240.48, 637.58)`, `('ser', 275.76, 637.58)`, `('obligado', 297.48, 637.58)`, `('a', 345.96, 637.58)`, `('prestar', 358.32, 637.58)`, `('trabajos', 400.44, 637.58)`, `('personales', 447.85, 637.58)`
  - **Coincidencia con `cpeum.json` (`Art. 5 v2`):** `"Art. 5o.- Nadie podrá ser obligado a prestar trabajos personales sin la justa retribución y sin su pleno consentimiento..."` (exacto).

---

### 2.2. Artículo 29 — `v3` (`2007-08-02`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Primero/Art_029/00_historia.pdf`
- **Páginas:** 1 y 2 (de 4)
- **Fecha fijada:** `publicacion: "2007-08-02"` (`etiqueta: "Reforma DOF 02-08-2007"`)
- **Encadenamiento de vigencia:**
  - `v2` (`1981-04-21`): `vigencia_desde: "1981-04-22"`, `vigencia_hasta: "2007-08-02"`
  - `v3` (`2007-08-02`): `vigencia_desde: "2007-08-03"`, `vigencia_hasta: "2011-06-10"` (la `v4` se publicó el `2011-06-10` y entró en vigor el `2011-06-11`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 02 de agosto de 2007",
    "tipo": "reforma",
    "publicacion": "2007-08-02",
    "page": 1,
    "top": 641.23
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 1:** `('Texto', x0=45.40, top=641.23, x1=76.22, bottom=652.63)`, `('derivado', x0=80.20, top=641.23, x1=121.66, bottom=652.63)`, `('de', x0=49.60, top=653.43, x1=62.50, bottom=664.83)`, `('la', x0=66.60, top=653.43, x1=75.90, bottom=664.83)`, `('reforma', x0=80.00, top=653.43, x1=117.33, bottom=664.83)`, `('publicada', x0=45.00, top=665.63, x1=94.88, bottom=677.03)`, `('en', x0=102.40, top=665.63, x1=115.30, bottom=677.03)`, `('el', x0=119.60, top=665.63, x1=122.00, bottom=677.03)`, `('D.O.F.', x0=70.20, top=677.83, x1=96.67, bottom=689.23)`, `('02', x0=42.60, top=689.83, x1=55.99, bottom=701.23)`, `('de', x0=60.40, top=689.83, x1=73.30, bottom=701.23)`, `('agosto', x0=77.40, top=689.83, x1=114.23, bottom=701.23)`, `('de', x0=118.60, top=689.83, x1=122.20, bottom=701.23)`
  - **Pág. 2:** `('2007', x0=73.20, top=137.83, x1=98.37, bottom=149.23)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 1 (`top=641.23–653.43`):** `('(REFORMADO,', 144.80, 641.23)`, `('D.O.F.', 221.20, 641.23)`, `('2', 257.00, 641.23)`, `('DE', 267.00, 641.23)`, `('AGOSTO', 284.60, 641.23)`, `('DE', 331.40, 641.23)`, `('2007)', 348.80, 641.23)`, `('Art.', 144.80, 653.43)`, `('29.-', 171.00, 653.43)`, `('En', 199.20, 653.43)`, `('los', 217.20, 653.43)`, `('casos', 236.60, 653.43)`, `('de', 269.60, 653.43)`, `('invasión,', 287.20, 653.43)`
  - **Coincidencia con `cpeum.json` (`Art. 29 v3`):** `"Art. 29.- En los casos de invasión, perturbación grave de la paz pública, o de cualquier otro que ponga a la sociedad en grave peligro o conflicto..."` (exacto).

---

### 2.3. Artículo 41 — `v15` (`2024-11-15`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Segundo/Art_041/00_historia.pdf`
- **Páginas:** 86 y 87 (de 115)
- **Fecha fijada:** `publicacion: "2024-11-15"` (`etiqueta: "Reforma DOF 15-11-2024"`)
- **Encadenamiento de vigencia:**
  - `v14` (`2019-12-20`): `vigencia_desde: "2019-12-21"`, `vigencia_hasta: "2024-11-15"`
  - `v15` (`2024-11-15`): `vigencia_desde: "2024-11-16"`, `vigencia_hasta: "2024-12-20"` (la `v16` se publicó el `2024-12-20` y entró en vigor el `2024-12-21`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 15 de noviembre de 2024",
    "tipo": "reforma",
    "publicacion": "2024-11-15",
    "page": 86,
    "top": 666.97788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 86:** `('Texto', x0=38.64, top=666.98, x1=69.50, bottom=678.38)`, `('derivado', x0=73.56, top=666.98, x1=115.06, bottom=678.38)`, `('de', x0=42.96, top=679.22, x1=55.90, bottom=690.62)`, `('la', x0=60.00, top=679.22, x1=69.34, bottom=690.62)`, `('reforma', x0=73.44, top=679.22, x1=110.82, bottom=690.62)`, `('publicada', x0=38.28, top=691.34, x1=88.26, bottom=702.74)`, `('en', x0=95.76, top=691.34, x1=108.70, bottom=702.74)`, `('el', x0=113.04, top=691.34, x1=115.48, bottom=702.74)`, `('D.O.F.', x0=63.60, top=703.46, x1=90.12, bottom=714.86)`, `('15', x0=65.04, top=715.70, x1=78.22, bottom=727.10)`, `('de', x0=82.56, top=715.70, x1=95.50, bottom=727.10)`
  - **Pág. 87:** `('noviembre', x0=42.36, top=115.10, x1=101.26, bottom=126.50)`, `('de', x0=105.49, top=115.10, x1=115.49, bottom=126.50)`, `('2024', x0=66.48, top=127.34, x1=91.40, bottom=138.74)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 86 (`top=666.62–678.86`):** `('(REFORMADO', 141.72, 666.62)`, `('PRIMER', 214.08, 666.62)`, `('PÁRRAFO,', 256.80, 666.62)`, `('D.O.F.', 312.60, 666.62)`, `('10', 345.36, 666.62)`, `('DE', 360.84, 666.62)`, `('FEBRERO', 377.76, 666.62)`, `('DE', 428.88, 666.62)`, `('2014)', 445.68, 666.62)`, `('Art.', 141.72, 678.86)`, `('41.-', 165.72, 678.86)`, `('El', 191.52, 678.86)`, `('pueblo', 203.88, 678.86)`, `('ejerce', 240.60, 678.86)`, `('su', 274.56, 678.86)`, `('soberanía', 289.32, 678.86)`
  - **Coincidencia con `cpeum.json` (`Art. 41 v15`):** `"Art. 41.- El pueblo ejerce su soberanía por medio de los Poderes de la Unión..."` (exacto).

---

### 2.4. Artículo 72 — `v2` (`1923-11-24`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Tercero/Art_072/00_historia.pdf`
- **Páginas:** 2 y 3 (de 6)
- **Fecha fijada:** `publicacion: "1923-11-24"` (`etiqueta: "Reforma DOF 24-11-1923"`)
- **Encadenamiento de vigencia:**
  - `v1` (`1917-02-05`): `vigencia_desde: "1917-05-01"`, `vigencia_hasta: "1923-11-24"`
  - `v2` (`1923-11-24`): `vigencia_desde: "1923-11-25"`, `vigencia_hasta: "2011-08-17"` (la `v3` se publicó el `2011-08-17` y entró en vigor el `2011-08-18`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 24 de noviembre de 1923",
    "tipo": "reforma",
    "publicacion": "1923-11-24",
    "page": 2,
    "top": 627.73788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 2:** `('Texto', x0=50.76, top=627.74, x1=81.62, bottom=639.14)`, `('derivado', x0=85.68, top=627.74, x1=127.18, bottom=639.14)`, `('de', x0=55.08, top=639.86, x1=68.02, bottom=651.26)`, `('la', x0=72.12, top=639.86, x1=81.46, bottom=651.26)`, `('reforma', x0=85.56, top=639.86, x1=122.94, bottom=651.26)`, `('publicada', x0=50.40, top=651.98, x1=100.38, bottom=663.38)`, `('en', x0=107.88, top=651.98, x1=120.82, bottom=663.38)`, `('el', x0=125.16, top=651.98, x1=127.60, bottom=663.38)`, `('D.O.F.', x0=75.72, top=664.10, x1=102.24, bottom=675.50)`
  - **Pág. 3:** `('24', x0=77.16, top=137.78, x1=90.34, bottom=149.18)`, `('de', x0=94.68, top=137.78, x1=107.62, bottom=149.18)`, `('noviembre', x0=54.48, top=150.02, x1=113.38, bottom=161.42)`, `('de', x0=117.61, top=150.02, x1=127.61, bottom=161.42)`, `('1923', x0=78.60, top=162.14, x1=103.52, bottom=173.54)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 2 (`top=627.74`):** `('Art.', 150.24, 627.74)`, `('72.-', 176.27, 627.74)`, `('Todo', 204.36, 627.74)`, `('proyecto', 234.36, 627.74)`, `('de', 283.44, 627.74)`, `('ley', 301.08, 627.74)`, `('o', 321.12, 627.74)`, `('decreto,', 332.64, 627.74)`, `('cuya', 380.16, 627.74)`, `('resolución', 409.56, 627.74)`
  - **Coincidencia con `cpeum.json` (`Art. 72 v2`):** `"Art. 72.- Todo proyecto de ley o decreto, cuya resolución no sea exclusiva de alguna de las Cámaras..."` (exacto).

---

### 2.5. Artículo 81 — `v1` (`2019-12-20`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Tercero/Art_081/00_historia.pdf`
- **Página:** 1 (de 1)
- **Fecha fijada:** `publicacion: "2019-12-20"` (`etiqueta: "Vigente (post 20-12-2019)"`)
- **Encadenamiento de vigencia:**
  - `v1` (`2019-12-20`): `vigencia_desde: "2019-12-21"`, `vigencia_hasta: null` (única versión registrada en `cpeum.json`, vigente).
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto vigente D.O.F el 20 de diciembre de 2019",
    "tipo": "vigente",
    "publicacion": "2019-12-20",
    "page": 1,
    "top": 289.57788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 1 (`top=289.58–326.06`):** `('Texto', x0=54.36, top=289.58, x1=85.22, bottom=300.98)`, `('vigente', x0=89.28, top=289.58, x1=123.60, bottom=300.98)`, `('D.O.F', x0=53.52, top=301.70, x1=79.56, bottom=313.10)`, `('el', x0=87.35, top=301.70, x1=96.59, bottom=313.10)`, `('20', x0=100.91, top=301.70, x1=114.09, bottom=313.10)`, `('de', x0=118.56, top=301.70, x1=127.58, bottom=313.10)`, `('diciembre', x0=56.52, top=313.82, x1=111.12, bottom=325.22)`, `('de', x0=115.43, top=313.82, x1=127.60, bottom=325.22)`, `('2019', x0=78.60, top=326.06, x1=103.52, bottom=337.46)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 1 (`top=289.58–301.70`):** `('(REFORMADO,', 150.24, 289.58)`, `('D.O.F.', 226.44, 289.58)`, `('20', 262.32, 289.58)`, `('DE', 278.76, 289.58)`, `('DICIEMBRE', 296.40, 289.58)`, `('DE', 359.75, 289.58)`, `('2019)', 377.15, 289.58)`, `('Art.', 150.24, 301.70)`, `('81.-', 174.60, 301.70)`, `('La', 200.88, 301.70)`, `('elección', 216.12, 301.70)`, `('del', 259.92, 301.70)`, `('presidente', 278.52, 301.70)`, `('será', 334.93, 301.70)`, `('directa', 360.01, 301.70)`
  - **Coincidencia con `cpeum.json` (`Art. 81 v1`):** `"Art. 81.- La elección del presidente será directa y en los términos que disponga la ley electoral..."` (exacto).
- **Observación documental sobre el PDF del Art. 81:** En la misma pág. 1 (`top=225.50`) existe un primer bloque con encabezado `Texto original 05 de febrero de 1917` (sin `D.O.F.`), que el separador lineal original omitió. Conforme a la restricción expresa de esta tarea (*«PROHIBIDO: Modificar texto normativo, crear o eliminar versiones»*), no se crea una nueva versión en este PR y se deja constancia para un eventual alta posterior del texto original de 1917.

---

### 2.6. Artículo 89 — `v6` (`1966-10-21`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Tercero/Art_089/00_historia.pdf`
- **Páginas:** 8 y 9 (de 38)
- **Fecha fijada:** `publicacion: "1966-10-21"` (`etiqueta: "Reforma DOF 21-10-1966"`)
- **Encadenamiento de vigencia:**
  - `v5` (`1966-10-21`): `vigencia_desde: "1966-10-22"`, `vigencia_hasta: "1966-10-22"` (`Texto intermedio: el siguiente decreto entró en vigor el mismo día.`)
  - `v6` (`1966-10-21`): `vigencia_desde: "1966-10-22"`, `vigencia_hasta: "1974-10-08"` (la `v7` se publicó el `1974-10-08` y entró en vigor el `1974-10-09`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 21 de octubre de 1966",
    "tipo": "reforma",
    "publicacion": "1966-10-21",
    "page": 8,
    "top": 636.13788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 8:** `('Texto', x0=50.76, top=636.14, x1=81.62, bottom=647.54)`, `('derivado', x0=85.68, top=636.14, x1=127.18, bottom=647.54)`, `('de', x0=55.08, top=648.26, x1=68.02, bottom=659.66)`, `('la', x0=72.12, top=648.26, x1=81.46, bottom=659.66)`, `('reforma', x0=85.56, top=648.26, x1=122.94, bottom=659.66)`, `('publicada', x0=50.40, top=660.38, x1=100.38, bottom=671.78)`, `('en', x0=107.88, top=660.38, x1=120.82, bottom=671.78)`, `('el', x0=125.16, top=660.38, x1=127.60, bottom=671.78)`, `('D.O.F.', x0=75.72, top=672.62, x1=102.24, bottom=684.02)`
  - **Pág. 9:** `('21', x0=54.00, top=137.78, x1=67.18, bottom=149.18)`, `('de', x0=71.52, top=137.78, x1=84.46, bottom=149.18)`, `('octubre', x0=88.56, top=137.78, x1=127.61, bottom=149.18)`, `('de', x0=70.08, top=150.02, x1=83.02, bottom=161.42)`, `('1966', x0=87.00, top=150.02, x1=111.92, bottom=161.42)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 8 (`top=636.14`):** `('Art.', 150.24, 636.14)`, `('89.-', 174.48, 636.14)`, `('Las', 200.64, 636.14)`, `('facultades', 220.92, 636.14)`, `('y', 275.63, 636.14)`, `('obligaciones', 285.11, 636.14)`, `('del', 350.02, 636.14)`, `('Presidente', 368.50, 636.14)`, `('son', 425.74, 636.14)`, `('las', 447.34, 636.14)`
  - **Coincidencia con `cpeum.json` (`Art. 89 v6`):** `"Art. 89.- Las facultades y obligaciones del Presidente son las siguientes:..."` (exacto).
- **Observación documental sobre `v5` y `v6` del Art. 89:** El PDF oficial de la SCJN incluye dos bloques consecutivos con el mismo encabezado `Texto derivado de la reforma publicada en el D.O.F. 21 de octubre de 1966` (`v5` en pág. 7 `top=163.90` y `v6` en págs. 8–9 `top=636.14`). Por ello `integrar_historial_scjn.py`, que buscaba candidatas con desigualdad estricta `c > prev`, dejó `fecha_sugerida: null`. Conforme a las reglas de integridad del esquema (`x_reglas_integridad`: *«No usar publicacion como identificador único: puede haber más de un evento el mismo día. No deduplicar versiones sólo porque el texto coincida»*) y a la prohibición de eliminar versiones, se conservan ambas versiones con la fecha literal del PDF (`1966-10-21`) y sus vigencias encadenadas.

---

### 2.7. Artículo 89 — `v12` (`1994-12-31`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Tercero/Art_089/00_historia.pdf`
- **Páginas:** 19 y 20 (de 38)
- **Fecha fijada:** `publicacion: "1994-12-31"` (`etiqueta: "Reforma DOF 31-12-1994"`)
- **Encadenamiento de vigencia:**
  - `v11` (`1993-10-25`): `vigencia_desde: "1993-10-26"`, `vigencia_hasta: "1994-12-31"`
  - `v12` (`1994-12-31`): `vigencia_desde: "1995-01-01"`, `vigencia_hasta: "2004-04-05"` (la `v13` se publicó el `2004-04-05` y entró en vigor el `2004-04-06`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 31 de diciembre de 1994",
    "tipo": "reforma",
    "publicacion": "1994-12-31",
    "page": 19,
    "top": 636.13788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 19:** `('Texto', x0=50.76, top=636.14, x1=81.62, bottom=647.54)`, `('derivado', x0=85.68, top=636.14, x1=127.18, bottom=647.54)`, `('de', x0=55.08, top=648.26, x1=68.02, bottom=659.66)`, `('la', x0=72.12, top=648.26, x1=81.46, bottom=659.66)`, `('reforma', x0=85.56, top=648.26, x1=122.94, bottom=659.66)`, `('publicada', x0=50.40, top=660.38, x1=100.38, bottom=671.78)`, `('en', x0=107.88, top=660.38, x1=120.82, bottom=671.78)`, `('el', x0=125.16, top=660.38, x1=127.60, bottom=671.78)`, `('D.O.F.', x0=75.72, top=672.62, x1=102.24, bottom=684.02)`
  - **Pág. 20:** `('31', x0=47.76, top=137.78, x1=60.94, bottom=149.18)`, `('de', x0=65.28, top=137.78, x1=78.22, bottom=149.18)`, `('diciembre', x0=82.32, top=137.78, x1=127.60, bottom=149.18)`, `('de', x0=70.08, top=150.02, x1=83.02, bottom=161.42)`, `('1994', x0=87.00, top=150.02, x1=111.92, bottom=161.42)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 19 (`top=636.14–648.26`):** `('(REFORMADO', 150.24, 636.14)`, `('PRIMER', 222.84, 636.14)`, `('PÁRRAFO,', 265.80, 636.14)`, `('D.O.F.', 321.95, 636.14)`, `('10', 355.07, 636.14)`, `('DE', 370.79, 636.14)`, `('AGOSTO', 387.95, 636.14)`, `('DE', 434.03, 636.14)`, `('1987)', 451.07, 636.14)`, `('Art.', 150.24, 648.26)`, `('89.-', 174.48, 648.26)`, `('Las', 200.64, 648.26)`, `('facultades', 220.92, 648.26)`, `('y', 275.63, 648.26)`, `('obligaciones', 285.11, 648.26)`, `('del', 350.03, 648.26)`, `('Presidente,', 368.51, 648.26)`
  - **Coincidencia con `cpeum.json` (`Art. 89 v12`):** `"Art. 89.- Las facultades y obligaciones del Presidente, son las siguientes:..."` (exacto).

---

### 2.8. Artículo 100 — `v5` (`1994-12-31`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Tercero/Art_100/00_historia.pdf`
- **Páginas:** 1 y 2 (de 13)
- **Fecha fijada:** `publicacion: "1994-12-31"` (`etiqueta: "Reforma DOF 31-12-1994"`)
- **Encadenamiento de vigencia:**
  - `v4` (`1993-09-03`): `vigencia_desde: "1993-09-04"`, `vigencia_hasta: "1994-12-31"`
  - `v5` (`1994-12-31`): `vigencia_desde: "1995-01-01"`, `vigencia_hasta: "1999-06-11"` (la `v6` se publicó el `1999-06-11` y entró en vigor el `1999-06-12`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 31 de diciembre de 1994",
    "tipo": "reforma",
    "publicacion": "1994-12-31",
    "page": 1,
    "top": 633.97788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 1:** `('Texto', x0=50.76, top=633.98, x1=81.62, bottom=645.38)`, `('derivado', x0=85.68, top=633.98, x1=127.18, bottom=645.38)`, `('de', x0=55.08, top=646.10, x1=68.02, bottom=657.50)`, `('la', x0=72.12, top=646.10, x1=81.46, bottom=657.50)`, `('reforma', x0=85.56, top=646.10, x1=122.94, bottom=657.50)`, `('publicada', x0=50.40, top=658.22, x1=100.38, bottom=669.62)`, `('en', x0=107.88, top=658.22, x1=120.82, bottom=669.62)`, `('el', x0=125.16, top=658.22, x1=127.60, bottom=669.62)`, `('D.O.F.', x0=75.72, top=670.46, x1=102.24, bottom=681.86)`
  - **Pág. 2:** `('31', x0=47.76, top=137.78, x1=60.94, bottom=149.18)`, `('de', x0=65.28, top=137.78, x1=78.22, bottom=149.18)`, `('diciembre', x0=82.32, top=137.78, x1=127.60, bottom=149.18)`, `('de', x0=70.08, top=150.02, x1=83.02, bottom=161.42)`, `('1994', x0=87.00, top=150.02, x1=111.92, bottom=161.42)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 1 (`top=633.98–647.90`):** `('(REFORMADO,', 150.24, 633.98)`, `('D.O.F.', 226.44, 633.98)`, `('31', 262.32, 633.98)`, `('DE', 278.76, 633.98)`, `('DICIEMBRE', 296.40, 633.98)`, `('DE', 359.75, 633.98)`, `('1994)', 377.15, 633.98)`, `('Art.', 150.24, 647.90)`, `('100.-', 178.08, 647.90)`, `('La', 215.16, 647.90)`, `('administración,', 233.88, 647.90)`, `('vigilancia', 318.35, 647.90)`, `('y', 372.23, 647.90)`, `('disciplina', 385.31, 647.90)`
  - **Coincidencia con `cpeum.json` (`Art. 100 v5`):** `"Art. 100.- La administración, vigilancia y disciplina del Poder Judicial de la Federación, con excepción de la Suprema Corte de Justicia de la Nación, estarán a cargo del Consejo de la Judicatura Federal..."` (exacto).

---

### 2.9. Artículo 115 — `v14` (`2009-08-24`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Quinto/Art_115/00_historia.pdf`
- **Páginas:** 38 y 39 (de 76)
- **Fecha fijada:** `publicacion: "2009-08-24"` (`etiqueta: "Reforma DOF 24-08-2009"`)
- **Encadenamiento de vigencia:**
  - `v13` (`2008-06-18`): `vigencia_desde: "2008-06-19"`, `vigencia_hasta: "2009-08-24"`
  - `v14` (`2009-08-24`): `vigencia_desde: "2009-08-25"`, `vigencia_hasta: "2014-02-10"` (la `v15` se publicó el `2014-02-10` y entró en vigor el `2014-02-11`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 24 de agosto de 2009",
    "tipo": "reforma",
    "publicacion": "2009-08-24",
    "page": 38,
    "top": 646.93788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 38:** `('Texto', x0=45.60, top=646.94, x1=76.46, bottom=658.34)`, `('derivado', x0=80.52, top=646.94, x1=122.02, bottom=658.34)`, `('de', x0=50.04, top=660.86, x1=62.98, bottom=672.26)`, `('la', x0=67.08, top=660.86, x1=76.42, bottom=672.26)`, `('reforma', x0=80.52, top=660.86, x1=117.90, bottom=672.26)`, `('publicada', x0=45.36, top=674.90, x1=95.34, bottom=686.30)`, `('en', x0=102.84, top=674.90, x1=115.78, bottom=686.30)`, `('el', x0=120.12, top=674.90, x1=122.56, bottom=686.30)`, `('D.O.F.', x0=70.68, top=688.82, x1=97.20, bottom=700.22)`, `('24', x0=51.36, top=702.86, x1=64.54, bottom=714.26)`, `('de', x0=68.88, top=702.86, x1=81.82, bottom=714.26)`, `('agosto', x0=86.04, top=702.86, x1=122.57, bottom=714.26)`
  - **Pág. 39:** `('de', x0=65.04, top=115.10, x1=77.98, bottom=126.50)`, `('2009', x0=81.96, top=115.10, x1=106.88, bottom=126.50)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 38 (`top=648.74–663.26`):** `('(REFORMADO,', 145.20, 648.74)`, `('D.O.F.', 221.40, 648.74)`, `('3', 257.28, 648.74)`, `('DE', 267.12, 648.74)`, `('FEBRERO', 284.76, 648.74)`, `('DE', 337.91, 648.74)`, `('1983)', 355.31, 648.74)`, `('Art.', 145.20, 663.26)`, `('115.-', 169.92, 663.26)`, `('Los', 203.65, 663.26)`, `('Estados', 224.41, 663.26)`, `('adoptarán,', 267.49, 663.26)`, `('para', 325.09, 663.26)`, `('su', 350.65, 663.26)`, `('régimen', 366.13, 663.26)`, `('interior,', 409.57, 663.26)`
  - **Coincidencia con `cpeum.json` (`Art. 115 v14`):** `"Art. 115.- Los Estados adoptarán, para su régimen interior, la forma de gobierno republicano, representativo, popular..."` (exacto).

---

### 2.10. Artículo 115 — `v18` (`2020-12-18`)
- **PDF:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Quinto/Art_115/00_historia.pdf`
- **Páginas:** 62 y 63 (de 76)
- **Fecha fijada:** `publicacion: "2020-12-18"` (`etiqueta: "Reforma DOF 18-12-2020"`)
- **Encadenamiento de vigencia:**
  - `v17` (`2019-06-06`): `vigencia_desde: "2019-06-07"`, `vigencia_hasta: "2020-12-18"`
  - `v18` (`2020-12-18`): `vigencia_desde: "2020-12-19"`, `vigencia_hasta: "2025-04-01"` (la `v19` se publicó el `2025-04-01` y entró en vigor el `2025-04-02`)
- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 18 de diciembre de 2020",
    "tipo": "reforma",
    "publicacion": "2020-12-18",
    "page": 62,
    "top": 645.73788
  }
  ```
- **Palabras y coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **Pág. 62:** `('Texto', x0=45.60, top=645.74, x1=76.46, bottom=657.14)`, `('derivado', x0=80.52, top=645.74, x1=122.02, bottom=657.14)`, `('de', x0=50.04, top=659.66, x1=62.98, bottom=671.06)`, `('la', x0=67.08, top=659.66, x1=76.42, bottom=671.06)`, `('reforma', x0=80.52, top=659.66, x1=117.90, bottom=671.06)`, `('publicada', x0=45.36, top=673.70, x1=95.34, bottom=685.10)`, `('en', x0=102.84, top=673.70, x1=115.78, bottom=685.10)`, `('el', x0=120.12, top=673.70, x1=122.56, bottom=685.10)`, `('D.O.F.', x0=70.68, top=687.62, x1=97.20, bottom=699.02)`, `('18', x0=72.00, top=701.66, x1=85.18, bottom=713.06)`, `('de', x0=89.52, top=701.66, x1=102.46, bottom=713.06)`
  - **Pág. 63:** `('diciembre', x0=51.48, top=115.10, x1=106.08, bottom=126.50)`, `('de', x0=110.41, top=115.10, x1=122.58, bottom=126.50)`, `('2020', x0=73.56, top=129.14, x1=98.48, bottom=140.54)`
- **Primeras palabras del texto siguiente en columna derecha (`x0 >= 130`):**
  - **Pág. 62 (`top=647.54–662.06`):** `('(REFORMADO', 145.20, 647.54)`, `('PRIMER', 217.56, 647.54)`, `('PÁRRAFO,', 260.28, 647.54)`, `('D.O.F.', 316.08, 647.54)`, `('10', 348.84, 647.54)`, `('DE', 364.32, 647.54)`, `('FEBRERO', 381.24, 647.54)`, `('DE', 432.36, 647.54)`, `('2014)', 449.16, 647.54)`, `('Art.', 145.20, 662.06)`, `('115.-', 169.92, 662.06)`, `('Los', 203.65, 662.06)`, `('estados', 224.53, 662.06)`, `('adoptarán,', 267.25, 662.06)`, `('para', 324.85, 662.06)`, `('su', 350.41, 662.06)`, `('régimen', 365.89, 662.06)`, `('interior,', 409.33, 662.06)`
  - **Coincidencia con `cpeum.json` (`Art. 115 v18`):** `"Art. 115.- Los estados adoptarán, para su régimen interior, la forma de gobierno republicano, representativo, democrático, laico y popular..."` (exacto).

---

## 3. Verificación de criterios de aceptación

1. **Diff solo de fechas y metadatos:** Comprobado (`git diff -U0 cpeum.json`); ningún campo `texto` fue modificado y no se creó ni eliminó ninguna versión.
2. **Cada fecha fijada tiene evidencia de página y coordenadas:** Documentado en las secciones 1 y 2 para las 10 versiones.
3. **Un solo vigente por artículo, vigencias encadenadas:** En los 136 artículos de `cpeum.json`, únicamente la última versión (`versiones[-1]`) tiene `vigencia_hasta: null` y todas las vigencias están encadenadas sin huecos.
4. **Golden cases intactos:** `cpeum-art-1.json` y `cpeum-art-4.json` coinciden byte a byte con `cpeum.json['articulos']['1']` y `cpeum.json['articulos']['4']`.
5. **Esquema válido 136/136:** Los 136 artículos validan sin errores contra `docs/cpeum-articulo-historial.schema.json` (Draft 2020-12).
6. **`build.py` reproducible:** `historial/N.json`, `articulos/N.html` de los 8 artículos afectados e `index.html` regenerados con `build.py`.
