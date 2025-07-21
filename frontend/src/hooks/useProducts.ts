import { useState, useEffect } from 'react';
import apiService from '@/services/api';
import { API_ENDPOINTS } from '@/constants/api';
import { Product } from '@/types';
import authService from '@/services/authService';
const authHeader = authService.getAuthHeader(); 

interface UsePaginatedProductsResult {
  products: Product[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
  loadMore: () => void;
  reset: () => void;
}

const PAGE_SIZE = 10;

export function usePaginatedProducts() : UsePaginatedProductsResult {
  const [products, setProducts] = useState<Product[]>([]);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);

  const fetchProducts = async (pageNum: number) => {
    setLoading(true);
    setError(null);
    try {
      const offset = pageNum * PAGE_SIZE;
      const response = await apiService.get<Product[]>(
        `${API_ENDPOINTS.PRODUCTS.GET_ALL}?limit=${PAGE_SIZE}&offset=${offset}`,
        authHeader ?? undefined
      );
      if (response.success && response.data) {
        setProducts(prev => pageNum === 0 ? (response.data ?? []) : [...prev, ...(response.data ?? [])]);
        setHasMore((response.data?.length ?? 0) === PAGE_SIZE);
      } else {
        setError(response.error || 'Failed to fetch products');
      }
    } catch (err) {
      setError('Failed to fetch products');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts(page);
  }, [page]);

  const loadMore = () => {
    if (hasMore && !loading) setPage(prev => prev + 1);
  };

  const reset = () => {
    setProducts([]);
    setPage(0);
    setHasMore(true);
  };

  return { products, loading, error, hasMore, loadMore, reset };
}