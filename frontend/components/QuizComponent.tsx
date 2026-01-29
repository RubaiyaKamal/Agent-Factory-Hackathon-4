'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

interface Question {
  id: string;
  text: string;
  options: string[];
  correctAnswer: number;
  explanation?: string;
}

interface QuizComponentProps {
  questions: Question[];
  onComplete: (score: number, total: number) => void;
}

export default function QuizComponent({ questions, onComplete }: QuizComponentProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<(number | null)[]>(Array(questions.length).fill(null));
  const [showResults, setShowResults] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const currentQuestion = questions[currentQuestionIndex];
  const selectedAnswer = selectedAnswers[currentQuestionIndex];

  const handleAnswerSelect = (optionIndex: number) => {
    if (showResults) return;

    const newAnswers = [...selectedAnswers];
    newAnswers[currentQuestionIndex] = optionIndex;
    setSelectedAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = () => {
    setIsSubmitting(true);

    // Calculate score
    let score = 0;
    selectedAnswers.forEach((answer, index) => {
      if (answer === questions[index].correctAnswer) {
        score++;
      }
    });

    setIsSubmitting(false);
    setShowResults(true);
    onComplete(score, questions.length);
  };

  const handleRestart = () => {
    setCurrentQuestionIndex(0);
    setSelectedAnswers(Array(questions.length).fill(null));
    setShowResults(false);
  };

  if (showResults) {
    const score = selectedAnswers.reduce((acc: number, answer, index) => {
      return answer === questions[index].correctAnswer ? acc + 1 : acc;
    }, 0);

    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quiz Results</h2>

        <div className="text-center mb-8">
          <div className="text-5xl font-bold text-blue-600 mb-2">
            {score}/{questions.length}
          </div>
          <div className="text-lg text-gray-600">
            {Math.round((score / questions.length) * 100)}% Correct
          </div>

          <div className="mt-4">
            {score / questions.length >= 0.7 ? (
              <div className="text-green-600 font-medium">Well done! You passed the quiz.</div>
            ) : (
              <div className="text-yellow-600 font-medium">Keep practicing to improve your knowledge.</div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          {questions.map((question, qIndex) => {
            const userAnswer = selectedAnswers[qIndex];
            const isCorrect = userAnswer === question.correctAnswer;

            return (
              <div key={question.id} className={`p-4 rounded-lg border ${isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                <h3 className="font-medium text-gray-900 mb-2">Question {qIndex + 1}: {question.text}</h3>

                <div className="mb-2">
                  <p className="text-sm font-medium">Your answer: {userAnswer !== null ? question.options[userAnswer] : 'No answer'}</p>
                  {!isCorrect && (
                    <p className="text-sm font-medium text-green-600">Correct answer: {question.options[question.correctAnswer]}</p>
                  )}
                </div>

                {question.explanation && (
                  <p className="text-sm text-gray-600">{question.explanation}</p>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-8 flex justify-center">
          <Button onClick={handleRestart}>Retake Quiz</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Quiz</h2>
        <div className="text-sm text-gray-500">
          Question {currentQuestionIndex + 1} of {questions.length}
        </div>
      </div>

      <div className="mb-2">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full"
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>
      </div>

      <h3 className="text-lg font-medium text-gray-900 mb-6">{currentQuestion.text}</h3>

      <div className="space-y-3 mb-8">
        {currentQuestion.options.map((option, optionIndex) => (
          <div
            key={optionIndex}
            className={`p-4 rounded-lg border cursor-pointer transition-colors ${
              selectedAnswer === optionIndex
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => handleAnswerSelect(optionIndex)}
          >
            <div className="flex items-center">
              <div className={`w-6 h-6 rounded-full border flex items-center justify-center mr-3 ${
                selectedAnswer === optionIndex
                  ? 'border-blue-500 bg-blue-500 text-white'
                  : 'border-gray-300'
              }`}>
                {String.fromCharCode(65 + optionIndex)}
              </div>
              <span>{option}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          Previous
        </Button>

        {currentQuestionIndex < questions.length - 1 ? (
          <Button
            onClick={handleNext}
            disabled={selectedAnswer === null}
          >
            Next
          </Button>
        ) : (
          <Button
            onClick={handleSubmit}
            disabled={selectedAnswer === null || isSubmitting}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Quiz'}
          </Button>
        )}
      </div>
    </div>
  );
}