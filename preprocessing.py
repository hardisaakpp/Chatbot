import nltk
import re
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.util import ngrams
from collections import Counter
import difflib
from typing import List, Dict, Tuple, Set
import json

# Descargar recursos necesarios
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

class AdvancedTextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('spanish'))
        
        # Agregar stop words específicas del dominio
        self.stop_words.update([
            'hola', 'gracias', 'por favor', 'ok', 'vale', 'si', 'no',
            'que', 'como', 'cuando', 'donde', 'porque', 'para', 'con',
            'sin', 'sobre', 'entre', 'hacia', 'desde', 'hasta', 'durante'
        ])
        
        # Diccionario de sinónimos y variaciones
        self.synonyms = {
            'ai': ['inteligencia artificial', 'ia', 'artificial intelligence'],
            'ml': ['machine learning', 'aprendizaje automático', 'aprendizaje de máquinas'],
            'dl': ['deep learning', 'aprendizaje profundo'],
            'nlp': ['procesamiento de lenguaje natural', 'natural language processing'],
            'bd': ['base de datos', 'database'],
            'db': ['base de datos', 'database'],
            'os': ['sistema operativo', 'operating system'],
            'iot': ['internet de las cosas', 'internet of things'],
            'ar': ['realidad aumentada', 'augmented reality'],
            'vr': ['realidad virtual', 'virtual reality'],
            'api': ['interfaz de programación', 'application programming interface'],
            'oop': ['programación orientada a objetos', 'object oriented programming'],
            'fp': ['programación funcional', 'functional programming'],
            'sql': ['structured query language', 'lenguaje de consulta estructurado'],
            'nosql': ['not only sql', 'no solo sql'],
            'git': ['control de versiones', 'version control'],
            'docker': ['contenedorización', 'containerization'],
            'kubernetes': ['orquestación de contenedores', 'container orchestration'],
            'aws': ['amazon web services', 'servicios web de amazon'],
            'azure': ['microsoft azure', 'servicios en la nube de microsoft'],
            'gcp': ['google cloud platform', 'plataforma en la nube de google']
        }
        
        # Patrones de preguntas comunes
        self.question_patterns = [
            r'^(qué|que|q)\s+es\s+(.+)',
            r'^(cómo|como)\s+(.+)',
            r'^(cuál|cuando|donde|por qué|para qué)\s+(.+)',
            r'^(explica|define|describe)\s+(.+)',
            r'^(dime|dame|muéstrame)\s+(.+)',
            r'^(información|info)\s+sobre\s+(.+)',
            r'^(habla|hablar)\s+de\s+(.+)',
            r'^(ayuda|ayúdame)\s+con\s+(.+)'
        ]

    def preprocess(self, text: str) -> List[str]:
        """
        Procesamiento completo del texto con múltiples técnicas
        """
        if not text or not text.strip():
            return []
        
        # Normalización básica
        text = self._normalize_text(text)
        
        # Tokenización
        tokens = word_tokenize(text.lower())
        
        # Limpieza y filtrado
        tokens = self._clean_tokens(tokens)
        
        # Lematización y stemming
        tokens = self._lemmatize_and_stem(tokens)
        
        # Expansión de sinónimos
        tokens = self._expand_synonyms(tokens)
        
        # Eliminación de duplicados manteniendo orden
        tokens = list(dict.fromkeys(tokens))
        
        return tokens

    def _normalize_text(self, text: str) -> str:
        """
        Normalización del texto
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Reemplazar caracteres especiales
        text = re.sub(r'[^\w\s\?¿¡!]', ' ', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        # Normalizar acentos (opcional)
        text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        text = text.replace('ü', 'u').replace('ñ', 'n')
        
        return text.strip()

    def _clean_tokens(self, tokens: List[str]) -> List[str]:
        """
        Limpieza de tokens
        """
        cleaned = []
        for token in tokens:
            # Eliminar tokens muy cortos o muy largos
            if len(token) < 2 or len(token) > 20:
                continue
            
            # Eliminar tokens que son solo números
            if token.isdigit():
                continue
            
            # Eliminar stop words
            if token in self.stop_words:
                continue
            
            # Eliminar tokens que son solo puntuación
            if token in string.punctuation:
                continue
            
            cleaned.append(token)
        
        return cleaned

    def _lemmatize_and_stem(self, tokens: List[str]) -> List[str]:
        """
        Lematización y stemming combinados
        """
        processed = []
        for token in tokens:
            # Lematización
            lemma = self.lemmatizer.lemmatize(token)
            
            # Stemming
            stem = self.stemmer.stem(token)
            
            # Usar el más corto entre lema y stem
            processed.append(lemma if len(lemma) <= len(stem) else stem)
        
        return processed

    def _expand_synonyms(self, tokens: List[str]) -> List[str]:
        """
        Expansión de sinónimos
        """
        expanded = []
        for token in tokens:
            expanded.append(token)
            
            # Buscar sinónimos
            for key, synonyms in self.synonyms.items():
                if token == key or token in synonyms:
                    expanded.extend(synonyms)
        
        return expanded

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extracción de palabras clave
        """
        tokens = self.preprocess(text)
        
        # Filtrar por frecuencia (eliminar palabras muy comunes)
        common_words = {'ser', 'estar', 'tener', 'hacer', 'decir', 'ver', 'dar', 'saber', 'poder', 'deber'}
        keywords = [token for token in tokens if token not in common_words]
        
        return keywords[:10]  # Limitar a 10 palabras clave

    def extract_question_type(self, text: str) -> str:
        """
        Extraer el tipo de pregunta
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['qué', 'que', 'q']):
            return 'what'
        elif any(word in text_lower for word in ['cómo', 'como']):
            return 'how'
        elif any(word in text_lower for word in ['cuándo', 'cuando']):
            return 'when'
        elif any(word in text_lower for word in ['dónde', 'donde']):
            return 'where'
        elif any(word in text_lower for word in ['por qué', 'porque']):
            return 'why'
        elif any(word in text_lower for word in ['cuál', 'cual']):
            return 'which'
        else:
            return 'general'

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcular similitud entre dos textos usando múltiples métodos
        """
        tokens1 = set(self.preprocess(text1))
        tokens2 = set(self.preprocess(text2))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        jaccard = intersection / union if union > 0 else 0
        
        # Cosine similarity (simplificado)
        common_tokens = tokens1.intersection(tokens2)
        cosine = len(common_tokens) / (len(tokens1) * len(tokens2)) ** 0.5
        
        # Sequence matcher para similitud de caracteres
        sequence_similarity = difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # Promedio ponderado
        final_similarity = (jaccard * 0.4 + cosine * 0.4 + sequence_similarity * 0.2)
        
        return min(final_similarity, 1.0)

    def find_best_match(self, user_input: str, questions: List[str], threshold: float = 0.3) -> Tuple[str, float]:
        """
        Encontrar la mejor coincidencia entre la entrada del usuario y las preguntas disponibles
        """
        best_match = ""
        best_score = 0.0
        
        for question in questions:
            score = self.calculate_similarity(user_input, question)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = question
        
        return best_match, best_score

    def generate_ngrams(self, text: str, n: int = 2) -> List[str]:
        """
        Generar n-gramas para mejor matching
        """
        tokens = self.preprocess(text)
        ngrams_list = list(ngrams(tokens, n))
        return [' '.join(gram) for gram in ngrams_list]

    def extract_intent(self, text: str) -> Dict[str, any]:
        """
        Extraer intención del usuario
        """
        text_lower = text.lower()
        
        intent = {
            'type': 'question',
            'confidence': 0.8,
            'keywords': self.extract_keywords(text),
            'question_type': self.extract_question_type(text)
        }
        
        # Detectar saludos
        greetings = ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'saludos']
        if any(greeting in text_lower for greeting in greetings):
            intent['type'] = 'greeting'
            intent['confidence'] = 0.9
        
        # Detectar despedidas
        farewells = ['adiós', 'hasta luego', 'nos vemos', 'chao', 'bye']
        if any(farewell in text_lower for farewell in farewells):
            intent['type'] = 'farewell'
            intent['confidence'] = 0.9
        
        # Detectar agradecimientos
        thanks = ['gracias', 'grasias', 'thank you', 'thanks']
        if any(thank in text_lower for thank in thanks):
            intent['type'] = 'thanks'
            intent['confidence'] = 0.9
        
        return intent

# Instancia global del procesador
processor = AdvancedTextProcessor()

def preprocess(text: str) -> List[str]:
    """
    Función de compatibilidad con el código existente
    """
    return processor.preprocess(text)

def get_best_response(user_input: str, responses_data: Dict) -> Tuple[str, float]:
    """
    Obtener la mejor respuesta basada en el procesamiento avanzado
    """
    # Extraer intención
    intent = processor.extract_intent(user_input)
    
    # Manejar intenciones especiales
    if intent['type'] == 'greeting':
        greetings = responses_data.get('saludos', ['Hola, ¿en qué puedo ayudarte?'])
        return greetings[0], 1.0
    
    elif intent['type'] == 'farewell':
        farewells = responses_data.get('despedidas', ['Hasta luego, ¡que tengas un buen día!'])
        return farewells[0], 1.0
    
    elif intent['type'] == 'thanks':
        return '¡De nada! Estoy aquí para ayudarte.', 1.0
    
    # Buscar en preguntas frecuentes
    questions = responses_data.get('preguntas_frecuentes', {})
    if questions:
        best_match, score = processor.find_best_match(user_input, list(questions.keys()))
        if best_match and best_match in questions:
            return questions[best_match], score
    
    # Respuesta por defecto
    return "Lo siento, no tengo una respuesta específica para esa pregunta. ¿Podrías reformularla o preguntar sobre otro tema?", 0.0