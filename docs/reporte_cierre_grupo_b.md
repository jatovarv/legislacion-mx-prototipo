# Cierre del historial del Grupo B (Arts. 3, 35, 72, 99, 100, 107, 109, 123)

Brief: cerrar el historial de los 8 artículos del Grupo B del diagnóstico (`diagnostico-15-articulos-historial-por-cotejar.md`) usando el texto vigente de la Cámara de Diputados como última versión, marcando en notas la diferencia de extracción sin inventar texto. Script reproducible: `cerrar_historial_grupo_b.py` (corrido una vez sobre el `cpeum.json` de `main`); salida mecánica en `reporte_cierre_grupo_b.json`.

## Método

Para cada artículo se tomó el último bloque del PDF de la SCJN (misma fecha que la última reforma del consolidado) y se le aplicó **sólo** la corrección mecánica descrita en la tabla (retirar una línea repetida, un párrafo duplicado, una anotación editorial o una marca «x»; nunca añadir palabras). El resultado debe coincidir palabra por palabra con el texto de la Cámara bajo la normalización de cotejo `comparable()` del integrador (misma que en PR #8/#11; se amplió para ignorar también la marca «(sic DD-MM-YYYY)» de la Cámara). Si no coincide, el script aborta y el artículo no se cierra. Siete artículos pasaron; el Art. 35 no se cierra como verificado (ver abajo).

En los 7 cerrados, el par «Última versión SCJN (cerrada el mismo día)» + «Vigente (consolidado Cámara)» se sustituye por **una sola versión vigente**: texto de la Cámara tal cual, fecha de publicación (idéntica en ambas fuentes), notas y encabezado del bloque SCJN, y `nota_extraccion` con la diferencia. Estado → `verificado`, con la misma forma que los demás artículos verificados.

## Resultado por artículo

| Art. | Última reforma | Versiones | Diferencia del bloque SCJN (documentada en `nota_extraccion`) | Resultado |
|---|---|---|---|---|
| 3 | 2024-12-20 | 15 | Único desfase: la raya del inciso b) de la fracción II («–sin hostilidades ni exclusivismos– atenderá») salió como guion con espacios en el PDF de la SCJN («exclusivismos - atenderá»). Diferencia tipográfica. | Verificado |
| 72 | 2011-08-17 | 3 | Único desfase: el numeral repetido «I (sic).-» del apartado final salió con guion en el PDF de la SCJN; la Cámara lo imprime «I (sic DOF 17-08-2011).». Diferencia tipográfica. | Verificado |
| 99 | 2024-09-15 | 8 | Único desfase: el párrafo «El personal del Tribunal regirá sus relaciones de trabajo…» aparece dos veces en el bloque SCJN (repetido en un corte de página: una vez suelto y otra como inicio del párrafo que sigue con «El ingreso, formación…»). La Cámara lo trae una sola vez. Duplicado de extracción. | Verificado |
| 100 | 2026-06-02 | 9 | Único desfase: la línea «El personal del Tribunal regirá … reglas especiales y excepciones» (párrafo del Art. 99, truncado) se coló 5 veces en el bloque SCJN como línea de corte de página, partiendo frases por la mitad. No forma parte del Art. 100. Retirada, el bloque coincide con la Cámara. | Verificado |
| 107 | 2024-10-31 | 19 | Único desfase: la fracción XVIII derogada trae en el PDF de la SCJN la anotación editorial «(REPUBLICADA DEROGACIÓN, D.O.F. 6 DE JUNIO DE 2011)»; la Cámara imprime «XVIII. Se deroga.». Anotación, no texto normativo. | Verificado |
| 109 | 2015-05-27 | 3 | Único desfase: tres párrafos sueltos con una «x» (marca del PDF de la SCJN en cortes de página, sin correlato en el texto). Retirados, el bloque coincide con la Cámara. | Verificado |
| 123 | 2026-03-03 | 33 | Únicos desfases: el numeral repetido «XI (SIC).-» del apartado B salió con guion en el PDF de la SCJN (la Cámara: «XI (sic 05-12-1960).») y «XIII bis.-» frente a «XIII bis.». Diferencias tipográficas. | Verificado |
| 35 | 2026-06-02 (Cámara) | 7 | Último bloque SCJN sin fecha legible y fusionado: contiene dos textos separados por la etiqueta «Texto vigente publicado en el D.O.F. el 02 de junio de 2026» (duplicada/sobreimpresa). La segunda parte coincide con el consolidado bajo la normalización de cotejo; la primera no tiene fecha legible. No se fecha por inferencia ni se separa. | **Pendiente**: re-extraer por coordenadas desde `Art_035_00_historia.pdf` (v2 y v4 también son bloques fusionados). Sigue `historial_parcial`; el texto vigente es el de la Cámara. |

## Limpiezas en versiones anteriores (mismo defecto, documentadas en cada versión)

- **Art. 100, v5–v8**: la línea «El personal del Tribunal regirá … reglas especiales y excepciones» (párrafo del Art. 99, truncado) aparece como línea de corte de página en todas las versiones desde v5, partiendo frases por la mitad («…estarán a / [línea] / cargo del Consejo…»). Se retiró (cadena exacta, párrafo suelto: 2, 1, 3 y 4 apariciones) y se reunieron las mitades de cada frase. En v5 apareció además el fragmento «31 de diciembre de 1994», resto de la etiqueta de la SCJN; se retiró del cuerpo y se dejó constancia (coincide con la `fecha_sugerida` de esa versión, que sigue sin confirmarse).
- **Art. 99, v7**: el párrafo «El personal del Tribunal regirá…» quedó partido por un corte de página («… excepciones» / «que señale la ley.»); se reunieron sus mitades.
- Todas llevan `extraccion_pendiente: true` (cotejo con el PDF pendiente). No se añadió ninguna palabra.

## Hallazgo adicional: 34 bloques fusionados (marcados, no separados)

Al revisar el Grupo B apareció un defecto general del separador lineal (Colab): versiones cuyo cuerpo contiene una etiqueta de la SCJN («Texto derivado de la reforma…», «Texto vigente…») a mitad del texto, es decir, **un bloque que reúne dos o tres versiones** (longitud ~2× la de sus vecinas). Son 34 versiones en 21 artículos, 16 de ellas en artículos ya `verificado` (el estado sólo garantiza que la versión vigente coincide con la Cámara). Se marcaron todas con `nota_extraccion` + `extraccion_pendiente` (la interfaz muestra «extracción por cotejar»); **no se separaron** para no fechar bloques por inferencia: la separación correcta exige el PDF de cada artículo y el extractor por coordenadas (`extraer_historia_scjn_pdf.py`, probado en Arts. 53/56/73).

| Art. | Estado | Bloques fusionados |
|---|---|---|
| 2 | historial_parcial | v3 (2015-05-22; 5 versiones) |
| 10 | historial_parcial | v2 (1971-10-22; 2 versiones) |
| 16 | verificado | v4 (1996-07-03; 2 versiones) |
| 20 | historial_parcial | v9 (2011-07-14; 2 versiones) |
| 22 | historial_parcial | v5 (2005-12-09; 2 versiones), v6 (2015-05-27; 2 versiones) |
| 26 | verificado | v2 (1983-02-03; 2 versiones) |
| 27 | verificado | v10 (1960-12-29; 2 versiones), v17 (1992-01-06; 2 versiones), v18 (2011-10-13; 2 versiones) |
| 28 | verificado | v3 (1983-02-03; 2 versiones), v8 (2013-12-20; 2 versiones) |
| 35 | historial_parcial | v2 (1990-04-06; 2 versiones), v4 (2014-02-10; 2 versiones), v6 (sin fecha; 2 versiones) |
| 74 | verificado | v11 (1993-10-25; 2 versiones) |
| 94 | verificado | v8 (1982-12-28; 2 versiones), v15 (2021-03-11; 2 versiones) |
| 95 | verificado | v4 (2007-08-02; 2 versiones) |
| 96 | verificado | v2 (1928-08-20; 2 versiones) |
| 97 | verificado | v7 (1987-08-10; 3 versiones), v8 (2007-11-13; 2 versiones) |
| 98 | verificado | v2 (1928-08-20; 2 versiones) |
| 99 | verificado | v7 (2014-02-10; 3 versiones) |
| 107 | verificado | v1 (1917-02-05; 2 versiones), v4 (1967-10-25; 2 versiones), v14 (2011-06-06; 2 versiones) |
| 108 | verificado | v3 (1994-12-31; 2 versiones) |
| 116 | historial_parcial | v14 (2015-05-27; 2 versiones) |
| 122 | historial_parcial | v10 (2012-08-09; 2 versiones) |
| 123 | verificado | v12 (1974-12-31; 2 versiones), v14 (1978-01-09; 2 versiones), v23 (2008-06-18; 2 versiones), v24 (2014-06-17; 2 versiones) |

PDF necesarios para el siguiente lote (re-extracción por coordenadas): Art_002_00_historia.pdf, Art_010_00_historia.pdf, Art_016_00_historia.pdf, Art_020_00_historia.pdf, Art_022_00_historia.pdf, Art_026_00_historia.pdf, Art_027_00_historia.pdf, Art_028_00_historia.pdf, Art_035_00_historia.pdf, Art_074_00_historia.pdf, Art_094_00_historia.pdf, Art_095_00_historia.pdf, Art_096_00_historia.pdf, Art_097_00_historia.pdf, Art_098_00_historia.pdf, Art_099_00_historia.pdf, Art_107_00_historia.pdf, Art_108_00_historia.pdf, Art_116_00_historia.pdf, Art_122_00_historia.pdf, Art_123_00_historia.pdf.

## Totales

- Estados: 128 verificado, 8 historial por cotejar (Grupo A: 2, 10, 20, 22, 82, 116, 122; más el 35).
- Versiones totales: 977; con fecha pendiente: 17 (sin cambio).
- Golden cases (Arts. 1 y 4) intactos; `index.html`, `historial/N.json`, `articulos/N.html` y `sitemap.xml` regenerados con `build.py`.
