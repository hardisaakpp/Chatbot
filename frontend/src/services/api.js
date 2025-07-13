import { APP_CONFIG } from '../utils/constants';

const API_BASE_URL = APP_CONFIG.API_BASE_URL;

export const apiService = {
  async sendMessage(message) {
    try {
      const formData = new FormData();
      formData.append('user_input', message);
      
      const response = await fetch(`${API_BASE_URL}/get_response`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      return data.response;
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      throw new Error('Lo siento, tuve un problema procesando tu pregunta. ¿Podrías intentar de nuevo?');
    }
  },

  async getStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error);
      throw error;
    }
  },

  async getCategories() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/categories`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error obteniendo categorías:', error);
      throw error;
    }
  },

  async getQuestionsByCategory(categoryId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/questions?category_id=${categoryId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error obteniendo preguntas por categoría:', error);
      throw error;
    }
  },

  async submitFeedback(feedbackData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error enviando feedback:', error);
      throw error;
    }
  },

  async getSuggestions(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/suggestions?session_id=${sessionId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error obteniendo sugerencias:', error);
      throw error;
    }
  },

  async getAnalytics() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error obteniendo analytics:', error);
      throw error;
    }
  }
}; 