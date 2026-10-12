# Brief — Gemini Ultra (Colab)
## Extracción de historial desde 00_historia.pdf

**Objetivo:** Extraer el texto de cada `00_historia.pdf` del zip de la SCJN y generar un JSON por artículo con todas las versiones.

### Código para Colab

```python
!pip install -q pymupdf

import pymupdf
import json
import os
import zipfile
from google.colab import drive

# Montar Drive
drive.mount('/content/drive')

# Descomprimir
zip_path = "/content/drive/MyDrive/CPEUM_SCJN_Historial/cpeum_scjn.zip"
extract_path = "/content/cpeum_scjn"
os.makedirs(extract_path, exist_ok=True)

print("Descomprimiendo...")
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)
print("Listo.")

# Buscar todos los 00_historia.pdf
historias = []
for root, dirs, files in os.walk(extract_path):
    for f in files:
        if f == "00_historia.pdf":
            historias.append(os.path.join(root, f))

print(f"Encontrados: {len(historias)} archivos 00_historia.pdf")

# Extraer texto
resultados = []
for i, path in enumerate(historias):
    try:
        doc = pymupdf.open(path)
        texto = ""
        for page in doc:
            texto += page.get_text("text") + "\n"
        doc.close()
        
        # Inferir número de artículo desde la ruta
        partes = path.split("/")
        art = next((p for p in partes if p.startswith("Art_")), "desconocido")
        num = art.replace("Art_", "").lstrip("0") or "0"
        
        resultados.append({
            "numero": num,
            "ruta": path,
            "texto_completo": texto.strip(),
            "paginas": len(texto.split("\n")) if texto else 0,
            "caracteres": len(texto)
        })
        if (i+1) % 20 == 0:
            print(f"  {i+1}/{len(historias)}")
    except Exception as e:
        resultados.append({"numero": "?", "ruta": path, "error": str(e)})

print(f"\nExtraídos: {len([r for r in resultados if 'texto_completo' in r])}/{len(historias)}")

# Guardar
out = "/content/drive/MyDrive/CPEUM_SCJN_Historial/historial_completo.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)
print(f"JSON guardado: {out}")
```

### Qué entregar
1. Cuántos `00_historia.pdf` encontró.
2. Cuántos extrajo sin error.
3. El archivo `historial_completo.json`.

No intentes separar versiones todavía. Solo extrae el texto completo de cada PDF.