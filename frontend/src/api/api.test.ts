import { describe, it, expect, vi } from 'vitest';
import { api } from './api';

/**
 * Tests Frontend API Simples
 *
 * Ces tests démontrent les concepts de base sans complexité excessive.
 * Pour l'Atelier 1, concentrez-vous sur les tests backend. Ceux-ci sont des exemples.
 */

describe('API Module', () => {
  /**
   * Test 1 : Vérifier que l'API peut récupérer les tâches
   * C'est le test le plus basique - est-ce que l'appel API fonctionne ?
   */
  it('fetches tasks from the backend', async () => {
    // Mocker fetch pour retourner des données fictives
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
   * Test 2 : Vérifier que l'API peut créer des tâches
   * Montre comment tester les requêtes POST
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
   * Test 3 : Vérifier que l'API gère les erreurs
   * Important de tester les cas d'erreur !
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
   * Test 4 : Vérifier que l'API peut supprimer des tâches
   */
  it('deletes a task', async () => {
    // Mocker fetch pour retourner une suppression réussie (204 No Content)
    const mockFetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        status: 204,
      })
    );
    (globalThis as any).fetch = mockFetch;

    await api.deleteTask(1);

    // Vérifier que fetch a été appelé avec la bonne URL et méthode
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/tasks/1',
      expect.objectContaining({
        method: 'DELETE',
      })
    );
  });

  /**
   * Test 5 : Vérifier que l'API peut mettre à jour des tâches
   */
  it('updates a task', async () => {
    const updatedTask = { id: 1, title: 'Updated Title', status: 'done' as const };

    // Mocker fetch pour retourner la tâche mise à jour
    const mockFetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(updatedTask),
      })
    );
    (globalThis as any).fetch = mockFetch;

    const result = await api.updateTask(1, { title: 'Updated Title' });

    // Vérifier le résultat
    expect(result.id).toBe(1);
    expect(result.title).toBe('Updated Title');

    // Vérifier que fetch a été appelé avec la bonne URL, méthode et body
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/tasks/1',
      expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({ title: 'Updated Title' }),
      })
    );
  });
});
