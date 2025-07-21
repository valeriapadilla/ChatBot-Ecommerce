'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';

import Input from '@/components/UI/Input';
import Button from '@/components/UI/Button';
import { useAuth } from '@/hooks/useAuth';
import { AUTH_CONTENT, AUTH_ROUTES } from '@/constants';
import { LoginFormData, AuthError } from '@/types';
import { isValidEmail } from '@/utils';


const loginSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .refine(isValidEmail, 'Please enter a valid email'),
  password: z.string()
    .min(1, 'Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

export default function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [authError, setAuthError] = useState<AuthError | null>(null);
  const router = useRouter();
  const { login } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setAuthError(null);
      const result = await login(data.email, data.password);
      
      if (result.success) {
        router.push('/products');
      } else {
        setAuthError({ message: result.error || 'Login failed' });
      }
    } catch (error) {
      setAuthError({ message: 'An unexpected error occurred' });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full max-w-sm mx-auto"
    >
      <div className="bg-white rounded-xl shadow-lg p-5 border border-gray-100">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            {AUTH_CONTENT.LOGIN.TITLE}
          </h1>
          <p className="text-sm text-gray-600">
            {AUTH_CONTENT.LOGIN.SUBTITLE}
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
          {/* Email Input */}
          <Input
            label={AUTH_CONTENT.LOGIN.EMAIL_LABEL}
            type="email"
            placeholder={AUTH_CONTENT.LOGIN.EMAIL_PLACEHOLDER}
            icon={Mail}
            error={errors.email?.message}
            {...register('email')}
          />

          {/* Password Input */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {AUTH_CONTENT.LOGIN.PASSWORD_LABEL}
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none">
                <Lock className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder={AUTH_CONTENT.LOGIN.PASSWORD_PLACEHOLDER}
                className={`block w-full rounded-md border px-3 py-2 text-sm text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 transition-all duration-200 pl-9 pr-9 ${
                  errors.password ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-gray-300 focus:border-teal-500'
                }`}
                {...register('password')}
              />
                              <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-2.5 flex items-center"
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <Eye className="h-4 w-4 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
            </div>
            {errors.password && (
              <p className="text-sm text-red-600">{errors.password.message}</p>
            )}
          </div>

          {/* Forgot Password */}
          <div className="text-right">
            <Link
              href="/forgot-password"
              className="text-sm text-teal-600 hover:text-teal-700 transition-colors"
            >
              {AUTH_CONTENT.LOGIN.FORGOT_PASSWORD}
            </Link>
          </div>

          {/* Auth Error */}
          {authError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-600">{authError.message}</p>
            </div>
          )}

          <Button
            type="submit"
            size="lg"
            loading={isSubmitting}
            className="w-full"
          >
            {AUTH_CONTENT.LOGIN.SUBMIT_TEXT}
          </Button>
        </form>

        {/* Sign Up Link */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            {AUTH_CONTENT.LOGIN.NO_ACCOUNT}{' '}
            <Link
              href={AUTH_ROUTES.SIGNUP}
              className="text-teal-600 hover:text-teal-700 font-medium transition-colors"
            >
              {AUTH_CONTENT.LOGIN.SIGNUP_LINK}
            </Link>
          </p>
        </div>
      </div>
    </motion.div>
  );
} 