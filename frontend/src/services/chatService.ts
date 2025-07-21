import apiService, { ApiResponse } from './api';
import authService from './authService';
import { API_ENDPOINTS } from '@/constants/api';

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  user_id?: string;
}

export interface SendMessageRequest {
  message: string;
  context?: string;
}

export interface SendMessageResponse {
  response: string; // Backend only returns the assistant's response
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
  total: number;
}

export interface ChatResult {
  success: boolean;
  data?: SendMessageResponse;
  error?: string;
}

class ChatService {
  async sendMessage(message: string, context?: string): Promise<ChatResult> {
    try {
      const authHeader = authService.getAuthHeader();
      if (!authHeader) {
        return {
          success: false,
          error: 'Authentication required',
        };
      }

      const response = await apiService.post<SendMessageResponse>(
        API_ENDPOINTS.CHAT.SEND_MESSAGE,
        { message, context },
        authHeader
      );

      if (response.success && response.data) {
        return {
          success: true,
          data: response.data,
        };
      }

      return {
        success: false,
        error: response.error || 'Failed to send message',
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to send message',
      };
    }
  }

  async getHistory(limit: number = 50, offset: number = 0): Promise<ApiResponse<ChatHistoryResponse>> {
    try {
      const authHeader = authService.getAuthHeader();
      if (!authHeader) {
        return {
          success: false,
          error: 'Authentication required',
        };
      }

      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString(),
      });

      return await apiService.get<ChatHistoryResponse>(
        `${API_ENDPOINTS.CHAT.GET_HISTORY}?${params}`,
        authHeader
      );
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get chat history',
      };
    }
  }


  async clearHistory(): Promise<ApiResponse<{ message: string }>> {
    try {
      const authHeader = authService.getAuthHeader();
      if (!authHeader) {
        return {
          success: false,
          error: 'Authentication required',
        };
      }

      return await apiService.post<{ message: string }>(
        API_ENDPOINTS.CHAT.CLEAR_HISTORY,
        {},
        authHeader
      );
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to clear chat history',
      };
    }
  }

  async getRecentMessages(limit: number = 5): Promise<ChatMessage[]> {
    try {
      const response = await this.getHistory(limit, 0);
      if (response.success && response.data) {
        return response.data.messages;
      }
      return [];
    } catch (error) {
      console.error('Failed to get recent messages:', error);
      return [];
    }
  }
}

export const chatService = new ChatService();
export default chatService; 