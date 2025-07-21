import Image from 'next/image';

export default function Logo() {
  return (
    <div className="flex items-center space-x-3">
      <div className="w-8 h-8 relative">
        <Image
          src="/makers-logo.png"
          alt="Makers Tech"
          fill
          className="object-contain"
        />
      </div>
      <h1 className="text-xl font-bold text-makers-blue">Makers Tech</h1>
    </div>
  );
} 