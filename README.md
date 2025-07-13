# Chatbot Básico

Un chatbot simple desarrollado con Flask que responde preguntas frecuentes basándose en un archivo JSON de respuestas predefinidas.

## Características

- Interfaz web simple y responsive
- Procesamiento de texto para mejorar la coincidencia de preguntas
- Respuestas basadas en un archivo JSON de preguntas frecuentes
- API REST para integración con otros sistemas

## Instalación

1. Clona el repositorio:
```bash
git clone <tu-repositorio-url>
cd ChatbotBasico
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:
```bash
python app.py
```

2. Abre tu navegador y ve a `http://localhost:5001`

3. Escribe tus preguntas en el chat y obtén respuestas automáticas.

## Estructura del Proyecto

```
ChatbotBasico/
├── app.py              # Aplicación principal Flask
├── chatbot.py          # Lógica del chatbot
├── preprocessing.py    # Procesamiento de texto
├── responses.json      # Base de datos de respuestas
├── static/             # Archivos estáticos (CSS, JS)
├── templates/          # Plantillas HTML
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## Personalización

Para agregar nuevas preguntas y respuestas, edita el archivo `responses.json`:

```json
{
  "preguntas_frecuentes": {
    "¿Cuál es tu nombre?": "Me llamo Chatbot Básico",
    "¿Cómo estás?": "¡Muy bien, gracias por preguntar!"
  }
}
```

## Tecnologías Utilizadas

- **Flask**: Framework web para Python
- **HTML/CSS/JavaScript**: Frontend
- **JSON**: Almacenamiento de respuestas

## Licencia

Este proyecto está bajo la Licencia MIT.
