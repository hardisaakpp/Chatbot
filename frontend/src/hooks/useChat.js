import { useState, useRef, useEffect } from 'react';
import { apiService } from '../services/api';
import { SYSTEM_MESSAGES } from '../utils/constants';

export const useChat = () => {
  const [messages, setMessages] = useState([
    {
      from: 'bot',
      text: SYSTEM_MESSAGES.WELCOME,
    },
    {
      from: 'bot',
      text: SYSTEM_MESSAGES.HELP,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [categories, setCategories] = useState([]); // Guardar categorías para interacción
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async (message) => {
    if (message.trim() === '' || isLoading) return;
    
    const userMessage = message.trim();
    setMessages(prevMessages => [...prevMessages, { from: 'user', text: userMessage }]);
    
    try {
      setIsLoading(true);
      const botResponse = await apiService.sendMessage(userMessage);
      setMessages(prevMessages => [...prevMessages, { from: 'bot', text: botResponse }]);
    } catch {
      setMessages(prevMessages => [...prevMessages, { from: 'bot', text: SYSTEM_MESSAGES.ERROR }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Botón: Temas disponibles
  const showCategories = async () => {
    if (isLoading) return;
    setIsLoading(true);
    try {
      const cats = await apiService.getCategories();
      setCategories(cats); // Guardar para interacción
      if (cats && cats.length > 0) {
        setMessages(prev => [...prev, { from: 'bot', type: 'categories', categories: cats, text: 'Estos son los temas disponibles:' }]);
      } else {
        setMessages(prev => [...prev, { from: 'bot', text: 'No hay temas disponibles en este momento.' }]);
      }
    } catch {
      setMessages(prev => [...prev, { from: 'bot', text: 'No se pudieron obtener los temas disponibles.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Botón: ¿Cómo funciona?
  const showHowItWorks = () => {
    if (isLoading) return;
    setMessages(prev => [...prev, { from: 'bot', text: 'Soy un chatbot académico. Puedes preguntarme sobre temas de tecnología, ciencia, matemáticas, programación y más. Simplemente escribe tu pregunta y te responderé con la mejor información disponible. ¡Prueba preguntando sobre inteligencia artificial, bases de datos, o hábitos de estudio!' }]);
  };

  // Al hacer clic en un tema
  const handleCategoryClick = async (categoryId, categoryName) => {
    if (isLoading) return;
    setIsLoading(true);
    try {
      const questions = await apiService.getQuestionsByCategory(categoryId);
      if (questions && questions.length > 0) {
        const list = questions.map(q => `• ${q.question}`).join('\n');
        setMessages(prev => [...prev, { from: 'bot', text: `Preguntas frecuentes de "${categoryName}":\n${list}` }]);
      } else {
        setMessages(prev => [...prev, { from: 'bot', text: `No hay preguntas frecuentes de "${categoryName}" en este momento.` }]);
      }
    } catch {
      setMessages(prev => [...prev, { from: 'bot', text: `No se pudieron obtener las preguntas de "${categoryName}".` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const askQuestion = async (question) => {
    if (isLoading) return;
    // Lógica especial para los botones
    if (question.toLowerCase().includes('temas disponibles')) {
      await showCategories();
      return;
    }
    if (question.toLowerCase().includes('cómo funciona')) {
      showHowItWorks();
      return;
    }
    // Por defecto, enviar al backend
    await sendMessage(question);
  };

  const clearChat = () => {
    setMessages([
      {
        from: 'bot',
        text: SYSTEM_MESSAGES.WELCOME,
      },
      {
        from: 'bot',
        text: SYSTEM_MESSAGES.HELP,
      },
    ]);
    setCategories([]);
  };

  return {
    messages,
    isLoading,
    chatEndRef,
    sendMessage,
    askQuestion,
    clearChat,
    categories,
    handleCategoryClick
  };
}; 