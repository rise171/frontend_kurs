import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../axios';
import Navbar from '../components/Navigation/Navbar';
import './TakeTestPage.css';

const TakeTestPage = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [test, setTest] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTestData = async () => {
      try {
        // Загрузка вопросов теста
        const questionsResponse = await api.get(`/tests/questions/${testId}/results`);
        setQuestions(questionsResponse.data);
        setAnswers(
          questionsResponse.data.reduce((acc, q) => ({
            ...acc,
            [q.id]: { additionalProp1: '', additionalProp2: '', additionalProp3: '' }
          }), {})
        );
        setError('');
      } catch (err) {
        setError('Не удалось загрузить тест');
        console.error('Error fetching test data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTestData();
  }, [testId]);

  const handleAnswerChange = (questionId, prop, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [prop]: value
      }
    }));
  };

  const handleSubmit = async () => {
    try {
      // Проверяем, что все вопросы отвечены
      const isComplete = Object.values(answers).every(answer => 
        answer.additionalProp1.trim() && 
        answer.additionalProp2.trim() && 
        answer.additionalProp3.trim()
      );

      if (!isComplete) {
        setError('Пожалуйста, ответьте на все вопросы');
        return;
      }

      // Отправляем результаты
      await api.post(`/tests/results/`, {
        test_id: parseInt(testId),
        user_id: parseInt(user.id),
        answers: answers
      });

      // Возвращаемся к списку тестов
      navigate('/tests');
    } catch (err) {
      setError('Не удалось сохранить результаты');
      console.error('Error submitting test:', err);
    }
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="page-container">
      <Navbar />
      <main className="main-content">
        <div className="take-test-page">
          <h1>Прохождение теста</h1>
          {error && <div className="error-message">{error}</div>}

          <div className="questions-list">
            {questions.map((question, index) => (
              <div key={question.id} className="question-card">
                <h3>Вопрос {index + 1}</h3>
                <p className="question-text">{question.text}</p>
                
                <div className="answer-inputs">
                  <div className="answer-group">
                    <label>Ответ 1:</label>
                    <input
                      type="text"
                      value={answers[question.id]?.additionalProp1 || ''}
                      onChange={(e) => handleAnswerChange(question.id, 'additionalProp1', e.target.value)}
                      placeholder="Введите ответ"
                    />
                  </div>

                  <div className="answer-group">
                    <label>Ответ 2:</label>
                    <input
                      type="text"
                      value={answers[question.id]?.additionalProp2 || ''}
                      onChange={(e) => handleAnswerChange(question.id, 'additionalProp2', e.target.value)}
                      placeholder="Введите ответ"
                    />
                  </div>

                  <div className="answer-group">
                    <label>Ответ 3:</label>
                    <input
                      type="text"
                      value={answers[question.id]?.additionalProp3 || ''}
                      onChange={(e) => handleAnswerChange(question.id, 'additionalProp3', e.target.value)}
                      placeholder="Введите ответ"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="test-actions">
            <button onClick={() => navigate('/tests')} className="cancel-button">
              Отмена
            </button>
            <button onClick={handleSubmit} className="submit-button">
              Завершить тест
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default TakeTestPage; 