import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext.jsx';
import { Navigate } from 'react-router-dom';
import Navbar from '../components/Navigation/Navbar';
import { api } from '../axios';
import { FaTrash } from 'react-icons/fa';
import './AdminPage.css';

const AdminPage = () => {
  const { isAuthenticated, isAdmin, user } = useAuth();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users');
      setUsers(response.data);
      setError('');
    } catch (err) {
      setError('Не удалось загрузить список пользователей');
      console.error('Error fetching users:', err);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Вы уверены, что хотите удалить этого пользователя?')) return;

    try {
      await api.delete(`/user/${userId}`);
      setSuccess('Пользователь успешно удален');
      fetchUsers();
      setError('');
    } catch (err) {
      setError('Не удалось удалить пользователя');
      console.error('Error deleting user:', err);
    }
  };

  if (!isAuthenticated() || !isAdmin()) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="page-container">
      <Navbar />
      <div className="admin-container">
        <div className="admin-welcome">
          <h2>Панель администратора</h2>
          <p>Добро пожаловать в панель управления! Здесь вы можете управлять пользователями системы и отслеживать их активность.</p>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <div className="users-section">
          <h3>Список пользователей</h3>
          <div className="users-list">
            {users.map(user => (
              <div key={user.id} className="user-card">
                <div className="user-info">
                  <p className="username">{user.username}</p>
                  <p className="email">{user.email}</p>
                  <p className="role" data-role={user.role}>
                    {user.role === 'admin' ? 'Администратор' : 'Пользователь'}
                  </p>
                </div>
                <button 
                  onClick={() => handleDeleteUser(user.id)}
                  className="delete-button"
                  disabled={user.role === 'admin'}
                >
                  <FaTrash />
                  Удалить
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage; 