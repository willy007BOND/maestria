"""
app.py - Aplicación Flask para MongoDB Quiz System

Rutas:
- /: Página principal con selección de categorías
- /exam: Página de examen con 20 preguntas
- /submit: Procesa respuestas y muestra resultados
- /progress: Dashboard de progreso y estadísticas
- /history: Historial de exámenes anteriores
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from datetime import datetime
from typing import List, Dict

from database import (
    get_all_categories,
    insert_exam,
    insert_exam_answer,
    get_question_by_id,
    update_study_progress,
    get_study_progress_all,
    get_exam_history
)
from quiz_generator import (
    QuizGenerator,
    format_exam_for_display,
    create_balanced_exam
)

app = Flask(__name__)
app.secret_key = 'mongodb-quiz-secret-key-2026'  # Cambiar en producción

# ============================================================
# RUTA PRINCIPAL: Selección de categorías
# ============================================================

@app.route('/')
def index():
    """Página principal con selección de categorías"""
    categories = get_all_categories()
    return render_template('index.html', categories=categories)

# ============================================================
# RUTA: Generar y mostrar examen
# ============================================================

@app.route('/start_exam', methods=['POST'])
def start_exam():
    """Genera un examen basado en las categorías seleccionadas"""

    # Obtener categorías seleccionadas del formulario
    selected_categories = request.form.getlist('categories')

    # Convertir a integers (si hay selección) o None (todas las categorías)
    if selected_categories:
        category_ids = [int(cat_id) for cat_id in selected_categories]
    else:
        category_ids = None

    # Generar examen balanceado
    generator = QuizGenerator(num_questions=20)
    exam_questions = generator.generate_balanced_exam(selected_categories=category_ids)

    # Formatear preguntas para display (sin respuestas correctas)
    formatted_questions = format_exam_for_display(exam_questions)

    # Guardar en sesión
    session['exam_questions'] = [q['id'] for q in exam_questions]
    session['selected_categories'] = category_ids if category_ids else []
    session['exam_start_time'] = datetime.now().isoformat()

    # Obtener resúmenes
    category_summary = generator.get_category_summary(exam_questions)
    difficulty_summary = generator.get_difficulty_summary(exam_questions)

    return render_template(
        'exam.html',
        questions=formatted_questions,
        category_summary=category_summary,
        difficulty_summary=difficulty_summary
    )

# ============================================================
# RUTA: Procesar respuestas y mostrar resultados
# ============================================================

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    """Procesa las respuestas del examen y muestra resultados"""

    # Obtener respuestas del usuario
    user_answers = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = int(key.replace('question_', ''))
            user_answers[question_id] = value

    # Obtener preguntas del examen de la sesión
    question_ids = session.get('exam_questions', [])
    selected_categories = session.get('selected_categories', [])
    exam_start_time = datetime.fromisoformat(session.get('exam_start_time'))

    # Calcular tiempo transcurrido
    time_spent = int((datetime.now() - exam_start_time).total_seconds())

    # Evaluar respuestas
    results = []
    correct_count = 0

    for question_id in question_ids:
        question = get_question_by_id(question_id)
        user_answer = user_answers.get(question_id, '')
        is_correct = user_answer == question['correct_answer']

        if is_correct:
            correct_count += 1

        results.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

    # Calcular score
    total_questions = len(question_ids)
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    # Guardar examen en BD
    exam_id = insert_exam(
        total_questions=total_questions,
        correct_answers=correct_count,
        score=score,
        selected_categories=json.dumps(selected_categories),
        time_spent_seconds=time_spent
    )

    # Guardar respuestas individuales y actualizar progreso por categoría
    category_stats = {}  # {category_id: {'answered': 0, 'correct': 0}}

    for result in results:
        question = result['question']
        category_id = question['category_id']

        # Insertar respuesta
        insert_exam_answer(
            exam_id=exam_id,
            question_id=question['id'],
            user_answer=result['user_answer'],
            is_correct=result['is_correct'],
            time_spent_seconds=time_spent // total_questions  # Promedio
        )

        # Acumular stats por categoría
        if category_id not in category_stats:
            category_stats[category_id] = {'answered': 0, 'correct': 0}
        category_stats[category_id]['answered'] += 1
        if result['is_correct']:
            category_stats[category_id]['correct'] += 1

    # Actualizar progreso de estudio
    for category_id, stats in category_stats.items():
        update_study_progress(
            category_id=category_id,
            questions_answered_delta=stats['answered'],
            questions_correct_delta=stats['correct']
        )

    # Limpiar sesión
    session.pop('exam_questions', None)
    session.pop('selected_categories', None)
    session.pop('exam_start_time', None)

    return render_template(
        'results.html',
        results=results,
        correct_count=correct_count,
        total_questions=total_questions,
        score=score,
        time_spent=time_spent,
        exam_id=exam_id
    )

# ============================================================
# RUTA: Dashboard de progreso
# ============================================================

@app.route('/progress')
def progress():
    """Muestra el progreso de estudio del usuario"""
    categories = get_all_categories()
    progress_data = get_study_progress_all()

    # Crear mapa de progreso por categoría
    progress_map = {p['category_id']: p for p in progress_data}

    # Combinar categorías con su progreso
    progress_list = []
    for category in categories:
        cat_id = category['id']
        prog = progress_map.get(cat_id, {
            'questions_answered': 0,
            'questions_correct': 0,
            'last_study_date': None
        })

        # Calcular porcentaje de éxito
        if prog['questions_answered'] > 0:
            success_rate = (prog['questions_correct'] / prog['questions_answered']) * 100
        else:
            success_rate = 0

        progress_list.append({
            'category': category,
            'answered': prog['questions_answered'],
            'correct': prog['questions_correct'],
            'success_rate': success_rate,
            'last_study_date': prog.get('last_study_date')
        })

    return render_template('progress.html', progress_list=progress_list)

# ============================================================
# RUTA: Historial de exámenes
# ============================================================

@app.route('/history')
def history():
    """Muestra el historial de exámenes realizados"""
    exams = get_exam_history(limit=20)

    # Formatear fechas y categorías
    for exam in exams:
        # Parsear categorías seleccionadas
        try:
            exam['categories'] = json.loads(exam['selected_categories']) if exam['selected_categories'] else []
        except:
            exam['categories'] = []

        # Formatear fecha
        if exam['exam_date']:
            try:
                dt = datetime.fromisoformat(exam['exam_date'])
                exam['formatted_date'] = dt.strftime('%d/%m/%Y %H:%M')
            except:
                exam['formatted_date'] = exam['exam_date']

    return render_template('history.html', exams=exams)

# ============================================================
# RUTA: Ver detalles de un examen específico
# ============================================================

@app.route('/exam/<int:exam_id>')
def view_exam(exam_id):
    """Muestra los detalles de un examen específico"""
    from database import get_exam_by_id, get_exam_answers

    exam = get_exam_by_id(exam_id)
    if not exam:
        return "Examen no encontrado", 404

    answers = get_exam_answers(exam_id)

    # Obtener preguntas completas
    results = []
    for answer in answers:
        question = get_question_by_id(answer['question_id'])
        results.append({
            'question': question,
            'user_answer': answer['user_answer'],
            'is_correct': answer['is_correct']
        })

    return render_template(
        'exam_detail.html',
        exam=exam,
        results=results
    )

# ============================================================
# API: Obtener categorías (JSON)
# ============================================================

@app.route('/api/categories')
def api_categories():
    """API endpoint para obtener categorías"""
    categories = get_all_categories()
    return jsonify(categories)

# ============================================================
# Manejador de errores
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ============================================================
# Punto de entrada
# ============================================================

if __name__ == '__main__':
    print("="*60)
    print("🚀 MONGODB QUIZ SYSTEM")
    print("="*60)
    print("\n📌 Servidor iniciando...")
    print("🌐 URL: http://127.0.0.1:5001")
    print("📊 Base de datos: mongodb_quiz.db")
    print("\n✨ Presiona Ctrl+C para detener el servidor\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
