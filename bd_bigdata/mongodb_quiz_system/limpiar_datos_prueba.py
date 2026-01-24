"""
Script para limpiar los datos de prueba
Útil si quieres empezar de cero después de las verificaciones
"""

import sqlite3
import os

DB_PATH = 'mongodb_quiz.db'

def limpiar_datos_prueba():
    """Limpia exámenes, respuestas y progreso, pero mantiene categorías y preguntas"""

    print("="*60)
    print("🗑️  LIMPIEZA DE DATOS DE PRUEBA")
    print("="*60)

    if not os.path.exists(DB_PATH):
        print("\n❌ No se encontró la base de datos mongodb_quiz.db")
        return

    respuesta = input("\n⚠️  ¿Estás seguro de que quieres ELIMINAR todos los exámenes y progreso?\n"
                     "Esto no afectará las preguntas ni categorías.\n"
                     "(s/n): ")

    if respuesta.lower() != 's':
        print("\n❌ Operación cancelada. No se eliminó nada.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Contar datos antes de eliminar
        cursor.execute("SELECT COUNT(*) FROM exams")
        total_exams = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM exam_answers")
        total_answers = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(questions_answered) FROM study_progress")
        total_progress = cursor.fetchone()[0] or 0

        print(f"\n📊 Datos a eliminar:")
        print(f"   • {total_exams} exámenes")
        print(f"   • {total_answers} respuestas")
        print(f"   • {total_progress} preguntas de progreso acumulado")

        # Eliminar datos
        print("\n🗑️  Eliminando datos...")

        cursor.execute("DELETE FROM exam_answers")
        print("   ✓ Respuestas eliminadas")

        cursor.execute("DELETE FROM exams")
        print("   ✓ Exámenes eliminados")

        # Resetear progreso (poner en 0 en lugar de eliminar)
        cursor.execute("""
            UPDATE study_progress
            SET questions_answered = 0,
                questions_correct = 0,
                last_study_date = NULL
        """)
        print("   ✓ Progreso reseteado")

        conn.commit()
        conn.close()

        print("\n✅ Limpieza completada exitosamente!")
        print("\n📝 Datos conservados:")
        print("   • 9 categorías de MongoDB")
        print("   • 520 preguntas")
        print("\n🆕 Ahora puedes empezar de cero con tus exámenes reales.")

    except Exception as e:
        print(f"\n❌ Error durante la limpieza: {e}")
        return

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    limpiar_datos_prueba()
