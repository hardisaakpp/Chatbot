from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from backend.database.database_service import DatabaseService
from backend.models import db, Message, Question
import logging

logger = logging.getLogger(__name__)

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Endpoint para recibir feedback de los usuarios"""
    try:
        data = request.get_json()
        message_id = data.get('message_id')
        rating = data.get('rating')  # 1-5 estrellas
        feedback_text = data.get('feedback_text', '')
        
        if not message_id or not rating:
            return jsonify({'error': 'ID del mensaje y calificación son requeridos'}), 400
        
        if not 1 <= rating <= 5:
            return jsonify({'error': 'La calificación debe estar entre 1 y 5'}), 400
        
        # Buscar el mensaje
        message = Message.query.get(message_id)
        if not message:
            return jsonify({'error': 'Mensaje no encontrado'}), 404
        
        # Actualizar feedback
        message.user_rating = rating
        message.user_feedback = feedback_text
        
        # Si hay una pregunta asociada, actualizar su precisión
        if message.question_id:
            question = Question.query.get(message.question_id)
            if question:
                # Convertir rating a score (1-5 -> 0.0-1.0)
                score = rating / 5.0
                question.update_accuracy(score)
        
        db.session.commit()
        
        return jsonify({'message': 'Feedback guardado exitosamente'})
        
    except Exception as e:
        logger.error(f"Error guardando feedback: {e}")
        db.session.rollback()
        return jsonify({'error': 'Error guardando feedback'}), 500

@chatbot_bp.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Obtener sugerencias de preguntas basadas en el historial"""
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify([])
        
        # Obtener preguntas populares y relacionadas
        suggestions = DatabaseService.get_question_suggestions(session_id)
        return jsonify(suggestions)
        
    except Exception as e:
        logger.error(f"Error obteniendo sugerencias: {e}")
        return jsonify({'error': 'Error obteniendo sugerencias'}), 500

@chatbot_bp.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    """Obtener analytics detallados (solo para admins)"""
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        analytics = DatabaseService.get_detailed_analytics()
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Error obteniendo analytics: {e}")
        return jsonify({'error': 'Error obteniendo analytics'}), 500

@chatbot_bp.route('/api/export', methods=['GET'])
@login_required
def export_data():
    """Exportar datos para análisis (solo para admins)"""
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data_type = request.args.get('type', 'conversations')
        export_data = DatabaseService.export_data(data_type)
        return jsonify(export_data)
        
    except Exception as e:
        logger.error(f"Error exportando datos: {e}")
        return jsonify({'error': 'Error exportando datos'}), 500
