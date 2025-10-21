import { Task, TaskStatus } from '../types/index';

interface TaskCardProps {
  task: Task;
  onEdit: () => void;
  onDelete: () => void;
  onStatusChange?: (newStatus: TaskStatus) => void;
}

export function TaskCard({ task, onEdit, onDelete }: TaskCardProps) {

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-medium text-gray-900 flex-1 truncate pr-2">
          {task.title}
        </h3>
        <div className="flex space-x-1">
          <button
            onClick={onEdit}
            className="text-gray-400 hover:text-blue-600 transition-colors"
            title="Edit task"
          >
            ✏️
          </button>
          <button
            onClick={() => {
              if (window.confirm(`Êtes-vous sûr de vouloir supprimer "${task.title}" ?`)) {
                onDelete();
              }
            }}
            className="text-gray-400 hover:text-red-600 transition-colors"
            title="Delete task"
          >
            🗑️
          </button>
        </div>
      </div>

      {task.description && (
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="flex items-center">
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(task.priority)}`}>
          {task.priority}
        </span>
      </div>
    </div>
  );
}
