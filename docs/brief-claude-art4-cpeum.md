# Brief cerrado — Claude Max
## Golden case + página estática del Artículo 4 CPEUM

**Repo:** https://github.com/jatovarv/legislacion-mx-prototipo  
**Rama base:** `main`  
**Objetivo:** Avanzar el segundo artículo real verificado (después del Art. 1) para SEO y demostración.

### Qué hacer

1. **Golden case del Artículo 4**  
   - Reconstruir las versiones verificables del Artículo 4o. de la CPEUM desde fuentes oficiales (SCJN cronología + DOF).  
   - Incluir al menos: texto original 1917 + reformas posteriores documentadas.  
   - Cada versión debe tener: texto íntegro, fecha de publicación, fecha de vigencia, y `dof_url` si se localiza.  
   - Marcar el artículo como `"estado": "verificado"` en `cpeum.json`.

2. **Página estática**  
   - El `build.py` ya genera páginas para artículos verificados.  
   - Asegúrate de que al marcar el Art. 4 como verificado se genere `articulos/4.html`.  
   - La página debe seguir el mismo patrón que `articulos/1.html` (texto vigente, versiones históricas en bloques plegables si están verificadas, enlace DOF).

3. **Sitemap**  
   - Actualizar `sitemap.xml` para incluir la nueva URL.

### Criterios de aceptación

- Artículo 4 marcado como verificado en `cpeum.json`.
- Existe `articulos/4.html` con texto vigente íntegro.
- Versiones históricas solo si están verificadas con fuente.
- Enlaces DOF cuando existan.
- SPA actual sigue funcionando.
- PR a `main` con título:  
  `Añade Artículo 4 CPEUM verificado + página estática`

### Notas

- No inventar textos ni fechas.  
- Si alguna versión no tiene fuente clara, dejarla fuera o marcarla como pendiente.  
- Prioridad: exactitud sobre cantidad.

Entrega el PR listo para revisión.