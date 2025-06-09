import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../axios';
import Navbar from '../components/Navigation/Navbar';
import './FeedbackPage.css';

const FeedbackPage = () => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [responses, setResponses] = useState({});
  const { user } = useAuth();

  // Статусы на русском языке
  const statusTranslations = {
    'pending': 'Ожидает ответа',
    'resolved': 'Ответ получен'
  };

  // Форматирование даты
  const formatDate = (dateString) => {
    if (!dateString) return '';
    
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return '';
      }
      return date.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (err) {
      console.error('Error formatting date:', err);
      return '';
    }
  };

  // Загрузка фидбеков
  const fetchFeedbacks = async () => {
    try {
      const endpoint = user.role === 'admin' ? '/feedback/admin' : '/feedback/my';
      const response = await api.get(endpoint, {
        params: { user_id: user.id }
      });
      setFeedbacks(response.data);
      setError('');
    } catch (err) {
      setError('Не удалось загрузить сообщения');
      console.error('Error fetching feedbacks:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedbacks();
  }, [user.id]);

  // Отправка нового сообщения
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      await api.post('/feedback/', {
        message: newMessage,
        user_id: parseInt(user.id),
        user_role: "user"
      });
      setNewMessage('');
      setSuccess('Сообщение успешно отправлено');
      fetchFeedbacks();
      setError('');
    } catch (err) {
      setError('Не удалось отправить сообщение');
      console.error('Error sending feedback:', err);
    }
  };

  // Обработка изменения текста ответа
  const handleResponseChange = (feedbackId, value) => {
    setResponses(prev => ({
      ...prev,
      [feedbackId]: value
    }));
  };

  // Ответ на сообщение (только для админа)
  const handleRespond = async (feedbackId) => {
    const response = responses[feedbackId];
    if (!response?.trim()) {
      setError('Введите текст ответа');
      return;
    }

    try {
      await api.put(`/feedback/${feedbackId}`, {
        id: feedbackId,
        status: 'resolved',
        response: response
      });
      setSuccess('Ответ успешно сохранен');
      setResponses(prev => ({
        ...prev,
        [feedbackId]: ''
      }));
      fetchFeedbacks();
      setError('');
    } catch (err) {
      setError('Не удалось отправить ответ');
      console.error('Error responding to feedback:', err);
    }
  };

  // Удаление фидбека (только для админа)
  const handleDelete = async (feedbackId) => {
    if (!window.confirm('Вы уверены, что хотите удалить это сообщение?')) return;

    try {
      await api.delete(`/feedback/${feedbackId}`);
      setSuccess('Сообщение успешно удалено');
      fetchFeedbacks();
      setError('');
    } catch (err) {
      setError('Не удалось удалить сообщение');
      console.error('Error deleting feedback:', err);
    }
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="page-container">
      <Navbar />
      <div className="content-wrapper">
        <main className="main-content">
          <div className="feedback-page">
            <h1>Обратная связь</h1>
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}

            {user.role !== 'admin' && (
              <form onSubmit={handleSubmit} className="feedback-form">
                <textarea
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Введите ваше сообщение..."
                  required
                />
                <button type="submit">Отправить</button>
              </form>
            )}

            <div className="feedbacks-list">
              {feedbacks.map((feedback, index) => (
                <div key={feedback.id} className="feedback-item">
                  <div className="feedback-header">
                    <span className="feedback-number">
                      Сообщение #{index + 1}
                    </span>
                    <span className={`feedback-status status-${feedback.status}`}>
                      {statusTranslations[feedback.status] || 'Ожидает ответа'}
                    </span>
                    <span className="feedback-date">
                      {formatDate(feedback.created_at)}
                    </span>
                  </div>
                  
                  <div className="feedback-message">{feedback.message}</div>
                  
                  {feedback.response && (
                    <div className="feedback-response">
                      <strong>Ответ:</strong> {feedback.response}
                    </div>
                  )}

                  {user.role === 'admin' && !feedback.response && (
                    <div className="admin-controls">
                      <div className="response-input-group">
                        <textarea
                          value={responses[feedback.id] || ''}
                          onChange={(e) => handleResponseChange(feedback.id, e.target.value)}
                          placeholder="Введите ответ на сообщение..."
                        />
                        {responses[feedback.id]?.trim() && (
                          <button 
                            onClick={() => handleRespond(feedback.id)}
                            className="save-button"
                          >
                            Сохранить ответ
                          </button>
                        )}
                      </div>

                      <button 
                        onClick={() => handleDelete(feedback.id)}
                        className="delete-button"
                      >
                        Удалить
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default FeedbackPage; 