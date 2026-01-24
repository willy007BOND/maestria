#!/bin/bash
# Script para iniciar el servidor Flask del MongoDB Quiz System

echo "=========================================="
echo "🚀 MongoDB Quiz System"
echo "=========================================="
echo ""

# Activar ambiente conda
echo "📦 Activando ambiente conda 'data'..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate data

# Verificar si la BD existe
if [ ! -f "mongodb_quiz.db" ]; then
    echo "⚠️  Base de datos no encontrada."
    echo "📝 Inicializando base de datos..."
    python init_db.py
fi

# Iniciar servidor
echo ""
echo "🌐 Iniciando servidor Flask..."
echo "📍 URL: http://127.0.0.1:5000"
echo ""
echo "✨ Presiona Ctrl+C para detener el servidor"
echo ""

python app.py
