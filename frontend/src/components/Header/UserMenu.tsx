'use client';

import { useState, useRef, useCallback } from 'react';
import { User, LogOut } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useClickOutside } from '@/hooks/useClickOutside';
import { useRouter } from 'next/navigation';

interface UserMenuProps {
  userName: string;
}

export default function UserMenu({ userName }: UserMenuProps) {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const userMenuRef = useRef<HTMLDivElement>(null);
  const { logout, isAuthenticated } = useAuth();
  const router = useRouter();

  const closeMenu = useCallback(() => setShowUserMenu(false), []);
  useClickOutside(userMenuRef, closeMenu);

  const handleLogout = useCallback(async () => {
    await logout();
    setShowUserMenu(false);
    router.push('/');
  }, [logout, router]);

  const toggleMenu = useCallback(() => setShowUserMenu(!showUserMenu), [showUserMenu]);

  // Don't render if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <>
      <span className="text-sm text-gray-600">Hello, {userName}</span>
      <div className="relative" ref={userMenuRef}>
        <button 
          className="p-2 text-gray-600 hover:text-makers-purple transition-colors"
          onClick={toggleMenu}
          aria-label="User menu"
        >
          <User className="w-5 h-5" />
        </button>
        
        {showUserMenu && (
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50">
            <div className="px-4 py-2 border-b border-gray-100">
              <p className="text-sm font-medium text-gray-900">{userName}</p>
              <p className="text-xs text-gray-500">User</p>
            </div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </button>
          </div>
        )}
      </div>
    </>
  );
} 