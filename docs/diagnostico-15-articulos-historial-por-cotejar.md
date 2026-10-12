# Diagnóstico de 15 artículos con historial por cotejar

**Fecha de revisión:** 12 de octubre de 2026  
**Repositorio:** `jatovarv/legislacion-mx-prototipo`  
**Fuente de trabajo:** `cpeum.json`, metadatos del historial SCJN ya incorporados y texto vigente del consolidado de la Cámara de Diputados.

> Todo el material está en el repositorio.

## Alcance

Este documento revisa los siguientes 15 artículos en estado `historial_parcial`:

`2, 3, 10, 20, 22, 35, 72, 82, 99, 100, 107, 109, 116, 122 y 123`.

Los artículos **53, 56 y 73 no forman parte de este lote**; permanecen identificados por separado.

No se reproduce ni se reconstruye texto normativo. El diagnóstico compara únicamente metadatos, fechas, longitud y huella SHA-256 de los cuerpos ya existentes en el repositorio.

## Criterio de decisión

### A. Pendiente de PDF actualizado o reconstrucción documental

Se aplica cuando la última fotografía histórica de la SCJN es anterior a la reforma que sustenta el texto vigente de la Cámara. El consolidado permite mostrar el texto actual, pero no basta por sí solo para reconstruir con seguridad todas las versiones intermedias.

**Acción:** conservar la versión vigente de la Cámara para consulta, mantener `estado: historial_parcial` y esperar un PDF actualizado de la SCJN o reconstruir las versiones faltantes con los decretos individuales del DOF.

### B. Corregir el cierre con el consolidado de la Cámara

Se aplica cuando SCJN y Cámara atribuyen la última versión a la misma fecha, pero el cuerpo extraído no coincide, o cuando la extracción SCJN dejó un encabezado sin fecha y un cuerpo manifiestamente anómalo.

**Acción:** usar como versión vigente canónica el texto ya extraído del consolidado de la Cámara, conservar las versiones históricas anteriores y revisar o aislar únicamente la última extracción SCJN defectuosa.

La diferencia de caracteres se informa como señal técnica de extracción. **No demuestra por sí sola una diferencia normativa.**

## Resultado ejecutivo

| Categoría | Artículos | Total |
|---|---|---:|
| A — PDF SCJN anterior o historial incompleto | 2, 10, 20, 22, 82, 116, 122 | 7 |
| B — Corregir última extracción con Cámara | 3, 35, 72, 99, 100, 107, 109, 123 | 8 |
| **Total** |  | **15** |

## Diagnóstico por artículo

| Art. | Última versión SCJN identificada | Versión vigente Cámara | Causa concreta | Propuesta |
|---:|---|---|---|---|
| **2** | 22-05-2015 | 30-09-2024 | El historial SCJN termina en 2015. Las notas del consolidado registran reformas posteriores de 2016, 2019 y 2024; esas versiones intermedias no están reconstruidas en el historial actual. | **A.** Mantener el texto vigente de Cámara, pero dejar el historial pendiente de PDF SCJN actualizado o de reconstrucción con decretos DOF. |
| **3** | 20-12-2024 | 20-12-2024 | La fecha coincide, pero las huellas no: la extracción SCJN tiene 10,709 caracteres y Cámara 10,770, diferencia de **+61** caracteres en Cámara. No hay una reforma posterior que explique el desfase. | **B.** Sustituir el cierre vigente por el texto ya disponible de Cámara y revisar sólo la última extracción SCJN. |
| **10** | 22-10-1971 | 26-03-2019 | El PDF histórico utilizado termina en 1971 y el consolidado registra una reforma posterior en 2019. Falta una versión histórica completa. | **A.** Conservar Cámara como texto vigente y dejar pendiente la incorporación documental de la reforma de 2019. |
| **20** | 14-07-2011 | 15-09-2024 | La fotografía SCJN termina en 2011; el consolidado incorpora una reforma de 2024 no presente como versión histórica SCJN. | **A.** Esperar PDF actualizado o reconstruir la versión de 2024 desde el decreto DOF antes de cerrar el historial. |
| **22** | 27-05-2015 | 14-03-2019 | La última versión SCJN precede a la reforma de 2019 que sustenta el texto vigente. | **A.** Mantener el consolidado como vigente y dejar pendiente la versión histórica de 2019. |
| **35** | Fecha no extraída | 02-06-2026 | El último bloque SCJN quedó con `fecha_pendiente: true`, `vigencia_desde: null` y `vigencia_hasta_indeterminada: true`. Además, el cuerpo extraído tiene 17,871 caracteres frente a 8,884 en Cámara, diferencia de **−8,987** caracteres en Cámara. La evidencia apunta a un corte o arrastre defectuoso, no a una fecha histórica confiable. | **B.** Usar Cámara para el texto vigente y aislar el bloque SCJN sin fecha para reextracción. No asignarle por inferencia la fecha 02-06-2026. |
| **72** | 17-08-2011 | 17-08-2011 | La fecha coincide, pero Cámara tiene **22** caracteres más y una huella distinta. No existe una reforma posterior en el registro que justifique otra versión. | **B.** Corregir la última versión con el consolidado de Cámara y conservar intactas las anteriores. |
| **82** | 01-04-2025 | 07-10-2026 | La SCJN llega a 2025; el consolidado incorpora la reforma de 07-10-2026. El historial no contiene todavía ese evento como versión histórica verificada. | **A.** Mantener Cámara como vigente y esperar PDF actualizado o integrar el decreto DOF de 2026 mediante cotejo independiente. |
| **99** | 15-09-2024 | 15-09-2024 | Misma fecha, pero Cámara tiene **191** caracteres menos y una huella distinta. El desfase corresponde al cierre extraído, no a una reforma posterior. | **B.** Adoptar el cuerpo vigente de Cámara y revisar la depuración del último bloque SCJN. |
| **100** | 02-06-2026 | 02-06-2026 | Misma fecha, pero Cámara tiene **871** caracteres menos y una huella distinta. No hay salto cronológico que explique una versión adicional. | **B.** Corregir el cierre con Cámara; revisar encabezados, notas y posibles residuos editoriales en la extracción SCJN. |
| **107** | 31-10-2024 | 31-10-2024 | Misma fecha, con **62** caracteres menos en Cámara y huella distinta. Es una diferencia de extracción de la última fotografía. | **B.** Usar Cámara como versión vigente y cotejar sólo el bloque final SCJN. |
| **109** | 27-05-2015 | 27-05-2015 | Misma fecha, con una diferencia mínima de **7** caracteres menos en Cámara y huella distinta. | **B.** Normalizar y corregir la última versión con Cámara; el resto del historial puede conservarse. |
| **116** | 02-06-2026 | 07-10-2026 | La última fotografía SCJN antecede a la reforma de 07-10-2026. | **A.** Mantener Cámara como vigente y dejar pendiente la nueva versión histórica hasta contar con PDF actualizado o decreto DOF cotejado. |
| **122** | 02-06-2026 | 07-10-2026 | La última fotografía SCJN antecede a la reforma de 07-10-2026. | **A.** Mantener Cámara como vigente y dejar pendiente la versión posterior para reconstrucción oficial. |
| **123** | 03-03-2026 | 03-03-2026 | Misma fecha, pero Cámara tiene **77** caracteres menos y una huella distinta. No hay una reforma posterior en el registro. | **B.** Corregir el cierre con el consolidado de Cámara y revisar únicamente la extracción SCJN de esa fecha. |

## Hechos confirmados e inferencias

### Hechos confirmados en el repositorio

- Los 15 artículos están marcados como `historial_parcial`.
- Cada uno contiene una versión vigente proveniente del consolidado de la Cámara de Diputados.
- En siete artículos, la fecha de la versión de Cámara es posterior a la última versión SCJN identificada.
- En siete artículos, SCJN y Cámara comparten fecha pero difieren en longitud y SHA-256.
- En el artículo 35, la última extracción SCJN carece de fecha utilizable y está expresamente marcada como pendiente e indeterminada.

### Inferencias técnicas

- Cuando la Cámara tiene una fecha posterior, se infiere que el PDF histórico disponible no cubre la última reforma o que el lote usado quedó desactualizado.
- Cuando la fecha coincide y sólo difiere el cuerpo, se infiere un problema de extracción, limpieza o inclusión de material editorial. La afirmación no sustituye un cotejo jurídico palabra por palabra.
- En el artículo 35, la combinación de fecha ausente y diferencia de tamaño permite clasificar provisionalmente el problema como extracción defectuosa; no permite inferir la fecha del bloque SCJN.

## Orden recomendado de trabajo

1. **Correcciones directas con Cámara:** 109, 72, 3, 107, 123, 99, 100 y 35.
2. **Actualización documental reciente:** 82, 116 y 122, todos afectados por la reforma de 07-10-2026.
3. **Historiales con brechas antiguas o amplias:** 2, 10, 20 y 22.
4. Tras cada corrección, ejecutar validación estructural y comparación del texto vigente contra `CPEUM.pdf` antes de cambiar `estado` a `verificado`.

## Fuentes utilizadas

- `cpeum.json` del repositorio.
- Metadatos `fuente_historial`, `encabezado_scjn`, `notas_scjn` y banderas de vigencia ya almacenadas.
- Texto vigente y `notas_camara` extraídos del consolidado oficial de la Cámara de Diputados: `https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf`.

Este documento es un diagnóstico de datos y procedencia. No sustituye el cotejo con los decretos del DOF ni certifica texto normativo.