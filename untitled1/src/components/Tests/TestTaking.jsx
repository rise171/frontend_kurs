import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { StorageService } from '../../utils/storage';
import './TestTaking.css';

const TestTaking = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const [test, setTest] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadTest();
  }, [testId]);

  const loadTest = () => {
    const foundTest = StorageService.getTestById(parseInt(testId));
    if (foundTest) {
      setTest(foundTest);
      // Инициализируем ответы
      const initialAnswers = {};
      foundTest.questions.forEach((_, index) => {
        initialAnswers[index] = null;
      });
      setAnswers(initialAnswers);
    } else {
      setError('Тест не найден');
    }
  };

  const handleAnswer = (questionIndex, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionIndex]: value
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < test.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const calculateScore = () => {
    let score = 0;
    Object.entries(answers).forEach(([index, answer]) => {
      const question = test.questions[parseInt(index)];
      if (answer === question.correctAnswer) {
        score += question.points || 1;
      }
    });
    return score;
  };

  const handleSubmit = () => {
    if (!Object.values(answers).every(answer => answer !== null)) {
      setError('Пожалуйста, ответьте на все вопросы');
      return;
    }

    setIsSubmitting(true);
    const score = calculateScore();
    const result = {
      test_id: test.id,
      user_id: 1, // Здесь должен быть ID текущего пользователя
      score,
      answers,
      max_score: test.max_score || test.questions.reduce((acc, q) => acc + (q.points || 1), 0)
    };

    try {
      StorageService.saveTestResult(result);
      navigate('/results', { state: { result } });
    } catch (err) {
      setError('Не удалось сохранить результаты теста');
      setIsSubmitting(false);
    }
  };

  if (!test) {
    return (
      <div className="test-taking">
        <div className="error-message">{error || 'Загрузка...'}</div>
      </div>
    );
  }

  const currentQuestion = test.questions[currentQuestionIndex];

  return (
    <div className="test-taking">
      <div className="test-header">
        <h2>{test.name}</h2>
        <div className="progress">
          Вопрос {currentQuestionIndex + 1} из {test.questions.length}
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="question-card">
        <h3 className="question-text">{currentQuestion.text}</h3>
        
        <div className="options-list">
          {currentQuestion.options.map((option, index) => (
            <label key={index} className="option-item">
              <input
                type="radio"
                name={`question-${currentQuestionIndex}`}
                value={index}
                checked={answers[currentQuestionIndex] === index}
                onChange={() => handleAnswer(currentQuestionIndex, index)}
              />
              <span className="option-text">{option}</span>
            </label>
          ))}
        </div>

        <div className="navigation-buttons">
          <button
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
            className="nav-button"
          >
            Назад
          </button>

          {currentQuestionIndex === test.questions.length - 1 ? (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="submit-button"
            >
              {isSubmitting ? 'Отправка...' : 'Завершить тест'}
            </button>
          ) : (
            <button
              onClick={handleNext}
              disabled={answers[currentQuestionIndex] === null}
              className="nav-button"
            >
              Далее
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default TestTaking; 