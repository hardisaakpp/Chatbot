#!/usr/bin/env python3
"""
Panel de administración para el chatbot
"""

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from flask import redirect, url_for, flash, request
from backend.models import db, User, Category, Question, Conversation, Message, Response, SystemLog, ChatbotStats

class SecureModelView(ModelView):
    """Vista base segura para el panel de administración"""
    
    def is_accessible(self):
        """Verificar si el usuario tiene acceso"""
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        """Redirigir si no tiene acceso"""
        flash('Debes iniciar sesión como administrador para acceder a esta página.', 'error')
        return redirect(url_for('login'))

class UserAdmin(SecureModelView):
    """Administración de usuarios"""
    column_list = ['id', 'username', 'email', 'is_admin', 'is_active', 'created_at', 'last_login']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_admin', 'is_active', 'created_at']
    form_excluded_columns = ['password_hash', 'conversations']
    
    def on_model_change(self, form, model, is_created):
        """Manejar cambios en el modelo"""
        if is_created and hasattr(form, 'password') and form.password.data:
            model.set_password(form.password.data)
    
    def scaffold_form(self):
        """Personalizar el formulario"""
        form = super().scaffold_form()
        # Agregar campo de contraseña si no existe
        if not hasattr(form, 'password'):
            from wtforms import PasswordField
            form.password = PasswordField('Contraseña')
        return form

class CategoryAdmin(SecureModelView):
    """Administración de categorías"""
    column_list = ['id', 'name', 'description', 'icon', 'color', 'is_active', 'created_at']
    column_searchable_list = ['name', 'description']
    column_filters = ['is_active', 'created_at']
    form_excluded_columns = ['questions']
    
    def on_model_change(self, form, model, is_created):
        """Validar color hex"""
        if model.color and not model.color.startswith('#'):
            model.color = f'#{model.color}'

class QuestionAdmin(SecureModelView):
    """Administración de preguntas"""
    column_list = ['id', 'question_text', 'category_id', 'difficulty_level', 'usage_count', 'accuracy_score', 'is_active', 'is_featured']
    column_searchable_list = ['question_text', 'answer_text', 'keywords']
    column_filters = ['category_id', 'difficulty_level', 'is_active', 'is_featured', 'created_at']
    form_excluded_columns = ['responses', 'messages']
    
    form_choices = {
        'difficulty_level': [
            (1, 'Fácil'),
            (2, 'Medio'),
            (3, 'Difícil')
        ]
    }
    
    def on_model_change(self, form, model, is_created):
        """Actualizar timestamp"""
        from datetime import datetime
        model.updated_at = datetime.utcnow()

class ConversationAdmin(SecureModelView):
    """Administración de conversaciones"""
    column_list = ['id', 'user', 'session_id', 'started_at', 'ended_at', 'total_messages', 'language']
    column_searchable_list = ['session_id']
    column_filters = ['language', 'started_at', 'ended_at']
    form_excluded_columns = ['messages']
    
    def on_model_change(self, form, model, is_created):
        """Actualizar total de mensajes"""
        if model.messages:
            model.total_messages = len(model.messages)

class MessageAdmin(SecureModelView):
    """Administración de mensajes"""
    column_list = ['id', 'conversation', 'user_input', 'bot_response', 'intent_detected', 'confidence_score', 'timestamp']
    column_searchable_list = ['user_input', 'bot_response']
    column_filters = ['intent_detected', 'confidence_score', 'timestamp']
    form_excluded_columns = []
    
    form_choices = {
        'intent_detected': [
            ('greeting', 'Saludo'),
            ('question', 'Pregunta'),
            ('farewell', 'Despedida'),
            ('thanks', 'Agradecimiento'),
            ('unknown', 'Desconocido')
        ]
    }

class ResponseAdmin(SecureModelView):
    """Administración de respuestas alternativas"""
    column_list = ['id', 'question', 'response_text', 'response_type', 'is_default', 'usage_count']
    column_searchable_list = ['response_text']
    column_filters = ['response_type', 'is_default', 'created_at']
    
    form_choices = {
        'response_type': [
            ('text', 'Texto'),
            ('image', 'Imagen'),
            ('link', 'Enlace'),
            ('video', 'Video')
        ]
    }

class SystemLogAdmin(SecureModelView):
    """Administración de logs del sistema"""
    column_list = ['id', 'level', 'message', 'module', 'timestamp', 'user']
    column_searchable_list = ['message', 'module']
    column_filters = ['level', 'timestamp']
    can_create = False  # Los logs se crean automáticamente
    can_edit = False    # Los logs no se editan
    
    def on_model_delete(self, model):
        """Confirmar eliminación de logs"""
        flash(f'Log eliminado: {model.message[:50]}...', 'info')

class ChatbotStatsAdmin(SecureModelView):
    """Administración de estadísticas"""
    column_list = ['id', 'date', 'total_conversations', 'total_messages', 'unique_users', 'avg_response_time', 'avg_confidence_score']
    column_filters = ['date']
    can_create = False  # Las estadísticas se generan automáticamente
    can_edit = False    # Las estadísticas no se editan manualmente

def init_admin(app):
    """Inicializar el panel de administración"""
    admin = Admin(app, name='Chatbot Admin', template_mode='bootstrap4')
    
    # Agregar vistas
    admin.add_view(UserAdmin(User, db.session, name='Usuarios', endpoint='admin_users'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Categorías', endpoint='admin_categories'))
    admin.add_view(QuestionAdmin(Question, db.session, name='Preguntas', endpoint='admin_questions'))
    admin.add_view(ConversationAdmin(Conversation, db.session, name='Conversaciones', endpoint='admin_conversations'))
    admin.add_view(MessageAdmin(Message, db.session, name='Mensajes', endpoint='admin_messages'))
    admin.add_view(ResponseAdmin(Response, db.session, name='Respuestas', endpoint='admin_responses'))
    admin.add_view(SystemLogAdmin(SystemLog, db.session, name='Logs', endpoint='admin_logs'))
    admin.add_view(ChatbotStatsAdmin(ChatbotStats, db.session, name='Estadísticas', endpoint='admin_stats'))
    
    return admin 