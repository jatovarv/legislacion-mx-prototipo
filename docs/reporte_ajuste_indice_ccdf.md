# Reporte — Ajuste del índice del CCDF con la fuente oficial de la Consejería (PR #18)

**Estado: bloqueado por falta de la fuente autorizada.** El DOCX oficial de la Consejería Jurídica y de Servicios Legales de la CDMX (última reforma 20-08-2026, GOCDMX 1929 Bis) **no está en el repositorio ni en Google Drive**, y desde el entorno de trabajo no es posible descargarlo (la Consejería, el Congreso de la CDMX y el buscador de legislación de la SCJN rechazan la conexión o están bloqueados). Conforme al brief («si el DOCX no está accesible, escalar y no proceder con correcciones de contenido»), **no se corrigió ningún nombre ni rango**: no hay fuente contra la cual cotejar y no se inventa estructura.

## Qué se pide para desbloquear
Adjuntar al repositorio (o a un brief) el archivo `CODIGO_CIVIL_PARA_EL_DF_15.4.docx` de la Consejería junto con su **SHA-256** (pendiente `ccdf-docx-hash` del registro de fuentes). Con el archivo en mano, el cotejo de los 51 Títulos es una tarea mecánica de una sesión: se registra en esta misma tabla la sección del DOCX de cada Título y se retiran las marcas `nombre_por_cotejar` / `rango_por_cotejar`.

## Qué sí se hizo en este ajuste (sin contenido normativo)
1. **Marcas explícitas**: cada Libro, Parte y Título de `ccdf.json` lleva `nombre_por_cotejar: true` y, si tiene rango, `rango_por_cotejar: true`; la interfaz muestra «por cotejar» en cada nodo.
2. **noindex temporal del índice**: `norma.estructura_cotejada: false` hace que `ccdf/index.html` se publique con `<meta name="robots" content="noindex,follow">` y **fuera del sitemap** (137 URL, sólo CPEUM). Las 10 fichas de artículos siguen sin texto, con `noindex` y fuera del sitemap. Al cotejar el índice basta poner `estructura_cotejada: true`.
3. **Preguntas del Coordinador registradas** en `ccdf.json → norma.cotejo_pendiente` y abajo, sin resolverlas por inferencia.
4. Retirada la captura ajena `shots/art72-fecha-pendiente.png`; rama actualizada con `main` (incluye PR #19); conteo corregido: son **51 Títulos** (14 + 7 + 5 + 6 + 17 + 1 + 1), no 30.

## Preguntas abiertas (requieren el DOCX; no se resuelven por inferencia)
| # | Pregunta | Estado |
|---|---|---|
| 1 | Nombres y rangos de los 51 Títulos. | Pendiente; todos marcados. |
| 2 | Salto del art. 1180 (fin del Libro Segundo, Título Séptimo «De la Prescripción») al 1281 (inicio del Libro Tercero): ¿hay un Título o artículos derogados que falten en el índice, o la numeración oficial salta? | Pendiente. No se añade ningún nodo hasta verlo en el DOCX. |
| 3 | Epígrafe del Libro Tercero, Título Primero: el índice dice «Disposiciones Generales»; confirmar contra el DOCX («Disposiciones Preliminares» vs «Disposiciones Generales»). | Pendiente; marcado `nombre_por_cotejar`. |
| 4 | Capítulos de cada Título. | Fuera del índice hasta el cotejo. |

## Tabla de cotejo (a llenar con el DOCX)
Columnas «Estado» y «Sección del DOCX» se completan en el cotejo; hoy todas están pendientes.

| Ubicación | Título | Epígrafe | Rango actual | Estado | Sección / página del DOCX |
|---|---|---|---|---|---|
| — | Disposiciones Preliminares |  | 1–21 | pendiente | — |
| Libro Primero | Título Primero | De las Personas Físicas | 22–24 | pendiente | — |
| Libro Primero | Título Segundo | De las Personas Morales | 25–28 | pendiente | — |
| Libro Primero | Título Tercero | Del Domicilio | 29–34 | pendiente | — |
| Libro Primero | Título Cuarto | Del Registro Civil | 35–138 | pendiente | — |
| Libro Primero | Título Cuarto Bis | De la Familia | 138 Ter–138 Sextus | pendiente | — |
| Libro Primero | Título Quinto | Del Matrimonio | 139–291 | pendiente | — |
| Libro Primero | Título Quinto Bis | Del Concubinato | 291 Bis–291 Quintus | pendiente | — |
| Libro Primero | Título Sexto | Del Parentesco, de los Alimentos y de la Violencia Familiar | 292–323 Septimus | pendiente | — |
| Libro Primero | Título Séptimo | De la Paternidad y Filiación | 324–410 F | pendiente | — |
| Libro Primero | Título Octavo | De la Patria Potestad | 411–448 | pendiente | — |
| Libro Primero | Título Noveno | De la Tutela | 449–640 | pendiente | — |
| Libro Primero | Título Décimo | De la Emancipación y de la Mayor Edad | 641–647 | pendiente | — |
| Libro Primero | Título Undécimo | De los Ausentes e Ignorados | 648–722 | pendiente | — |
| Libro Primero | Título Duodécimo | Del Patrimonio de la Familia | 723–746 | pendiente | — |
| Libro Segundo | Título Primero | Disposiciones Preliminares | 747–749 | pendiente | — |
| Libro Segundo | Título Segundo | Clasificación de los Bienes | 750–789 | pendiente | — |
| Libro Segundo | Título Tercero | De la Posesión | 790–829 | pendiente | — |
| Libro Segundo | Título Cuarto | De la Propiedad | 830–979 | pendiente | — |
| Libro Segundo | Título Quinto | Del Usufructo, del Uso y de la Habitación | 980–1056 | pendiente | — |
| Libro Segundo | Título Sexto | De las Servidumbres | 1057–1134 | pendiente | — |
| Libro Segundo | Título Séptimo | De la Prescripción | 1135–1180 | pendiente | — |
| Libro Tercero | Título Primero | Disposiciones Generales | 1281–1294 | pendiente | — |
| Libro Tercero | Título Segundo | De la Sucesión por Testamento | 1295–1498 | pendiente | — |
| Libro Tercero | Título Tercero | De la Forma de los Testamentos | 1499–1598 | pendiente | — |
| Libro Tercero | Título Cuarto | De la Sucesión Legítima | 1599–1637 | pendiente | — |
| Libro Tercero | Título Quinto | Disposiciones Comunes a las Sucesiones Testamentaria y Legítima | 1638–1791 | pendiente | — |
| Libro Cuarto › Primera Parte | Título Primero | Fuentes de las Obligaciones | 1792–1934 | pendiente | — |
| Libro Cuarto › Primera Parte | Título Segundo | Modalidades de las Obligaciones | 1935–1987 | pendiente | — |
| Libro Cuarto › Primera Parte | Título Tercero | De la Transmisión de las Obligaciones | 1988–2061 | pendiente | — |
| Libro Cuarto › Primera Parte | Título Cuarto | Efectos de las Obligaciones | 2062–2184 | pendiente | — |
| Libro Cuarto › Primera Parte | Título Quinto | Extinción de las Obligaciones | 2185–2223 | pendiente | — |
| Libro Cuarto › Primera Parte | Título Sexto | De la Inexistencia y de la Nulidad | 2224–2242 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Primero | De los Contratos Preparatorios. La Promesa | 2243–2247 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Segundo | De la Compraventa | 2248–2326 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Tercero | De la Permuta | 2327–2331 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Cuarto | De las Donaciones | 2332–2383 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Quinto | Del Mutuo | 2384–2397 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Sexto | Del Arrendamiento | 2398–2496 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Séptimo | Del Comodato | 2497–2515 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Octavo | Del Depósito y del Secuestro | 2516–2545 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Noveno | Del Mandato | 2546–2604 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Décimo | Del Contrato de Prestación de Servicios | 2605–2669 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Undécimo | De las Asociaciones y de las Sociedades | 2670–2738 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Duodécimo | De la Aparcería Rural | 2739–2763 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Décimo Tercero | De los Contratos Aleatorios | 2764–2793 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Décimo Cuarto | De la Fianza | 2794–2855 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Décimo Quinto | De la Prenda | 2856–2892 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Décimo Sexto | De la Hipoteca | 2893–2943 | pendiente | — |
| Libro Cuarto › Segunda Parte | Título Décimo Séptimo | De las Transacciones | 2944–2963 | pendiente | — |
| Libro Cuarto › Tercera Parte | Título Primero | De la Concurrencia y Prelación de los Créditos | 2964–2998 | pendiente | — |
| Libro Cuarto › Cuarta Parte | Título Primero | Del Registro Público | 2999–3074 | pendiente | — |

## Criterios de aceptación del brief, estado
1. Cada Título cita fuente o lleva marca → **todos llevan `nombre_por_cotejar` y `rango_por_cotejar`**.
2. Sin texto normativo inventado ni completado → **cumplido** (no hay texto).
3. 10 fichas con texto vacío, noindex y fuera del sitemap → **cumplido**.
4. Golden cases CPEUM intactos → **cumplido** (verificado en el build).
5. Reporte con sección del DOCX por corrección → **no aplicable**: no hubo correcciones por falta del DOCX.
6. DOCX no disponible → **documentado aquí y noindex temporal aplicado al índice**.
