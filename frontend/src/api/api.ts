import { Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority } from '../types/index';

// API Base URL - will proxy to backend via Vite
const API_BASE = '/api';

// Helper function for API calls
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

// Task API functions
export const api = {
  // Get all tasks with optional filters
  async getTasks(
    status?: TaskStatus,
    priority?: TaskPriority,
    assignee?: string
  ): Promise<Task[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (priority) params.append('priority', priority);
    if (assignee) params.append('assignee', assignee);

    const query = params.toString();
    const endpoint = `/tasks${query ? `?${query}` : ''}`;

    return apiRequest<Task[]>(endpoint);
  },

  // Get single task
  async getTask(taskId: string): Promise<Task> {
    return apiRequest<Task>(`/tasks/${taskId}`);
  },

  // Create new task
  async createTask(task: TaskCreate): Promise<Task> {
    return apiRequest<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  },

  // Update existing task
  async updateTask(taskId: string, updates: TaskUpdate): Promise<Task> {
    return apiRequest<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  // Delete task
  async deleteTask(taskId: string): Promise<void> {
    await apiRequest(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },
};