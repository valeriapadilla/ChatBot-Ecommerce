import { render, screen, fireEvent } from '@testing-library/react';
import ChatInput from '../ChatInput';

describe('ChatInput', () => {
  it('renders input and button', () => {
    render(<ChatInput onSendMessage={jest.fn()} loading={false} />);
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('calls onSendMessage when form is submitted', () => {
    const mockSend = jest.fn();
    render(<ChatInput onSendMessage={mockSend} loading={false} />);
    fireEvent.change(screen.getByPlaceholderText(/type your message/i), { target: { value: 'Hello' } });
    fireEvent.click(screen.getByRole('button'));
    expect(mockSend).toHaveBeenCalledWith('Hello');
  });
}); 