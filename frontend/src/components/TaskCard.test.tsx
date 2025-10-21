import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';
import { Task } from '../types/index';

describe('TaskCard', () => {
  // Tâche de test utilisée dans tous les tests
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'This is a test description',
    status: 'todo',
    priority: 'medium',
    created_at: '2025-01-01T10:00:00Z',
    updated_at: '2025-01-01T10:00:00Z',
  };

  /**
   * EXEMPLE : Test de rendu des informations de la tâche
   * Ce test vérifie que tous les éléments de la tâche sont affichés
   */
  it('affiche correctement les informations de la tâche', () => {
    render(
      <TaskCard
        task={mockTask}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Vérifier que le titre est affiché
    expect(screen.getByText('Test Task')).toBeTruthy();

    // Vérifier que la description est affichée
    expect(screen.getByText('This is a test description')).toBeTruthy();

    // Vérifier que la priorité est affichée
    expect(screen.getByText('medium')).toBeTruthy();
  });

  /**
   * EXEMPLE : Test des couleurs de priorité
   * Ce test vérifie que chaque niveau de priorité a la bonne couleur
   */
  it('affiche les bonnes couleurs selon la priorité', () => {
    render(
      <TaskCard
        task={{ ...mockTask, priority: 'high' }}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
        onStatusChange={vi.fn()}
      />
    );

    // Haute priorité = rouge
    const highBadge = screen.getByText('high');
    expect(highBadge.className).toContain('bg-red-100');
    expect(highBadge.className).toContain('text-red-800');
  });

  /**
   * EXEMPLE : Test du bouton d'édition
   * Ce test vérifie que cliquer sur le bouton Edit appelle la fonction onEdit
   */
  it('appelle onEdit quand on clique sur le bouton éditer', () => {
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

  /**
   * EXERCICE 1 : Test du bouton de suppression
   * Écrivez un test qui vérifie que cliquer sur le bouton Delete
   * et confirmer la suppression appelle bien la fonction onDelete
   *
   * Indice : Vous devez mocker window.confirm pour qu'il retourne true
   */
  it.todo('appelle onDelete quand on clique sur supprimer et confirme');
  // TODO: Créez un mock de onDelete
  // TODO: Mockez window.confirm avec vi.spyOn(window, 'confirm').mockReturnValue(true)
  // TODO: Cliquez sur le bouton de suppression (title='Delete task')
  // TODO: Vérifiez que onDelete a été appelé

  /**
   * EXERCICE 2 : Test d'annulation de suppression
   * Écrivez un test qui vérifie que si l'utilisateur annule
   * la confirmation de suppression, onDelete n'est PAS appelé
   */
  it.todo('n\'appelle pas onDelete si l\'utilisateur annule');
  // TODO: Mockez window.confirm pour retourner false
  // TODO: Vérifiez que onDelete n'est PAS appelé (avec .not.toHaveBeenCalled())

  /**
   * EXERCICE 3 : Test sans description
   * Écrivez un test qui vérifie que si une tâche n'a pas de description,
   * celle-ci n'est pas affichée dans le DOM
   */
  it.todo('n\'affiche pas la description si elle est absente');
  // TODO: Créez une tâche sans description ({ ...mockTask, description: undefined })
  // TODO: Vérifiez que la description n'apparaît pas avec screen.queryByText()
});
