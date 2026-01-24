/**
 * quiz.js - JavaScript functionality for MongoDB Quiz System
 */

// ============================================================
// General Utilities
// ============================================================

/**
 * Show a toast notification
 */
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-info-circle-fill me-2"></i>
            <div>${message}</div>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;

    document.body.appendChild(toast);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Confirm action with modal
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// ============================================================
// Exam Page Functionality
// ============================================================

/**
 * Initialize exam page features
 */
function initExamPage() {
    // Smooth scroll to question on click
    const questionCards = document.querySelectorAll('.question-card');
    questionCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            this.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    });

    // Highlight selected options
    const radioInputs = document.querySelectorAll('input[type="radio"]');
    radioInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Remove highlight from all options in this question
            const questionName = this.name;
            const allOptions = document.querySelectorAll(`input[name="${questionName}"]`);
            allOptions.forEach(opt => {
                opt.closest('.option-item').classList.remove('bg-light', 'border', 'border-success');
            });

            // Highlight selected option
            this.closest('.option-item').classList.add('bg-light', 'border', 'border-success');
        });
    });

    // Auto-save answers to localStorage
    saveAnswersToLocalStorage();
}

/**
 * Save user answers to localStorage (for recovery if page refreshes)
 */
function saveAnswersToLocalStorage() {
    const form = document.getElementById('examForm');
    if (!form) return;

    const inputs = form.querySelectorAll('input[type="radio"]');
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            const answers = {};
            const allInputs = form.querySelectorAll('input[type="radio"]:checked');
            allInputs.forEach(inp => {
                answers[inp.name] = inp.value;
            });
            localStorage.setItem('examAnswers', JSON.stringify(answers));
        });
    });

    // Load saved answers on page load
    const savedAnswers = localStorage.getItem('examAnswers');
    if (savedAnswers) {
        try {
            const answers = JSON.parse(savedAnswers);
            for (const [name, value] of Object.entries(answers)) {
                const input = form.querySelector(`input[name="${name}"][value="${value}"]`);
                if (input) {
                    input.checked = true;
                    input.dispatchEvent(new Event('change'));
                }
            }
        } catch (e) {
            console.error('Error loading saved answers:', e);
        }
    }
}

/**
 * Clear saved answers from localStorage
 */
function clearSavedAnswers() {
    localStorage.removeItem('examAnswers');
}

// ============================================================
// Progress Tracking
// ============================================================

/**
 * Update progress indicators
 */
function updateProgressIndicators() {
    const totalQuestions = document.querySelectorAll('.question-card').length;
    const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;

    // Update various progress elements
    const progressElements = document.querySelectorAll('[data-progress]');
    progressElements.forEach(elem => {
        const percentage = Math.round((answeredQuestions / totalQuestions) * 100);
        elem.textContent = `${answeredQuestions} / ${totalQuestions} (${percentage}%)`;
    });
}

// ============================================================
// Keyboard Navigation
// ============================================================

/**
 * Enable keyboard shortcuts for exam navigation
 */
function enableKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Numbers 1-5 for selecting options A-E
        if (e.key >= '1' && e.key <= '5') {
            const focusedCard = document.activeElement.closest('.question-card');
            if (focusedCard) {
                const options = focusedCard.querySelectorAll('input[type="radio"]');
                const index = parseInt(e.key) - 1;
                if (options[index]) {
                    options[index].checked = true;
                    options[index].dispatchEvent(new Event('change'));
                }
            }
        }

        // Arrow keys for navigation
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault();
            const cards = Array.from(document.querySelectorAll('.question-card'));
            const activeCard = document.activeElement.closest('.question-card');
            const currentIndex = cards.indexOf(activeCard);

            if (e.key === 'ArrowDown' && currentIndex < cards.length - 1) {
                cards[currentIndex + 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
                cards[currentIndex + 1].focus();
            } else if (e.key === 'ArrowUp' && currentIndex > 0) {
                cards[currentIndex - 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
                cards[currentIndex - 1].focus();
            }
        }
    });
}

// ============================================================
// Form Validation
// ============================================================

/**
 * Validate exam form before submission
 */
function validateExamForm() {
    const form = document.getElementById('examForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        const totalQuestions = document.querySelectorAll('.question-card').length;
        const answeredQuestions = new Set();

        document.querySelectorAll('input[type="radio"]:checked').forEach(input => {
            answeredQuestions.add(input.name);
        });

        const unanswered = totalQuestions - answeredQuestions.size;

        if (unanswered > 0) {
            const confirmSubmit = confirm(
                `Tienes ${unanswered} pregunta(s) sin responder.\n\n¿Estás seguro de que deseas enviar el examen?`
            );

            if (!confirmSubmit) {
                e.preventDefault();
                return false;
            }
        }

        // Clear saved answers on successful submission
        clearSavedAnswers();
    });
}

// ============================================================
// Results Page Functionality
// ============================================================

/**
 * Initialize results page features
 */
function initResultsPage() {
    // Animate score display
    animateScore();

    // Enable collapsible explanations
    enableCollapsibleExplanations();
}

/**
 * Animate the score counter
 */
function animateScore() {
    const scoreElement = document.querySelector('[data-score]');
    if (!scoreElement) return;

    const targetScore = parseFloat(scoreElement.dataset.score);
    let currentScore = 0;
    const increment = targetScore / 50;
    const duration = 1000; // 1 second

    const timer = setInterval(() => {
        currentScore += increment;
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(timer);
        }
        scoreElement.textContent = currentScore.toFixed(1) + '%';
    }, duration / 50);
}

/**
 * Enable collapsible explanations for incorrect answers
 */
function enableCollapsibleExplanations() {
    const explanations = document.querySelectorAll('.explanation-content');
    explanations.forEach(exp => {
        exp.style.display = 'none';
        const toggle = exp.previousElementSibling;
        if (toggle) {
            toggle.style.cursor = 'pointer';
            toggle.addEventListener('click', () => {
                exp.style.display = exp.style.display === 'none' ? 'block' : 'none';
            });
        }
    });
}

// ============================================================
// Progress Page Functionality
// ============================================================

/**
 * Initialize progress page features
 */
function initProgressPage() {
    // Animate progress bars on scroll
    const progressBars = document.querySelectorAll('.progress-bar');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }
        });
    });

    progressBars.forEach(bar => observer.observe(bar));
}

// ============================================================
// Initialization on Page Load
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize based on current page
    if (document.getElementById('examForm')) {
        initExamPage();
        validateExamForm();
        enableKeyboardShortcuts();
    }

    if (document.querySelector('[data-score]')) {
        initResultsPage();
    }

    if (document.querySelector('.progress-bar')) {
        initProgressPage();
    }

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add loading indicator to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
            }
        });
    });
});

// ============================================================
// Utility Functions
// ============================================================

/**
 * Format time in MM:SS format
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * Get random element from array
 */
function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

/**
 * Shuffle array
 */
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Export functions for use in other scripts
window.QuizApp = {
    showToast,
    confirmAction,
    formatTime,
    clearSavedAnswers,
    updateProgressIndicators
};
