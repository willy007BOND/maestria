# MongoDB Quiz System

Sistema de evaluación interactivo para estudiar MongoDB con 520 preguntas distribuidas en 9 categorías.

## Características

- **520 preguntas** de MongoDB (conceptuales y de sintaxis)
- **9 categorías** basadas en las sesiones del curso
- **Exámenes de 20 preguntas** con selección de categorías
- **Explicaciones detalladas** cuando fallas una pregunta
- **Sistema de progreso** por categoría
- **Historial de exámenes** realizados
- **Interfaz web moderna** con Bootstrap 5

## Distribución de Preguntas

### Por categoría:
1. **Instalación y Entorno** - 31 preguntas
2. **CRUD - Create** - 58 preguntas
3. **CRUD - Read** - 78 preguntas
4. **CRUD - Update** - 59 preguntas
5. **CRUD - Delete** - 49 preguntas
6. **Agregación** - 103 preguntas
7. **MongoDB + Python (PyMongo)** - 62 preguntas
8. **Otras Funcionalidades** - 40 preguntas
9. **Operaciones Avanzadas** - 40 preguntas

### Por tipo:
- Conceptuales: 201 (38.7%)
- Sintaxis: 319 (61.3%)

### Por dificultad:
- Fácil: 118 (22.7%)
- Media: 260 (50.0%)
- Difícil: 142 (27.3%)

## Requisitos

- Python 3.8+
- Flask 3.1.2
- SQLite (incluido en Python)

## Instalación

1. **Activar ambiente conda (si usas conda):**
   ```bash
   conda activate data
   ```

2. **Instalar dependencias:**
   ```bash
   pip install flask
   ```

3. **Inicializar la base de datos:**
   ```bash
   python init_db.py
   ```

   Esto creará el archivo `mongodb_quiz.db` con:
   - Las 9 categorías
   - Las 520 preguntas
   - Sistema de progreso inicializado

## Uso

### Método 1: Script de inicio rápido (Recomendado para macOS/Linux)

```bash
./start_server.sh
```

Este script automáticamente:
- Activa el ambiente conda 'data'
- Verifica si existe la BD (si no, la crea)
- Inicia el servidor Flask

### Método 2: Manual

1. **Activar ambiente conda:**
   ```bash
   conda activate data
   ```

2. **Iniciar el servidor:**
   ```bash
   python app.py
   ```

3. **Abrir en el navegador:**
   ```
   http://127.0.0.1:5000
   ```

### Flujo de uso de la aplicación:
- Selecciona las categorías que quieres estudiar (o déjalo vacío para todas)
- Responde el examen de 20 preguntas
- Revisa tus resultados y las explicaciones
- Consulta tu progreso por categoría
- Revisa el historial de exámenes anteriores

## Estructura del Proyecto

```
mongodb_quiz_system/
├── app.py                      # Aplicación Flask principal
├── database.py                 # Gestión de base de datos SQLite
├── quiz_generator.py           # Generador de exámenes
├── question_bank.py            # Banco de 520 preguntas
├── init_db.py                  # Script de inicialización
├── mongodb_quiz.db             # Base de datos SQLite (auto-generada)
├── README.md                   # Este archivo
├── static/
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   └── js/
│       └── quiz.js            # JavaScript interactivo
└── templates/
    ├── base.html              # Template base
    ├── index.html             # Página principal
    ├── exam.html              # Página de examen
    ├── results.html           # Resultados con explicaciones
    ├── progress.html          # Dashboard de progreso
    ├── history.html           # Historial de exámenes
    ├── exam_detail.html       # Detalle de examen específico
    ├── 404.html               # Página de error 404
    └── 500.html               # Página de error 500
```

## Funcionalidades de la Interfaz

### Página Principal (/)
- Selección de categorías para personalizar el examen
- Estadísticas del banco de preguntas
- Acceso rápido a progreso e historial

### Página de Examen (/exam)
- 20 preguntas aleatorias
- Indicador de tiempo transcurrido
- Barra de progreso de respuestas
- Validación antes de enviar

### Página de Resultados (/submit)
- Puntuación y estadísticas
- Revisión detallada pregunta por pregunta
- Explicaciones cuando fallas
- Indicador visual de respuestas correctas/incorrectas

### Dashboard de Progreso (/progress)
- Estadísticas globales
- Progreso por categoría con barras visuales
- Tasa de éxito por categoría

### Historial (/history)
- Lista de exámenes anteriores
- Puntuación y tiempo de cada examen
- Ver detalles de exámenes pasados

## Base de Datos

### Esquema SQLite

- **categories** - 9 categorías de MongoDB
- **questions** - 520 preguntas con opciones y explicaciones
- **exams** - Histórico de exámenes realizados
- **exam_answers** - Respuestas individuales por examen
- **study_progress** - Progreso del usuario por categoría

## Características Técnicas

- **Backend:** Flask 3.1.2
- **Base de datos:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Arquitectura:** MVC (Model-View-Controller)
- **Session management:** Flask sessions
- **Responsive design:** Compatible con móviles y tablets

## Desarrollo

### Agregar más preguntas

1. Edita `question_bank.py`
2. Agrega preguntas siguiendo el formato:
   ```python
   {
       "category_id": 1,  # 1-9
       "question_type": "conceptual",  # o "syntax"
       "question_text": "¿Pregunta?",
       "option_a": "Opción A",
       "option_b": "Opción B",
       "option_c": "Opción C",
       "option_d": "Opción D",
       "option_e": "Opción E",
       "correct_answer": "b",  # a, b, c, d, o e
       "explanation": "Explicación detallada...",
       "dataset_reference": "N/A",  # o nombre del dataset
       "difficulty": "medium"  # easy, medium, o hard
   }
   ```
3. Agrega las preguntas a `ALL_QUESTIONS`
4. Reinicializa la BD: `python init_db.py`

### Reiniciar la base de datos

Si quieres empezar de cero:

```bash
rm mongodb_quiz.db
python init_db.py
```

## Créditos

- **Desarrollado para:** Maestría UNIR
- **Curso:** Bases de Datos y Big Data
- **Tema:** MongoDB
- **Total de preguntas:** 520

## Licencia

Proyecto educativo para uso académico.
