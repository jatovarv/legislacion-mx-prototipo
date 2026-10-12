# Brief cerrado — Claude Max
## Corrección puntual en el PR #6

**Contexto:** El PR #6 está aprobado en lo esencial, pero el Coordinador detectó defectos de presentación que deben corregirse antes del merge.

**PR:** https://github.com/jatovarv/legislacion-mx-prototipo/pull/6

### Qué corregir

1. **Fracciones/incisos pegados** (10 casos en 8 artículos):  
   Arts. 3, 20, 38, 73, 79, 95, 103, 122.  
   Separar las fracciones e incisos que quedaron unidos cuando entre ellas había una nota de reforma.

2. **“lecto- escritura”** en el Art. 3 → corregir a “lecto-escritura”.

3. Regenerar los `articulos/N.html` afectados.

### Criterios
- No cambiar el texto legal más allá de separar fracciones y corregir el guion.
- Conservar las marcas `(sic DOF …)`.
- No inventar texto.
- Abrir un commit en la misma rama del PR #6 (o un PR de seguimiento si es más limpio).

Cuando esté listo, avisa. El Coordinador revisa el commit.