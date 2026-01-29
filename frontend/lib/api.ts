// lib/api.ts
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = BACKEND_URL;
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken');
    }
    return null;
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const token = this.getAuthToken();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Clear auth token if unauthorized
        if (typeof window !== 'undefined') {
          localStorage.removeItem('authToken');
        }
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Handle empty responses
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    } else {
      return response.text();
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return data
      ? this.request(endpoint, { method: 'POST', body: JSON.stringify(data) })
      : this.request(endpoint, { method: 'POST' });
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Specific API endpoints for different features
class ApiService {
  private apiClient: ApiClient;

  constructor() {
    this.apiClient = new ApiClient();
  }

  // Authentication APIs
  async login(credentials: { email: string; password: string }) {
    return this.apiClient.post('/auth/login', credentials);
  }

  async register(userData: { name: string; email: string; password: string }) {
    return this.apiClient.post('/auth/register', userData);
  }

  async logout() {
    return this.apiClient.post('/auth/logout');
  }

  async getUserProfile() {
    return this.apiClient.get('/auth/profile');
  }

  async forgotPassword(email: string) {
    return this.apiClient.post('/auth/forgot-password', { email });
  }

  async resetPassword(token: string, newPassword: string) {
    return this.apiClient.post('/auth/reset-password', { token, newPassword });
  }

  // Course APIs
  async getCourses() {
    return this.apiClient.get('/courses');
  }

  async getCourse(courseId: string) {
    return this.apiClient.get(`/courses/${courseId}`);
  }

  async getCourseContent(courseId: string) {
    return this.apiClient.get(`/courses/${courseId}/content`);
  }

  async updateCourseProgress(courseId: string, progress: number) {
    return this.apiClient.put(`/courses/${courseId}/progress`, { progress });
  }

  // Quiz APIs
  async getQuizzes() {
    return this.apiClient.get('/quizzes');
  }

  async getQuiz(quizId: string) {
    return this.apiClient.get(`/quizzes/${quizId}`);
  }

  async submitQuiz(quizId: string, answers: any[]) {
    return this.apiClient.post(`/quizzes/${quizId}/submit`, { answers });
  }

  async getQuizResults(quizId: string) {
    return this.apiClient.get(`/quizzes/${quizId}/results`);
  }

  // User APIs
  async updateUserProfile(profileData: any) {
    return this.apiClient.put('/auth/profile', profileData);
  }

  async getUserProgress() {
    return this.apiClient.get('/users/progress');
  }

  async getUserAnalytics() {
    return this.apiClient.get('/users/analytics');
  }

  // Content APIs
  async getContent(searchQuery: string) {
    return this.apiClient.get(`/content/search?q=${encodeURIComponent(searchQuery)}`);
  }

  async getChapterContent(courseId: string, chapterId: string) {
    return this.apiClient.get(`/courses/${courseId}/chapters/${chapterId}/content`);
  }
}

export const apiService = new ApiService();