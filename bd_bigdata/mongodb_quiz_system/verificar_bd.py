"""
Script de verificación de la base de datos
Muestra el contenido actual de exámenes, respuestas y progreso
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = 'mongodb_quiz.db'

def print_section(title):
    """Imprime un separador de sección"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def verificar_base_datos():
    """Verifica el contenido de la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ============================================================
    # 1. VERIFICAR CATEGORÍAS
    # ============================================================
    print_section("1. CATEGORÍAS")
    cursor.execute("SELECT * FROM categories ORDER BY id")
    categories = cursor.fetchall()

    print(f"\nTotal de categorías: {len(categories)}")
    for cat in categories:
        print(f"  {cat['id']}. {cat['name']} (Sesión {cat['session_number']})")

    # ============================================================
    # 2. VERIFICAR PREGUNTAS
    # ============================================================
    print_section("2. PREGUNTAS EN LA BASE DE DATOS")
    cursor.execute("SELECT COUNT(*) as total FROM questions")
    total_questions = cursor.fetchone()['total']
    print(f"\nTotal de preguntas: {total_questions}")

    cursor.execute("""
        SELECT category_id, COUNT(*) as count
        FROM questions
        GROUP BY category_id
        ORDER BY category_id
    """)
    for row in cursor.fetchall():
        cat_name = [c['name'] for c in categories if c['id'] == row['category_id']][0]
        print(f"  Categoría {row['category_id']} ({cat_name}): {row['count']} preguntas")

    # ============================================================
    # 3. VERIFICAR EXÁMENES
    # ============================================================
    print_section("3. HISTORIAL DE EXÁMENES")
    cursor.execute("SELECT COUNT(*) as total FROM exams")
    total_exams = cursor.fetchone()['total']
    print(f"\nTotal de exámenes realizados: {total_exams}")

    if total_exams > 0:
        cursor.execute("""
            SELECT id, exam_date, total_questions, correct_answers, score,
                   selected_categories, time_spent_seconds
            FROM exams
            ORDER BY exam_date DESC
            LIMIT 10
        """)
        exams = cursor.fetchall()

        print("\nÚltimos 10 exámenes:")
        for exam in exams:
            exam_date = exam['exam_date'][:19] if exam['exam_date'] else 'N/A'
            score = exam['score'] if exam['score'] is not None else 0
            correct = exam['correct_answers'] if exam['correct_answers'] is not None else 0
            total = exam['total_questions'] if exam['total_questions'] is not None else 20
            time_spent = exam['time_spent_seconds'] if exam['time_spent_seconds'] else 0

            try:
                cats = json.loads(exam['selected_categories']) if exam['selected_categories'] else []
                cats_str = f"{len(cats)} categorías" if cats else "Todas"
            except:
                cats_str = "N/A"

            print(f"\n  Examen #{exam['id']}")
            print(f"    Fecha: {exam_date}")
            print(f"    Resultado: {correct}/{total} correctas ({score:.1f}%)")
            print(f"    Tiempo: {time_spent//60}:{time_spent%60:02d}")
            print(f"    Categorías: {cats_str}")
    else:
        print("\n⚠️  No hay exámenes registrados todavía.")
        print("   Realiza un examen para verificar que se guarde correctamente.")

    # ============================================================
    # 4. VERIFICAR RESPUESTAS DE EXÁMENES
    # ============================================================
    print_section("4. RESPUESTAS INDIVIDUALES")
    cursor.execute("SELECT COUNT(*) as total FROM exam_answers")
    total_answers = cursor.fetchone()['total']
    print(f"\nTotal de respuestas registradas: {total_answers}")

    if total_answers > 0:
        cursor.execute("""
            SELECT exam_id, COUNT(*) as count,
                   SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
            FROM exam_answers
            GROUP BY exam_id
            ORDER BY exam_id DESC
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  Examen #{row['exam_id']}: {row['count']} respuestas ({row['correct']} correctas)")

    # ============================================================
    # 5. VERIFICAR PROGRESO DE ESTUDIO
    # ============================================================
    print_section("5. PROGRESO DE ESTUDIO POR CATEGORÍA")
    cursor.execute("""
        SELECT sp.*, c.name as category_name
        FROM study_progress sp
        JOIN categories c ON sp.category_id = c.id
        ORDER BY c.id
    """)
    progress_data = cursor.fetchall()

    if progress_data:
        total_answered = 0
        total_correct = 0

        print("\nProgreso por categoría:")
        for prog in progress_data:
            answered = prog['questions_answered'] if prog['questions_answered'] else 0
            correct = prog['questions_correct'] if prog['questions_correct'] else 0
            total_answered += answered
            total_correct += correct

            if answered > 0:
                accuracy = (correct / answered) * 100
                print(f"\n  {prog['category_name']}:")
                print(f"    Respondidas: {answered}")
                print(f"    Correctas: {correct}")
                print(f"    Precisión: {accuracy:.1f}%")
                if prog['last_study_date']:
                    print(f"    Última vez: {prog['last_study_date'][:19]}")
            else:
                print(f"\n  {prog['category_name']}: Sin actividad")

        if total_answered > 0:
            overall_accuracy = (total_correct / total_answered) * 100
            print(f"\n  📊 RESUMEN GENERAL:")
            print(f"    Total respondidas: {total_answered}")
            print(f"    Total correctas: {total_correct}")
            print(f"    Precisión global: {overall_accuracy:.1f}%")
    else:
        print("\n⚠️  No hay progreso registrado todavía.")

    # ============================================================
    # 6. ESTADÍSTICAS GENERALES
    # ============================================================
    print_section("6. ESTADÍSTICAS GENERALES")

    if total_exams > 0:
        cursor.execute("SELECT AVG(score) as avg_score, MAX(score) as best_score FROM exams WHERE score IS NOT NULL")
        stats = cursor.fetchone()
        avg_score = stats['avg_score'] if stats['avg_score'] else 0
        best_score = stats['best_score'] if stats['best_score'] else 0

        print(f"\nPromedio de puntuación: {avg_score:.1f}%")
        print(f"Mejor puntuación: {best_score:.1f}%")
        print(f"Total de exámenes: {total_exams}")

    conn.close()

    # ============================================================
    # 7. VERIFICAR INTEGRIDAD
    # ============================================================
    print_section("7. VERIFICACIÓN DE INTEGRIDAD")

    issues = []

    if total_questions != 520:
        issues.append(f"⚠️  Preguntas esperadas: 520, encontradas: {total_questions}")
    else:
        print(f"✅ Preguntas: {total_questions}/520")

    if len(categories) != 9:
        issues.append(f"⚠️  Categorías esperadas: 9, encontradas: {len(categories)}")
    else:
        print(f"✅ Categorías: {len(categories)}/9")

    if total_exams > 0:
        print(f"✅ Exámenes registrados: {total_exams}")
        print(f"✅ Respuestas registradas: {total_answers}")
    else:
        print("ℹ️  No hay exámenes todavía (normal si es primera vez)")

    if issues:
        print("\n⚠️  PROBLEMAS DETECTADOS:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ Base de datos íntegra y funcionando correctamente")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🔍 VERIFICACIÓN DE BASE DE DATOS - MongoDB Quiz System")
    print("="*60)

    try:
        verificar_base_datos()
        print("✅ Verificación completada exitosamente\n")
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}\n")
