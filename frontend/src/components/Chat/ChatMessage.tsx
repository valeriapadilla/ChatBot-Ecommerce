'use client';

import { motion } from 'framer-motion';
import { User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Image from 'next/image';
import { ChatMessage as ChatMessageType } from '@/services/chatService';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const timestamp = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>

        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center overflow-hidden ${
            isUser 
              ? 'bg-teal-500 text-white' 
              : 'bg-gray-100'
          }`}>
            {isUser ? (
              <User className="h-4 w-4" />
            ) : (
              <Image
                src="/markerito.png"
                alt="Markerito"
                width={32}
                height={32}
                className="w-full h-full object-cover"
              />
            )}
          </div>
        </div>

        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-3 rounded-2xl max-w-full ${
            isUser
              ? 'bg-teal-500 text-white rounded-br-md'
              : 'bg-white text-gray-900 border border-gray-200 rounded-bl-md'
          }`}>
            {isUser ? (
              <div className="whitespace-pre-wrap break-words">
                {message.content}
              </div>
            ) : (
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    strong: ({ children }: { children: React.ReactNode }) => (
                      <strong className="font-semibold text-gray-900">{children}</strong>
                    ),
                    em: ({ children }: { children: React.ReactNode }) => (
                      <em className="italic text-gray-700">{children}</em>
                    ),
                    code: ({ children, className }: { children: React.ReactNode; className?: string }) => (
                      <code className={`bg-gray-100 px-1 py-0.5 rounded text-sm font-mono ${className || ''}`}>
                        {children}
                      </code>
                    ),
                    p: ({ children }: { children: React.ReactNode }) => (
                      <p className="mb-2 last:mb-0">{children}</p>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>
          
          <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
            {timestamp}
          </div>
        </div>
      </div>
    </motion.div>
  );
} 