# Chatbot Básico

Un chatbot inteligente desarrollado con Flask que utiliza procesamiento avanzado de lenguaje natural para responder preguntas frecuentes de manera más precisa y contextual.

## 🚀 Características

### **Interfaz de Usuario**
- ✅ Interfaz web moderna y responsive
- ✅ Animaciones de carga y efectos visuales
- ✅ Historial de conversación con timestamps
- ✅ Botones de preguntas rápidas
- ✅ Contador de mensajes en tiempo real
- ✅ Diseño adaptativo para móviles y tablets

### **Procesamiento Avanzado**
- ✅ **Detección de intenciones**: Saludos, despedidas, agradecimientos, preguntas
- ✅ **Manejo de sinónimos**: Reconocimiento de variaciones y abreviaciones
- ✅ **Corrección de errores**: Tolerancia a errores tipográficos
- ✅ **Extracción de palabras clave**: Identificación automática de términos importantes
- ✅ **Cálculo de similitud**: Múltiples algoritmos para mejor matching
- ✅ **Normalización de texto**: Lematización, stemming y limpieza
- ✅ **Respuestas contextuales**: Sugerencias para preguntas no encontradas

### **Funcionalidades Técnicas**
- ✅ API REST completa con endpoints adicionales
- ✅ Logging detallado para debugging
- ✅ Manejo robusto de errores
- ✅ Estadísticas del sistema
- ✅ Análisis de texto en tiempo real

## 🛠️ Instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/hardisaakpp/Chatbot.git
cd Chatbot
```

2. **Crea un entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. **Ejecuta la aplicación:**
```bash
python app.py
```

2. **Abre tu navegador y ve a:** `http://localhost:5002`

3. **¡Interactúa con el chatbot!** Prueba:
   - Preguntas directas: "¿Qué es la inteligencia artificial?"
   - Abreviaciones: "¿Qué es AI?"
   - Variaciones: "Explica machine learning"
   - Saludos: "Hola"
   - Despedidas: "Adiós"

## 📊 Mejoras en el Procesamiento

### **Sistema de Sinónimos**
El chatbot reconoce automáticamente variaciones y abreviaciones:

| Término | Sinónimos Reconocidos |
|---------|----------------------|
| AI | inteligencia artificial, ia, artificial intelligence |
| ML | machine learning, aprendizaje automático |
| DL | deep learning, aprendizaje profundo |
| NLP | procesamiento de lenguaje natural |
| BD | base de datos, database |
| IoT | internet de las cosas, internet of things |
| AR | realidad aumentada, augmented reality |
| VR | realidad virtual, virtual reality |

### **Detección de Intenciones**
- **Saludos**: "hola", "buenos días", "saludos"
- **Despedidas**: "adiós", "hasta luego", "nos vemos"
- **Agradecimientos**: "gracias", "thank you"
- **Preguntas**: Cualquier consulta sobre temas académicos

### **Algoritmos de Similitud**
- **Jaccard Similarity**: Para comparación de conjuntos de tokens
- **Cosine Similarity**: Para similitud vectorial
- **Sequence Matcher**: Para similitud de caracteres
- **Promedio ponderado**: Combinación de múltiples métodos

## 🏗️ Estructura del Proyecto

```
ChatbotBasico/
├── app.py                 # Aplicación principal Flask
├── preprocessing.py       # Procesamiento avanzado de NLP
├── responses.json         # Base de datos de respuestas
├── test_processing.py     # Script de pruebas
├── static/                # Archivos estáticos
│   ├── styles.css         # Estilos modernos y responsive
│   └── script.js          # JavaScript con animaciones
├── templates/
│   └── index.html         # Interfaz de usuario mejorada
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## 🔧 API Endpoints

### **POST /get_response**
Obtiene respuesta del chatbot
```json
{
  "user_input": "¿Qué es la inteligencia artificial?"
}
```

### **POST /api/analyze**
Análisis completo del texto
```json
{
  "text": "¿Qué es machine learning?"
}
```

### **GET /api/stats**
Estadísticas del sistema
```json
{
  "total_questions": 50,
  "total_greetings": 5,
  "total_farewells": 5,
  "processor_info": {
    "synonyms_count": 21,
    "stop_words_count": 200
  }
}
```

## 🧪 Pruebas

Ejecuta el script de pruebas para ver las mejoras en acción:

```bash
python test_processing.py
```

Este script demuestra:
- Detección de intenciones
- Manejo de sinónimos
- Corrección de errores tipográficos
- Cálculo de similitud
- Extracción de palabras clave

## 🎯 Personalización

### **Agregar Nuevas Respuestas**
Edita `responses.json`:

```json
{
  "preguntas_frecuentes": {
    "tu pregunta": "tu respuesta",
    "otra pregunta": "otra respuesta"
  }
}
```

### **Agregar Sinónimos**
Modifica `preprocessing.py`:

```python
self.synonyms = {
    'nuevo_termino': ['sinonimo1', 'sinonimo2', 'sinonimo3']
}
```

### **Ajustar Umbrales**
Modifica los parámetros de similitud en `preprocessing.py`:

```python
threshold: float = 0.3  # Umbral de confianza
```

## 📈 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **NLP**: NLTK, Procesamiento de texto avanzado
- **Algoritmos**: Jaccard, Cosine, Sequence Matcher
- **UI/UX**: Font Awesome, Google Fonts, Animaciones CSS

## 🔮 Próximas Mejoras

- [ ] Integración con APIs de IA externas
- [ ] Base de datos para persistencia
- [ ] Sistema de usuarios y personalización
- [ ] Análisis de sentimientos
- [ ] Soporte multiidioma
- [ ] Chat en tiempo real con WebSockets

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

- **Desarrollador**: Carlos Ortiz
- **Repositorio**: [https://github.com/hardisaakpp/Chatbot](https://github.com/hardisaakpp/Chatbot)

---

**¡Disfruta usando tu chatbot inteligente! 🤖✨**
