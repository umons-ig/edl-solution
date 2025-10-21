# 🎨 Atelier 2 : Connecter Frontend React et Backend FastAPI

**Durée estimée :** 3 heures
**Prérequis :** Atelier 1 terminé (backend avec tests et CI/CD)

## 🎯 Objectifs de l'Atelier

**Objectif principal :** Connecter un frontend React à votre backend FastAPI et tester l'intégration

À la fin de cet atelier, vous aurez **construit** :

1. ✅ Une **connexion fonctionnelle** entre frontend et backend (proxy Vite)
2. ✅ Des **appels API** complets (GET, POST, DELETE, PUT)
3. ✅ Des **tests frontend** qui mockent les appels API
4. ✅ Un **pipeline CI/CD** complet (frontend + backend)
5. ✅ Une **application full-stack testée** automatiquement

---

## 📦 Architecture de l'Application

```
┌─────────────────────┐         ┌─────────────────────┐
│  Frontend (React)   │         │  Backend (FastAPI)  │
│  localhost:3000     │ ─────▶  │  localhost:8000     │
│                     │         │                     │
│  Vite Proxy         │         │  API REST           │
│  /api/* → :8000/*   │         │  /tasks, /health    │
└─────────────────────┘         └─────────────────────┘
```

**Stack technique :**
- React 18 + TypeScript
- Vitest + React Testing Library
- React Query (gestion d'état async)
- Tailwind CSS (styling)

---

## 📋 Phase 1 : Connecter Frontend et Backend (45 min)

### 1.1 - Démarrer les Deux Services

**Terminal 1 - Backend :**
```bash
cd backend
uv run uvicorn src.app:app --reload
```

**Terminal 2 - Frontend :**
```bash
cd frontend
npm install
npm run dev
```

**Vérification :**
- Backend : http://localhost:8000/docs
- Frontend : http://localhost:3000

### 1.2 - Observer la Connexion en Action

**🎯 EXERCICE : Comprendre le flux de données**

1. Ouvrez http://localhost:3000
2. Ouvrez DevTools (F12) → Onglet **Network**
3. Rafraîchissez la page

**Questions :**
- Quelle requête voyez-vous ? `GET /api/tasks`
- Quel est le statut ? `200 OK`
- Où cette requête est-elle envoyée ? `http://localhost:3000/api/tasks`

4. Maintenant **arrêtez le backend** (Ctrl+C dans Terminal 1)
5. Rafraîchissez le frontend

**Questions :**
- Que voyez-vous dans l'UI ? "Erreur de Connexion"
- Pourquoi ? Le backend n'est plus accessible

6. **Redémarrez le backend** et rafraîchissez le frontend

### 1.3 - 🎯 EXERCICE : Ajouter un Filtre par Priorité

**Objectif :** Implémenter un filtre pour afficher seulement les tâches d'une certaine priorité.

**Ce que vous allez construire :**
Un menu déroulant qui filtre les tâches par priorité (high, medium, low).

**Étape 1 : Ajouter le filtre dans l'API**

Ouvrez `frontend/src/api/api.ts` et **modifiez** la fonction `getTasks` pour accepter un paramètre optionnel :

```typescript
async getTasks(priority?: string): Promise<Task[]> {
  // Construire l'URL avec le paramètre priority si fourni
  const endpoint = priority ? `/tasks?priority=${priority}` : '/tasks';
  return apiRequest<Task[]>(endpoint);
},
```

**Étape 2 : Ajouter l'état du filtre dans App.tsx**

Ouvrez `frontend/src/App.tsx` et ajoutez un état pour le filtre (après la ligne `const [editingTask, setEditingTask] = ...`) :

```typescript
const [priorityFilter, setPriorityFilter] = useState<string>('');
```

**Étape 3 : Utiliser le filtre dans la requête**

Modifiez le `useQuery` pour inclure le filtre :

```typescript
const { data: tasks = [], isLoading, error } = useQuery({
  queryKey: ['tasks', priorityFilter],  // ← Ajoutez priorityFilter ici
  queryFn: () => api.getTasks(priorityFilter || undefined),  // ← Passez le filtre
});
```

**Étape 4 : Ajouter le menu déroulant**

Dans `App.tsx`, trouvez la section avec le bouton "Nouvelle Tâche" (autour de la ligne 100).

Juste **avant** le bouton "Nouvelle Tâche", ajoutez ce select :

```typescript
{/* Filtre par priorité */}
<select
  value={priorityFilter}
  onChange={(e) => setPriorityFilter(e.target.value)}
  className="px-4 py-2 rounded bg-white text-gray-800 border border-gray-300"
>
  <option value="">Toutes les priorités</option>
  <option value="high">Haute</option>
  <option value="medium">Moyenne</option>
  <option value="low">Basse</option>
</select>
```

**Étape 5 : Tester**

1. Sauvegardez tous les fichiers
2. Créez plusieurs tâches avec différentes priorités
3. Utilisez le menu déroulant pour filtrer
4. Observez dans DevTools → Network : `GET /api/tasks?priority=high`

**Vous venez d'apprendre :**
- ✅ Comment passer des paramètres dans une URL
- ✅ Comment gérer l'état dans React (`useState`)
- ✅ Comment React Query refetch automatiquement quand les paramètres changent
- ✅ L'importance de `queryKey` pour le cache

---

## 📋 Phase 2 : Écrire des Tests Frontend (60 min)

### 2.1 - Comprendre la Structure des Tests

Les tests sont **co-localisés** avec les composants :

```
src/
├── App.tsx
├── App.test.tsx              ← Tests du composant principal
├── components/
│   ├── TaskCard.tsx
│   ├── TaskCard.test.tsx     ← Tests de la carte
│   ├── TaskForm.tsx
│   └── TaskForm.test.tsx     ← Tests du formulaire
```

### 2.2 - Analyser un Test Existant

Ouvrez `src/App.test.tsx` :

```typescript
it('affiche le header TaskFlow avec succès', async () => {
  // 1. Mock de l'API
  const mockTasks: any[] = [];
  (globalThis as any).fetch = vi.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(mockTasks),
      ok: true,
    })
  );

  // 2. Créer un QueryClient pour React Query
  const queryClient = createTestQueryClient();

  // 3. Render le composant
  render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );

  // 4. Attendre que le chargement soit terminé
  await waitFor(() => {
    expect(screen.getByText('TaskFlow')).toBeTruthy();
  });

  // 5. Vérifier le résultat
  expect(screen.getByText('Gestion de tâches Kanban')).toBeTruthy();
});
```

**Points clés :**
- ✅ **Mock fetch** : On ne fait PAS de vrai appel API
- ✅ **QueryClientProvider** : Nécessaire pour React Query
- ✅ **waitFor** : Attend les opérations asynchrones
- ✅ **screen.getByText** : Cherche un élément dans le DOM

### 2.3 - 🎯 EXERCICE 1 : Implémenter le Test d'Affichage de Tâches

Dans `src/App.test.tsx`, vous avez ce TODO :

```typescript
it.todo('affiche la liste des tâches retournées par l\'API');
```

**Votre mission :** Transformez ce `.todo` en test fonctionnel.

**Étapes :**

1. Remplacez `it.todo(...)` par `it(...)`

2. Créez un mock de tâches :
```typescript
const mockTasks = [
  {
    id: '1',
    title: 'Ma première tâche',
    description: 'Test de connexion',
    status: 'todo',
    priority: 'high',
    created_at: '2025-01-01T10:00:00Z',
    updated_at: '2025-01-01T10:00:00Z',
  },
];
```

3. Mockez fetch (comme dans l'exemple au-dessus)

4. Rendez le composant App

5. Vérifiez que le titre de la tâche apparaît :
```typescript
expect(await screen.findByText('Ma première tâche')).toBeTruthy();
```

**Lancez le test :**
```bash
npm test
```

**Résultat attendu :** ✅ Test passe

### 2.4 - 🎯 EXERCICE 2 : Tester la Suppression d'une Tâche

Ouvrez `src/components/TaskCard.test.tsx`.

**TODO à implémenter :**
```typescript
it.todo('appelle onDelete quand on clique sur supprimer et confirme');
```

**Votre mission :** Implémentez ce test.

**Indices :**

1. Créez un mock pour `onDelete` :
```typescript
const onDelete = vi.fn();
```

2. Mockez `window.confirm` pour qu'il retourne `true` :
```typescript
const confirmSpy = vi.spyOn(window, 'confirm');
confirmSpy.mockReturnValue(true);
```

3. Rendez le TaskCard :
```typescript
render(
  <TaskCard
    task={mockTask}
    onEdit={vi.fn()}
    onDelete={onDelete}
    onStatusChange={vi.fn()}
  />
);
```

4. Trouvez et cliquez sur le bouton delete :
```typescript
const deleteButton = screen.getByTitle('Delete task');
fireEvent.click(deleteButton);
```

5. Vérifiez que `onDelete` a été appelé :
```typescript
expect(onDelete).toHaveBeenCalledTimes(1);
```

6. Nettoyez le mock :
```typescript
confirmSpy.mockRestore();
```

**Lancez le test :**
```bash
npm test
```

### 2.5 - 🎯 EXERCICE 3 : Tester le Formulaire

Dans `src/components/TaskForm.test.tsx`, implémentez :

```typescript
it.todo('appelle onCancel quand on clique sur Annuler');
```

**Votre mission :** Écrivez un test qui vérifie que cliquer sur "Annuler" appelle bien `onCancel`.

**Code à écrire :**

```typescript
it('appelle onCancel quand on clique sur Annuler', () => {
  // TODO: Créez les mocks
  const onSubmit = vi.fn();
  const onCancel = vi.fn();

  // TODO: Rendez le composant
  render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

  // TODO: Trouvez et cliquez sur le bouton "Annuler"
  const cancelButton = screen.getByText('Annuler');
  fireEvent.click(cancelButton);

  // TODO: Vérifiez que onCancel a été appelé
  expect(onCancel).toHaveBeenCalledTimes(1);
});
```

### 2.6 - Vérifier la Couverture des Tests

```bash
npm run test:coverage
```

**Résultat attendu :**
```
File               | % Stmts | % Branch | % Funcs | % Lines |
-------------------|---------|----------|---------|---------|
App.tsx            |   72.64 |    71.42 |   15.38 |   72.64 |
TaskCard.tsx       |      88 |    66.66 |   66.66 |      88 |
TaskForm.tsx       |     100 |    95.45 |   85.71 |     100 |
```

**Note :** On ne vise PAS 100% de couverture. L'objectif est de **comprendre comment tester**.

---

## 📋 Phase 3 : Créer le Pipeline CI/CD (45 min)

### 3.1 - Créer la Structure du Workflow

**🎯 EXERCICE : Créer le fichier de workflow**

1. Créez le dossier (si nécessaire) :
```bash
mkdir -p .github/workflows
```

2. Créez le fichier :
```bash
touch .github/workflows/ci.yml
```

3. Ouvrez `.github/workflows/ci.yml` dans votre éditeur

### 3.2 - Implémenter le Job de Tests Frontend

**🎯 EXERCICE : Écrire le workflow pour le frontend**

Ajoutez ce contenu à `.github/workflows/ci.yml` :

```yaml
name: TaskFlow CI/CD

# Déclencher sur push et pull request vers main
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-frontend:
    name: Tests Frontend
    runs-on: ubuntu-latest

    # Tous les commandes s'exécutent dans ./frontend
    defaults:
      run:
        working-directory: ./frontend

    steps:
      # 1. Récupérer le code
      - name: 📥 Checkout Code
        uses: actions/checkout@v4

      # 2. Installer Node.js
      - name: 🔧 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: './frontend/package-lock.json'

      # 3. Installer les dépendances
      - name: 📦 Install Dependencies
        run: npm ci

      # 4. Lancer les tests
      - name: 🧪 Run Tests
        run: npm test -- --run

      # 5. Vérifier que le build fonctionne
      - name: 🏗️ Build Check
        run: npm run build
```

**Explications :**
- `on: push/pull_request` : Quand exécuter le workflow
- `runs-on: ubuntu-latest` : Machine virtuelle Linux
- `working-directory` : Tous les `run` s'exécutent dans `./frontend`
- `npm ci` : Installation rapide et déterministe (vs `npm install`)
- `npm test -- --run` : Lance les tests sans mode watch

### 3.3 - Ajouter le Job de Tests Backend

**🎯 EXERCICE : Ajouter le backend au workflow**

Dans le même fichier `.github/workflows/ci.yml`, ajoutez un second job **AVANT** le job frontend :

```yaml
jobs:
  test-backend:
    name: Tests Backend
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: ./backend

    steps:
      - name: 📥 Checkout Code
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 📦 Setup UV
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: 📚 Install Dependencies
        run: uv sync

      - name: 🧪 Run Tests
        run: |
          uv run pytest \
            --cov=src \
            --cov-report=term-missing \
            --cov-fail-under=90 \
            -v

  test-frontend:
    # ... (le job frontend que vous avez écrit au-dessus)
```

**Note :** Maintenant vous avez **2 jobs** qui s'exécutent en **parallèle** !

### 3.4 - Tester le Workflow Localement

**Avant de pusher, vérifiez que tout fonctionne :**

```bash
# Backend
cd backend
uv run pytest
# ✅ Doit passer

# Frontend
cd frontend
npm test -- --run
# ✅ Doit passer

npm run build
# ✅ Doit construire sans erreur
```

### 3.5 - Pousser et Voir le CI/CD en Action

**🎯 EXERCICE : Déclencher le workflow**

1. Committez vos changements :
```bash
git add .
git commit -m "feat: add CI/CD workflow for frontend and backend"
git push origin main
```

2. Allez sur GitHub → Actions
   - URL : `https://github.com/VOTRE_USERNAME/edl-starter/actions`

3. Observez le workflow s'exécuter :
   - ✅ test-backend (Python, pytest)
   - ✅ test-frontend (Node.js, vitest, build)

**Résultat attendu :**
```
✅ test-backend   ✓ Completed in 45s
✅ test-frontend  ✓ Completed in 1m 12s
```

### 3.6 - 🎯 EXERCICE BONUS : Ajouter un Job d'Intégration

**Pour les plus rapides :** Ajoutez un 3ème job qui vérifie que le backend et le frontend peuvent communiquer.

Ajoutez après les deux premiers jobs :

```yaml
  integration-check:
    name: Test d'Intégration
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]  # Attend que les deux passent

    steps:
      - name: 📥 Checkout Code
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 📦 Setup UV
        uses: astral-sh/setup-uv@v3

      - name: 🔗 Basic Integration Test
        run: |
          cd backend
          uv sync

          # Démarrer le backend en arrière-plan
          uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 &
          BACKEND_PID=$!

          # Attendre que le backend démarre
          sleep 3

          # Tester l'API
          curl -f http://localhost:8000/health || exit 1
          curl -f http://localhost:8000/tasks || exit 1

          echo "✅ Integration test passed!"

          # Arrêter le backend
          kill $BACKEND_PID
```

---

## 📋 Phase 4 : Intégration Complète (30 min)

### 4.1 - Vérifier le Système Complet

**🎯 CHECKLIST FINALE :**

Dans votre terminal local :

- [ ] Backend démarre sans erreur : `uv run uvicorn src.app:app --reload`
- [ ] Frontend démarre sans erreur : `npm run dev`
- [ ] Vous pouvez créer une tâche via l'interface
- [ ] Les tests backend passent : `cd backend && uv run pytest`
- [ ] Les tests frontend passent : `cd frontend && npm test -- --run`
- [ ] Le build frontend réussit : `cd frontend && npm run build`

Sur GitHub Actions :

- [ ] Le workflow CI s'exécute automatiquement sur push
- [ ] Les tests backend passent ✅
- [ ] Les tests frontend passent ✅
- [ ] Le build frontend réussit ✅

### 4.2 - Déboguer les Problèmes Courants

#### ❌ "Connection Error" dans le frontend

**Cause :** Backend pas lancé

**Solution :**
```bash
cd backend
uv run uvicorn src.app:app --reload
```

#### ❌ Tests échouent dans GitHub Actions

**Cause :** Tests qui passent en local mais échouent sur GitHub

**Solution :**
1. Vérifiez les logs dans GitHub Actions
2. Reproduisez exactement la même commande en local :
```bash
cd frontend
npm ci  # Pas npm install !
npm test -- --run
```

#### ❌ Build frontend échoue

**Cause :** Erreurs TypeScript ou imports manquants

**Solution :**
```bash
cd frontend
npm run build
# Lire les erreurs et les corriger
```

### 4.3 - Améliorer Votre Application (Exercices Optionnels)

**Pour aller plus loin :**

1. **Ajoutez un filtre par statut**
   - Dans `App.tsx`, ajoutez un `<select>` pour filtrer par "todo", "in_progress", "done"
   - Modifiez `api.getTasks()` pour accepter un paramètre `?status=todo`

2. **Ajoutez un test pour le filtre**
   - Testez que le filtre appelle l'API avec le bon paramètre

3. **Améliorez le workflow CI/CD**
   - Ajoutez l'upload des rapports de couverture
   - Ajoutez un job de lint (ESLint)

---

## ✅ Checklist de Fin d'Atelier

Avant de considérer l'atelier comme terminé :

### Fonctionnalités
- [ ] Le backend et le frontend communiquent correctement
- [ ] Vous pouvez créer, modifier, supprimer des tâches via l'interface
- [ ] Les erreurs de connexion sont bien gérées (backend down)

### Tests
- [ ] Au moins 3 tests frontend fonctionnent (que vous avez implémentés)
- [ ] Tous les tests passent localement (`npm test`)
- [ ] La couverture est > 60%

### CI/CD
- [ ] Fichier `.github/workflows/ci.yml` créé
- [ ] Job de tests backend configuré
- [ ] Job de tests frontend configuré
- [ ] Le workflow s'exécute automatiquement sur GitHub
- [ ] Tous les jobs passent ✅

### Compréhension
- [ ] Vous comprenez le rôle du proxy Vite
- [ ] Vous savez comment mocker des appels API dans les tests
- [ ] Vous comprenez la différence entre `npm install` et `npm ci`
- [ ] Vous savez lire les logs de GitHub Actions

---

## 🎯 Ce que Vous Avez Appris

Félicitations ! 🎉 Vous avez maintenant :

✅ **Connecté un frontend React à un backend FastAPI**
✅ **Écrit des tests frontend** qui mockent les appels API
✅ **Créé un pipeline CI/CD complet** qui teste automatiquement votre code
✅ **Compris l'architecture client-serveur** et le rôle du proxy
✅ **Pratiqué le développement full-stack** moderne

### Prochaine Étape : Atelier 3

Dans l'Atelier 3, vous allez **déployer votre application en production** sur le cloud avec :
- Déploiement sur Render
- Configuration des variables d'environnement
- Gestion CORS pour la production
- Monitoring et health checks

**Prêt pour la production ? 🚀**

---

## 📚 Ressources Supplémentaires

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Vite Proxy Configuration](https://vitejs.dev/config/server-options.html#server-proxy)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Version 2.0** - Atelier 2 Révisé avec Focus sur l'Implémentation 🚀
