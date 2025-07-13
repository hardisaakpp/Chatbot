import React, { useState } from 'react';
import { apiService } from '../../services/api';

const FeedbackModal = ({ isOpen, onClose, messageId, userInput, botResponse }) => {
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (rating === 0) {
      alert('Por favor, selecciona una calificación');
      return;
    }

    setIsSubmitting(true);
    
    try {
      await apiService.submitFeedback({
        message_id: messageId,
        rating: rating,
        feedback_text: feedback
      });
      
      setSubmitStatus('success');
      setTimeout(() => {
        onClose();
        setRating(0);
        setFeedback('');
        setSubmitStatus(null);
      }, 2000);
      
    } catch (error) {
      console.error('Error enviando feedback:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            ¿Cómo fue tu experiencia?
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {submitStatus === 'success' ? (
          <div className="text-center py-8">
            <div className="text-green-500 text-6xl mb-4">✓</div>
            <p className="text-green-600 font-semibold">¡Gracias por tu feedback!</p>
            <p className="text-gray-600 text-sm">Tu opinión nos ayuda a mejorar</p>
          </div>
        ) : submitStatus === 'error' ? (
          <div className="text-center py-8">
            <div className="text-red-500 text-6xl mb-4">✗</div>
            <p className="text-red-600 font-semibold">Error al enviar feedback</p>
            <p className="text-gray-600 text-sm">Intenta de nuevo más tarde</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            {/* Mensaje original */}
            <div className="mb-4 p-3 bg-gray-50 rounded">
              <p className="text-sm text-gray-600 mb-1">Tu pregunta:</p>
              <p className="text-sm font-medium">{userInput}</p>
            </div>

            {/* Respuesta del bot */}
            <div className="mb-4 p-3 bg-blue-50 rounded">
              <p className="text-sm text-gray-600 mb-1">Respuesta:</p>
              <p className="text-sm">{botResponse}</p>
            </div>

            {/* Calificación con estrellas */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Califica esta respuesta:
              </label>
              <div className="flex space-x-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    className={`text-2xl ${
                      star <= rating ? 'text-yellow-400' : 'text-gray-300'
                    } hover:text-yellow-400 transition-colors`}
                  >
                    ★
                  </button>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {rating === 1 && 'Muy mala'}
                {rating === 2 && 'Mala'}
                {rating === 3 && 'Regular'}
                {rating === 4 && 'Buena'}
                {rating === 5 && 'Excelente'}
              </p>
            </div>

            {/* Comentario opcional */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Comentario (opcional):
              </label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="3"
                placeholder="¿Qué te gustaría que mejoremos?"
                maxLength="500"
              />
              <p className="text-xs text-gray-500 mt-1">
                {feedback.length}/500 caracteres
              </p>
            </div>

            {/* Botones */}
            <div className="flex space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
                disabled={isSubmitting}
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
                disabled={isSubmitting || rating === 0}
              >
                {isSubmitting ? 'Enviando...' : 'Enviar Feedback'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default FeedbackModal; 