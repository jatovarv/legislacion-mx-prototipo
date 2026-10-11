# legislacion-mx-prototipo

Prototipo navegable de legislación mexicana vigente e histórica (CPEUM, después CCCDMX), con el historial de versiones **desplegado bajo cada artículo**. Navegación inspirada en [Légifrance](https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006070721/). Objetivo: sitio público monetizable con tráfico útil, a costo cero.

## Qué hay

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Navegador interactivo (HTML + CSS + JS, sin dependencias). Lleva los datos embebidos, así que funciona abriéndolo en local (doble clic) o publicado en GitHub Pages. |
| `articulos/N.html` | **Páginas estáticas para SEO**, una por artículo verificado (hoy `articulos/1.html` y `articulos/4.html`): texto vigente íntegro, fechas, enlace al DOF y versiones anteriores, legibles sin JavaScript. Generadas; no se editan a mano. |
| `sitemap.xml`, `robots.txt` | Para buscadores. Generados. |
| `cpeum.json` | **Fuente de datos editable**: estructura completa de la CPEUM (Títulos, Capítulos, Secciones y rangos de artículos) + los artículos cargados con sus versiones. |
| `cpeum-art-1.json` | Golden case del Artículo 1o. (4 versiones cotejadas con DOF/SCJN). `cpeum.json` lo incluye verbatim. |
| `cpeum-art-4.json` | Golden case del Artículo 4o.: 25 versiones (texto original, 23 reformas y 1 fe de erratas) extraídas del PDF «Historia del texto del artículo» de la SCJN y cotejadas con el texto consolidado de la Cámara de Diputados; el bloque `fuentes` documenta el método y las advertencias. |
| `build.py` | Genera todo lo anterior a partir de `cpeum.json`: inyecta los datos en `index.html` (entre `<!-- DATA:START -->` y `<!-- DATA:END -->`), escribe `articulos/N.html`, `sitemap.xml` y `robots.txt`. Sin dependencias: `python3 build.py`. |

## Funciones del prototipo

- Árbol lateral con la estructura completa de la Constitución (136 artículos), buscador por número o tema, y menú deslizable en móvil.
- Artículo con migas de pan, metadatos (vigencia, DOF, capítulo), navegación anterior/siguiente y enlaces permanentes (`#/art/1`, `#/art/1/v/v2`).
- Botón **Ver historial**: despliega bajo el artículo la lista de versiones (más reciente primero); al elegir una se muestra su **texto íntegro** y, opcionalmente, los cambios resaltados respecto a la versión anterior.
- Selector **«Versión vigente al»** (como el *Version en vigueur au* de Légifrance): muestra el texto que regía en la fecha elegida y la conserva al saltar entre artículos (`?al=AAAA-MM-DD`).
- Fecha de consulta en cabecera y pie, estilos de impresión, enlace copiable.

## Estado de los textos

- **Verificado**: Artículos 1o. y 4o. (golden cases). En el 4o., `vigencia_verificada: false` marca las versiones cuya entrada en vigor se asume al día siguiente de la publicación (regla general) porque el decreto sólo existe escaneado; la interfaz las señala con «vigencia por cotejar».
- **Prototipo** (punto ámbar y aviso visible): artículos 2o., 3o., 5o., 6o., 39, 123 y 135. Su texto es **simulado** y sus fechas son ilustrativas; sirven únicamente para probar la navegación, el historial y el diseño. No reproducen el texto constitucional.
- **Pendiente** (punto gris): el resto; navegables, sin texto.
- La etiqueta `tema` de cada artículo es editorial, no forma parte del texto oficial.

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

Cargar más artículos reales en `cpeum.json` con `"estado": "verificado"`: cada uno genera su página estática y entra al sitemap sin tocar código.
