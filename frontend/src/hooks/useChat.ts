import { useState, useCallback, useRef } from 'react';
import { useAuth } from './useAuth';
import chatService, { ChatMessage, ChatResult } from '@/services/chatService';

export interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  isSending: boolean;
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearHistory: () => Promise<void>;
  loadHistory: () => Promise<void>;
  hasMoreMessages: boolean;
  loadMoreMessages: () => Promise<void>;
}

export const useChat = (): UseChatReturn => {
  const { isAuthenticated } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMoreMessages, setHasMoreMessages] = useState(true);
  const [currentOffset, setCurrentOffset] = useState(0);
  const abortControllerRef = useRef<AbortController | null>(null);

  const loadHistory = useCallback(async () => {
    if (!isAuthenticated) return;

    try {
      setIsLoading(true);
      setError(null);
      
      const response = await chatService.getHistory(50, 0);
      
      if (response.success && response.data) {
        setMessages(response.data.messages);
        setCurrentOffset(response.data.messages.length);
        setHasMoreMessages(response.data.total > response.data.messages.length);
      } else {
        setError(response.error || 'Failed to load chat history');
      }
    } catch (err) {
      setError('Failed to load chat history');
      console.error('Error loading chat history:', err);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  const loadMoreMessages = useCallback(async () => {
    if (!isAuthenticated || isLoading || !hasMoreMessages) return;

    try {
      setIsLoading(true);
      setError(null);
      
      const response = await chatService.getHistory(20, currentOffset);
      
      if (response.success && response.data) {
        setMessages(prev => [...response.data!.messages, ...prev]);
        setCurrentOffset(prev => prev + response.data!.messages.length);
        setHasMoreMessages(response.data.total > currentOffset + response.data.messages.length);
      } else {
        setError(response.error || 'Failed to load more messages');
      }
    } catch (err) {
      setError('Failed to load more messages');
      console.error('Error loading more messages:', err);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated, isLoading, hasMoreMessages, currentOffset]);

  const sendMessage = useCallback(async (message: string) => {
    if (!isAuthenticated || !message.trim()) return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    abortControllerRef.current = new AbortController();

    try {
      setIsSending(true);
      setError(null);

      // Create temporary user message
      const userMessage: ChatMessage = {
        id: `temp-user-${Date.now()}`,
        content: message,
        role: 'user',
        timestamp: new Date().toISOString(),
      };

      // Add user message to UI immediately
      setMessages(prev => [...prev, userMessage]);

      const recentMessages = messages.slice(-5);
      const context = recentMessages.length > 0 
        ? recentMessages.map(m => `${m.role}: ${m.content}`).join('\n')
        : undefined;

      const result: ChatResult = await chatService.sendMessage(message, context);

      if (result.success && result.data) {
        // Create assistant message from response
        const assistantMessage: ChatMessage = {
          id: `temp-assistant-${Date.now()}`,
          content: result.data.response,
          role: 'assistant',
          timestamp: new Date().toISOString(),
        };

        // Replace temporary user message and add assistant message
        setMessages(prev => {
          const filtered = prev.filter(m => m.id !== userMessage.id);
          return [...filtered, userMessage, assistantMessage];
        });
      } else {
        // Remove temporary user message on error
        setMessages(prev => prev.filter(m => m.id !== userMessage.id));
        setError(result.error || 'Failed to send message');
      }
    } catch (err) {
      // Remove temporary messages on error
      setMessages(prev => prev.filter(m => !m.id.startsWith('temp-')));
      setError('Failed to send message');
      console.error('Error sending message:', err);
    } finally {
      setIsSending(false);
      abortControllerRef.current = null;
    }
  }, [isAuthenticated, messages]);

  const clearHistory = useCallback(async () => {
    if (!isAuthenticated) return;

    try {
      setError(null);
      const response = await chatService.clearHistory();
      
      if (response.success) {
        setMessages([]);
        setCurrentOffset(0);
        setHasMoreMessages(true);
      } else {
        setError(response.error || 'Failed to clear chat history');
      }
    } catch (err) {
      setError('Failed to clear chat history');
      console.error('Error clearing chat history:', err);
    }
  }, [isAuthenticated]);

  return {
    messages,
    isLoading,
    isSending,
    error,
    sendMessage,
    clearHistory,
    loadHistory,
    hasMoreMessages,
    loadMoreMessages,
  };
}; 