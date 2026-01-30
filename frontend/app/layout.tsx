import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/contexts/AuthContext';
import Header from '@/components/Header';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Course Companion FTE',
  description: 'A Digital Full-Time Equivalent Educational Tutor',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
      <body className="min-h-screen bg-gray-50 antialiased">
        <div className="relative flex min-h-dvh flex-col bg-white">
          <AuthProvider>
            <Header />
            {children}
          </AuthProvider>
        </div>

        {/* Skip link for keyboard navigation */}
        <div className="fixed top-0 left-0 z-[100]">
          <a
            href="#main-content"
            className="sr-only focus:not-sr-only focus:absolute px-4 py-2 bg-blue-600 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Skip to main content
          </a>
        </div>
      </body>
    </html>
  );
}