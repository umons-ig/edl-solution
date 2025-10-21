import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api/api';
import { Task, TaskStatus, TaskCreate } from './types/index';
import { KanbanBoard } from './components/KanbanBoard';
import { TaskForm } from './components/TaskForm';

function App() {
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const queryClient = useQueryClient();

  // Fetch tasks
  const { data: tasks = [], isLoading, error } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => api.getTasks(),
  });

  // Create task
  const createMutation = useMutation({
    mutationFn: api.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setShowForm(false);
    },
  });

  // Update task
  const updateMutation = useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: Partial<TaskCreate> }) =>
      api.updateTask(id, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setEditingTask(null);
    },
  });

  // Delete task
  const deleteMutation = useMutation({
    mutationFn: api.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md p-8 bg-white rounded-lg shadow-lg">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Erreur de Connexion</h2>
            <p className="text-gray-600 mb-4">
              Impossible de se connecter au backend. Assurez-vous que le serveur backend est démarré.
            </p>
            <div className="bg-gray-100 p-4 rounded text-sm font-mono text-left">
              <p>1. Démarrez le backend: <code className="text-blue-600">cd backend && uv run uvicorn src.app:app --reload</code></p>
              <p>2. Rafraîchissez cette page</p>
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
              <p className="text-gray-600 mt-1">Gestion de tâches Kanban</p>
            </div>
            <button
              onClick={() => setShowForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
            >
              + Nouvelle Tâche
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {tasks.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">📋</div>
            <h3 className="text-xl font-medium text-gray-900 mb-2">Aucune tâche</h3>
            <p className="text-gray-500 mb-6">Créez votre première tâche pour commencer !</p>
            <button
              onClick={() => setShowForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md font-medium"
            >
              Créer une Tâche
            </button>
          </div>
        ) : (
          <KanbanBoard
            tasks={tasks}
            onStatusChange={(taskId: string, newStatus: TaskStatus) => {
              updateMutation.mutate({ id: taskId, updates: { status: newStatus } });
            }}
            onEdit={(task: Task) => setEditingTask(task)}
            onDelete={(taskId: string) => deleteMutation.mutate(taskId)}
          />
        )}
      </main>

      {/* Task Form Modal */}
      {(showForm || editingTask) && (
        <TaskForm
          task={editingTask}
          onSubmit={(data) => {
            if (editingTask) {
              updateMutation.mutate({ id: editingTask.id, updates: data });
            } else {
              createMutation.mutate(data);
            }
          }}
          onCancel={() => {
            setShowForm(false);
            setEditingTask(null);
          }}
          isLoading={createMutation.isPending || updateMutation.isPending}
        />
      )}
    </div>
  );
}

export default App;
