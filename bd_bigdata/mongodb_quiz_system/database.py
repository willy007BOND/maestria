"""
database.py - Módulo de gestión de base de datos SQLite para MongoDB Quiz System
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

DB_PATH = 'mongodb_quiz.db'

def get_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    return conn

def init_database():
    """Inicializa la base de datos creando todas las tablas"""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla: categories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            session_number INTEGER
        )
    ''')

    # Tabla: questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            question_type TEXT NOT NULL CHECK(question_type IN ('conceptual', 'syntax')),
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            option_e TEXT NOT NULL,
            correct_answer TEXT NOT NULL CHECK(correct_answer IN ('a', 'b', 'c', 'd', 'e')),
            explanation TEXT NOT NULL,
            dataset_reference TEXT,
            difficulty TEXT NOT NULL CHECK(difficulty IN ('easy', 'medium', 'hard')),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    # Tabla: exams
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_questions INTEGER DEFAULT 20,
            correct_answers INTEGER,
            score REAL,
            selected_categories TEXT,
            time_spent_seconds INTEGER
        )
    ''')

    # Tabla: exam_answers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exam_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            user_answer TEXT NOT NULL CHECK(user_answer IN ('a', 'b', 'c', 'd', 'e')),
            is_correct BOOLEAN NOT NULL,
            time_spent_seconds INTEGER,
            FOREIGN KEY (exam_id) REFERENCES exams (id),
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    ''')

    # Tabla: study_progress
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL UNIQUE,
            questions_answered INTEGER DEFAULT 0,
            questions_correct INTEGER DEFAULT 0,
            last_study_date TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

# ==================== FUNCIONES PARA CATEGORIES ====================

def insert_category(name: str, description: str, session_number: int) -> int:
    """Inserta una nueva categoría"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO categories (name, description, session_number) VALUES (?, ?, ?)',
        (name, description, session_number)
    )
    category_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return category_id

def get_all_categories() -> List[Dict]:
    """Obtiene todas las categorías"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY session_number')
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categories

def get_category_by_id(category_id: int) -> Optional[Dict]:
    """Obtiene una categoría por su ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ==================== FUNCIONES PARA QUESTIONS ====================

def insert_question(category_id: int, question_type: str, question_text: str,
                   option_a: str, option_b: str, option_c: str, option_d: str, option_e: str,
                   correct_answer: str, explanation: str,
                   dataset_reference: Optional[str] = None, difficulty: str = 'medium') -> int:
    """Inserta una nueva pregunta"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions
        (category_id, question_type, question_text, option_a, option_b, option_c,
         option_d, option_e, correct_answer, explanation, dataset_reference, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (category_id, question_type, question_text, option_a, option_b, option_c,
          option_d, option_e, correct_answer, explanation, dataset_reference, difficulty))
    question_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return question_id

def get_questions_by_category(category_id: int) -> List[Dict]:
    """Obtiene todas las preguntas de una categoría"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE category_id = ?', (category_id,))
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions

def get_random_questions(limit: int = 20, category_ids: Optional[List[int]] = None) -> List[Dict]:
    """Obtiene preguntas aleatorias, opcionalmente filtradas por categorías"""
    conn = get_connection()
    cursor = conn.cursor()

    if category_ids:
        placeholders = ','.join('?' * len(category_ids))
        query = f'''
            SELECT * FROM questions
            WHERE category_id IN ({placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        '''
        cursor.execute(query, (*category_ids, limit))
    else:
        cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT ?', (limit,))

    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions

def get_question_by_id(question_id: int) -> Optional[Dict]:
    """Obtiene una pregunta por su ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def count_questions_by_category(category_id: int) -> int:
    """Cuenta cuántas preguntas hay en una categoría"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM questions WHERE category_id = ?', (category_id,))
    count = cursor.fetchone()['count']
    conn.close()
    return count

def get_total_questions() -> int:
    """Obtiene el total de preguntas en la base de datos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM questions')
    count = cursor.fetchone()['count']
    conn.close()
    return count

# ==================== FUNCIONES PARA EXAMS ====================

def create_exam(selected_categories: List[int]) -> int:
    """Crea un nuevo examen"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO exams (selected_categories) VALUES (?)',
        (json.dumps(selected_categories),)
    )
    exam_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return exam_id

def finish_exam(exam_id: int, correct_answers: int, time_spent_seconds: int):
    """Finaliza un examen actualizando los resultados"""
    score = (correct_answers / 20) * 100
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE exams
        SET correct_answers = ?, score = ?, time_spent_seconds = ?
        WHERE id = ?
    ''', (correct_answers, score, time_spent_seconds, exam_id))
    conn.commit()
    conn.close()

def get_exam_by_id(exam_id: int) -> Optional[Dict]:
    """Obtiene un examen por su ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exams WHERE id = ?', (exam_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        exam = dict(row)
        exam['selected_categories'] = json.loads(exam['selected_categories'])
        return exam
    return None

def get_all_exams() -> List[Dict]:
    """Obtiene todos los exámenes ordenados por fecha"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exams ORDER BY exam_date DESC')
    exams = []
    for row in cursor.fetchall():
        exam = dict(row)
        exam['selected_categories'] = json.loads(exam['selected_categories'])
        exams.append(exam)
    conn.close()
    return exams

# ==================== FUNCIONES PARA EXAM_ANSWERS ====================

def insert_exam_answer(exam_id: int, question_id: int, user_answer: str,
                      is_correct: bool, time_spent_seconds: Optional[int] = None) -> int:
    """Inserta una respuesta de examen"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO exam_answers
        (exam_id, question_id, user_answer, is_correct, time_spent_seconds)
        VALUES (?, ?, ?, ?, ?)
    ''', (exam_id, question_id, user_answer, is_correct, time_spent_seconds))
    answer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return answer_id

def get_exam_answers(exam_id: int) -> List[Dict]:
    """Obtiene todas las respuestas de un examen con detalles de la pregunta"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ea.*, q.question_text, q.option_a, q.option_b, q.option_c,
               q.option_d, q.option_e, q.correct_answer, q.explanation,
               q.question_type, q.dataset_reference, c.name as category_name
        FROM exam_answers ea
        JOIN questions q ON ea.question_id = q.id
        JOIN categories c ON q.category_id = c.id
        WHERE ea.exam_id = ?
    ''', (exam_id,))
    answers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return answers

# ==================== FUNCIONES PARA STUDY_PROGRESS ====================

def update_study_progress(category_id: int, is_correct: bool):
    """Actualiza el progreso de estudio de una categoría"""
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si existe el registro
    cursor.execute('SELECT * FROM study_progress WHERE category_id = ?', (category_id,))
    existing = cursor.fetchone()

    if existing:
        # Actualizar
        cursor.execute('''
            UPDATE study_progress
            SET questions_answered = questions_answered + 1,
                questions_correct = questions_correct + ?,
                last_study_date = CURRENT_TIMESTAMP
            WHERE category_id = ?
        ''', (1 if is_correct else 0, category_id))
    else:
        # Insertar
        cursor.execute('''
            INSERT INTO study_progress
            (category_id, questions_answered, questions_correct, last_study_date)
            VALUES (?, 1, ?, CURRENT_TIMESTAMP)
        ''', (category_id, 1 if is_correct else 0))

    conn.commit()
    conn.close()

def get_study_progress() -> List[Dict]:
    """Obtiene el progreso de estudio de todas las categorías"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sp.*, c.name as category_name, c.session_number
        FROM study_progress sp
        JOIN categories c ON sp.category_id = c.id
        ORDER BY c.session_number
    ''')
    progress = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return progress

def get_category_stats(category_id: int) -> Dict:
    """Obtiene estadísticas detalladas de una categoría"""
    conn = get_connection()
    cursor = conn.cursor()

    # Total de preguntas en la categoría
    cursor.execute('SELECT COUNT(*) as total FROM questions WHERE category_id = ?', (category_id,))
    total_questions = cursor.fetchone()['total']

    # Progreso del usuario en esta categoría
    cursor.execute('SELECT * FROM study_progress WHERE category_id = ?', (category_id,))
    progress = cursor.fetchone()

    conn.close()

    if progress:
        progress_dict = dict(progress)
        progress_dict['total_questions'] = total_questions
        if progress_dict['questions_answered'] > 0:
            progress_dict['accuracy'] = (progress_dict['questions_correct'] / progress_dict['questions_answered']) * 100
        else:
            progress_dict['accuracy'] = 0
        return progress_dict
    else:
        return {
            'category_id': category_id,
            'total_questions': total_questions,
            'questions_answered': 0,
            'questions_correct': 0,
            'accuracy': 0,
            'last_study_date': None
        }

# ==================== FUNCIONES DE ESTADÍSTICAS GENERALES ====================

def get_overall_stats() -> Dict:
    """Obtiene estadísticas generales del usuario"""
    conn = get_connection()
    cursor = conn.cursor()

    # Total de exámenes
    cursor.execute('SELECT COUNT(*) as total FROM exams WHERE score IS NOT NULL')
    total_exams = cursor.fetchone()['total']

    # Promedio general
    cursor.execute('SELECT AVG(score) as avg_score FROM exams WHERE score IS NOT NULL')
    avg_score = cursor.fetchone()['avg_score'] or 0

    # Mejor score
    cursor.execute('SELECT MAX(score) as best_score FROM exams WHERE score IS NOT NULL')
    best_score = cursor.fetchone()['best_score'] or 0

    # Total de preguntas contestadas
    cursor.execute('SELECT SUM(questions_answered) as total FROM study_progress')
    total_answered = cursor.fetchone()['total'] or 0

    # Total de preguntas correctas
    cursor.execute('SELECT SUM(questions_correct) as total FROM study_progress')
    total_correct = cursor.fetchone()['total'] or 0

    conn.close()

    overall_accuracy = (total_correct / total_answered * 100) if total_answered > 0 else 0

    return {
        'total_exams': total_exams,
        'avg_score': round(avg_score, 2),
        'best_score': round(best_score, 2),
        'total_questions_answered': total_answered,
        'total_questions_correct': total_correct,
        'overall_accuracy': round(overall_accuracy, 2)
    }

if __name__ == '__main__':
    # Inicializar la base de datos si se ejecuta directamente
    init_database()
