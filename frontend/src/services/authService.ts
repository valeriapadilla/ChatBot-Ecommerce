import apiService, { ApiResponse } from './api';
import { API_ENDPOINTS } from '@/constants/api';

// Types for authentication
export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  name?: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    name?: string;
  };
}

export interface AuthResult {
  success: boolean;
  data?: AuthResponse;
  error?: string;
}

class AuthService {
  /**
   * Login user with email and password
   */
  async login(credentials: LoginRequest): Promise<AuthResult> {
    try {
      const response = await apiService.post<AuthResponse>(
        API_ENDPOINTS.AUTH.LOGIN,
        credentials
      );

      if (response.success && response.data) {
        // Store token in localStorage
        this.setToken(response.data.access_token);
        return {
          success: true,
          data: response.data,
        };
      }

      return {
        success: false,
        error: response.error || 'Login failed',
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Login failed',
      };
    }
  }

  /**
   * Sign up new user
   */
  async signup(userData: SignupRequest): Promise<AuthResult> {
    try {
      const response = await apiService.post<AuthResponse>(
        API_ENDPOINTS.AUTH.SIGNUP,
        userData
      );

      if (response.success && response.data) {
        // Store token in localStorage
        this.setToken(response.data.access_token);
        return {
          success: true,
          data: response.data,
        };
      }

      return {
        success: false,
        error: response.error || 'Signup failed',
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Signup failed',
      };
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<ApiResponse> {
    try {
      const token = this.getToken();
      const response = await apiService.post(
        API_ENDPOINTS.AUTH.LOGOUT,
        {},
        { Authorization: `Bearer ${token}` }
      );

      // Clear token regardless of response
      this.clearToken();

      return response;
    } catch (error) {
      // Clear token even if request fails
      this.clearToken();
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Logout failed',
      };
    }
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<ApiResponse<AuthResponse['user']>> {
    try {
      const token = this.getToken();
      if (!token) {
        return {
          success: false,
          error: 'No authentication token',
        };
      }

      return await apiService.get<AuthResponse['user']>(
        API_ENDPOINTS.AUTH.ME,
        { Authorization: `Bearer ${token}` }
      );
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get user info',
      };
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Get stored token
   */
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  /**
   * Set token in localStorage
   */
  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  /**
   * Clear token from localStorage
   */
  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  /**
   * Get authorization header for authenticated requests
   */
  getAuthHeader(): Record<string, string> | null {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : null;
  }
}

export const authService = new AuthService();
export default authService; 