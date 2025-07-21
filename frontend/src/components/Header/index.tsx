'use client';

import { useAuth } from '@/hooks/useAuth';
import Logo from './Logo';
import Navigation from './Navigation';
import UserMenu from './UserMenu';
import AuthButtons from './AuthButtons';

export default function Header() {
  const { user, isAuthenticated } = useAuth();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Logo />
          <Navigation />
          
          <div className="flex items-center space-x-4">
            {isAuthenticated && user ? (
              <UserMenu userName={user.name} />
            ) : (
              <AuthButtons />
            )}
          </div>
        </div>
      </div>
    </header>
  );
} 