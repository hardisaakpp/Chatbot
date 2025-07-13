import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('general');

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getAnalytics();
      setAnalytics(data);
    } catch (err) {
      console.error('Error cargando analytics:', err);
      setError('No se pudieron cargar las estadísticas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={loadAnalytics}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Intentar de nuevo
        </button>
      </div>
    );
  }

  if (!analytics) {
    return <div className="text-center py-8">No hay datos disponibles</div>;
  }

  const { general, popular_questions, best_rated, needs_improvement, intent_distribution, daily_trends } = analytics;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard de Analytics</h1>
        <p className="text-gray-600">Estadísticas detalladas del chatbot</p>
      </div>

      {/* Métricas generales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Usuarios Totales</p>
              <p className="text-2xl font-semibold text-gray-900">{general.total_users}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Conversaciones</p>
              <p className="text-2xl font-semibold text-gray-900">{general.total_conversations}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Mensajes</p>
              <p className="text-2xl font-semibold text-gray-900">{general.total_messages}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Preguntas</p>
              <p className="text-2xl font-semibold text-gray-900">{general.total_questions}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            {[
              { id: 'general', name: 'General', icon: '📊' },
              { id: 'popular', name: 'Populares', icon: '🔥' },
              { id: 'best', name: 'Mejor Calificadas', icon: '⭐' },
              { id: 'improve', name: 'Necesitan Mejora', icon: '⚠️' },
              { id: 'intents', name: 'Intenciones', icon: '🎯' },
              { id: 'trends', name: 'Tendencias', icon: '📈' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Contenido de las tabs */}
          {activeTab === 'general' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Usuarios Activos</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-3xl font-bold text-blue-600">{general.active_users}</p>
                  <p className="text-sm text-gray-600">de {general.total_users} usuarios totales</p>
                </div>
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Promedio de Mensajes</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-3xl font-bold text-green-600">
                    {general.total_conversations > 0 
                      ? Math.round(general.total_messages / general.total_conversations) 
                      : 0}
                  </p>
                  <p className="text-sm text-gray-600">por conversación</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'popular' && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Preguntas Más Populares</h3>
              <div className="space-y-3">
                {popular_questions.map((question, index) => (
                  <div key={question.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-lg font-bold text-gray-400 mr-3">#{index + 1}</span>
                      <div>
                        <p className="font-medium text-gray-900">{question.question}</p>
                        <p className="text-sm text-gray-600">{question.usage_count} usos</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {(question.accuracy * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-gray-500">precisión</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'best' && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Mejor Calificadas</h3>
              <div className="space-y-3">
                {best_rated.map((question, index) => (
                  <div key={question.id} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-lg font-bold text-green-400 mr-3">#{index + 1}</span>
                      <div>
                        <p className="font-medium text-gray-900">{question.question}</p>
                        <p className="text-sm text-green-600">Excelente calificación</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-green-600">
                        {(question.accuracy * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-green-500">precisión</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'improve' && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Necesitan Mejora</h3>
              <div className="space-y-3">
                {needs_improvement.map((question, index) => (
                  <div key={question.id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-lg font-bold text-red-400 mr-3">#{index + 1}</span>
                      <div>
                        <p className="font-medium text-gray-900">{question.question}</p>
                        <p className="text-sm text-red-600">Baja calificación</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-red-600">
                        {(question.accuracy * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-red-500">precisión</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'intents' && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Distribución de Intenciones</h3>
              <div className="space-y-3">
                {intent_distribution.map((intent, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-lg font-bold text-gray-400 mr-3">#{index + 1}</span>
                      <div>
                        <p className="font-medium text-gray-900 capitalize">{intent.intent}</p>
                        <p className="text-sm text-gray-600">{intent.count} mensajes</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {((intent.count / general.total_messages) * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-gray-500">del total</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'trends' && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Tendencias de los Últimos 7 Días</h3>
              <div className="space-y-3">
                {daily_trends.map((day, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-lg font-bold text-blue-400 mr-3">#{index + 1}</span>
                      <div>
                        <p className="font-medium text-gray-900">{day.date}</p>
                        <p className="text-sm text-blue-600">{day.conversations} conversaciones</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-blue-600">{day.messages}</p>
                      <p className="text-xs text-blue-500">mensajes</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Botón de actualizar */}
      <div className="text-center">
        <button
          onClick={loadAnalytics}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Actualizar Datos
        </button>
      </div>
    </div>
  );
};

export default AnalyticsDashboard; 