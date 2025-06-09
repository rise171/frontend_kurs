import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../axios';
import './TestCard.css';

const TestCard = ({ test, onSelect, onDelete, isAdmin }) => {
  const [results, setResults] = useState([]);
  const [interpretation, setInterpretation] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Загрузка результатов теста
    const fetchResults = async () => {
      try {
        const response = await api.get(`/tests/results/history/${test.id}`);
        setResults(response.data);
      } catch (err) {
        console.error('Error fetching test results:', err);
      }
    };

    // Загрузка интерпретации
    const fetchInterpretation = async () => {
      try {
        const response = await api.get(`/interpretations/${test.interpretation_id}`);
        setInterpretation(response.data);
      } catch (err) {
        console.error('Error fetching interpretation:', err);
      }
    };

    fetchResults();
    if (test.interpretation_id) {
      fetchInterpretation();
    }
  }, [test.id, test.interpretation_id]);

  const handleStartTest = () => {
    navigate(`/tests/${test.id}/take`);
  };

  const handleEditTest = () => {
    navigate(`/tests/${test.id}/edit`);
  };

  const getLatestResult = () => {
    if (results.length === 0) return null;
    return results[0];
  };

  const latestResult = getLatestResult();

  return (
    <div className="test-card">
      <h3 className="test-title">{test.name}</h3>
      <p className="test-description">{test.description}</p>
      <div className="test-info">
        <span>Максимальный балл: {test.max_score}</span>
        {latestResult && (
          <span className="test-score">
            Последний результат: {latestResult.score}
            {interpretation && (
              <div className="interpretation">
                {latestResult.score >= interpretation.min_score && 
                 latestResult.score <= interpretation.max_score && 
                 interpretation.description}
              </div>
            )}
          </span>
        )}
      </div>
      
      <div className="test-actions">
        {isAdmin ? (
          <>
            <button onClick={handleEditTest} className="edit-button">
              Редактировать
            </button>
            <button onClick={onDelete} className="delete-button">
              Удалить
            </button>
          </>
        ) : (
          <button onClick={handleStartTest} className="start-button">
            {latestResult ? 'Пройти снова' : 'Пройти тест'}
          </button>
        )}
      </div>
    </div>
  );
};

export default TestCard; 