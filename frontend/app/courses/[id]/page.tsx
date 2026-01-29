'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { useStore } from '@/lib/store';

interface Chapter {
  id: string;
  title: string;
  duration: string;
  completed: boolean;
}

interface Course {
  id: string;
  title: string;
  description: string;
  instructor: string;
  duration: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  progress: number;
  chapters: Chapter[];
  thumbnail: string;
}

export default function CourseDetailPage() {
  const { id } = useParams();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const { user, courses: storeCourses, updateCourseProgress } = useStore();

  // Get the current course from store to access completed chapters
  const currentStoreCourse = storeCourses.find(c => c.id === id);

  // Mock data for the course
  useEffect(() => {
    const mockCourse: Course = {
      id: String(id),
      title: id === '1' ? 'Introduction to AI Agents' :
             id === '2' ? 'Cloud-Native Python Development' :
             id === '3' ? 'Generative AI Fundamentals' : 'Modern Python with Typing',
      description: id === '1' ? 'Learn the fundamentals of building AI agents with modern tools and techniques.' :
                    id === '2' ? 'Master cloud-native development with Python, containers, and Kubernetes.' :
                    id === '3' ? 'Explore the foundations of generative AI, LLMs, prompting, and RAG systems.' :
                    'Advanced Python programming with type hints, async/await, and best practices.',
      instructor: 'Dr. Jane Smith',
      duration: id === '1' ? '4 weeks' :
                id === '2' ? '6 weeks' :
                id === '3' ? '5 weeks' : '3 weeks',
      level: id === '1' ? 'beginner' :
             id === '2' ? 'intermediate' :
             id === '3' ? 'intermediate' : 'advanced',
      progress: currentStoreCourse?.progress || 0,
      thumbnail: id === '1' ? '/ai-agents-intro.png' :
                 id === '2' ? '/cloud-python.png' :
                 id === '3' ? '/generative-ai.png' : '/modern-python.png',
      chapters: [
        { id: '1', title: 'Introduction to Concepts', duration: '15 min', completed: currentStoreCourse?.completedChapters.includes('1') || false },
        { id: '2', title: 'Getting Started', duration: '25 min', completed: currentStoreCourse?.completedChapters.includes('2') || false },
        { id: '3', title: 'Core Principles', duration: '30 min', completed: currentStoreCourse?.completedChapters.includes('3') || false },
        { id: '4', title: 'Practical Applications', duration: '40 min', completed: currentStoreCourse?.completedChapters.includes('4') || false },
        { id: '5', title: 'Advanced Techniques', duration: '35 min', completed: currentStoreCourse?.completedChapters.includes('5') || false },
        { id: '6', title: 'Final Project', duration: '45 min', completed: currentStoreCourse?.completedChapters.includes('6') || false },
      ]
    };

    setCourse(mockCourse);
    setLoading(false);
  }, [id, user, currentStoreCourse]);

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleChapterClick = (chapterId: string) => {
    // Allow access to courses 1 and 2 for testing
    // In production, uncomment the premium check below

    // if (user?.tier !== 'premium' && course?.level !== 'beginner' && id !== '2') {
    //   alert('This feature requires a premium subscription.');
    //   return;
    // }

    // Update progress in the store
    const completedChapters = course?.chapters.filter(ch => ch.completed || ch.id === chapterId).length || 0;
    const totalChapters = course?.chapters.length || 1;
    const newProgress = Math.round((completedChapters / totalChapters) * 100);

    if (course) {
      updateCourseProgress(course.id, newProgress);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading course...</p>
        </div>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Course not found</h2>
          <Link href="/courses">
            <Button>Back to Courses</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sky-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link href="/courses" className="text-blue-600 hover:text-blue-800 mb-4 inline-block">
          &larr; Back to Courses
        </Link>

        <div className="bg-white rounded-lg shadow-md overflow-hidden mb-6">
          <img
            src={course.thumbnail}
            alt={course.title}
            className="w-full h-80 object-contain bg-gradient-to-br from-green-100 via-white to-blue-100"
          />

          <div className="p-6">
            <div className="flex flex-wrap justify-between items-start mb-4">
              <h1 className="text-3xl font-bold text-gray-900 mr-4">{course.title}</h1>
              <span className={`text-sm px-3 py-1 rounded-full ${getLevelColor(course.level)}`}>
                {course.level}
              </span>
            </div>

            <p className="text-gray-600 mb-4">{course.description}</p>

            <div className="flex flex-wrap gap-4 mb-6">
              <div>
                <span className="text-sm text-gray-500">Instructor</span>
                <p className="font-medium">{course.instructor}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Duration</span>
                <p className="font-medium">{course.duration}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Progress</span>
                <p className="font-medium">{course.progress}%</p>
              </div>
            </div>

            <div className="mb-6">
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full"
                  style={{ width: `${course.progress}%` }}
                ></div>
              </div>
            </div>

            <div className="flex flex-wrap gap-3">
              {/* All courses are FREE for testing! */}
              <Link href={`/courses/${course.id}/chapter/1`}>
                <Button className="bg-green-600 hover:bg-green-700">
                  {course.progress > 0 ? '▶ Continue Learning' : '🚀 Start Learning FREE'}
                </Button>
              </Link>

              <Button variant="outline">📚 Bookmark</Button>
              <Button variant="outline">🔗 Share</Button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Course Content</h2>

          <div className="space-y-4">
            {course.chapters.map((chapter) => (
              <Link
                key={chapter.id}
                href={`/courses/${course.id}/chapter/${chapter.id}`}
                className={`flex items-center justify-between p-4 rounded-lg border hover:shadow-md transition-shadow cursor-pointer ${
                  chapter.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200 hover:border-sky-300'
                }`}
                onClick={() => handleChapterClick(chapter.id)}
              >
                <div className="flex items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-4 ${
                    chapter.completed ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-700'
                  }`}>
                    {chapter.completed ? '✓' : parseInt(chapter.id)}
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{chapter.title}</h3>
                    <p className="text-sm text-gray-500">{chapter.duration}</p>
                  </div>
                </div>

                <div className={`px-4 py-2 rounded-md ${
                  chapter.completed ? 'bg-green-500 text-white' : 'bg-sky-500 text-white'
                }`}>
                  {chapter.completed ? 'Completed' : 'Start'}
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}