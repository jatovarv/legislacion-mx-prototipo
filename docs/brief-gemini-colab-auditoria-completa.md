# Brief — Gemini Ultra (Colab)
## Auditoría completa + muestra + cobertura (todo en uno)

**Objetivo:** En una sola ejecución, Colab debe:
1. Contar artículos con número vs "desconocido".
2. Mostrar las fechas de Arts. 1, 4, 73 y 123.
3. Listar cuántos artículos tienen más de 1 versión.
4. Generar un resumen JSON con la cobertura.

### Código para Colab

```python
import json
from collections import Counter
from google.colab import drive

drive.mount('/content/drive')

with open("/content/drive/MyDrive/CPEUM_SCJN_Historial/versiones_separadas.json", encoding="utf-8") as f:
    datos = json.load(f)

print(f"Total registros: {len(datos)}")

# 1) Contar número vs desconocido
con_numero = [r for r in datos if r.get("numero") and str(r["numero"]).isdigit()]
sin_numero = [r for r in datos if not r.get("numero") or not str(r["numero"]).isdigit()]
print(f"Con número: {len(con_numero)}")
print(f"Sin número (desconocido/transitorios): {len(sin_numero)}")

# 2) Distribución de versiones
dist = Counter(r["total_versiones"] for r in con_numero)
print(f"\nDistribución de versiones (artículos numerados):")
for n, c in sorted(dist.items()):
    print(f"  {n} versiones: {c} artículos")

# 3) Muestra de Arts. clave
print("\n=== Muestras ===")
for num in ["1", "4", "73", "123"]:
    art = next((r for r in datos if str(r.get("numero")) == num), None)
    if art:
        fechas = [v["fecha_dof"] for v in art["versiones"]]
        print(f"Art. {num}: {art['total_versiones']} versiones → {fechas[:8]}{'...' if len(fechas)>8 else ''}")
    else:
        print(f"Art. {num}: NO ENCONTRADO")

# 4) Resumen de cobertura
resumen = {
    "total_registros": len(datos),
    "con_numero": len(con_numero),
    "sin_numero": len(sin_numero),
    "total_versiones": sum(r["total_versiones"] for r in datos),
    "articulos_con_historial": sum(1 for r in con_numero if r["total_versiones"] > 1),
    "articulos_sin_historial": sum(1 for r in con_numero if r["total_versiones"] <= 1),
    "muestras": {}
}
for num in ["1", "4", "73", "123"]:
    art = next((r for r in datos if str(r.get("numero")) == num), None)
    if art:
        resumen["muestras"][num] = {
            "versiones": art["total_versiones"],
            "fechas": [v["fecha_dof"] for v in art["versiones"]]
        }

out = "/content/drive/MyDrive/CPEUM_SCJN_Historial/resumen_cobertura.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(resumen, f, ensure_ascii=False, indent=2)
print(f"\nResumen guardado: {out}")
print(json.dumps(resumen, ensure_ascii=False, indent=2))
```

### Qué entregar
1. La salida completa del script.
2. Confirmar que `resumen_cobertura.json` se guardó.
3. Si algún artículo clave (1, 4, 73, 123) no aparece, decirlo.