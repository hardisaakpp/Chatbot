#!/bin/bash

# Script de inicio rápido para el Chatbot Académico
echo "🚀 Iniciando Chatbot Académico..."

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar que Node.js esté instalado
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    exit 1
fi

# Verificar que npm esté instalado
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm no está instalado"
    exit 1
fi

echo "✅ Dependencias verificadas"

# Función para limpiar procesos al salir
cleanup() {
    echo "🛑 Deteniendo servicios..."
    pkill -f "python.*app.py"
    pkill -f "npm.*dev"
    exit 0
}

# Capturar Ctrl+C para limpiar procesos
trap cleanup SIGINT

# Iniciar backend
echo "🔧 Iniciando backend..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Esperar un momento para que el backend se inicie
sleep 3

# Verificar que el backend esté funcionando
if curl -s http://localhost:5002 > /dev/null; then
    echo "✅ Backend iniciado correctamente en http://localhost:5002"
else
    echo "❌ Error: No se pudo iniciar el backend"
    cleanup
fi

# Iniciar frontend
echo "🎨 Iniciando frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Esperar un momento para que el frontend se inicie
sleep 5

# Verificar que el frontend esté funcionando
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ Frontend iniciado correctamente en http://localhost:5173"
else
    echo "❌ Error: No se pudo iniciar el frontend"
    cleanup
fi

echo ""
echo "🎉 ¡Chatbot Académico iniciado exitosamente!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5002"
echo "👨‍💼 Admin:    http://localhost:5002/admin (admin/admin123)"
echo ""
echo "💡 Presiona Ctrl+C para detener todos los servicios"
echo ""

# Mantener el script ejecutándose
wait 