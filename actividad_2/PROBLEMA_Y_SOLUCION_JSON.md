# Problema Estructural en act-2-companies.json

## Fecha
2025-12-29

## Archivo Afectado
`/Users/willdev/github/UNIR/maestria/actividad_2/act-2-companies.json`

## Descripción del Problema

El archivo `act-2-companies.json` contiene **18,801 objetos JSON** pero tiene un **problema estructural crítico** que lo hace inválido como documento JSON estándar.

### Formato Incorrecto (NDJSON / JSON Lines)

El archivo está en formato **NDJSON** (Newline Delimited JSON) o **JSON Lines**, donde cada línea es un objeto JSON independiente:

```json
{ "_id" : { "$oid" : "52cdef7c4bab8bd675297d8a" }, "name" : "Wetpaint", ... }
{ "_id" : { "$oid" : "52cdef7c4bab8bd675297d8b" }, "name" : "AdventNet", ... }
{ "_id" : { "$oid" : "52cdef7c4bab8bd675297d8c" }, "name" : "Zoho", ... }
```

### Problemas Específicos

1. **Falta de array contenedor**: No hay corchetes `[` al inicio y `]` al final
2. **Falta de separadores**: Los objetos no están separados por comas `,`
3. **Incompatibilidad con parsers JSON estándar**: La mayoría de herramientas esperan un array JSON válido

### Verificación del Error

```bash
python3 -m json.tool act-2-companies.json
# Resultado: JSON inválido (error de parsing)
```

## Solución Implementada

Se creó un script Python (`fix_json_structure.py`) que realiza la conversión de NDJSON a JSON array válido.

### Proceso de Corrección

1. **Lectura línea por línea**: Cada línea se parsea como un objeto JSON independiente
2. **Acumulación en array**: Todos los objetos se agregan a una lista Python
3. **Serialización válida**: Se genera un archivo JSON con estructura de array

### Script de Corrección

El script `fix_json_structure.py` realiza:

- Lee 18,801 líneas individuales
- Valida cada objeto JSON
- Genera un array JSON válido
- Maneja errores de parsing (si existen)
- Proporciona estadísticas del proceso

## Resultados

### Archivo Original
- **Formato**: NDJSON (JSON Lines)
- **Tamaño**: 74.6 MB
- **Objetos**: 18,801
- **Estado**: ❌ JSON inválido
- **Líneas**: 18,801

### Archivo Corregido
- **Nombre**: `act-2-companies-fixed.json`
- **Formato**: JSON Array válido
- **Objetos**: 18,801
- **Estado**: ✅ JSON válido
- **Estructura**: `[ {...}, {...}, ... ]`

### Estadísticas del Proceso
- Objetos procesados: **18,801**
- Errores encontrados: **0**
- Tasa de éxito: **100%**

## Verificación de la Solución

```bash
python3 -m json.tool act-2-companies-fixed.json > /dev/null
# Resultado: ✓ JSON válido
```

## Diferencias Estructurales

### Antes (NDJSON - Inválido)
```json
{ "name": "Company1", ... }
{ "name": "Company2", ... }
{ "name": "Company3", ... }
```

### Después (JSON Array - Válido)
```json
[
  { "name": "Company1", ... },
  { "name": "Company2", ... },
  { "name": "Company3", ... }
]
```

## Archivos Generados

1. **fix_json_structure.py**: Script de corrección documentado
2. **act-2-companies-fixed.json**: Archivo JSON corregido
3. **PROBLEMA_Y_SOLUCION_JSON.md**: Este documento de documentación

## Uso del Archivo Corregido

### Python
```python
import json

with open('act-2-companies-fixed.json', 'r') as f:
    companies = json.load(f)

print(f"Total empresas: {len(companies)}")
```

### JavaScript/Node.js
```javascript
const companies = require('./act-2-companies-fixed.json');
console.log(`Total empresas: ${companies.length}`);
```

### Herramientas CLI
```bash
# Contar objetos
jq 'length' act-2-companies-fixed.json

# Filtrar empresas
jq '.[].name' act-2-companies-fixed.json

# Buscar por nombre
jq '.[] | select(.name == "Digg")' act-2-companies-fixed.json
```

## Notas Técnicas

- El formato NDJSON es válido para streaming y procesamiento línea por línea
- Para uso general en aplicaciones web/móviles, se requiere formato JSON array
- El archivo original puede conservarse si se necesita procesamiento streaming
- La conversión es reversible sin pérdida de datos

## Recomendaciones

1. Usar `act-2-companies-fixed.json` para aplicaciones estándar
2. Conservar el original si se necesita procesamiento por lotes
3. Para archivos muy grandes, considerar usar bases de datos en lugar de JSON
4. Implementar validación JSON en pipelines de datos futuros

## Autor de la Corrección
Claude Code (Sonnet 4.5)

## Herramientas Utilizadas
- Python 3
- Módulo `json` (biblioteca estándar)
- Validación: `python3 -m json.tool`
