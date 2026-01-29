// lib/store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
  tier: 'free' | 'premium';
}

interface Course {
  id: string;
  title: string;
  description: string;
  progress: number;
  completedChapters: string[];
  totalChapters: number;
}

interface QuizResult {
  id: string;
  quizId: string;
  score: number;
  totalQuestions: number;
  date: string;
}

interface LearningStats {
  totalHoursLearned: number;
  coursesCompleted: number;
  currentStreak: number;
  lastActivityDate: string;
}

interface Store {
  user: User | null;
  courses: Course[];
  quizResults: QuizResult[];
  learningStats: LearningStats;
  loading: boolean;

  // User methods
  setUser: (user: User) => void;
  clearUser: () => void;

  // Course methods
  setCourses: (courses: Course[]) => void;
  updateCourseProgress: (courseId: string, progress: number) => void;
  markChapterComplete: (courseId: string, chapterId: string) => void;

  // Quiz methods
  addQuizResult: (result: QuizResult) => void;

  // Stats methods
  updateLearningTime: (hours: number) => void;
  updateStreak: () => void;

  setLoading: (loading: boolean) => void;
}

export const useStore = create<Store>()(
  persist(
    (set, get) => ({
      user: {
        id: '1',
        name: 'Student',
        email: 'student@example.com',
        tier: 'free'
      },
      courses: [
        {
          id: '1',
          title: 'Introduction to AI Agents',
          description: 'Learn the fundamentals of building AI agents',
          progress: 0,
          completedChapters: [],
          totalChapters: 6
        },
        {
          id: '2',
          title: 'Cloud-Native Python Development',
          description: 'Master cloud-native development with Python',
          progress: 0,
          completedChapters: [],
          totalChapters: 6
        },
        {
          id: '3',
          title: 'Generative AI Fundamentals',
          description: 'Explore the foundations of generative AI',
          progress: 0,
          completedChapters: [],
          totalChapters: 6
        },
        {
          id: '4',
          title: 'Modern Python with Typing',
          description: 'Advanced Python programming with type hints',
          progress: 0,
          completedChapters: [],
          totalChapters: 6
        }
      ],
      quizResults: [],
      learningStats: {
        totalHoursLearned: 0,
        coursesCompleted: 0,
        currentStreak: 0,
        lastActivityDate: new Date().toISOString()
      },
      loading: false,

      setUser: (user) => set({ user }),

      clearUser: () => set({ user: null }),

      setCourses: (courses) => set({ courses }),

      updateCourseProgress: (courseId, progress) => {
        set((state) => ({
          courses: state.courses.map(course =>
            course.id === courseId ? { ...course, progress } : course
          ),
        }));

        // Update stats
        const state = get();
        const course = state.courses.find(c => c.id === courseId);
        if (course && course.progress === 100) {
          set((state) => ({
            learningStats: {
              ...state.learningStats,
              coursesCompleted: state.learningStats.coursesCompleted + 1
            }
          }));
        }
      },

      markChapterComplete: (courseId, chapterId) => {
        set((state) => {
          const courses = state.courses.map(course => {
            if (course.id === courseId) {
              const completedChapters = [...course.completedChapters];
              if (!completedChapters.includes(chapterId)) {
                completedChapters.push(chapterId);
              }
              const progress = Math.round((completedChapters.length / course.totalChapters) * 100);
              return { ...course, completedChapters, progress };
            }
            return course;
          });

          return { courses };
        });

        // Update learning time (assume 20 minutes per chapter)
        get().updateLearningTime(0.33);
        get().updateStreak();
      },

      addQuizResult: (result) => {
        set((state) => ({
          quizResults: [...state.quizResults, result]
        }));
        get().updateStreak();
      },

      updateLearningTime: (hours) => {
        set((state) => ({
          learningStats: {
            ...state.learningStats,
            totalHoursLearned: state.learningStats.totalHoursLearned + hours
          }
        }));
      },

      updateStreak: () => {
        set((state) => {
          const today = new Date().toDateString();
          const lastActivity = new Date(state.learningStats.lastActivityDate).toDateString();
          const yesterday = new Date(Date.now() - 86400000).toDateString();

          let newStreak = state.learningStats.currentStreak;

          if (today !== lastActivity) {
            if (lastActivity === yesterday) {
              newStreak += 1;
            } else if (lastActivity !== today) {
              newStreak = 1;
            }
          }

          return {
            learningStats: {
              ...state.learningStats,
              currentStreak: newStreak,
              lastActivityDate: new Date().toISOString()
            }
          };
        });
      },

      setLoading: (loading) => set({ loading }),
    }),
    {
      name: 'course-companion-storage',
    }
  )
);
