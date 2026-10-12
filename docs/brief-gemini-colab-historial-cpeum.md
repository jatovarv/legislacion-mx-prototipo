# Brief cerrado — Gemini Ultra (Colab)
## Automatización del historial de la CPEUM (Fase 1: descarga y extracción)

**Objetivo:** Descargar los PDF “Historia del texto” de la SCJN para los 136 artículos y extraer las versiones históricas de cada uno.

**Patrón de URL conocido:**
```
https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-XXX.pdf
https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-XXX_2.pdf
```
Ejemplos confirmados:
- Art. 4: `CPEUM-004_2.pdf`
- Art. 40: `CPEUM-040.pdf`
- Art. 94: `CPEUM-094.pdf`

### Código para Colab

```python
!pip install -q pymupdf requests

import pymupdf
import requests
import json
import os
import re
from google.colab import files

os.makedirs("scjn_pdfs", exist_ok=True)
os.makedirs("historial", exist_ok=True)

def try_download(num):
    padded = f"{num:03d}"
    candidates = [
        f"https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-{padded}.pdf",
        f"https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-{padded}_2.pdf",
    ]
    for url in candidates:
        try:
            r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/pdf"):
                path = f"scjn_pdfs/{padded}.pdf"
                with open(path, "wb") as f:
                    f.write(r.content)
                return path, url
        except Exception:
            pass
    return None, None

# Descargar (prueba con los primeros 10; luego escalar)
results = []
for n in range(1, 11):  # empezar pequeño
    path, url = try_download(n)
    results.append({"numero": n, "path": path, "url": url, "ok": path is not None})
    print(f"Art. {n}: {'OK' if path else 'FALLÓ'}")

print("Descarga de prueba terminada. Revisa results.")
# Si la descarga falla en Colab, el usuario subirá los PDFs manualmente.
```

### Qué entregar en esta fase
1. Lista de qué artículos se pudieron descargar y cuáles no.
2. Para los que sí se descargaron: un JSON por artículo con las versiones históricas extraídas (fecha + texto).
3. No inventar texto. Si un PDF no se puede leer, marcarlo.

### Criterios
- Empezar con un lote pequeño (Arts. 1–10) para validar el patrón de URL.
- Si la descarga falla, detenerse y reportar. El usuario puede subir los PDFs.
- El resultado debe servir para alimentar el historial bajo cada artículo.

Cuando tengas el resultado del lote de prueba, avisa. El Coordinador lo revisa antes de escalar a los 136.