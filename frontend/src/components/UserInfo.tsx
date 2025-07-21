'use client';

import { useLocalStorage } from '@/hooks/useLocalStorage';

export default function UserInfo() {
  const { userData, isAuthenticated } = useLocalStorage();

  if (!isAuthenticated()) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No user data found in localStorage</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">User Data from localStorage</h3>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">ID:</span>
          <span className="font-mono text-gray-900">{userData.id}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Name:</span>
          <span className="font-mono text-gray-900">{userData.name}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Email:</span>
          <span className="font-mono text-gray-900">{userData.email}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Role:</span>
          <span className="font-mono text-gray-900">{userData.role}</span>
        </div>
      </div>
    </div>
  );
} 