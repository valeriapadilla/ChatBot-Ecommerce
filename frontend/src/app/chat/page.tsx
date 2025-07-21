import ProtectedRoute from '@/components/Auth/ProtectedRoute';
import ChatInterface from '@/components/Chat/ChatInterface';

export default function ChatPage() {
  return (
    <ProtectedRoute>
      <ChatInterface />
    </ProtectedRoute>
  );
} 