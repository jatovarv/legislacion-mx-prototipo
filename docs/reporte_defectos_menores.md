# Reporte de corrección y documentación de 3 defectos menores preexistentes en `main`

**Repositorio:** `jatovarv/legislacion-mx-prototipo`  
**Rama:** `fix/defectos-menores-main`  
**Base:** `main` (`a970b17`, posterior al merge del PR #19)  
**Método:** Inspección y extracción por coordenadas con `pdfplumber` (`extraer_historia_scjn_pdf.py`, columna izquierda `x0 < 130`, columna derecha `x0 >= 130`) sobre los PDFs oficiales «Historia del texto» de la SCJN (`CPEUM_SCJN_Historial/cpeum_scjn.zip`).

---

## Resumen ejecutivo

| # | Artículo | Defecto reportado | Hallazgo en PDF SCJN (`00_historia.pdf`) | Acción aplicada en este PR |
|---|---|---|---|---|
| 1 | **Art. 71** | Dos versiones (`v3` y `v4`) con `"tipo": "vigente"` | En `Titulo_Tercero/Art_071/00_historia.pdf`, el bloque de 2012 (pág. 1, `top=615.86`) conservó por errata editorial de la SCJN el rótulo `Texto vigente D.O.F. 9 de agosto de 2012` cuando se añadió el bloque de 2016 (pág. 2, `top=453.86`, `Texto vigente D.O.F. 29 de enero de 2016`). | Se cambia `v3.tipo` de `"vigente"` a `"reforma"` en `cpeum.json` y se regenera `historial/71.json`. (`v3.etiqueta` ya era `"Reforma DOF 09-08-2012"`). Solo `v4` conserva `"tipo": "vigente"` y `"vigencia_hasta": null`. |
| 2 | **Art. 1** *(golden case)* | Hueco de un día entre `v1` (`vigencia_hasta: "2001-08-13"`) y `v2` (`vigencia_desde: "2001-08-15"`) | En `Titulo_Primero/Art_001/00_historia.pdf` (3 págs.) existen únicamente **4 versiones**: `05-02-1917` (pág. 1, `top=546.19`), `14-08-2001` (pág. 1, `top=610.22`), `04-12-2006` (pág. 2, `top=304.74`) y `10-06-2011` (pág. 2, `top=528.40`). **No existe versión intermedia del `14-08-2001`**: `v2` *es* la reforma publicada el `14-08-2001` (en vigor el `15-08-2001`), y el hueco se debe a que en el golden case inicial se calculó `v1.vigencia_hasta = v2.publicacion - 1 día` (`2001-08-13`) en vez de `v2.vigencia_desde - 1 día` (`2001-08-14`). | Conforme a la regla del brief (*«Si no hay versión intermedia, documentar el hueco en el reporte y dejar el golden case intacto»*), se documenta con evidencia de página y coordenadas y **se deja intacto el golden case** (`cpeum-art-1.json` y `cpeum.json['articulos']['1']`). |
| 3 | **Art. 81** | Historial incompleto (falta el «Texto original» de 1917 en `cpeum.json`) | En `Titulo_Tercero/Art_081/00_historia.pdf` (pág. 1, `top=225.50`) aparece el encabezado `Texto original 05 de febrero de 1917` (sin `D.O.F.`), omitido por la expresión regular del separador lineal original. | Conforme a los límites del brief (*«NO crear la versión 1917 en este PR. Solo dejar constancia para un PR futuro»*), se documentan página, coordenadas, salida de `pdfplumber` y texto literal íntegro sin modificar el Art. 81 en `cpeum.json`. |

---

## 1. Defecto 1 — Artículo 71: dos versiones con `tipo: "vigente"`

### 1.1. Evidencia de fechas de publicación y vigencia en `cpeum.json`

El Artículo 71 cuenta con 4 versiones encadenadas:

| `id` | `tipo` (antes) | `tipo` (después) | `etiqueta` | `publicacion` | `vigencia_desde` | `vigencia_hasta` | `encabezado_scjn` |
|---|---|---|---|---|---|---|---|
| `v1` | `"original"` | `"original"` | `"Original"` | `1917-02-05` | `1917-05-01` | `2011-08-17` | `Texto original D.O.F. 05 de febrero de 1917` |
| `v2` | `"reforma"` | `"reforma"` | `"Reforma DOF 17-08-2011"` | `2011-08-17` | `2011-08-18` | `2012-08-09` | `Texto derivado de la reforma publicada en el D.O.F. 17 de agosto de 2011` |
| **`v3`** | **`"vigente"`** | **`"reforma"`** | `"Reforma DOF 09-08-2012"` | **`2012-08-09`** | **`2012-08-10`** | **`2016-01-29`** | `Texto vigente D.O.F. 9 de agosto de 2012` |
| `v4` | `"vigente"` | `"vigente"` | `"Vigente (post 29-01-2016)"` | `2016-01-29` | `2016-01-30` | `null` | `Texto vigente D.O.F. 29 de enero de 2016` |

### 1.2. Evidencia de página y coordenadas en el PDF SCJN (`Titulo_Tercero/Art_071/00_historia.pdf`)

- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  [
    {"etiqueta_scjn": "Texto original D.O.F. 05 de febrero de 1917", "tipo": "original", "publicacion": "1917-02-05", "page": 1, "top": 254.29788},
    {"etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 17 de agosto de 2011", "tipo": "reforma", "publicacion": "2011-08-17", "page": 1, "top": 429.85788},
    {"etiqueta_scjn": "Texto vigente D.O.F. 9 de agosto de 2012", "tipo": "reforma", "publicacion": "2012-08-09", "page": 1, "top": 615.85788},
    {"etiqueta_scjn": "Texto vigente D.O.F. 29 de enero de 2016", "tipo": "vigente", "publicacion": "2016-01-29", "page": 2, "top": 453.85788}
  ]
  ```
- **Coordenadas en columna izquierda (`x0 < 130`, `pdfplumber`):**
  - **`v3` (Pág. 1, `top=615.86–662.30`):** `('Texto', x0=48.96, top=615.86, x1=80.53, bottom=625.82)`, `('vigente', x0=83.88, top=615.86, x1=125.77, bottom=625.82)`, `('D.O.F.', x0=70.32, top=627.98, x1=104.39, bottom=637.94)`, `('9', x0=46.20, top=640.22, x1=53.28, bottom=650.18)`, `('de', x0=56.64, top=640.22, x1=70.22, bottom=650.18)`, `('agosto', x0=73.80, top=640.22, x1=111.61, bottom=650.18)`, `('de', x0=114.97, top=640.22, x1=128.66, bottom=650.18)`, `('2012', x0=73.20, top=652.34, x1=101.53, bottom=662.30)`
  - **`v4` (Pág. 2, `top=453.86–500.30`):** `('Texto', x0=48.96, top=453.86, x1=80.53, bottom=463.82)`, `('vigente', x0=83.88, top=453.86, x1=125.78, bottom=463.82)`, `('D.O.F.', x0=70.32, top=465.98, x1=104.39, bottom=475.94)`, `('29', x0=45.48, top=478.10, x1=59.64, bottom=488.06)`, `('de', x0=63.00, top=478.10, x1=76.70, bottom=488.06)`, `('enero', x0=80.04, top=478.10, x1=112.33, bottom=488.06)`, `('de', x0=115.81, top=478.10, x1=129.38, bottom=488.06)`, `('2016', x0=73.20, top=490.34, x1=101.53, bottom=500.30)`

Con el cambio de `v3.tipo` a `"reforma"`, ningún artículo en los 136 de `cpeum.json` tiene más de una versión con `"tipo": "vigente"` ni más de una versión con `"vigencia_hasta": null`.

---

## 2. Defecto 2 — Artículo 1 (golden case): verificación del hueco de un día (`14-08-2001`)

### 2.1. Estado en `cpeum-art-1.json` y `cpeum.json['articulos']['1']`

| `id` | `etiqueta` | `publicacion` | `vigencia_desde` | `vigencia_hasta` | Observación |
|---|---|---|---|---|---|
| `v1` | `"Original"` | `1917-02-05` | `1917-05-01` | **`2001-08-13`** | Calculado originalmente como `v2.publicacion - 1 día` (`2001-08-14 - 1 = 2001-08-13`) |
| `v2` | `"Post 14-08-2001"` | `2001-08-14` | **`2001-08-15`** | `2006-12-04` | El decreto DOF `14-08-2001` entró en vigor al día siguiente (`2001-08-15`); `vigencia_hasta` = `v3.vigencia_desde - 1 día` (`2006-12-04`) |
| `v3` | `"Post 04-12-2006"` | `2006-12-04` | `2006-12-05` | `2011-06-10` | `vigencia_hasta` = `v4.vigencia_desde - 1 día` (`2011-06-10`) |
| `v4` | `"Vigente (post 10-06-2011)"` | `2011-06-10` | `2011-06-11` | `null` | Versión vigente |

### 2.2. Evidencia de página y coordenadas en el PDF SCJN (`Titulo_Primero/Art_001/00_historia.pdf`)

El PDF oficial de la SCJN consta de 3 páginas y contiene **únicamente 4 encabezados de versión** en la columna izquierda (`x0 < 130`):

- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  [
    {"etiqueta_scjn": "Texto original D.O.F. 05 de febrero de 1917", "tipo": "original", "publicacion": "1917-02-05", "page": 1, "top": 546.19},
    {"etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 14 de agosto de 2001", "tipo": "reforma", "publicacion": "2001-08-14", "page": 1, "top": 610.22},
    {"etiqueta_scjn": "Texto derivado de la reforma publicada en el D.O.F. 04 de diciembre de 2006", "tipo": "reforma", "publicacion": "2006-12-04", "page": 2, "top": 304.74},
    {"etiqueta_scjn": "Texto vigente D.O.F. 10 de junio de 2011", "tipo": "vigente", "publicacion": "2011-06-10", "page": 2, "top": 528.40}
  ]
  ```
- **Palabras y coordenadas de `pdfplumber` en la columna izquierda (`x0 < 130`) de la Pág. 1 (`v1` y `v2`):**
  - **Bloque 1 (`v1`, Pág. 1, `top=546.19–592.62`):**
    `('Texto', x0=53.83, top=546.19, x1=85.29, bottom=556.19)`, `('original', x0=88.62, top=546.19, x1=131.43, bottom=556.19)`, `('D.O.F.', x0=75.62, top=558.40, x1=110.00, bottom=568.40)`, `('05', x0=46.23, top=570.42, x1=60.52, bottom=580.42)`, `('de', x0=64.03, top=570.42, x1=77.66, bottom=580.42)`, `('febrero', x0=81.03, top=570.42, x1=122.24, bottom=580.42)`, `('de', x0=125.62, top=570.42, x1=139.25, bottom=580.42)`, `('1917', x0=78.62, top=582.62, x1=107.11, bottom=592.62)`
  - **Bloque 2 (`v2`, Pág. 1, `top=610.22–681.02`):**
    `('Texto', x0=50.83, top=610.22, x1=82.29, bottom=620.22)`, `('derivado', x0=85.64, top=610.22, x1=134.67, bottom=620.22)`, `('de', x0=55.02, top=622.42, x1=68.66, bottom=632.42)`, `('la', x0=72.03, top=622.42, x1=82.12, bottom=632.42)`, `('reforma', x0=85.44, top=622.42, x1=130.30, bottom=632.42)`, `('publicada', x0=50.42, top=634.62, x1=104.49, bottom=644.62)`, `('en', x0=107.84, top=634.62, x1=121.54, bottom=644.62)`, `('el', x0=125.03, top=634.62, x1=135.03, bottom=644.62)`, `('D.O.F.', x0=75.62, top=646.62, x1=110.00, bottom=656.62)`, `('14', x0=48.02, top=658.82, x1=62.32, bottom=668.82)`, `('de', x0=65.83, top=658.82, x1=79.45, bottom=668.82)`, `('agosto', x0=82.82, top=658.82, x1=120.66, bottom=668.82)`, `('de', x0=124.00, top=658.82, x1=137.63, bottom=668.82)`, `('2001', x0=78.62, top=671.02, x1=107.11, bottom=681.02)`
  - **Bloque 3 (`v3`, Pág. 2, `top=304.74–375.57`):**
    `('Texto', x0=50.83, top=304.74, x1=82.29, bottom=314.74)`, `('derivado', x0=85.64, top=304.74, x1=134.67, bottom=314.74)`, ..., `('04', x0=47.62, top=353.34, x1=61.92, bottom=363.34)`, `('de', x0=65.42, top=353.34, x1=79.05, bottom=363.34)`, `('diciembre', x0=82.42, top=353.34, x1=137.81, bottom=363.34)`, `('de', x0=70.03, top=365.57, x1=83.66, bottom=375.57)`, `('2006', x0=87.03, top=365.57, x1=115.52, bottom=375.57)`
  - **Bloque 4 (`v4`, Pág. 2, `top=528.40–574.80`):**
    `('Texto', x0=54.42, top=528.40, x1=85.89, bottom=538.40)`, `('vigente', x0=89.22, top=528.40, x1=131.24, bottom=538.40)`, `('D.O.F.', x0=75.62, top=540.60, x1=110.00, bottom=550.60)`, `('10', x0=52.62, top=552.60, x1=66.92, bottom=562.60)`, `('de', x0=70.42, top=552.60, x1=84.05, bottom=562.60)`, `('junio', x0=87.42, top=552.60, x1=116.08, bottom=562.60)`, `('de', x0=119.41, top=552.60, x1=133.03, bottom=562.60)`, `('2011', x0=78.62, top=564.80, x1=107.11, bottom=574.80)`

### 2.3. Conclusión sobre el Artículo 1

No existe ninguna versión intermedia en el PDF de la SCJN entre el texto original (`05-02-1917`) y la primera reforma (`14-08-2001`, que es `v2`). El hueco de un día (`2001-08-14`) en `v1.vigencia_hasta` (`"2001-08-13"`) proviene de haber restado un día a `v2.publicacion` (`2001-08-14`) en vez de a `v2.vigencia_desde` (`2001-08-15`) al redactar manualmente `cpeum-art-1.json`. Conforme a la instrucción del brief (*«Si no hay versión intermedia, documentar el hueco en el reporte y dejar el golden case intacto»*), **no se modifica `cpeum-art-1.json` ni `cpeum.json['articulos']['1']`**.

---

## 3. Defecto 3 — Artículo 81: historial incompleto (constancia del «Texto original» de 1917)

### 3.1. Hallazgo en el PDF SCJN (`Titulo_Tercero/Art_081/00_historia.pdf`)

El PDF oficial de la SCJN para el Artículo 81 (1 página en total) contiene **dos versiones**:
1. **Texto original de 1917** (Pág. 1, `top=225.50`), cuyo encabezado en la columna izquierda dice `Texto original 05 de febrero de 1917` (sin las siglas `D.O.F.`), razón por la cual `separar_versiones_scjn.py` no lo detectó como frontera de versión.
2. **Texto vigente de 2019** (Pág. 1, `top=289.58`), cuyo encabezado dice `Texto vigente D.O.F el 20 de diciembre de 2019` (actual `v1` en `cpeum.json`).

### 3.2. Salida de `pdfplumber` y coordenadas de la columna izquierda (`x0 < 130`, Pág. 1)

- **Salida de `extraer_historia_scjn_pdf.py` (`pdfplumber`):**
  ```json
  [
    {
      "etiqueta_scjn": "Texto original 05 de febrero de 1917",
      "tipo": "original",
      "publicacion": "1917-02-05",
      "page": 1,
      "top": 225.49788,
      "texto": "Art. 81.- La elección del Presidente será directa y en los términos que disponga la ley electoral.",
      "notas_scjn": []
    },
    {
      "etiqueta_scjn": "Texto vigente D.O.F el 20 de diciembre de 2019",
      "tipo": "vigente",
      "publicacion": "2019-12-20",
      "page": 1,
      "top": 289.57788,
      "texto": "Art. 81.- La elección del presidente será directa y en los términos que disponga la ley electoral. El cargo de presidente de los Estados Unidos Mexicanos puede ser revocado en los términos establecidos en esta Constitución.",
      "notas_scjn": [
        "(REFORMADO, D.O.F. 20 DE DICIEMBRE DE 2019)"
      ]
    }
  ]
  ```
- **Palabras y coordenadas de `pdfplumber` en la columna izquierda (`x0 < 130`, Pág. 1):**
  - **Encabezado «Texto original» (`top=225.50–259.70`):**
    ```python
    [
      ('Texto',    x0=53.88, top=225.50, x1=85.45,  bottom=235.46),
      ('original', x0=88.80, top=225.50, x1=131.69, bottom=235.46),
      ('05',       x0=46.32, top=237.62, x1=60.48,  bottom=247.58),
      ('de',       x0=63.84, top=237.62, x1=77.54,  bottom=247.58),
      ('febrero',  x0=80.88, top=237.62, x1=122.17, bottom=247.58),
      ('de',       x0=125.65, top=237.62, x1=139.22, bottom=247.58),
      ('1917',     x0=78.60, top=249.74, x1=106.93, bottom=259.70),
    ]
    ```
  - **Encabezado «Texto vigente» (`top=289.58–336.02`):**
    ```python
    [
      ('Texto',     x0=54.36, top=289.58, x1=85.93,  bottom=299.54),
      ('vigente',   x0=89.28, top=289.58, x1=131.17, bottom=299.54),
      ('D.O.F',     x0=53.52, top=301.70, x1=83.98,  bottom=311.66),
      ('el',        x0=87.35, top=301.70, x1=97.48,  bottom=311.66),
      ('20',        x0=100.91, top=301.70, x1=115.07, bottom=311.66),
      ('de',        x0=118.56, top=301.70, x1=132.13, bottom=311.66),
      ('diciembre', x0=56.52, top=313.82, x1=111.97, bottom=323.78),
      ('de',        x0=115.43, top=313.82, x1=129.01, bottom=323.78),
      ('2019',      x0=78.60, top=326.06, x1=106.93, bottom=336.02),
    ]
    ```
- **Palabras y coordenadas del texto original de 1917 en columna derecha (`x0 >= 130`, Pág. 1, `top=225.50–237.62`):**
  `('Art.', 150.24, 225.50)`, `('81.-', 174.60, 225.50)`, `('La', 200.88, 225.50)`, `('elección', 216.12, 225.50)`, `('del', 259.92, 225.50)`, `('Presidente', 278.64, 225.50)`, `('será', 334.92, 225.50)`, `('directa', 359.88, 225.50)`, `('y', 398.04, 225.50)`, `('en', 407.64, 225.50)`, `('los', 423.48, 225.50)`, `('términos', 441.12, 225.50)`, `('que', 489.12, 225.50)`, `('disponga', 511.32, 225.50)`, `('la', 559.92, 225.50)`, `('ley', 150.24, 237.62)`, `('electoral.', 168.36, 237.62)`

### 3.3. Acción en este PR

Conforme a la instrucción expresa del brief (*«NO crear la versión 1917 en este PR (el brief anterior no lo permitía). Solo dejar constancia para un PR futuro»*), no se modifica el Artículo 81 en `cpeum.json` y queda lista la evidencia íntegra para incorporar la versión original (`1917-02-05`, vigencia `1917-05-01` → `2019-12-20`) cuando se autorice.

---

## 4. Verificación de criterios de aceptación

1. **No inventar ni parafrasear texto normativo:** Ningún campo `texto` fue modificado.
2. **Solo se modifican los campos de tipo/etiqueta del Art. 71:** El diff en `cpeum.json` es de una sola línea (`"tipo": "vigente"` → `"tipo": "reforma"` en `Art. 71 v3`).
3. **Golden cases 1 y 4 intactos:** `cpeum-art-1.json` y `cpeum-art-4.json` idénticos a `cpeum.json['articulos']['1']` y `cpeum.json['articulos']['4']`.
4. **Un solo vigente por artículo en los 136:** Comprobado tanto por `vigencia_hasta: null` (1 por artículo en los 136) como por `tipo == "vigente"` (nunca en versiones no finales).
5. **`docs/reporte_defectos_menores.md` con evidencia de página + coordenadas para los tres casos:** Incluido en este documento.
6. **`build.py` regenerado solo para los artículos afectados:** Regenerado `historial/71.json`.
