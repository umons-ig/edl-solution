import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';
import { Task } from '../types/index';

describe('TaskCard', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'This is a test description',
    status: 'todo',
    priority: 'medium',
    assignee: 'John Doe',
    due_date: '2025-01-15',
    created_at: '2025-01-01T10:00:00Z',
    updated_at: '2025-01-01T10:00:00Z',
  };

  it('renders task information correctly', () => {
    render(
      <TaskCard
        task={mockTask}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Check title is rendered
    expect(screen.getByText('Test Task')).toBeInTheDocument();

    // Check description is rendered
    expect(screen.getByText('This is a test description')).toBeInTheDocument();

    // Check assignee is rendered
    expect(screen.getByText('👤 John Doe')).toBeInTheDocument();

    // Check priority badge
    expect(screen.getByText('medium')).toBeInTheDocument();
  });

  it('shows correct priority colors', () => {
    const renderWithPriority = (priority: 'low' | 'medium' | 'high') => {
      render(
        <TaskCard
          task={{ ...mockTask, priority }}
          onEdit={vi.fn()}
          onDelete={vi.fn()}
          onStatusChange={vi.fn()}
        />
      );
      return screen.getByText(priority);
    };

    // High priority should have red background
    const highTask = renderWithPriority('high');
    expect(highTask).toHaveClass('bg-red-100', 'text-red-800');

    // Medium priority should have yellow background
    const mediumTask = renderWithPriority('medium');
    expect(mediumTask).toHaveClass('bg-yellow-100', 'text-yellow-800');

    // Low priority should have green background
    const lowTask = renderWithPriority('low');
    expect(lowTask).toHaveClass('bg-green-100', 'text-green-800');
  });

  it('calls onEdit when edit button is clicked', () => {
    const onEdit = vi.fn();
    render(
      <TaskCard
        task={mockTask}
        onEdit={onEdit}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    const editButton = screen.getByTitle('Edit task');
    fireEvent.click(editButton);

    expect(onEdit).toHaveBeenCalledTimes(1);
  });

  it('calls onDelete when delete button is clicked and confirmed', () => {
    const onDelete = vi.fn();

    // Mock window.confirm to return true
    const confirmSpy = vi.spyOn(window, 'confirm');
    confirmSpy.mockReturnValue(true);

    render(
      <TaskCard
        task={mockTask}
        onEdit={vi.fn()}
        onDelete={onDelete}
        onStatusChange={vi.fn()}
      />
    );

    const deleteButton = screen.getByTitle('Delete task');
    fireEvent.click(deleteButton);

    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(confirmSpy).toHaveBeenCalledWith('Are you sure you want to delete "Test Task"?');

    confirmSpy.mockRestore();
  });

  it('does not call onDelete when delete is cancelled', () => {
    const onDelete = vi.fn();

    // Mock window.confirm to return false
    const confirmSpy = vi.spyOn(window, 'confirm');
    confirmSpy.mockReturnValue(false);

    render(
      <TaskCard
        task={mockTask}
        onEdit={vi.fn()}
        onDelete={onDelete}
        onStatusChange={vi.fn()}
      />
    );

    const deleteButton = screen.getByTitle('Delete task');
    fireEvent.click(deleteButton);

    expect(onDelete).not.toHaveBeenCalled();
    expect(confirmSpy).toHaveBeenCalledWith('Are you sure you want to delete "Test Task"?');

    confirmSpy.mockRestore();
  });

  it('formats due dates correctly', () => {
    render(
      <TaskCard
        task={mockTask}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Date should be formatted as Jan 15
    expect(screen.getByText('📅 Jan 15')).toBeInTheDocument();
  });

  it('does not render description when not provided', () => {
    const taskWithoutDescription = { ...mockTask, description: undefined };
    render(
      <TaskCard
        task={taskWithoutDescription}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Should not find the description text
    expect(screen.queryByText('This is a test description')).not.toBeInTheDocument();
  });

  it('does not render assignee when not provided', () => {
    const taskWithoutAssignee = { ...mockTask, assignee: undefined };
    render(
      <TaskCard
        task={taskWithoutAssignee}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Should not find the assignee text
    expect(screen.queryByText('👤 John Doe')).not.toBeInTheDocument();
  });

  it('truncates long titles', () => {
    const taskWithLongTitle = {
      ...mockTask,
      title: 'This is a very long task title that should be truncated in the UI'
    };

    render(
      <TaskCard
        task={taskWithLongTitle}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Check that the title element has truncate class
    const titleElement = screen.getByText('This is a very long task title that should be truncated in the UI');
    expect(titleElement).toHaveClass('truncate');
  });
});