# Reporte: cierre del hueco del Art. 1 e incorporación del Texto original de 1917 del Art. 81

**Repositorio:** `jatovarv/legislacion-mx-prototipo`  
**Rama:** `fix/art1-hueco-art81-original`  
**Base:** posterior al PR #20 (`Corrige 3 defectos menores en Arts. 71, 1 y 81`)

---

## 1. Artículo 1 (golden case): cierre del hueco del `14-08-2001`

### 1.1. Motivo y regla aplicada
La primera reforma del Artículo 1o. (`v2`) fue publicada en el Diario Oficial de la Federación el **`14-08-2001`** (`publicacion: "2001-08-14"`) y entró en vigor al día siguiente, **`15-08-2001`** (`vigencia_desde: "2001-08-15"`), conforme al artículo primero transitorio del decreto y a la regla general del repositorio. Por tanto, el texto original (`v1`, en vigor desde el `1917-05-01`) rigió hasta el **`14-08-2001`** inclusive (`vigencia_hasta: "2001-08-14"`), y no hasta el `13-08-2001` (que se había calculado restando un día a la fecha de publicación en lugar de a la fecha de entrada en vigor).

Con autorización expresa para actualizar este único campo en el golden case del Artículo 1o., se aplicó de forma idéntica en `cpeum.json`, `cpeum-art-1.json` y `historial/1.json`, regenerando `articulos/1.html`. No existe en `tests/` ningún fixture que almacene `vigencia_hasta` (`tests/historial_prueba_art1_art4.json` solo contiene el texto lineal en bruto de prueba del separador).

### 1.2. Diff de los campos cambiados del Artículo 1

- En **`cpeum-art-1.json`** y **`cpeum.json`**:
  ```diff
           "id": "v1",
           "etiqueta": "Original",
           "publicacion": "1917-02-05",
           "vigencia_desde": "1917-05-01",
  -        "vigencia_hasta": "2001-08-13",
  +        "vigencia_hasta": "2001-08-14",
           "capitulo": "De las Garantías Individuales",
  ```
- En **`historial/1.json`**:
  `"vigencia_hasta":"2001-08-13"` → `"vigencia_hasta":"2001-08-14"`.
- En **`articulos/1.html`**:
  `del 1 de mayo de 1917 al 13 de agosto de 2001` → `del 1 de mayo de 1917 al 14 de agosto de 2001`.

---

## 2. Artículo 81: incorporación del «Texto original» de 1917 como `v1`

### 2.1. Fuente y extracción literal por coordenadas
- **PDF oficial SCJN:** `CPEUM_SCJN_Historial/cpeum_scjn.zip` → `Titulo_Tercero/Art_081/00_historia.pdf` (`CPEUM-081_0.pdf`), **página 1 de 1**.
- **Extractor:** `extraer_historia_scjn_pdf.py` (`pdfplumber`, columna izquierda `x0 < 130` para encabezados, columna derecha `x0 >= 130` para texto normativo).

### 2.2. Salida en bruto de `extraer_historia_scjn_pdf.py` (`pdfplumber`)
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

### 2.3. Coordenadas `(x0, top, x1, bottom)` de `pdfplumber` en la página 1

- **Encabezado de la versión original (columna izquierda `x0 < 130`, pág. 1, `top=225.50–259.70`):**
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

- **Inicio y fin (totalidad de palabras) del texto de 1917 (columna derecha `x0 >= 130`, pág. 1, `top=225.50–237.62`):**
  ```python
  [
    ('Art.',       x0=150.24, top=225.50),
    ('81.-',       x0=174.60, top=225.50),
    ('La',         x0=200.88, top=225.50),
    ('elección',   x0=216.12, top=225.50),
    ('del',        x0=259.92, top=225.50),
    ('Presidente', x0=278.64, top=225.50),
    ('será',       x0=334.92, top=225.50),
    ('directa',    x0=359.88, top=225.50),
    ('y',          x0=398.04, top=225.50),
    ('en',         x0=407.64, top=225.50),
    ('los',        x0=423.48, top=225.50),
    ('términos',   x0=441.12, top=225.50),
    ('que',        x0=489.12, top=225.50),
    ('disponga',   x0=511.32, top=225.50),
    ('la',         x0=559.92, top=225.50),
    ('ley',        x0=150.24, top=237.62),
    ('electoral.', x0=168.36, top=237.62),
  ]
  ```
  - **Inicio del texto:** `"Art. 81.- La elección del Presidente"` (`x0=150.24, top=225.50`)
  - **Fin del texto:** `"disponga la ley electoral."` (`x0=168.36, top=237.62`)
  - **Texto literal íntegro (conservando `"Presidente"` con mayúscula inicial de época):**
    `"Art. 81.- La elección del Presidente será directa y en los términos que disponga la ley electoral."`

- **Encabezado de la versión vigente (columna izquierda `x0 < 130`, pág. 1, `top=289.58–336.02`):**
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

### 2.4. Cadena de vigencias del Artículo 81

| `id` | `tipo` | `etiqueta` | `publicacion` | `vigencia_desde` | `vigencia_hasta` |
|---|---|---|---|---|---|
| `v1` | `"original"` | `"Original"` | `1917-02-05` | `1917-05-01` | `2019-12-20` |
| `v2` | `"vigente"` | `"Vigente (post 20-12-2019)"` | `2019-12-20` | `2019-12-21` | `null` |

---

## 3. Verificación de criterios de aceptación

1. **En `cpeum.json` solo cambian los Arts. 1 y 81:** Verificado con `git diff cpeum.json`.
2. **Art. 1: un único campo cambia (`v1.vigencia_hasta = "2001-08-14"`) y es coherente en los tres archivos:** Comprobado en `cpeum.json`, `cpeum-art-1.json` y `historial/1.json`.
3. **Art. 81: 2 versiones; la `v1` literal del PDF, con evidencia; un solo vigente; vigencias encadenadas:** `v1` (`1917-05-01` → `2019-12-20`) y `v2` (`2019-12-21` → `null`).
4. **Golden case Art. 4 idéntico a `main`:** `cpeum-art-4.json` y `cpeum.json['articulos']['4']` sin cambios.
5. **Un solo vigente y una sola vigencia abierta por artículo en los 136:** Comprobado en los 136 artículos (`vigencia_hasta: null` solo en `versiones[-1]`, sin huecos en las cadenas de vigencia).
6. **Esquema 136/136; `build.py` reproducible; páginas regeneradas solo de los Arts. 1 y 81:** Regenerados `historial/1.json`, `historial/81.json`, `articulos/1.html`, `articulos/81.html` e `index.html`.
