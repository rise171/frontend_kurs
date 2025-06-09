import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext.jsx';
import { Navigate } from 'react-router-dom';
import Navbar from '../components/Navigation/Navbar';
import ThoughtModal from '../components/Thoughts/ThoughtModal';
import { api } from '../axios';
import './ThoughtsPage.css';

const ThoughtsPage = () => {
  const { isAuthenticated, user } = useAuth();
  const [thoughts, setThoughts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedThought, setSelectedThought] = useState(null);
  const [viewingThought, setViewingThought] = useState(null);

  useEffect(() => {
    fetchThoughts();
  }, [user]);

  const fetchThoughts = async () => {
    try {
      const response = await api.get('/thoughts/', {
        params: { user_id: user.id }
      });
      setThoughts(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching thoughts:', err);
      setError('Не удалось загрузить записи');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateThought = () => {
    setSelectedThought(null);
    setIsModalOpen(true);
  };

  const handleEditThought = (thought) => {
    setSelectedThought(thought);
    setIsModalOpen(true);
    setViewingThought(null);
  };

  const handleViewThought = (thought) => {
    setViewingThought(thought);
    setSelectedThought(null);
  };

  const handleDeleteThought = async (thoughtId) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту запись?')) {
      return;
    }

    try {
      await api.delete(`/thoughts/${thoughtId}`, {
        params: { user_id: user.id }
      });
      await fetchThoughts();
      setViewingThought(null);
    } catch (err) {
      console.error('Error deleting thought:', err);
      setError('Не удалось удалить запись');
    }
  };

  const handleSaveThought = async (thoughtData) => {
    try {
      if (selectedThought) {
        const apiData = {
          situation: thoughtData.situation,
          thought: thoughtData.thought,
          emotion: thoughtData.emotion,
          behavior: thoughtData.behavior
        };

        console.log('Отправляем данные на сервер (обновление):', apiData);
        
        await api.put(`/thoughts/${selectedThought.id}`, apiData, {
          params: { user_id: user.id }
        });
      } else {
        const apiData = {
          user_id: parseInt(user.id),
          situation: thoughtData.situation,
          thought: thoughtData.thought,
          emotion: thoughtData.emotion,
          behavior: thoughtData.behavior,
          date: new Date().toISOString()
        };

        console.log('Отправляем данные на сервер (создание):', apiData);
        
        await api.post('/thoughts/', apiData);
      }

      await fetchThoughts();
      setIsModalOpen(false);
      setSelectedThought(null);
      setError(null);
    } catch (err) {
      console.error('Ошибка при сохранении заметки:', err);
      if (err.response) {
        console.error('Детали ошибки:', err.response.data);
      }
      setError('Не удалось сохранить запись. Пожалуйста, проверьте введенные данные.');
    }
  };

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="page-container">
      <Navbar />
      <main className="thoughts-content">
        <div className="thoughts-header">
          <h2>Дневник мыслей</h2>
          {thoughts.length > 0 && (
            <button onClick={handleCreateThought} className="create-button">
              Создать запись
            </button>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        {isLoading ? (
          <div className="loading">Загрузка...</div>
        ) : (
          <div className="thoughts-layout">
            <div className="thoughts-list">
              {thoughts.length === 0 ? (
                <div className="no-thoughts">
                  <p>У вас пока нет записей</p>
                  <button onClick={handleCreateThought} className="create-button">
                    Создать первую запись
                  </button>
                </div>
              ) : (
                thoughts.map(thought => (
                  <div
                    key={thought.id}
                    className={`thought-item ${viewingThought?.id === thought.id ? 'selected' : ''}`}
                    onClick={() => handleViewThought(thought)}
                  >
                    <div className="thought-preview">
                      <div className="thought-date">
                        {new Date(thought.date).toLocaleDateString()}
                      </div>
                      <div className="thought-situation">{thought.situation.substring(0, 100)}...</div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {viewingThought && (
              <div className="thought-details">
                <h3>Запись от {new Date(viewingThought.date).toLocaleDateString()}</h3>
                <div className="thought-section">
                  <h4>Ситуация</h4>
                  <p>{viewingThought.situation}</p>
                </div>
                <div className="thought-section">
                  <h4>Мысли</h4>
                  <p>{viewingThought.thought}</p>
                </div>
                <div className="thought-section">
                  <h4>Эмоции</h4>
                  <p>{viewingThought.emotion}</p>
                </div>
                <div className="thought-section">
                  <h4>Поведение</h4>
                  <p>{viewingThought.behavior}</p>
                </div>
                <div className="thought-actions">
                  <button
                    onClick={() => handleEditThought(viewingThought)}
                    className="edit-button"
                  >
                    Редактировать
                  </button>
                  <button
                    onClick={() => handleDeleteThought(viewingThought.id)}
                    className="delete-button"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        <ThoughtModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveThought}
          currentThought={selectedThought}
        />
      </main>
    </div>
  );
};

export default ThoughtsPage; 