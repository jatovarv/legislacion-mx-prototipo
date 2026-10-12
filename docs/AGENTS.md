# Prompt Maestro de Decisión — Plataforma de Legislación Mexicana
## Cómo elegir qué IA hace qué (y cuándo usar el Coordinador)

**Objetivo:** Avanzar lo más rápido posible hacia un sitio público indexable y monetizable, usando las fortalezas de cada IA y evitando cuellos de botella.

### Jerarquía de decisión

1. **Grok Heavy (yo)**  
   - Coordinación general, revisión final, merges, actualización de `sources_registry.json`, decisiones de estrategia.  
   - No hace extracción masiva de PDFs si otra IA puede hacerlo más rápido.

2. **Claude Max**  
   - Mejor para: extracción precisa de textos legales desde PDF, generación de páginas estáticas, PRs limpios, golden cases.  
   - Usar cuando se necesita exactitud y entrega lista para mergear.

3. **GPT (ChatGPT Pro 500)**  
   - Mejor para: investigación de fuentes, cierre de textos vigentes con discrepancias, genealogías, JSON de registro.  
   - Usar cuando hay conflicto entre portales oficiales o se necesita dictamen documentado.

4. **Gemini Ultra**  
   - Mejor para: **procesamiento masivo**. Tiene Colab + H100.  
   - Usar cuando haya que descargar o procesar cientos de PDFs (historial SCJN, Gacetas, DOF).  
   - Si el chat no puede descargar, pedirle que lo haga en Colab y entregue el resultado.  
   - Ideal para “una noche de automatización” del historial completo.

5. **Bot Coordinador**  
   - Revisa entregas contra checklists.  
   - Emite veredicto formal (Aprobado / Ajustes necesarios / Rechazado).  
   - No hace el trabajo; valida que el trabajo esté listo para mergear.

### Reglas de asignación

| Tipo de tarea | IA preferida | Alternativa |
|---------------|--------------|-------------|
| Extraer 1–10 artículos con exactitud | Claude | GPT |
| Extraer 100+ artículos o PDFs en lote | **Gemini (Colab)** | Claude (si es poco) |
| Investigar fuentes y discrepancias | GPT | Claude |
| Generar páginas estáticas + sitemap | Claude | Grok (si es pequeño) |
| Vigilancia DOF / scripts de actualización | Gemini o Grok | Claude |
| Revisión de calidad antes de merge | Coordinador | Grok |

### Regla de oro
- Si la tarea es **masiva** (cientos de PDFs, miles de páginas) → **Gemini en Colab**.  
- Si la tarea es **precisa y entregable** (PR listo) → **Claude**.  
- Si hay **duda o conflicto de fuentes** → **GPT**.  
- Siempre que haya entrega → **Coordinador** revisa antes de mergear.

### Estado actual del proyecto
- Art. 1 y Art. 4: verificados con historial.
- PR #6 (Claude): 136 páginas del texto vigente listas para merge.
- Historial de los 134 restantes: pendiente de automatización masiva (candidato ideal para Gemini + Colab).
- Vigilancia DOF: esqueleto mergeado, cron desactivado.

Este prompt debe consultarse antes de asignar cualquier tarea nueva.