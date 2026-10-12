# Brief — Gemini Ultra (Colab)
## Re-extracción masiva de los 136 artículos del CPEUM

**Objetivo:** Extraer los 136 artículos del CPEUM.pdf consolidado con fracciones separadas y notas fuera del texto.

### Código para Colab

```python
!pip install -q pymupdf

import pymupdf
import json
import re

# Descargar el PDF
import urllib.request
url = "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf"
urllib.request.urlretrieve(url, "CPEUM.pdf")

doc = pymupdf.open("CPEUM.pdf")
print(f"Páginas: {len(doc)}")

# ... (extractor con is_noise y corte por Artículo)
```

### Criterios
- Fracciones e incisos separados.
- Notas de reforma fuera del texto vigente.
- Marcas `(sic DOF …)` conservadas.
- Exactamente 136 artículos.

Entrega el JSON.