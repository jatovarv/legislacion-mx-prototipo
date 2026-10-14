# Dictamen y propuesta de actualización — Arts. 82, 116 y 122

**Decreto:** DOF 07-10-2026, código 5800617  
**Materia:** nacionalidad única para el ejercicio de la titularidad de los Poderes Ejecutivos Federal y Locales  
**Fecha de revisión:** 14 de octubre de 2026  
**Base del repositorio examinada:** `main` en `c682cd37f28e03676065f0db0760b6fc0fc0b333`  
**Alcance:** dictamen documental y propuesta de actualización. **Este documento no modifica `cpeum.json`.**

> Todo el material está en el repositorio.

## 1. Conclusión ejecutiva

La reforma está **materialmente incorporada** en la última versión de los artículos 82, 116 y 122 que actualmente contiene `cpeum.json`. La inspección automática del archivo confirmó, después de normalizar únicamente espacios y saltos de línea, la presencia de todos los bloques literales publicados en el Decreto DOF 07-10-2026.

Por tanto, **no se propone reemplazar ni reescribir el campo `texto`**. La actualización necesaria es de procedencia y vigencia:

- cambiar `vigencia_verificada` de `false` a `true`;
- corregir `vigencia_nota`, porque la entrada en vigor ya no es una suposición: consta en el transitorio Primero;
- incorporar `fecha_inferida: false` y `origen_fecha: "decreto_dof"`;
- incorporar el enlace directo al DOF;
- actualizar la nota general de cada artículo para distinguir entre:
  1. texto y vigencia verificados por DOF/Cámara, y
  2. historial SCJN todavía pendiente de un PDF que incluya el bloque de 07-10-2026.

Los tres artículos deben conservar `estado: "historial_parcial"` mientras el PDF histórico de la SCJN permanezca desactualizado. El estado parcial describe la cobertura de esa fuente histórica, **no una duda sobre la vigencia del decreto**.

## 2. Jerarquía y fuentes

1. **Fuente normativa prevalente:** [Decreto DOF 07-10-2026, código 5800617](https://www.dof.gob.mx/nota_detalle.php?codigo=5800617&fecha=07/10/2026).
2. **Texto consolidado oficial:** [CPEUM, Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf), última reforma DOF 07-10-2026.
3. **Fuente histórica auxiliar:** PDFs `00_historia.pdf` de la SCJN.
4. **Trazabilidad interna:** `docs/reporte_grupo_a.md` y `docs/dictamen-grupo-a-dof-2026-10-07.md`.

No se detectó contradicción material entre el Decreto y el consolidado de la Cámara. La discrepancia con la SCJN es cronológica: sus PDFs terminan antes del 07-10-2026.

## 3. Vigencia y aplicabilidad

### Texto literal de los transitorios relevantes

```text
Primero. El presente Decreto entrará en vigor el día siguiente al de su publicación en el Diario Oficial de la Federación.

Segundo. Lo dispuesto en este Decreto será aplicable a partir del proceso electoral correspondiente al año 2028.

Tercero. Lo dispuesto en este Decreto no será aplicable a quienes se encuentren en ejercicio de los cargos a que este se refiere, a la fecha de su entrada en vigor.
```

### Dictamen temporal

- **Publicación:** `2026-10-07`.
- **Vigencia formal:** `2026-10-08`.
- **Aplicabilidad electoral:** a partir del proceso electoral correspondiente a `2028`.
- **Régimen de quienes ya ejercían el cargo:** exclusión prevista en el transitorio Tercero.

La fecha de vigencia y la fecha de aplicabilidad no deben confundirse ni almacenarse como si fueran equivalentes.

## 4. Texto literal de la reforma

Las transcripciones siguientes reproducen los bloques reformados o adicionados por el Decreto. Las notas de procedencia se presentan fuera de los bloques para no contaminar el texto normativo.

### 4.1. Artículo 82

**Operaciones del Decreto:** reforma del párrafo primero; reforma del primer párrafo de la fracción I; adición de los párrafos segundo y tercero de la fracción I.

```text
Para ser Presidente o Presidenta se requiere:

I. Ser ciudadano o ciudadana mexicana por nacimiento, en pleno goce de sus derechos, hijo o hija de padre o madre mexicanos; no tener ni adquirir otra nacionalidad y, en caso de tenerla renunciar a ella previo a solicitar su registro como candidato o candidata en los términos que establezca la ley, y haber residido en el país al menos durante veinte años.

Quien ejerza el cargo no podrá adquirir ni solicitar otra nacionalidad, ni invocar ante autoridad extranjera una nacionalidad distinta de la mexicana.

Quedan comprendidos en esta prohibición el uso de pasaporte o documento de identidad expedido por un Estado extranjero, el ejercicio de los derechos políticos inherentes a la ciudadanía ante este y el acogerse a su protección diplomática. La contravención de esta disposición se sancionará en los términos del Título Cuarto de esta Constitución.
```

**Evidencia de Cámara:** p. 88 de 416; marcas editoriales `Párrafo reformado DOF 07-10-2026` y `Fracción reformada DOF 01-07-1994, 07-10-2026`.

**Estado SCJN:** el PDF termina en `Texto vigente D.O.F. 01 de abril de 2025`; no contiene el bloque de 07-10-2026.

**Registro actual:** última versión `v12`; publicación y vigencia ya están almacenadas como `2026-10-07` y `2026-10-08`.

**Dictamen:** texto de la reforma ya incluido; metadatos DOF incompletos; PDF SCJN desactualizado.

### 4.2. Artículo 116

**Operaciones del Decreto:** reforma del párrafo quinto de la fracción I; adición de un párrafo sexto.

```text
Sólo podrá ser gobernador o gobernadora constitucional de un Estado un ciudadano o ciudadana mexicana por nacimiento que no tenga ni adquiera otra nacionalidad y, en caso de tenerla renunciar a ella previo a solicitar su registro como candidato o candidata en los términos que establezca la ley, así como ser nativo o nativa de dicho Estado, o con residencia efectiva no menor de cinco años inmediatamente anteriores al día de los comicios, y tener 30 años cumplidos el día de la elección, o menos, si así lo establece la Constitución Política de la Entidad Federativa.

Quien ejerza el cargo no podrá adquirir ni solicitar otra nacionalidad, ni invocar ante autoridad extranjera una nacionalidad distinta de la mexicana. Quedan comprendidos en esta prohibición, entre otros supuestos, el uso de pasaporte o documento de identidad expedido por un Estado extranjero, el ejercicio de los derechos políticos inherentes a la ciudadanía ante este y el acogerse a su protección diplomática. La contravención de esta disposición se sancionará en los términos del Título Cuarto de esta Constitución, y de las constituciones de las entidades federativas.
```

**Evidencia de Cámara:** p. 129 de 416; marcas editoriales `Párrafo reformado DOF 26-09-2008, 07-10-2026` y `Párrafo adicionado DOF 07-10-2026`.

**Estado SCJN:** el PDF termina en `Texto vigente D.O.F. 02 de junio de 2026`; no contiene el bloque de 07-10-2026.

**Registro actual:** última versión `v23`; publicación y vigencia ya están almacenadas como `2026-10-07` y `2026-10-08`.

**Dictamen:** texto de la reforma ya incluido; metadatos DOF incompletos; PDF SCJN desactualizado.

### 4.3. Artículo 122

**Operaciones del Decreto:** reforma del párrafo segundo de la fracción III del Apartado A; adición de un párrafo tercero; recorrido del subsecuente.

```text
La Constitución Política de la Ciudad de México establecerá las facultades del Jefe o Jefa de Gobierno y los requisitos que deberá reunir quien aspire a ocupar dicho encargo. En todo caso se requerirá ser ciudadana o ciudadano mexicano por nacimiento y no tener ni adquirir otra nacionalidad y, en caso de tenerla renunciar a ella previo a solicitar su registro como candidato o candidata en los términos que establezca la ley.

Quien ejerza el cargo no podrá adquirir ni solicitar otra nacionalidad, ni invocar ante autoridad extranjera una nacionalidad distinta de la mexicana. Quedan comprendidos en esta prohibición, entre otros supuestos, el uso de pasaporte o documento de identidad expedido por un Estado extranjero, el ejercicio de los derechos políticos inherentes a la ciudadanía ante este y el acogerse a su protección diplomática. La contravención de esta disposición se sancionará en los términos del Título Cuarto de esta Constitución, y de la Constitución Política de la Ciudad de México.
```

**Evidencia de Cámara:** p. 139 de 416; marcas editoriales `Párrafo reformado DOF 07-10-2026` y `Párrafo adicionado DOF 07-10-2026`.

**Estado SCJN:** el PDF termina en `Texto vigente D.O.F. 02 de junio de 2026`; no contiene el bloque de 07-10-2026.

**Registro actual:** última versión `v22`; publicación y vigencia ya están almacenadas como `2026-10-07` y `2026-10-08`.

**Dictamen:** texto de la reforma ya incluido; metadatos DOF incompletos; PDF SCJN desactualizado.

## 5. Separación entre texto normativo y notas editoriales

### Texto normativo

Sólo debe residir en `versiones[].texto`. En esta propuesta no se modifica porque el texto literal de los tres artículos ya coincide con los bloques del Decreto.

### Metadatos y notas editoriales

Deben permanecer fuera de `texto`:

- `publicacion`;
- `vigencia_desde`;
- `vigencia_verificada`;
- `vigencia_nota`;
- `fecha_inferida`;
- `origen_fecha`;
- `dof_url`;
- `dof_etiqueta`;
- `fuente_url`;
- `fuente_etiqueta`;
- `notas_camara`;
- la nota general del artículo sobre el PDF pendiente de la SCJN.

## 6. Discrepancias y escalamiento

### Sin discrepancia material

- DOF y Cámara coinciden en los pasajes reformados.
- Los últimos objetos de `cpeum.json` contienen todos los bloques literales, después de normalizar únicamente espacios y saltos de línea.
- `publicacion` y `vigencia_desde` ya tienen los valores correctos.

### Discrepancia documental

Los PDFs históricos de la SCJN no incluyen el bloque DOF 07-10-2026:

| Artículo | Última fecha SCJN | Reforma DOF vigente |
|---:|:---:|:---:|
| 82 | 01-04-2025 | 07-10-2026 |
| 116 | 02-06-2026 | 07-10-2026 |
| 122 | 02-06-2026 | 07-10-2026 |

### Regla de escalamiento

Si una futura versión del PDF SCJN difiere del Decreto o del consolidado de Cámara, no debe sustituirse automáticamente el texto. Debe abrirse una incidencia de cotejo y prevalecer provisionalmente el Decreto publicado en el DOF.

## 7. Propuesta de diff para `cpeum.json`

La propuesta se entrega como **JSON Patch RFC 6902**:

```text
docs/propuesta-diff-cpeum-arts-82-116-122.jsonpatch
```

Características:

- sólo contiene rutas de los artículos `82`, `116` y `122`;
- incluye operaciones `test` para evitar aplicar el parche sobre una estructura distinta;
- no reemplaza ningún campo `texto`;
- mantiene `estado: "historial_parcial"`;
- verifica formalmente la vigencia desde `2026-10-08`;
- incorpora el enlace DOF solicitado;
- preserva la marca de pendiente de PDF SCJN.

## 8. Resultado propuesto

| Artículo | Texto | Publicación | Vigencia formal | DOF | Estado |
|---:|---|:---:|:---:|---|---|
| 82 | sin cambio; ya literal | 2026-10-07 | 2026-10-08, verificada | incorporado | historial_parcial |
| 116 | sin cambio; ya literal | 2026-10-07 | 2026-10-08, verificada | incorporado | historial_parcial |
| 122 | sin cambio; ya literal | 2026-10-07 | 2026-10-08, verificada | incorporado | historial_parcial |

## 9. Controles antes de integrar

1. Aplicar el JSON Patch sobre el `cpeum.json` de la base indicada.
2. Confirmar que todas las operaciones `test` pasan.
3. Validar los 136 artículos con `docs/cpeum-articulo-historial.schema.json`.
4. Confirmar que sólo cambiaron los objetos `articulos.82`, `articulos.116` y `articulos.122`.
5. Ejecutar `python3 build.py`.
6. Verificar que los golden cases de los artículos 1 y 4 permanezcan intactos.
7. Revisar que el enlace DOF renderice correctamente.
