# legislacion-mx-prototipo

Prototipo navegable de legislación mexicana vigente e histórica (CPEUM; CCDF/CCCDMX en estructura base), con el historial de versiones **desplegado bajo cada artículo**. Navegación inspirada en [Légifrance](https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006070721/). Objetivo: sitio público monetizable con tráfico útil, a costo cero.

## Qué hay

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Navegador interactivo (HTML + CSS + JS, sin dependencias). Lleva embebidos la estructura y el texto vigente de los 136 artículos; el historial de cada artículo se carga de `historial/N.json` al abrirlo (requiere servir el sitio por HTTP, p. ej. GitHub Pages). |
| `historial/N.json` | Historial completo de cada artículo (todas las versiones), generado. |
| `integrar_historial_scjn.py` | Integra en `cpeum.json` la salida del separador (`versiones_separadas.json`, en Drive `/MyDrive/CPEUM_SCJN_Historial/`): cotejo de la última versión SCJN contra el consolidado, fechas de vigencia, marcado de casos dudosos. Escribe `docs/reporte_integracion_historial.json`. |
| `separar_versiones_scjn.py` | Separador de versiones a partir del texto lineal (PyMuPDF) de los PDF «Historia del texto» de la SCJN (validado con Arts. 1 y 4). |
| `cerrar_historial_grupo_b.py` | Cierra el historial del Grupo B (Arts. 3, 72, 99, 100, 107, 109, 123) con el texto vigente de la Cámara como última versión, tras demostrar que la diferencia con el último bloque SCJN es de extracción (no normativa); aísla el bloque sin fecha del Art. 35 y marca los bloques fusionados. Se corre una vez sobre `cpeum.json`; escribe `docs/reporte_cierre_grupo_b.json`. |
| `extraer_historia_scjn_pdf.py` | Extractor por coordenadas (pdfplumber) directamente del PDF de la SCJN: columna izquierda = etiqueta, derecha = texto; frontera de versión en el primer «Art. N.-» tras la etiqueta. Necesario para PDF largos o con bloques fusionados por el separador lineal (24 artículos extraídos por coordenadas: Arts. 2, 10, 16, 20, 22, 26, 27, 28, 35, 53, 56, 73, 74, 94, 95, 96, 97, 98, 99, 107, 108, 116, 122 y 123). |
| `articulos/N.html` | **Páginas estáticas para SEO**, una por cada uno de los 136 artículos (texto vigente; los verificados incluyen además su historial): texto vigente íntegro, fechas, enlace al DOF y versiones anteriores, legibles sin JavaScript. Generadas; no se editan a mano. |
| `sitemap.xml`, `robots.txt` | Para buscadores. Generados. |
| `cpeum.json` | **Fuente de datos editable**: estructura completa de la CPEUM (Títulos, Capítulos, Secciones y rangos de artículos) + los artículos cargados con sus versiones. |
| `cpeum-art-1.json` | Golden case del Artículo 1o. (4 versiones cotejadas con DOF/SCJN). `cpeum.json` lo incluye verbatim. |
| `cpeum-art-4.json` | Golden case del Artículo 4o.: 25 versiones (texto original, 23 reformas y 1 fe de erratas) extraídas del PDF «Historia del texto del artículo» de la SCJN y cotejadas con el texto consolidado de la Cámara de Diputados; el bloque `fuentes` documenta el método y las advertencias. |
| `ccdf.json` | **Código Civil para el Distrito Federal (CCDF/CCCDMX) — estructura base**: metadatos de la norma (última reforma verificada GOCDMX 20-08-2026, ed. 1929 Bis; conflicto de metadatos del Congreso 02-09-2026 documentado), índice por Libros, Partes y Títulos con rangos `rango_por_cotejar`, y 10 artículos de muestra sin texto (`texto: null`, estado `pendiente`). Sin historial todavía. |
| `build_ccdf.py` | Genera `ccdf/index.html` (índice navegable, metadatos, schema.org/Legislation) y `ccdf/articulos/N.html` a partir de `ccdf.json`; lo invoca `build.py`. Un artículo sin texto se publica con el marcador «pendiente de cotejo», `noindex` y fuera del sitemap; al cargar el texto cotejado pasa a indexarse solo. |
| `build.py` | Genera todo lo anterior a partir de `cpeum.json`: inyecta los datos en `index.html` (entre `<!-- DATA:START -->` y `<!-- DATA:END -->`), escribe `articulos/N.html`, `sitemap.xml` y `robots.txt`. Sin dependencias: `python3 build.py`. |

## Funciones del prototipo

- Árbol lateral con la estructura completa de la Constitución (136 artículos), buscador por número o tema, y menú deslizable en móvil.
- Artículo con migas de pan, metadatos (vigencia, DOF, capítulo), navegación anterior/siguiente y enlaces permanentes (`#/art/1`, `#/art/1/v/v2`).
- Botón **Ver historial**: despliega bajo el artículo la lista de versiones (más reciente primero); al elegir una se muestra su **texto íntegro** y, opcionalmente, los cambios resaltados respecto a la versión anterior.
- Selector **«Versión vigente al»** (como el *Version en vigueur au* de Légifrance): muestra el texto que regía en la fecha elegida y la conserva al saltar entre artículos (`?al=AAAA-MM-DD`).
- Fecha de consulta en cabecera y pie, estilos de impresión, enlace copiable.

## Estado de los textos

- **Verificado** (133 artículos): texto vigente cotejado con el consolidado de la Cámara de Diputados (última reforma DOF 07-10-2026) e historial de la SCJN cuya última versión coincide con ese texto vigente. Incluye los 17 artículos sin reformas desde 1917 (una sola versión) y los golden cases 1o. y 4o. `vigencia_verificada: false` marca las versiones cuya entrada en vigor se asume al día siguiente de la publicación (regla general); la interfaz las señala con «vigencia por cotejar». 9 versiones tienen `publicacion: null` (`fecha_pendiente: true`): la fecha quedó partida por un corte de página en el PDF de la SCJN; `fecha_sugerida` guarda la única fecha que citan sus notas dentro de la ventana entre versiones vecinas, como pista para el cotejo manual, nunca como dato. Una más (Art. 81, única versión SCJN y coincidente con el consolidado) lleva la fecha de las notas de la Cámara marcada «fecha por cotejar». Reglas de vigencia: una fe de erratas a la publicación original (DOF 06-02-1917) no crea vigencia propia —el texto corregido es el que entró en vigor el 1o. de mayo de 1917 y el original «no rigió por sí solo»—; la versión anterior a una de fecha pendiente queda «hasta fecha por determinar»; sólo la versión vigente se anuncia como «Vigente desde».
- **Historial por cotejar** (`historial_parcial`, punto ámbar, 3 artículos: 82, 116 y 122): el texto vigente es el del consolidado, pero el PDF de la SCJN es anterior a la última reforma (`DOF 07-10-2026`; véase `docs/reporte_grupo_a.md`). Los Arts. 2, 10, 20, 22, 35, 53, 56 y 73 se re-extrajeron por coordenadas desde su PDF y pasaron a verificados (7, 3, 10, 8, 9, 5, 7 y 95 versiones); los Arts. 3, 72, 99, 100, 107, 109 y 123 (Grupo B) se cerraron con el texto de la Cámara una vez demostrado que la diferencia con el último bloque SCJN era de extracción (`docs/reporte_cierre_grupo_b.md`). El detalle de la integración está en `docs/reporte_integracion_historial.json`.
- **Notas de extracción**: `nota_extraccion` documenta en una versión lo que se descontó o retiró del bloque SCJN (línea de corte de página repetida, párrafo duplicado, anotación editorial). Las **34 versiones fusionadas** por el separador lineal en 21 artículos quedaron íntegramente separadas mediante extracción por coordenadas desde sus PDFs (`docs/reporte_versiones_fusionadas.md`); `extraccion_pendiente: true` sólo permanece en 4 versiones del Art. 100 (`v5`–`v8`) donde se retiró la línea repetida de pie de página proveniente del Art. 99 («extracción por cotejar»).
- **Vigente, historial en construcción** (punto azul): estado soportado; hoy no queda ninguno.
- La etiqueta `tema` de cada artículo es editorial, no forma parte del texto oficial.

## Estado del CCDF (Código Civil para el Distrito Federal)

- **Estructura base publicada** en `ccdf/index.html`: Libros Primero a Cuarto (el Cuarto con sus cuatro Partes), 30 Títulos y las Disposiciones Preliminares. Los rangos de artículos de cada Título provienen de la estructura general del Código y están marcados «por cotejar»; los Capítulos se añadirán al cotejar el texto consolidado.
- **Texto normativo: ninguno todavía.** El texto consolidado recomendado (DOCX de la Consejería Jurídica y de Servicios Legales de la CDMX) no está en el repositorio ni tiene hash verificado (`sources_registry.json`, pendiente `ccdf-docx-hash`), así que los 10 artículos de muestra (1, 22, 146, 308, 1281, 1502, 1792, 1834, 2248, 2999) se publican como fichas «pendiente de cotejo», con `noindex` y fuera del sitemap. No se reproduce ni parafrasea texto normativo sin cotejar.
- **Última reforma verificada:** 20-08-2026, Gaceta Oficial de la Ciudad de México 1929 Bis (arts. 1834 y 1502-I), en vigor desde el 21-08-2026 (`docs/brief-gpt-cierre-ccdf-vigente.md`, `docs/ccdf-sources-registry-entry.json`). La fecha 02-09-2026 del Congreso se conserva como conflicto de metadatos y no genera evento.
- **Siguiente paso:** con el DOCX (y su SHA-256) en mano, cotejar rangos, añadir Capítulos y cargar `texto` en `ccdf.json`; `build.py` hace el resto. El historial del CCDF queda fuera de alcance por ahora.

## Cómo añadir o corregir un artículo

1. En `cpeum.json`, dentro de `articulos`, añade la clave con el número (`"7"`) y sus `versiones` ordenadas de la más antigua a la vigente. Campos de cada versión: `id`, `etiqueta`, `publicacion` (fecha DOF), `vigencia_desde`, `vigencia_hasta` (`null` si está vigente), `capitulo`, `texto`; opcionalmente `dof_url` y `dof_etiqueta` (enlace «Ver decreto en el DOF»), `tipo` (`original`, `reforma`, `fe_de_erratas`), `vigencia_verificada` y `vigencia_nota`.
2. En `texto`, separa párrafos con una línea en blanco. Los apartados (`A. `), fracciones (`I. `) e incisos (`a) `) se reconocen por su prefijo y se formatean solos.
3. Marca `"estado": "verificado"` sólo cuando el texto esté cotejado con el DOF; mientras tanto, `"prototipo"`.
4. Ejecuta `python3 build.py` para regenerar `index.html`, las páginas estáticas, `sitemap.xml` y `robots.txt`. Sólo los artículos con `"estado": "verificado"` obtienen página estática; los de prototipo nunca se publican como página indexable.

Fuentes oficiales para la carga: [Leyes Federales Vigentes](https://www.diputados.gob.mx/LeyesBiblio/) y [Reformas constitucionales por artículo](https://www.diputados.gob.mx/LeyesBiblio/ref/cpeum_art.htm) (Cámara de Diputados), más el DOF de cada reforma.

## Publicar gratis

GitHub Pages: *Settings → Pages → Deploy from a branch → `main` / root*. El sitio queda en `https://<usuario>.github.io/legislacion-mx-prototipo/` y el Artículo 1o. en `https://<usuario>.github.io/legislacion-mx-prototipo/articulos/1.html`.

Las URL absolutas de `canonical`, `sitemap.xml` y `robots.txt` salen de la URL base: por defecto `https://jatovarv.github.io/legislacion-mx-prototipo`. Con dominio propio, regenera con `python3 build.py --site-url https://tudominio.mx` y vuelve a hacer commit.

## Páginas estáticas (SEO)

El navegador interactivo usa rutas por `#`, que Google indexa mal; las páginas de `articulos/` son las que captan tráfico de búsqueda. Cada una lleva título y descripción propios, `canonical`, Open Graph y datos estructurados (`schema.org/Legislation` + `BreadcrumbList`), y enlaza al navegador interactivo para comparar versiones. Hay un comentario HTML que marca el hueco reservado para publicidad.

## Siguiente paso recomendado para monetizar

Resolver los 3 artículos «historial por cotejar» (82, 116 y 122, cuando la SCJN actualice sus PDF al DOF 07-10-2026) y las 9 versiones con fecha pendiente (más la del Art. 81) (PDF de la SCJN a mano), y cargar `dof_url` por versión desde la cronología oficial de la Cámara, como en el Art. 4o.
