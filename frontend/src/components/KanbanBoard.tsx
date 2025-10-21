import { Task, TaskStatus } from '../types/index';
import { TaskCard } from './TaskCard';

interface KanbanBoardProps {
  tasks: Task[];
  onStatusChange: (taskId: string, newStatus: TaskStatus) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export function KanbanBoard({ tasks, onStatusChange, onEdit, onDelete }: KanbanBoardProps) {
  const columns: { id: TaskStatus; title: string; color: string }[] = [
    { id: 'todo', title: 'À Faire', color: 'bg-gray-100 border-gray-300' },
    { id: 'in_progress', title: 'En Cours', color: 'bg-blue-50 border-blue-300' },
    { id: 'done', title: 'Terminé', color: 'bg-green-50 border-green-300' },
  ];

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter(task => task.status === status);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {columns.map((column) => (
        <div key={column.id} className={`rounded-lg border-2 p-4 ${column.color}`}>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            {column.title}
            <span className="ml-2 bg-white px-2 py-1 rounded text-sm font-medium text-gray-700">
              {getTasksByStatus(column.id).length}
            </span>
          </h2>

          <div className="space-y-3 min-h-[200px]">
            {getTasksByStatus(column.id).map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => onEdit(task)}
                onDelete={() => onDelete(task.id)}
                onStatusChange={(newStatus) => onStatusChange(task.id, newStatus)}
              />
            ))}

            {getTasksByStatus(column.id).length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <p>Aucune tâche</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
