import json
import logging
from flask import Flask, render_template, request, jsonify
from preprocessing import get_best_response, processor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load predefined responses
try:
    with open('responses.json', 'r', encoding='utf-8') as file:
        responses = json.load(file)
    logger.info("Respuestas cargadas correctamente")
except Exception as e:
    logger.error(f"Error cargando responses.json: {e}")
    responses = {
        "saludos": ["Hola, ¿en qué puedo ayudarte?"],
        "despedidas": ["Hasta luego, ¡que tengas un buen día!"],
        "preguntas_frecuentes": {}
    }

def get_response(user_input):
    """
    Función mejorada para obtener respuestas usando el procesamiento avanzado
    """
    try:
        # Usar el nuevo sistema de procesamiento
        response, confidence = get_best_response(user_input, responses)
        
        # Log para debugging
        intent = processor.extract_intent(user_input)
        keywords = processor.extract_keywords(user_input)
        
        logger.info(f"Usuario: '{user_input}' | Intención: {intent['type']} | Confianza: {confidence:.2f} | Keywords: {keywords}")
        
        # Si la confianza es muy baja, sugerir reformular
        if confidence < 0.3 and intent['type'] == 'question':
            response += "\n\n💡 **Sugerencia**: Intenta reformular tu pregunta o usar palabras más específicas."
        
        return response
        
    except Exception as e:
        logger.error(f"Error procesando respuesta: {e}")
        return "Lo siento, tuve un problema procesando tu pregunta. ¿Podrías intentar de nuevo?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chatbot_response():
    try:
        user_input = request.form['user_input'].strip()
        
        if not user_input:
            return jsonify({'error': 'Por favor, ingresa una pregunta'}), 400
        
        response = get_response(user_input)
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"Error en endpoint /get_response: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Endpoint adicional para análisis de texto
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texto requerido'}), 400
        
        # Análisis completo del texto
        analysis = {
            'keywords': processor.extract_keywords(text),
            'intent': processor.extract_intent(text),
            'question_type': processor.extract_question_type(text),
            'processed_tokens': processor.preprocess(text)
        }
        
        return jsonify(analysis)
        
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        return jsonify({'error': 'Error en el análisis'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Endpoint para estadísticas del chatbot
    """
    try:
        stats = {
            'total_questions': len(responses.get('preguntas_frecuentes', {})),
            'total_greetings': len(responses.get('saludos', [])),
            'total_farewells': len(responses.get('despedidas', [])),
            'processor_info': {
                'synonyms_count': len(processor.synonyms),
                'stop_words_count': len(processor.stop_words)
            }
        }
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({'error': 'Error obteniendo estadísticas'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)