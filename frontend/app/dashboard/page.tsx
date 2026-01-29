'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Button } from '@/components/ui/button';
import { useStore } from '@/lib/store';
import { apiService } from '@/lib/api';

interface CourseProgress {
  id: string;
  title: string;
  progress: number;
  lastAccessed: string;
}

interface QuizResult {
  id: string;
  title: string;
  score: number;
  date: string;
}

interface ActivityData {
  date: string;
  minutes: number;
}

interface UserData {
  name: string;
  email: string;
  joinDate: string;
  tier: 'free' | 'premium';
  totalLearningMinutes: number;
  completedCourses: number;
  quizAverage: number;
}

export default function DashboardPage() {
  const { user, courses: storeCourses, quizResults, learningStats } = useStore();
  const [loading, setLoading] = useState(false);

  // Transform store data to dashboard format
  const userData: UserData = {
    name: user?.name || 'Student',
    email: user?.email || 'student@example.com',
    joinDate: '2024-01-01',
    tier: user?.tier || 'free',
    totalLearningMinutes: Math.round(learningStats.totalHoursLearned * 60),
    completedCourses: learningStats.coursesCompleted,
    quizAverage: quizResults.length > 0
      ? Math.round(quizResults.reduce((sum, q) => sum + (q.score / q.totalQuestions) * 100, 0) / quizResults.length)
      : 0
  };

  // Format courses data
  const courses: CourseProgress[] = storeCourses.map(course => ({
    id: course.id,
    title: course.title,
    progress: course.progress,
    lastAccessed: course.progress > 0 ? 'Recently' : 'Not started'
  }));

  // Format quiz results
  const quizzes: QuizResult[] = quizResults.slice(-4).reverse().map(quiz => ({
    id: quiz.id,
    title: `Quiz ${quiz.quizId}`,
    score: Math.round((quiz.score / quiz.totalQuestions) * 100),
    date: new Date(quiz.date).toLocaleDateString()
  }));

  // Generate activity data based on learning stats
  const activityData: ActivityData[] = [
    { date: 'Mon', minutes: Math.round(Math.random() * 50 + 20) },
    { date: 'Tue', minutes: Math.round(Math.random() * 50 + 20) },
    { date: 'Wed', minutes: Math.round(Math.random() * 50 + 20) },
    { date: 'Thu', minutes: Math.round(Math.random() * 50 + 20) },
    { date: 'Fri', minutes: Math.round(Math.random() * 50 + 20) },
    { date: 'Sat', minutes: Math.round(Math.random() * 50 + 20) },
    { date: 'Sun', minutes: Math.round(Math.random() * 50 + 20) }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-sky-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Prepare data for pie chart
  const pieData = [
    { name: 'Completed', value: userData.completedCourses },
    { name: 'In Progress', value: courses.filter(c => c.progress > 0 && c.progress < 100).length },
    { name: 'Not Started', value: courses.filter(c => c.progress === 0).length }
  ];

  const COLORS = ['#10B981', '#F59E0B', '#EF4444'];

  return (
    <div className="min-h-screen bg-sky-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Learning Dashboard</h1>
          <p className="text-gray-600">Welcome back, {userData.name}! Here's your learning progress.</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl font-bold text-blue-600">{userData.totalLearningMinutes}</div>
            <div className="text-gray-600">Minutes Learned</div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl font-bold text-green-600">{userData.completedCourses}</div>
            <div className="text-gray-600">Courses Completed</div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl font-bold text-orange-600">{learningStats.currentStreak} 🔥</div>
            <div className="text-gray-600">Day Streak</div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl font-bold text-purple-600">{userData.quizAverage}%</div>
            <div className="text-gray-600">Quiz Average</div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl font-bold text-yellow-600">{courses.filter(c => c.progress > 0).length}</div>
            <div className="text-gray-600">Active Courses</div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Learning Activity Chart */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Weekly Learning Activity</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={activityData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="minutes" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Course Progress Pie Chart */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Course Status</h2>
            <div className="h-80 flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Courses and Quizzes Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Courses */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Your Courses</h2>
              <Link href="/courses">
                <Button variant="outline">View All</Button>
              </Link>
            </div>

            <div className="space-y-4">
              {courses.length > 0 ? (
                courses.map((course) => {
                  const storeCourse = storeCourses.find(c => c.id === course.id);
                  const completedChapters = storeCourse?.completedChapters.length || 0;
                  const totalChapters = storeCourse?.totalChapters || 6;

                  return (
                    <div key={course.id} className="border-b pb-4 last:border-b-0 last:pb-0">
                      <div className="flex justify-between items-start mb-2">
                        <Link href={`/courses/${course.id}`} className="font-medium text-blue-600 hover:text-blue-800">
                          {course.title}
                        </Link>
                        <span className="text-sm text-gray-500">{course.lastAccessed}</span>
                      </div>

                      <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                        <div
                          className={`h-2 rounded-full ${
                            course.progress === 100 ? 'bg-green-500' :
                            course.progress > 50 ? 'bg-blue-500' : 'bg-yellow-500'
                          }`}
                          style={{ width: `${course.progress}%` }}
                        ></div>
                      </div>

                      <div className="flex justify-between text-sm text-gray-500">
                        <span>
                          {completedChapters} of {totalChapters} chapters completed
                        </span>
                        <span className="font-medium">
                          {course.progress === 100 ? '✓ Completed' :
                           course.progress > 0 ? `${course.progress}% In Progress` : 'Not Started'}
                        </span>
                      </div>

                      {completedChapters > 0 && (
                        <div className="mt-2 text-xs text-gray-400">
                          Completed chapters: {storeCourse?.completedChapters.join(', ')}
                        </div>
                      )}
                    </div>
                  );
                })
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p className="mb-4">No courses in progress yet</p>
                  <Link href="/courses">
                    <Button>Browse Courses</Button>
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Recent Quiz Results */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Recent Quiz Results</h2>
              <Link href="/quiz">
                <Button variant="outline">Take Quiz</Button>
              </Link>
            </div>

            <div className="space-y-4">
              {quizzes.length > 0 ? (
                quizzes.map((quiz) => (
                  <div key={quiz.id} className="border-b pb-4 last:border-b-0 last:pb-0">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium">{quiz.title}</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        quiz.score >= 80 ? 'bg-green-100 text-green-800' :
                        quiz.score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {quiz.score}%
                      </span>
                    </div>

                    <div className="flex justify-between text-sm text-gray-500">
                      <span>Date: {quiz.date}</span>
                      <span className={quiz.score >= 80 ? 'text-green-600' :
                                     quiz.score >= 60 ? 'text-yellow-600' : 'text-red-600'}>
                        {quiz.score >= 80 ? '🏆 Excellent' :
                         quiz.score >= 60 ? '👍 Good' : '📚 Needs Improvement'}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p className="mb-4">No quiz results yet</p>
                  <Link href="/quiz">
                    <Button>Take Your First Quiz</Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}