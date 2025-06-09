import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { StorageService } from '../../utils/storage';
import './TestResults.css';

const TestResults = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [test, setTest] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (location.state?.result) {
      setResult(location.state.result);
      loadTest(location.state.result.test_id);
    } else {
      setError('Результаты не найдены');
    }
  }, [location]);

  const loadTest = (testId) => {
    const foundTest = StorageService.getTestById(testId);
    if (foundTest) {
      setTest(foundTest);
    } else {
      setError('Тест не найден');
    }
  };

  const calculatePercentage = () => {
    if (!result || !test) return 0;
    return Math.round((result.score / result.max_score) * 100);
  };

  const getResultMessage = () => {
    const percentage = calculatePercentage();
    if (percentage >= 90) return 'Отличный результат!';
    if (percentage >= 70) return 'Хороший результат!';
    if (percentage >= 50) return 'Удовлетворительный результат';
    return 'Есть над чем поработать';
  };

  const handleRetakeTest = () => {
    navigate(`/test/${test.id}`);
  };

  const handleBackToTests = () => {
    navigate('/tests');
  };

  if (!result || !test) {
    return (
      <div className="test-results">
        <div className="error-message">{error || 'Загрузка...'}</div>
      </div>
    );
  }

  return (
    <div className="test-results">
      <div className="results-header">
        <h2>{test.name}</h2>
        <div className="score-summary">
          <div className="score-circle">
            <div className="score-percentage">{calculatePercentage()}%</div>
            <div className="score-label">Результат</div>
          </div>
          <div className="score-details">
            <p className="score-message">{getResultMessage()}</p>
            <p className="score-points">
              Набрано баллов: {result.score} из {result.max_score}
            </p>
          </div>
        </div>
      </div>

      <div className="answers-review">
        <h3>Обзор ответов</h3>
        {test.questions.map((question, index) => {
          const userAnswer = result.answers[index];
          const isCorrect = userAnswer === question.correctAnswer;

          return (
            <div
              key={index}
              className={`answer-item ${isCorrect ? 'correct' : 'incorrect'}`}
            >
              <div className="question-info">
                <span className="question-number">Вопрос {index + 1}</span>
                <p className="question-text">{question.text}</p>
              </div>

              <div className="answer-details">
                <div className="user-answer">
                  <strong>Ваш ответ:</strong>
                  <span>{question.options[userAnswer]}</span>
                </div>
                {!isCorrect && (
                  <div className="correct-answer">
                    <strong>Правильный ответ:</strong>
                    <span>{question.options[question.correctAnswer]}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="results-actions">
        <button onClick={handleRetakeTest} className="retake-button">
          Пройти тест заново
        </button>
        <button onClick={handleBackToTests} className="back-button">
          К списку тестов
        </button>
      </div>
    </div>
  );
};

export default TestResults; 