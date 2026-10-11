# legislacion-mx-prototipo

Prototipo navegable de legislación mexicana vigente e histórica (CPEUM, después CCCDMX), con el historial de versiones **desplegado bajo cada artículo**. Navegación inspirada en [Légifrance](https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006070721/). Objetivo: sitio público monetizable con tráfico útil, a costo cero.

## Qué hay

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Sitio completo (HTML + CSS + JS, sin dependencias). Lleva los datos embebidos, así que funciona abriéndolo en local (doble clic) o publicado en GitHub Pages. |
| `cpeum.json` | **Fuente de datos editable**: estructura completa de la CPEUM (Títulos, Capítulos, Secciones y rangos de artículos) + los artículos cargados con sus versiones. |
| `cpeum-art-1.json` | Golden case del Artículo 1o. (4 versiones cotejadas con DOF/SCJN). `cpeum.json` lo incluye verbatim. |
| `build.py` | Inyecta `cpeum.json` dentro de `index.html` (entre `<!-- DATA:START -->` y `<!-- DATA:END -->`). Sin dependencias: `python3 build.py`. |

## Funciones del prototipo

- Árbol lateral con la estructura completa de la Constitución (136 artículos), buscador por número o tema, y menú deslizable en móvil.
- Artículo con migas de pan, metadatos (vigencia, DOF, capítulo), navegación anterior/siguiente y enlaces permanentes (`#/art/1`, `#/art/1/v/v2`).
- Botón **Ver historial**: despliega bajo el artículo la lista de versiones (más reciente primero); al elegir una se muestra su **texto íntegro** y, opcionalmente, los cambios resaltados respecto a la versión anterior.
- Selector **«Versión vigente al»** (como el *Version en vigueur au* de Légifrance): muestra el texto que regía en la fecha elegida y la conserva al saltar entre artículos (`?al=AAAA-MM-DD`).
- Fecha de consulta en cabecera y pie, estilos de impresión, enlace copiable.

## Estado de los textos

- **Verificado**: sólo el Artículo 1o. (golden case).
- **Prototipo** (punto ámbar y aviso visible): artículos 2o., 3o., 4o., 5o., 6o., 39, 123 y 135. Su texto es **simulado** y sus fechas son ilustrativas; sirven únicamente para probar la navegación, el historial y el diseño. No reproducen el texto constitucional.
- **Pendiente** (punto gris): el resto; navegables, sin texto.
- La etiqueta `tema` de cada artículo es editorial, no forma parte del texto oficial.

## Cómo añadir o corregir un artículo

1. En `cpeum.json`, dentro de `articulos`, añade la clave con el número (`"7"`) y sus `versiones` ordenadas de la más antigua a la vigente. Campos de cada versión: `id`, `etiqueta`, `publicacion` (fecha DOF), `vigencia_desde`, `vigencia_hasta` (`null` si está vigente), `capitulo`, `texto`.
2. En `texto`, separa párrafos con una línea en blanco. Los apartados (`A. `), fracciones (`I. `) e incisos (`a) `) se reconocen por su prefijo y se formatean solos.
3. Marca `"estado": "verificado"` sólo cuando el texto esté cotejado con el DOF; mientras tanto, `"prototipo"`.
4. Ejecuta `python3 build.py` para regenerar `index.html`.

Fuentes oficiales para la carga: [Leyes Federales Vigentes](https://www.diputados.gob.mx/LeyesBiblio/) y [Reformas constitucionales por artículo](https://www.diputados.gob.mx/LeyesBiblio/ref/cpeum_art.htm) (Cámara de Diputados), más el DOF de cada reforma.

## Publicar gratis

GitHub Pages: *Settings → Pages → Deploy from a branch → `main` / root*. El sitio queda en `https://<usuario>.github.io/legislacion-mx-prototipo/`.

## Siguiente paso recomendado para monetizar

El prototipo es una sola página con rutas por `#`, que Google indexa mal. Para captar tráfico de búsqueda, generar con `build.py` una página estática por artículo (`cpeum/articulo-1.html`, …) con la misma interfaz y datos; el esquema de `cpeum.json` ya lo permite.
