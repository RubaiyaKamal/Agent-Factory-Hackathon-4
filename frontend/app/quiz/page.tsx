'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import QuizComponent from '@/components/QuizComponent';
import { useStore } from '@/lib/store';

interface Question {
  id: string;
  text: string;
  options: string[];
  correctAnswer: number;
  explanation?: string;
}

export default function QuizPage() {
  const { addQuizResult } = useStore();
  const [quizStarted, setQuizStarted] = useState(false);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [score, setScore] = useState(0);
  const [total, setTotal] = useState(0);

  // Sample quiz questions
  const sampleQuestions: Question[] = [
    {
      id: '1',
      text: 'What is an AI agent?',
      options: [
        'A human who works with AI',
        'A software program that can perceive its environment and take actions',
        'A type of computer hardware',
        'A programming language for AI'
      ],
      correctAnswer: 1,
      explanation: 'An AI agent is a software program that can perceive its environment and take actions to achieve specific goals.'
    },
    {
      id: '2',
      text: 'Which of the following is NOT a characteristic of a good AI agent?',
      options: [
        'Autonomy',
        'Reactivity',
        'Proactiveness',
        'Rigidity'
      ],
      correctAnswer: 3,
      explanation: 'Rigidity is not a characteristic of a good AI agent. Good agents should be adaptable and flexible.'
    },
    {
      id: '3',
      text: 'What does RAG stand for in the context of AI?',
      options: [
        'Robotic Action Generation',
        'Response Augmentation Generator',
        'Retrieval-Augmented Generation',
        'Reasoning and Analysis Gateway'
      ],
      correctAnswer: 2,
      explanation: 'RAG stands for Retrieval-Augmented Generation, a technique that enhances LLMs with external knowledge.'
    },
    {
      id: '4',
      text: 'Which Python library is commonly used for building AI agents?',
      options: [
        'NumPy',
        'Pandas',
        'LangChain',
        'Matplotlib'
      ],
      correctAnswer: 2,
      explanation: 'LangChain is a popular library for developing applications powered by language models, including AI agents.'
    },
    {
      id: '5',
      text: 'What is the main advantage of cloud-native development?',
      options: [
        'Lower hardware costs',
        'Better performance on single machines',
        'Scalability and resilience',
        'Simpler debugging'
      ],
      correctAnswer: 2,
      explanation: 'Cloud-native development enables applications to be scalable, resilient, and portable across cloud environments.'
    }
  ];

  const handleQuizComplete = (score: number, total: number) => {
    setScore(score);
    setTotal(total);
    setQuizCompleted(true);

    // Save quiz result to store
    const quizResult = {
      id: `quiz-${Date.now()}`,
      quizId: 'AI Agents Quiz',
      score: score,
      totalQuestions: total,
      date: new Date().toISOString()
    };

    addQuizResult(quizResult);
  };

  if (!quizStarted) {
    return (
      <div className="min-h-screen bg-sky-100 flex items-center justify-center">
        <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Knowledge Check Quiz</h1>

          <div className="mb-6">
            <p className="text-gray-600 mb-4">
              Test your understanding of AI agents, cloud-native development, and related concepts.
            </p>

            <div className="bg-blue-50 p-4 rounded-lg mb-6 text-left">
              <h3 className="font-medium text-blue-800 mb-2">Quiz Details:</h3>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• {sampleQuestions.length} questions</li>
                <li>• Multiple choice format</li>
                <li>• Instant feedback after completion</li>
                <li>• Ability to retake the quiz</li>
              </ul>
            </div>
          </div>

          <Button onClick={() => setQuizStarted(true)}>
            Start Quiz
          </Button>
        </div>
      </div>
    );
  }

  if (quizCompleted) {
    return (
      <div className="min-h-screen bg-sky-100 flex items-center justify-center">
        <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Quiz Completed!</h1>

          <div className="mb-8">
            <div className="text-6xl font-bold text-blue-600 mb-2">
              {score}/{total}
            </div>
            <div className="text-xl text-gray-600 mb-4">
              {Math.round((score / total) * 100)}% Correct
            </div>

            {score / total >= 0.7 ? (
              <div className="text-green-600 font-medium text-lg">
                Excellent work! You have a strong understanding of the concepts.
              </div>
            ) : (
              <div className="text-yellow-600 font-medium text-lg">
                Good effort! Review the material and try again to improve your score.
              </div>
            )}
          </div>

          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/dashboard">
              <Button>
                View Dashboard
              </Button>
            </Link>

            <Button
              variant="outline"
              onClick={() => {
                setQuizStarted(false);
                setQuizCompleted(false);
              }}
            >
              Take Another Quiz
            </Button>

            <Link href="/courses">
              <Button variant="outline">
                Browse Courses
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sky-100">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link href="/courses" className="text-blue-600 hover:text-blue-800 mb-6 inline-block">
          &larr; Back to Courses
        </Link>

        <QuizComponent
          questions={sampleQuestions}
          onComplete={handleQuizComplete}
        />
      </div>
    </div>
  );
}