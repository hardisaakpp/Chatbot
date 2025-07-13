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

  const askQuestion = async (question) => {
    if (isLoading) return;
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
  };

  return {
    messages,
    isLoading,
    chatEndRef,
    sendMessage,
    askQuestion,
    clearChat
  };
}; 