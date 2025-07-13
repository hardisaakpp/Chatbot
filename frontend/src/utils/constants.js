// Configuración de la aplicación
export const APP_CONFIG = {
  TITLE: 'Chatbot Académico',
  VERSION: '1.0.0',
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5002',
};

// Mensajes del sistema
export const SYSTEM_MESSAGES = {
  WELCOME: '¡Hola! Soy tu asistente académico',
  HELP: 'Puedo ayudarte con preguntas sobre diversos temas. ¿En qué puedo asistirte hoy?',
  ERROR: 'Lo siento, tuve un problema procesando tu pregunta. ¿Podrías intentar de nuevo?',
  LOADING: 'Procesando tu pregunta...',
};

// Preguntas rápidas predefinidas
export const QUICK_QUESTIONS = [
  {
    text: 'Temas disponibles',
    question: '¿Cuáles son los temas disponibles?',
    icon: 'ListIcon'
  },
  {
    text: '¿Cómo funciona?',
    question: '¿Cómo funciona este chatbot?',
    icon: 'HelpOutlineIcon'
  },
  {
    text: 'Matemáticas',
    question: '¿Puedes ayudarme con matemáticas?',
    icon: 'CalculateIcon'
  }
];

// Configuración de animaciones
export const ANIMATION_CONFIG = {
  MESSAGE_TIMEOUT: 500,
  SCROLL_BEHAVIOR: 'smooth',
}; 