'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { User, Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';

import Input from '@/components/UI/Input';
import Button from '@/components/UI/Button';
import { useAuth } from '@/hooks/useAuth';
import { AUTH_CONTENT, AUTH_ROUTES } from '@/constants';
import { SignupFormData, AuthError } from '@/types';
import { isValidEmail, isValidPassword } from '@/utils';

// Validation schema
const signupSchema = z.object({
  name: z.string().optional(),
  email: z.string()
    .min(1, 'Email is required')
    .refine(isValidEmail, 'Please enter a valid email'),
  password: z.string()
    .min(1, 'Password is required')
    .refine(isValidPassword, 'Password must be at least 8 characters with uppercase, lowercase, and number'),
  confirmPassword: z.string()
    .min(1, 'Please confirm your password'),
}).refine((data: { password: string; confirmPassword: string }) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

export default function SignupForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [authError, setAuthError] = useState<AuthError | null>(null);
  const router = useRouter();
  const { signup } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupFormData) => {
    try {
      setAuthError(null);
      const result = await signup(data.name || '', data.email, data.password);
      
      if (result.success) {
        router.push('/products');
      } else {
        setAuthError({ message: result.error || 'Signup failed' });
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
            {AUTH_CONTENT.SIGNUP.TITLE}
          </h1>
          <p className="text-sm text-gray-600">
            {AUTH_CONTENT.SIGNUP.SUBTITLE}
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
          {/* Name Input */}
          <Input
            label={AUTH_CONTENT.SIGNUP.NAME_LABEL}
            type="text"
            placeholder={AUTH_CONTENT.SIGNUP.NAME_PLACEHOLDER}
            icon={User}
            error={errors.name?.message}
            {...register('name')}
          />

          {/* Email Input */}
          <Input
            label={AUTH_CONTENT.SIGNUP.EMAIL_LABEL}
            type="email"
            placeholder={AUTH_CONTENT.SIGNUP.EMAIL_PLACEHOLDER}
            icon={Mail}
            error={errors.email?.message}
            {...register('email')}
          />

          {/* Password Input */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {AUTH_CONTENT.SIGNUP.PASSWORD_LABEL}
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder={AUTH_CONTENT.SIGNUP.PASSWORD_PLACEHOLDER}
                className={`block w-full rounded-lg border px-4 py-3 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 transition-all duration-200 pl-10 pr-10 ${
                  errors.password ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-gray-300 focus:border-teal-500'
                }`}
                {...register('password')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                )}
              </button>
            </div>
            {errors.password && (
              <p className="text-sm text-red-600">{errors.password.message}</p>
            )}
          </div>

          {/* Confirm Password Input */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {AUTH_CONTENT.SIGNUP.CONFIRM_PASSWORD_LABEL}
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                placeholder={AUTH_CONTENT.SIGNUP.CONFIRM_PASSWORD_PLACEHOLDER}
                className={`block w-full rounded-lg border px-4 py-3 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 transition-all duration-200 pl-10 pr-10 ${
                  errors.confirmPassword ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-gray-300 focus:border-teal-500'
                }`}
                {...register('confirmPassword')}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                )}
              </button>
            </div>
            {errors.confirmPassword && (
              <p className="text-sm text-red-600">{errors.confirmPassword.message}</p>
            )}
          </div>

          {/* Password Requirements */}
          <div className="bg-gray-50 rounded-md p-2">
            <p className="text-xs text-gray-600 mb-1">Password requirements:</p>
            <ul className="text-xs text-gray-500 space-y-0.5">
              <li>• At least 8 characters</li>
              <li>• One uppercase letter</li>
              <li>• One lowercase letter</li>
              <li>• One number</li>
            </ul>
          </div>

          {/* Auth Error */}
          {authError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-600">{authError.message}</p>
            </div>
          )}

          {/* Submit Button */}
          <Button
            type="submit"
            size="lg"
            loading={isSubmitting}
            className="w-full"
          >
            {AUTH_CONTENT.SIGNUP.SUBMIT_TEXT}
          </Button>
        </form>

        {/* Sign In Link */}
        <div className="mt-4 text-center">
          <p className="text-xs text-gray-600">
            {AUTH_CONTENT.SIGNUP.HAS_ACCOUNT}{' '}
            <Link
              href={AUTH_ROUTES.LOGIN}
              className="text-teal-600 hover:text-teal-700 font-medium transition-colors"
            >
              {AUTH_CONTENT.SIGNUP.LOGIN_LINK}
            </Link>
          </p>
        </div>
      </div>
    </motion.div>
  );
} 