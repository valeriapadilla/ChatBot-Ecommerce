// User types
export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  isAuthenticated: boolean;
}

// Auth form types
export interface LoginFormData {
  email: string;
  password: string;
}

export interface SignupFormData {
  name?: string;
  email: string;
  password: string;
  confirmPassword: string;
}

// Auth error types
export interface AuthError {
  message: string;
}

export interface NavigationItem {
  href: string;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
}



export interface FloatingChatButtonProps {
  isAuthenticated?: boolean;
}

export interface AnimationConfig {
  initial: object;
  animate: object;
  transition: object;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface Product {
  id: string;
  name: string;
  features: string;
  price: number;
  image_url?: string;
  category: string;
  inStock: boolean;
}

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
} 