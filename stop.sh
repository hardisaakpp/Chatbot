#!/bin/bash

# Script para detener todos los servicios del Chatbot Académico
echo "🛑 Deteniendo Chatbot Académico..."

# Detener procesos de Python (backend)
echo "🔧 Deteniendo backend..."
pkill -f "python.*app.py"

# Detener procesos de npm (frontend)
echo "🎨 Deteniendo frontend..."
pkill -f "npm.*dev"

# Detener procesos de Vite
echo "⚡ Deteniendo servidor de desarrollo..."
pkill -f "vite"

# Esperar un momento para que los procesos se detengan
sleep 2

# Verificar que los puertos estén libres
if ! lsof -i :5002 > /dev/null 2>&1; then
    echo "✅ Puerto 5002 (backend) liberado"
else
    echo "⚠️ Puerto 5002 aún en uso"
fi

if ! lsof -i :5173 > /dev/null 2>&1; then
    echo "✅ Puerto 5173 (frontend) liberado"
else
    echo "⚠️ Puerto 5173 aún en uso"
fi

echo "🎉 Todos los servicios detenidos" 