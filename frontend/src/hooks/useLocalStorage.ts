import { useState, useEffect } from 'react';

export const useLocalStorage = () => {
  const [userData, setUserData] = useState({
    token: '',
    id: '',
    name: '',
    role: '',
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setUserData({
        token: localStorage.getItem('auth_token') || '',
        id: localStorage.getItem('user_id') || '',
        name: localStorage.getItem('user_name') || '',
        role: localStorage.getItem('user_role') || '',
      });
    }
  }, []);

  const getUserData = () => {
    if (typeof window !== 'undefined') {
      return {
        token: localStorage.getItem('auth_token') || '',
        id: localStorage.getItem('user_id') || '',
        name: localStorage.getItem('user_name') || '',
        role: localStorage.getItem('user_role') || '',
      };
    }
    return userData;
  };

  const isAuthenticated = () => {
    return !!localStorage.getItem('auth_token');
  };

  return {
    userData,
    getUserData,
    isAuthenticated,
  };
}; 