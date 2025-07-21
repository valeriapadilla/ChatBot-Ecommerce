import { render, screen } from '@testing-library/react';
import ChatMessage from '../ChatMessage';

describe('ChatMessage', () => {
  it('renders user message', () => {
    render(<ChatMessage message="Hello" sender="user" />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('renders bot message', () => {
    render(<ChatMessage message="Hi, how can I help you?" sender="bot" />);
    expect(screen.getByText(/how can I help/i)).toBeInTheDocument();
  });
}); 