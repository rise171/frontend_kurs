import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext.jsx';
import { Navigate } from 'react-router-dom';
import Navbar from '../components/Navigation/Navbar';
import MoodModal from '../components/Mood/MoodModal';
import { api } from '../axios';
import './CalendarPage.css';

const moodLabels = {
  'anger': 'Злость',
  'anxiety': 'Тревога',
  'sadness': 'Грусть',
  'happiness': 'Радость',
  'melancholy': 'Меланхолия'
};

const CalendarPage = () => {
  const { isAuthenticated, user } = useAuth();
  const [selectedDate, setSelectedDate] = useState(null);
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [moodData, setMoodData] = useState({});
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedMood, setSelectedMood] = useState(null);

  useEffect(() => {
    if (user?.id) {
      fetchMoodData();
    } else {
      console.error('User ID not available in context:', user);
    }
  }, [currentMonth, user]);

  const fetchMoodData = async () => {
    if (!user?.id) {
      console.error("Cannot fetch mood data - user ID is missing");
      return;
    }

    try {
      const startDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1);
      const endDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0);
      
      const params = {
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        user_id: user.id
      };
      
      console.log('Fetching mood data with params:', params);

      const response = await api.get('/mood/', { params });
      console.log('Received mood data:', response.data);

      const moodMap = {};
      response.data.forEach(entry => {
        moodMap[entry.date] = {
          mood: entry.mood,
          id: entry.id
        };
      });
      setMoodData(moodMap);
    } catch (error) {
      console.error('Error fetching mood data:', error);
      if (error.response) {
        console.log('Error response data:', error.response.data);
      }
    }
  };

  const handleDateClick = async (date) => {
    setSelectedDate(date);
    const formattedDate = date.toISOString().split('T')[0];
    console.log('Selected date:', formattedDate);

    try {
      // Запрашиваем настроение для конкретной даты
      const response = await api.get(`/mood/by-date/${formattedDate}`, {
        params: {
          user_id: user.id
        }
      });
      console.log('Mood for date:', response.data);
      
      if (response.data && response.data.length > 0) {
        setSelectedMood(response.data[0].mood);
      } else {
        setSelectedMood(null);
      }
    } catch (error) {
      console.error('Error fetching mood for date:', error);
      setSelectedMood(null);
    }
  };

  const handleMoodSave = async (mood) => {
    if (!user?.id) {
      console.error('User ID is not available in context');
      return;
    }

    if (!selectedDate) {
      console.error('No date selected');
      return;
    }

    // Для создания настроения используем полный ISO формат
    const fullDateTime = new Date(selectedDate).toISOString();
    // Для поиска в локальном состоянии используем короткий формат
    const dateStr = selectedDate.toISOString().split('T')[0];

    console.log('Saving mood with data:', {
      mood,
      date: fullDateTime,
      userId: user.id
    });

    try {
      const moodEntry = moodData[dateStr];
      let response;
      
      if (moodEntry) {
        console.log('Updating existing mood:', {
          moodId: moodEntry.id,
          userId: user.id,
          mood: mood
        });

        response = await api.put(`/mood/${moodEntry.id}`, {
          "mood": mood,
          "user_id": parseInt(user.id),
          "date": fullDateTime
        });
      } else {
        const requestData = {
          "mood": mood,
          "user_id": parseInt(user.id),
          "date": fullDateTime
        };
        
        console.log('Creating new mood entry:', requestData);
        response = await api.post('/mood/', requestData);
      }
      
      console.log('API Response:', response.data);
      await fetchMoodData();
      setSelectedMood(mood);
      setIsModalOpen(false);
    } catch (error) {
      console.error('Error saving mood:', error);
      if (error.response) {
        console.log('Error status:', error.response.status);
        console.log('Error data:', error.response.data);
        if (error.response.data.detail) {
          console.log('Validation errors:', error.response.data.detail);
        }
        console.log('Request config:', error.config);
        const requestData = error.config.data ? JSON.parse(error.config.data) : null;
        console.log('Request data:', requestData);
      }
    }
  };

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const days = [];
    
    // Добавляем пустые дни в начало для выравнивания календаря
    for (let i = 0; i < firstDay.getDay(); i++) {
      days.push(null);
    }
    
    // Добавляем дни месяца
    for (let i = 1; i <= lastDay.getDate(); i++) {
      days.push(new Date(year, month, i));
    }
    
    return days;
  };

  const changeMonth = (offset) => {
    setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + offset, 1));
  };

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="page-container">
      <Navbar />
      <main className="main-content calendar-layout">
        <div className="calendar-container">
          <div className="calendar-header">
            <h2>{currentMonth.toLocaleString('ru', { month: 'long', year: 'numeric' })}</h2>
            <div className="calendar-controls">
              <button onClick={() => changeMonth(-1)}>&lt;</button>
              <button onClick={() => changeMonth(1)}>&gt;</button>
            </div>
          </div>
          
          <div className="calendar-grid">
            {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map(day => (
              <div key={day} className="calendar-day-header">{day}</div>
            ))}
            
            {getDaysInMonth(currentMonth).map((date, index) => {
              const dateStr = date ? date.toISOString().split('T')[0] : null;
              const hasMood = dateStr && moodData[dateStr];
              
              return (
                <div
                  key={index}
                  className={`calendar-day ${date ? 'has-date' : ''} ${
                    hasMood ? 'has-mood' : ''
                  } ${date && selectedDate && date.toDateString() === selectedDate.toDateString() ? 'selected' : ''}`}
                  onClick={() => date && handleDateClick(date)}
                >
                  {date && date.getDate()}
                </div>
              );
            })}
          </div>
        </div>

        <div className="mood-details">
          {selectedDate ? (
            <div className="mood-info">
              <h3>Настроение на {selectedDate.toLocaleDateString()}</h3>
              {selectedMood ? (
                <>
                  <p>Выбранное настроение: {moodLabels[selectedMood]}</p>
                  <button onClick={() => setIsModalOpen(true)} className="change-mood-button">
                    Изменить настроение
                  </button>
                </>
              ) : (
                <>
                  <p>Настроение не выбрано</p>
                  <button onClick={() => setIsModalOpen(true)} className="add-mood-button">
                    Добавить настроение
                  </button>
                </>
              )}
            </div>
          ) : (
            <p className="select-date-prompt">Выберите дату для просмотра или добавления настроения</p>
          )}
        </div>
      </main>

      <MoodModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleMoodSave}
        selectedDate={selectedDate}
        currentMood={selectedMood}
      />
    </div>
  );
};

export default CalendarPage; 