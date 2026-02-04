'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, DollarSign, Zap } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface UsageStats {
  totalTokens: number;
  totalCost: number;
  messagesCount: number;
}

interface AIChatProps {
  context?: {
    courseContent?: string;
    currentChapter?: string;
    studentLevel?: 'beginner' | 'intermediate' | 'advanced';
  };
  skill?: 'concept-explainer' | 'quiz-master' | 'socratic-tutor' | 'progress-motivator';
}

export default function AIChat({ context, skill }: AIChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState<UsageStats>({
    totalTokens: 0,
    totalCost: 0,
    messagesCount: 0,
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [...messages, userMessage].map((m) => ({
            role: m.role,
            content: m.content,
          })),
          context,
          useSkill: skill,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.message,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Update stats
      setStats((prev) => ({
        totalTokens: prev.totalTokens + data.usage.total_tokens,
        totalCost: prev.totalCost + data.cost.amount,
        messagesCount: prev.messagesCount + 1,
      }));
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Header with Stats */}
      <div className="p-4 border-b bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-lg font-semibold text-gray-800">
              AI Tutor {skill && `- ${skill.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}`}
            </h2>
            <p className="text-sm text-gray-600">Powered by GPT-4o-mini</p>
          </div>
          <div className="flex gap-4 text-sm">
            <div className="flex items-center gap-1 bg-white px-3 py-1 rounded-full">
              <Zap className="w-4 h-4 text-yellow-500" />
              <span className="font-mono">{stats.totalTokens.toLocaleString()}</span>
              <span className="text-gray-500">tokens</span>
            </div>
            <div className="flex items-center gap-1 bg-white px-3 py-1 rounded-full">
              <DollarSign className="w-4 h-4 text-green-500" />
              <span className="font-mono">${stats.totalCost.toFixed(4)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg font-medium mb-2">Start a conversation!</p>
            <p className="text-sm">Ask me anything about the course content.</p>
            <div className="mt-4 grid grid-cols-2 gap-2 max-w-md mx-auto">
              <button
                onClick={() => setInput("What is MCP?")}
                className="p-2 text-sm bg-blue-50 hover:bg-blue-100 rounded-lg text-left"
              >
                "What is MCP?"
              </button>
              <button
                onClick={() => setInput("Explain Claude SDK")}
                className="p-2 text-sm bg-blue-50 hover:bg-blue-100 rounded-lg text-left"
              >
                "Explain Claude SDK"
              </button>
              <button
                onClick={() => setInput("Quiz me on basics")}
                className="p-2 text-sm bg-blue-50 hover:bg-blue-100 rounded-lg text-left"
              >
                "Quiz me on basics"
              </button>
              <button
                onClick={() => setInput("Show my progress")}
                className="p-2 text-sm bg-blue-50 hover:bg-blue-100 rounded-lg text-left"
              >
                "Show my progress"
              </button>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3 flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm text-gray-600">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-gray-50">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything..."
            className="flex-1 resize-none rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={2}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className="px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Cost per message: ~$0.0001-0.0005 • Press Enter to send
        </p>
      </div>
    </div>
  );
}
