#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models import db, User, Category, Question, Conversation, Message, ChatbotStats
from backend.database.database_service import DatabaseService
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Crear datos de ejemplo en la base de datos"""
    app = create_app()
    
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        print("🗄️  Poblando base de datos con datos de ejemplo...")
        
        # 1. Crear usuarios de ejemplo
        print("👥 Creando usuarios...")
        users = []
        
        # Usuario admin
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@chatbot.com'
        admin.is_admin = True
        admin.set_password('admin123')
        users.append(admin)
        
        # Usuarios normales
        normal_users = [
            {'username': 'maria', 'email': 'maria@example.com'},
            {'username': 'juan', 'email': 'juan@example.com'},
            {'username': 'ana', 'email': 'ana@example.com'},
            {'username': 'carlos', 'email': 'carlos@example.com'}
        ]
        
        for user_data in normal_users:
            user = User()
            user.username = user_data['username']
            user.email = user_data['email']
            user.is_admin = False
            user.set_password('password123')
            users.append(user)
        
        db.session.add_all(users)
        db.session.commit()
        print(f"✅ {len(users)} usuarios creados")
        
        # 2. Crear categorías
        print("📂 Creando categorías...")
        categories_data = [
            {
                'name': 'Matemáticas',
                'description': 'Preguntas sobre matemáticas, álgebra, geometría, etc.',
                'icon': 'fas fa-calculator',
                'color': '#3B82F6'
            },
            {
                'name': 'Historia',
                'description': 'Preguntas sobre historia mundial, eventos históricos, etc.',
                'icon': 'fas fa-landmark',
                'color': '#EF4444'
            },
            {
                'name': 'Ciencia',
                'description': 'Preguntas sobre física, química, biología, etc.',
                'icon': 'fas fa-flask',
                'color': '#10B981'
            },
            {
                'name': 'Literatura',
                'description': 'Preguntas sobre libros, autores, géneros literarios, etc.',
                'icon': 'fas fa-book',
                'color': '#8B5CF6'
            },
            {
                'name': 'Tecnología',
                'description': 'Preguntas sobre programación, computadoras, internet, etc.',
                'icon': 'fas fa-laptop-code',
                'color': '#F59E0B'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            categories.append(category)
        
        db.session.add_all(categories)
        db.session.commit()
        print(f"✅ {len(categories)} categorías creadas")
        
        # 3. Crear preguntas y respuestas
        print("❓ Creando preguntas y respuestas...")
        questions_data = [
            # Matemáticas
            {
                'question': '¿Cuál es la fórmula del área de un círculo?',
                'answer': 'La fórmula del área de un círculo es A = πr², donde r es el radio del círculo.',
                'category': 'Matemáticas',
                'keywords': 'área, círculo, fórmula, radio, pi',
                'difficulty': 1
            },
            {
                'question': '¿Qué es el teorema de Pitágoras?',
                'answer': 'El teorema de Pitágoras establece que en un triángulo rectángulo, el cuadrado de la hipotenusa es igual a la suma de los cuadrados de los catetos: a² + b² = c².',
                'category': 'Matemáticas',
                'keywords': 'teorema, pitágoras, triángulo, rectángulo, hipotenusa',
                'difficulty': 2
            },
            {
                'question': '¿Cómo se resuelve una ecuación cuadrática?',
                'answer': 'Una ecuación cuadrática se resuelve usando la fórmula cuadrática: x = (-b ± √(b² - 4ac)) / 2a, donde ax² + bx + c = 0.',
                'category': 'Matemáticas',
                'keywords': 'ecuación, cuadrática, fórmula, resolver',
                'difficulty': 3
            },
            
            # Historia
            {
                'question': '¿Cuándo comenzó la Segunda Guerra Mundial?',
                'answer': 'La Segunda Guerra Mundial comenzó el 1 de septiembre de 1939 cuando Alemania invadió Polonia.',
                'category': 'Historia',
                'keywords': 'segunda guerra mundial, alemania, polonia, 1939',
                'difficulty': 1
            },
            {
                'question': '¿Quién fue Napoleón Bonaparte?',
                'answer': 'Napoleón Bonaparte fue un líder político y militar francés que se convirtió en emperador de Francia y conquistó gran parte de Europa a principios del siglo XIX.',
                'category': 'Historia',
                'keywords': 'napoleón, bonaparte, francia, emperador, conquista',
                'difficulty': 2
            },
            
            # Ciencia
            {
                'question': '¿Qué es la fotosíntesis?',
                'answer': 'La fotosíntesis es el proceso mediante el cual las plantas convierten la luz solar, dióxido de carbono y agua en glucosa y oxígeno.',
                'category': 'Ciencia',
                'keywords': 'fotosíntesis, plantas, luz solar, glucosa, oxígeno',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es la estructura del ADN?',
                'answer': 'El ADN tiene una estructura de doble hélice, formada por dos cadenas de nucleótidos que se enrollan entre sí, con bases nitrogenadas que se aparean específicamente.',
                'category': 'Ciencia',
                'keywords': 'ADN, doble hélice, nucleótidos, bases nitrogenadas',
                'difficulty': 3
            },
            
            # Literatura
            {
                'question': '¿Quién escribió "Don Quijote"?',
                'answer': '"Don Quijote" fue escrito por Miguel de Cervantes Saavedra y se publicó en dos partes en 1605 y 1615.',
                'category': 'Literatura',
                'keywords': 'don quijote, cervantes, novela, literatura española',
                'difficulty': 1
            },
            {
                'question': '¿Qué es la poesía épica?',
                'answer': 'La poesía épica es un género literario que narra las hazañas de héroes legendarios o históricos, generalmente en verso y con un tono elevado.',
                'category': 'Literatura',
                'keywords': 'poesía, épica, héroes, verso, narrativa',
                'difficulty': 2
            },
            
            # Tecnología
            {
                'question': '¿Qué es HTML?',
                'answer': 'HTML (HyperText Markup Language) es el lenguaje de marcado estándar para crear páginas web. Define la estructura y el contenido de una página.',
                'category': 'Tecnología',
                'keywords': 'HTML, lenguaje, marcado, web, páginas',
                'difficulty': 1
            },
            {
                'question': '¿Qué es un algoritmo?',
                'answer': 'Un algoritmo es un conjunto de instrucciones paso a paso diseñadas para realizar una tarea específica o resolver un problema.',
                'category': 'Tecnología',
                'keywords': 'algoritmo, instrucciones, tarea, problema, programación',
                'difficulty': 2
            },
            {
                'question': '¿Qué es la inteligencia artificial?',
                'answer': 'La inteligencia artificial es la simulación de procesos de inteligencia humana por parte de máquinas, especialmente sistemas informáticos.',
                'category': 'Tecnología',
                'keywords': 'inteligencia artificial, IA, máquinas, simulación, procesos',
                'difficulty': 2
            }
        ]
        
        questions = []
        for q_data in questions_data:
            category = Category.query.filter_by(name=q_data['category']).first()
            question = Question(
                question_text=q_data['question'],
                answer_text=q_data['answer'],
                category_id=category.id if category else None,
                keywords=q_data['keywords'],
                difficulty_level=q_data['difficulty'],
                usage_count=random.randint(0, 50),
                accuracy_score=random.uniform(0.6, 1.0),
                is_active=True,
                created_by=admin.id
            )
            questions.append(question)
        
        db.session.add_all(questions)
        db.session.commit()
        print(f"✅ {len(questions)} preguntas creadas")
        
        # 4. Crear conversaciones y mensajes de ejemplo
        print("💬 Creando conversaciones de ejemplo...")
        
        # Generar conversaciones para los últimos 7 días
        for i in range(20):
            # Usuario aleatorio
            user = random.choice(users)
            
            # Fecha aleatoria en los últimos 7 días
            days_ago = random.randint(0, 7)
            start_time = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            
            # Crear conversación
            conversation = Conversation(
                user_id=user.id if not user.is_admin else None,
                session_id=f"session_{i}_{int(start_time.timestamp())}",
                started_at=start_time,
                ended_at=start_time + timedelta(minutes=random.randint(5, 30)),
                total_messages=random.randint(3, 15),
                language='es'
            )
            db.session.add(conversation)
            db.session.flush()  # Para obtener el ID
            
            # Crear mensajes para esta conversación
            num_messages = conversation.total_messages
            for j in range(num_messages):
                message_time = start_time + timedelta(minutes=j * 2)
                
                # Seleccionar pregunta aleatoria
                question = random.choice(questions)
                
                # Generar input de usuario
                user_inputs = [
                    question.question_text,
                    question.question_text.split('?')[0] + '?',
                    question.question_text.lower(),
                    question.question_text.replace('¿', '').replace('?', '')
                ]
                user_input = random.choice(user_inputs)
                
                message = Message(
                    conversation_id=conversation.id,
                    question_id=question.id,
                    user_input=user_input,
                    bot_response=question.answer_text,
                    intent_detected='question',
                    confidence_score=random.uniform(0.7, 1.0),
                    response_time=random.uniform(0.1, 2.0),
                    keywords_extracted=question.keywords,
                    user_rating=random.randint(1, 5) if random.random() > 0.3 else None,
                    timestamp=message_time
                )
                db.session.add(message)
                
                # Incrementar uso de la pregunta
                question.usage_count += 1
        
        db.session.commit()
        print("✅ Conversaciones y mensajes creados")
        
        # 5. Crear estadísticas diarias
        print("📊 Creando estadísticas diarias...")
        for i in range(7):
            date = datetime.utcnow().date() - timedelta(days=i)
            
            # Calcular estadísticas para este día
            day_start = datetime.combine(date, datetime.min.time())
            day_end = datetime.combine(date, datetime.max.time())
            
            conversations_count = Conversation.query.filter(
                Conversation.started_at >= day_start,
                Conversation.started_at <= day_end
            ).count()
            
            messages_count = Message.query.filter(
                Message.timestamp >= day_start,
                Message.timestamp <= day_end
            ).count()
            
            unique_users = db.session.query(Conversation.session_id).filter(
                Conversation.started_at >= day_start,
                Conversation.started_at <= day_end
            ).distinct().count()
            
            # Crear estadísticas
            stats = ChatbotStats(
                date=date,
                total_conversations=conversations_count,
                total_messages=messages_count,
                unique_users=unique_users,
                avg_response_time=random.uniform(0.5, 1.5),
                avg_confidence_score=random.uniform(0.7, 0.95),
                avg_user_rating=random.uniform(3.5, 4.8)
            )
            db.session.add(stats)
        
        db.session.commit()
        print("✅ Estadísticas diarias creadas")
        
        print("\n🎉 ¡Base de datos poblada exitosamente!")
        print("\n📋 Resumen:")
        print(f"   • {len(users)} usuarios")
        print(f"   • {len(categories)} categorías")
        print(f"   • {len(questions)} preguntas")
        print(f"   • 20 conversaciones de ejemplo")
        print(f"   • Estadísticas de 7 días")
        print("\n🔑 Credenciales de administrador:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")

if __name__ == '__main__':
    create_sample_data() 