#!/usr/bin/env python3
"""
Script para instalar spaCy y descargar el modelo de español
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Instalando spaCy y modelo de español...")
    print("=" * 50)
    
    # Verificar si Python está disponible
    if not run_command("python --version", "Verificando Python"):
        print("❌ Python no está disponible")
        sys.exit(1)
    
    # Instalar spaCy (versión más reciente)
    if not run_command("pip install spacy", "Instalando spaCy"):
        print("❌ Error al instalar spaCy")
        sys.exit(1)
    
    # Descargar modelo de español
    if not run_command("python -m spacy download es_core_news_sm", "Descargando modelo de español"):
        print("❌ Error al descargar modelo de español")
        sys.exit(1)
    
    # Verificar instalación
    print("\n🔍 Verificando instalación...")
    try:
        import spacy
        nlp = spacy.load("es_core_news_sm")
        test_text = "Hola, ¿cómo estás?"
        doc = nlp(test_text)
        print(f"✅ spaCy funcionando correctamente")
        print(f"   Texto de prueba: '{test_text}'")
        print(f"   Tokens: {[token.text for token in doc]}")
    except Exception as e:
        print(f"❌ Error al verificar spaCy: {e}")
        sys.exit(1)
    
    print("\n🎉 ¡spaCy instalado correctamente!")
    print("📝 El modelo de español está listo para usar")
    print("\n💡 Para usar spaCy en tu código:")
    print("   import spacy")
    print("   nlp = spacy.load('es_core_news_sm')")
    print("   doc = nlp('Tu texto aquí')")

if __name__ == "__main__":
    main() 