import Link from 'next/link';
import { NAVIGATION_ITEMS } from '@/constants';

export default function Navigation() {
  return (
    <nav className="hidden md:flex items-center space-x-8">
      {NAVIGATION_ITEMS.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="text-gray-600 hover:text-makers-purple transition-colors"
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
} 