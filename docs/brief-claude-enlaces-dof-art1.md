# Brief cerrado — Claude Max
## Añadir hipervínculos al DOF en las versiones del Artículo 1 CPEUM

**Repo:** https://github.com/jatovarv/legislacion-mx-prototipo  
**Rama base:** `main`  
**Objetivo:** Que en el historial de cada versión del Artículo 1o. aparezca un enlace claro al decreto correspondiente del DOF (o fuente oficial equivalente) para poder cotejar.

### Enlaces DOF confirmados (usar exactamente estos)

| Versión | Fecha publicación | URL |
|---------|-------------------|-----|
| Original (v1) | 1917-02-05 | https://www.dof.gob.mx/Constitucion1917/constitucion_1917.pdf |
| Post 14-08-2001 (v2) | 2001-08-14 | https://dof.gob.mx/nota_detalle.php?codigo=762221&fecha=14/08/2001 |
| Post 04-12-2006 (v3) | 2006-12-04 | https://www.diputados.gob.mx/LeyesBiblio/ref/dof/CPEUM_ref_169_04dic06.pdf |
| Vigente post 10-06-2011 (v4) | 2011-06-10 | https://dof.gob.mx/nota_detalle.php?codigo=5194486&fecha=10/06/2011 |

### Qué hacer

1. En `cpeum.json`, cada objeto de `articulos["1"].versiones` ya debe tener (o añádelo si no está) los campos:
   - `dof_url`: la URL de la tabla anterior
   - `dof_etiqueta`: `"Ver decreto en el DOF"`

2. En el HTML (o en el JS que renderiza el panel de versión), cuando se muestre una versión del Artículo 1, añadir un enlace visible y accesible:
   - Texto: “Ver decreto en el DOF”
   - `href` = `dof_url` de esa versión
   - `target="_blank"` y `rel="noopener"`
   - Colocarlo junto a la metadata de la versión (publicación / vigencia), no escondido.

3. No modificar los textos legales. No inventar enlaces. Solo el Artículo 1 tiene estos campos por ahora.

4. Regenerar `index.html` si usas `build.py`, o editar el JS embebido de forma que lea `dof_url` si existe.

5. Abrir un PR a `main` con título claro:  
   `Añade hipervínculos al DOF en el historial del Artículo 1 CPEUM`

### Criterios de aceptación

- En el Artículo 1, al abrir el historial y seleccionar cualquier versión, aparece el enlace al DOF.
- Los cuatro enlaces apuntan a las URLs de la tabla.
- El resto del prototipo (árbol, fecha, avisos de prototipo) sigue funcionando igual.
- No se introducen textos legales inventados.

### Notas

- El enlace de 2006 usa el PDF oficial de la Cámara de Diputados porque es la fuente más estable localizada del decreto.
- Los otros tres son notas directas del DOF.
- Después de este PR, el siguiente bloque natural es páginas estáticas por artículo para SEO.

Entrega el PR listo para revisión.