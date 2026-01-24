# 🔍 Guía de Verificación del Sistema

Esta guía te ayuda a verificar que el progreso y el historial se almacenen correctamente en la base de datos.

---

## ✅ Verificación Automática

### Opción 1: Verificar estado actual de la BD

```bash
conda activate data
python verificar_bd.py
```

**Esto mostrará:**
- ✅ Categorías configuradas (9 esperadas)
- ✅ Preguntas cargadas (520 esperadas)
- ✅ Historial de exámenes realizados
- ✅ Respuestas individuales registradas
- ✅ Progreso de estudio por categoría
- ✅ Estadísticas generales

### Opción 2: Prueba de almacenamiento completa

```bash
conda activate data
python test_almacenamiento.py
```

**Esta prueba:**
1. Genera 20 preguntas aleatorias
2. Simula un examen completo (70% correctas)
3. Guarda el examen en la BD
4. Guarda las 20 respuestas individuales
5. Actualiza el progreso por categoría
6. Verifica que todo se guardó correctamente

✅ Si ves "PRUEBA EXITOSA", el sistema funciona perfectamente.

---

## 🧪 Verificación Manual

### Paso 1: Realizar un examen real

1. Inicia el servidor:
   ```bash
   ./start_server.sh
   ```

2. Abre tu navegador en: `http://127.0.0.1:5001`

3. Selecciona algunas categorías (o déjalas todas)

4. Responde el examen de 20 preguntas

5. Envía el examen

### Paso 2: Verificar el historial

1. En la aplicación web, ve a **"Historial"** (History)

2. Deberías ver tu examen recién enviado con:
   - Fecha y hora
   - Puntuación obtenida
   - Número de preguntas correctas
   - Tiempo empleado

### Paso 3: Verificar el progreso

1. En la aplicación web, ve a **"Progreso"** (Progress)

2. Deberías ver:
   - Total de preguntas respondidas
   - Total de respuestas correctas
   - Precisión global
   - Progreso por cada categoría con:
     * Número de preguntas respondidas
     * Número de respuestas correctas
     * Porcentaje de precisión
     * Fecha de última actividad

### Paso 4: Verificar con el script

```bash
conda activate data
python verificar_bd.py
```

Deberías ver:
- Tu examen en el "HISTORIAL DE EXÁMENES"
- Las 20 respuestas en "RESPUESTAS INDIVIDUALES"
- Progreso actualizado en "PROGRESO DE ESTUDIO POR CATEGORÍA"

---

## 📊 Qué se almacena exactamente

### En la tabla `exams`:
```
✓ ID del examen
✓ Fecha y hora
✓ Total de preguntas (20)
✓ Respuestas correctas
✓ Puntuación (%)
✓ Categorías seleccionadas (JSON)
✓ Tiempo empleado (segundos)
```

### En la tabla `exam_answers`:
```
✓ ID de la respuesta
✓ ID del examen (relación)
✓ ID de la pregunta
✓ Respuesta del usuario (a-e)
✓ ¿Es correcta? (bool)
✓ Tiempo empleado en la pregunta
```

### En la tabla `study_progress`:
```
✓ ID de categoría
✓ Preguntas respondidas (acumulado)
✓ Preguntas correctas (acumulado)
✓ Última fecha de estudio
```

---

## 🔧 Solución de Problemas

### Problema: "No hay exámenes registrados"

**Solución:**
1. Asegúrate de haber enviado al menos un examen
2. Verifica que la BD existe: `ls -la mongodb_quiz.db`
3. Si no existe, ejecuta: `python init_db.py`

### Problema: Los datos no persisten

**Posible causa:** La BD se está recreando cada vez.

**Solución:**
1. No ejecutes `init_db.py` después de realizar exámenes
2. Verifica que `mongodb_quiz.db` tenga permisos de escritura
3. Verifica que no haya errores en la consola del servidor

### Problema: El progreso no se actualiza

**Verificación:**
```bash
python -c "
from database import get_study_progress_all
progress = get_study_progress_all()
for p in progress:
    if p['questions_answered'] > 0:
        print(f\"Cat {p['category_id']}: {p['questions_answered']} preguntas\")
"
```

---

## 📈 Comandos Útiles de Verificación

### Ver último examen:
```bash
python -c "
from database import get_exam_history
exams = get_exam_history(limit=1)
if exams:
    e = exams[0]
    print(f\"Examen #{e['id']}: {e['score']:.1f}% ({e['correct_answers']}/20)\")
else:
    print('No hay exámenes')
"
```

### Contar total de exámenes:
```bash
python -c "
import sqlite3
conn = sqlite3.connect('mongodb_quiz.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM exams')
print(f\"Total de exámenes: {cursor.fetchone()[0]}\")
conn.close()
"
```

### Ver progreso global:
```bash
python -c "
import sqlite3
conn = sqlite3.connect('mongodb_quiz.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT SUM(questions_answered) as ans, SUM(questions_correct) as cor FROM study_progress')
r = cursor.fetchone()
if r['ans'] > 0:
    print(f\"Respondidas: {r['ans']}, Correctas: {r['cor']}, Precisión: {(r['cor']/r['ans'])*100:.1f}%\")
conn.close()
"
```

---

## ✅ Checklist de Verificación Completa

Ejecuta esto después de realizar un examen:

```bash
# 1. Activar ambiente
conda activate data

# 2. Verificar BD completa
python verificar_bd.py

# 3. Revisar si hay datos
echo "Verificando exámenes..."
python -c "import sqlite3; c = sqlite3.connect('mongodb_quiz.db'); print(f\"Exámenes: {c.cursor().execute('SELECT COUNT(*) FROM exams').fetchone()[0]}\"); c.close()"

echo "Verificando respuestas..."
python -c "import sqlite3; c = sqlite3.connect('mongodb_quiz.db'); print(f\"Respuestas: {c.cursor().execute('SELECT COUNT(*) FROM exam_answers').fetchone()[0]}\"); c.close()"

echo "Verificando progreso..."
python -c "import sqlite3; c = sqlite3.connect('mongodb_quiz.db'); r = c.cursor().execute('SELECT SUM(questions_answered) FROM study_progress').fetchone(); print(f\"Preguntas respondidas: {r[0] if r[0] else 0}\"); c.close()"

echo "✅ Verificación completada"
```

---

## 🎯 Resultado Esperado

Después de realizar un examen, deberías ver:

```
✅ Exámenes registrados: 1 (o más)
✅ Respuestas registradas: 20 (por cada examen)
✅ Progreso actualizado en N categorías
✅ Estadísticas generales calculadas correctamente
```

Si ves todo esto, **el sistema funciona perfectamente** y puedes confiar en que tus datos se están guardando correctamente.

---

## 📞 Si algo no funciona

1. Revisa los logs del servidor Flask
2. Ejecuta `python verificar_bd.py` para diagnóstico
3. Asegúrate de que la BD tiene permisos de escritura
4. Verifica que estás usando el ambiente conda correcto (`data`)

---

**¡El sistema está diseñado para ser 100% confiable en el almacenamiento de datos!**
