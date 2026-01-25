"""
init_db.py - Script de inicialización de la base de datos MongoDB Quiz System

Este script:
1. Crea la base de datos y todas las tablas
2. Inserta las categorías (9 de MongoDB + categorías de tests)
3. Carga las preguntas del banco (520 originales + preguntas de tests)
4. Inicializa el progreso de estudio para cada categoría
"""

import sys
import os
from database import (
    init_database,
    insert_category,
    insert_question,
    get_connection
)
from question_bank import get_all_questions, get_question_stats

# Definición de las categorías (9 de MongoDB + categorías de tests)
CATEGORIES = [
    {
        "name": "Instalación y Entorno",
        "description": "Conceptos básicos de MongoDB, instalación, configuración y herramientas",
        "session_number": 3
    },
    {
        "name": "CRUD - Create",
        "description": "Operaciones de creación de documentos (insertOne, insertMany)",
        "session_number": 3
    },
    {
        "name": "CRUD - Read",
        "description": "Operaciones de lectura con find, filtros, proyecciones y operadores",
        "session_number": 3
    },
    {
        "name": "CRUD - Update",
        "description": "Operaciones de actualización (updateOne, updateMany, operadores $set, $inc, etc.)",
        "session_number": 4
    },
    {
        "name": "CRUD - Delete",
        "description": "Operaciones de eliminación (deleteOne, deleteMany)",
        "session_number": 4
    },
    {
        "name": "Agregación",
        "description": "Pipeline de agregación, stages ($match, $group, $project, $sort, etc.)",
        "session_number": 5
    },
    {
        "name": "MongoDB + Python (PyMongo)",
        "description": "Uso de PyMongo para interactuar con MongoDB desde Python",
        "session_number": 6
    },
    {
        "name": "Otras Funcionalidades",
        "description": "Índices, performance, validación de esquemas, transacciones",
        "session_number": 7
    },
    {
        "name": "Operaciones Avanzadas",
        "description": "Replicación, sharding, backup, seguridad y operaciones en producción",
        "session_number": 8
    },
    {
        "name": "Test 1 - Fundamentos de Datos",
        "description": "Preguntas sobre fundamentos de datos: datos vs información, calidad, captura, formatos (CSV, JSON, XML) y bases de datos",
        "session_number": 1
    },
    {
        "name": "Test 2 - NoSQL y MongoDB",
        "description": "Preguntas sobre bases de datos NoSQL, MongoDB, tipos de BD NoSQL, teorema CAP y patrones de diseño en MongoDB",
        "session_number": 2
    },
    {
        "name": "Test 3 - MongoDB CRUD",
        "description": "Preguntas sobre operaciones CRUD en MongoDB: comandos, herramientas GUI, inserción, actualización, eliminación y consultas",
        "session_number": 3
    },
    {
        "name": "Test 4 - Agregación MongoDB",
        "description": "Preguntas sobre funciones de agregación, Map-Reduce, framework de agregación, operadores y pipeline de agregación",
        "session_number": 4
    },
    {
        "name": "Test 5 - Backup, Índices, Replicación y Sharding",
        "description": "Preguntas sobre mongodump, mongorestore, índices, replica sets, sharding y arquitectura distribuida en MongoDB",
        "session_number": 5
    }
]

def check_if_already_initialized():
    """Verifica si la BD ya está inicializada"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except:
        return False

def initialize_categories():
    """Inserta las 9 categorías en la base de datos"""
    print("\n📁 Insertando categorías...")
    category_ids = {}

    for i, category in enumerate(CATEGORIES, 1):
        try:
            category_id = insert_category(
                name=category['name'],
                description=category['description'],
                session_number=category['session_number']
            )
            category_ids[i] = category_id
            print(f"  ✓ Categoría {i}: {category['name']}")
        except Exception as e:
            print(f"  ✗ Error en categoría {i}: {e}")
            return None

    return category_ids

def initialize_questions():
    """Inserta todas las preguntas del banco en la base de datos"""
    print("\n📝 Insertando preguntas...")
    questions = get_all_questions()

    total = len(questions)
    success_count = 0
    error_count = 0

    for i, q in enumerate(questions, 1):
        try:
            insert_question(
                category_id=q['category_id'],
                question_type=q['question_type'],
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                option_e=q['option_e'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                dataset_reference=q.get('dataset_reference'),
                difficulty=q['difficulty']
            )
            success_count += 1

            # Mostrar progreso cada 50 preguntas
            if i % 50 == 0:
                print(f"  Progreso: {i}/{total} preguntas insertadas...")

        except Exception as e:
            error_count += 1
            print(f"  ✗ Error en pregunta {i}: {e}")

    print(f"\n  ✓ {success_count} preguntas insertadas correctamente")
    if error_count > 0:
        print(f"  ✗ {error_count} preguntas con errores")

    return success_count

def initialize_study_progress():
    """Inicializa el progreso de estudio para cada categoría"""
    print("\n📊 Inicializando progreso de estudio...")
    conn = get_connection()
    cursor = conn.cursor()

    for i in range(1, len(CATEGORIES) + 1):  # Todas las categorías
        try:
            cursor.execute('''
                INSERT INTO study_progress (category_id, questions_answered, questions_correct)
                VALUES (?, 0, 0)
            ''', (i,))
            print(f"  ✓ Progreso inicializado para categoría {i}")
        except Exception as e:
            print(f"  ✗ Error en categoría {i}: {e}")

    conn.commit()
    conn.close()

def show_statistics():
    """Muestra estadísticas del banco de preguntas"""
    print("\n" + "="*60)
    print("📈 ESTADÍSTICAS DEL BANCO DE PREGUNTAS")
    print("="*60)

    stats = get_question_stats()

    print(f"\n📊 Total de preguntas: {stats['total']}")

    print("\n📁 Por categoría:")
    category_names = [cat['name'] for cat in CATEGORIES]
    for cat_id, count in sorted(stats['by_category'].items()):
        print(f"  {cat_id}. {category_names[cat_id-1]}: {count} preguntas")

    print("\n🏷️  Por tipo:")
    for q_type, count in stats['by_type'].items():
        percentage = (count / stats['total']) * 100
        print(f"  {q_type.capitalize()}: {count} ({percentage:.1f}%)")

    print("\n⭐ Por dificultad:")
    for difficulty, count in stats['by_difficulty'].items():
        percentage = (count / stats['total']) * 100
        print(f"  {difficulty.capitalize()}: {count} ({percentage:.1f}%)")

def main():
    """Función principal de inicialización"""
    print("="*60)
    print("🚀 MONGODB QUIZ SYSTEM - INICIALIZACIÓN DE BASE DE DATOS")
    print("="*60)

    # Verificar si ya está inicializada
    if check_if_already_initialized():
        print("\n⚠️  La base de datos ya parece estar inicializada.")
        response = input("¿Deseas reinicializarla? Esto borrará todos los datos (s/n): ")
        if response.lower() != 's':
            print("\n❌ Inicialización cancelada.")
            return

        # Eliminar archivo de BD existente
        if os.path.exists('mongodb_quiz.db'):
            os.remove('mongodb_quiz.db')
            print("✓ Base de datos anterior eliminada.")

    # Paso 1: Crear estructura de BD
    print("\n🗄️  Paso 1: Creando estructura de base de datos...")
    init_database()

    # Paso 2: Insertar categorías
    print("\n📂 Paso 2: Insertando categorías...")
    category_ids = initialize_categories()
    if not category_ids:
        print("\n❌ Error al insertar categorías. Abortando.")
        return

    # Paso 3: Insertar preguntas
    print("\n📝 Paso 3: Insertando preguntas del banco...")
    questions_inserted = initialize_questions()
    if questions_inserted == 0:
        print("\n❌ Error al insertar preguntas. Abortando.")
        return

    # Paso 4: Inicializar progreso
    print("\n📊 Paso 4: Inicializando progreso de estudio...")
    initialize_study_progress()

    # Mostrar estadísticas
    show_statistics()

    # Resumen final
    print("\n" + "="*60)
    print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print("\n🎯 La base de datos está lista para usar.")
    print("📌 Archivo: mongodb_quiz.db")
    print("🚀 Puedes iniciar la aplicación con: python app.py\n")

if __name__ == "__main__":
    main()
