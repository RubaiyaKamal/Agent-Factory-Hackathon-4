'use client';

import { useState } from 'react';
import AIChat from '@/components/AIChat';
import { BookOpen, MessageSquare, Target, TrendingUp } from 'lucide-react';

export default function AITutorPage() {
  const [selectedSkill, setSelectedSkill] = useState<string>('concept-explainer');
  const [studentLevel, setStudentLevel] = useState<'beginner' | 'intermediate' | 'advanced'>('intermediate');

  const skills = [
    {
      id: 'concept-explainer',
      name: 'Concept Explainer',
      icon: BookOpen,
      description: 'Get clear explanations adapted to your level',
      color: 'blue',
    },
    {
      id: 'quiz-master',
      name: 'Quiz Master',
      icon: Target,
      description: 'Test your knowledge with interactive quizzes',
      color: 'green',
    },
    {
      id: 'socratic-tutor',
      name: 'Socratic Tutor',
      icon: MessageSquare,
      description: 'Learn through guided questions',
      color: 'purple',
    },
    {
      id: 'progress-motivator',
      name: 'Progress Motivator',
      icon: TrendingUp,
      description: 'Stay motivated with progress insights',
      color: 'orange',
    },
  ];

  const context = {
    courseContent: 'AI Agent Development Course - Claude SDK, MCP Servers, Agent Skills',
    currentChapter: 'Introduction to MCP',
    studentLevel,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">AI Tutor</h1>
          <p className="text-gray-600">Your personalized AI learning companion powered by GPT-4o-mini</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Skills Selection */}
          <div className="lg:col-span-1 space-y-4">
            {/* Student Level */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold text-gray-900 mb-3">Your Level</h3>
              <div className="space-y-2">
                {['beginner', 'intermediate', 'advanced'].map((level) => (
                  <button
                    key={level}
                    onClick={() => setStudentLevel(level as any)}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                      studentLevel === level
                        ? 'bg-blue-100 text-blue-700 font-medium'
                        : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Skills */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold text-gray-900 mb-3">Select Teaching Style</h3>
              <div className="space-y-2">
                {skills.map((skill) => {
                  const Icon = skill.icon;
                  return (
                    <button
                      key={skill.id}
                      onClick={() => setSelectedSkill(skill.id)}
                      className={`w-full text-left p-3 rounded-lg transition-all ${
                        selectedSkill === skill.id
                          ? 'bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-300'
                          : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                      }`}
                    >
                      <div className="flex items-start gap-2">
                        <Icon className={`w-5 h-5 mt-0.5 text-${skill.color}-600`} />
                        <div>
                          <p className="font-medium text-gray-900 text-sm">{skill.name}</p>
                          <p className="text-xs text-gray-600 mt-1">{skill.description}</p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Cost Info */}
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg shadow p-4 border border-green-200">
              <h3 className="font-semibold text-green-900 mb-2">💰 Cost Efficient</h3>
              <div className="text-sm text-green-800 space-y-1">
                <p>• $0.15 per 1M input tokens</p>
                <p>• $0.60 per 1M output tokens</p>
                <p className="font-medium mt-2">~$0.0001-0.0005 per message</p>
              </div>
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <div className="h-[calc(100vh-12rem)]">
              <AIChat
                context={context}
                skill={selectedSkill as any}
              />
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-gray-900 mb-4">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="font-medium text-blue-600 mb-1">1. Choose Your Level</p>
              <p className="text-gray-600">Select beginner, intermediate, or advanced</p>
            </div>
            <div>
              <p className="font-medium text-green-600 mb-1">2. Pick a Teaching Style</p>
              <p className="text-gray-600">Choose how you want to learn</p>
            </div>
            <div>
              <p className="font-medium text-purple-600 mb-1">3. Ask Questions</p>
              <p className="text-gray-600">Chat naturally with your AI tutor</p>
            </div>
            <div>
              <p className="font-medium text-orange-600 mb-1">4. Track Your Costs</p>
              <p className="text-gray-600">See real-time token and cost usage</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
