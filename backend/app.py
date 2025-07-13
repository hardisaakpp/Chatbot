import json
import logging
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from backend.config import config
from backend.models import db, User
from backend.utils.preprocessing import processor
from backend.database.database_service import DatabaseService
from backend.admin import init_admin
from backend.routes.chatbot_routes import chatbot_bp

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask-Login
login_manager = LoginManager()

def create_app(config_name='development'):
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    # Configurar sesiones
    app.secret_key = app.config['SECRET_KEY']
    # Inicializar panel de administración
    init_admin(app)
    
    # Registrar blueprints
    app.register_blueprint(chatbot_bp)
    
    return app

app = create_app()
CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])  # Habilitar CORS para toda la app
login_manager.init_app(app)
setattr(login_manager, 'login_view', 'login')
setattr(login_manager, 'login_message', 'Debes iniciar sesión para acceder a esta página.')

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario para Flask-Login"""
    return User.query.get(int(user_id))

def get_response(user_input):
    """
    Función mejorada para obtener respuestas usando la base de datos
    """
    try:
        # Obtener session_id para tracking
        session_id = session.get('session_id')
        if not session_id:
            session_id = f"session_{int(datetime.utcnow().timestamp())}"
            session['session_id'] = session_id
        # Usar el servicio de base de datos
        response, confidence = DatabaseService.get_best_response(user_input, session_id)
        
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
    return jsonify({"message": "API del chatbot funcionando"})

@app.route('/get_response', methods=['POST'])
def chatbot_response():
    """Endpoint para obtener respuesta del chatbot"""
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
    """Endpoint para análisis de texto"""
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
    """Endpoint para estadísticas del chatbot"""
    try:
        stats = DatabaseService.get_stats()
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({'error': 'Error obteniendo estadísticas'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Endpoint para obtener categorías"""
    try:
        categories = DatabaseService.get_categories()
        return jsonify(categories)
        
    except Exception as e:
        logger.error(f"Error obteniendo categorías: {e}")
        return jsonify({'error': 'Error obteniendo categorías'}), 500

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Endpoint para obtener preguntas por categoría"""
    try:
        category_id = request.args.get('category_id', type=int)
        if category_id is not None:
            questions = DatabaseService.get_questions_by_category(category_id)
        else:
            questions = DatabaseService.get_questions_by_category()
        return jsonify(questions)
        
    except Exception as e:
        logger.error(f"Error obteniendo preguntas: {e}")
        return jsonify({'error': 'Error obteniendo preguntas'}), 500

@app.route('/api/questions', methods=['POST'])
def add_question():
    """Endpoint para agregar nueva pregunta"""
    try:
        data = request.get_json()
        
        question_text = data.get('question_text', '').strip()
        answer_text = data.get('answer_text', '').strip()
        category_id = data.get('category_id')
        keywords = data.get('keywords', '')
        
        if not question_text or not answer_text:
            return jsonify({'error': 'Pregunta y respuesta son requeridas'}), 400
        
        success = DatabaseService.add_question(question_text, answer_text, category_id, keywords)
        
        if success:
            return jsonify({'message': 'Pregunta agregada exitosamente'}), 201
        else:
            return jsonify({'error': 'Error agregando pregunta'}), 500
            
    except Exception as e:
        logger.error(f"Error agregando pregunta: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Endpoint para obtener historial de conversación"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify([])
        
        limit = request.args.get('limit', 50, type=int)
        history = DatabaseService.get_conversation_history(session_id, limit)
        return jsonify(history)
        
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        return jsonify({'error': 'Error obteniendo historial'}), 500

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or '/admin')
        else:
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    return redirect('/')

@app.route('/admin')
@login_required
def admin_dashboard():
    """Dashboard de administración"""
    if not current_user.is_admin:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    stats = DatabaseService.get_stats()
    return render_template('admin_dashboard.html', stats=stats)

def setup_database():
    """Configurar base de datos en el primer request"""
    try:
        db.create_all()
        logger.info("Base de datos inicializada correctamente")
        DatabaseService.save_daily_stats()
    except Exception as e:
        logger.error(f"Error configurando base de datos: {e}")

if __name__ == '__main__':
    with app.app_context():
        setup_database()
    app.run(debug=True, port=5002)