#!/usr/bin/env python3
"""
Servicio de base de datos para el chatbot
"""

import time
import json
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from models import db, Question, Category, Conversation, Message, User, SystemLog, ChatbotStats
from preprocessing import processor

class DatabaseService:
    """Servicio para manejar operaciones de base de datos"""
    
    @staticmethod
    def get_best_response(user_input: str, session_id: Optional[str] = None) -> Tuple[str, float]:
        """
        Obtener la mejor respuesta desde la base de datos
        """
        start_time = time.time()
        
        try:
            # Extraer intención
            intent = processor.extract_intent(user_input)
            
            # Manejar intenciones especiales
            if intent['type'] == 'greeting':
                response = "¡Hola! Soy tu asistente académico. ¿En qué puedo ayudarte hoy?"
                confidence = 1.0
            elif intent['type'] == 'farewell':
                response = "¡Hasta luego! ¡Mucho éxito en tus estudios!"
                confidence = 1.0
            elif intent['type'] == 'thanks':
                response = "¡De nada! Estoy aquí para ayudarte."
                confidence = 1.0
            else:
                # Buscar en la base de datos
                best_match, confidence = DatabaseService._find_best_question(user_input)
                
                if best_match and confidence >= 0.3:
                    response = best_match.answer_text
                    # Incrementar contador de uso
                    best_match.increment_usage()
                else:
                    response = "Lo siento, no tengo una respuesta específica para esa pregunta. ¿Podrías reformularla o preguntar sobre otro tema?"
                    confidence = 0.0
            
            # Calcular tiempo de respuesta
            response_time = time.time() - start_time
            
            # Guardar mensaje en la base de datos
            DatabaseService._save_message(user_input, response, intent, confidence, response_time, session_id)
            
            return response, confidence
            
        except Exception as e:
            # Log del error
            DatabaseService._log_error(f"Error obteniendo respuesta: {str(e)}")
            return "Lo siento, tuve un problema procesando tu pregunta. ¿Podrías intentar de nuevo?", 0.0
    
    @staticmethod
    def _find_best_question(user_input: str) -> Tuple[Optional[Question], float]:
        """
        Encontrar la mejor pregunta en la base de datos
        """
        try:
            # Obtener todas las preguntas activas
            questions = Question.query.filter_by(is_active=True).all()
            
            if not questions:
                return None, 0.0
            
            best_match = None
            best_score = 0.0
            
            for question in questions:
                score = processor.calculate_similarity(user_input, question.question_text)
                if score > best_score and score >= 0.3:
                    best_score = score
                    best_match = question
            
            return best_match, best_score
            
        except Exception as e:
            DatabaseService._log_error(f"Error buscando pregunta: {str(e)}")
            return None, 0.0
    
    @staticmethod
    def _save_message(user_input: str, bot_response: str, intent: Dict, confidence: float, response_time: float, session_id: Optional[str] = None):
        """
        Guardar mensaje en la base de datos
        """
        try:
            # Obtener o crear conversación
            conversation = DatabaseService._get_or_create_conversation(session_id)
            
            # Crear mensaje
            message = Message(
                conversation_id=conversation.id,
                user_input=user_input,
                bot_response=bot_response,
                intent_detected=intent['type'],
                confidence_score=confidence,
                response_time=response_time,
                keywords_extracted=', '.join(intent.get('keywords', [])),
                timestamp=datetime.utcnow()
            )
            
            db.session.add(message)
            
            # Actualizar contador de mensajes en la conversación
            conversation.total_messages += 1
            
            db.session.commit()
            
        except Exception as e:
            DatabaseService._log_error(f"Error guardando mensaje: {str(e)}")
            db.session.rollback()
    
    @staticmethod
    def _get_or_create_conversation(session_id: Optional[str] = None) -> Conversation:
        """
        Obtener o crear una conversación
        """
        if not session_id:
            session_id = f"anon_{int(time.time())}"
        
        # Buscar conversación activa para esta sesión
        conversation = Conversation.query.filter_by(
            session_id=session_id,
            ended_at=None
        ).first()
        
        if not conversation:
            # Crear nueva conversación
            conversation = Conversation(
                session_id=session_id,
                started_at=datetime.utcnow(),
                total_messages=0,
                language='es'
            )
            db.session.add(conversation)
            db.session.commit()
        
        return conversation
    
    @staticmethod
    def _log_error(message: str, level: str = 'ERROR'):
        """
        Guardar log de error en la base de datos
        """
        try:
            log = SystemLog(
                level=level,
                message=message,
                module='database_service',
                function='get_best_response',
                timestamp=datetime.utcnow()
            )
            db.session.add(log)
            db.session.commit()
        except:
            # Si falla el logging, no hacer nada para evitar loops infinitos
            pass
    
    @staticmethod
    def get_questions_by_category(category_id: Optional[int] = None) -> List[Dict]:
        """
        Obtener preguntas por categoría
        """
        try:
            query = Question.query.filter_by(is_active=True)
            
            if category_id:
                query = query.filter_by(category_id=category_id)
            
            questions = query.all()
            
            return [
                {
                    'id': q.id,
                    'question': q.question_text,
                    'answer': q.answer_text,
                    'category': q.category.name if q.category else 'Sin categoría',
                    'difficulty': q.difficulty_level,
                    'usage_count': q.usage_count
                }
                for q in questions
            ]
            
        except Exception as e:
            DatabaseService._log_error(f"Error obteniendo preguntas por categoría: {str(e)}")
            return []
    
    @staticmethod
    def get_categories() -> List[Dict]:
        """
        Obtener todas las categorías activas
        """
        try:
            categories = Category.query.filter_by(is_active=True).all()
            
            return [
                {
                    'id': c.id,
                    'name': c.name,
                    'description': c.description,
                    'icon': c.icon,
                    'color': c.color,
                    'question_count': len(c.questions)
                }
                for c in categories
            ]
            
        except Exception as e:
            DatabaseService._log_error(f"Error obteniendo categorías: {str(e)}")
            return []
    
    @staticmethod
    def get_stats() -> Dict:
        """
        Obtener estadísticas del chatbot
        """
        try:
            # Estadísticas generales
            total_questions = Question.query.filter_by(is_active=True).count()
            total_conversations = Conversation.query.count()
            total_messages = Message.query.count()
            
            # Preguntas más populares
            popular_questions = Question.query.filter_by(is_active=True)\
                .order_by(Question.usage_count.desc())\
                .limit(5).all()
            
            # Estadísticas por categoría
            categories = Category.query.filter_by(is_active=True).all()
            category_stats = []
            
            for category in categories:
                question_count = Question.query.filter_by(
                    category_id=category.id,
                    is_active=True
                ).count()
                
                category_stats.append({
                    'name': category.name,
                    'count': question_count,
                    'color': category.color
                })
            
            return {
                'total_questions': total_questions,
                'total_conversations': total_conversations,
                'total_messages': total_messages,
                'popular_questions': [
                    {
                        'question': q.question_text[:50] + '...',
                        'usage_count': q.usage_count
                    }
                    for q in popular_questions
                ],
                'category_stats': category_stats
            }
            
        except Exception as e:
            DatabaseService._log_error(f"Error obteniendo estadísticas: {str(e)}")
            return {}
    
    @staticmethod
    def add_question(question_text: str, answer_text: str, category_id: Optional[int] = None, keywords: Optional[str] = None) -> bool:
        """
        Agregar nueva pregunta a la base de datos
        """
        try:
            question = Question(
                question_text=question_text,
                answer_text=answer_text,
                category_id=category_id,
                keywords=keywords,
                difficulty_level=1,
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(question)
            db.session.commit()
            
            return True
            
        except Exception as e:
            DatabaseService._log_error(f"Error agregando pregunta: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def update_question_accuracy(question_id: int, accuracy_score: float) -> bool:
        """
        Actualizar puntuación de precisión de una pregunta
        """
        try:
            question = Question.query.get(question_id)
            if question:
                question.update_accuracy(accuracy_score)
                return True
            return False
            
        except Exception as e:
            DatabaseService._log_error(f"Error actualizando precisión: {str(e)}")
            return False
    
    @staticmethod
    def get_conversation_history(session_id: str, limit: int = 50) -> List[Dict]:
        """
        Obtener historial de conversación
        """
        try:
            conversation = Conversation.query.filter_by(session_id=session_id).first()
            
            if not conversation:
                return []
            
            messages = Message.query.filter_by(conversation_id=conversation.id)\
                .order_by(Message.timestamp.desc())\
                .limit(limit).all()
            
            return [
                {
                    'user_input': msg.user_input,
                    'bot_response': msg.bot_response,
                    'timestamp': msg.timestamp.isoformat(),
                    'confidence': msg.confidence_score
                }
                for msg in reversed(messages)  # Orden cronológico
            ]
            
        except Exception as e:
            DatabaseService._log_error(f"Error obteniendo historial: {str(e)}")
            return []
    
    @staticmethod
    def save_daily_stats():
        """
        Guardar estadísticas diarias
        """
        try:
            today = date.today()
            
            # Verificar si ya existen estadísticas para hoy
            existing_stats = ChatbotStats.query.filter_by(date=today).first()
            if existing_stats:
                return
            
            # Calcular estadísticas del día
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            # Conversaciones del día
            conversations_today = Conversation.query.filter(
                Conversation.started_at >= today_start,
                Conversation.started_at <= today_end
            ).count()
            
            # Mensajes del día
            messages_today = Message.query.filter(
                Message.timestamp >= today_start,
                Message.timestamp <= today_end
            ).count()
            
            # Usuarios únicos del día
            unique_users = db.session.query(Conversation.session_id)\
                .filter(
                    Conversation.started_at >= today_start,
                    Conversation.started_at <= today_end
                ).distinct().count()
            
            # Tiempo promedio de respuesta
            messages_with_time = Message.query.filter(
                Message.timestamp >= today_start,
                Message.timestamp <= today_end,
                Message.response_time.isnot(None)
            ).all()
            
            avg_response_time = 0.0
            if messages_with_time:
                avg_response_time = sum(msg.response_time for msg in messages_with_time) / len(messages_with_time)
            
            # Confianza promedio
            messages_with_confidence = Message.query.filter(
                Message.timestamp >= today_start,
                Message.timestamp <= today_end,
                Message.confidence_score.isnot(None)
            ).all()
            
            avg_confidence = 0.0
            if messages_with_confidence:
                avg_confidence = sum(msg.confidence_score for msg in messages_with_confidence) / len(messages_with_confidence)
            
            # Crear estadísticas
            stats = ChatbotStats(
                date=today,
                total_conversations=conversations_today,
                total_messages=messages_today,
                unique_users=unique_users,
                avg_response_time=avg_response_time,
                avg_confidence_score=avg_confidence,
                avg_user_rating=0.0  # Por implementar
            )
            
            db.session.add(stats)
            db.session.commit()
            
        except Exception as e:
            DatabaseService._log_error(f"Error guardando estadísticas diarias: {str(e)}")
            db.session.rollback() 