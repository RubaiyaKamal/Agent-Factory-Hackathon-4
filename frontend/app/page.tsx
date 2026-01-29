'use client';

import { useState } from 'react';
import Link from 'next/link';
import Header from '@/components/Header';
import { BookOpenIcon, AcademicCapIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);

  const features = [
    {
      title: 'Learn',
      description: 'Access course materials and learn at your own pace',
      icon: BookOpenIcon,
      href: '/courses' as const,
      color: 'from-sky-400 to-blue-500',
    },
    {
      title: 'Practice',
      description: 'Take quizzes and assess your understanding',
      icon: AcademicCapIcon,
      href: '/quiz' as const,
      color: 'from-blue-400 to-indigo-500',
    },
    {
      title: 'Track',
      description: 'Monitor your progress and achievements',
      icon: ChartBarIcon,
      href: '/dashboard' as const,
      color: 'from-indigo-400 to-purple-500',
    },
  ] as const;

  return (
    <div className="min-h-screen bg-sky-100">
      <Header />

      <main id="main-content" className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Welcome to Course Companion FTE
          </h1>
          <p className="text-xl text-gray-700 mb-4 max-w-3xl mx-auto">
            Your digital tutor working <span className="font-semibold text-sky-600">168 hours/week</span> at{' '}
            <span className="font-semibold text-sky-600">85-90% cost savings</span> compared to human tutors
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link
                key={feature.title}
                href={feature.href}
                className={`group relative bg-gradient-to-br ${feature.color} p-1 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 cursor-pointer overflow-hidden`}
              >
                <div className="bg-white/95 backdrop-blur-sm rounded-xl p-8 h-full">
                  {/* Icon */}
                  <div className={`relative flex justify-center mb-6`}>
                    <div className={`p-4 rounded-full bg-gradient-to-br ${feature.color} shadow-lg transform group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className="w-12 h-12 text-white" />
                    </div>
                  </div>

                  {/* Content */}
                  <div className="relative text-center">
                    <h3 className={`text-2xl font-bold mb-3 bg-gradient-to-br ${feature.color} bg-clip-text text-transparent`}>
                      {feature.title}
                    </h3>
                    <p className="text-gray-700 text-lg leading-relaxed font-medium">
                      {feature.description}
                    </p>
                  </div>

                  {/* Arrow Icon */}
                  <div className="relative flex justify-center mt-6">
                    <div className={`p-2 rounded-full bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:translate-x-2`}>
                      <svg
                        className="w-5 h-5 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M13 7l5 5m0 0l-5 5m5-5H6"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>

        {/* Stats Section */}
        <div className="bg-gradient-to-br from-white via-sky-50 to-purple-50 rounded-2xl shadow-lg p-8 mb-12 border border-sky-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="bg-white/60 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-sky-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-sky-500 to-blue-600 bg-clip-text text-transparent mb-2">24/7</div>
              <div className="text-gray-700 font-semibold">Always Available</div>
            </div>
            <div className="bg-white/60 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-purple-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-purple-500 to-pink-600 bg-clip-text text-transparent mb-2">99%+</div>
              <div className="text-gray-700 font-semibold">Consistency</div>
            </div>
            <div className="bg-white/60 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-green-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent mb-2">85-90%</div>
              <div className="text-gray-700 font-semibold">Cost Savings</div>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white py-8 border-t border-sky-200" role="contentinfo">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600">
          <p>© {new Date().getFullYear()} Course Companion FTE - A Digital Full-Time Equivalent Educational Tutor</p>
        </div>
      </footer>
    </div>
  );
}