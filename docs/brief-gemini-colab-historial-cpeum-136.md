# Brief cerrado — Gemini Ultra (Colab)
## Automatización del historial de la CPEUM (136 artículos)

**Objetivo:** Descargar los PDF “Historia del texto” de la SCJN para los 136 artículos y extraer las versiones históricas de cada uno.

**Patrón de URL:**
```
https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-XXX.pdf
https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-XXX_2.pdf
```

### Código para Colab (136 artículos)

```python
!pip install -q pymupdf requests

import pymupdf
import requests
import json
import os
import re
import time

os.makedirs("scjn_pdfs", exist_ok=True)
os.makedirs("historial", exist_ok=True)

def try_download(num):
    padded = f"{num:03d}"
    for suffix in ["", "_2"]:
        url = f"https://www.scjn.gob.mx/sites/default/files/cpeum/documento/CPEUM-{padded}{suffix}.pdf"
        try:
            r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200 and "pdf" in r.headers.get("content-type", "").lower():
                path = f"scjn_pdfs/{padded}.pdf"
                with open(path, "wb") as f:
                    f.write(r.content)
                return path, url
        except Exception:
            pass
    return None, None

# Descargar los 136
log = []
for n in range(1, 137):
    path, url = try_download(n)
    log.append({"numero": n, "ok": path is not None, "url": url})
    print(f"Art. {n:3d}: {'OK' if path else 'FALLÓ'}")
    time.sleep(0.4)  # no saturar

ok = sum(1 for x in log if x["ok"])
print(f"\nDescargados: {ok}/136")
with open("historial/descarga_log.json", "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print("Log guardado en historial/descarga_log.json")
print("Si muchos fallan, detente y reporta. No inventes URLs.")
```

### Qué entregar
1. `historial/descarga_log.json` con el resultado de los 136.
2. Cuántos se descargaron y cuántos fallaron.
3. Si la mayoría falla, detente. No inventes texto ni URLs.

Cuando entregues el log, el Coordinador decide si escalamos la extracción o si hace falta otro método.