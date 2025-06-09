// Ключи для localStorage
const STORAGE_KEYS = {
  TESTS: 'psychology_tests',
  TEST_RESULTS: 'psychology_test_results',
  LAST_BACKUP: 'last_backup_date'
};

// Утилиты для работы с localStorage
export const StorageService = {
  // Тесты
  saveTest: (test) => {
    const tests = StorageService.getAllTests();
    const newTest = {
      ...test,
      id: tests.length > 0 ? Math.max(...tests.map(t => t.id)) + 1 : 1,
      created_at: new Date().toISOString()
    };
    
    const updatedTests = [...tests, newTest];
    localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(updatedTests));
    return newTest;
  },

  getAllTests: () => {
    const tests = localStorage.getItem(STORAGE_KEYS.TESTS);
    return tests ? JSON.parse(tests) : [];
  },

  getTestById: (id) => {
    const tests = StorageService.getAllTests();
    return tests.find(test => test.id === parseInt(id));
  },

  updateTest: (id, updatedData) => {
    const tests = StorageService.getAllTests();
    const index = tests.findIndex(test => test.id === parseInt(id));
    
    if (index !== -1) {
      tests[index] = { ...tests[index], ...updatedData };
      localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(tests));
      return tests[index];
    }
    return null;
  },

  deleteTest: (id) => {
    const tests = StorageService.getAllTests();
    const filteredTests = tests.filter(test => test.id !== parseInt(id));
    localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(filteredTests));
  },

  // Результаты тестов
  saveTestResult: (result) => {
    const results = StorageService.getAllTestResults();
    const newResult = {
      ...result,
      id: results.length > 0 ? Math.max(...results.map(r => r.id)) + 1 : 1,
      completed_at: new Date().toISOString()
    };
    
    const updatedResults = [...results, newResult];
    localStorage.setItem(STORAGE_KEYS.TEST_RESULTS, JSON.stringify(updatedResults));
    return newResult;
  },

  getAllTestResults: () => {
    const results = localStorage.getItem(STORAGE_KEYS.TEST_RESULTS);
    return results ? JSON.parse(results) : [];
  },

  getTestResultsByUserId: (userId) => {
    const results = StorageService.getAllTestResults();
    return results.filter(result => result.user_id === parseInt(userId));
  },

  getTestResultsByTestId: (testId) => {
    const results = StorageService.getAllTestResults();
    return results.filter(result => result.test_id === parseInt(testId));
  },

  // Экспорт/импорт данных
  exportToFile: () => {
    const data = {
      tests: StorageService.getAllTests(),
      results: StorageService.getAllTestResults(),
      exported_at: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `psychology_data_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    localStorage.setItem(STORAGE_KEYS.LAST_BACKUP, new Date().toISOString());
  },

  importFromFile: (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          
          if (data.tests && data.results) {
            localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(data.tests));
            localStorage.setItem(STORAGE_KEYS.TEST_RESULTS, JSON.stringify(data.results));
            resolve(true);
          } else {
            reject(new Error('Неверный формат файла'));
          }
        } catch (error) {
          reject(error);
        }
      };

      reader.onerror = () => reject(new Error('Ошибка чтения файла'));
      reader.readAsText(file);
    });
  },

  // Очистка данных
  clearAllData: () => {
    localStorage.removeItem(STORAGE_KEYS.TESTS);
    localStorage.removeItem(STORAGE_KEYS.TEST_RESULTS);
    localStorage.removeItem(STORAGE_KEYS.LAST_BACKUP);
  }
}; 