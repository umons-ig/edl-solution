# 🎨 Atelier 2 : Connecter Frontend React et Backend FastAPI

**Durée estimée :** 2-3 heures
**Prérequis :** Atelier 1 terminé (compréhension de TDD et GitHub Actions)

## 🎯 Objectifs de l'Atelier

**Objectif principal :** Apprendre à connecter un frontend React à un backend API

À la fin de cet atelier, vous serez capable de :

1. ✅ **Comprendre l'architecture client-serveur** (frontend ↔ backend)
2. ✅ **Configurer et utiliser un proxy Vite** pour rediriger les requêtes API
3. ✅ **Faire des appels API depuis React** (GET, POST, DELETE, PUT)
4. ✅ **Gérer les états asynchrones** avec React Query
5. ✅ **Écrire des tests** qui mockent les appels API
6. ✅ **Debugger les problèmes** de connexion frontend-backend

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

**Technologies utilisées :**
- React 18 + TypeScript
- Vite (build tool)
- Vitest (framework de tests)
- React Testing Library (tests de composants)
- React Query (gestion d'état async)
- Tailwind CSS (styling)

---

## 📋 Phase 1 : Préparation (15 min)

### 1.1 - Vérifier que le Backend Fonctionne

**⚠️ IMPORTANT :** Le backend doit tourner avant de lancer le frontend !

```bash
# Terminal 1 - Backend
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv run uvicorn src.app:app --reload
```

Vérifiez que le backend répond :
```bash
curl http://localhost:8000/health
# Réponse : {"status":"healthy"}
```

### 1.2 - Installer les Dépendances Frontend

```bash
# Terminal 2 - Frontend
cd frontend
npm install
```

### 1.3 - Explorer la Structure du Projet

```
frontend/
├── src/
│   ├── components/
│   │   ├── KanbanBoard.tsx       # Board Kanban
│   │   ├── TaskCard.tsx          # Carte de tâche
│   │   └── TaskForm.tsx          # Formulaire
│   ├── api/
│   │   └── api.ts                # Appels API
│   ├── types/
│   │   └── index.ts              # Types TypeScript
│   ├── test/
│   │   └── setup.ts              # Configuration tests
│   └── App.tsx                   # Composant principal
├── vite.config.ts                # Config Vite + Proxy
└── vitest.config.ts              # Config tests
```

**Question de réflexion :** Pourquoi sépare-t-on le code en plusieurs dossiers (components, api, types) ?

---

## 📋 Phase 2 : Comprendre l'Architecture Client-Serveur (30 min)

### 2.1 - Le Problème à Résoudre

**Sans proxy, voici ce qui se passe :**

```
Frontend (localhost:3000) → Backend (localhost:8000)
        ❌ CORS Error!
```

Les navigateurs bloquent les requêtes entre différents ports (politique CORS).

**Solutions possibles :**
1. ✅ **Proxy Vite** (développement) - ce que nous utilisons
2. Configurer CORS sur le backend (production)
3. Déployer frontend et backend sur le même domaine

### 2.2 - Comprendre le Proxy Vite

Ouvrez `frontend/vite.config.ts` :

```typescript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

**Comment ça marche ?**

```
┌─────────────────────────────────────────────────────────┐
│ 1. Frontend fait une requête                            │
│    fetch('/api/tasks')                                  │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Vite intercepte toute requête commençant par /api/  │
│    Règle : "/api" → "http://localhost:8000"            │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Vite réécrit le chemin                              │
│    /api/tasks → /tasks                                  │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Vite envoie la requête au backend                   │
│    GET http://localhost:8000/tasks                      │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Backend répond avec les données                     │
│    [{ id: '1', title: 'Task 1', ... }]                 │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Vite renvoie la réponse au frontend                 │
│    Frontend reçoit les données                         │
└─────────────────────────────────────────────────────────┘
```

**Table de redirection :**

| Frontend appelle      | Vite redirige vers                | Backend reçoit |
|-----------------------|----------------------------------|----------------|
| `GET /api/tasks`      | `GET http://localhost:8000/tasks` | `GET /tasks` |
| `POST /api/tasks`     | `POST http://localhost:8000/tasks` | `POST /tasks` |
| `DELETE /api/tasks/1` | `DELETE http://localhost:8000/tasks/1` | `DELETE /tasks/1` |

### 2.3 - Exercice Pratique : Observer le Proxy en Action

**Étape 1 :** Lancez le backend et le frontend

```bash
# Terminal 1 - Backend
cd backend
uv run uvicorn src.app:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Étape 2 :** Ouvrez http://localhost:3000 et ouvrez DevTools (F12)

**Étape 3 :** Allez dans l'onglet **Network** et essayez ces actions :

1. **Créer une tâche** :
   - Cliquez sur "Create Task"
   - Remplissez le formulaire
   - Soumettez
   - **Observez :** Requête `POST /api/tasks` → Status 201

2. **Lister les tâches** :
   - **Observez :** Requête `GET /api/tasks` → Status 200
   - Cliquez sur la requête pour voir les données JSON

3. **Supprimer une tâche** :
   - Cliquez sur le bouton delete
   - **Observez :** Requête `DELETE /api/tasks/{id}` → Status 204

**Questions de réflexion :**
1. Dans Network tab, voyez-vous `localhost:3000/api/tasks` ou `localhost:8000/tasks` ?
2. Pourquoi le frontend utilise-t-il `/api/` comme préfixe ?

### 2.4 - Analyser le Fichier API

Ouvrez `frontend/src/api/api.ts` :

```typescript
const API_BASE = import.meta.env.VITE_API_URL || '/api';

async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;  // → /api/tasks

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  async getTasks(): Promise<Task[]> {
    return apiRequest<Task[]>('/tasks');
  },

  async createTask(task: TaskCreate): Promise<Task> {
    return apiRequest<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  },

  async deleteTask(id: string): Promise<void> {
    return apiRequest<void>(`/tasks/${id}`, {
      method: 'DELETE',
    });
  },
};
```

**Explication ligne par ligne :**

1. **`API_BASE`** : Préfixe pour toutes les requêtes (`/api`)
2. **`apiRequest()`** : Fonction générique pour tous les appels
3. **`fetch(url, options)`** : Fonction native du navigateur
4. **`Content-Type: application/json`** : Indique que nous envoyons du JSON
5. **`response.ok`** : Vérifie si status est 200-299
6. **`response.json()`** : Parse la réponse JSON

**Exercice :** Ajoutez une fonction `updateTask` dans `api` :

```typescript
async updateTask(id: string, updates: TaskUpdate): Promise<Task> {
  return apiRequest<Task>(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}
```

### 2.5 - Tester Manuellement l'API

**Sans le frontend**, testez le backend directement :

```bash
# GET - Lister les tâches
curl http://localhost:8000/tasks

# POST - Créer une tâche
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test via curl", "priority": "high"}'

# DELETE - Supprimer une tâche
curl -X DELETE http://localhost:8000/tasks/1
```

**Avec le frontend**, faites la même chose via l'interface et comparez les résultats.

---

## 📋 Phase 3 : Faire des Appels API depuis React (40 min)

### 3.1 - Comprendre le Flux de Données

```
┌──────────────────────┐
│   User Action        │ Clic sur "Create Task"
└──────────────────────┘
          ↓
┌──────────────────────┐
│   React Component    │ TaskForm → onSubmit(data)
└──────────────────────┘
          ↓
┌──────────────────────┐
│   React Query        │ useMutation → api.createTask(data)
└──────────────────────┘
          ↓
┌──────────────────────┐
│   API Layer          │ fetch('/api/tasks', { method: 'POST', ... })
└──────────────────────┘
          ↓
┌──────────────────────┐
│   Vite Proxy         │ Redirige vers localhost:8000/tasks
└──────────────────────┘
          ↓
┌──────────────────────┐
│   Backend API        │ FastAPI crée la tâche
└──────────────────────┘
          ↓
┌──────────────────────┐
│   Response           │ { id: '123', title: '...' }
└──────────────────────┘
          ↓
┌──────────────────────┐
│   React Query        │ Invalide le cache, refetch les données
└──────────────────────┘
          ↓
┌──────────────────────┐
│   UI Update          │ La nouvelle tâche apparaît
└──────────────────────┘
```

### 3.2 - Analyser l'Utilisation de React Query

Ouvrez `frontend/src/App.tsx` et trouvez :

```typescript
const { data: tasks = [], isLoading, error } = useQuery({
  queryKey: ['tasks'],
  queryFn: api.getTasks,
});
```

**Pourquoi utiliser React Query au lieu de useState + useEffect ?**

**❌ Avec useState (approche traditionnelle) :**
```typescript
const [tasks, setTasks] = useState([]);
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  setIsLoading(true);
  fetch('/api/tasks')
    .then(res => res.json())
    .then(data => {
      setTasks(data);
      setIsLoading(false);
    })
    .catch(err => {
      setError(err);
      setIsLoading(false);
    });
}, []);
```

**✅ Avec React Query (moderne) :**
```typescript
const { data: tasks = [], isLoading, error } = useQuery({
  queryKey: ['tasks'],
  queryFn: api.getTasks,
});
```

**Avantages de React Query :**
- ✅ **Cache automatique** : Les données sont mises en cache
- ✅ **Gestion des états** : loading, error, success gérés automatiquement
- ✅ **Refetch automatique** : Rafraîchit les données quand la fenêtre reprend le focus
- ✅ **Optimistic updates** : Mise à jour optimiste de l'UI
- ✅ **Moins de code** : ~20 lignes → ~4 lignes

### 3.3 - Exercice Pratique : Ajouter un Filtre

**Objectif :** Filtrer les tâches par statut en modifiant l'appel API

**Étape 1 :** Dans `src/api/api.ts`, modifiez `getTasks` :

```typescript
async getTasks(status?: string): Promise<Task[]> {
  const params = status ? `?status=${status}` : '';
  return apiRequest<Task[]>(`/tasks${params}`);
}
```

**Étape 2 :** Dans `src/App.tsx`, ajoutez un état pour le filtre :

```typescript
const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);

const { data: tasks = [], isLoading, error } = useQuery({
  queryKey: ['tasks', statusFilter],  // ← Change la clé de cache quand le filtre change
  queryFn: () => api.getTasks(statusFilter),
});
```

**Étape 3 :** Ajoutez un select pour changer le filtre :

```tsx
<select onChange={(e) => setStatusFilter(e.target.value || undefined)}>
  <option value="">Tous</option>
  <option value="todo">À Faire</option>
  <option value="in_progress">En Cours</option>
  <option value="done">Terminé</option>
</select>
```

**Étape 4 :** Testez dans le navigateur :
- Sélectionnez "À Faire" → Observez la requête `GET /api/tasks?status=todo`
- Changez de filtre → Nouvelle requête API

### 3.4 - Analyser les Mutations

**Pour les opérations qui modifient les données (POST, PUT, DELETE), on utilise `useMutation` :**

```typescript
const createTaskMutation = useMutation({
  mutationFn: (taskData: TaskCreate) => api.createTask(taskData),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tasks'] });
    setShowForm(false);
  },
  onError: (error) => {
    console.error('Erreur lors de la création:', error);
  },
});
```

**Comment ça marche ?**

1. **`mutationFn`** : Fonction appelée pour créer la tâche
2. **`onSuccess`** : Callback après succès
   - `invalidateQueries` : Marque le cache comme périmé → refetch automatique
   - `setShowForm(false)` : Ferme le formulaire
3. **`onError`** : Callback en cas d'erreur

**Pour utiliser la mutation :**

```typescript
const handleSubmit = (taskData: TaskCreate) => {
  createTaskMutation.mutate(taskData);
};
```

### 3.5 - Exercice : Comprendre le Cycle de Vie

**Étape 1 :** Ajoutez des `console.log` dans `src/App.tsx` :

```typescript
const createTaskMutation = useMutation({
  mutationFn: (taskData: TaskCreate) => {
    console.log('1. 🚀 Mutation appelée avec:', taskData);
    return api.createTask(taskData);
  },
  onSuccess: (newTask) => {
    console.log('2. ✅ Succès! Tâche créée:', newTask);
    queryClient.invalidateQueries({ queryKey: ['tasks'] });
    console.log('3. 🔄 Cache invalidé, refetch en cours...');
    setShowForm(false);
  },
  onError: (error) => {
    console.log('❌ Erreur:', error);
  },
});
```

**Étape 2 :** Ouvrez la console (F12) et créez une tâche

**Étape 3 :** Observez l'ordre des logs :
```
1. 🚀 Mutation appelée avec: { title: "Ma tâche", ... }
2. ✅ Succès! Tâche créée: { id: "123", title: "Ma tâche", ... }
3. 🔄 Cache invalidé, refetch en cours...
```

**Question :** Que se passe-t-il après le log 3 ?

---

## 📋 Phase 4 : Écrire des Tests Frontend (45 min)

### 4.1 - Analyser les Tests Existants

Ouvrez `frontend/src/App.test.tsx` :

```typescript
it('affiche le header TaskFlow avec succès', async () => {
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

  await waitFor(() => {
    expect(screen.getByText('TaskFlow')).toBeTruthy();
  });
});
```

**Points clés :**
- ✅ Mock de `fetch` pour éviter les vrais appels API
- ✅ Utilisation de `waitFor` pour les opérations async
- ✅ `QueryClientProvider` nécessaire pour React Query

### 4.2 - Exercice 1 : Test d'Affichage de Tâches

Dans `src/App.test.tsx`, complétez le test TODO :

```typescript
it('affiche la liste des tâches retournées par l\'API', async () => {
  // TODO: Créez un mock avec des tâches
  const mockTasks = [
    {
      id: '1',
      title: 'Ma première tâche',
      status: 'todo',
      priority: 'high',
      created_at: '2025-01-01T10:00:00Z',
      updated_at: '2025-01-01T10:00:00Z',
    },
  ];

  // TODO: Mockez fetch
  (globalThis as any).fetch = vi.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(mockTasks),
      ok: true,
    })
  );

  const queryClient = createTestQueryClient();

  // TODO: Rendez l'App
  render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );

  // TODO: Vérifiez que le titre de la tâche est affiché
  expect(await screen.findByText('Ma première tâche')).toBeTruthy();
});
```

Lancez le test :
```bash
npm test
```

### 4.3 - Exercice 2 : Test de TaskCard (Suppression)

Dans `src/components/TaskCard.test.tsx`, complétez :

```typescript
it('appelle onDelete quand on clique sur supprimer et confirme', () => {
  const onDelete = vi.fn();

  // Mock window.confirm
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

  confirmSpy.mockRestore();
});
```

### 4.4 - Exercice 3 : Test de TaskForm (Bouton Cancel)

Dans `src/components/TaskForm.test.tsx` :

```typescript
it('appelle onCancel quand on clique sur Cancel', () => {
  const onSubmit = vi.fn();
  const onCancel = vi.fn();

  render(<TaskForm onSubmit={onSubmit} onCancel={onCancel} />);

  const cancelButton = screen.getByText('Cancel');
  fireEvent.click(cancelButton);

  expect(onCancel).toHaveBeenCalledTimes(1);
});
```

### 4.5 - Vérifier la Couverture des Tests

```bash
npm run test:coverage
```

Ouvrez le rapport :
```bash
open coverage/index.html  # macOS
start coverage/index.html # Windows
```

**Objectif :** Au moins 70% de couverture.

---

## 📋 Phase 5 : Configurer le CI/CD Frontend (30 min)

### 5.1 - Analyser le Workflow Existant

Ouvrez `.github/workflows/ci.yml` et vérifiez qu'il contient un job frontend :

```yaml
frontend-tests:
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install dependencies
      working-directory: ./frontend
      run: npm ci

    - name: Run tests
      working-directory: ./frontend
      run: npm test -- --run

    - name: Build
      working-directory: ./frontend
      run: npm run build
```

### 5.2 - Pousser et Vérifier

```bash
git add .
git commit -m "feat(frontend): add tests for workshop 2"
git push
```

Vérifiez dans GitHub Actions :
- ✅ Backend tests pass
- ✅ Frontend tests pass
- ✅ Build succeeds

---

## 📋 Phase 6 : Debugging et Bonnes Pratiques (20 min)

### 6.1 - Problèmes Courants

#### Erreur : "Connection Error"

**Cause :** Backend pas lancé.

**Solution :**
```bash
cd backend
uv run uvicorn src.app:app --reload
```

#### Erreur : "Module not found"

**Cause :** Dépendances pas installées.

**Solution :**
```bash
cd frontend
npm install
```

#### Tests échouent

**Cause :** Mocks incorrects.

**Solution :** Vérifiez que vous mockez bien `fetch` avec `vi.fn()`.

### 6.2 - Bonnes Pratiques

1. **Toujours tester les 3 états :**
   - ✅ Loading
   - ✅ Success
   - ✅ Error

2. **Utiliser des queries sémantiques :**
   - `getByText` → élément doit exister
   - `queryByText` → élément peut ne pas exister
   - `findByText` → élément apparaîtra (async)

3. **Nettoyer les mocks :**
   ```typescript
   afterEach(() => {
     vi.clearAllMocks();
   });
   ```

---

## 📋 Phase 7 : Exercices Avancés (Optionnel)

### 7.1 - Ajouter un Test de Filtre

Testez que le filtrage par priorité fonctionne :

```typescript
it('filtre les tâches par priorité', async () => {
  const mockTasks = [
    { id: '1', title: 'High priority', priority: 'high', /* ... */ },
    { id: '2', title: 'Low priority', priority: 'low', /* ... */ },
  ];

  // TODO: Mockez l'API
  // TODO: Rendez l'App
  // TODO: Sélectionnez le filtre "high"
  // TODO: Vérifiez que seule la tâche "High priority" est visible
});
```

### 7.2 - Tester une Mutation

Testez la création d'une tâche :

```typescript
it('crée une nouvelle tâche', async () => {
  const user = userEvent.setup();

  // Mock initial fetch (liste vide)
  (globalThis as any).fetch = vi.fn()
    .mockImplementationOnce(() => Promise.resolve({
      json: () => Promise.resolve([]),
      ok: true,
    }))
    // Mock POST create task
    .mockImplementationOnce(() => Promise.resolve({
      json: () => Promise.resolve({ id: '1', title: 'New task' }),
      ok: true,
      status: 201,
    }));

  // TODO: Rendez l'App
  // TODO: Cliquez sur "Create Task"
  // TODO: Remplissez le formulaire
  // TODO: Soumettez
  // TODO: Vérifiez que la tâche apparaît
});
```

---

## 📚 Ressources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Vite Proxy Configuration](https://vitejs.dev/config/server-options.html#server-proxy)

---

## ✅ Checklist de Fin d'Atelier

- [ ] Le backend et le frontend communiquent correctement
- [ ] Vous comprenez le rôle du proxy Vite
- [ ] Vous avez écrit au moins 3 tests frontend
- [ ] Tous les tests passent (`npm test`)
- [ ] Le build réussit (`npm run build`)
- [ ] Le CI/CD fonctionne sur GitHub Actions
- [ ] Vous comprenez comment mocker des appels API
- [ ] Vous savez utiliser React Testing Library

---

## 🎯 Pour Aller Plus Loin

1. **Tests d'intégration E2E** avec Playwright ou Cypress
2. **Accessibility testing** avec jest-axe
3. **Visual regression testing** avec Chromatic
4. **Performance testing** avec Lighthouse CI

---

**Félicitations ! 🎉**

Vous avez complété l'Atelier 2. Vous maîtrisez maintenant :
- ✅ Les tests frontend avec Vitest
- ✅ Le mocking d'APIs
- ✅ La connexion backend-frontend
- ✅ Le CI/CD pour React

**Questions ? Consultez [CONNEXION-BACKEND-FRONTEND.md](./CONNEXION-BACKEND-FRONTEND.md)** 🚀
