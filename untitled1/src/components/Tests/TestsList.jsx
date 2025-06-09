import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { StorageService } from '../../utils/storage';
import { useAuth } from '../../context/AuthContext';
import './TestsList.css';

const TestsList = () => {
  const [tests, setTests] = useState([]);
  const [userResults, setUserResults] = useState({});
  const navigate = useNavigate();
  const { user, isAdmin } = useAuth();

  useEffect(() => {
    loadTests();
    if (user) {
      loadUserResults();
    }
  }, [user]);

  const loadTests = () => {
    const allTests = StorageService.getAllTests();
    setTests(allTests);
  };

  const loadUserResults = () => {
    const results = StorageService.getTestResultsByUserId(user.id);
    const resultsByTest = results.reduce((acc, result) => {
      if (!acc[result.test_id] || new Date(result.completed_at) > new Date(acc[result.test_id].completed_at)) {
        acc[result.test_id] = result;
      }
      return acc;
    }, {});
    setUserResults(resultsByTest);
  };

  const handleStartTest = (testId) => {
    navigate(`/test/${testId}`);
  };

  const handleViewResults = (testId) => {
    navigate('/results', { 
      state: { result: userResults[testId] }
    });
  };

  const handleManageTests = () => {
    navigate('/admin/tests');
  };

  return (
    <div className="tests-list-container">
      <div className="tests-header">
        <h2>Доступные тесты</h2>
        {isAdmin && (
          <button onClick={handleManageTests} className="manage-tests-button">
            Управление тестами
          </button>
        )}
      </div>

      <div className="tests-grid">
        {tests.map(test => {
          const userResult = userResults[test.id];
          const hasCompleted = !!userResult;

          return (
            <div key={test.id} className="test-item">
              <div className="test-content">
                <h3>{test.name}</h3>
                <p>{test.description}</p>
                {hasCompleted && (
                  <div className="test-result-preview">
                    <span className="result-label">Ваш результат:</span>
                    <span className="result-score">
                      {Math.round((userResult.score / userResult.max_score) * 100)}%
                    </span>
                  </div>
                )}
              </div>
              
              <div className="test-actions">
                <button
                  onClick={() => handleStartTest(test.id)}
                  className="start-test-button"
                >
                  {hasCompleted ? 'Пройти заново' : 'Начать тест'}
                </button>
                {hasCompleted && (
                  <button
                    onClick={() => handleViewResults(test.id)}
                    className="view-results-button"
                  >
                    Посмотреть результаты
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {tests.length === 0 && (
        <div className="no-tests">
          <p>Нет доступных тестов</p>
          {isAdmin && (
            <button onClick={handleManageTests} className="create-first-test">
              Создать первый тест
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default TestsList; 