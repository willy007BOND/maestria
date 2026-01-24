"""
quiz_generator.py - Generador de exámenes para MongoDB Quiz System

Funcionalidades:
- Generar exámenes de 20 preguntas aleatorias
- Filtrar preguntas por categorías seleccionadas
- Balancear distribución de dificultades
- Evitar repetición de preguntas en el mismo examen
"""

import random
from typing import List, Dict, Optional
from database import get_random_questions, get_all_categories

class QuizGenerator:
    """Clase para generar exámenes personalizados"""

    def __init__(self, num_questions: int = 20):
        """
        Inicializa el generador de quiz

        Args:
            num_questions: Número de preguntas por examen (default: 20)
        """
        self.num_questions = num_questions

    def generate_exam(self, selected_categories: Optional[List[int]] = None) -> List[Dict]:
        """
        Genera un examen con preguntas aleatorias

        Args:
            selected_categories: Lista de IDs de categorías a incluir (None = todas)

        Returns:
            Lista de diccionarios con las preguntas del examen
        """
        # Obtener preguntas aleatorias (database.py ya maneja el filtro de categorías)
        questions = get_random_questions(
            limit=self.num_questions,
            category_ids=selected_categories
        )

        # Mezclar el orden de las preguntas
        random.shuffle(questions)

        return questions

    def generate_balanced_exam(
        self,
        selected_categories: Optional[List[int]] = None,
        difficulty_distribution: Optional[Dict[str, float]] = None
    ) -> List[Dict]:
        """
        Genera un examen con distribución balanceada de dificultades

        Args:
            selected_categories: Lista de IDs de categorías a incluir
            difficulty_distribution: Dict con % por dificultad
                                   Ej: {'easy': 0.3, 'medium': 0.5, 'hard': 0.2}

        Returns:
            Lista de preguntas balanceadas por dificultad
        """
        if difficulty_distribution is None:
            # Distribución por defecto: 30% fácil, 50% medio, 20% difícil
            difficulty_distribution = {
                'easy': 0.3,
                'medium': 0.5,
                'hard': 0.2
            }

        # Calcular cantidad de preguntas por dificultad
        num_easy = int(self.num_questions * difficulty_distribution.get('easy', 0))
        num_medium = int(self.num_questions * difficulty_distribution.get('medium', 0))
        num_hard = self.num_questions - num_easy - num_medium

        # Obtener todas las preguntas disponibles (filtradas por categoría)
        all_questions = get_random_questions(
            limit=1000,  # Obtener un pool grande
            category_ids=selected_categories
        )

        # Separar por dificultad
        easy_questions = [q for q in all_questions if q['difficulty'] == 'easy']
        medium_questions = [q for q in all_questions if q['difficulty'] == 'medium']
        hard_questions = [q for q in all_questions if q['difficulty'] == 'hard']

        # Seleccionar aleatoriamente
        selected_questions = []

        if len(easy_questions) >= num_easy:
            selected_questions.extend(random.sample(easy_questions, num_easy))
        else:
            selected_questions.extend(easy_questions)

        if len(medium_questions) >= num_medium:
            selected_questions.extend(random.sample(medium_questions, num_medium))
        else:
            selected_questions.extend(medium_questions)

        if len(hard_questions) >= num_hard:
            selected_questions.extend(random.sample(hard_questions, num_hard))
        else:
            selected_questions.extend(hard_questions)

        # Si no alcanzamos 20 preguntas, completar con las que faltan
        if len(selected_questions) < self.num_questions:
            remaining = self.num_questions - len(selected_questions)
            used_ids = {q['id'] for q in selected_questions}
            available = [q for q in all_questions if q['id'] not in used_ids]
            if available:
                additional = random.sample(available, min(remaining, len(available)))
                selected_questions.extend(additional)

        # Mezclar el orden final
        random.shuffle(selected_questions)

        return selected_questions[:self.num_questions]

    def get_category_summary(self, questions: List[Dict]) -> Dict[int, int]:
        """
        Obtiene un resumen de cuántas preguntas hay por categoría

        Args:
            questions: Lista de preguntas del examen

        Returns:
            Dict {category_id: count}
        """
        summary = {}
        for q in questions:
            cat_id = q['category_id']
            summary[cat_id] = summary.get(cat_id, 0) + 1
        return summary

    def get_difficulty_summary(self, questions: List[Dict]) -> Dict[str, int]:
        """
        Obtiene un resumen de cuántas preguntas hay por dificultad

        Args:
            questions: Lista de preguntas del examen

        Returns:
            Dict {difficulty: count}
        """
        summary = {'easy': 0, 'medium': 0, 'hard': 0}
        for q in questions:
            summary[q['difficulty']] += 1
        return summary

    def get_type_summary(self, questions: List[Dict]) -> Dict[str, int]:
        """
        Obtiene un resumen de cuántas preguntas hay por tipo

        Args:
            questions: Lista de preguntas del examen

        Returns:
            Dict {question_type: count}
        """
        summary = {'conceptual': 0, 'syntax': 0}
        for q in questions:
            summary[q['question_type']] += 1
        return summary

def get_available_categories() -> List[Dict]:
    """
    Obtiene todas las categorías disponibles

    Returns:
        Lista de diccionarios con info de categorías
    """
    return get_all_categories()

def format_exam_for_display(questions: List[Dict]) -> List[Dict]:
    """
    Formatea las preguntas del examen para mostrar al usuario
    (sin revelar la respuesta correcta ni explicación)

    Args:
        questions: Lista de preguntas completas

    Returns:
        Lista de preguntas sin respuestas correctas
    """
    formatted = []
    for i, q in enumerate(questions, 1):
        formatted.append({
            'number': i,
            'id': q['id'],
            'question_text': q['question_text'],
            'option_a': q['option_a'],
            'option_b': q['option_b'],
            'option_c': q['option_c'],
            'option_d': q['option_d'],
            'option_e': q['option_e'],
            'difficulty': q['difficulty'],
            'question_type': q['question_type'],
            'dataset_reference': q.get('dataset_reference')
        })
    return formatted

# Funciones auxiliares para uso directo
def create_quick_exam(category_ids: Optional[List[int]] = None) -> List[Dict]:
    """
    Función de conveniencia para crear un examen rápido de 20 preguntas

    Args:
        category_ids: Lista de IDs de categorías (None = todas)

    Returns:
        Lista de 20 preguntas aleatorias
    """
    generator = QuizGenerator(num_questions=20)
    return generator.generate_exam(selected_categories=category_ids)

def create_balanced_exam(category_ids: Optional[List[int]] = None) -> List[Dict]:
    """
    Función de conveniencia para crear un examen balanceado

    Args:
        category_ids: Lista de IDs de categorías (None = todas)

    Returns:
        Lista de 20 preguntas con distribución balanceada de dificultad
    """
    generator = QuizGenerator(num_questions=20)
    return generator.generate_balanced_exam(selected_categories=category_ids)

# Test del módulo
if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST DEL GENERADOR DE EXÁMENES")
    print("="*60)

    # Crear un examen de prueba
    print("\n📝 Generando examen de 20 preguntas...")
    generator = QuizGenerator(num_questions=20)

    # Examen con todas las categorías
    exam = generator.generate_exam()
    print(f"✓ Examen generado con {len(exam)} preguntas")

    # Mostrar resúmenes
    cat_summary = generator.get_category_summary(exam)
    diff_summary = generator.get_difficulty_summary(exam)
    type_summary = generator.get_type_summary(exam)

    print("\n📊 Resumen por categoría:")
    for cat_id, count in sorted(cat_summary.items()):
        print(f"  Categoría {cat_id}: {count} preguntas")

    print("\n⭐ Resumen por dificultad:")
    for diff, count in diff_summary.items():
        print(f"  {diff.capitalize()}: {count} preguntas")

    print("\n🏷️  Resumen por tipo:")
    for q_type, count in type_summary.items():
        print(f"  {q_type.capitalize()}: {count} preguntas")

    # Examen balanceado
    print("\n\n📝 Generando examen balanceado...")
    balanced_exam = generator.generate_balanced_exam()
    diff_summary_balanced = generator.get_difficulty_summary(balanced_exam)

    print("\n⭐ Distribución de dificultad (balanceado):")
    for diff, count in diff_summary_balanced.items():
        percentage = (count / len(balanced_exam)) * 100
        print(f"  {diff.capitalize()}: {count} ({percentage:.0f}%)")

    print("\n✅ Tests completados\n")
