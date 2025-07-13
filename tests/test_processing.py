#!/usr/bin/env python3
"""
Script de prueba para demostrar las mejoras en el procesamiento del chatbot
"""

import json
from backend.utils.preprocessing import processor, get_best_response

def test_processing_improvements():
    """Demostrar las mejoras en el procesamiento"""
    
    # Cargar respuestas
    with open('responses.json', 'r', encoding='utf-8') as f:
        responses = json.load(f)
    
    print("🤖 **DEMOSTRACIÓN DE MEJORAS EN EL PROCESAMIENTO**\n")
    
    # Casos de prueba
    test_cases = [
        # Saludos
        "hola",
        "buenos días",
        "saludos",
        
        # Despedidas
        "adiós",
        "hasta luego",
        "nos vemos",
        
        # Agradecimientos
        "gracias",
        "thank you",
        
        # Preguntas con sinónimos
        "que es ai",
        "que es machine learning",
        "que es ml",
        "que es deep learning",
        "que es dl",
        "que es nlp",
        "que es bd",
        "que es os",
        "que es iot",
        "que es ar",
        "que es vr",
        "que es api",
        "que es oop",
        "que es fp",
        "que es sql",
        "que es nosql",
        "que es git",
        "que es docker",
        "que es kubernetes",
        "que es aws",
        "que es azure",
        "que es gcp",
        
        # Preguntas con variaciones
        "explica que es inteligencia artificial",
        "dime que es machine learning",
        "define deep learning",
        "información sobre blockchain",
        "habla de ciberseguridad",
        "ayuda con programación",
        
        # Preguntas con errores tipográficos
        "que es inteligenci artifical",
        "que es machin lernin",
        "que es deep lernin",
        
        # Preguntas en diferentes formatos
        "¿Qué es la inteligencia artificial?",
        "¿Cómo funciona machine learning?",
        "¿Cuál es la definición de deep learning?",
        
        # Preguntas complejas
        "como puedo aprender programacion desde cero",
        "que necesito para empezar en ciberseguridad",
        "cuales son los mejores lenguajes de programacion",
        "como mejorar mis habitos de estudio",
        "que es la computacion en la nube y como funciona"
    ]
    
    print("📋 **CASOS DE PRUEBA:**\n")
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"**Caso {i}:** '{user_input}'")
        
        # Análisis completo
        intent = processor.extract_intent(user_input)
        keywords = processor.extract_keywords(user_input)
        question_type = processor.extract_question_type(user_input)
        
        # Obtener respuesta
        response, confidence = get_best_response(user_input, responses)
        
        print(f"  🎯 **Intención:** {intent['type']} (confianza: {intent['confidence']:.2f})")
        print(f"  🔍 **Tipo de pregunta:** {question_type}")
        print(f"  🏷️ **Palabras clave:** {keywords[:5]}")
        print(f"  📊 **Confianza de respuesta:** {confidence:.2f}")
        print(f"  💬 **Respuesta:** {response[:100]}{'...' if len(response) > 100 else ''}")
        print()
    
    print("🎉 **DEMOSTRACIÓN COMPLETADA**")
    print("\n**Mejoras implementadas:**")
    print("✅ Procesamiento avanzado de texto")
    print("✅ Detección de intenciones")
    print("✅ Manejo de sinónimos y variaciones")
    print("✅ Corrección de errores tipográficos")
    print("✅ Extracción de palabras clave")
    print("✅ Cálculo de similitud mejorado")
    print("✅ Respuestas contextuales")
    print("✅ Sugerencias para preguntas no encontradas")

def test_similarity():
    """Probar el cálculo de similitud"""
    print("\n🔍 **PRUEBA DE SIMILITUD:**\n")
    
    test_pairs = [
        ("que es ai", "que es inteligencia artificial"),
        ("que es ml", "que es machine learning"),
        ("que es deep learning", "que es dl"),
        ("como aprender programacion", "como aprender a programar"),
        ("que es bd", "que es base de datos"),
        ("que es os", "que es sistema operativo"),
        ("que es iot", "que es internet de las cosas"),
        ("que es ar", "que es realidad aumentada"),
        ("que es vr", "que es realidad virtual"),
        ("que es api", "que es interfaz de programacion"),
        ("que es oop", "que es programacion orientada a objetos"),
        ("que es fp", "que es programacion funcional"),
        ("que es sql", "que es structured query language"),
        ("que es nosql", "que es not only sql"),
        ("que es git", "que es control de versiones"),
        ("que es docker", "que es contenedorizacion"),
        ("que es kubernetes", "que es orquestacion de contenedores"),
        ("que es aws", "que es amazon web services"),
        ("que es azure", "que es microsoft azure"),
        ("que es gcp", "que es google cloud platform")
    ]
    
    for text1, text2 in test_pairs:
        similarity = processor.calculate_similarity(text1, text2)
        print(f"'{text1}' vs '{text2}': {similarity:.3f}")

if __name__ == "__main__":
    test_processing_improvements()
    test_similarity() 