import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../axios';
import Navbar from '../components/Navigation/Navbar';
import './EditTestPage.css';

const EditTestPage = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [test, setTest] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [interpretation, setInterpretation] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState({
    sentence: '',
    options: ['', '', ''],
    correct_option: 0,
    score: 10
  });
  const [interpretationData, setInterpretationData] = useState({
    min_score: 0,
    max_score: 100,
    title: '',
    description: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const fetchQuestions = async () => {
    try {
      console.log('Загрузка вопросов для теста:', testId);
      const response = await api.get(`/tests/questions/${testId}/results`);
      console.log('Получены вопросы:', response.data);
      setQuestions(response.data);
      return response.data;
    } catch (err) {
      console.error('Ошибка при загрузке вопросов:', err);
      setError('Не удалось загрузить вопросы теста');
      return [];
    }
  };

  useEffect(() => {
    const fetchTestData = async () => {
      try {
        setIsLoading(true);
        // Загрузка теста
        const testResponse = await api.get(`/tests/${testId}`);
        console.log('Загружен тест:', testResponse.data);
        setTest(testResponse.data);

        // Загрузка вопросов теста
        await fetchQuestions();

        // Загрузка интерпретации, если она есть
        if (testResponse.data?.interpretation_id) {
          const interpretationResponse = await api.get(`/interpretations/${testResponse.data.interpretation_id}`);
          console.log('Загружена интерпретация:', interpretationResponse.data);
          setInterpretation(interpretationResponse.data);
          setInterpretationData({
            min_score: interpretationResponse.data.min_score,
            max_score: interpretationResponse.data.max_score,
            title: interpretationResponse.data.title,
            description: interpretationResponse.data.description
          });
        }

        setError('');
      } catch (err) {
        console.error('Ошибка при загрузке данных теста:', err);
        setError('Не удалось загрузить данные теста');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTestData();
  }, [testId]);

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    // Проверяем, что все поля заполнены
    if (!currentQuestion.sentence.trim() || currentQuestion.options.some(opt => !opt.trim())) {
      setError('Пожалуйста, заполните все поля вопроса');
      return;
    }

    try {
      console.log('Отправка вопроса:', {
        ...currentQuestion,
        test_id: parseInt(testId)
      });

      const response = await api.post(`/tests/${testId}/questions`, {
        ...currentQuestion,
        test_id: parseInt(testId)
      });

      console.log('Вопрос успешно создан:', response.data);
      
      // Обновляем список вопросов
      const updatedQuestions = await fetchQuestions();
      console.log('Обновлен список вопросов:', updatedQuestions);

      // Очищаем форму
      setCurrentQuestion({
        sentence: '',
        options: ['', '', ''],
        correct_option: 0,
        score: 10
      });

      setSuccess('Вопрос успешно добавлен');
      setError('');
    } catch (err) {
      console.error('Ошибка при добавлении вопроса:', err);
      setError(`Не удалось добавить вопрос: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleOptionChange = (index, value) => {
    setCurrentQuestion(prev => ({
      ...prev,
      options: prev.options.map((opt, i) => i === index ? value : opt)
    }));
  };

  const handleDeleteQuestion = async (questionId) => {
    if (!window.confirm('Вы уверены, что хотите удалить этот вопрос?')) return;

    try {
      await api.delete(`/tests/questions/${questionId}`);
      setQuestions(questions.filter(q => q.id !== questionId));
      setError('');
    } catch (err) {
      setError('Не удалось удалить вопрос');
      console.error('Error deleting question:', err);
    }
  };

  const handleInterpretationSubmit = async (e) => {
    e.preventDefault();
    try {
      let interpretationId = test?.interpretation_id;

      if (interpretationId) {
        // Обновляем существующую интерпретацию
        await api.put(`/interpretations/${interpretationId}`, interpretationData);
      } else {
        // Создаем новую интерпретацию
        const response = await api.post('/interpretations/', {
          ...interpretationData,
          test_id: parseInt(testId)
        });
        interpretationId = response.data.id;
      }

      setInterpretation({
        ...interpretationData,
        id: interpretationId
      });
      setError('');
    } catch (err) {
      setError('Не удалось сохранить интерпретацию');
      console.error('Error saving interpretation:', err);
    }
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;

  if (user.role !== 'admin') {
    navigate('/tests');
    return null;
  }

  return (
    <div className="page-container">
      <Navbar />
      <main className="main-content">
        <div className="edit-test-page">
          <h1>Редактирование теста</h1>
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <section className="questions-section">
            <h2>Добавить вопрос</h2>
            <form onSubmit={handleQuestionSubmit} className="question-form">
              <div className="form-group">
                <label>Текст вопроса:</label>
                <textarea
                  value={currentQuestion.sentence}
                  onChange={(e) => setCurrentQuestion(prev => ({ ...prev, sentence: e.target.value }))}
                  required
                />
              </div>

              {currentQuestion.options.map((option, index) => (
                <div key={index} className="form-group">
                  <label>Вариант {index + 1}:</label>
                  <input
                    type="text"
                    value={option}
                    onChange={(e) => handleOptionChange(index, e.target.value)}
                    required
                  />
                  <label>
                    <input
                      type="radio"
                      name="correct_option"
                      checked={currentQuestion.correct_option === index}
                      onChange={() => setCurrentQuestion(prev => ({ ...prev, correct_option: index }))}
                    />
                    Правильный ответ
                  </label>
                </div>
              ))}

              <div className="form-group">
                <label>Баллы за вопрос:</label>
                <input
                  type="number"
                  value={currentQuestion.score}
                  onChange={(e) => setCurrentQuestion(prev => ({ ...prev, score: parseInt(e.target.value) }))}
                  min="1"
                  required
                />
              </div>

              <button type="submit" className="add-button">
                Добавить вопрос
              </button>
            </form>
          </section>

          <section className="questions-list">
            <h2>Вопросы теста</h2>
            {questions.map((question, index) => (
              <div key={question.id} className="question-card">
                <div className="question-header">
                  <h3>Вопрос {index + 1}</h3>
                  <button
                    onClick={() => handleDeleteQuestion(question.id)}
                    className="delete-button"
                  >
                    Удалить
                  </button>
                </div>
                <p className="question-text">{question.sentence}</p>
                <div className="question-options">
                  {question.options.map((option, optIndex) => (
                    <p key={optIndex} className={optIndex === question.correct_option ? 'correct-option' : ''}>
                      {optIndex + 1}. {option}
                      {optIndex === question.correct_option && ' ✓'}
                    </p>
                  ))}
                </div>
                <div className="question-score">
                  Баллы: {question.score}
                </div>
              </div>
            ))}
          </section>

          <section className="interpretation-section">
            <h2>Интерпретация результатов</h2>
            <form onSubmit={handleInterpretationSubmit} className="interpretation-form">
              <div className="form-group">
                <label>Минимальный балл:</label>
                <input
                  type="number"
                  value={interpretationData.min_score}
                  onChange={(e) => setInterpretationData(prev => ({ ...prev, min_score: parseInt(e.target.value) }))}
                  required
                />
              </div>

              <div className="form-group">
                <label>Максимальный балл:</label>
                <input
                  type="number"
                  value={interpretationData.max_score}
                  onChange={(e) => setInterpretationData(prev => ({ ...prev, max_score: parseInt(e.target.value) }))}
                  required
                />
              </div>

              <div className="form-group">
                <label>Заголовок:</label>
                <input
                  type="text"
                  value={interpretationData.title}
                  onChange={(e) => setInterpretationData(prev => ({ ...prev, title: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label>Описание:</label>
                <textarea
                  value={interpretationData.description}
                  onChange={(e) => setInterpretationData(prev => ({ ...prev, description: e.target.value }))}
                  required
                />
              </div>

              <button type="submit" className="save-button">
                Сохранить интерпретацию
              </button>
            </form>
          </section>

          <div className="page-actions">
            <button onClick={() => navigate('/tests')} className="back-button">
              Вернуться к списку тестов
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default EditTestPage; 