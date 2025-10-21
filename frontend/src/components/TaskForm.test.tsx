import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskForm } from './TaskForm';
import { Task } from '../types/index';

describe('TaskForm', () => {
  // Tâche de test pour les tests d'édition
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'Test description',
    status: 'in_progress',
    priority: 'high',
    created_at: '2025-01-01T10:00:00Z',
    updated_at: '2025-01-01T10:00:00Z',
  };

  /**
   * EXEMPLE : Test de rendu du formulaire de création
   * Ce test vérifie que le formulaire s'affiche correctement
   * en mode création (sans tâche fournie)
   */
  it('affiche correctement le formulaire de création', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    expect(screen.getByText('Créer une Nouvelle Tâche')).toBeTruthy();
    expect(screen.getByText('Créer')).toBeTruthy();
    expect(screen.getByPlaceholderText('Entrez le titre de la tâche')).toBeTruthy();
  });

  /**
   * EXEMPLE : Test de rendu du formulaire d'édition
   * Ce test vérifie que le formulaire s'affiche correctement
   * en mode édition (avec une tâche fournie)
   */
  it('affiche correctement le formulaire d\'édition avec les données existantes', () => {
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm task={mockTask} onSubmit={onSubmit} onCancel={onCancel} />);

    expect(screen.getByText('Modifier la Tâche')).toBeTruthy();
    expect(screen.getByText('Mettre à Jour')).toBeTruthy();
    expect(screen.getByDisplayValue('Test Task')).toBeTruthy();
    expect(screen.getByDisplayValue('Test description')).toBeTruthy();
  });

  /**
   * EXEMPLE : Test de soumission du formulaire
   * Ce test vérifie que la fonction onSubmit est appelée
   * avec les bonnes données quand on soumet le formulaire
   */
  it('appelle onSubmit avec les données du formulaire', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    const onCancel = vi.fn();

    render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

    // Remplir le formulaire
    await user.type(screen.getByPlaceholderText('Entrez le titre de la tâche'), 'New Task');
    await user.type(screen.getByPlaceholderText('Entrez la description (optionnel)'), 'My description');

    // Sélectionner la priorité
    const prioritySelect = screen.getByDisplayValue('Moyenne');
    await user.selectOptions(prioritySelect, 'high');

    // Soumettre le formulaire
    fireEvent.click(screen.getByText('Créer'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'New Task',
          description: 'My description',
          status: 'todo',
          priority: 'high',
        })
      );
    });
  });

  /**
   * EXERCICE 1 : Test du bouton Annuler
   * Écrivez un test qui vérifie que cliquer sur le bouton "Annuler"
   * appelle la fonction onCancel
   */
  it.todo('appelle onCancel quand on clique sur Annuler');
  // TODO: Créez des mocks pour onSubmit et onCancel
  // TODO: Rendez le formulaire
  // TODO: Cliquez sur le bouton "Annuler"
  // TODO: Vérifiez que onCancel a été appelé 1 fois

  /**
   * EXERCICE 2 : Test des boutons désactivés pendant le chargement
   * Écrivez un test qui vérifie que quand isLoading=true,
   * les boutons sont désactivés et affichent "Enregistrement..."
   */
  it.todo('désactive les boutons quand isLoading est true');
  // TODO: Rendez le formulaire avec isLoading={true}
  // TODO: Vérifiez que le bouton affiche "Enregistrement..."
  // TODO: Vérifiez que les boutons sont disabled

  /**
   * EXERCICE 3 : Test du champ titre obligatoire
   * Écrivez un test qui vérifie que le champ titre est requis
   * (le formulaire ne peut pas être soumis sans titre)
   */
  it.todo('exige le champ titre');
  // TODO: Rendez le formulaire
  // TODO: Essayez de soumettre sans remplir le titre
  // TODO: Vérifiez que onSubmit n'a PAS été appelé

  /**
   * EXERCICE 4 : Test des options de statut
   * Écrivez un test qui vérifie que le dropdown de statut
   * contient bien les 3 options : "À Faire", "En Cours", "Terminé"
   */
  it.todo('affiche toutes les options de statut');
  // TODO: Rendez le formulaire
  // TODO: Récupérez toutes les options du select de statut
  // TODO: Vérifiez que les 3 statuts sont présents ("À Faire", "En Cours", "Terminé")
});
