# 🤖 Chatbot Académico Inteligente

Un chatbot inteligente para asistencia académica con base de datos completa, analytics y sistema de feedback.

## ✨ Características Principales

### 🗄️ **Base de Datos Completa**
- **Gestión de Preguntas y Respuestas**: Sistema completo de Q&A con categorías
- **Tracking de Conversaciones**: Historial completo de chats con análisis de intenciones
- **Sistema de Usuarios**: Autenticación y roles (admin/usuario)
- **Estadísticas Automáticas**: Métricas de uso y rendimiento en tiempo real
- **Panel de Administración**: Interfaz completa para gestionar datos

### 🎯 **Funcionalidades Avanzadas**
- **Procesamiento de Lenguaje Natural**: Usando spaCy para análisis semántico avanzado
- **Sistema de Feedback**: Los usuarios pueden calificar respuestas (1-5 estrellas)
- **Sugerencias Inteligentes**: Preguntas recomendadas basadas en el historial
- **Analytics Detallados**: Dashboard completo con métricas y tendencias
- **Mejora Continua**: Las respuestas mejoran automáticamente con el feedback
- **Categorización**: Organización por temas (Matemáticas, Historia, Ciencia, etc.)
- **Extracción de Entidades**: Identificación automática de conceptos y materias

### 📊 **Analytics y Reportes**
- **Métricas en Tiempo Real**: Usuarios, conversaciones, mensajes
- **Análisis de Rendimiento**: Preguntas más populares y mejor calificadas
- **Tendencias Temporales**: Estadísticas de los últimos 7 días
- **Distribución de Intenciones**: Análisis de tipos de consultas
- **Exportación de Datos**: Para análisis externo

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- SQLite (incluido) o PostgreSQL/MySQL

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd ChatbotBasico
```

### 2. Configurar el backend
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar spaCy y modelo de español
python scripts/install_spacy.py

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus configuraciones
```

### 3. Configurar el frontend
```bash
cd frontend
npm install
```

### 4. Poblar la base de datos con datos de ejemplo
```bash
# Desde la raíz del proyecto
python scripts/populate_database.py
```

### 5. Ejecutar el proyecto
```bash
# Terminal 1: Backend
python backend/app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 📋 Estructura del Proyecto

```
ChatbotBasico/
├── backend/
│   ├── app.py                 # Aplicación principal Flask
│   ├── models.py              # Modelos de base de datos
│   ├── admin.py               # Panel de administración
│   ├── database/
│   │   └── database_service.py # Servicio de base de datos
│   ├── routes/
│   │   └── chatbot_routes.py  # Rutas del chatbot
│   └── utils/
│       └── preprocessing.py   # Procesamiento de texto con spaCy
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/          # Componentes del chat
│   │   │   └── Admin/         # Componentes de administración
│   │   ├── services/
│   │   │   └── api.js         # Servicios de API
│   │   └── hooks/
│   │       └── useChat.js     # Hook personalizado
│   └── package.json
├── scripts/
│   └── populate_database.py   # Script para datos de ejemplo
└── README.md
```

## 🗄️ Modelos de Base de Datos

### Usuarios (`users`)
- Gestión de usuarios con roles (admin/usuario)
- Autenticación segura con hash de contraseñas
- Tracking de actividad y último login

### Categorías (`categories`)
- Organización de preguntas por temas
- Iconos y colores personalizables
- Descripciones detalladas

### Preguntas (`questions`)
- Preguntas y respuestas con metadatos
- Palabras clave y sinónimos
- Niveles de dificultad
- Contador de uso y puntuación de precisión

### Conversaciones (`conversations`)
- Historial completo de chats
- Tracking de sesiones
- Metadatos de conversación

### Mensajes (`messages`)
- Mensajes individuales con análisis
- Detección de intenciones
- Feedback de usuarios
- Tiempo de respuesta

### Estadísticas (`chatbot_stats`)
- Métricas diarias automáticas
- Tendencias temporales
- Análisis de rendimiento

## 🔧 API Endpoints

### Chat
- `POST /get_response` - Obtener respuesta del chatbot
- `POST /api/feedback` - Enviar feedback de usuario
- `GET /api/suggestions` - Obtener sugerencias de preguntas

### Administración
- `GET /api/analytics` - Analytics detallados (solo admin)
- `GET /api/export` - Exportar datos (solo admin)
- `GET /api/stats` - Estadísticas básicas
- `GET /api/categories` - Listar categorías
- `GET /api/questions` - Listar preguntas por categoría

### Gestión de Contenido
- `POST /api/questions` - Agregar nueva pregunta
- `PUT /api/questions/{id}` - Actualizar pregunta
- `DELETE /api/questions/{id}` - Eliminar pregunta

## 📊 Dashboard de Analytics

### Métricas Generales
- **Usuarios Totales**: Número total de usuarios registrados
- **Conversaciones**: Total de conversaciones iniciadas
- **Mensajes**: Total de mensajes intercambiados
- **Preguntas**: Total de preguntas en la base de datos

### Análisis Detallado
- **Preguntas Populares**: Más utilizadas por los usuarios
- **Mejor Calificadas**: Con mayor puntuación de precisión
- **Necesitan Mejora**: Con baja puntuación
- **Distribución de Intenciones**: Tipos de consultas más comunes
- **Tendencias Temporales**: Evolución en los últimos 7 días

## 🎯 Sistema de Feedback

### Características
- **Calificación con Estrellas**: Sistema 1-5 estrellas
- **Comentarios Opcionales**: Feedback textual detallado
- **Mejora Automática**: Las respuestas mejoran con el feedback
- **Análisis de Satisfacción**: Métricas de satisfacción del usuario

### Flujo de Feedback
1. Usuario recibe respuesta del chatbot
2. Se muestra opción para calificar la respuesta
3. Usuario puede dar 1-5 estrellas y comentario opcional
4. El sistema actualiza la precisión de la pregunta
5. Los datos se usan para mejorar futuras respuestas

## 🔐 Panel de Administración

### Acceso
- URL: `http://localhost:5002/admin`
- Usuario: `admin`
- Contraseña: `admin123`

### Funcionalidades
- **Gestión de Usuarios**: Crear, editar, eliminar usuarios
- **Gestión de Categorías**: Organizar preguntas por temas
- **Gestión de Preguntas**: CRUD completo de Q&A
- **Análisis de Conversaciones**: Revisar chats de usuarios
- **Logs del Sistema**: Monitoreo de errores y actividad
- **Estadísticas**: Métricas detalladas del sistema

## 🚀 Funcionalidades Avanzadas

### Sugerencias Inteligentes
- **Basadas en Popularidad**: Preguntas más utilizadas
- **Basadas en Historial**: Relacionadas con conversaciones previas
- **Personalización**: Adaptadas al contexto del usuario

### Mejora Continua
- **Aprendizaje Automático**: El sistema mejora con el uso
- **Análisis de Patrones**: Identificación de tendencias
- **Optimización de Respuestas**: Mejora de precisión

### Exportación de Datos
- **Formatos Soportados**: JSON, CSV
- **Tipos de Datos**: Conversaciones, mensajes, preguntas
- **Análisis Externo**: Para herramientas de BI

## 🛠️ Desarrollo

### Agregar Nueva Funcionalidad
1. Crear modelo en `backend/models.py`
2. Agregar métodos en `backend/database/database_service.py`
3. Crear rutas en `backend/routes/`
4. Desarrollar componentes frontend
5. Actualizar documentación

### Testing
```bash
# Ejecutar tests
python -m pytest tests/

# Tests específicos
python -m pytest tests/unit/
python -m pytest tests/integration/
```

## 🤖 Procesamiento de Lenguaje Natural con spaCy

### Características de spaCy
- **Modelo de Español**: `es_core_news_sm` para procesamiento en español
- **Análisis Semántico**: Similitud entre textos usando vectores de palabras
- **Extracción de Entidades**: Identificación automática de conceptos y materias
- **Análisis de Estructura**: Sujeto, verbo, objeto y dependencias gramaticales
- **Lematización Avanzada**: Normalización de palabras para mejor matching

### Funcionalidades Implementadas
- **Preprocesamiento Inteligente**: Tokenización, lematización y filtrado automático
- **Detección de Intenciones**: Saludos, preguntas, agradecimientos, despedidas
- **Cálculo de Similitud**: Combinación de similitud semántica y léxica
- **Extracción de Palabras Clave**: Sustantivos, verbos y nombres propios relevantes
- **Análisis de Tipos de Pregunta**: Qué, cómo, cuándo, dónde, por qué, cuál

### Scripts de Instalación y Prueba
```bash
# Instalar spaCy y modelo de español
python scripts/install_spacy.py

# Probar la instalación
python scripts/test_spacy.py
```

### Uso en el Código
```python
from backend.utils.preprocessing import processor

# Procesar texto
tokens = processor.preprocess("¿Qué es la inteligencia artificial?")

# Extraer palabras clave
keywords = processor.extract_keywords("Explica las matemáticas")

# Calcular similitud
similarity = processor.calculate_similarity("IA", "inteligencia artificial")

# Extraer intención
intent = processor.extract_intent("Hola, ¿cómo estás?")
```

## 📈 Roadmap

### Próximas Funcionalidades
- [x] **Procesamiento de Lenguaje Natural**: spaCy implementado
- [ ] **Integración con IA**: OpenAI, GPT, etc.
- [ ] **Multilingüe**: Soporte para múltiples idiomas
- [ ] **Chat en Tiempo Real**: WebSockets para chat en vivo
- [ ] **Análisis de Sentimientos**: Detección de emociones
- [ ] **Integración con LMS**: Moodle, Canvas, etc.
- [ ] **API Pública**: Para integraciones externas

### Mejoras Técnicas
- [ ] **Caché Redis**: Para mejor rendimiento
- [ ] **Microservicios**: Arquitectura escalable
- [ ] **Docker**: Containerización completa
- [ ] **CI/CD**: Pipeline de despliegue automático

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

- **Email**: soporte@chatbot.com
- **Documentación**: [Wiki del proyecto]
- **Issues**: [GitHub Issues]

---

**¡Gracias por usar nuestro Chatbot Académico Inteligente! 🎓**
