import React, { useState } from 'react';
import { Button } from '../common/Button';
import { Card } from '../common/Card';
import { login, setAuthToken } from '../../services/api';
import './LoginPage.css';

interface LoginPageProps {
  onLoginSuccess: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const token = await login(username, password);
      // Store token
      setAuthToken(token);
      onLoginSuccess();
    } catch (err) {
      setError('Invalid credentials. Please try again.');
        console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Card title="Welcome Back" className="login-card">
        <div className="login-header">
            <span className="login-icon">⚗️</span>
            <h2>ChemViz Login</h2>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
            />
          </div>
          
          {error && <div className="error-msg">{error}</div>}

          <Button type="submit" isLoading={loading} className="w-full mt-4">
            Sign In
          </Button>
        </form>
      </Card>
    </div>
  );
};
