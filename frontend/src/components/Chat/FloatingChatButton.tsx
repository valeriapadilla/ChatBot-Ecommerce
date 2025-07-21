'use client';

import { motion } from 'framer-motion';
import { MessageCircle, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { FloatingChatButtonProps } from '@/types';
import { AUTH_ROUTES, CHAT_CONTENT, ANIMATION_DELAYS } from '@/constants';

export default function FloatingChatButton({ isAuthenticated = false }: FloatingChatButtonProps) {
  const href = isAuthenticated ? AUTH_ROUTES.CHAT : AUTH_ROUTES.LOGIN;
  const tooltipText = isAuthenticated 
    ? CHAT_CONTENT.AUTHENTICATED_TOOLTIP 
    : CHAT_CONTENT.UNAUTHENTICATED_TOOLTIP;

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: 0.2, duration: 0.3, type: "spring" }}
      className="fixed bottom-8 right-8 z-50"
    >
      {/* Arrow and text */}
      <motion.div
        initial={{ x: 20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.3 }}
        className="absolute right-full mr-4 top-1/2 transform -translate-y-1/2 flex items-center space-x-2"
      >
        <div className="bg-white text-gray-700 text-sm px-3 py-2 rounded-lg shadow-lg border border-gray-200 whitespace-nowrap font-medium">
          Need help choosing?
        </div>
        <ArrowLeft className="w-4 h-4 text-gray-400" />
      </motion.div>

      <Link href={href}>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          className="group relative bg-teal-600 text-white w-16 h-16 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center"
        >
          <MessageCircle className="w-6 h-6" />
          
          {/* Tooltip on hover */}
          <div className="absolute right-full mr-3 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
            <div className="bg-gray-900 text-white text-sm px-3 py-2 rounded-lg whitespace-nowrap">
              {tooltipText}
              <div className="absolute left-full top-1/2 transform -translate-y-1/2 w-0 h-0 border-l-4 border-l-gray-900 border-t-4 border-t-transparent border-b-4 border-b-transparent"></div>
            </div>
          </div>
        </motion.button>
      </Link>
    </motion.div>
  );
} 