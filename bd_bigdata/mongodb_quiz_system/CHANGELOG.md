# Changelog - MongoDB Quiz System

## [1.1.0] - 2026-01-24

### 🐛 Bugs Corregidos

#### Bug #1: Contador de preguntas sin responder calculaba mal
**Problema:**
- El cuadro emergente mostraba un número incorrecto de preguntas sin responder
- Fórmula incorrecta: `totalQuestions - checked.length / 5`
- Dividía el total de inputs marcados entre 5 en lugar de contar preguntas únicas

**Solución:**
```javascript
// Antes (incorrecto)
const unanswered = totalQuestions - document.querySelectorAll('input[type="radio"]:checked').length / 5;

// Ahora (correcto)
const answeredQuestions = new Set();
radioInputs.forEach(input => {
    if (input.checked) {
        answeredQuestions.add(input.name);
    }
});
const unanswered = totalQuestions - answeredQuestions.size;
```

**Resultado:** Ahora cuenta correctamente cuántas preguntas están sin responder.

---

#### Bug #2: Botón "Enviar examen" se quedaba en "Procesando..."
**Problema:**
- El botón cambiaba a "Procesando..." incluso si el usuario cancelaba el envío
- Causaba confusión porque parecía que el examen se estaba enviando
- Se ejecutaban dos validaciones (quiz.js y exam.html) causando conflictos

**Solución:**
1. Movida toda la validación a `exam.html` (un solo lugar)
2. Agregado flag `isSubmitting` para prevenir doble envío
3. El spinner solo se muestra DESPUÉS de que el usuario confirma
4. `quiz.js` excluye `#examForm` del handler genérico de formularios

**Código:**
```javascript
let isSubmitting = false;
document.getElementById('examForm').addEventListener('submit', function(e) {
    if (isSubmitting) return; // Ya se está enviando

    // Validar preguntas sin responder
    const unanswered = totalQuestions - answeredQuestions.size;
    if (unanswered > 0) {
        if (!confirm(`Tienes ${unanswered} pregunta(s) sin responder...`)) {
            e.preventDefault();
            return false; // Usuario canceló - NO mostrar spinner
        }
    }

    // Solo si llegamos aquí (confirmado)
    isSubmitting = true;
    // Mostrar spinner
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border...">Procesando...';
});
```

**Resultado:**
- El botón solo muestra "Procesando..." cuando realmente se está enviando
- Si el usuario cancela, el botón vuelve a su estado normal
- UX mejorada significativamente

---

### 📝 Archivos Modificados

- `templates/exam.html` - Validación y manejo de submit mejorado
- `static/js/quiz.js` - Eliminada validación duplicada, simplificado handler

---

### ✅ Verificación

Para probar los fixes:
1. Inicia el servidor: `./start_server.sh`
2. Ve a http://127.0.0.1:5001
3. Inicia un examen
4. Responde solo algunas preguntas (no todas)
5. Click en "Enviar examen"
6. Verifica que el contador muestre el número correcto
7. Cancela el envío
8. Verifica que el botón vuelva a su estado normal (NO "Procesando...")
9. Vuelve a enviar y confirma
10. Ahora sí debería mostrar "Procesando..." y enviar

---

## [1.0.0] - 2026-01-24

### 🎉 Lanzamiento Inicial

- 520 preguntas de MongoDB
- 9 categorías basadas en sesiones del curso
- Sistema de exámenes de 20 preguntas aleatorias
- Dashboard de progreso
- Historial de exámenes
- Interfaz web moderna con Bootstrap 5
- Base de datos SQLite
- Sistema de progreso por categoría

---

## Notas de Versión

### Versión Actual: 1.1.0

**Mejoras de UX:**
- ✅ Contador preciso de preguntas sin responder
- ✅ Botón de envío funciona correctamente
- ✅ Sin validaciones duplicadas
- ✅ Feedback visual mejorado

**Próximas mejoras planeadas:**
- Modo oscuro (dark mode)
- Exportar resultados a PDF
- Estadísticas más detalladas
- Modo de práctica (sin límite de tiempo)
- Filtros avanzados por dificultad
