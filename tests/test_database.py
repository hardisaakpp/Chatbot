#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento de la base de datos
"""

import requests
import json
import time

def test_chatbot_api():
    """Probar la API del chatbot"""
    base_url = "http://localhost:5002"
    
    print("🧪 Probando API del Chatbot con Base de Datos")
    print("=" * 50)
    
    # Test 1: Obtener estadísticas
    print("\n1. 📊 Obteniendo estadísticas...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estadísticas obtenidas:")
            print(f"   - Total preguntas: {stats.get('total_questions', 0)}")
            print(f"   - Total conversaciones: {stats.get('total_conversations', 0)}")
            print(f"   - Total mensajes: {stats.get('total_messages', 0)}")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 2: Obtener categorías
    print("\n2. 📂 Obteniendo categorías...")
    try:
        response = requests.get(f"{base_url}/api/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Categorías obtenidas: {len(categories)}")
            for cat in categories[:3]:  # Mostrar solo las primeras 3
                print(f"   - {cat['name']}: {cat['question_count']} preguntas")
        else:
            print(f"❌ Error obteniendo categorías: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 3: Probar preguntas del chatbot
    test_questions = [
        "¿Qué es la inteligencia artificial?",
        "¿Cómo funciona machine learning?",
        "¿Qué es Docker?",
        "¿Qué es DevOps?",
        "¿Qué es una API REST?",
        "¿Qué es la realidad aumentada?",
        "¿Qué es Git?",
        "¿Qué es Kubernetes?",
        "¿Qué es AWS?",
        "¿Qué es GraphQL?"
    ]
    
    print(f"\n3. 🤖 Probando {len(test_questions)} preguntas...")
    
    for i, question in enumerate(test_questions, 1):
        try:
            print(f"\n   Pregunta {i}: {question}")
            
            response = requests.post(f"{base_url}/get_response", data={
                'user_input': question
            })
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', 'Sin respuesta')
                print(f"   ✅ Respuesta: {answer[:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
            # Pausa entre preguntas
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 4: Obtener estadísticas actualizadas
    print(f"\n4. 📊 Estadísticas después de las pruebas...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estadísticas actualizadas:")
            print(f"   - Total mensajes: {stats.get('total_messages', 0)}")
            print(f"   - Preguntas más populares:")
            for pq in stats.get('popular_questions', [])[:3]:
                print(f"     • {pq['question']} ({pq['usage_count']} usos)")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 5: Probar análisis de texto
    print(f"\n5. 🔍 Probando análisis de texto...")
    try:
        test_text = "¿Qué es la inteligencia artificial y cómo se relaciona con machine learning?"
        
        response = requests.post(f"{base_url}/api/analyze", json={
            'text': test_text
        })
        
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Análisis completado:")
            print(f"   - Keywords: {analysis.get('keywords', [])[:5]}")
            print(f"   - Intención: {analysis.get('intent', {}).get('type', 'N/A')}")
            print(f"   - Tipo de pregunta: {analysis.get('question_type', 'N/A')}")
        else:
            print(f"❌ Error en análisis: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")
    print("\n💡 Próximos pasos:")
    print("   1. Accede al chatbot: http://localhost:5002")
    print("   2. Panel de administración: http://localhost:5002/admin")
    print("   3. Usuario admin: admin / admin123")

if __name__ == '__main__':
    # Esperar un momento para que la aplicación se inicie
    print("⏳ Esperando que la aplicación se inicie...")
    time.sleep(3)
    
    test_chatbot_api() 