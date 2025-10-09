// Type definitions for the TaskFlow application

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

export interface TaskCreate {
  title: string
  description?: string
  status?: 'todo' | 'in_progress' | 'done'
  priority?: 'low' | 'medium' | 'high'
  assignee?: string
}

export interface TaskUpdate extends Partial<TaskCreate> {}

// Component prop interfaces
export interface TaskCardProps {
  task: Task
  onUpdate?: (taskId: string, updates: TaskUpdate) => void
  onDelete?: (taskId: string) => void
}

export interface TaskFormProps {
  onSubmit?: (task: TaskCreate) => void
  initialData?: Partial<TaskCreate>
}