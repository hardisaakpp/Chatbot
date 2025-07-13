from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de usuario para el sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relaciones
    conversations = db.relationship('Conversation', backref='user', lazy=True)
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    """Modelo para categorías de preguntas"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Para iconos de Font Awesome
    color = db.Column(db.String(7))  # Color en formato hex
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    questions = db.relationship('Question', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Question(db.Model):
    """Modelo para preguntas y respuestas"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    # Metadatos
    keywords = db.Column(db.Text)  # Palabras clave separadas por comas
    synonyms = db.Column(db.Text)  # Sinónimos separados por comas
    difficulty_level = db.Column(db.Integer, default=1)  # 1=fácil, 2=medio, 3=difícil
    usage_count = db.Column(db.Integer, default=0)  # Contador de uso
    accuracy_score = db.Column(db.Float, default=0.0)  # Puntuación de precisión
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)  # Para preguntas destacadas
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relaciones
    responses = db.relationship('Response', backref='question', lazy=True)
    
    def __repr__(self):
        return f'<Question {self.question_text[:50]}...>'
    
    def increment_usage(self):
        """Incrementar contador de uso"""
        self.usage_count += 1
        db.session.commit()
    
    def update_accuracy(self, score):
        """Actualizar puntuación de precisión"""
        if self.accuracy_score == 0:
            self.accuracy_score = score
        else:
            # Promedio ponderado
            self.accuracy_score = (self.accuracy_score + score) / 2
        db.session.commit()

class Conversation(db.Model):
    """Modelo para conversaciones de usuarios"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=False)  # Para usuarios anónimos
    
    # Metadatos de la conversación
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    total_messages = db.Column(db.Integer, default=0)
    language = db.Column(db.String(10), default='es')
    
    # Relaciones
    messages = db.relationship('Message', backref='conversation', lazy=True, order_by='Message.timestamp')
    
    def __repr__(self):
        return f'<Conversation {self.id} - {self.session_id}>'
    
    def end_conversation(self):
        """Finalizar conversación"""
        self.ended_at = datetime.utcnow()
        db.session.commit()

class Message(db.Model):
    """Modelo para mensajes individuales"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=True)
    
    # Contenido del mensaje
    user_input = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    
    # Metadatos
    intent_detected = db.Column(db.String(50))  # greeting, question, farewell, etc.
    confidence_score = db.Column(db.Float, default=0.0)
    response_time = db.Column(db.Float)  # Tiempo de respuesta en segundos
    keywords_extracted = db.Column(db.Text)  # Palabras clave extraídas
    
    # Feedback del usuario
    user_rating = db.Column(db.Integer)  # 1-5 estrellas
    user_feedback = db.Column(db.Text)  # Comentario del usuario
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id} - {self.user_input[:30]}...>'

class Response(db.Model):
    """Modelo para respuestas alternativas a una pregunta"""
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    response_text = db.Column(db.Text, nullable=False)
    response_type = db.Column(db.String(20), default='text')  # text, image, link, etc.
    response_data = db.Column(db.Text)  # Datos adicionales (URLs, etc.)
    
    # Metadatos
    is_default = db.Column(db.Boolean, default=False)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Response {self.id} - {self.response_text[:30]}...>'

class SystemLog(db.Model):
    """Modelo para logs del sistema"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), nullable=False)  # INFO, WARNING, ERROR
    message = db.Column(db.Text, nullable=False)
    module = db.Column(db.String(100))
    function = db.Column(db.String(100))
    line_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<SystemLog {self.level} - {self.message[:50]}...>'

class ChatbotStats(db.Model):
    """Modelo para estadísticas del chatbot"""
    __tablename__ = 'chatbot_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    
    # Métricas diarias
    total_conversations = db.Column(db.Integer, default=0)
    total_messages = db.Column(db.Integer, default=0)
    unique_users = db.Column(db.Integer, default=0)
    avg_response_time = db.Column(db.Float, default=0.0)
    avg_confidence_score = db.Column(db.Float, default=0.0)
    avg_user_rating = db.Column(db.Float, default=0.0)
    
    # Métricas por categoría
    questions_by_category = db.Column(db.Text)  # JSON con estadísticas por categoría
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatbotStats {self.date} - {self.total_messages} messages>' 