#!/usr/bin/env python3
"""
Script para migrar datos del archivo JSON a la base de datos SQLite
"""

import json
import os
from datetime import datetime
from models import db, Category, Question, User
from config import config

def create_app():
    """Crear aplicación Flask para la migración"""
    from flask import Flask
    
    app = Flask(__name__)
    app.config.from_object(config['development'])
    
    db.init_app(app)
    
    return app

def load_json_data():
    """Cargar datos del archivo JSON"""
    try:
        with open('responses.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo responses.json")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: JSON inválido en responses.json: {e}")
        return None

def create_default_categories():
    """Crear categorías por defecto"""
    categories = [
        {
            'name': 'Inteligencia Artificial',
            'description': 'Preguntas sobre IA, machine learning y deep learning',
            'icon': 'fas fa-brain',
            'color': '#6200ea'
        },
        {
            'name': 'Programación',
            'description': 'Lenguajes de programación y desarrollo de software',
            'icon': 'fas fa-code',
            'color': '#03dac6'
        },
        {
            'name': 'Bases de Datos',
            'description': 'Sistemas de gestión de bases de datos',
            'icon': 'fas fa-database',
            'color': '#ff6b6b'
        },
        {
            'name': 'Ciberseguridad',
            'description': 'Seguridad informática y protección de datos',
            'icon': 'fas fa-shield-alt',
            'color': '#4ecdc4'
        },
        {
            'name': 'Tecnologías Emergentes',
            'description': 'Blockchain, IoT, realidad aumentada y virtual',
            'icon': 'fas fa-rocket',
            'color': '#45b7d1'
        },
        {
            'name': 'Metodologías',
            'description': 'Agile, DevOps, metodologías de desarrollo',
            'icon': 'fas fa-tasks',
            'color': '#96ceb4'
        },
        {
            'name': 'Estudio y Productividad',
            'description': 'Técnicas de estudio y mejora de productividad',
            'icon': 'fas fa-graduation-cap',
            'color': '#feca57'
        },
        {
            'name': 'General',
            'description': 'Preguntas generales y misceláneas',
            'icon': 'fas fa-question-circle',
            'color': '#6c5ce7'
        }
    ]
    
    created_categories = {}
    
    for cat_data in categories:
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            db.session.commit()
            print(f"✅ Categoría creada: {category.name}")
        else:
            print(f"ℹ️ Categoría ya existe: {category.name}")
        
        created_categories[cat_data['name']] = category
    
    return created_categories

def map_question_to_category(question_text, categories):
    """Mapear pregunta a categoría basándose en palabras clave"""
    question_lower = question_text.lower()
    
    # Mapeo de palabras clave a categorías
    category_keywords = {
        'Inteligencia Artificial': ['ai', 'inteligencia artificial', 'machine learning', 'ml', 'deep learning', 'dl', 'nlp', 'neural', 'red neuronal'],
        'Programación': ['programacion', 'programar', 'lenguaje', 'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'git', 'docker', 'kubernetes'],
        'Bases de Datos': ['base de datos', 'bd', 'sql', 'nosql', 'database', 'mysql', 'postgresql', 'mongodb'],
        'Ciberseguridad': ['ciberseguridad', 'seguridad', 'hacker', 'malware', 'phishing', 'firewall', 'criptografia'],
        'Tecnologías Emergentes': ['blockchain', 'iot', 'realidad aumentada', 'ar', 'realidad virtual', 'vr', 'nube', 'cloud', 'aws', 'azure', 'gcp'],
        'Metodologías': ['agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'testing', 'microservicios'],
        'Estudio y Productividad': ['estudio', 'habito', 'productividad', 'aprender', 'técnica', 'método']
    }
    
    for category_name, keywords in category_keywords.items():
        if any(keyword in question_lower for keyword in keywords):
            return categories.get(category_name)
    
    # Si no coincide, usar categoría General
    return categories.get('General')

def migrate_questions(json_data, categories):
    """Migrar preguntas del JSON a la base de datos"""
    questions_data = json_data.get('preguntas_frecuentes', {})
    
    migrated_count = 0
    skipped_count = 0
    
    for question_text, answer_text in questions_data.items():
        # Verificar si la pregunta ya existe
        existing_question = Question.query.filter_by(question_text=question_text).first()
        if existing_question:
            print(f"ℹ️ Pregunta ya existe: {question_text[:50]}...")
            skipped_count += 1
            continue
        
        # Determinar categoría
        category = map_question_to_category(question_text, categories)
        
        # Extraer palabras clave (simplificado)
        keywords = extract_keywords(question_text)
        
        # Crear nueva pregunta
        question_data = {
            'question_text': question_text,
            'answer_text': answer_text,
            'category_id': category.id if category else None,
            'keywords': ', '.join(keywords),
            'difficulty_level': 1,  # Por defecto fácil
            'is_active': True
        }
        question = Question(**question_data)
        
        db.session.add(question)
        migrated_count += 1
        print(f"✅ Pregunta migrada: {question_text[:50]}...")
    
    db.session.commit()
    return migrated_count, skipped_count

def extract_keywords(text):
    """Extraer palabras clave del texto (versión simplificada)"""
    # Lista de palabras comunes a excluir
    stop_words = {
        'que', 'es', 'el', 'la', 'de', 'del', 'y', 'o', 'a', 'en', 'con', 'por', 'para',
        'como', 'cuando', 'donde', 'porque', 'si', 'no', 'un', 'una', 'unos', 'unas',
        'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'mi', 'tu', 'su'
    }
    
    # Convertir a minúsculas y dividir en palabras
    words = text.lower().split()
    
    # Filtrar palabras comunes y palabras muy cortas
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Limitar a 10 palabras clave
    return keywords[:10]

def create_admin_user():
    """Crear usuario administrador por defecto"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_data = {
            'username': 'admin',
            'email': 'admin@chatbot.com',
            'is_admin': True,
            'is_active': True
        }
        admin = User(**admin_data)
        admin.set_password('admin123')  # Cambiar en producción
        
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario administrador creado:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("   ⚠️  IMPORTANTE: Cambia la contraseña en producción")
    else:
        print("ℹ️ Usuario administrador ya existe")

def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración de datos JSON a base de datos...")
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        # Crear tablas
        db.create_all()
        print("✅ Tablas de base de datos creadas")
        
        # Cargar datos JSON
        json_data = load_json_data()
        if not json_data:
            return
        
        print(f"✅ Datos JSON cargados: {len(json_data.get('preguntas_frecuentes', {}))} preguntas")
        
        # Crear categorías
        print("\n📂 Creando categorías...")
        categories = create_default_categories()
        
        # Migrar preguntas
        print("\n📝 Migrando preguntas...")
        migrated, skipped = migrate_questions(json_data, categories)
        
        # Crear usuario administrador
        print("\n👤 Creando usuario administrador...")
        create_admin_user()
        
        # Resumen
        print("\n🎉 Migración completada exitosamente!")
        print(f"   📊 Preguntas migradas: {migrated}")
        print(f"   ⏭️ Preguntas omitidas: {skipped}")
        print(f"   📂 Categorías creadas: {len(categories)}")
        print(f"   👤 Usuario admin: admin/admin123")
        print("\n💡 Próximos pasos:")
        print("   1. Ejecuta la aplicación: python app.py")
        print("   2. Accede al panel admin: http://localhost:5002/admin")
        print("   3. Cambia la contraseña del administrador")

if __name__ == '__main__':
    main() 