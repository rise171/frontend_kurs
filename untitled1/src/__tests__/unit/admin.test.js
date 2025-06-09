import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AdminPage from '../../pages/AdminPage';
import { AuthProvider } from '../../context/AuthContext';
import { api } from '../../axios';

// Мокаем axios и useAuth
jest.mock('../../axios', () => ({
  api: {
    get: jest.fn(),
    delete: jest.fn()
  }
}));

jest.mock('../../context/AuthContext', () => ({
  ...jest.requireActual('../../context/AuthContext'),
  useAuth: () => ({
    isAuthenticated: () => true,
    isAdmin: () => true,
    user: { id: 1, role: 'admin' }
  })
}));

const mockUsers = [
  { id: 1, username: 'admin', email: 'admin@test.com', role: 'admin' },
  { id: 2, username: 'user1', email: 'user1@test.com', role: 'user' }
];

const renderAdminPage = () => {
  render(
    <BrowserRouter>
      <AuthProvider>
        <AdminPage />
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('AdminPage Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    api.get.mockResolvedValue({ data: mockUsers });
  });

  test('renders admin panel with user list', async () => {
    renderAdminPage();

    await waitFor(() => {
      expect(screen.getByText('Панель администратора')).toBeInTheDocument();
      expect(screen.getByText('Список пользователей')).toBeInTheDocument();
    });

    expect(screen.getByText('admin@test.com')).toBeInTheDocument();
    expect(screen.getByText('user1@test.com')).toBeInTheDocument();
  });

  test('handles user deletion', async () => {
    window.confirm = jest.fn(() => true);
    api.delete.mockResolvedValueOnce({});

    renderAdminPage();

    await waitFor(() => {
      expect(screen.getByText('user1@test.com')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByText('Удалить');
    fireEvent.click(deleteButtons[1]); // Кликаем по кнопке удаления обычного пользователя

    await waitFor(() => {
      expect(api.delete).toHaveBeenCalledWith('/user/2');
      expect(api.get).toHaveBeenCalledTimes(2); // Initial load + after deletion
    });
  });

  test('shows error message when user deletion fails', async () => {
    window.confirm = jest.fn(() => true);
    api.delete.mockRejectedValueOnce(new Error('Delete failed'));

    renderAdminPage();

    await waitFor(() => {
      expect(screen.getByText('user1@test.com')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByText('Удалить');
    fireEvent.click(deleteButtons[1]);

    await waitFor(() => {
      expect(screen.getByText('Не удалось удалить пользователя')).toBeInTheDocument();
    });
  });

  test('admin user cannot be deleted', async () => {
    renderAdminPage();

    await waitFor(() => {
      expect(screen.getByText('admin@test.com')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByText('Удалить');
    expect(deleteButtons[0]).toBeDisabled();
  });
}); 