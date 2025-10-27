import { describe, it, expect, vi } from 'vitest';
import { api } from './api';

/**
 * Simple Frontend API Tests
 *
 * These tests demonstrate basic testing concepts without overwhelming complexity.
 * For Atelier 1, focus on backend tests. These are here as examples.
 */

describe('API Module', () => {
  /**
   * Test 1: Verify API can fetch tasks
   * This is the most basic test - does the API call work?
   */
  it('fetches tasks from the backend', async () => {
    // Mock fetch to return fake data
    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([
          { id: 1, title: 'Test Task', status: 'todo' }
        ]),
      })
    );

    const tasks = await api.getTasks();

    expect(tasks).toHaveLength(1);
    expect(tasks[0].title).toBe('Test Task');
  });

  /**
   * Test 2: Verify API can create tasks
   * Shows how to test POST requests
   */
  it('creates a new task', async () => {
    const newTask = { title: 'New Task', status: 'todo' as const };

    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ ...newTask, id: 1 }),
      })
    );

    const created = await api.createTask(newTask);

    expect(created.id).toBe(1);
    expect(created.title).toBe('New Task');
  });

  /**
   * Test 3: Verify API handles errors
   * Important to test error cases!
   */
  it('throws error when API fails', async () => {
    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Server Error',
      })
    );

    await expect(api.getTasks()).rejects.toThrow('API error: 500 Server Error');
  });

  /**
   * TODO (Atelier 1 - Exercice 6): Implémenter ce test
   *
   * Test 4: Verify API can delete tasks
   */
  it.todo('deletes a task', async () => {
    // TODO: Votre code ici
    // 1. Mocker fetch pour retourner { ok: true, status: 204 }
    // 2. Appeler await api.deleteTask(1)
    // 3. Vérifier que fetch a été appelé avec '/tasks/1' et method: 'DELETE'
  });

  /**
   * TODO (Atelier 1 - Exercice 7): Implémenter ce test
   *
   * Test 5: Verify API can update tasks
   */
  it.todo('updates a task', async () => {
    // TODO: Votre code ici
    // 1. Mocker fetch pour retourner { ok: true, json: () => Promise.resolve({ id: 1, title: 'Updated', ... }) }
    // 2. Appeler await api.updateTask(1, { title: 'Updated Title' })
    // 3. Vérifier que fetch a été appelé avec '/tasks/1', method: 'PUT'
  });
});
