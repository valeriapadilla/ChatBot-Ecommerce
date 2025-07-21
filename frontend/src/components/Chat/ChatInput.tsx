'use client';

import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import Button from '@/components/UI/Button';

interface ChatInputProps {
  onSendMessage: (message: string) => Promise<void>;
  disabled?: boolean;
  placeholder?: string;
}

export default function ChatInput({ onSendMessage, disabled = false, placeholder }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || disabled || isSubmitting) return;

    const trimmedMessage = message.trim();
    setMessage('');
    setIsSubmitting(true);

    try {
      await onSendMessage(trimmedMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [message]);

  return (
    <form onSubmit={handleSubmit} className="flex items-end space-x-3">
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder || "Type your message..."}
          disabled={disabled || isSubmitting}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 transition-all duration-200 min-h-[44px] max-h-[120px] disabled:bg-gray-50 disabled:cursor-not-allowed"
          rows={1}
        />
      </div>
      
      <Button
        type="submit"
        disabled={!message.trim() || disabled || isSubmitting}
        size="lg"
        className="px-4 py-3"
      >
        <Send className="h-4 w-4" />
      </Button>
    </form>
  );
} 