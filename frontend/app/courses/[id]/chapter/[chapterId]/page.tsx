'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import { useStore } from '@/lib/store';

interface ChapterContent {
  id: string;
  title: string;
  duration: string;
  content: string;
  completed: boolean;
}

export default function ChapterPage() {
  const { id: courseId, chapterId } = useParams();
  const router = useRouter();
  const { courses, markChapterComplete } = useStore();
  const [chapter, setChapter] = useState<ChapterContent | null>(null);
  const [loading, setLoading] = useState(true);

  // Get current course to check chapter completion
  const currentCourse = courses.find(c => c.id === courseId);
  const isCompleted = currentCourse?.completedChapters.includes(chapterId as string) || false;

  useEffect(() => {
    // Map chapter IDs to concept files by course
    const conceptMaps: Record<string, Record<string, string>> = {
      '1': {  // AI Agents course
        '1': '01-introduction-to-concepts',
        '2': '02-getting-started',
        '3': '03-core-principles',
        '4': '04-practical-applications',
        '5': '05-advanced-techniques',
        '6': '06-final-project'
      },
      '2': {  // Cloud-Native Python course
        '1': '01-introduction-cloud-native',
        '2': '02-building-cloud-apis',
        '3': '03-databases-and-storage',
        '4': '04-kubernetes-deployment',
        '5': '05-monitoring-observability',
        '6': '06-production-best-practices'
      },
      '3': {  // Generative AI Fundamentals (placeholder - uses AI Agents content for now)
        '1': '01-introduction-to-concepts',
        '2': '02-getting-started',
        '3': '03-core-principles',
        '4': '04-practical-applications',
        '5': '05-advanced-techniques',
        '6': '06-final-project'
      },
      '4': {  // Modern Python (placeholder - uses AI Agents content for now)
        '1': '01-introduction-to-concepts',
        '2': '02-getting-started',
        '3': '03-core-principles',
        '4': '04-practical-applications',
        '5': '05-advanced-techniques',
        '6': '06-final-project'
      }
    };

    const courseMap = conceptMaps[courseId as string] || conceptMaps['1'];
    const conceptFile = courseMap[chapterId as string];

    if (conceptFile) {
      // Fetch the concept content
      fetch(`/concepts/${conceptFile}.md`)
        .then(res => res.text())
        .then(content => {
          setChapter({
            id: chapterId as string,
            title: content.split('\n')[0].replace('# ', ''),
            duration: chapterId === '1' ? '15 min' :
                     chapterId === '2' ? '25 min' :
                     chapterId === '3' ? '30 min' :
                     chapterId === '4' ? '40 min' :
                     chapterId === '5' ? '35 min' : '45 min',
            content: content,
            completed: isCompleted
          });
          setLoading(false);
        })
        .catch(error => {
          console.error('Error loading chapter:', error);
          setLoading(false);
        });
    }
  }, [courseId, chapterId, isCompleted]);

  const handleMarkComplete = () => {
    if (courseId && chapterId) {
      markChapterComplete(courseId as string, chapterId as string);
      // Update local state
      if (chapter) {
        setChapter({ ...chapter, completed: true });
      }
    }
  };

  const handleTakeNotes = () => {
    // For now, just alert - can be expanded later
    alert('Notes feature coming soon! You can use a separate notepad for now.');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-sky-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading chapter...</p>
        </div>
      </div>
    );
  }

  if (!chapter) {
    return (
      <div className="min-h-screen bg-sky-100 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Chapter not found</h2>
          <Link
            href={`/courses/${courseId}`}
            className="text-sky-600 hover:text-sky-800"
          >
            Back to Course
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sky-100">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation */}
        <div className="mb-6">
          <Link
            href={`/courses/${courseId}`}
            className="text-sky-600 hover:text-sky-800 inline-flex items-center"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Back to Course
          </Link>
        </div>

        {/* Chapter Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">{chapter.title}</h1>
            <span className="text-sm text-gray-500 bg-sky-100 px-3 py-1 rounded-full">
              {chapter.duration}
            </span>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={handleMarkComplete}
              disabled={isCompleted}
              className={`px-4 py-2 rounded-md transition ${
                isCompleted
                  ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                  : 'bg-green-500 text-white hover:bg-green-600'
              }`}
            >
              {isCompleted ? '✓ Completed' : 'Mark as Complete'}
            </button>
            <button
              onClick={handleTakeNotes}
              className="px-4 py-2 bg-sky-500 text-white rounded-md hover:bg-sky-600 transition"
            >
              Take Notes
            </button>
          </div>
        </div>

        {/* Chapter Content */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <article className="prose prose-lg max-w-none
            prose-headings:text-gray-900
            prose-h1:text-3xl prose-h1:font-bold prose-h1:mb-4
            prose-h2:text-2xl prose-h2:font-bold prose-h2:mt-8 prose-h2:mb-4 prose-h2:text-sky-700
            prose-h3:text-xl prose-h3:font-semibold prose-h3:mt-6 prose-h3:mb-3 prose-h3:text-sky-600
            prose-p:text-gray-700 prose-p:leading-relaxed prose-p:mb-4
            prose-a:text-sky-600 prose-a:no-underline hover:prose-a:underline
            prose-strong:text-gray-900 prose-strong:font-semibold
            prose-code:bg-gray-100 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:text-pink-600
            prose-pre:bg-gray-900 prose-pre:text-gray-100 prose-pre:p-4 prose-pre:rounded-lg prose-pre:overflow-x-auto
            prose-ul:list-disc prose-ul:pl-6 prose-ul:mb-4
            prose-ol:list-decimal prose-ol:pl-6 prose-ol:mb-4
            prose-li:text-gray-700 prose-li:mb-2
            prose-blockquote:border-l-4 prose-blockquote:border-sky-500 prose-blockquote:pl-4 prose-blockquote:italic prose-blockquote:text-gray-600
            prose-img:rounded-lg prose-img:shadow-md
          ">
            <ReactMarkdown>{chapter.content}</ReactMarkdown>
          </article>
        </div>

        {/* Navigation Footer */}
        <div className="mt-6 flex justify-between items-center bg-white rounded-lg shadow-md p-6">
          {parseInt(chapterId as string) > 1 && (
            <Link
              href={`/courses/${courseId}/chapter/${parseInt(chapterId as string) - 1}`}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
            >
              ← Previous Chapter
            </Link>
          )}
          {parseInt(chapterId as string) < 6 && (
            <Link
              href={`/courses/${courseId}/chapter/${parseInt(chapterId as string) + 1}`}
              className="ml-auto px-4 py-2 bg-sky-500 text-white rounded-md hover:bg-sky-600 transition"
            >
              Next Chapter →
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
