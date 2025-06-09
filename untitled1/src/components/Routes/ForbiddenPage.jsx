import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ForbiddenPage.css';

const ForbiddenPage = () => {
  const navigate = useNavigate();

  return (
    <div className="forbidden-page">
      <div className="forbidden-content">
        <h1>403</h1>
        <h2>Доступ запрещен</h2>
        <p>У вас нет прав для доступа к этой странице</p>
        <button onClick={() => navigate('/')} className="back-home">
          Вернуться на главную
        </button>
      </div>
    </div>
  );
};

export default ForbiddenPage; 