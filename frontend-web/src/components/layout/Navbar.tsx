import React from 'react';
import './Navbar.css';

export const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="navbar-logo">⚗️</span>
          <h1>ChemViz</h1>
        </div>
        <div className="navbar-actions">
           {/* Future: Auth/User info */}
           <span className="badge">v1.0</span>
        </div>
      </div>
    </nav>
  );
};
