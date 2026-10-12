# Brief corregido — Gemini Ultra (Colab)
## Scraper SCJN — versión diagnóstica

**Problema:** El log anterior mostró 403 en todas las páginas. Necesitamos ver qué responde realmente el servidor.

### Código de diagnóstico

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.scjn.gob.mx/constitucion-politica-de-los-estados-unidos-mexicanos/articulos/339"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9",
}

r = requests.get(url, headers=headers, timeout=30)
print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('content-type')}")
print(f"Longitud: {len(r.text)}")
print("--- Primeros 500 caracteres ---")
print(r.text[:500])
print("--- Últimos 200 caracteres ---")
print(r.text[-200:])

# Buscar enlaces PDF aunque sea
soup = BeautifulSoup(r.text, "html.parser")
pdfs = [a.get("href") for a in soup.find_all("a", href=True) if ".pdf" in a.get("href", "").lower()]
print(f"\nEnlaces .pdf encontrados: {len(pdfs)}")
for p in pdfs[:5]:
    print(" ", p)
```

### Qué entregar
1. El status code y el content-type.
2. Los primeros 500 caracteres de la respuesta.
3. Cuántos enlaces .pdf encontró.
4. Si la respuesta es un bloqueo (captcha, access denied, etc.), pégalo.

Con eso ajustamos el scraper o buscamos otra vía.