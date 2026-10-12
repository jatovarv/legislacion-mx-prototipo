# Brief cerrado — Gemini Ultra (Colab)
## Scraper SCJN — Descarga de PDFs de decretos por artículo

**Objetivo:** Desde las páginas de Títulos de la SCJN, descargar todos los PDFs de decretos de reforma de la CPEUM.

**Portal:** https://www.scjn.gob.mx/constitucion-politica-de-los-estados-unidos-mexicanos

### Código para Colab

```python
!pip install -q requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import os
import time
import json
from urllib.parse import urljoin

BASE = "https://www.scjn.gob.mx"
TITULOS = range(339, 349)  # páginas de títulos

os.makedirs("scjn_pdfs", exist_ok=True)

def get_page(n):
    url = f"{BASE}/constitucion-politica-de-los-estados-unidos-mexicanos/articulos/{n}"
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"Error {n}: {e}")
    return None

def extract_pdfs(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    pdfs = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            full = urljoin(page_url, href)
            pdfs.append(full)
    return pdfs

all_pdfs = set()
log = []

for n in TITULOS:
    print(f"Página {n}...")
    html = get_page(n)
    if not html:
        log.append({"pagina": n, "ok": False})
        continue
    pdfs = extract_pdfs(html, f"{BASE}/constitucion-politica-de-los-estados-unidos-mexicanos/articulos/{n}")
    print(f"  {len(pdfs)} PDFs")
    all_pdfs.update(pdfs)
    log.append({"pagina": n, "ok": True, "pdfs": len(pdfs)})
    time.sleep(0.5)

print(f"\nTotal PDFs únicos: {len(all_pdfs)}")

# Descargar (limitado para no saturar; ajustar si hace falta)
descargados = 0
for i, url in enumerate(list(all_pdfs)[:50]):  # primer lote
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            name = url.split("/")[-1].split("?")[0]
            with open(f"scjn_pdfs/{name}", "wb") as f:
                f.write(r.content)
            descargados += 1
    except Exception:
        pass
    if (i+1) % 10 == 0:
        print(f"  {i+1} procesados")
    time.sleep(0.3)

print(f"\nDescargados: {descargados}")

with open("scjn_pdfs/log.json", "w", encoding="utf-8") as f:
    json.dump({"paginas": log, "total_unicos": len(all_pdfs), "descargados": descargados}, f, indent=2)

print("Log guardado.")
```

### Qué entregar
1. Cuántos PDFs únicos encontró.
2. Cuántos descargó.
3. El archivo `scjn_pdfs/log.json`.
4. Si hay errores de red, reportarlos.

Cuando tengas el log, el Coordinador decide si escalamos la descarga o si hace falta otro método.