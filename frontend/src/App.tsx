import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './lib/api';
import { Task, TaskStatus, TaskCreate, TaskUpdate } from './types/index';
import { KanbanBoard } from './components/KanbanBoard';
import { TaskForm } from './components/TaskForm';

function App() {
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const queryClient = useQueryClient();

  // Fetch all tasks
  const { data: tasks = [], isLoading, error } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => api.getTasks(),
  });

  // Mutations
  const createTaskMutation = useMutation({
    mutationFn: (taskData: TaskCreate) => api.createTask(taskData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setShowTaskForm(false);
    },
  });

  const updateTaskMutation = useMutation({
    mutationFn: ({ taskId, updates }: { taskId: string; updates: TaskUpdate }) =>
      api.updateTask(taskId, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setEditingTask(null);
    },
  });

  const deleteTaskMutation = useMutation({
    mutationFn: (taskId: string) => api.deleteTask(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // Handle task status updates (drag and drop)
  const handleStatusUpdate = useCallback((taskId: string, newStatus: TaskStatus) => {
    updateTaskMutation.mutate({ taskId, updates: { status: newStatus } });
  }, [updateTaskMutation]);

  // Handle form submission
  const handleTaskSubmit = useCallback((taskData: TaskCreate) => {
    createTaskMutation.mutate(taskData);
  }, [createTaskMutation]);

  const handleTaskEdit = useCallback((taskData: TaskUpdate, taskId: string) => {
    updateTaskMutation.mutate({ taskId, updates: taskData });
  }, [updateTaskMutation]);

  const handleDeleteTask = useCallback((taskId: string) => {
    deleteTaskMutation.mutate(taskId);
  }, [deleteTaskMutation]);

  const handleEditTask = useCallback((task: Task) => {
    setEditingTask(task);
  }, []);

  const handleFormCancel = useCallback(() => {
    setShowTaskForm(false);
    setEditingTask(null);
  }, []);

  const handleCreateTask = useCallback(() => {
    setShowTaskForm(true);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading TaskFlow...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md p-8 bg-white rounded-lg shadow-lg">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Connection Error</h2>
            <p className="text-gray-600 mb-4">
              Unable to connect to the backend API. Make sure the backend server is running.
            </p>
            <div className="bg-gray-100 p-4 rounded text-sm font-mono text-left">
              <p>1. Start the backend: <code className="text-blue-600">cd backend && uv run uvicorn src.app:app --reload</code></p>
              <p>2. Refresh this page</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">TaskFlow</h1>
              <p className="text-gray-600 mt-1">Kanban-style task management</p>
            </div>
            <button
              onClick={handleCreateTask}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
            >
              + New Task
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {tasks.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">📋</div>
            <h3 className="text-xl font-medium text-gray-900 mb-2">No tasks yet</h3>
            <p className="text-gray-500 mb-6">Get started by creating your first task!</p>
            <button
              onClick={handleCreateTask}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md font-medium"
            >
              Create Your First Task
            </button>
          </div>
        ) : (
          <KanbanBoard
            tasks={tasks}
            onStatusUpdate={handleStatusUpdate}
            onEditTask={handleEditTask}
            onDeleteTask={handleDeleteTask}
          />
        )}
      </main>

      {/* Task Form Modal */}
      {(showTaskForm || editingTask) && (
        <TaskForm
          task={editingTask}
          onSubmit={(taskData) => {
            if (editingTask) {
              handleTaskEdit(taskData, editingTask.id);
            } else {
              handleTaskSubmit(taskData);
            }
          }}
          onCancel={handleFormCancel}
          isLoading={createTaskMutation.isPending || updateTaskMutation.isPending}
        />
      )}
    </div>
  );
}

export default App;