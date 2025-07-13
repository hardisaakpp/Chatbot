# Chatbot Académico

Un chatbot inteligente desarrollado con React (frontend) y Flask (backend) que puede responder preguntas sobre temas académicos y tecnológicos.

## 🚀 Características

- **Interfaz moderna**: Diseño responsive con Material-UI
- **Base de datos SQLite**: Almacenamiento persistente de preguntas y respuestas
- **Procesamiento de lenguaje natural**: Análisis de intenciones y palabras clave
- **Sistema de categorías**: Organización temática de preguntas
- **Panel de administración**: Gestión de preguntas y estadísticas
- **Modo oscuro/claro**: Interfaz adaptable a preferencias del usuario

## 📋 Requisitos

- Python 3.8+
- Node.js 18+
- npm o yarn

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd ChatbotBasico
```

### 2. Configurar el backend
```bash
# Instalar dependencias de Python
pip install -r requirements.txt

# Inicializar la base de datos
python scripts/migrate_data.py
```

### 3. Configurar el frontend
```bash
cd frontend
npm install
```

## 🚀 Ejecución

### 1. Iniciar el backend
```bash
cd backend
python app.py
```
El backend estará disponible en: http://localhost:5002

### 2. Iniciar el frontend
```bash
cd frontend
npm run dev
```
El frontend estará disponible en: http://localhost:5173

## 📖 Uso

### Para usuarios
1. Abre http://localhost:5173 en tu navegador
2. Escribe tu pregunta en el campo de texto
3. Presiona Enter o haz clic en el botón de enviar
4. El chatbot responderá basándose en su base de conocimientos

### Para administradores
1. Accede a http://localhost:5002/admin
2. Usuario: `admin`
3. Contraseña: `admin123`
4. Gestiona preguntas, categorías y revisa estadísticas

## 🗂️ Estructura del proyecto

```
ChatbotBasico/
├── backend/
│   ├── app.py                 # Aplicación principal Flask
│   ├── models.py              # Modelos de base de datos
│   ├── config.py              # Configuración
│   ├── database/
│   │   └── database_service.py # Servicio de base de datos
│   ├── services/
│   │   └── chatbot_service.py # Servicio del chatbot
│   ├── utils/
│   │   └── preprocessing.py   # Procesamiento de texto
│   └── responses.json         # Datos iniciales
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/          # Componentes del chat
│   │   │   │   ├── ChatContainer.jsx
│   │   │   │   ├── MessageList.jsx
│   │   │   │   ├── MessageInput.jsx
│   │   │   │   ├── QuickActions.jsx
│   │   │   │   └── ChatFooter.jsx
│   │   │   ├── Admin/         # Componentes de administración
│   │   │   └── common/        # Componentes comunes
│   │   │       └── Header.jsx
│   │   ├── hooks/             # Hooks personalizados
│   │   │   ├── useChat.js
│   │   │   └── useTheme.js
│   │   ├── services/          # Servicios de API
│   │   │   └── api.js
│   │   ├── utils/             # Utilidades y constantes
│   │   │   └── constants.js
│   │   ├── styles/            # Estilos adicionales
│   │   ├── App.jsx            # Componente principal
│   │   └── main.jsx           # Punto de entrada
│   └── package.json
├── scripts/
│   └── migrate_data.py        # Script de migración
├── tests/                     # Pruebas organizadas
│   ├── unit/                  # Tests unitarios
│   ├── integration/           # Tests de integración
│   └── e2e/                   # Tests end-to-end
├── env.example                # Variables de entorno de ejemplo
├── start.sh                   # Script de inicio
└── stop.sh                    # Script de parada
```

## 🔧 Configuración

### Variables de entorno
Copia el archivo de ejemplo y configúralo:

```bash
cp env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Configuración del Backend
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///chatbot.db
LOG_LEVEL=INFO
PORT=5002

# Configuración del Frontend
VITE_API_BASE_URL=http://localhost:5002
VITE_APP_TITLE=Chatbot Académico

# Configuración de Desarrollo
NODE_ENV=development
FLASK_ENV=development
```

### Personalización
- **Preguntas**: Agrega nuevas preguntas desde el panel de administración
- **Categorías**: Crea nuevas categorías para organizar el contenido
- **Estilo**: Modifica los estilos en `frontend/src/App.css`

## 🧪 Pruebas

```bash
# Ejecutar pruebas del backend
python -m pytest tests/

# Ejecutar pruebas del frontend
cd frontend
npm test
```

## 📊 Estadísticas

El sistema recopila automáticamente:
- Número total de conversaciones
- Mensajes por sesión
- Tiempo de respuesta promedio
- Puntuación de confianza
- Preguntas más populares

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema:
1. Revisa los logs del backend en la consola
2. Verifica que ambos servicios estén ejecutándose
3. Asegúrate de que la base de datos esté inicializada
4. Revisa la consola del navegador para errores del frontend

## 🔄 Actualizaciones

Para actualizar el sistema:
1. Detén ambos servicios
2. Ejecuta `git pull` para obtener los últimos cambios
3. Ejecuta `python scripts/migrate_data.py` si hay cambios en la base de datos
4. Reinicia ambos servicios
