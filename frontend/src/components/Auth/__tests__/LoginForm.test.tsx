import { render, screen, fireEvent } from '@testing-library/react';
import LoginForm from '../LoginForm';

describe('LoginForm', () => {
  it('renders login form fields', () => {
    render(<LoginForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('shows error on empty submit', () => {
    render(<LoginForm />);
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    expect(screen.getByText(/required/i)).toBeInTheDocument();
  });
}); 