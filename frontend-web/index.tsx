
/**
 * ARCHITECTURE: Project Root
 * Purpose: Web entry point bridging the root index.html to the React frontend-web.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './frontend-web/App';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
