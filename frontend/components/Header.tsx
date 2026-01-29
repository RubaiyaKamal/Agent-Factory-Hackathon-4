'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { useStore } from '@/lib/store';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';

export default function Header() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user } = useStore();
  const { signOut } = useAuth();

  const isActive = (path: string) => pathname === path;

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-blue-600">
              Course Companion FTE
            </Link>

            <nav className="ml-10 hidden md:flex space-x-8">
              <Link
                href="/"
                className={`${isActive('/') ? 'text-blue-600' : 'text-gray-500'} hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors`}
              >
                Home
              </Link>

              <Link
                href="/courses"
                className={`${isActive('/courses') ? 'text-blue-600' : 'text-gray-500'} hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors`}
              >
                Courses
              </Link>

              <Link
                href="/quiz"
                className={`${isActive('/quiz') ? 'text-blue-600' : 'text-gray-500'} hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors`}
              >
                Quiz
              </Link>

              {user && (
                <>
                  <Link
                    href="/dashboard"
                    className={`${isActive('/dashboard') ? 'text-blue-600' : 'text-gray-500'} hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors`}
                  >
                    Dashboard
                  </Link>

                  <Link
                    href="/profile"
                    className={`${isActive('/profile') ? 'text-blue-600' : 'text-gray-500'} hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors`}
                  >
                    Profile
                  </Link>
                </>
              )}
            </nav>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Welcome, {user.name}
                </span>

                <Button
                  onClick={() => signOut()}
                  variant="outline"
                  className="text-sm"
                >
                  Sign out
                </Button>
              </div>
            ) : (
              <div className="flex space-x-3">
                <Link href="/login">
                  <Button variant="outline">Sign in</Button>
                </Link>

                <Link href="/register">
                  <Button>Sign up</Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-gray-700 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {mobileMenuOpen ? (
                <X className="block h-6 w-6" aria-hidden="true" />
              ) : (
                <Menu className="block h-6 w-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t">
            <div className="pt-2 pb-3 space-y-1 px-2">
              <Link
                href="/"
                className={`${isActive('/') ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} hover:bg-gray-50 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium`}
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>

              <Link
                href="/courses"
                className={`${isActive('/courses') ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} hover:bg-gray-50 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium`}
                onClick={() => setMobileMenuOpen(false)}
              >
                Courses
              </Link>

              <Link
                href="/quiz"
                className={`${isActive('/quiz') ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} hover:bg-gray-50 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium`}
                onClick={() => setMobileMenuOpen(false)}
              >
                Quiz
              </Link>

              {user && (
                <>
                  <Link
                    href="/dashboard"
                    className={`${isActive('/dashboard') ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} hover:bg-gray-50 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Dashboard
                  </Link>

                  <Link
                    href="/profile"
                    className={`${isActive('/profile') ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} hover:bg-gray-50 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Profile
                  </Link>
                </>
              )}

              <div className="pt-4 pb-3 border-t border-gray-200">
                {user ? (
                  <div className="flex items-center px-5">
                    <div className="flex-shrink-0">
                      <div className="bg-gray-200 border-2 border-dashed rounded-xl w-10 h-10" />
                    </div>
                    <div className="ml-3">
                      <div className="text-base font-medium text-gray-800">{user.name}</div>
                      <div className="text-sm font-medium text-gray-500">{user.email}</div>
                    </div>
                  </div>
                ) : null}

                <div className="mt-3 px-2 space-y-1">
                  {user ? (
                    <button
                      onClick={() => {
                        signOut();
                        setMobileMenuOpen(false);
                      }}
                      className="w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 rounded-md"
                    >
                      Sign out
                    </button>
                  ) : (
                    <>
                      <Link
                        href="/login"
                        className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 rounded-md"
                        onClick={() => setMobileMenuOpen(false)}
                      >
                        Sign in
                      </Link>
                      <Link
                        href="/register"
                        className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 rounded-md"
                        onClick={() => setMobileMenuOpen(false)}
                      >
                        Sign up
                      </Link>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}