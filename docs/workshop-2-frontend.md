# Workshop 2: React Frontend & API Integration

**Duration**: 2.5 hours
**Branch**: Based on workshop 1 completion
**Level**: Intermediate
**Prerequisites**: Workshop 1 (backend API) completed

## 🎯 Objectives

By the end of this workshop, you will be able to:
- Set up a modern React application with TypeScript
- Implement responsive components with Tailwind CSS
- Connect frontend to backend API with proper error handling
- Manage component state and data flow
- Write React tests with Vitest
- Implement basic CRUD operations in the UI

## 📋 Prerequisites

### Completed Workshop 1 Requirements
- ✅ Backend API running with FastAPI
- ✅ Task management endpoints implemented
- ✅ GitHub repository with CI/CD setup

### Additional Requirements
- ✅ **Node.js 18+** and **npm** installed
- ✅ Basic JavaScript/TypeScript knowledge
- ✅ Understanding of React concepts

### Tool Installation Check
```bash
# Verify tools
node --version      # Should show v18.x.x
npm --version       # Should show current version

# Test the backend API (make sure it's running)
curl http://localhost:8000/
```

## 🚀 Getting Started

### 1. Setup Frontend Project

The frontend project structure should already be set up. Navigate to it:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 2. Verify Backend Connection

Make sure your backend API is running:

```bash
# In another terminal, start the backend
cd backend
uv run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Test the connection:

```bash
# Test backend API
curl http://localhost:8000/
curl http://localhost:8000/tasks
```

## 📚 Workshop Structure

This workshop builds the frontend UI on top of your backend API:

### React Basics (30 min)
- Project structure overview
- Component architecture
- State management basics

### UI Layout & Styling (60 min)
- Responsive design with Tailwind CSS
- Header and navigation
- Main layout components

### Task Management Interface (60 min)
- Task form for creating tasks
- Task list with filtering
- Task card components

### API Integration (30 min)
- HTTP client setup
- Error handling
- Loading states

---

## 🎨 Part 1: React Project Overview (30 min)

### Understanding the Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── types/         # TypeScript type definitions
│   ├── index.css      # Global styles (Tailwind)
│   ├── main.tsx       # App entry point
│   └── App.tsx        # Main app component
├── public/
├── package.json
├── vite.config.ts     # Vite configuration
└── tailwind.config.js # Tailwind configuration
```

### Key Technologies

- **React 18**: Modern React with functional components
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server
- **Vitest**: Unit testing framework

### Running the App

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test
```

---

## 🏗️ Part 2: UI Layout & Components (60 min)

### 2A: Main App Structure

Create the basic app layout:

```typescript
// src/App.tsx
import { TaskBoard } from './components/TaskBoard'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-2xl font-bold text-gray-900">
              TaskFlow 📋
            </h1>
            <p className="text-sm text-gray-600">
              Your Task Management Dashboard
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <TaskBoard />
      </main>
    </div>
  )
}

export default App
```

### 2B: Task Board Component

Build the main dashboard layout:

```typescript
// src/components/TaskBoard.tsx
export function TaskBoard() {
  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <span className="text-blue-600">📝</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Tasks</p>
              <p className="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <span className="text-yellow-600">⏳</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <span className="text-green-600">✅</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>
      </div>

      {/* Kanban Board Placeholder */}
      <div className="bg-white p-8 rounded-lg shadow-sm border text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Kanban Board Coming Soon
        </h3>
        <p className="text-gray-600">
          We'll build the task management interface here
        </p>
      </div>
    </div>
  )
}
```

---

## 📝 Part 3: Task Form Component (30 min)

### 3A: Task Creation Form

Create a form for adding new tasks:

```typescript
// src/components/TaskForm.tsx
import { useState } from 'react'

interface TaskFormData {
  title: string
  description: string
  status: 'todo' | 'in_progress' | 'done'
  priority: 'low' | 'medium' | 'high'
  assignee?: string
}

export function TaskForm() {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium'
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.title.trim()) return

    setIsSubmitting(true)

    try {
      // We'll implement API call here later
      console.log('Creating task:', formData)

      // Reset form
      setFormData({
        title: '',
        description: '',
        status: 'todo',
        priority: 'medium'
      })
    } catch (error) {
      console.error('Error creating task:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleChange = (field: keyof TaskFormData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }))
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">
        Create New Task
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={handleChange('title')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter task title..."
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            value={formData.description}
            onChange={handleChange('description')}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter task description..."
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={formData.status}
              onChange={handleChange('status')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="todo">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              value={formData.priority}
              onChange={handleChange('priority')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Assignee
          </label>
          <input
            type="text"
            value={formData.assignee || ''}
            onChange={handleChange('assignee')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Assign to team member..."
          />
        </div>

        <button
          type="submit"
          disabled={isSubmitting || !formData.title.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isSubmitting ? 'Creating Task...' : 'Create Task'}
        </button>
      </form>
    </div>
  )
}
```

---

## 🔗 Part 4: API Integration (30 min)

### 4A: API Client Setup

Create an API client for backend communication:

```typescript
// src/api/client.ts
const API_BASE_URL = 'http://localhost:8000'

export interface Task {
  id: string
  title: string
  description?: string
  status: 'todo' | 'in_progress' | 'done'
  priority: 'low' | 'medium' | 'high'
  assignee?: string
  created_at: string
  updated_at: string
}

export interface CreateTaskData {
  title: string
  description?: string
  status?: 'todo' | 'in_progress' | 'done'
  priority?: 'low' | 'medium' | 'high'
  assignee?: string
}

export interface UpdateTaskData extends Partial<CreateTaskData> {}

class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)

      if (!response.ok) {
        const errorMessage = await response.text()
        throw new Error(`API Error: ${response.status} - ${errorMessage}`)
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return null as T
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Task CRUD operations
  async getTasks(params?: {
    status?: string
    priority?: string
    assignee?: string
  }): Promise<Task[]> {
    const searchParams = new URLSearchParams()
    if (params?.status) searchParams.append('status', params.status)
    if (params?.priority) searchParams.append('priority', params.priority)
    if (params?.assignee) searchParams.append('assignee', params.assignee)

    const queryString = searchParams.toString()
    const endpoint = queryString ? `/tasks?${queryString}` : '/tasks'

    return this.request<Task[]>(endpoint)
  }

  async getTask(id: string): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`)
  }

  async createTask(data: CreateTaskData): Promise<Task> {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateTask(id: string, data: UpdateTaskData): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteTask(id: string): Promise<void> {
    return this.request<void>(`/tasks/${id}`, {
      method: 'DELETE',
    })
  }
}

// Create and export a default instance
export const apiClient = new ApiClient(API_BASE_URL)
```

### 4B: Using the API in Components

Update TaskForm to use the real API:

```typescript
// src/components/TaskForm.tsx (updated)
import { useState } from 'react'
import { apiClient, CreateTaskData } from '../api/client'

// ... existing code ...

export function TaskForm() {
  // ... existing state ...

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.title.trim()) return

    setIsSubmitting(true)

    try {
      // Create task through API
      await apiClient.createTask(formData)

      // Reset form
      setFormData({
        title: '',
        description: '',
        status: 'todo',
        priority: 'medium'
      })

      // Emit success event or call callback to refresh task list
      // This will be implemented when we build the task list component

    } catch (error) {
      console.error('Failed to create task:', error)
      // In a real app, show error to user
      alert('Failed to create task. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  // ... rest of form JSX ...
}
```

---

## 🧪 Part 5: Writing Tests (30 min)

### Unit Tests with Vitest

Create tests for your components:

```typescript
// src/components/__tests__/TaskForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { TaskForm } from '../TaskForm'

// Mock the API client
jest.mock('../../api/client', () => ({
  apiClient: {
    createTask: jest.fn(),
  },
}))

const { apiClient } = require('../../api/client')

describe('TaskForm', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders form fields correctly', () => {
    render(<TaskForm />)

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/priority/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/assignee/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /create task/i })).toBeInTheDocument()
  })

  it('shows validation errors for empty title', async () => {
    render(<TaskForm />)

    const submitButton = screen.getByRole('button', { name: /create task/i })

    fireEvent.click(submitButton)

    // Form should not submit without title
    await waitFor(() => {
      expect(apiClient.createTask).not.toHaveBeenCalled()
    })
  })

  it('submits form with valid data', async () => {
    const mockCreateTask = apiClient.createTask as jest.MockedFunction<any>
    mockCreateTask.mockResolvedValueOnce({})

    render(<TaskForm />)

    // Fill out form
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Test Task' }
    })

    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'Test description' }
    })

    fireEvent.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(mockCreateTask).toHaveBeenCalledWith({
        title: 'Test Task',
        description: 'Test description',
        status: 'todo',
        priority: 'medium'
      })
    })
  })

  it('shows loading state during submission', async () => {
    const mockCreateTask = apiClient.createTask as jest.MockedFunction<any>
    mockCreateTask.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

    render(<TaskForm />)

    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Test Task' }
    })

    fireEvent.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(screen.getByRole('button')).toHaveTextContent('Creating Task...')
    })
  })
})
```

### API Client Tests

```typescript
// src/api/__tests__/client.test.ts
import { apiClient, Task } from '../client'

// Mock fetch
global.fetch = jest.fn()

const mockFetch = global.fetch as jest.MockedFunction<typeof fetch>

describe('ApiClient', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  describe('getTasks', () => {
    it('fetches all tasks', async () => {
      const mockTasks: Task[] = [
        {
          id: '1',
          title: 'Test Task',
          status: 'todo',
          priority: 'medium',
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        }
      ]

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockTasks
      } as Response)

      const result = await apiClient.getTasks()

      expect(result).toEqual(mockTasks)
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/tasks',
        expect.objectContaining({
          headers: { 'Content-Type': 'application/json' }
        })
      )
    })

    it('handles query parameters', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

      await apiClient.getTasks({ status: 'todo', assignee: 'alice' })

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/tasks?status=todo&assignee=alice',
        expect.any(Object)
      )
    })
  })

  describe('createTask', () => {
    it('creates task successfully', async () => {
      const taskData = { title: 'New Task' }
      const mockResponse: Task = {
        id: '123',
        title: 'New Task',
        status: 'todo',
        priority: 'medium',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      }

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response)

      const result = await apiClient.createTask(taskData)

      expect(result).toEqual(mockResponse)
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/tasks',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(taskData)
        })
      )
    })

    it('handles API errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        text: async () => 'Bad Request'
      } as Response)

      await expect(apiClient.createTask({ title: '' })).rejects.toThrow('API Error: 400 - Bad Request')
    })
  })
})
```

---

## 🎉 Workshop 2 Complete!

### What You Built:
- ✅ **Modern React/TypeScript setup** with Vite
- ✅ **Responsive UI** with Tailwind CSS
- ✅ **API integration** with error handling
- ✅ **Component state management**
- ✅ **Unit tests** with Vitest
- ✅ **ESLint configuration** for code quality

### React Concepts Mastered:
- Component architecture and composition
- Form handling and validation
- API client implementation
- Error boundaries and loading states
- Testing with Vitest and React Testing Library
- Tailwind CSS utility classes

### Resources:
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vitest Guide](https://vitest.dev/guide/)

### Next Steps:
Now you have both backend and frontend working together! You can:
- Add more UI components (task lists, kanban board)
- Implement real-time features
- Add user authentication
- Deploy to production

---

## 📋 Assessment Criteria

- [ ] React app runs successfully
- [ ] Components render correctly
- [ ] API integration works (creates/fetches tasks)
- [ ] Error handling implemented
- [ ] Basic tests pass
- [ ] ESLint passes with no errors

---

**Questions?** Ask your instructor or check the troubleshooting guide.</content>
</xai:function_call=str_replace>

<parameter name="file_path">../docs/workshop-2-frontend.md