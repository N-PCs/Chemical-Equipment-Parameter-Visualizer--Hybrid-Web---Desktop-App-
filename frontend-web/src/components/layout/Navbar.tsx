import React from 'react';
import './Navbar.css';

interface NavbarProps {
  onLogout?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onLogout }) => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="navbar-logo">⚗️</span>
          <h1>ChemViz</h1>
        </div>
        <div className="navbar-actions">
           {onLogout && (
             <button onClick={onLogout} className="btn-logout">
               Logout
             </button>
           )}
           <span className="badge">v1.0</span>
        </div>
      </div>
    </nav>
  );
};
