# Reporte: 18 solapes de vigencia de un día en `cpeum.json`

- **Base analizada:** `main` en `c682cd3` («Cierra hueco del Art. 1 e incorpora Texto original 1917 del Art. 81 (#21)»). Ya incluye los PR #18, #20 y #21.
- **Definición de solape:** `vigencia_hasta` de una versión es igual al `vigencia_desde` de la versión siguiente del mismo artículo.
- **Fuente de verificación:** PDF oficiales de la SCJN, descargados de `https://www.scjn.gob.mx/sites/default/files/cpeum/documento/`.
- **Extracción:** `pdfplumber`, columna izquierda de encabezados (`x1 < 145`). La coordenada `top` está en puntos PDF y corresponde a la primera palabra del encabezado («Texto»).
- **Alcance:** este PR es solo documental. No modifica ningún dato (`cpeum.json`, `cpeum-art-*.json`, `historial/`, `articulos/`).

## 1. Resumen

| Clase | Casos | Descripción |
|---|---|---|
| (a) Versión intermedia legítima | **14** | Dos o tres decretos publicados el mismo día. La SCJN muestra un bloque «Texto derivado…» por cada decreto, todos con la misma fecha DOF. |
| (b) Error de cálculo | **0** | Ningún caso equivale al hueco del Art. 1 (que se corrigió en el #21). |
| (c) Otro: fe de erratas de 1917 | **4** | Arts. 20, 37, 73 y 85. El texto original (DOF 05-02-1917) y la fe de erratas (DOF 06-02-1917) son anteriores a la entrada en vigor de la Constitución (01-05-1917). |

- **Art. 4 (golden case):** está implicado en 2 casos de clase (a), las versiones `v12` y `v22`. No se propone corregirlo; cualquier cambio requeriría autorización de Jaime.
- **Recomendación general:** dejar los 18 casos como están y formalizar la convención de la sección 4.

## 2. Tabla de los 18 casos

Fechas en formato AAAA-MM-DD. En las columnas «Encabezado SCJN», la notación «p. X top Y» indica página y coordenada. La marca «→» señala un encabezado partido por un salto de página.

| # | Art. | Versión A (tipo) | Publ. A | Desde A | Hasta A | Versión B (tipo) | Publ. B | Desde B | Hasta B | Encabezado SCJN de A | Encabezado SCJN de B | Clase | Recomendación |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | v12 (reforma) «Reforma DOF 12-10-2011 (decreto 1)» | 2011-10-12 | 2011-10-13 | 2011-10-13 | v13 (reforma) «(decreto 2)» | 2011-10-12 | 2011-10-13 | 2011-10-13 | `CPEUM-004_2.pdf` p. 7 top 543.38 «…12 de octubre de 2011» | p. 8 top 556.10 «…12 de octubre de 2011» | a | Dejar (golden) |
| 2 | 4 | v22 (reforma) «Reforma DOF 02-12-2024 (decreto 1)» | 2024-12-02 | 2024-12-03 | 2024-12-03 | v23 (reforma) «(decreto 2)» | 2024-12-02 | 2024-12-03 | 2025-01-17 | p. 23 top 642.38 «…02 de diciembre de 2024» | p. 26 top 448.82 «…02 de diciembre de 2024» | a | Dejar (golden) |
| 3 | 20 | v1 (original) | 1917-02-05 | 1917-05-01 | 1917-05-01 | v2 (fe_de_erratas) | 1917-02-06 | 1917-05-01 | 1948-12-02 | `CPEUM-020_1.pdf` p. 1 top 281.42 «Texto original D.O.F. 05 de febrero de 1917» | p. 2 top 540.50 «Texto derivado de la fe de erratas… 06 de febrero de 1917» | c | Dejar |
| 4 | 27 | v14 (reforma) | 1976-02-06 | 1976-02-07 | 1976-02-07 | v15 (reforma) | 1976-02-06 | 1976-02-07 | 1983-02-03 | `CPEUM-027_2.pdf` p. 98 top 624.02 «…06 de febrero de 1976» | p. 107 top 563.18 «…06 de febrero de 1976» | a | Dejar |
| 5 | 37 | v1 (original) | 1917-02-05 | 1917-05-01 | 1917-05-01 | v2 (fe_de_erratas) | 1917-02-06 | 1917-05-01 | 1934-01-18 | `CPEUM-037.pdf` p. 1 top 223.63 «Texto original…» | p. 1 top 457.83 «…fe de erratas… 06 de febrero de 1917» | c | Dejar |
| 6 | 43 | v9 (reforma) | 2021-05-17 | 2021-05-18 | 2021-05-18 | v10 (vigente) | 2021-05-17 | 2021-05-18 | null | `CPEUM-043.pdf` p. 2 top 569.78 «…17 de mayo de 2021» | p. 2 top 666.98 «Texto vigente D.O.F.» → p. 3 top 137.8 «17 de mayo de 2021» | a | Dejar |
| 7 | 73 | v1 (original) | 1917-02-05 | 1917-05-01 | 1917-05-01 | v2 (fe_de_erratas) | 1917-02-06 | 1917-05-01 | 1921-07-08 | `CPEUM-073_5.pdf` p. 1 top 267.26 | p. 6 top 237.50 «…fe de erratas… 06 de febrero de 1917» | c | Dejar |
| 8 | 73 | v4 (reforma) | 1928-08-20 | 1928-08-21 | 1928-08-21 | v5 (reforma) | 1928-08-20 | 1928-08-21 | 1929-09-06 | p. 15 top 676.82 «Texto derivado de la reforma» → p. 16 top 137.8 «publicada en el D.O.F. 20 de agosto de 1928» | p. 21 top 527.18 «…20 de agosto de 1928» | a | Dejar |
| 9 | 73 | v9 (reforma) | 1934-01-18 | 1934-01-19 | 1934-01-19 | v10 (reforma) | 1934-01-18 | 1934-01-19 | 1934-12-13 | p. 44 top 371.78 «…18 de enero de 1934» | p. 49 top 568.34 «…18 de enero de 1934» | a | Dejar |
| 10 | 73 | v14 (reforma) | 1940-12-14 | 1940-12-15 | 1940-12-15 | v15 (reforma) | 1940-12-14 | 1940-12-15 | 1942-10-24 | p. 72 top 303.62 «…14 de diciembre de 1940» | p. 78 top 233.78 «…14 de diciembre de 1940» | a | Dejar |
| 11 | 73 | v37 (reforma) | 1987-08-10 | 1987-08-11 | 1987-08-11 | v38 (reforma) | 1987-08-10 | 1987-08-11 | 1987-08-11 | p. 230 top 527.30 «…10 de agosto de 1987» | p. 238 top 401.42 «…10 de agosto de 1987» | a | Dejar |
| 12 | 73 | v38 (reforma) | 1987-08-10 | 1987-08-11 | 1987-08-11 | v39 (reforma) | 1987-08-10 | 1987-08-11 | 1990-04-06 | p. 238 top 401.42 | p. 249 top 317.54 «…10 de agosto de 1987» (tercer bloque del mismo día) | a | Dejar |
| 13 | 73 | v46 (reforma) | 1999-06-28 | 1999-06-29 | 1999-06-29 | v47 (reforma) | 1999-06-28 | 1999-06-29 | 1999-07-30 | p. 310 top 149.90 «…28 de junio de 1999» | p. 316 top 513.26 «…28 de junio de 1999» | a | Dejar |
| 14 | 73 | v62 (reforma) | 2009-04-30 | 2009-05-01 | 2009-05-01 | v63 (reforma) | 2009-04-30 | 2009-05-01 | 2009-05-04 | p. 426 top 137.8, primera línea sobreimpresa (`RETFeOxRtMo…`); el resto dice «…D.O.F. 30 de abril de 2009» (top 174.3–198.6) | p. 434 top 137.78 «…30 de abril de 2009» | a | Dejar |
| 15 | 73 | v66 (reforma) | 2011-10-12 | 2011-10-13 | 2011-10-13 | v67 (reforma) | 2011-10-12 | 2011-10-13 | 2012-06-25 | p. 458 top 303.62 «…12 de octubre de 2011» | p. 465 top 358.34 «…12 de octubre de 2011» | a | Dejar |
| 16 | 85 | v1 (original) | 1917-02-05 | 1917-05-01 | 1917-05-01 | v2 (fe_de_erratas) | 1917-02-06 | 1917-05-01 | 1933-04-29 | `CPEUM-085.pdf` p. 1 top 223.58 | p. 1 top 562.82 «…fe de erratas… 6 de febrero de 1917» | c | Dejar |
| 17 | 89 | v5 (reforma) | 1966-10-21 | 1966-10-22 | 1966-10-22 | v6 (reforma) | 1966-10-21 | 1966-10-22 | 1974-10-08 | `CPEUM-089_4.pdf` p. 7 top 198.62 «…21 de octubre de 1966» | p. 8 top 636.14 «…D.O.F.» → p. 9 top 137.8 «21 de octubre de 1966» | a | Dejar |
| 18 | 123 | v15 (reforma) | 1978-01-09 | 1978-01-10 | 1978-01-10 | v16 (reforma) | 1978-01-09 | 1978-01-10 | 1978-01-13 | `CPEUM-123_9.pdf` p. 108 top 354.14 «…09 de enero de 1978» | p. 118 top 657.98 «Texto derivado de la reforma» → p. 119 top 137.8 «publicada en el D.O.F. 09 de enero de 1978» | a | Dejar |

Notas a la tabla:

- **Caso 1:** la versión siguiente es v14, publicada el 2011-10-13 y vigente desde el 2011-10-14 (SCJN p. 9 top 592.58). Por eso v13 cierra correctamente el 2011-10-13.
- **Casos 11 y 12:** el 10-08-1987 hay tres bloques del mismo día, que producen dos solapes encadenados.
- **Caso 18:** v17 es la fe de erratas del 13-01-1978 (SCJN p. 131 top 205.94).

## 3. Hechos e inferencias

### Hechos comprobados

1. **Bloques del mismo día:** en los 14 casos de clase (a), el PDF oficial de la SCJN contiene dos bloques de encabezado distintos con la misma fecha DOF; en el Art. 73 de 1987, tres. Las páginas y coordenadas están en la tabla.
2. **Textos distintos:** las versiones A y B tienen texto diferente. Por ejemplo:
   - Art. 73, v62 → v63: se añade la fracción XXIX-O.
   - Art. 73, v4 → v5: cambia la fracción VI.
3. **Notas de vigencia en clase (a):** las 14 versiones A llevan en `vigencia_nota` la frase «Texto intermedio: el siguiente decreto entró en vigor el mismo día».
   - Las dos del Art. 4 dicen además «…se publicó el mismo día y entró en vigor en la misma fecha, por lo que esta versión no rigió por sí sola», con `vigencia_verificada: true`.
   - Las demás tienen `vigencia_verificada: false`.
4. **Notas de vigencia en clase (c):** las 4 versiones originales de 1917 llevan una nota de fe de erratas anterior a la entrada en vigor de la Constitución (1o. de mayo de 1917): «no rigió por sí solo; se conserva como texto publicado».
5. **Sin huecos:** ninguna de las 18 parejas tiene un hueco. En todas, la versión B empieza el mismo día en que termina A.
6. **Encabezado sobreimpreso:** el encabezado de la p. 426 del Art. 73 tiene la primera línea sobreimpresa en el PDF. Las líneas legibles («…publicada en el D.O.F. 30 de abril de 2009») permiten fecharlo, como ya registra `notas_scjn` de v62.

### Inferencias

1. **Clase (a):** cuando se publican varios decretos el mismo día y todos entran en vigor al día siguiente, la versión que refleja solo el primero no rigió por sí sola. La SCJN la conserva como paso intermedio de la compilación. Su intervalo `[desde, hasta]` de un solo día, igual al inicio de la siguiente, es una convención de representación y no un error.
2. **Sin clase (b):** aplicar «hasta = desde siguiente − 1 día» dejaría `vigencia_hasta < vigencia_desde`, un intervalo inválido. Por eso no se clasifica ningún caso como error.
3. **Clase (c):** el texto original y su fe de erratas se publicaron antes del 01-05-1917. En esa fecha entró en vigor el texto ya corregido, así que el original tampoco rigió por sí solo. Es la misma situación que (a), con otra causa.
4. **Orden de los decretos del mismo día:** el orden v_A antes de v_B sigue el orden de los bloques en el PDF de la SCJN. No verifiqué en el DOF el orden de publicación dentro del mismo día.

## 4. Convención propuesta (única) para versiones intermedias del mismo día

Una versión que no rigió por sí sola sigue estas reglas. Aplica a decretos publicados el mismo día con la misma entrada en vigor y a textos de 1917 corregidos antes de su entrada en vigor.

1. Se conserva como versión propia, porque es texto publicado y la SCJN la registra como bloque independiente.
2. Fechas: `vigencia_desde = vigencia_hasta = vigencia_desde` de la versión siguiente. Es la convención actual, que ya usan los 18 casos.
3. Se añade un campo explícito `intermedia: true`. Hoy esa información solo está en el texto libre de `vigencia_nota`.
4. `vigencia_nota` lleva una fórmula fija:
   - Para clase (a): «Texto intermedio: no rigió por sí sola; el decreto siguiente, publicado el mismo día, entró en vigor en la misma fecha».
   - Para clase (c): la variante equivalente de fe de erratas.
5. **Validador:** sigue exigiendo cero huecos y una sola vigencia abierta. Admite el solape de un día solo si la versión anterior tiene `intermedia: true`, `vigencia_desde == vigencia_hasta` y la misma fecha de publicación (o es la fe de erratas de 1917). Cualquier otro solape es error.
6. **Presentación:** el sitio puede mostrar estas versiones como «versión intermedia (no rigió por sí sola)» en lugar de «vigente del X al X».

**Aplicación:** añadir `intermedia: true` a las 18 versiones A, 2 de ellas del Art. 4, sin cambiar ninguna fecha.
- Para las del Art. 4 (golden case), hace falta autorización expresa de Jaime y actualizar `cpeum-art-4.json`.
- Se sugiere hacerlo en un PR de datos aparte.

## 5. Casos a corregir

**Ninguno.** No hay valores de fecha propuestos, porque no se encontró ningún error de cálculo de clase (b).
