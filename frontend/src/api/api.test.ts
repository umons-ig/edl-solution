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
});
