# Brief — Colab
## Separación de versiones v2

**Objetivo:** Ajustar el regex para capturar fechas DOF multilínea y cortar después del delimitador.

### Cambios
- Detectar encabezados D.O.F. y notas parentéticas.
- Cortar con m.end().
- Deduplicar solo consecutivos idénticos.