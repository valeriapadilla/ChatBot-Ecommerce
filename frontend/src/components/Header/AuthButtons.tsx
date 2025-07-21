import Link from 'next/link';
import { AUTH_ROUTES } from '@/constants';

export default function AuthButtons() {
  return (
    <>
      <Link
        href={AUTH_ROUTES.LOGIN}
        className="text-gray-600 hover:text-makers-purple transition-colors"
      >
        Sign In
      </Link>
      <Link
        href={AUTH_ROUTES.SIGNUP}
        className="bg-teal-600 text-white px-4 py-2 rounded-full hover:bg-teal-700 transition-colors"
      >
        Sign Up
      </Link>
    </>
  );
} 