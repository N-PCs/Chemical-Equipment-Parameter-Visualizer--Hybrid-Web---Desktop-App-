import React from 'react';
import './Button.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary', 
  isLoading = false, 
  className = '', 
  disabled,
  ...props 
}) => {
  return (
    <button 
      className={`btn btn-${variant} ${className}`} 
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <span className="btn-loader"></span> : children}
    </button>
  );
};
