import React, { useState, useEffect } from 'react';
import { StorageService } from '../../utils/storage';
import './TestManager.css';

const TestManager = () => {
  const [tests, setTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    questions: [],
    interpretations: []
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadTests();
  }, []);

  const loadTests = () => {
    const allTests = StorageService.getAllTests();
    setTests(allTests);
  };

  const handleCreateTest = () => {
    setSelectedTest(null);
    setIsEditing(true);
    setFormData({
      name: '',
      description: '',
      questions: [],
      interpretations: []
    });
  };

  const handleEditTest = (test) => {
    setSelectedTest(test);
    setIsEditing(true);
    setFormData({
      name: test.name,
      description: test.description,
      questions: test.questions || [],
      interpretations: test.interpretations || []
    });
  };

  const handleDeleteTest = (testId) => {
    if (window.confirm('Вы уверены, что хотите удалить этот тест?')) {
      try {
        StorageService.deleteTest(testId);
        loadTests();
        setSuccess('Тест успешно удален');
        setError('');
      } catch (err) {
        setError('Не удалось удалить тест');
        console.error('Error deleting test:', err);
      }
    }
  };

  const handleAddQuestion = () => {
    setFormData(prev => ({
      ...prev,
      questions: [
        ...prev.questions,
        {
          text: '',
          options: ['', ''],  // Начинаем с 2 вариантов ответа
          correctAnswer: 0,
          points: 1
        }
      ]
    }));
  };

  const handleAddOption = (questionIndex) => {
    setFormData(prev => ({
      ...prev,
      questions: prev.questions.map((q, i) => 
        i === questionIndex ? {
          ...q,
          options: [...q.options, '']
        } : q
      )
    }));
  };

  const handleDeleteOption = (questionIndex, optionIndex) => {
    setFormData(prev => ({
      ...prev,
      questions: prev.questions.map((q, i) => {
        if (i === questionIndex) {
          const newOptions = q.options.filter((_, j) => j !== optionIndex);
          return {
            ...q,
            options: newOptions,
            correctAnswer: q.correctAnswer >= optionIndex ? 
              (q.correctAnswer > 0 ? q.correctAnswer - 1 : 0) : 
              q.correctAnswer
          };
        }
        return q;
      })
    }));
  };

  const handleQuestionChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      questions: prev.questions.map((q, i) => 
        i === index ? { ...q, [field]: value } : q
      )
    }));
  };

  const handleOptionChange = (questionIndex, optionIndex, value) => {
    setFormData(prev => ({
      ...prev,
      questions: prev.questions.map((q, i) => 
        i === questionIndex ? {
          ...q,
          options: q.options.map((opt, j) => j === optionIndex ? value : opt)
        } : q
      )
    }));
  };

  const handleDeleteQuestion = (index) => {
    setFormData(prev => ({
      ...prev,
      questions: prev.questions.filter((_, i) => i !== index)
    }));
  };

  const handleAddInterpretation = () => {
    setFormData(prev => ({
      ...prev,
      interpretations: [
        ...prev.interpretations,
        {
          minScore: 0,
          maxScore: 0,
          description: ''
        }
      ]
    }));
  };

  const handleInterpretationChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      interpretations: prev.interpretations.map((interp, i) => 
        i === index ? { ...interp, [field]: value } : interp
      )
    }));
  };

  const handleDeleteInterpretation = (index) => {
    setFormData(prev => ({
      ...prev,
      interpretations: prev.interpretations.filter((_, i) => i !== index)
    }));
  };

  const handleSaveTest = (e) => {
    e.preventDefault();

    // Валидация
    if (!formData.name.trim() || !formData.description.trim()) {
      setError('Заполните название и описание теста');
      return;
    }

    if (formData.questions.length === 0) {
      setError('Добавьте хотя бы один вопрос');
      return;
    }

    // Проверка вопросов
    const invalidQuestions = formData.questions.some(q => 
      !q.text.trim() || q.options.some(opt => !opt.trim())
    );

    if (invalidQuestions) {
      setError('Заполните все поля вопросов и варианты ответов');
      return;
    }

    try {
      if (selectedTest) {
        StorageService.updateTest(selectedTest.id, formData);
      } else {
        StorageService.saveTest(formData);
      }
      
      loadTests();
      setIsEditing(false);
      setSelectedTest(null);
      setSuccess('Тест успешно сохранен');
      setError('');
    } catch (err) {
      setError('Не удалось сохранить тест');
      console.error('Error saving test:', err);
    }
  };

  const handleExport = () => {
    try {
      StorageService.exportToFile();
      setSuccess('Данные успешно экспортированы');
      setError('');
    } catch (err) {
      setError('Не удалось экспортировать данные');
      console.error('Error exporting data:', err);
    }
  };

  const handleImport = (e) => {
    const file = e.target.files[0];
    if (file) {
      StorageService.importFromFile(file)
        .then(() => {
          loadTests();
          setSuccess('Данные успешно импортированы');
          setError('');
        })
        .catch((err) => {
          setError('Не удалось импортировать данные');
          console.error('Error importing data:', err);
        });
    }
  };

  return (
    <div className="test-manager">
      <div className="test-manager-header">
        <h2>Управление тестами</h2>
        <div className="test-manager-actions">
          <button onClick={handleCreateTest} className="create-button">
            Создать тест
          </button>
          <input
            type="file"
            accept=".json"
            onChange={handleImport}
            id="import-file"
            style={{ display: 'none' }}
          />
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      {isEditing ? (
        <form onSubmit={handleSaveTest} className="test-form">
          <div className="form-group">
            <label htmlFor="name">Название теста</label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Описание теста</label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required
            />
          </div>

          <div className="questions-section">
            <h3>Вопросы</h3>
            {formData.questions.map((question, qIndex) => (
              <div key={qIndex} className="question-item">
                <div className="question-header">
                  <h4>Вопрос {qIndex + 1}</h4>
                  <button
                    type="button"
                    onClick={() => handleDeleteQuestion(qIndex)}
                    className="delete-question-button"
                  >
                    Удалить вопрос
                  </button>
                </div>

                <div className="form-group">
                  <label>Текст вопроса</label>
                  <textarea
                    value={question.text}
                    onChange={(e) => handleQuestionChange(qIndex, 'text', e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Баллы за правильный ответ</label>
                  <input
                    type="number"
                    min="1"
                    value={question.points}
                    onChange={(e) => handleQuestionChange(qIndex, 'points', parseInt(e.target.value))}
                    required
                  />
                </div>

                <div className="options-group">
                  <div className="options-header">
                    <h5>Варианты ответов</h5>
                    <button
                      type="button"
                      onClick={() => handleAddOption(qIndex)}
                      className="add-option-button"
                    >
                      Добавить вариант
                    </button>
                  </div>
                  {question.options.map((option, oIndex) => (
                    <div key={oIndex} className="option-item">
                      <input
                        type="text"
                        value={option}
                        onChange={(e) => handleOptionChange(qIndex, oIndex, e.target.value)}
                        placeholder={`Вариант ${oIndex + 1}`}
                        required
                      />
                      <input
                        type="radio"
                        name={`correct-${qIndex}`}
                        checked={question.correctAnswer === oIndex}
                        onChange={() => handleQuestionChange(qIndex, 'correctAnswer', oIndex)}
                      />
                      <label>Правильный ответ</label>
                      {question.options.length > 2 && (
                        <button
                          type="button"
                          onClick={() => handleDeleteOption(qIndex, oIndex)}
                          className="delete-option-button"
                        >
                          Удалить
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={handleAddQuestion}
              className="add-question-button"
            >
              Добавить вопрос
            </button>
          </div>

          <div className="interpretations-section">
            <h3>Интерпретации результатов</h3>
            {formData.interpretations.map((interpretation, iIndex) => (
              <div key={iIndex} className="interpretation-item">
                <div className="interpretation-header">
                  <h4>Интерпретация {iIndex + 1}</h4>
                  <button
                    type="button"
                    onClick={() => handleDeleteInterpretation(iIndex)}
                    className="delete-interpretation-button"
                  >
                    Удалить интерпретацию
                  </button>
                </div>

                <div className="score-range">
                  <div className="form-group">
                    <label>Минимальный балл</label>
                    <input
                      type="number"
                      value={interpretation.minScore}
                      onChange={(e) => handleInterpretationChange(iIndex, 'minScore', parseInt(e.target.value))}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Максимальный балл</label>
                    <input
                      type="number"
                      value={interpretation.maxScore}
                      onChange={(e) => handleInterpretationChange(iIndex, 'maxScore', parseInt(e.target.value))}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Описание результата</label>
                  <textarea
                    value={interpretation.description}
                    onChange={(e) => handleInterpretationChange(iIndex, 'description', e.target.value)}
                    required
                  />
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={handleAddInterpretation}
              className="add-interpretation-button"
            >
              Добавить интерпретацию
            </button>
          </div>

          <div className="form-actions">
            <button type="submit" className="save-button">
              {selectedTest ? 'Сохранить изменения' : 'Создать тест'}
            </button>
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="cancel-button"
            >
              Отмена
            </button>
          </div>
        </form>
      ) : (
        <div className="tests-list">
          {tests.map(test => (
            <div key={test.id} className="test-card">
              <div className="test-info">
                <h3>{test.name}</h3>
                <p>{test.description}</p>
                <div className="test-stats">
                  <span>Вопросов: {test.questions?.length || 0}</span>
                  <span>Интерпретаций: {test.interpretations?.length || 0}</span>
                </div>
                <span className="test-date">
                  Создан: {new Date(test.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="test-actions">
                <button
                  onClick={() => handleEditTest(test)}
                  className="edit-button"
                >
                  Редактировать
                </button>
                <button
                  onClick={() => handleDeleteTest(test.id)}
                  className="delete-button"
                >
                  Удалить
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TestManager; 