// Mock данные для тестов
export const mockUsers = [
  { id: 1, username: 'admin', email: 'admin@test.com', role: 'admin' },
  { id: 2, username: 'user1', email: 'user1@test.com', role: 'user' },
  { id: 3, username: 'user2', email: 'user2@test.com', role: 'user' }
];

export const mockThoughts = [
  {
    id: 1,
    user_id: 2,
    situation: 'Тестовая ситуация 1',
    thought: 'Тестовая мысль 1',
    emotion: 'Спокойствие',
    behavior: 'Размышление',
    date: '2024-02-20T10:00:00Z'
  },
  {
    id: 2,
    user_id: 2,
    situation: 'Тестовая ситуация 2',
    thought: 'Тестовая мысль 2',
    emotion: 'Радость',
    behavior: 'Улыбка',
    date: '2024-02-21T11:00:00Z'
  }
];

export const mockTests = [
  {
    id: 1,
    name: 'Тест на тревожность',
    description: 'Описание теста на тревожность',
    max_score: 100
  },
  {
    id: 2,
    name: 'Тест на депрессию',
    description: 'Описание теста на депрессию',
    max_score: 50
  }
];

// Мок функции для API
export const mockApi = {
  // Аутентификация
  login: jest.fn((data) => {
    if (data.login === 'admin' && data.password === 'admin') {
      return Promise.resolve({
        data: {
          user: { id: 1, login: 'admin', role: 'admin' },
          access_token: 'mock-token'
        }
      });
    }
    return Promise.reject(new Error('Invalid credentials'));
  }),

  // Пользователи
  getUsers: jest.fn(() => Promise.resolve({ data: mockUsers })),
  deleteUser: jest.fn((id) => {
    if (mockUsers.find(u => u.id === id)) {
      return Promise.resolve({ data: { success: true } });
    }
    return Promise.reject(new Error('User not found'));
  }),

  // Мысли
  getThoughts: jest.fn((userId) => {
    const userThoughts = mockThoughts.filter(t => t.user_id === userId);
    return Promise.resolve({ data: userThoughts });
  }),
  createThought: jest.fn((data) => {
    const newThought = { ...data, id: Math.random() };
    return Promise.resolve({ data: newThought });
  }),

  // Тесты
  getTests: jest.fn(() => Promise.resolve({ data: mockTests })),
  getTest: jest.fn((id) => {
    const test = mockTests.find(t => t.id === id);
    if (test) {
      return Promise.resolve({ data: test });
    }
    return Promise.reject(new Error('Test not found'));
  })
}; 