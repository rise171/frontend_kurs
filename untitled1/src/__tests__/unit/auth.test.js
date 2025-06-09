import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AuthPage from '../../components/Auth/AuthPage';
import { AuthProvider } from '../../context/AuthContext';
import { api } from '../../axios';

// Мокаем axios
jest.mock('../../axios', () => ({
  api: {
    post: jest.fn()
  }
}));

const renderAuthPage = () => {
  render(
    <BrowserRouter>
      <AuthProvider>
        <AuthPage />
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('AuthPage Component', () => {
  beforeEach(() => {
    // Очищаем моки перед каждым тестом
    jest.clearAllMocks();
  });

  test('renders login form by default', () => {
    renderAuthPage();
    expect(screen.getByText('Вход')).toBeInTheDocument();
    expect(screen.getByLabelText('Логин')).toBeInTheDocument();
    expect(screen.getByLabelText('Пароль')).toBeInTheDocument();
  });

  test('switches to registration form', () => {
    renderAuthPage();
    fireEvent.click(screen.getByText('Зарегистрироваться'));
    expect(screen.getByText('Регистрация')).toBeInTheDocument();
    expect(screen.getByLabelText('Имя пользователя')).toBeInTheDocument();
  });

  test('handles successful login', async () => {
    const mockResponse = {
      data: {
        user: {
          id: 1,
          login: 'testuser',
          role: 'user'
        },
        access_token: 'test-token'
      }
    };

    api.post.mockResolvedValueOnce(mockResponse);

    renderAuthPage();

    fireEvent.change(screen.getByLabelText('Логин'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText('Пароль'), {
      target: { value: 'password' }
    });

    fireEvent.click(screen.getByText('Войти'));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/user/login', {
        login: 'testuser',
        password: 'password'
      });
    });
  });

  test('displays error message on login failure', async () => {
    api.post.mockRejectedValueOnce(new Error('Login failed'));

    renderAuthPage();

    fireEvent.change(screen.getByLabelText('Логин'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText('Пароль'), {
      target: { value: 'password' }
    });

    fireEvent.click(screen.getByText('Войти'));

    await waitFor(() => {
      expect(screen.getByText(/не удалось/i)).toBeInTheDocument();
    });
  });
}); 