# Reporte de separación de las 34 versiones fusionadas (Tarea 4)

## 1. Resumen ejecutivo

En el estado posterior al PR #13 (`origin/main`), `cpeum.json` registraba **34 versiones con bloques fusionados** distribuidas en **21 artículos** (`2, 10, 16, 20, 22, 26, 27, 28, 35, 74, 94, 95, 96, 97, 98, 99, 107, 108, 116, 122, 123`), todas marcadas con `extraccion_pendiente: true` («extracción por cotejar»).

Mediante la extracción por coordenadas desde los PDFs originales de la SCJN (`00_historia.pdf` en `cpeum_scjn.zip`, procesados con `extraer_historia_scjn_pdf.py` usando el umbral horizontal `SPLIT_X = 130` pt —y `170` pt en el Art. 35— entre la columna izquierda de etiquetas y la columna derecha de texto normativo):

- **34 de 34 versiones fusionadas (100 %)** quedaron **resueltas y separadas** sin inferir ninguna fecha ni alterar texto normativo:
  - **3** en el **Art. 35** (resueltas en la Tarea 2, PR #15).
  - **5** en artículos del **Grupo A** (`Arts. 2, 10, 20, 22`, resueltas en la Tarea 3, PR #16).
  - **26** en los **16 artículos restantes** (`Arts. 16, 26, 27, 28, 74, 94, 95, 96, 97, 98, 99, 107, 108, 116, 122, 123`, resueltas en esta Tarea 4).
- **0 versiones fusionadas** requieren un PDF actualizado para su separación (todas correspondían a reformas ya contenidas en el `00_historia.pdf` de la SCJN; véase la sección 4 respecto del estado general de los artículos 82, 116 y 122 por la reforma de `07-10-2026`).
- Adicionalmente, la re-extracción por coordenadas de estos artículos permitió **recuperar desde el PDF de la SCJN la fecha legible** de **8 versiones** que tenían `fecha_pendiente: true` (`Art. 28` `2024-10-30`; `Art. 35` `2019-06-06` y `2019-12-20`; `Art. 94` `1996-08-22`; `Art. 116` `2007-11-13`; `Art. 122` `2020-12-18`; `Art. 123` `1960-12-05` y `1994-12-31`), reduciendo el total de versiones con `fecha_pendiente: true` en toda la CPEUM de 18 a **10** (9 en artículos verificados más la del Art. 81).

---

## 2. Inventario completo de las 34 versiones fusionadas y su resolución

| # | Art. | Versión original (`main`) | Fecha en `main` | Etiqueta(s) SCJN incrustada(s) en el cuerpo | Causa probable del fallo en el separador lineal | Versiones resultantes tras extracción por coordenadas (`00_historia.pdf`) | Tarea / PR |
|---:|---:|:---:|:---:|---|---|---|---|
| 1 | **2** | `v3` | `2015-05-22` | 4 etiquetas (`Texto derivado de la reforma...` ×3; `Texto vigente publicado en el D.O.F. 30 de septiembre de 2024`) | Etiquetas partidas por salto de página en el volcado lineal y etiqueta final sin `el` antes de la fecha | `v3` (`2015-05-22`), `v4` (`2016-01-29`), `v5` (`2019-06-06`), `v6` (`2019-08-09`) y cierre con `v7` (`2024-09-30`) | Tarea 3 (PR #16) |
| 2 | **10** | `v2` | `1971-10-22` | 1 etiqueta (`Texto vigente derivado de la reforma publicada en el D.O.F.`) | Fórmula atípica `Texto vigente derivado de la reforma...` con corte de página antes de la fecha `26 de marzo de 2019` | `v2` (`1971-10-22`) y `v3` (`2019-03-26`) | Tarea 3 (PR #16) |
| 3 | **16** | `v4` | `1996-07-03` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la columna izquierda (`08 de marzo de 1999` quedó en la página siguiente) | `v4` (`1996-07-03`) y `v5` (`1999-03-08`) | Tarea 4 |
| 4 | **20** | `v9` | `2011-07-14` | 1 etiqueta (`Texto vigente 15 de septiembre de 2024`) | Omisión de `publicado en el D.O.F.` entre `Texto vigente` y la fecha en el volcado lineal | `v9` (`2011-07-14`) y `v10` (`2024-09-15`) | Tarea 3 (PR #16) |
| 5 | **22** | `v5` | `2005-12-09` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `18 de junio de 2008` | `v5` (`2005-12-09`) y `v6` (`2008-06-18`) | Tarea 3 (PR #16) |
| 6 | **22** | `v6` | `2015-05-27` | 1 etiqueta (`Texto vigente publicado en el D.O.F.`) | Corte de página entre `D.O.F.` y la fecha `14 de marzo de 2019` | `v7` (`2015-05-27`) y `v8` (`2019-03-14`) | Tarea 3 (PR #16) |
| 7 | **26** | `v2` | `1983-02-03` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `07 de abril de 2006` | `v2` (`1983-02-03`) y `v3` (`2006-04-07`) | Tarea 4 |
| 8 | **27** | `v10` | `1960-12-29` | 1 etiqueta (`Texto derivado de la fe de erratas`) | Corte de página a mitad de la etiqueta de la fe de erratas de `07 de enero de 1961` | `v10` (`1960-12-29`) y `v11` (`1961-01-07`) | Tarea 4 |
| 9 | **27** | `v17` | `1992-01-06` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `28 de enero de 1992` | `v18` (`1992-01-06`) y `v19` (`1992-01-28`) | Tarea 4 |
| 10 | **27** | `v18` | `2011-10-13` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `11 de junio de 2013` | `v20` (`2011-10-13`) y `v21` (`2013-06-11`) | Tarea 4 |
| 11 | **28** | `v3` | `1983-02-03` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `27 de junio de 1990` | `v3` (`1983-02-03`) y `v4` (`1990-06-27`) | Tarea 4 |
| 12 | **28** | `v8` | `2013-12-20` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `10 de febrero de 2014` | `v9` (`2013-12-20`) y `v10` (`2014-02-10`) | Tarea 4 |
| 13 | **35** | `v2` | `1990-04-06` | 1 etiqueta (`Texto derivado de la reforma Art. 35.- Son prerrogativas del ciudadano:`) | Intercalación del arranque del artículo dentro de la etiqueta de `22 de agosto de 1996` en el volcado lineal | `v2` (`1990-04-06`) y `v3` (`1996-08-22`) | Tarea 2 (PR #15) |
| 14 | **35** | `v4` | `2014-02-10` | 1 etiqueta (`Texto derivado de la reforma`) | Etiqueta de la reforma de `26 de marzo de 2019` escrita con `DOF` sin puntos y partida por salto de página | `v5` (`2014-02-10`) y `v6` (`2019-03-26`) | Tarea 2 (PR #15) |
| 15 | **35** | `v6` | `null` | 1 etiqueta (`Texto vigente publicado en el D.O.F. el 02 de junio de 2026`) | Preposición `el` antes de la fecha en `Texto vigente publicado en el D.O.F. el 02 de junio de 2026` no reconocida por el regex lineal | `v8` (`2019-12-20`) y `v9` (`2026-06-02`) | Tarea 2 (PR #15) |
| 16 | **74** | `v11` | `1993-10-25` | 1 etiqueta (`Texto derivado de la reforma Art. 74.- Son facultades exclusivas de la Cámara de Diputados:`) | Intercalación del arranque del artículo a mitad de la etiqueta de la reforma de `22 de agosto de 1996` en el volcado lineal | `v11` (`1993-10-25`) y `v12` (`1996-08-22`) | Tarea 4 |
| 17 | **94** | `v8` | `1982-12-28` | 1 etiqueta (`Texto derivado de la reforma publicada en el`) | Corte de página entre `publicada en el` y `D.O.F. 10 de agosto de 1987` | `v8` (`1982-12-28`) y `v9` (`1987-08-10`) | Tarea 4 |
| 18 | **94** | `v15` | `2021-03-11` | 1 etiqueta (`Texto derivado de la reforma publicada en el`) | Corte de página entre `publicada en el` y `D.O.F. 15 de septiembre de 2024` | `v16` (`2021-03-11`) y `v17` (`2024-09-15`) | Tarea 4 |
| 19 | **95** | `v4` | `2007-08-02` | 1 etiqueta (`Texto derivado de la reforma publicada en el`) | Corte de página entre `publicada en el` y `D.O.F. 10 de febrero de 2014` | `v4` (`2007-08-02`) y `v5` (`2014-02-10`) | Tarea 4 |
| 20 | **96** | `v2` | `1928-08-20` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `31 de diciembre de 1994` | `v2` (`1928-08-20`) y `v3` (`1994-12-31`) | Tarea 4 |
| 21 | **97** | `v7` | `1987-08-10` | 2 etiquetas (`Texto derivado de la reforma` ×2) | Cortes de página a mitad de las etiquetas de `31 de diciembre de 1994` y `11 de junio de 1999` (3 versiones reunidas en 1) | `v7` (`1987-08-10`), `v8` (`1994-12-31`) y `v9` (`1999-06-11`) | Tarea 4 |
| 22 | **97** | `v8` | `2007-11-13` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `10 de junio de 2011` | `v10` (`2007-11-13`) y `v11` (`2011-06-10`) | Tarea 4 |
| 23 | **98** | `v2` | `1928-08-20` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `19 de febrero de 1951` | `v2` (`1928-08-20`) y `v3` (`1951-02-19`) | Tarea 4 |
| 24 | **99** | `v7` | `2014-02-10` | 2 etiquetas (`Texto derivado de la reforma publicada en el 20 de diciembre de 2019`; `Texto derivado de la reforma publicada en el`) | Omisión de `D.O.F.` en la etiqueta de `20 de diciembre de 2019` y corte de página en la etiqueta de `11 de marzo de 2021` (3 versiones reunidas en 1) | `v7` (`2014-02-10`), `v8` (`2019-12-20`) y `v9` (`2021-03-11`) | Tarea 4 |
| 25 | **107** | `v1` | `1917-02-05` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `19 de febrero de 1951` | `v1` (`1917-02-05`) y `v2` (`1951-02-19`) | Tarea 4 |
| 26 | **107** | `v4` | `1967-10-25` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `20 de marzo de 1974` | `v5` (`1967-10-25`) y `v6` (`1974-03-20`) | Tarea 4 |
| 27 | **107** | `v14` | `2011-06-06` | 1 etiqueta (`Texto derivado de la reforma publicada en el`) | Corte de página entre `publicada en el` y `D.O.F. 10 de febrero de 2014` | `v16` (`2011-06-06`) y `v17` (`2014-02-10`) | Tarea 4 |
| 28 | **108** | `v3` | `1994-12-31` | 1 etiqueta (`Texto derivado de la fe de`) | Corte de página a mitad de la etiqueta de la fe de erratas de `03 de enero de 1995` | `v3` (`1994-12-31`) y `v4` (`1995-01-03`) | Tarea 4 |
| 29 | **116** | `v14` | `2015-05-27` | 1 etiqueta (`Texto derivado de la reforma publicada en el`) | Corte de página entre `publicada en el` y `D.O.F. 20 de diciembre de 2019` | `v14` (`2015-05-27`) y `v15` (`2019-12-20`) | Tarea 4 |
| 30 | **122** | `v10` | `2012-08-09` | 1 etiqueta (`Texto derivado de la reforma D.O.F. 27 de diciembre de 2013`) | Omisión de `publicada en el` antes de `D.O.F. 27 de diciembre de 2013` en la etiqueta de la SCJN | `v10` (`2012-08-09`) y `v11` (`2013-12-27`) | Tarea 4 |
| 31 | **123** | `v12` | `1974-12-31` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `06 de febrero de 1975` | `v12` (`1974-12-31`) y `v13` (`1975-02-06`) | Tarea 4 |
| 32 | **123** | `v14` | `1978-01-09` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta del segundo decreto publicado el `09 de enero de 1978` | `v15` (`1978-01-09`, primer decreto) y `v16` (`1978-01-09`, segundo decreto) | Tarea 4 |
| 33 | **123** | `v23` | `2008-06-18` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `24 de agosto de 2009` | `v25` (`2008-06-18`) y `v26` (`2009-08-24`) | Tarea 4 |
| 34 | **123** | `v24` | `2014-06-17` | 1 etiqueta (`Texto derivado de la reforma`) | Corte de página a mitad de la etiqueta de la reforma de `27 de enero de 2016` | `v27` (`2014-06-17`) y `v28` (`2016-01-27`) | Tarea 4 |

---

## 3. Fechas pendientes recuperadas desde el PDF de la SCJN y evidencia documental

Al extraer por coordenadas los PDFs de los artículos con bloques fusionados, `extraer_historia_scjn_pdf.py` reunió las líneas de la columna izquierda (`x0 < SPLIT_X`) y recuperó las fechas legibles en el PDF de la SCJN para **8 versiones** que en `main` tenían `publicacion: null` y `fecha_pendiente: true`:

| Art. | Versión en `main` | Versión actual | Fecha recuperada del PDF SCJN | Páginas y coordenadas verticales (`top`) en `00_historia.pdf` |
|---:|:---:|:---:|:---:|---|
| **28** | `v12` | `v14` | `2024-10-30` | **Pág. 62** (`top=637.94..674.42`) → **Pág. 63** (`top=137.78..150.02`, fecha en `x0=54.00..131.66`) |
| **35** | `v5` | `v7` | `2019-06-06` | **Pág. 7** (`top=551.06..611.78`, fecha en `x0=73.44..159.97`; tenía `el 6 de junio de 2019` con `el`) |
| **35** | `v6` (1.ª mitad) | `v8` | `2019-12-20` | **Pág. 9** (`top=453.86..526.70`, fecha en `x0=80.64..153.13`; tenía `el 20 de diciembre de 2019` con `el`) |
| **94** | `v10` | `v11` | `1996-08-22` | **Pág. 6** (`top=668.30..704.78`) → **Pág. 7** (`top=114.14..126.26`, fecha en `x0=47.28..119.77`) |
| **116** | `v5` | `v5` | `2007-11-13` | **Pág. 8** (`top=617.18..659.06`) → **Pág. 9** (`top=137.78..165.74`, fecha en `x0=54.48..131.18`) |
| **122** | `v16` | `v17` | `2020-12-18` | **Pág. 142** (`top=207.74..268.46`, fecha en `x0=47.76..137.90`; tenía `el 18 de diciembre de 2020` con `el`) |
| **123** | `v6` | `v6` | `1960-12-05` | **Pág. 25** (`top=635.54..672.02`) → **Pág. 26** (`top=137.78..150.02`, fecha en `x0=47.76..137.90`) |
| **123** | `v21` | `v23` | `1994-12-31` | **Pág. 203** (`top=653.18..689.66`) → **Pág. 204** (`top=137.78..150.02`, fecha en `x0=47.76..137.90`) |

### 3.1. Evidencia palabra por palabra (`pdfplumber`) y salida en bruto de `extraer_historia_scjn_pdf.py`

A continuación se documentan las coordenadas exactas `(x0, top, x1, bottom)` de cada palabra en la columna izquierda (`x0 < 130`) y la salida en bruto de `extraer_historia_scjn_pdf.py` para las 5 fechas partidas por corte de página (más la del Art. 122):

#### 1) Art. 28 — `30-10-2024` (`v14`, antes `v12` en `main`)
- **Archivo PDF:** `Titulo_Primero/Capitulo_I/Art_028/00_historia.pdf`
- **Salida en bruto de `extraer_historia_scjn_pdf.py`:**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 30 de octubre de 2024",
    "tipo": "reforma",
    "publicacion": "2024-10-30",
    "page": 62,
    "top": 637.93788
  }
  ```
- **Palabras y coordenadas en el PDF (`pdfplumber`, columna izquierda `x0 < 130`):**
  - **Página 62 (final de página):**
    - `'Texto'` (`x0=50.76, top=637.94, x1=82.32, bottom=647.90`), `'derivado'` (`x0=85.68, top=637.94, x1=134.65, bottom=647.90`)
    - `'de'` (`x0=55.08, top=650.06, x1=68.65, bottom=660.02`), `'la'` (`x0=72.12, top=650.06, x1=82.14, bottom=660.02`), `'reforma'` (`x0=85.56, top=650.06, x1=130.50, bottom=660.02`)
    - `'publicada'` (`x0=50.40, top=662.30, x1=104.57, bottom=672.26`), `'en'` (`x0=107.88, top=662.30, x1=121.69, bottom=672.26`), `'el'` (`x0=125.16, top=662.30, x1=135.17, bottom=672.26`)
    - `'D.O.F.'` (`x0=75.72, top=674.42, x1=109.79, bottom=684.38`)
  - **Página 63 (inicio de página, continuación inmediata de la columna izquierda):**
    - `'30'` (`x0=54.00, top=137.78, x1=68.16, bottom=147.74`), `'de'` (`x0=71.52, top=137.78, x1=85.22, bottom=147.74`), `'octubre'` (`x0=88.56, top=137.78, x1=131.66, bottom=147.74`)
    - `'de'` (`x0=70.08, top=150.02, x1=83.66, bottom=159.98`), `'2024'` (`x0=87.00, top=150.02, x1=115.45, bottom=159.98`)

#### 2) Art. 94 — `22-08-1996` (`v11`, antes `v10` en `main`)
- **Archivo PDF:** `Titulo_Tercero/Capitulo_IV/Art_094/00_historia.pdf`
- **Salida en bruto de `extraer_historia_scjn_pdf.py`:**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 22 de agosto de 1996",
    "tipo": "reforma",
    "publicacion": "1996-08-22",
    "page": 6,
    "top": 668.29788
  }
  ```
- **Palabras y coordenadas en el PDF (`pdfplumber`, columna izquierda `x0 < 130`):**
  - **Página 6 (final de página):**
    - `'Texto'` (`x0=41.04, top=668.30, x1=72.60, bottom=678.26`), `'derivado'` (`x0=75.96, top=668.30, x1=124.93, bottom=678.26`)
    - `'de'` (`x0=45.36, top=680.42, x1=58.93, bottom=690.38`), `'la'` (`x0=62.40, top=680.42, x1=72.42, bottom=690.38`), `'reforma'` (`x0=75.84, top=680.42, x1=120.78, bottom=690.38`)
    - `'publicada'` (`x0=40.68, top=692.54, x1=94.85, bottom=702.50`), `'en'` (`x0=98.16, top=692.54, x1=111.97, bottom=702.50`), `'el'` (`x0=115.44, top=692.54, x1=125.45, bottom=702.50`)
    - `'D.O.F.'` (`x0=66.00, top=704.78, x1=100.07, bottom=714.74`)
  - **Página 7 (inicio de página, continuación inmediata de la columna izquierda):**
    - `'22'` (`x0=47.28, top=114.14, x1=61.44, bottom=124.10`), `'de'` (`x0=64.80, top=114.14, x1=78.50, bottom=124.10`), `'agosto'` (`x0=81.96, top=114.14, x1=119.77, bottom=124.10`)
    - `'de'` (`x0=63.00, top=126.26, x1=76.58, bottom=136.22`), `'1996'` (`x0=79.92, top=126.26, x1=108.37, bottom=136.22`)

#### 3) Art. 116 — `13-11-2007` (`v5`, antes `v5` en `main`)
- **Archivo PDF:** `Titulo_Quinto/Art_116/00_historia.pdf`
- **Salida en bruto de `extraer_historia_scjn_pdf.py`:**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 13 de noviembre de 2007",
    "tipo": "reforma",
    "publicacion": "2007-11-13",
    "page": 8,
    "top": 617.17788
  }
  ```
- **Palabras y coordenadas en el PDF (`pdfplumber`, columna izquierda `x0 < 130`):**
  - **Página 8 (final de página):**
    - `'Texto'` (`x0=50.76, top=617.18, x1=82.32, bottom=627.14`), `'derivado'` (`x0=85.68, top=617.18, x1=134.65, bottom=627.14`)
    - `'de'` (`x0=55.08, top=631.10, x1=68.65, bottom=641.06`), `'la'` (`x0=72.12, top=631.10, x1=82.14, bottom=641.06`), `'reforma'` (`x0=85.56, top=631.10, x1=130.50, bottom=641.06`)
    - `'publicada'` (`x0=50.40, top=645.14, x1=104.57, bottom=655.10`), `'en'` (`x0=107.88, top=645.14, x1=121.69, bottom=655.10`), `'el'` (`x0=125.16, top=645.14, x1=135.17, bottom=655.10`)
    - `'D.O.F.'` (`x0=75.72, top=659.06, x1=109.79, bottom=669.02`)
  - **Página 9 (inicio de página, continuación inmediata de la columna izquierda):**
    - `'13'` (`x0=77.16, top=137.78, x1=91.32, bottom=147.74`), `'de'` (`x0=94.68, top=137.78, x1=108.38, bottom=147.74`)
    - `'noviembre'` (`x0=54.48, top=151.82, x1=114.14, bottom=161.78`), `'de'` (`x0=117.61, top=151.82, x1=131.18, bottom=161.78`)
    - `'2007'` (`x0=78.60, top=165.74, x1=106.93, bottom=175.70`)

#### 4) Art. 123 — `05-12-1960` (`v6`, antes `v6` en `main`)
- **Archivo PDF:** `Titulo_Sexto/Art_123/00_historia.pdf`
- **Salida en bruto de `extraer_historia_scjn_pdf.py`:**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 05 de diciembre de 1960",
    "tipo": "reforma",
    "publicacion": "1960-12-05",
    "page": 25,
    "top": 635.53788
  }
  ```
- **Palabras y coordenadas en el PDF (`pdfplumber`, columna izquierda `x0 < 130`):**
  - **Página 25 (final de página):**
    - `'Texto'` (`x0=50.76, top=635.54, x1=82.32, bottom=645.50`), `'derivado'` (`x0=85.68, top=635.54, x1=134.65, bottom=645.50`)
    - `'de'` (`x0=55.08, top=647.66, x1=68.65, bottom=657.62`), `'la'` (`x0=72.12, top=647.66, x1=82.14, bottom=657.62`), `'reforma'` (`x0=85.56, top=647.66, x1=130.50, bottom=657.62`)
    - `'publicada'` (`x0=50.40, top=659.78, x1=104.57, bottom=669.74`), `'en'` (`x0=107.88, top=659.78, x1=121.69, bottom=669.74`), `'el'` (`x0=125.16, top=659.78, x1=135.17, bottom=669.74`)
    - `'D.O.F.'` (`x0=75.72, top=672.02, x1=109.79, bottom=681.98`)
  - **Página 26 (inicio de página, continuación inmediata de la columna izquierda):**
    - `'05'` (`x0=47.76, top=137.78, x1=61.92, bottom=147.74`), `'de'` (`x0=65.28, top=137.78, x1=78.97, bottom=147.74`), `'diciembre'` (`x0=82.32, top=137.78, x1=137.90, bottom=147.74`)
    - `'de'` (`x0=70.08, top=150.02, x1=83.66, bottom=159.98`), `'1960'` (`x0=87.00, top=150.02, x1=115.45, bottom=159.98`)

#### 5) Art. 123 — `31-12-1994` (`v23`, antes `v21` en `main`)
- **Archivo PDF:** `Titulo_Sexto/Art_123/00_historia.pdf`
- **Salida en bruto de `extraer_historia_scjn_pdf.py`:**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 31 de diciembre de 1994",
    "tipo": "reforma",
    "publicacion": "1994-12-31",
    "page": 203,
    "top": 653.17788
  }
  ```
- **Palabras y coordenadas en el PDF (`pdfplumber`, columna izquierda `x0 < 130`):**
  - **Página 203 (final de página):**
    - `'Texto'` (`x0=50.76, top=653.18, x1=82.32, bottom=663.14`), `'derivado'` (`x0=85.68, top=653.18, x1=134.65, bottom=663.14`)
    - `'de'` (`x0=55.08, top=665.30, x1=68.65, bottom=675.26`), `'la'` (`x0=72.12, top=665.30, x1=82.14, bottom=675.26`), `'reforma'` (`x0=85.56, top=665.30, x1=130.50, bottom=675.26`)
    - `'publicada'` (`x0=50.40, top=677.42, x1=104.57, bottom=687.38`), `'en'` (`x0=107.88, top=677.42, x1=121.69, bottom=687.38`), `'el'` (`x0=125.16, top=677.42, x1=135.17, bottom=687.38`)
    - `'D.O.F.'` (`x0=75.72, top=689.66, x1=109.79, bottom=699.62`)
  - **Página 204 (inicio de página, continuación inmediata de la columna izquierda):**
    - `'31'` (`x0=47.76, top=137.78, x1=61.92, bottom=147.74`), `'de'` (`x0=65.28, top=137.78, x1=78.97, bottom=147.74`), `'diciembre'` (`x0=82.32, top=137.78, x1=137.90, bottom=147.74`)
    - `'de'` (`x0=70.08, top=150.02, x1=83.66, bottom=159.98`), `'1994'` (`x0=87.00, top=150.02, x1=115.45, bottom=159.98`)

#### 6) Art. 122 — `18-12-2020` (`v17`, antes `v16` en `main`)
- **Archivo PDF:** `Titulo_Quinto/Art_122/00_historia.pdf`
- **Salida en bruto de `extraer_historia_scjn_pdf.py`:**
  ```json
  {
    "etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. el 18 de diciembre de 2020",
    "tipo": "reforma",
    "publicacion": "2020-12-18",
    "page": 142,
    "top": 207.73788
  }
  ```
- **Palabras y coordenadas en el PDF (`pdfplumber`, página 142, columna izquierda `x0 < 130`):**
  - `'Texto'` (`50.76, 207.74`), `'derivado'` (`85.68, 207.74`), `'de'` (`55.08, 219.86`), `'la'` (`72.12, 219.86`), `'reforma'` (`85.56, 219.86`), `'publicada'` (`50.40, 231.98`), `'en'` (`107.88, 231.98`), `'el'` (`125.16, 231.98`), `'D.O.F.'` (`69.00, 244.22`), `'el'` (`106.44, 244.22`), `'18'` (`47.76, 256.34`), `'de'` (`65.28, 256.34`), `'diciembre'` (`82.32, 256.34`), `'de'` (`70.08, 268.46`), `'2020'` (`87.00, 268.46`).

---

## 4. Log de pendientes restantes en el repositorio y causa de cada uno

Tras completar las Tareas 1 a 4:

1. **Bloques fusionados (`Bloque fusionado por el separador...`):** **0 pendientes** (los 34 fueron separados íntegramente con `extraer_historia_scjn_pdf.py`).
2. **Artículos en estado `historial_parcial` (3 de 136: Arts. 82, 116 y 122):**
   - Su `00_historia.pdf` en la colección de la SCJN fue generado antes de la reforma publicada en el **DOF 07-10-2026** (última versión SCJN: `2025-04-01` en el Art. 82; `2026-06-02` en los Arts. 116 y 122).
   - En los tres artículos (`82`, `116` y `122`) se alineó el esquema de versiones para que el último bloque de la SCJN (`v11` en Art. 82, `v22` en Art. 116 y `v21` en Art. 122) figure como penúltima versión con `"tipo": "reforma"` y etiqueta `Última versión SCJN (...)`, mientras que únicamente la última versión tomada del consolidado de la Cámara (`2026-10-07`: `v12` en Art. 82, `v23` en Art. 116 y `v22` en Art. 122) lleva `"tipo": "vigente"` y `"vigencia_hasta": null`. Quedan en espera de que la SCJN publique el `00_historia.pdf` actualizado al `07-10-2026` (documentado en `docs/reporte_grupo_a.md`).
3. **Versiones con `extraccion_pendiente: true` no fusionadas (4 versiones en 1 artículo):**
   - **Art. 100 (`v5, v6, v7, v8`):** no son bloques fusionados; están marcadas preventivamente porque el PDF original de la SCJN (`Art_100/00_historia.pdf`) imprime por error al pie de página un renglón del Art. 99 («El personal del Tribunal regirá sus relaciones de trabajo...») que parte frases a mitad de renglón. Tanto `separar_versiones_scjn.py` como `extraer_historia_scjn_pdf.py` retiran ese renglón intruso y producen exactamente el mismo texto byte por byte en `v1` a `v8`.
4. **Versiones con `fecha_pendiente: true` (10 versiones en 8 artículos):**
   - En artículos `verificados` donde aún no se ha re-extraído el PDF por coordenadas para recuperar la etiqueta partida por salto de página: **Art. 5** (`v2`, pista `1942-11-17`), **Art. 29** (`v3`, pista `2007-08-02`), **Art. 41** (`v15`, pista `2024-11-15`), **Art. 72** (`v2`, pista `1923-11-24`), **Art. 89** (`v6`, sin pista; `v12`, pista `1994-12-31`), **Art. 100** (`v5`, pista `1994-12-31`) y **Art. 115** (`v14`, pista `2009-08-24`; `v18`, pista `2020-12-18`).
   - En el **Art. 81 (`v1`)**: conserva `fecha_pendiente: true` con pista `2019-12-20` porque el documento fuente de la SCJN para el Art. 81 solo contiene una versión sin fecha impresa en la etiqueta.
