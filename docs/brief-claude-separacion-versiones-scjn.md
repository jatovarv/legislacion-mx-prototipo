# Brief — Claude Max
## Separación correcta de versiones del historial SCJN

**Contexto:** Colab extrajo el texto de los 159 archivos 00_historia.pdf. Los intentos de separación por regex fallaron porque la SCJN estructura cada versión con encabezados de nivel superior, no con notas parentéticas.

**Objetivo:** Definir y aplicar la regla de corte correcta para que Art. 1 tenga 4 versiones y Art. 4 tenga 25.

### Qué hacer
1. Analizar la estructura real de los PDF de la SCJN (encabezados "Texto Original", "Texto derivado de la reforma...", "Texto vigente").
2. Proponer el script de separación que corte solo en esos encabezados.
3. Validar que Art. 1 = 4 y Art. 4 = 25 antes de aplicar al lote.
4. Entregar el script y el resultado de la validación.

### Criterios
- No inventar textos.
- Cortar solo en encabezados de nivel superior.
- Abortar si Arts. 1 y 4 no cumplen el conteo esperado.