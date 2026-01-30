/**
 * ARCHITECTURE: /frontend-web/services/
 * Purpose: Management of basic authentication credentials.
 */

export const authService = {
  /**
   * Encodes and stores credentials for basic auth.
   */
  setCredentials(username: string, password: string): void {
    const token = btoa(`${username}:${password}`);
    localStorage.setItem('auth_token', token);
  },

  /**
   * Retrieves the formatted Authorization header.
   */
  getAuthHeader(): Record<string, string> {
    const token = localStorage.getItem('auth_token');
    return token ? { 'Authorization': `Basic ${token}` } : {};
  },

  /**
   * Checks if a session is currently active.
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },

  /**
   * Clears session data.
   */
  logout(): void {
    localStorage.removeItem('auth_token');
  }
};