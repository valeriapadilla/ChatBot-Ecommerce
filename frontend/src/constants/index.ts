// Navigation and routing constants
export const NAVIGATION_ITEMS = [
  { href: '/', label: 'Home' },
  { href: '/products', label: 'Products' },
  { href: '/about', label: 'About' },
] as const;

export const AUTH_ROUTES = {
  LOGIN: '/login',
  SIGNUP: '/signup',
  CHAT: '/chat',
} as const;

// UI Content constants
export const HERO_CONTENT = {
  BADGE_TEXT: 'AI-Powered Shopping Experience',
  TITLE: 'Makers Tech',
  DESCRIPTION: 'Experience the future of online shopping with our AI assistant Makerito. Get personalized product recommendations with instant answers.',
  CTA_TEXT: 'Talk with Makerito',
} as const;

export const CHAT_CONTENT = {
  AUTHENTICATED_TOOLTIP: 'Chat with Makerito',
  UNAUTHENTICATED_TOOLTIP: 'Sign in to chat',
} as const;

// Authentication UI content
export const AUTH_CONTENT = {
  LOGIN: {
    TITLE: 'Welcome Back',
    SUBTITLE: 'Sign in to continue your AI shopping experience',
    EMAIL_LABEL: 'Email *',
    EMAIL_PLACEHOLDER: 'Enter your email',
    PASSWORD_LABEL: 'Password *',
    PASSWORD_PLACEHOLDER: 'Enter your password',
    SUBMIT_TEXT: 'Sign In',
    FORGOT_PASSWORD: 'Forgot password?',
    NO_ACCOUNT: "Don't have an account?",
    SIGNUP_LINK: 'Sign up',
  },
  SIGNUP: {
    TITLE: 'Join Makers Tech',
    SUBTITLE: 'Create your account and start shopping with AI',
    NAME_LABEL: 'Name',
    NAME_PLACEHOLDER: 'Enter your name (optional)',
    EMAIL_LABEL: 'Email *',
    EMAIL_PLACEHOLDER: 'Enter your email',
    PASSWORD_LABEL: 'Password *',
    PASSWORD_PLACEHOLDER: 'Create a password',
    CONFIRM_PASSWORD_LABEL: 'Confirm Password *',
    CONFIRM_PASSWORD_PLACEHOLDER: 'Confirm your password',
    SUBMIT_TEXT: 'Create Account',
    HAS_ACCOUNT: 'Already have an account?',
    LOGIN_LINK: 'Sign in',
  },
} as const;

// Animation timing constants
export const ANIMATION_DELAYS = {
  HERO_BADGE: 0.2,
  HERO_TITLE: 0.4,
  HERO_DESCRIPTION: 0.6,
  HERO_CTA: 0.8,
  FLOATING_CHAT: 0.2, // Updated to match the new faster animation
} as const; 