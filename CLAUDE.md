# Proyecto Maestría UNIR

Este repositorio contiene los trabajos y proyectos desarrollados durante la maestría en UNIR.

## Estructura del Proyecto

### 📁 `/actividad_2`
Actividad 2 del curso, enfocada en procesamiento de datos JSON.

**Contenido:**
- `act-2-companies.json` - Dataset original de empresas
- `act-2-companies-fixed.json` - Dataset corregido y normalizado
- `fix_json_structure.py` - Script Python para corrección de estructura JSON
- `PROBLEMA_Y_SOLUCION_JSON.md` - Documentación del problema y solución implementada

### 📁 `/bd_bigdata`
Bases de datos y Big Data. Contiene datasets procesados, notebooks de limpieza de datos y proyectos relacionados con MongoDB.

**Contenido:**
- `limpieza de datos.ipynb` - Jupyter Notebook con procesos de limpieza de datos
- `csv_a_json.py` - Script de conversión de CSV a JSON
- `Documentación-20260121/` - Carpeta con documentación del proyecto

**Datasets limpios:**
- `data_act_01_limpio.csv` / `data_act_01_limpio.json`
- `infovuelos_limpio.csv` / `infovuelos_limpio.json`
- `listings_limpio.csv` / `listings_limpio.json`
- `neighbourhoods.csv`

**Datasets originales:**
- `infovuelos_sample.csv`
- `listings.csv`
- `dataset_limpio.csv`

#### 📁 `/bd_bigdata/mongodb_quiz_system`
**Aplicación Web de Evaluación de MongoDB**

Sistema de evaluación interactivo desarrollado con Python y SQLite para estudiar MongoDB de forma dinámica.

**Estado: COMPLETO Y FUNCIONAL** ✅

**Tecnologías:**
- **Backend:** Python 3.11 + Flask 3.1.2
- **Base de datos:** SQLite
- **Frontend:** HTML5/CSS3/JavaScript + Bootstrap
- **Ambiente:** Conda (ambiente: data)

**Propósito:**
Aplicación web educativa que permite estudiar MongoDB y Big Data mediante exámenes dinámicos de 20 preguntas aleatorias. El sistema incluye:
- Banco de 610 preguntas (conceptuales y de sintaxis)
- Preguntas basadas en datasets reales (infovuelos, listings, data_act_01)
- Explicaciones detalladas cuando se falla una pregunta
- Sistema de 18 categorías (9 de MongoDB + 9 tests del curso)
- Selección de categorías para personalizar exámenes

---

#### **Arquitectura de la Aplicación**

```
mongodb_quiz_system/
├── app.py                      # Aplicación Flask principal
├── database.py                 # ✅ Gestión de base de datos SQLite
├── quiz_generator.py           # Generador de exámenes con filtro de categorías
├── question_bank.py            # Banco de 610 preguntas (520 MongoDB + 90 tests)
├── init_db.py                  # Script para inicializar la BD
├── extraer_preguntas_tests.py  # Preguntas extraídas de los tests PDF
├── mongodb_quiz.db             # Base de datos SQLite (auto-generada)
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── quiz.js
└── templates/                  # Templates HTML
    ├── index.html              # Página principal
    ├── exam.html               # Página de examen
    ├── results.html            # Resultados con explicaciones
    └── progress.html           # Dashboard de progreso
```

---

#### **Esquema de Base de Datos**

**Tabla: `categories`**
- Categorías de preguntas basadas en sesiones de MongoDB
- Campos: id, name, description, session_number

**Tabla: `questions`**
- Banco de 610 preguntas con opciones múltiples (a-e)
- Tipos: 'conceptual' y 'syntax'
- Dificultades: 'easy', 'medium', 'hard'
- Campos: id, category_id, question_type, question_text, option_a-e, correct_answer, explanation, dataset_reference, difficulty

**Tabla: `exams`**
- Histórico de exámenes realizados (20 preguntas por examen)
- Campos: id, exam_date, total_questions, correct_answers, score, selected_categories (JSON), time_spent_seconds

**Tabla: `exam_answers`**
- Respuestas individuales por examen
- Campos: id, exam_id, question_id, user_answer, is_correct, time_spent_seconds

**Tabla: `study_progress`**
- Progreso del usuario por categoría
- Campos: id, category_id, questions_answered, questions_correct, last_study_date

---

#### **Categorías de Preguntas (18 categorías, 610 preguntas totales)**

**Categorías MongoDB (1-9): 520 preguntas**
1. **Instalación y Entorno** (Sesión 3) - 31 preguntas
2. **CRUD - Create** (Sesión 3) - 58 preguntas
3. **CRUD - Read** (Sesión 3) - 78 preguntas
4. **CRUD - Update** (Sesión 4) - 59 preguntas
5. **CRUD - Delete** (Sesión 4) - 49 preguntas
6. **Agregación** (Sesiones 4, 5, 6) - 103 preguntas
7. **MongoDB + Python (PyMongo)** (Sesión 6) - 62 preguntas
8. **Otras Funcionalidades** (Sesión 7) - 40 preguntas
9. **Operaciones Avanzadas** (Sesión 8) - 40 preguntas

**Categorías Tests del Curso (10-18): 90 preguntas**
10. **Test 1 - Fundamentos de Datos** - 10 preguntas
11. **Test 2 - NoSQL y MongoDB** - 10 preguntas
12. **Test 3 - MongoDB CRUD** - 10 preguntas
13. **Test 4 - Agregación MongoDB** - 10 preguntas
14. **Test 5 - Backup, Índices, Replicación y Sharding** - 10 preguntas
15. **Test 6 - Drivers MongoDB** - 10 preguntas
16. **Test 7 - Cassandra** - 10 preguntas
17. **Test 8 - Grafo (Neo4j)** - 10 preguntas
18. **Test 9 - Redis** - 10 preguntas

**Distribución de preguntas:**
- 52.3% preguntas de sintaxis (basadas en datasets reales)
- 47.7% preguntas conceptuales
- Dificultades: 23.8% fácil, 51.8% medio, 24.4% difícil

---

#### **Funcionalidades Implementadas**

✅ **Base de datos SQLite completa**
- Esquema de 5 tablas con relaciones
- Funciones CRUD para todas las entidades
- Sistema de estadísticas y progreso
- 610 preguntas distribuidas en 18 categorías

✅ **Módulo `database.py`**
- Inicialización de base de datos
- Gestión de categorías
- Gestión de preguntas (insertar, obtener aleatorias, filtrar por categoría)
- Gestión de exámenes y respuestas
- Sistema de progreso por categoría
- Estadísticas generales

✅ **Módulo `question_bank.py`**
- 610 preguntas completas (291 conceptuales, 319 de sintaxis)
- Distribución: 145 fáciles, 316 medias, 149 difíciles
- Basadas en datasets reales (infovuelos, listings, data_act_01)
- Incluye preguntas de tests del curso (90 preguntas de Tests 1-9)

✅ **Módulo `quiz_generator.py`**
- Generador de exámenes aleatorios de 20 preguntas
- Filtrado por categorías seleccionadas
- Balanceo automático de dificultades
- Resúmenes de distribución

✅ **Script `init_db.py`**
- Inicialización completa de base de datos
- Carga automática de 610 preguntas
- Configuración de 18 categorías (9 MongoDB + 9 Tests)
- Inicialización de progreso

✅ **Script `extraer_preguntas_tests.py`**
- Preguntas extraídas de los Tests 1-9 en formato Python
- Función de formateo para integración con question_bank.py
- 90 preguntas de tests del curso (10 por test)

✅ **Aplicación Flask `app.py`**
- Ruta principal (/) con selector de categorías
- Generación y presentación de exámenes (/start_exam)
- Procesamiento de respuestas (/submit_exam)
- Dashboard de progreso (/progress)
- Historial de exámenes (/history)
- Detalle de exámenes específicos (/exam/<id>)
- Manejo de errores (404, 500)

✅ **Templates HTML (9 archivos)**
- base.html: Template base con navbar Bootstrap
- index.html: Página principal con selección de categorías
- exam.html: Interfaz de examen con timer y progreso
- results.html: Resultados detallados con explicaciones
- progress.html: Dashboard con gráficos de progreso
- history.html: Lista de exámenes anteriores
- exam_detail.html: Detalles de examen específico
- 404.html, 500.html: Páginas de error personalizadas

✅ **Frontend completo**
- static/css/style.css: Estilos personalizados MongoDB
- static/js/quiz.js: Funcionalidad interactiva JavaScript
- Diseño responsive con Bootstrap 5
- Validación de formularios en tiempo real
- LocalStorage para recuperar respuestas
- Animaciones y transiciones suaves

✅ **Documentación**
- README.md completo con instrucciones de uso
- .gitignore configurado
- Comentarios en código

---

#### **Características del Sistema de Exámenes**

- **Exámenes aleatorios:** 20 preguntas por examen
- **Combinación de categorías:** Selección múltiple de categorías antes del examen
- **Validación y explicaciones:** Respuesta correcta + explicación del error
- **Historial:** Almacenamiento persistente de todos los exámenes
- **Estadísticas:** Dashboard con progreso por categoría
- **Datasets reales:** Preguntas de sintaxis basadas en infovuelos_limpio, listings_limpio, data_act_01_limpio
- **Interfaz moderna:** Responsive con Bootstrap 5, iconos Bootstrap Icons
- **Timer:** Contador de tiempo durante el examen
- **Progreso en vivo:** Barra de progreso de respuestas contestadas
- **Recuperación:** LocalStorage para no perder respuestas al refrescar

---

#### **Cómo usar la aplicación**

1. **Inicializar la base de datos (primera vez):**
   ```bash
   cd bd_bigdata/mongodb_quiz_system
   python init_db.py
   ```

2. **Iniciar el servidor:**
   ```bash
   python app.py
   ```

3. **Abrir en navegador:**
   ```
   http://127.0.0.1:5001
   ```

4. **Flujo de uso:**
   - Selecciona categorías o deja vacío para todas
   - Responde el examen de 20 preguntas
   - Revisa resultados con explicaciones
   - Consulta tu progreso en /progress
   - Ve historial en /history

---

#### **Tecnologías utilizadas**

- **Backend:** Python 3.11 + Flask 3.1.2
- **Base de datos:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript ES6
- **Framework CSS:** Bootstrap 5.3
- **Iconos:** Bootstrap Icons 1.11
- **Arquitectura:** MVC (Model-View-Controller)

### 📁 `/vision_computador`
Proyectos y ejercicios relacionados con Visión por Computador.

**Contenido:**
- `Python de cero a heroe/` - Recursos y ejercicios de Python aplicado a visión computacional

## Estado del Repositorio

**Última actualización:** 2026-01-25
**Último commit:** Integración Test 9 - Redis - 610 preguntas totales

## Notas de Desarrollo

- Los datasets han pasado por procesos de limpieza y normalización
- Se mantienen versiones en CSV y JSON de los datasets principales
- El proyecto mongodb_quiz_system está completo y funcional con 610 preguntas en 18 categorías
- Se han integrado los Tests 1-9 del curso al sistema de quiz (90 preguntas adicionales)
- Pendiente: Integrar Test 10 (último test del curso)
