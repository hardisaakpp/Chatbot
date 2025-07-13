import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';

const QuestionSuggestions = ({ sessionId, onSuggestionClick }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (sessionId) {
      loadSuggestions();
    }
  }, [sessionId]);

  const loadSuggestions = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getSuggestions(sessionId);
      setSuggestions(data);
    } catch (err) {
      console.error('Error cargando sugerencias:', err);
      setError('No se pudieron cargar las sugerencias');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    if (onSuggestionClick) {
      onSuggestionClick(suggestion.question);
    }
  };

  if (loading) {
    return (
      <div className="p-4 text-center">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
        <p className="text-sm text-gray-600 mt-2">Cargando sugerencias...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-center">
        <p className="text-sm text-red-600">{error}</p>
        <button
          onClick={loadSuggestions}
          className="mt-2 text-sm text-blue-600 hover:text-blue-800 underline"
        >
          Intentar de nuevo
        </button>
      </div>
    );
  }

  if (suggestions.length === 0) {
    return null;
  }

  return (
    <div className="border-t border-gray-200 pt-4">
      <h4 className="text-sm font-medium text-gray-700 mb-3">
        💡 Preguntas sugeridas:
      </h4>
      
      <div className="space-y-2">
        {suggestions.map((suggestion, index) => (
          <button
            key={`${suggestion.id}-${index}`}
            onClick={() => handleSuggestionClick(suggestion)}
            className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors group"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm text-gray-800 group-hover:text-gray-900">
                  {suggestion.question}
                </p>
                <div className="flex items-center mt-1 space-x-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    suggestion.type === 'popular' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {suggestion.type === 'popular' ? '🔥 Popular' : '🔗 Relacionada'}
                  </span>
                  {suggestion.usage_count && (
                    <span className="text-xs text-gray-500">
                      {suggestion.usage_count} usos
                    </span>
                  )}
                  {suggestion.category && (
                    <span className="text-xs text-gray-500">
                      {suggestion.category}
                    </span>
                  )}
                </div>
              </div>
              <svg 
                className="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>
        ))}
      </div>
      
      <div className="mt-3 text-center">
        <button
          onClick={loadSuggestions}
          className="text-xs text-blue-600 hover:text-blue-800 underline"
        >
          Actualizar sugerencias
        </button>
      </div>
    </div>
  );
};

export default QuestionSuggestions; 