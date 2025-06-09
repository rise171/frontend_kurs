import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../axios';
import Navbar from '../components/Navigation/Navbar';
import TestCard from '../components/Tests/TestCard';
import CreateTestModal from '../components/Tests/CreateTestModal';
import './TestsPage.css';

const TestsPage = () => {
  const [tests, setTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useAuth();

  // Загрузка списка тестов
  const fetchTests = async () => {
    try {
      const response = await api.get('/tests/');
      setTests(response.data);
      setError('');
    } catch (err) {
      setError('Не удалось загрузить тесты');
      console.error('Error fetching tests:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTests();
  }, []);

  // Удаление теста (только для админа)
  const handleDeleteTest = async (testId) => {
    if (!window.confirm('Вы уверены, что хотите удалить этот тест?')) return;

    try {
      await api.delete(`/tests/${testId}`);
      fetchTests();
      setSelectedTest(null);
      setError('');
    } catch (err) {
      setError('Не удалось удалить тест');
      console.error('Error deleting test:', err);
    }
  };

  // Создание нового теста (только для админа)
  const handleCreateTest = async (testData) => {
    try {
      const response = await api.post('/tests/', testData);
      fetchTests();
      setIsCreateModalOpen(false);
      setError('');
      return response.data.id; // Возвращаем ID созданного теста
    } catch (err) {
      setError('Не удалось создать тест');
      console.error('Error creating test:', err);
      return null;
    }
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="page-container">
      <Navbar />
      <main className="main-content">
        <div className="tests-page">
          <div className="tests-header">
            <h1>Тесты</h1>
            {user.role === 'admin' && (
              <button 
                className="create-test-button"
                onClick={() => setIsCreateModalOpen(true)}
              >
                Создать тест
              </button>
            )}
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="tests-grid">
            {tests.map(test => (
              <TestCard
                key={test.id}
                test={test}
                onSelect={() => setSelectedTest(test)}
                onDelete={user.role === 'admin' ? () => handleDeleteTest(test.id) : undefined}
                isAdmin={user.role === 'admin'}
              />
            ))}
          </div>

          {isCreateModalOpen && (
            <CreateTestModal
              onClose={() => setIsCreateModalOpen(false)}
              onCreate={handleCreateTest}
            />
          )}
        </div>
      </main>
    </div>
  );
};

export default TestsPage; 