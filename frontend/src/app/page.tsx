'use client';

import Header from '@/components/Header';
import Hero from '@/components/Hero';
import FloatingChatButton from '@/components/Chat/FloatingChatButton';
import { useAuth } from '@/hooks/useAuth';

export default function Home() {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-teal-600"></div>
      </main>
    );
  }

  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <FloatingChatButton isAuthenticated={isAuthenticated} />
    </main>
  );
}
