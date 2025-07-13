#!/bin/bash

echo "🚀 Iniciando Chatbot Académico Inteligente..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    exit 1
fi

# Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm no está instalado"
    exit 1
fi

echo "✅ Dependencias verificadas"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias de Python
echo "📥 Instalando dependencias de Python..."
pip install -r requirements.txt

# Verificar si la base de datos existe
if [ ! -f "backend/chatbot.db" ]; then
    echo "🗄️  Inicializando base de datos..."
    python scripts/populate_database.py
else
    echo "✅ Base de datos ya existe"
fi

# Instalar dependencias del frontend
echo "📥 Instalando dependencias del frontend..."
cd frontend
npm install
cd ..

echo "🎉 Configuración completada!"
echo ""
echo "📋 Para ejecutar el proyecto:"
echo "   1. Terminal 1 (Backend): python backend/app.py"
echo "   2. Terminal 2 (Frontend): cd frontend && npm run dev"
echo ""
echo "🌐 URLs:"
echo "   • Frontend: http://localhost:5173"
echo "   • Backend API: http://localhost:5002"
echo "   • Panel Admin: http://localhost:5002/admin"
echo ""
echo "🔑 Credenciales de administrador:"
echo "   • Usuario: admin"
echo "   • Contraseña: admin123"
echo ""
echo "✨ ¡Listo para usar!" 