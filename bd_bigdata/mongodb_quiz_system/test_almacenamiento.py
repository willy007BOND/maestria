"""
Script de prueba de almacenamiento
Simula un examen completo y verifica que se guarde correctamente
"""

import json
from database import (
    insert_exam,
    insert_exam_answer,
    get_question_by_id,
    update_study_progress,
    get_exam_by_id,
    get_exam_answers,
    get_study_progress_all,
    get_random_questions
)

def test_almacenamiento():
    """Prueba completa del sistema de almacenamiento"""

    print("="*60)
    print("🧪 PRUEBA DE ALMACENAMIENTO - MongoDB Quiz System")
    print("="*60)

    # ============================================================
    # PASO 1: Generar preguntas aleatorias
    # ============================================================
    print("\n📝 Paso 1: Generando 20 preguntas aleatorias...")
    questions = get_random_questions(limit=20, category_ids=None)

    if len(questions) != 20:
        print(f"❌ Error: Se esperaban 20 preguntas, se obtuvieron {len(questions)}")
        return False

    print(f"✅ Generadas {len(questions)} preguntas")

    # ============================================================
    # PASO 2: Simular respuestas
    # ============================================================
    print("\n✍️  Paso 2: Simulando respuestas del usuario...")

    # Simular que el usuario respondió correctamente el 70% de las preguntas
    user_answers = {}
    correct_count = 0

    for i, q in enumerate(questions):
        # Simular respuesta correcta para 70% de las preguntas
        if i < 14:  # 14 de 20 = 70%
            user_answers[q['id']] = q['correct_answer']  # Respuesta correcta
            correct_count += 1
        else:
            # Respuesta incorrecta (elegir cualquier opción que no sea la correcta)
            wrong_options = ['a', 'b', 'c', 'd', 'e']
            wrong_options.remove(q['correct_answer'])
            user_answers[q['id']] = wrong_options[0]

    print(f"✅ Simuladas {len(user_answers)} respuestas")
    print(f"   Correctas: {correct_count}/20 ({(correct_count/20)*100:.0f}%)")

    # ============================================================
    # PASO 3: Guardar examen
    # ============================================================
    print("\n💾 Paso 3: Guardando examen en la base de datos...")

    total_questions = 20
    score = (correct_count / total_questions) * 100
    selected_categories = []  # Todas las categorías
    time_spent = 180  # 3 minutos simulados

    exam_id = insert_exam(
        total_questions=total_questions,
        correct_answers=correct_count,
        score=score,
        selected_categories=json.dumps(selected_categories),
        time_spent_seconds=time_spent
    )

    print(f"✅ Examen guardado con ID: {exam_id}")

    # ============================================================
    # PASO 4: Guardar respuestas individuales
    # ============================================================
    print("\n📋 Paso 4: Guardando respuestas individuales...")

    category_stats = {}  # {category_id: {'answered': 0, 'correct': 0}}

    for q in questions:
        question_id = q['id']
        user_answer = user_answers[question_id]
        is_correct = (user_answer == q['correct_answer'])
        category_id = q['category_id']

        # Insertar respuesta
        insert_exam_answer(
            exam_id=exam_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_spent_seconds=time_spent // total_questions
        )

        # Acumular stats por categoría
        if category_id not in category_stats:
            category_stats[category_id] = {'answered': 0, 'correct': 0}
        category_stats[category_id]['answered'] += 1
        if is_correct:
            category_stats[category_id]['correct'] += 1

    print(f"✅ Guardadas {len(user_answers)} respuestas individuales")

    # ============================================================
    # PASO 5: Actualizar progreso de estudio
    # ============================================================
    print("\n📊 Paso 5: Actualizando progreso de estudio...")

    for category_id, stats in category_stats.items():
        update_study_progress(
            category_id=category_id,
            questions_answered_delta=stats['answered'],
            questions_correct_delta=stats['correct']
        )

    print(f"✅ Actualizado progreso de {len(category_stats)} categorías")

    # ============================================================
    # PASO 6: VERIFICAR que se guardó correctamente
    # ============================================================
    print("\n🔍 Paso 6: Verificando que los datos se guardaron...")

    # Verificar examen
    saved_exam = get_exam_by_id(exam_id)
    if not saved_exam:
        print("❌ Error: No se pudo recuperar el examen guardado")
        return False

    print(f"✅ Examen recuperado:")
    print(f"   - ID: {saved_exam['id']}")
    print(f"   - Fecha: {saved_exam['exam_date']}")
    print(f"   - Puntuación: {saved_exam['score']:.1f}%")
    print(f"   - Correctas: {saved_exam['correct_answers']}/{saved_exam['total_questions']}")

    # Verificar respuestas
    saved_answers = get_exam_answers(exam_id)
    if len(saved_answers) != 20:
        print(f"❌ Error: Se esperaban 20 respuestas, se recuperaron {len(saved_answers)}")
        return False

    print(f"✅ Respuestas recuperadas: {len(saved_answers)}/20")

    # Verificar progreso
    progress_data = get_study_progress_all()
    categories_with_progress = [p for p in progress_data if p['questions_answered'] > 0]

    print(f"✅ Progreso actualizado en {len(categories_with_progress)} categorías:")
    for prog in categories_with_progress:
        cat_id = prog['category_id']
        if cat_id in category_stats:
            expected = category_stats[cat_id]
            actual_answered = prog['questions_answered']
            actual_correct = prog['questions_correct']

            if actual_answered == expected['answered'] and actual_correct == expected['correct']:
                print(f"   ✓ Categoría {cat_id}: {actual_answered} preguntas ({actual_correct} correctas)")
            else:
                print(f"   ✗ Categoría {cat_id}: Datos no coinciden")
                return False

    # ============================================================
    # RESULTADO FINAL
    # ============================================================
    print("\n" + "="*60)
    print("✅ PRUEBA EXITOSA - TODO SE GUARDÓ CORRECTAMENTE")
    print("="*60)
    print("\nResumen:")
    print(f"  • Examen ID {exam_id} guardado")
    print(f"  • 20 respuestas registradas")
    print(f"  • Progreso actualizado en {len(categories_with_progress)} categorías")
    print(f"  • Puntuación: {score:.1f}%")
    print(f"  • Tiempo: {time_spent//60}:{time_spent%60:02d}")
    print("\n✅ El sistema de almacenamiento funciona perfectamente!")
    print("\n" + "="*60 + "\n")

    return True

if __name__ == "__main__":
    try:
        success = test_almacenamiento()
        if success:
            print("\n🎉 ¡Puedes confiar en que el sistema guarda todo correctamente!\n")
        else:
            print("\n⚠️  Hubo problemas con el almacenamiento. Revisa los errores arriba.\n")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}\n")
        import traceback
        traceback.print_exc()
