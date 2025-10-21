import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';

/**
 * Crée un client React Query pour les tests
 * On désactive les retry pour que les tests échouent rapidement
 */
const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

describe('App', () => {
  /**
   * EXEMPLE : Test de rendu de l'interface avec des données mockées
   * Ce test vérifie que l'application affiche correctement le header
   */
  it('affiche le header TaskFlow avec succès', async () => {
    // Mock d'un appel API réussi avec une liste vide
    const mockTasks: any[] = [];
    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockTasks),
        ok: true,
      })
    );

    const queryClient = createTestQueryClient();

    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );

    // Attendre que le chargement soit terminé et vérifier le header
    await waitFor(() => {
      expect(screen.getByText('TaskFlow')).toBeTruthy();
    });

    expect(screen.getByText('Gestion de tâches Kanban')).toBeTruthy();
  });

  /**
   * EXEMPLE : Test de gestion d'erreur réseau
   * Ce test vérifie que l'application affiche un message d'erreur
   * quand le backend est inaccessible
   */
  it('affiche une erreur de connexion quand le backend est inaccessible', async () => {
    const queryClient = createTestQueryClient();

    // Mock d'une erreur réseau (backend down)
    (globalThis as any).fetch = vi.fn(() =>
      Promise.reject(new Error('Network error'))
    );

    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );

    // Devrait afficher le message d'erreur de connexion
    expect(await screen.findByText('Erreur de Connexion')).toBeTruthy();
  });

  /**
   * EXERCICE 1 : Test d'affichage de tâches
   * Écrivez un test qui vérifie que l'application affiche correctement
   * une liste de tâches mockées retournées par l'API
   *
   * Indice : Créez un tableau de tâches avec au moins une tâche
   * et vérifiez que son titre apparaît dans le DOM
   */
  it.todo('affiche la liste des tâches retournées par l\'API');
  // TODO: Créez un mock avec des tâches
  // TODO: Vérifiez que les titres des tâches sont affichés

  /**
   * EXERCICE 2 : Test du bouton de création
   * Écrivez un test qui vérifie que le bouton "Create Task"
   * est présent dans l'interface
   */
  it.todo('affiche le bouton de création de tâche');
  // TODO: Vérifiez que le bouton "Create Task" est présent
});
