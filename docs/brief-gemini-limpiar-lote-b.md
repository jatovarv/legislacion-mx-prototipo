# Brief — Gemini Ultra
## Limpieza lote B (Arts. 89, 107, 108, 109, 122, 123)

**Objetivo:** Separar el texto vigente de las notas de reforma en los artículos contaminados del lote B.

**Artículos:** 89, 107, 108, 109, 122, 123

### Criterios
- Texto vigente por separado.
- Notas de reforma como metadato.
- No inventar texto.
- Confianza alta/media/baja por artículo.

Entrega el JSON con la estructura:
```json
{
  "numero": "89",
  "texto_vigente": "...",
  "notas_reforma": ["..."],
  "confianza": "alta"
}
```