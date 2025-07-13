#!/usr/bin/env python3
"""
Script de prueba para verificar que spaCy funciona correctamente
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_spacy_installation():
    """Probar la instalación básica de spaCy"""
    print("🔍 Probando instalación de spaCy...")
    
    try:
        import spacy
        print("✅ spaCy importado correctamente")
        
        # Cargar modelo
        nlp = spacy.load("es_core_news_sm")
        print("✅ Modelo de español cargado correctamente")
        
        return nlp
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_text_processing(nlp):
    """Probar el procesamiento de texto"""
    print("\n🔍 Probando procesamiento de texto...")
    
    test_texts = [
        "¿Qué es la inteligencia artificial?",
        "Explica cómo funciona el machine learning",
        "Hola, ¿cómo estás?",
        "Gracias por tu ayuda",
        "¿Cuál es la diferencia entre SQL y NoSQL?"
    ]
    
    for text in test_texts:
        print(f"\n📝 Texto: '{text}'")
        doc = nlp(text)
        
        # Tokens
        tokens = [token.text for token in doc if not token.is_space]
        print(f"   Tokens: {tokens}")
        
        # Lemas
        lemmas = [token.lemma_ for token in doc if not token.is_space and not token.is_punct]
        print(f"   Lemas: {lemmas}")
        
        # POS tags
        pos_tags = [(token.text, token.pos_) for token in doc if not token.is_space]
        print(f"   POS: {pos_tags}")
        
        # Entidades
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        if entities:
            print(f"   Entidades: {entities}")

def test_advanced_processor():
    """Probar el procesador avanzado"""
    print("\n🔍 Probando procesador avanzado...")
    
    try:
        from backend.utils.preprocessing import processor
        
        test_cases = [
            ("¿Qué es la inteligencia artificial?", "pregunta sobre IA"),
            ("Hola, ¿cómo estás?", "saludo"),
            ("Gracias por tu ayuda", "agradecimiento"),
            ("Explica las matemáticas", "pregunta sobre matemáticas")
        ]
        
        for text, description in test_cases:
            print(f"\n📝 {description}: '{text}'")
            
            # Preprocesamiento
            tokens = processor.preprocess(text)
            print(f"   Tokens procesados: {tokens}")
            
            # Palabras clave
            keywords = processor.extract_keywords(text)
            print(f"   Palabras clave: {keywords}")
            
            # Intención
            intent = processor.extract_intent(text)
            print(f"   Intención: {intent['type']} (confianza: {intent['confidence']:.2f})")
            
            # Entidades
            entities = processor.extract_entities(text)
            if entities:
                print(f"   Entidades: {entities}")
            
            # Estructura de oración
            structure = processor.get_sentence_structure(text)
            if structure['subject'] or structure['verb'] or structure['object']:
                print(f"   Estructura: S={structure['subject']}, V={structure['verb']}, O={structure['object']}")
        
        return True
    except Exception as e:
        print(f"❌ Error en procesador avanzado: {e}")
        return False

def test_similarity():
    """Probar cálculo de similitud"""
    print("\n🔍 Probando cálculo de similitud...")
    
    try:
        from backend.utils.preprocessing import processor
        
        test_pairs = [
            ("¿Qué es la IA?", "¿Qué es la inteligencia artificial?"),
            ("Hola", "Buenos días"),
            ("Gracias", "Muchas gracias"),
            ("Matemáticas", "Matemática")
        ]
        
        for text1, text2 in test_pairs:
            similarity = processor.calculate_similarity(text1, text2)
            print(f"   '{text1}' vs '{text2}': {similarity:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ Error en cálculo de similitud: {e}")
        return False

def main():
    print("🧪 Pruebas de spaCy para Chatbot Académico")
    print("=" * 50)
    
    # Probar instalación
    nlp = test_spacy_installation()
    if not nlp:
        print("❌ No se pudo cargar spaCy")
        sys.exit(1)
    
    # Probar procesamiento básico
    test_text_processing(nlp)
    
    # Probar procesador avanzado
    if not test_advanced_processor():
        print("❌ Error en procesador avanzado")
        sys.exit(1)
    
    # Probar similitud
    if not test_similarity():
        print("❌ Error en cálculo de similitud")
        sys.exit(1)
    
    print("\n🎉 ¡Todas las pruebas pasaron!")
    print("✅ spaCy está funcionando correctamente")
    print("✅ El procesador avanzado está operativo")
    print("✅ El cálculo de similitud funciona")
    print("\n🚀 El chatbot está listo para usar spaCy")

if __name__ == "__main__":
    main() 