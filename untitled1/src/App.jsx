import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navigation/Navbar';
import AuthPage from './components/Auth/AuthPage';
import AdminPage from './pages/AdminPage';
import UserPage from './pages/UserPage';
import CalendarPage from './pages/CalendarPage';
import ThoughtsPage from './pages/ThoughtsPage';
import FeedbackPage from './pages/FeedbackPage';
import TestsList from './components/Tests/TestsList';
import TestManager from './components/Tests/TestManager';
import TestTaking from './components/Tests/TestTaking';
import TestResults from './components/Tests/TestResults';
import ForbiddenPage from './components/Routes/ForbiddenPage';
import ProtectedRoute from './components/Routes/ProtectedRoute';
import './App.css';

// Компонент для редиректа с корневого маршрута
const RootRedirect = () => {
  const { isAuthenticated, isAdmin } = useAuth();
  
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  
  return <Navigate to="/tests" replace />;
};

// Компонент для отображения навигации
const AppLayout = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const isAuthPage = location.pathname === '/login';

  return (
    <div className="app">
      {isAuthenticated() && !isAuthPage && <Navbar />}
      <main className={`main-content ${!isAuthenticated() || isAuthPage ? 'no-navbar' : ''}`}>
        {children}
      </main>
    </div>
  );
};

// Основной компонент приложения
const AppContent = () => {
  return (
    <AppLayout>
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/" element={<RootRedirect />} />
        <Route path="/login" element={<AuthPage />} />
        <Route path="/forbidden" element={<ForbiddenPage />} />

        {/* Защищенные маршруты для всех пользователей */}
        <Route
          path="/user"
          element={
            <ProtectedRoute>
              <UserPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tests"
          element={
            <ProtectedRoute>
              <TestsList />
            </ProtectedRoute>
          }
        />
        <Route
          path="/test/:testId"
          element={
            <ProtectedRoute>
              <TestTaking />
            </ProtectedRoute>
          }
        />
        <Route
          path="/results"
          element={
            <ProtectedRoute>
              <TestResults />
            </ProtectedRoute>
          }
        />
        <Route
          path="/calendar"
          element={
            <ProtectedRoute>
              <CalendarPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/thoughts"
          element={
            <ProtectedRoute>
              <ThoughtsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/feedback"
          element={
            <ProtectedRoute>
              <FeedbackPage />
            </ProtectedRoute>
          }
        />

        {/* Защищенные маршруты только для администраторов */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute requireAdmin={true}>
              <AdminPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/tests"
          element={
            <ProtectedRoute requireAdmin={true}>
              <TestManager />
            </ProtectedRoute>
          }
        />

        {/* Маршрут для несуществующих страниц */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppLayout>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

export default App; 