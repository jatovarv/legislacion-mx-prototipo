# Brief — GPT
## Limpieza lote A (Arts. 2, 3, 16, 28, 73)

**Objetivo:** Separar el texto vigente de las notas de reforma en los artículos contaminados del lote A.

**Artículos:** 2, 3, 16, 28, 73

### Criterios
- Texto vigente por separado.
- Notas de reforma como metadato.
- No inventar texto.
- Confianza alta/media/baja por artículo.

Entrega el JSON con la estructura:
```json
{
  "numero": "2",
  "texto_vigente": "...",
  "notas_reforma": ["..."],
  "confianza": "alta"
}
```