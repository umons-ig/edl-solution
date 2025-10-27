import { Task } from '../types/index';

interface SimpleTaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

export function SimpleTaskList({ tasks, onEdit, onDelete }: SimpleTaskListProps) {
  const getPriorityLabel = (priority: string) => {
    const labels = { low: 'Basse', medium: 'Moyenne', high: 'Haute' };
    return labels[priority as keyof typeof labels] || priority;
  };

  const getStatusLabel = (status: string) => {
    const labels = { todo: 'À Faire', in_progress: 'En Cours', done: 'Terminé' };
    return labels[status as keyof typeof labels] || status;
  };

  return (
    <div className="task-list">
      {tasks.length === 0 ? (
        <p className="empty-state">Aucune tâche</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id} className="task-item">
              <div className="task-content">
                <h3>{task.title}</h3>
                {task.description && <p>{task.description}</p>}
                <div className="task-meta">
                  <span className={`status status-${task.status}`}>{getStatusLabel(task.status)}</span>
                  <span className={`priority priority-${task.priority}`}>{getPriorityLabel(task.priority)}</span>
                </div>
              </div>
              <div className="task-actions">
                <button onClick={() => onEdit(task)} className="btn-edit">Modifier</button>
                <button onClick={() => {
                  if (window.confirm(`Supprimer "${task.title}" ?`)) {
                    onDelete(task.id);
                  }
                }} className="btn-delete">Supprimer</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
