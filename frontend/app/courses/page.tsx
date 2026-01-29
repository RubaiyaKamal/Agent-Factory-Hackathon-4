'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { useStore } from '@/lib/store';
import { apiClient } from '@/lib/api';

interface Course {
  id: string;
  title: string;
  description: string;
  duration: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  progress: number;
  thumbnail: string;
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'beginner' | 'intermediate' | 'advanced'>('all');
  const { user } = useStore();

  // Mock data for courses
  useEffect(() => {
    const mockCourses: Course[] = [
      {
        id: '1',
        title: 'Introduction to AI Agents',
        description: 'Learn the fundamentals of building AI agents with modern tools and techniques.',
        duration: '4 weeks',
        level: 'beginner',
        progress: user?.tier === 'premium' ? 65 : 0,
        thumbnail: '/ai-agents-intro.png'
      },
      {
        id: '2',
        title: 'Cloud-Native Python Development',
        description: 'Master cloud-native development with Python, containers, and Kubernetes.',
        duration: '6 weeks',
        level: 'intermediate',
        progress: user?.tier === 'premium' ? 30 : 0,
        thumbnail: '/cloud-python.png'
      },
      {
        id: '3',
        title: 'Generative AI Fundamentals',
        description: 'Explore the foundations of generative AI, LLMs, prompting, and RAG systems.',
        duration: '5 weeks',
        level: 'intermediate',
        progress: user?.tier === 'premium' ? 0 : 0,
        thumbnail: '/generative-ai.png'
      },
      {
        id: '4',
        title: 'Modern Python with Typing',
        description: 'Advanced Python programming with type hints, async/await, and best practices.',
        duration: '3 weeks',
        level: 'advanced',
        progress: user?.tier === 'premium' ? 15 : 0,
        thumbnail: '/modern-python.png'
      }
    ];

    setCourses(mockCourses);
    setLoading(false);
  }, [user]);

  const filteredCourses = filter === 'all'
    ? courses
    : courses.filter(course => course.level === filter);

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading courses...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sky-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Browse Courses</h1>
          <p className="text-gray-600">Expand your knowledge with our expertly crafted courses</p>
        </div>

        <div className="mb-6 flex flex-wrap gap-2">
          <Button
            variant={filter === 'all' ? 'primary' : 'outline'}
            onClick={() => setFilter('all')}
          >
            All Courses
          </Button>
          <Button
            variant={filter === 'beginner' ? 'primary' : 'outline'}
            onClick={() => setFilter('beginner')}
          >
            Beginner
          </Button>
          <Button
            variant={filter === 'intermediate' ? 'primary' : 'outline'}
            onClick={() => setFilter('intermediate')}
          >
            Intermediate
          </Button>
          <Button
            variant={filter === 'advanced' ? 'primary' : 'outline'}
            onClick={() => setFilter('advanced')}
          >
            Advanced
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => (
            <div key={course.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <img
                src={course.thumbnail}
                alt={course.title}
                className="w-full h-128 object-contain bg-gradient-to-br from-green-100 via-white to-blue-100"
              />

              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-gray-900">{course.title}</h3>
                  <span className={`text-xs px-2 py-1 rounded-full ${getLevelColor(course.level)}`}>
                    {course.level}
                  </span>
                </div>

                <p className="text-gray-600 mb-4">{course.description}</p>

                <div className="mb-4">
                  <div className="flex justify-between text-sm text-gray-500 mb-1">
                    <span>Duration: {course.duration}</span>
                    {course.progress > 0 && (
                      <span>Progress: {course.progress}%</span>
                    )}
                  </div>

                  {course.progress > 0 && (
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${course.progress}%` }}
                      ></div>
                    </div>
                  )}
                </div>

                <div className="flex justify-between items-center">
                  {/* All courses FREE for testing! */}
                  {course.progress > 0 ? (
                    <Link href={`/courses/${course.id}?continue=true`}>
                      <Button className="bg-blue-600 hover:bg-blue-700">▶ Continue Learning</Button>
                    </Link>
                  ) : (
                    <Link href={`/courses/${course.id}`}>
                      <Button className="bg-green-600 hover:bg-green-700">🚀 Start FREE</Button>
                    </Link>
                  )}

                  <span className="text-sm font-semibold text-green-600">
                    FREE
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredCourses.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No courses found for the selected filter.</p>
          </div>
        )}
      </div>
    </div>
  );
}