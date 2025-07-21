import { useState, useEffect } from 'react';
import { User } from '@/types';
import authService, { AuthResult } from '@/services/authService';

const decodeJWT = (token: string) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (error) {
    return null;
  }
};

// Simple localStorage utilities -  save what we need
const saveUserData = (userData: User, token: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user_id', userData.id);
    localStorage.setItem('user_name', userData.name);
    localStorage.setItem('user_role', userData.role);
  }
};

const clearUserData = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
    localStorage.removeItem('user_role');
  }
};

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      if (authService.isAuthenticated()) {
        const token = authService.getToken();
        if (token) {
          const payload = decodeJWT(token);
          if (payload) {
            const userData: User = {
              id: payload.sub,
              name: payload.name || localStorage.getItem('user_name') || '',
              email: payload.email,
              role: payload.role || 'user',
              isAuthenticated: true,
            };
            setUser(userData);
            saveUserData(userData, token);
          }
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      clearUserData();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      setIsLoading(true);
      const result: AuthResult = await authService.login({ email, password });
      
      if (result.success && result.data) {
        const payload = decodeJWT(result.data.access_token);
        if (payload) {
          const userData: User = {
            id: payload.sub,
            name: payload.name || result.data.user.name || '',
            email: payload.email,
            role: payload.role || 'user',
            isAuthenticated: true,
          };
          setUser(userData);
          saveUserData(userData, result.data.access_token);
          return { success: true };
        }
      }
      
      return { success: false, error: result.error };
    } catch (error) {
      console.error('Login failed:', error);
      return { success: false, error: 'Login failed' };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<{ success: boolean; error?: string }> => {
    try {
      const result = await authService.logout();
      setUser(null);
      clearUserData();
      return { success: result.success, error: result.error };
    } catch (error) {
      console.error('Logout failed:', error);
      setUser(null);
      clearUserData();
      return { success: false, error: 'Logout failed' };
    }
  };

  const signup = async (name: string, email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      setIsLoading(true);
      const result: AuthResult = await authService.signup({ name, email, password });
      
      if (result.success && result.data) {
        const payload = decodeJWT(result.data.access_token);
        if (payload) {
          const userData: User = {
            id: payload.sub,
            name: payload.name || result.data.user.name || '',
            email: payload.email,
            role: payload.role || 'user',
            isAuthenticated: true,
          };
          setUser(userData);
          saveUserData(userData, result.data.access_token);
          return { success: true };
        }
      }
      
      return { success: false, error: result.error };
    } catch (error) {
      console.error('Signup failed:', error);
      return { success: false, error: 'Signup failed' };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    user,
    isAuthenticated: !!user?.isAuthenticated,
    isLoading,
    login,
    logout,
    signup,
  };
}; 