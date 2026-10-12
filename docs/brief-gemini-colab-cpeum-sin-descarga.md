# Brief cerrado — Gemini Ultra (Colab)
## Re-extracción de los 136 artículos del CPEUM (sin descargar)

**Importante:** No descargues el PDF. El usuario ya lo tiene. Súbelo a Colab o cárgalo desde Drive.

### Pasos en Colab

1. Sube el archivo `CPEUM.pdf` (el mismo que ya descargaste de la Cámara).
2. Ejecuta el siguiente código (usa `pymupdf`, no `fitz`).

```python
# Instalar si hace falta
!pip install -q pymupdf

import pymupdf
import json
import re
from google.colab import files

# Subir el PDF
print("Sube el CPEUM.pdf")
uploaded = files.upload()
pdf_name = list(uploaded.keys())[0]

doc = pymupdf.open(pdf_name)
print(f"Páginas: {len(doc)}")

articles = []
current = None
buf = []

def is_noise(line):
    s = line.strip()
    if not s:
        return True
    if re.match(r"^(CONSTITUCIÓN POLÍTICA|CÁMARA DE DIPUTADOS|Secretaría|Última Reforma)", s):
        return True
    if re.match(r"^\d+\s+de\s+\d+$", s) or re.match(r"^\d+\s*$", s):
        return True
    if re.match(r"^(Párrafo|Artículo|Fracción|Denominación).*(reformad|adicionad|DOF)", s, re.I):
        return True
    if re.match(r"^(Título|Capítulo|Sección)\s+", s, re.I):
        return True
    return False

for i, page in enumerate(doc):
    if i % 50 == 0:
        print(f"Página {i+1}")
    text = page.get_text("text") or ""
    for raw in text.split("\n"):
        line = raw.strip()
        if is_noise(line):
            continue
        m = re.match(r"^Artículo\s+(\d+[oª]?)\.?\s*(.*)$", line, re.I)
        if m:
            if current and buf:
                articles.append({
                    "numero": current,
                    "texto_vigente": "\n".join(buf).strip(),
                    "notas_reforma": [],
                    "confianza": "alta"
                })
            num = re.sub(r"[oª]", "", m.group(1)).strip()
            current = num
            rest = m.group(2).strip()
            buf = [rest] if rest else []
        elif current:
            buf.append(line)

if current and buf:
    articles.append({
        "numero": current,
        "texto_vigente": "\n".join(buf).strip(),
        "notas_reforma": [],
        "confianza": "alta"
    })

print(f"Artículos extraídos: {len(articles)}")

# Guardar
out = "cpeum-136-articulos.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

files.download(out)
print("JSON descargado.")
```

### Qué debe entregar
- El archivo `cpeum-136-articulos.json` con los 136 artículos.
- Confirmación de que no se intentó descargar el PDF de internet.
- Si algún artículo queda con fracciones pegadas, indícalo.

### Criterios
- Usar el PDF que el usuario sube.
- No inventar texto.
- Separar fracciones e incisos cuando sea posible.
- Conservar marcas `(sic DOF …)` dentro del texto.

Cuando lo tengas, entrega el JSON. El Coordinador lo coteja contra el PR #6.