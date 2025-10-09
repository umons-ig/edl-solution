import { Task, TaskStatus } from '../types/index';
import { TaskCard } from './TaskCard';

interface KanbanBoardProps {
  tasks: Task[];
  onStatusUpdate: (taskId: string, newStatus: TaskStatus) => void;
  onEditTask: (task: Task) => void;
  onDeleteTask: (taskId: string) => void;
}

export function KanbanBoard({
  tasks,
  onStatusUpdate,
  onEditTask,
  onDeleteTask,
}: KanbanBoardProps) {
  const columns: { id: TaskStatus; title: string; color: string }[] = [
    { id: 'todo', title: 'To Do', color: 'bg-gray-100 border-gray-300' },
    { id: 'in_progress', title: 'In Progress', color: 'bg-blue-50 border-blue-300' },
    { id: 'done', title: 'Done', color: 'bg-green-50 border-green-300' },
  ];

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter(task => task.status === status);
  };

  const handleDrop = (taskId: string, newStatus: TaskStatus) => {
    // In a real implementation, this would trigger the status update
    // For now, we'll implement basic drag feedback
    onStatusUpdate(taskId, newStatus);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {columns.map((column) => (
        <div key={column.id} className={`rounded-lg border-2 p-4 ${column.color}`}>
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="w-3 h-3 rounded-full mr-2 inline-block"
                  style={{ backgroundColor: getColorForStatus(column.id) }}></span>
            {column.title}
            <span className="ml-auto bg-white px-2 py-1 rounded text-sm font-medium text-gray-700">
              {getTasksByStatus(column.id).length}
            </span>
          </h2>

          <div className="space-y-3 min-h-[400px]">
            {getTasksByStatus(column.id).map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => onEditTask(task)}
                onDelete={() => onDeleteTask(task.id)}
                onStatusChange={(newStatus) => handleDrop(task.id, newStatus)}
              />
            ))}

            {getTasksByStatus(column.id).length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <p>Drop tasks here</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

function getColorForStatus(status: TaskStatus): string {
  switch (status) {
    case 'todo':
      return '#9ca3af'; // gray-400
    case 'in_progress':
      return '#3b82f6'; // blue-500
    case 'done':
      return '#10b981'; // emerald-500
    default:
      return '#9ca3af';
  }
}