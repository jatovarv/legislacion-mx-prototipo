# Reporte — Ajuste del índice del CCDF con fuente oficial (PR #18)

**Estado: índice cotejado.** El DOCX de la Consejería sigue sin estar disponible (no está en el repositorio ni en Drive; los sitios oficiales no son accesibles desde el entorno de trabajo). El Coordinador/Jaime aportó en su lugar el **PDF oficial del Código publicado por el Congreso de la Ciudad de México** (Instituto de Investigaciones Legislativas), que se obtuvo a través del navegador del escritorio de Jaime y se verificó por hash:

| Dato | Valor |
|---|---|
| URL | https://www.congresocdmx.gob.mx/media/documentos/e793ac29adb26ebcde17cd1aeab3faf4150fd489.pdf |
| Título del archivo | CÓDIGO CIVIL PARA EL DF ACTUALIZADO 02-09-26 (metadatos del PDF: creado 2026-09-02, Word/Quartz) |
| SHA-256 | `985e3bfa4654a1e0ba68162a94033114c10499d98cdb8a640e79299d6ca4983d` |
| Tamaño / páginas | 3,120,455 bytes / 381 páginas |
| Articulado | pp. 1–332 (arts. 1 a 3074); transitorios desde p. 374 |

**Advertencia de metadatos.** El archivo lleva la etiqueta «ACTUALIZADO 02-09-26», la fecha que el registro de fuentes tiene documentada como *conflicto de metadatos* (no se localizó decreto de esa fecha). El índice (nombres de Libros/Partes/Títulos/Capítulos y rangos de artículos) **no depende de ese dato**; la última reforma verificada del Código sigue siendo la GOCDMX 1929 Bis de 20-08-2026 y la fuente autorizada para el **texto** sigue siendo el DOCX de la Consejería, pendiente de hash. Queda a decisión del Coordinador si el índice se considera verificado con esta fuente o si debe volver a cotejarse contra el DOCX cuando exista.

## Método (reproducible)
`cotejar_estructura_ccdf_pdf.py <pdf>` extrae con PyMuPDF las líneas del PDF, reconoce los encabezados en mayúsculas (`LIBRO`, `PRIMERA PARTE`/`PARTE SEGUNDA`/`TERCERA PARTE`, `TITULO`, `CAPITULO`), toma como epígrafe las líneas que siguen y registra cada «ARTICULO N» (con Bis/Ter/Quáter…/letras) bajo el encabezado vigente. El rango de cada nodo es su primer y último artículo. Resultado: **3,074 numerales, todos presentes** (3,187 artículos contando los Bis/letras; 335 marcados DEROGADO), **4 Libros, 3 Partes, 51 Títulos, 224 Capítulos y 5 secciones intermedias**. La página del PDF de cada nodo queda guardada en `ccdf.json` (`pagina`) y se muestra al pasar el cursor por el rango en `ccdf/index.html`. No se extrajo ni guardó texto normativo.

## Respuesta a las correcciones mínimas del Coordinador
1. **51 Títulos cotejados** — tabla completa abajo, con página del PDF, epígrafe y rango. El índice anterior tenía 51 Títulos pero **no los mismos**: tres no existen como tales en la fuente (Quinto Bis, Aparcería, Cuarta Parte) y tres faltaban (Primero Bis, Derechos de autor, Registro Público como Título Segundo de la Tercera Parte), además de un corrimiento de numeración en la Parte Segunda (ver «Títulos retirados» y las filas marcadas «no estaba en el índice»).
2. **Salto 1180 → 1281** — resuelto: el Libro Segundo tiene un **Título Octavo «De los derechos de autor»**, arts. 1181–1280, los 100 **derogados**, en tres Capítulos sin epígrafe (PDF pp. 148–152). Se incorporó al índice.
3. **Libro Tercero, Título Primero** — el PDF lo titula **«Disposiciones preliminares»** (p. 152); corregido (el índice decía «Disposiciones Generales»). El Libro Segundo, Título Primero también dice «Disposiciones Preliminares» (p. 107).
4. **Marcas** — ya no queda ningún nodo con `nombre_por_cotejar` / `rango_por_cotejar`: todos citan página del PDF. Lo no modelado se declara en `norma.cotejo_pendiente.abiertas` (subencabezado «Disposiciones generales» del Capítulo IV del Título Quinto, Secciones del Capítulo V «De la adopción», y el encabezado «CAPITULO III DE LA VIOLENCIA FAMILIAR» que el PDF repite antes del art. 323 Séptimus, tomado como continuación).
5. Descripción del PR corregida (51 Títulos). 6. Captura ajena retirada en el commit anterior. 7. Rama al día con `main`.

## Diferencias respecto al índice anterior (de memoria, sin fuente)
Además de rangos corregidos en 12 Títulos, hubo cambios estructurales:
- **Faltaban**: Libro Primero, **Título Primero Bis** (arts. 24 A–24 O, apoyos para el ejercicio de la capacidad jurídica; sin epígrafe en la fuente; p. 4); Libro Segundo, **Título Octavo «De los derechos de autor»** (1181–1280, derogados); Libro Cuarto, Tercera Parte, **Título Segundo «Del registro publico»** (2999–3074).
- **Títulos retirados o renumerados** (según la fuente):
  - Libro Primero › **Título Quinto Bis «Del Concubinato»** (291 Bis–291 Quintus): no existe como Título. El concubinato es el **Capítulo XI del Título Quinto** (art. 291 Bis…, p. 47).
  - Libro Cuarto › Segunda Parte › **Título Duodécimo «De la Aparcería Rural»** (2739–2763): no existe como Título. La aparcería rural es el **Capítulo VII del Título Decimoprimero «De las asociaciones y de las sociedades»** (2739–2763, p. 286). En consecuencia la Parte Segunda tiene **16 Títulos, no 17**, y del Decimosegundo en adelante la numeración de la fuente va una unidad por debajo del índice anterior: contratos aleatorios = Decimosegundo, fianza = Decimotercero, prenda = Decimocuarto, hipoteca = Decimoquinto, transacciones = Decimosexto (la fuente escribe «DECIMOPRIMERO», «DECIMOSEGUNDO»…, no «Undécimo»/«Décimo Tercero»). En la tabla, las filas «epígrafe: X → Y» de esos Títulos reflejan este corrimiento, no un cambio de materia.
  - Libro Cuarto › **Cuarta Parte › Título Primero «Del Registro Público»** (2999–3074): no hay Cuarta Parte. El Registro Público es el **Título Segundo de la Tercera Parte** (2999–3074, p. 316).
- Epígrafe del Libro Primero, Título Séptimo: «De la filiación» (no «De la Paternidad y Filiación»). La Segunda Parte del Libro Cuarto se titula en la fuente «PARTE SEGUNDA».
- Rangos con sufijo que el índice anterior no tenía: Título Segundo 25–28 Bis; Cuarto 35–138 Bis; Sexto 292–323 Nonies; Duodécimo 723–746 Bis; Libro IV Título Primero 1792–1937, Segundo 1938–2028, Tercero 2029–2061; Decimoprimero 2670–2763; Decimoquinto 2893–2943 (2939 Decies).

## Tabla de cotejo de los 51 Títulos (+ Disposiciones preliminares)
| Ubicación | Título | Epígrafe (fuente) | Rango | Artículos | Capítulos | PDF | Resultado del cotejo |
|---|---|---|---|---|---|---|---|
| — | Disposiciones preliminares | *(sin epígrafe en la fuente)* | 1–21 | 21 (1 derog.) | 0 | p. 1 | confirmado |
| Libro Primero | Título Primero | De las personas físicas | 22–24 | 3 (0 derog.) | 0 | p. 3 | confirmado |
| Libro Primero | Título Primero Bis | *(sin epígrafe en la fuente)* | 24 A–24 O | 15 (0 derog.) | 2 | p. 4 | **Título no estaba en el índice** |
| Libro Primero | Título Segundo | De las personas morales | 25–28 Bis | 5 (0 derog.) | 0 | p. 7 | rango: 25–28 → 25–28 Bis |
| Libro Primero | Título Tercero | Del domicilio | 29–34 | 6 (0 derog.) | 0 | p. 8 | confirmado |
| Libro Primero | Título Cuarto | Del Registro Civil | 35–138 Bis | 109 (22 derog.) | 11 | p. 9 | rango: 35–138 → 35–138 Bis |
| Libro Primero | Título Cuarto Bis | De la Familia | 138 Ter–138 Sextus | 4 (0 derog.) | 1 | p. 25 | confirmado |
| Libro Primero | Título Quinto | Del matrimonio | 139–291 Bis | 165 (50 derog.) | 11 | p. 25 | rango: 139–291 → 139–291 Bis |
| Libro Primero | Título Sexto | Del parentesco, de los alimentos y de la violencia familiar | 292–323 Nonies | 45 (1 derog.) | 4 | p. 47 | rango: 292–323 Septimus → 292–323 Nonies |
| Libro Primero | Título Séptimo | De la filiación | 324–410 F | 99 (23 derog.) | 5 | p. 55 | epígrafe: «De la Paternidad y Filiación» → «De la filiación» |
| Libro Primero | Título Octavo | De la patria potestad | 411–448 | 43 (2 derog.) | 3 | p. 66 | confirmado |
| Libro Primero | Título Noveno | De la tutela | 449–640 | 207 (18 derog.) | 17 | p. 73 | confirmado |
| Libro Primero | Título Décimo | De la emancipación y de la mayor edad | 641–647 | 7 (4 derog.) | 2 | p. 96 | confirmado |
| Libro Primero | Título Undécimo | De los ausentes e ignorados | 648–722 | 75 (0 derog.) | 7 | p. 97 | confirmado |
| Libro Primero | Título Duodécimo | Del patrimonio de la familia | 723–746 Bis | 25 (0 derog.) | 1 | p. 104 | rango: 723–746 → 723–746 Bis |
| Libro Segundo | Título Primero | Disposiciones Preliminares | 747–749 | 3 (0 derog.) | 0 | p. 107 | confirmado |
| Libro Segundo | Título Segundo | Clasificación de los bienes | 750–789 | 40 (1 derog.) | 5 | p. 108 | confirmado |
| Libro Segundo | Título Tercero | De la posesión | 790–829 | 40 (0 derog.) | 1 | p. 112 | confirmado |
| Libro Segundo | Título Cuarto | De la propiedad | 830–979 | 151 (1 derog.) | 6 | p. 116 | confirmado |
| Libro Segundo | Título Quinto | Del usufructo, del uso y de la habitación | 980–1056 | 77 (0 derog.) | 5 | p. 129 | confirmado |
| Libro Segundo | Título Sexto | De las servidumbres | 1057–1134 | 78 (0 derog.) | 9 | p. 136 | confirmado |
| Libro Segundo | Título Séptimo | De la prescripción | 1135–1180 | 46 (0 derog.) | 6 | p. 143 | confirmado |
| Libro Segundo | Título Octavo | De los derechos de autor | 1181–1280 | 100 (100 derog.) | 3 | p. 148 | **Título no estaba en el índice** |
| Libro Tercero | Título Primero | Disposiciones preliminares | 1281–1294 | 14 (0 derog.) | 0 | p. 152 | epígrafe: «Disposiciones Generales» → «Disposiciones preliminares» |
| Libro Tercero | Título Segundo | De la sucesión por testamento | 1295–1498 | 205 (0 derog.) | 9 | p. 153 | confirmado |
| Libro Tercero | Título Tercero | De la forma de los testamentos | 1499–1598 | 103 (82 derog.) | 8 | p. 171 | confirmado |
| Libro Tercero | Título Cuarto | De la sucesión legítima | 1599–1637 | 39 (1 derog.) | 7 | p. 177 | confirmado |
| Libro Tercero | Título Quinto | Disposiciones comunes a las sucesiones testamentaria y legítima | 1638–1791 | 155 (0 derog.) | 8 | p. 181 | confirmado |
| Libro Cuarto › Primera Parte | Título Primero | Fuentes de las obligaciones | 1792–1937 | 149 (1 derog.) | 6 | p. 194 | rango: 1792–1934 → 1792–1937 |
| Libro Cuarto › Primera Parte | Título Segundo | Modalidades de las obligaciones | 1938–2028 | 91 (0 derog.) | 6 | p. 208 | rango: 1935–1987 → 1938–2028 |
| Libro Cuarto › Primera Parte | Título Tercero | De la transmisión de las obligaciones | 2029–2061 | 33 (0 derog.) | 3 | p. 217 | rango: 1988–2061 → 2029–2061 |
| Libro Cuarto › Primera Parte | Título Cuarto | Efectos de las obligaciones | 2062–2184 | 123 (0 derog.) | 6 | p. 220 | confirmado |
| Libro Cuarto › Primera Parte | Título Quinto | Extinción de las obligaciones | 2185–2223 | 39 (0 derog.) | 4 | p. 230 | confirmado |
| Libro Cuarto › Primera Parte | Título Sexto | De la inexistencia y de la nulidad | 2224–2242 | 19 (0 derog.) | 0 | p. 233 | confirmado |
| Libro Cuarto › Parte Segunda | Título Primero | De los contratos preparatorios.- La promesa. | 2243–2247 | 5 (0 derog.) | 0 | p. 235 | epígrafe: «De los Contratos Preparatorios. La Promesa» → «De los contratos preparatorios.- La promesa.» |
| Libro Cuarto › Parte Segunda | Título Segundo | De la compra-venta | 2248–2326 | 79 (1 derog.) | 9 | p. 235 | epígrafe: «De la Compraventa» → «De la compra-venta» |
| Libro Cuarto › Parte Segunda | Título Tercero | De la permuta | 2327–2331 | 5 (0 derog.) | 0 | p. 243 | confirmado |
| Libro Cuarto › Parte Segunda | Título Cuarto | De las donaciones | 2332–2383 | 52 (0 derog.) | 3 | p. 244 | confirmado |
| Libro Cuarto › Parte Segunda | Título Quinto | Del mutuo | 2384–2397 | 14 (0 derog.) | 2 | p. 248 | confirmado |
| Libro Cuarto › Parte Segunda | Título Sexto | Del arrendamiento | 2398–2496 | 111 (15 derog.) | 9 | p. 249 | confirmado |
| Libro Cuarto › Parte Segunda | Título Séptimo | Del comodato | 2497–2515 | 19 (0 derog.) | 0 | p. 262 | confirmado |
| Libro Cuarto › Parte Segunda | Título Octavo | Del depósito y del secuestro | 2516–2545 | 30 (0 derog.) | 2 | p. 263 | confirmado |
| Libro Cuarto › Parte Segunda | Título Noveno | Del mandato | 2546–2604 | 59 (0 derog.) | 6 | p. 266 | confirmado |
| Libro Cuarto › Parte Segunda | Título Décimo | Del contrato de prestación de servicios | 2605–2669 | 65 (0 derog.) | 5 | p. 272 | confirmado |
| Libro Cuarto › Parte Segunda | Título Decimoprimero | De las asociaciones y de las sociedades | 2670–2763 | 94 (2 derog.) | 7 | p. 278 | **Título no estaba en el índice** |
| Libro Cuarto › Parte Segunda | Título Decimosegundo | De los contratos aleatorios | 2764–2793 | 30 (0 derog.) | 3 | p. 288 | **Título no estaba en el índice** |
| Libro Cuarto › Parte Segunda | Título Decimotercero | De la fianza | 2794–2855 | 62 (0 derog.) | 6 | p. 291 | epígrafe: «De los Contratos Aleatorios» → «De la fianza»; rango: 2764–2793 → 2794–2855 |
| Libro Cuarto › Parte Segunda | Título Decimocuarto | De la prenda | 2856–2892 | 37 (1 derog.) | 0 | p. 297 | epígrafe: «De la Fianza» → «De la prenda»; rango: 2794–2855 → 2856–2892 |
| Libro Cuarto › Parte Segunda | Título Decimoquinto | De la hipoteca | 2893–2943 | 56 (0 derog.) | 4 | p. 300 | epígrafe: «De la Prenda» → «De la hipoteca»; rango: 2856–2892 → 2893–2943 |
| Libro Cuarto › Parte Segunda | Título Decimosexto | De las transacciones | 2944–2963 | 20 (0 derog.) | 0 | p. 309 | epígrafe: «De la Hipoteca» → «De las transacciones»; rango: 2893–2943 → 2944–2963 |
| Libro Cuarto › Tercera Parte | Título Primero | De la concurrencia y prelación de los créditos | 2964–2998 | 35 (0 derog.) | 7 | p. 311 | confirmado |
| Libro Cuarto › Tercera Parte | Título Segundo | Del registro publico | 2999–3074 | 80 (9 derog.) | 5 | p. 316 | **Título no estaba en el índice** |

## Criterios de aceptación del brief
1. Cada Título cita la fuente (página del PDF) → **cumplido**; sin marcas pendientes de nombre/rango.
2. Sin texto normativo inventado ni completado → **cumplido** (solo estructura).
3. 10 fichas de artículos con texto vacío, `noindex` y fuera del sitemap → **sin cambios, cumplido**.
4. Golden cases CPEUM → **intactos**.
5. Página/sección del DOCX por corrección → **no aplicable al DOCX** (no disponible); se cita la **página del PDF del Congreso** en cada nodo y en esta tabla.
6. `noindex` temporal del índice → **retirado**: con el índice cotejado (`estructura_cotejada: true`), `ccdf/index.html` vuelve al sitemap (138 URL). Si el Coordinador prefiere esperar al DOCX, basta poner `estructura_cotejada: false`.
