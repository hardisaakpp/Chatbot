import spacy
import re
import string
from collections import Counter
import difflib
from typing import List, Dict, Tuple, Set, Any
import json
import os

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    # Si el modelo no está instalado, descargarlo
    print("Descargando modelo de spaCy para español...")
    os.system("python -m spacy download es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

class AdvancedTextProcessor:
    def __init__(self):
        self.nlp = nlp
        
        # Stop words específicas del dominio académico
        self.domain_stop_words = {
            'hola', 'gracias', 'por favor', 'ok', 'vale', 'si', 'no',
            'que', 'como', 'cuando', 'donde', 'porque', 'para', 'con',
            'sin', 'sobre', 'entre', 'hacia', 'desde', 'hasta', 'durante',
            'muy', 'mas', 'menos', 'poco', 'mucho', 'todo', 'nada'
        }
        
        # Diccionario de sinónimos y variaciones académicas
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
            'gcp': ['google cloud platform', 'plataforma en la nube de google'],
            'matematica': ['matemáticas', 'math', 'mathematics'],
            'fisica': ['física', 'physics'],
            'quimica': ['química', 'chemistry'],
            'biologia': ['biología', 'biology'],
            'historia': ['history'],
            'geografia': ['geografía', 'geography'],
            'literatura': ['literature'],
            'filosofia': ['filosofía', 'philosophy']
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
        Procesamiento completo del texto usando spaCy
        """
        if not text or not text.strip():
            return []
        
        # Procesar con spaCy
        doc = self.nlp(text.lower())
        
        # Extraer tokens relevantes
        tokens = []
        for token in doc:
            # Filtrar tokens relevantes
            if self._is_relevant_token(token):
                # Usar lema en lugar de token original
                tokens.append(token.lemma_)
        
        # Expansión de sinónimos
        tokens = self._expand_synonyms(tokens)
        
        # Eliminación de duplicados manteniendo orden
        tokens = list(dict.fromkeys(tokens))
        
        return tokens

    def _is_relevant_token(self, token) -> bool:
        """
        Determinar si un token es relevante para el procesamiento
        """
        # Excluir stop words de spaCy y del dominio
        if token.is_stop or token.lemma_ in self.domain_stop_words:
            return False
        
        # Excluir puntuación
        if token.is_punct:
            return False
        
        # Excluir espacios
        if token.is_space:
            return False
        
        # Excluir números
        if token.like_num:
            return False
        
        # Excluir tokens muy cortos o muy largos
        if len(token.lemma_) < 2 or len(token.lemma_) > 20:
            return False
        
        # Incluir solo sustantivos, verbos, adjetivos y adverbios
        return token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN']

    def _expand_synonyms(self, tokens: List[str]) -> List[str]:
        """
        Expansión de sinónimos usando spaCy
        """
        expanded = []
        for token in tokens:
            expanded.append(token)
            
            # Buscar sinónimos en el diccionario
            for key, synonyms in self.synonyms.items():
                if token == key or token in synonyms:
                    expanded.extend(synonyms)
        
        return expanded

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extracción de palabras clave usando spaCy
        """
        doc = self.nlp(text.lower())
        
        # Extraer sustantivos y verbos como palabras clave
        keywords = []
        for token in doc:
            if token.pos_ in ['NOUN', 'VERB', 'PROPN'] and not token.is_stop:
                keywords.append(token.lemma_)
        
        # Filtrar palabras muy comunes
        common_words = {'ser', 'estar', 'tener', 'hacer', 'decir', 'ver', 'dar', 'saber', 'poder', 'deber'}
        keywords = [kw for kw in keywords if kw not in common_words]
        
        return keywords[:10]  # Limitar a 10 palabras clave

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extraer entidades nombradas usando spaCy
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities

    def extract_question_type(self, text: str) -> str:
        """
        Extraer el tipo de pregunta usando spaCy
        """
        doc = self.nlp(text.lower())
        
        # Buscar palabras interrogativas
        question_words = {
            'qué': 'what', 'que': 'what', 'q': 'what',
            'cómo': 'how', 'como': 'how',
            'cuándo': 'when', 'cuando': 'when',
            'dónde': 'where', 'donde': 'where',
            'por qué': 'why', 'porque': 'why',
            'cuál': 'which', 'cual': 'which'
        }
        
        for token in doc:
            if token.text in question_words:
                return question_words[token.text]
        
        return 'general'

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcular similitud entre dos textos usando spaCy
        """
        # Procesar ambos textos
        doc1 = self.nlp(text1.lower())
        doc2 = self.nlp(text2.lower())
        
        # Similitud semántica usando spaCy
        semantic_similarity = doc1.similarity(doc2)
        
        # Similitud basada en tokens
        tokens1 = set(self.preprocess(text1))
        tokens2 = set(self.preprocess(text2))
        
        if not tokens1 or not tokens2:
            return semantic_similarity
        
        # Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        jaccard = intersection / union if union > 0 else 0
        
        # Sequence matcher para similitud de caracteres
        sequence_similarity = difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # Promedio ponderado (dar más peso a la similitud semántica)
        final_similarity = (semantic_similarity * 0.5 + jaccard * 0.3 + sequence_similarity * 0.2)
        
        return min(final_similarity, 1.0)

    def find_best_match(self, user_input: str, questions: List[str], threshold: float = 0.3) -> Tuple[str, float]:
        """
        Encontrar la mejor coincidencia usando spaCy
        """
        best_match = ""
        best_score = 0.0
        
        for question in questions:
            score = self.calculate_similarity(user_input, question)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = question
        
        return best_match, best_score

    def extract_intent(self, text: str) -> Dict[str, Any]:
        """
        Extraer intención del usuario usando spaCy
        """
        doc = self.nlp(text.lower())
        
        intent = {
            'type': 'question',
            'confidence': 0.8,
            'keywords': self.extract_keywords(text),
            'question_type': self.extract_question_type(text),
            'entities': self.extract_entities(text)
        }
        
        # Detectar saludos
        greetings = ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'saludos']
        if any(greeting in text.lower() for greeting in greetings):
            intent['type'] = 'greeting'
            intent['confidence'] = 0.9
        
        # Detectar despedidas
        farewells = ['adiós', 'hasta luego', 'nos vemos', 'chao', 'bye']
        if any(farewell in text.lower() for farewell in farewells):
            intent['type'] = 'farewell'
            intent['confidence'] = 0.9
        
        # Detectar agradecimientos
        thanks = ['gracias', 'grasias', 'thank you', 'thanks']
        if any(thank in text.lower() for thank in thanks):
            intent['type'] = 'thanks'
            intent['confidence'] = 0.9
        
        return intent

    def get_sentence_structure(self, text: str) -> Dict[str, Any]:
        """
        Analizar la estructura de la oración usando spaCy
        """
        doc = self.nlp(text)
        
        structure = {
            'subject': [],
            'verb': [],
            'object': [],
            'dependencies': []
        }
        
        for token in doc:
            # Extraer sujeto
            if token.dep_ in ['nsubj', 'nsubjpass']:
                structure['subject'].append(token.text)
            
            # Extraer verbo
            elif token.pos_ == 'VERB':
                structure['verb'].append(token.text)
            
            # Extraer objeto
            elif token.dep_ in ['dobj', 'pobj']:
                structure['object'].append(token.text)
            
            # Guardar dependencias
            structure['dependencies'].append({
                'token': token.text,
                'dep': token.dep_,
                'head': token.head.text
            })
        
        return structure

# Instancia global del procesador
processor = AdvancedTextProcessor()

def preprocess(text: str) -> List[str]:
    """
    Función de compatibilidad con el código existente
    """
    return processor.preprocess(text)

def get_best_response(user_input: str, responses_data: Dict) -> Tuple[str, float]:
    """
    Obtener la mejor respuesta basada en el procesamiento con spaCy
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