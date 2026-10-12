# Brief cerrado — Claude Max
## Limpiar y completar la extracción del texto vigente de la CPEUM

**Contexto:** Ya extrajimos el texto vigente de 134 artículos del CPEUM.pdf (Cámara de Diputados). 123 salieron limpios. 11 están contaminados con decretos de reforma o transitorios.

**Archivos disponibles en el repo / entorno:**
- `/workspace/artifacts/cpeum-vigente-articulos.json` (extracción actual)
- `/workspace/artifacts/articulos/` (123 páginas HTML ya generadas)

**Artículos contaminados a limpiar:**  
2, 3, 16, 28, 73, 89, 107, 108, 109, 122, 123

### Qué hacer

1. Para cada artículo contaminado, localiza en el CPEUM.pdf el texto vigente real del artículo (no el decreto de reforma ni los transitorios).
2. Sustituye el texto en `cpeum-vigente-articulos.json`.
3. Regenera la página HTML correspondiente en `articulos/N.html` con el mismo formato que las 123 ya generadas (aviso de “Texto vigente. Historial en construcción.”).
4. Entrega un PR a `main` con:
   - `cpeum-vigente-articulos.json` actualizado
   - Las 11 páginas HTML corregidas
   - `sitemap.xml` actualizado con las 134 URLs

### Criterios
- El texto de cada artículo contaminado debe ser el texto vigente real, no el decreto.
- Las páginas deben seguir el mismo formato que las 123 existentes.
- No inventar texto. Si un artículo no se puede limpiar con certeza, márcalo y explica.

**Repo:** https://github.com/jatovarv/legislacion-mx-prototipo  
**Rama base:** `main`

Entrega el PR listo para revisión.