# Brief — Gemini Ultra (Colab)
## Separación de versiones del historial SCJN

**Objetivo:** A partir de `historial_completo.json`, separar cada artículo en versiones históricas usando las fechas del DOF como fronteras.

### Código para Colab

```python
import json
import re
from google.colab import drive

drive.mount('/content/drive')

with open("/content/drive/MyDrive/CPEUM_SCJN_Historial/historial_completo.json", encoding="utf-8") as f:
    datos = json.load(f)

print(f"Artículos: {len(datos)}")

# Patrón de fecha DOF (multilínea)
patron = re.compile(
    r"D\s*\.?\s*O\s*\.?\s*F\s*\.?\s*\n\s*(\d{1,2})\s+de\s+(\w+)\s+de\s*\n\s*(\d{4})",
    re.IGNORECASE
)

meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

def normalizar_fecha(d, m, a):
    mes = meses.get(m.lower(), "00")
    return f"{a}-{mes}-{int(d):02d}"

resultados = []
for art in datos:
    texto = art.get("texto_completo", "")
    matches = list(patron.finditer(texto))
    versiones = []
    for i, m in enumerate(matches):
        inicio = m.start()
        fin = matches[i+1].start() if i+1 < len(matches) else len(texto)
        versiones.append({
            "fecha_dof": normalizar_fecha(*m.groups()),
            "texto": texto[inicio:fin].strip()
        })
    resultados.append({
        "numero": art.get("numero"),
        "total_versiones": len(versiones),
        "versiones": versiones
    })

print(f"Total versiones: {sum(r['total_versiones'] for r in resultados)}")

out = "/content/drive/MyDrive/CPEUM_SCJN_Historial/versiones_separadas.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)
print(f"Guardado: {out}")
```

### Qué entregar
1. Cuántos artículos procesó.
2. Total de versiones encontradas.
3. Confirmar que `versiones_separadas.json` se guardó.
4. Si algún artículo queda con 0 versiones, reportarlo.