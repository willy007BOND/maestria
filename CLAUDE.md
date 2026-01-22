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

**Estado: En Desarrollo Activo** ⚙️

**Tecnologías:**
- **Backend:** Python 3.11 + Flask 3.1.2
- **Base de datos:** SQLite
- **Frontend:** HTML5/CSS3/JavaScript + Bootstrap
- **Ambiente:** Conda (ambiente: data)

**Propósito:**
Aplicación web educativa que permite estudiar MongoDB mediante exámenes dinámicos de 20 preguntas aleatorias. El sistema incluye:
- Banco de ~500 preguntas (conceptuales y de sintaxis)
- Preguntas basadas en datasets reales (infovuelos, listings, data_act_01)
- Explicaciones detalladas cuando se falla una pregunta
- Sistema de categorías basado en las 9 sesiones de MongoDB
- Selección de categorías para personalizar exámenes

---

#### **Arquitectura de la Aplicación**

```
mongodb_quiz_system/
├── app.py                      # Aplicación Flask principal
├── database.py                 # ✅ Gestión de base de datos SQLite
├── quiz_generator.py           # Generador de exámenes con filtro de categorías
├── question_bank.py            # Banco de ~500 preguntas
├── init_db.py                  # Script para inicializar la BD
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
- Banco de ~500 preguntas con opciones múltiples (a-e)
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

#### **Categorías de Preguntas (9 categorías, ~520 preguntas totales)**

1. **Instalación y Entorno** (Sesión 3) - 30 preguntas
2. **CRUD - Create** (Sesión 3) - 60 preguntas
3. **CRUD - Read** (Sesión 3) - 80 preguntas
4. **CRUD - Update** (Sesión 4) - 60 preguntas
5. **CRUD - Delete** (Sesión 4) - 50 preguntas
6. **Agregación** (Sesiones 4, 5, 6) - 100 preguntas
7. **MongoDB + Python (PyMongo)** (Sesión 6) - 60 preguntas
8. **Otras Funcionalidades** (Sesión 7) - 40 preguntas
9. **Operaciones Avanzadas** (Sesión 8) - 40 preguntas

**Distribución de preguntas:**
- 60% preguntas de sintaxis (basadas en datasets reales)
- 40% preguntas conceptuales
- Dificultades: 30% fácil, 50% medio, 20% difícil

---

#### **Funcionalidades Implementadas**

✅ **Base de datos SQLite completa**
- Esquema de 5 tablas con relaciones
- Funciones CRUD para todas las entidades
- Sistema de estadísticas y progreso

✅ **Módulo `database.py`**
- Inicialización de base de datos
- Gestión de categorías
- Gestión de preguntas (insertar, obtener aleatorias, filtrar por categoría)
- Gestión de exámenes y respuestas
- Sistema de progreso por categoría
- Estadísticas generales

---

#### **Funcionalidades Pendientes**

🔄 **En progreso:**
- Generación de banco de ~500 preguntas

⏳ **Por implementar:**
- Módulo quiz_generator.py (selector de categorías)
- Aplicación Flask (app.py) con rutas
- Templates HTML (index, exam, results, progress)
- CSS y JavaScript para interactividad
- Script de inicialización (init_db.py)
- Pruebas de la aplicación completa

---

#### **Características del Sistema de Exámenes**

- **Exámenes aleatorios:** 20 preguntas por examen
- **Combinación de categorías:** Selección múltiple de categorías antes del examen
- **Validación y explicaciones:** Respuesta correcta + explicación del error
- **Historial:** Almacenamiento persistente de todos los exámenes
- **Estadísticas:** Dashboard con progreso por categoría
- **Datasets reales:** Preguntas de sintaxis basadas en infovuelos_limpio, listings_limpio, data_act_01_limpio

### 📁 `/vision_computador`
Proyectos y ejercicios relacionados con Visión por Computador.

**Contenido:**
- `Python de cero a heroe/` - Recursos y ejercicios de Python aplicado a visión computacional

## Estado del Repositorio

**Última actualización:** 2026-01-21
**Último commit:** Normalización de datos

## Notas de Desarrollo

- Los datasets han pasado por procesos de limpieza y normalización
- Se mantienen versiones en CSV y JSON de los datasets principales
- El proyecto mongodb_quiz_system está en fase de desarrollo inicial
