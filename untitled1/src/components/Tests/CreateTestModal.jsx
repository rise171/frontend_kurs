import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreateTestModal.css';

const CreateTestModal = ({ onClose, onCreate }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    max_score: 100
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.description.trim()) {
      setError('Пожалуйста, заполните название и описание теста.');
      return;
    }

    try {
      const testId = await onCreate({
        ...formData,
        max_score: parseInt(formData.max_score)
      });
      
      if (testId) {
        navigate(`/tests/${testId}/edit`);
      }
    } catch (err) {
      setError('Не удалось создать тест');
      console.error('Error creating test:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Создание нового теста</h2>
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Название теста</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Описание теста</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="max_score">Максимальный балл</label>
            <input
              type="number"
              id="max_score"
              name="max_score"
              min="1"
              value={formData.max_score}
              onChange={handleChange}
              required
            />
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="cancel-button">
              Отмена
            </button>
            <button type="submit" className="create-button">
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateTestModal; 