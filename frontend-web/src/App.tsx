import { useState, useEffect } from 'react';
import { Navbar } from './components/layout/Navbar';
import { Container } from './components/layout/Container';
import { Dashboard } from './components/dashboard/Dashboard';
import { LoginPage } from './components/auth/LoginPage';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
        setIsAuthenticated(true);
    }
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };
  
  const handleLogout = () => {
      localStorage.removeItem('token');
      // Also clear header in api service? We should probably export a logout function.
      // For now, reloading page or manual removal works.
      setIsAuthenticated(false);
      window.location.reload(); 
  }

  if (!isAuthenticated) {
     return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app">
      <Navbar onLogout={handleLogout} /> 
      {/* We could pass handleLogout to Navbar if we updated it */}
      <Container>
        <Dashboard />
      </Container>
    </div>
  );
}

export default App;
