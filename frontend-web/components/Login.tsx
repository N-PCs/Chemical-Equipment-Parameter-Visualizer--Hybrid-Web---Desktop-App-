
import React, { useState } from 'react';
import { authService } from '../services/auth-service';

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Explicit validation for demo and backend compatibility
    if (username === 'admin' && password === 'admin123') {
      authService.setCredentials(username, password);
      onLogin();
    } else if (!username || !password) {
      setError('Please provide both administrative credentials.');
    } else {
      setError('Invalid Access Key or System UID. Please refer to demo credentials.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden transform transition-all">
        {/* Branding Area */}
        <div className="bg-blue-600 p-8 text-center">
          <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-sm">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 4a2 2 0 114 0v1a2 2 0 012 2v3a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2V4zM7 10v1a2 2 0 002 2h6a2 2 0 002-2v-1" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Chemical Equipment Visualizer Login</h2>
        </div>

        {/* Form Area */}
        <div className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">System UID</label>
              <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-slate-300"
              />
            </div>
            
            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Access Key</label>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-slate-300"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-50 text-red-600 border border-red-100 rounded-lg text-xs font-medium">
                {error}
              </div>
            )}

            {/* Demo Credentials Hint */}
            <div className="p-4 bg-blue-50/50 rounded-2xl border border-blue-100/50">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-[10px] font-bold text-blue-600 uppercase tracking-widest">Demo Credentials</span>
              </div>
              <div className="flex justify-between text-xs text-slate-600 font-medium">
                <span>UID: <span className="text-slate-900 font-bold">admin</span></span>
                <span>KEY: <span className="text-slate-900 font-bold">admin123</span></span>
              </div>
            </div>

            <button 
              type="submit" 
              className="w-full py-3 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 transition-colors shadow-lg shadow-slate-200"
            >
              Initialize Session
            </button>
          </form>
          
          <div className="mt-8 text-center">
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest leading-relaxed">
              Secure Administrative Gateway<br/>
              <span className="opacity-50 font-normal normal-case">Access limited to authorized personnel only</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
