import React from 'react';
import './MoodModal.css';

const moodOptions = [
  { value: 'anger', label: 'Злость' },
  { value: 'anxiety', label: 'Тревога' },
  { value: 'sadness', label: 'Грусть' },
  { value: 'happiness', label: 'Радость' },
  { value: 'melancholy', label: 'Меланхолия' }
];

const MoodModal = ({ isOpen, onClose, onSave, selectedDate, currentMood }) => {
  const [selectedMood, setSelectedMood] = React.useState(currentMood || '');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(selectedMood);
    onClose();
  };

  return (
    <div className="mood-modal-overlay">
      <div className="mood-modal">
        <h3>Выберите настроение</h3>
        <p>Дата: {selectedDate?.toLocaleDateString()}</p>
        
        <form onSubmit={handleSubmit}>
          <div className="mood-options">
            {moodOptions.map((mood) => (
              <label key={mood.value} className="mood-option">
                <input
                  type="radio"
                  name="mood"
                  value={mood.value}
                  checked={selectedMood === mood.value}
                  onChange={(e) => setSelectedMood(e.target.value)}
                />
                <span>{mood.label}</span>
              </label>
            ))}
          </div>
          
          <div className="modal-buttons">
            <button type="button" onClick={onClose} className="cancel-button">
              Отмена
            </button>
            <button type="submit" className="save-button" disabled={!selectedMood}>
              Сохранить
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MoodModal; 