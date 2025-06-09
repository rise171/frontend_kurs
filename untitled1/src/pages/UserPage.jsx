import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../axios';
import Navbar from '../components/Navigation/Navbar';
import './UserPage.css';

const UserPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [moodStats, setMoodStats] = useState({
    Злость: 0,
    Тревога: 0,
    Грусть: 0,
    Радость: 0,
    Меланхолия: 0
  });
  const [currentMonth, setCurrentMonth] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const positiveQuotes = [
    "Каждый день - это новая возможность стать лучше",
    "Ваши мысли формируют вашу реальность",
    "Позитивное мышление помогает найти решение",
    "Улыбка - лучшее лекарство для души",
    "Вы сильнее, чем вы думаете"
  ];

  const [randomQuote, setRandomQuote] = useState('');

  useEffect(() => {
    // Выбираем случайную фразу при загрузке
    const randomIndex = Math.floor(Math.random() * positiveQuotes.length);
    setRandomQuote(positiveQuotes[randomIndex]);

    // Получаем текущий месяц и год
    const now = new Date();
    const monthName = now.toLocaleString('ru-RU', { month: 'long' });
    const year = now.getFullYear();
    setCurrentMonth(`${monthName} ${year}`);

    // Загружаем статистику настроений
    fetchMoodStats(now.getMonth() + 1, year);
  }, []);

  const fetchMoodStats = async (month, year) => {
    try {
      const response = await api.get('/mood/statistics', {
        params: {
          month,
          year,
          user_id: user.id
        }
      });

      // Преобразуем английские названия в русские
      const moodTranslations = {
        'anger': 'Злость',
        'anxiety': 'Тревога',
        'sadness': 'Грусть',
        'happiness': 'Радость',
        'melancholy': 'Меланхолия'
      };

      // Обрабатываем полученные данные, устанавливая 0 для отсутствующих настроений
      const stats = {
        Злость: 0,
        Тревога: 0,
        Грусть: 0,
        Радость: 0,
        Меланхолия: 0
      };

      // Преобразуем полученные данные
      Object.entries(response.data).forEach(([mood, count]) => {
        const translatedMood = moodTranslations[mood] || mood;
        if (translatedMood in stats) {
          stats[translatedMood] = count;
        }
      });

      setMoodStats(stats);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching mood statistics:', err);
      setIsLoading(false);
    }
  };

  const handleDiaryClick = () => {
    navigate('/thoughts');
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="page-container">
      <Navbar />
      <div className="content-wrapper">
        <main className="main-content">
          <div className="user-page">
            <div className="welcome-section">
              <h1>Добро пожаловать!</h1>
              <div className="quote-widget">
                <p>{randomQuote}</p>
              </div>
            </div>

            <div className="mood-statistics">
              <h2>Статистика настроений за {currentMonth}</h2>
              <div className="mood-grid">
                {Object.entries(moodStats).map(([mood, count]) => (
                  <div key={mood} className="mood-item">
                    <span className="mood-name">{mood}</span>
                    <span className="mood-count">{count}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="diary-prompt" onClick={handleDiaryClick}>
              <h3>Дневник мыслей</h3>
              <p>Запишите свои мысли и чувства, чтобы лучше понять себя</p>
              <button className="start-diary-button">Начать запись</button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default UserPage; 