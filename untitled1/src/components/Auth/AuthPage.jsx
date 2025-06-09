import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext.jsx';
import { api } from '../../axios';
import { useNavigate } from 'react-router-dom';
import './AuthPage.css';

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    login: '',
    password: '',
  });
  const [formErrors, setFormErrors] = useState({
    username: '',
    login: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login: authLogin } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    const errors = {
      username: '',
      login: '',
      password: '',
    };
    let isValid = true;

    if (!isLogin && !formData.username.trim()) {
      errors.username = 'Имя пользователя обязательно';
      isValid = false;
    } else if (!isLogin && formData.username.length < 2) {
      errors.username = 'Имя пользователя должно быть не менее 2 символов';
      isValid = false;
    }

    if (!formData.login.trim()) {
      errors.login = 'Логин обязателен';
      isValid = false;
    } else if (formData.login.length < 3) {
      errors.login = 'Логин должен быть не менее 3 символов';
      isValid = false;
    }

    if (!formData.password) {
      errors.password = 'Пароль обязателен';
      isValid = false;
    } else if (formData.password.length < 6) {
      errors.password = 'Пароль должен быть не менее 6 символов';
      isValid = false;
    }

    setFormErrors(errors);
    return isValid;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Очищаем ошибку поля при вводе
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const endpoint = isLogin ? '/user/login' : '/user/register';
      const requestData = isLogin ? {
        login: formData.login,
        password: formData.password
      } : {
        username: formData.username,
        login: formData.login,
        password: formData.password,
        role: formData.login === 'admin' ? 'admin' : 'user'
      };

      console.log("Отправляем запрос авторизации:", requestData);
      const response = await api.post(endpoint, requestData);
      console.log("Ответ сервера:", response.data);

      if (isLogin) {
        if (response.data) {
          const userData = {
            id: response.data.user?.id || response.data.id || response.data.user_id,
            login: formData.login,
            role: response.data.role || (formData.login === 'admin' ? 'admin' : 'user')
          };

          if (!userData.id && response.data.user) {
            console.log("Ищем ID в объекте пользователя:", response.data.user);
            userData.id = response.data.user.id || response.data.user.user_id;
          }

          if (!userData.id) {
            console.error("Не удалось найти ID пользователя в ответе:", response.data);
            throw new Error("Не удалось получить ID пользователя");
          }
          
          const token = response.data.access_token || response.data.token;
          authLogin(userData, token);
          navigate(userData.role === 'admin' ? '/admin' : '/main');
        } else {
          throw new Error("Неверный формат ответа от сервера");
        }
      } else {
        if (response.data) {
          setIsLogin(true);
          setFormData(prev => ({
            ...prev,
            username: ''
          }));
          setError('Регистрация успешна! Теперь вы можете войти.');
        }
      }

    } catch (err) {
      console.error("Ошибка авторизации:", err);
      if (err.response) {
        console.log("Ответ с ошибкой:", err.response.data);
      }
      const message = err.response?.data?.detail ||
        err.message ||
        "Ошибка авторизации. Проверьте введенные данные.";
      setError(typeof message === "string" ? message : message.join("\n"));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>
        {error && <div className={`message-box ${error.includes('успешна') ? 'success-message' : 'error-message'}`}>
          {error}
        </div>}
        
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="username">Имя пользователя</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                className={formErrors.username ? 'error' : ''}
                disabled={isLoading}
              />
              {formErrors.username && <span className="error-text">{formErrors.username}</span>}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="login">Логин</label>
            <input
              type="text"
              id="login"
              name="login"
              value={formData.login}
              onChange={handleInputChange}
              className={formErrors.login ? 'error' : ''}
              disabled={isLoading}
            />
            {formErrors.login && <span className="error-text">{formErrors.login}</span>}
            {!isLogin && formData.login === 'admin' && (
              <small className="role-hint">Будет создан аккаунт администратора</small>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className={formErrors.password ? 'error' : ''}
              disabled={isLoading}
            />
            {formErrors.password && <span className="error-text">{formErrors.password}</span>}
          </div>

          <button 
            type="submit" 
            className="submit-button"
            disabled={isLoading}
          >
            {isLoading 
              ? 'Загрузка...' 
              : (isLogin ? 'Войти' : 'Зарегистрироваться')
            }
          </button>
        </form>

        <p className="toggle-form">
          {isLogin ? "Нет аккаунта? " : "Уже есть аккаунт? "}
          <button
            className="toggle-button"
            onClick={() => {
              setIsLogin(!isLogin);
              setFormData({
                username: '',
                login: '',
                password: ''
              });
              setFormErrors({
                username: '',
                login: '',
                password: ''
              });
              setError('');
            }}
            disabled={isLoading}
          >
            {isLogin ? 'Зарегистрироваться' : 'Войти'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthPage; 