'use client';

import { ReactNode, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '@/lib/store';

interface ProtectedRouteProps {
  children: ReactNode;
  allowedRoles?: string[];
}

export default function ProtectedRoute({ children, allowedRoles = [] }: ProtectedRouteProps) {
  const router = useRouter();
  const { user, loading } = useStore();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    } else if (user && allowedRoles.length > 0 && !allowedRoles.includes(user.tier)) {
      router.push('/unauthorized'); // Redirect to unauthorized page if role is not allowed
    }
  }, [user, loading, router, allowedRoles]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // The redirect effect handles navigation
  }

  return <>{children}</>;
}