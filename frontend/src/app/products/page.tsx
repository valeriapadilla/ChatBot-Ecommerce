'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Header from '@/components/Header';
import FloatingChatButton from '@/components/Chat/FloatingChatButton';
import { usePaginatedProducts } from '@/hooks/useProducts';

export default function ProductsPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const { products, loading, error, hasMore, loadMore } = usePaginatedProducts();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-teal-600"></div>
      </main>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <Header />

      <div className="pt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Our Products
            </h1>
            <p className="text-lg text-gray-600">
              Discover our amazing collection of products
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map(product => (
              <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="h-48 bg-gray-200 flex items-center justify-center">
                  {product.image_url ? (
                    <img src={product.image_url} alt={product.name} className="object-contain h-full" />
                  ) : (
                    <span className="text-gray-500">Product Image</span>
                  )}
                </div>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {product.name}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {product.features}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-2xl font-bold text-teal-600">${product.price}</span>
                    <button className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors">
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {error && <p className="text-red-500 mt-4">{error}</p>}
          {loading && <p className="mt-4">Loading...</p>}
          {hasMore && !loading && (
            <div className="flex justify-center mt-8">
              <button
                className="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
                onClick={loadMore}
              >
                Load More
              </button>
            </div>
          )}
        </div>
      </div>

      <FloatingChatButton isAuthenticated={isAuthenticated} />
    </main>
  );
}