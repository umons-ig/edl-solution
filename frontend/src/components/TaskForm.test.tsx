import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskForm } from './TaskForm';
import { Task } from '../types/index';

describe('TaskForm', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'This is a test description',
    status: 'in_progress',
    priority: 'high',
    assignee: 'John Doe',
    due_date: '2025-01-15',
    created_at: '2025-01-01T10:00:00Z',
    updated_at: '2025-01-01T10:00:00Z',
  };

  it('renders create form correctly when no task provided', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    expect(screen.getByText('Create New Task')).toBeInTheDocument();
    expect(screen.getByText('Create Task')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter task title')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter task description (optional)')).toBeInTheDocument();
  });

  it('renders edit form correctly when task is provided', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm task={mockTask} onSubmit={onSubmit} onCancel={onCancel} />);

    expect(screen.getByText('Edit Task')).toBeInTheDocument();
    expect(screen.getByText('Update Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('This is a test description')).toBeInTheDocument();
    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
  });

  it('calls onSubmit with form data when form is submitted', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    // Fill out the form
    await user.type(screen.getByPlaceholderText('Enter task title'), 'New Task Title');
    await user.type(screen.getByPlaceholderText('Enter task description (optional)'), 'New description');

    // Select priority
    const prioritySelect = screen.getByDisplayValue('Medium');
    await user.selectOptions(prioritySelect, 'high');

    // Add assignee
    await user.type(screen.getByPlaceholderText('Assign to...'), 'Jane Smith');

    // Submit the form
    fireEvent.click(screen.getByText('Create Task'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        title: 'New Task Title',
        description: 'New description',
        status: 'todo',
        priority: 'high',
        assignee: 'Jane Smith',
      });
    });
  });

  it('filters out empty string values when submitting', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    // Fill only title, leave others empty
    await user.type(screen.getByPlaceholderText('Enter task title'), 'Task with minimal data');

    // Submit the form
    fireEvent.click(screen.getByText('Create Task'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        title: 'Task with minimal data',
        status: 'todo',
        priority: 'medium',
      });
    });
  });

  it('calls onCancel when cancel button is clicked', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);

    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it('disables buttons when isLoading is true', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} isLoading={true} />);

    const submitButton = screen.getByText('Saving...');
    const cancelButton = screen.getByText('Cancel');

    expect(submitButton).toBeDisabled();
    expect(cancelButton).toBeDisabled();
  });

  it('requires title field', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    const submitButton = screen.getByText('Create Task');
    fireEvent.click(submitButton);

    // HTML5 validation should prevent submission
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('populates form with existing task data for editing', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm task={mockTask} onSubmit={onSubmit} onCancel={onCancel} />);

    // Check that the edit form shows existing task data
    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('This is a test description')).toBeInTheDocument();
    expect(screen.getByDisplayValue('In Progress')).toBeInTheDocument();
    expect(screen.getByDisplayValue('High')).toBeInTheDocument();
    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
  });

  it('shows all status options in dropdown', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    const statusSelect = screen.getAllByRole('option', { hidden: true });
    const statusOptions = statusSelect.map(option => option.textContent);

    expect(statusOptions).toContain('To Do');
    expect(statusOptions).toContain('In Progress');
    expect(statusOptions).toContain('Done');
  });
});