import React, { useState, useEffect } from 'react';
import './ThoughtModal.css';

const ThoughtModal = ({ isOpen, onClose, onSave, currentThought }) => {
  const [thoughtData, setThoughtData] = useState({
    situation: '',
    thought: '',
    emotion: '',
    behavior: ''
  });

  useEffect(() => {
    if (currentThought) {
      setThoughtData(currentThought);
    } else {
      setThoughtData({
        situation: '',
        thought: '',
        emotion: '',
        behavior: ''
      });
    }
  }, [currentThought]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(thoughtData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setThoughtData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{currentThought ? 'Редактировать запись' : 'Новая запись'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="situation">Ситуация</label>
            <textarea
              id="situation"
              name="situation"
              value={thoughtData.situation}
              onChange={handleChange}
              placeholder="Опишите ситуацию..."
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="thought">Мысли</label>
            <textarea
              id="thought"
              name="thought"
              value={thoughtData.thought}
              onChange={handleChange}
              placeholder="Какие мысли возникли..."
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="emotion">Эмоции</label>
            <textarea
              id="emotion"
              name="emotion"
              value={thoughtData.emotion}
              onChange={handleChange}
              placeholder="Какие эмоции вы испытывали..."
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="behavior">Поведение</label>
            <textarea
              id="behavior"
              name="behavior"
              value={thoughtData.behavior}
              onChange={handleChange}
              placeholder="Как вы себя вели..."
              required
            />
          </div>

          <div className="modal-buttons">
            <button type="submit" className="save-button">
              {currentThought ? 'Сохранить' : 'Создать'}
            </button>
            <button type="button" onClick={onClose} className="cancel-button">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ThoughtModal; 