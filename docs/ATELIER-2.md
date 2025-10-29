# 🚀 Atelier 2 : CI/CD avec GitHub Actions

**Prérequis :** Atelier 1 terminé (backend et frontend avec tests)

## 📦 Qu'est-ce que CI/CD ?

**CI (Continuous Integration) :**

- Intégration Continue
- À chaque push, les tests s'exécutent automatiquement
- Détecte les bugs immédiatement

**CD (Continuous Deployment) :**

- Déploiement Continu (Atelier 3)
- Si les tests passent, déploiement automatique

**GitHub Actions :**

- Service gratuit de GitHub
- Exécute vos tests sur des serveurs GitHub
- Vérifie chaque commit et pull request

---

## Phase 1 : Comprendre GitHub Actions (20 min)

### Étape 1.1 : Anatomie d'un Workflow

Un workflow GitHub Actions est un fichier **YAML** dans `.github/workflows/`.

**Structure de base :**

```yaml
name: Mon Workflow          # 1️⃣ Nom affiché dans GitHub

on:                         # 2️⃣ Quand s'exécute-t-il ?
  push:
    branches: [main]        # Sur push vers main
  pull_request:
    branches: [main]        # Sur pull request vers main

jobs:                       # 3️⃣ Les tâches à faire
  test:                     # Nom du job
    runs-on: ubuntu-latest  # 4️⃣ Machine virtuelle Linux

    steps:                  # 5️⃣ Les étapes du job
      - name: Récupérer le code
        uses: actions/checkout@v4    # ✅ Action pré-faite

      - name: Lancer les tests
        run: pytest                  # ✅ Commande shell
```

**Concepts clés :**

1. **`name`** : Le nom qui apparaît sur GitHub
2. **`on`** : Les déclencheurs (push, pull_request, schedule, etc.)
3. **`jobs`** : Les tâches (peuvent s'exécuter en parallèle)
4. **`runs-on`** : Le système d'exploitation (ubuntu, windows, macos)
5. **`steps`** : Les étapes du job (séquentielles)

**Deux types de steps :**

- **`uses`** : Utilise une action pré-faite (ex: `actions/checkout@v4`)
- **`run`** : Exécute une commande shell (ex: `pytest`)

---

### Étape 1.2 : Où Trouver les Actions ?

**Actions officielles GitHub :**

- `actions/checkout@v4` - Clone le repo
- `actions/setup-python@v5` - Installe Python
- `actions/setup-node@v4` - Installe Node.js

**Marketplace :**

- <https://github.com/marketplace?type=actions>
- Des milliers d'actions pré-faites

**Documentation :**

- <https://docs.github.com/en/actions>

---

## Phase 2 : Workflow Backend (40 min)

### Étape 2.1 : Créer le Fichier Workflow

```bash
mkdir -p .github/workflows
touch .github/workflows/backend.yml
```

### Étape 2.2 : Écrire le Workflow Backend

Ouvrez `.github/workflows/backend.yml` et copiez ce contenu :

```yaml
name: Backend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test Backend
    runs-on: ubuntu-latest

    steps:
      # Étape 1 : Récupérer le code
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      # Étape 2 : Installer Python
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # Étape 3 : Installer UV
      - name: 📦 Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      # Étape 4 : Installer les dépendances
      - name: 📚 Install dependencies
        run: |
          cd backend
          uv sync

      # Étape 5 : Lancer les tests
      - name: 🧪 Run tests
        run: |
          cd backend
          uv run pytest -v --cov
```

### Étape 2.3 : Comprendre Chaque Ligne

**Ligne par ligne :**

```yaml
name: Backend Tests           # Nom affiché dans l'onglet Actions
```

```yaml
on:
  push:
    branches: [main]          # Déclenche sur push vers main
  pull_request:
    branches: [main]          # Déclenche sur PR vers main
```

```yaml
jobs:
  test:                       # ID du job
    name: Test Backend        # Nom affiché
    runs-on: ubuntu-latest    # Ubuntu (gratuit et rapide)
```

```yaml
steps:
  - name: 📥 Checkout code
    uses: actions/checkout@v4  # Clone le repo
```

**Pourquoi `actions/checkout@v4` ?**

- Sans ça, GitHub Actions ne voit pas votre code !
- C'est toujours la première étape

```yaml
  - name: 🐍 Setup Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.11'   # Version Python
```

```yaml
  - name: 📦 Install UV
    run: |
      curl -LsSf https://astral.sh/uv/install.sh | sh
      echo "$HOME/.cargo/bin" >> $GITHUB_PATH
```

**Explication :**

- `curl -LsSf ... | sh` : Télécharge et installe UV
- `echo "$HOME/.cargo/bin" >> $GITHUB_PATH` : Ajoute UV au PATH pour les étapes suivantes
- Sans cette ligne, `uv` ne serait pas trouvé dans les étapes suivantes

```yaml
  - name: 📚 Install dependencies
    run: |                     # | permet plusieurs lignes
      cd backend
      uv sync
```

```yaml
  - name: 🧪 Run tests
    run: |
      cd backend
      uv run pytest -v --cov
```

**Important :** Ce sont les **mêmes commandes** que vous exécutez localement !

---

### Étape 2.4 : Tester Localement Avant de Pousser

Avant de pousser, vérifiez que ça marche localement :

```bash
cd backend
uv run pytest -v --cov
```

✅ Si ça passe localement, ça devrait passer sur GitHub !

---

### Étape 2.5 : Pousser et Observer

```bash
git add .github/workflows/backend.yml
git commit -m "ci: add backend workflow"
git push origin main
```

**Observer sur GitHub :**

1. Allez sur votre repo GitHub
2. Cliquez sur l'onglet **Actions**
3. Vous verrez votre workflow en cours d'exécution
4. Cliquez dessus pour voir les détails

**Résultat attendu :**

```
✅ Backend Tests
  └─ Test Backend
      ├─ 📥 Checkout code
      ├─ 🐍 Setup Python
      ├─ 📦 Install UV
      ├─ 📚 Install dependencies
      └─ 🧪 Run tests
```

---

## Phase 3 : Workflow Frontend (40 min)

### Étape 3.1 : Créer le Workflow Frontend

```bash
touch .github/workflows/frontend.yml
```

### Étape 3.2 : Écrire le Workflow Frontend

Ouvrez `.github/workflows/frontend.yml` :

```yaml
name: Frontend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test Frontend
    runs-on: ubuntu-latest

    steps:
      # Étape 1 : Récupérer le code
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      # Étape 2 : Installer Node.js
      - name: 🟢 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      # Étape 3 : Installer les dépendances
      - name: 📦 Install dependencies
        run: |
          cd frontend
          npm ci

      # Étape 4 : Lancer les tests
      - name: 🧪 Run tests
        run: |
          cd frontend
          npm test -- --run

      # Étape 5 : Vérifier le build
      - name: 🏗️ Build check
        run: |
          cd frontend
          npm run build
```

### Étape 3.3 : Comprendre les Différences avec le Backend

**`npm ci` vs `npm install` :**

```yaml
- name: 📦 Install dependencies
  run: npm ci    # ✅ Plus rapide et déterministe (pour CI)
```

- `npm ci` : Installe exactement ce qui est dans `package-lock.json`
- `npm install` : Peut mettre à jour les versions (moins fiable)

**Cache npm :**

```yaml
- name: 🟢 Setup Node.js
  uses: actions/setup-node@v4
  with:
    cache: 'npm'   # ✅ Met en cache node_modules
```

Accélère les builds (évite de re-télécharger chaque fois).

**Tests en mode "run once" :**

```yaml
npm test -- --run   # ✅ Lance les tests une fois (pas en mode watch)
```

**Build check :**

```yaml
npm run build   # ✅ Vérifie que le build fonctionne (détecte les erreurs TypeScript)
```

---

### Étape 3.4 : Pousser et Observer

```bash
git add .github/workflows/frontend.yml
git commit -m "ci: add frontend workflow"
git push origin main
```

**Vous verrez maintenant 2 workflows en parallèle :**

```
✅ Backend Tests
✅ Frontend Tests
```

**Les deux s'exécutent en même temps !** 🚀

---

## Phase 4 : Vue d'Ensemble avec Reusable Workflows (30 min)

### Problématique

**Actuellement :**

Vous avez 2 workflows séparés (backend et frontend) qui tournent en parallèle. C'est bien, mais :

- Ils apparaissent dans 2 onglets différents sur GitHub Actions
- Difficile d'avoir une **vue d'ensemble** en un coup d'œil
- Il faut 2 badges dans le README

**Question :** Peut-on avoir un workflow "principal" qui orchestre backend + frontend ?

**Réponse : Oui, avec les Reusable Workflows !**

---

### ✍️ Exercice : Créer un Workflow Full Stack avec Reusable Workflows (30 min)

**🎯 Objectif :** Créer un workflow "CI Pipeline" qui appelle backend et frontend en parallèle

**Étape 1 : Rendre les workflows existants réutilisables**

Modifiez `.github/workflows/backend.yml` :

```yaml
name: Backend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_call:    # ✅ NOUVEAU : Permet d'appeler ce workflow depuis un autre

jobs:
  test:
    name: Test Backend
    runs-on: ubuntu-latest

    steps:
      # ... (reste du workflow inchangé)
```

**Ajoutez `workflow_call:` dans la section `on:`**

Modifiez `.github/workflows/frontend.yml` de la même façon :

```yaml
name: Frontend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_call:    # ✅ NOUVEAU : Permet d'appeler ce workflow depuis un autre

jobs:
  test:
    name: Test Frontend
    runs-on: ubuntu-latest

    steps:
      # ... (reste du workflow inchangé)
```

**Comprendre `workflow_call:` :**

```yaml
on:
  push:
    # ... déclenche sur push comme avant
  workflow_call:    # Permet à d'autres workflows d'appeler celui-ci
```

Le workflow peut maintenant être déclenché de **2 façons** :
1. Par un push/PR (comme avant)
2. **Par un autre workflow** (nouveau !)

---

**Étape 2 : Créer le workflow orchestrateur**

Créez `.github/workflows/ci-pipeline.yml` :

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # Job 1 : Appeler le workflow Backend
  backend:
    name: Backend Tests
    uses: ./.github/workflows/backend.yml    # ✅ Appelle backend.yml

  # Job 2 : Appeler le workflow Frontend (en parallèle)
  frontend:
    name: Frontend Tests
    uses: ./.github/workflows/frontend.yml   # ✅ Appelle frontend.yml

  # Job 3 : Résumé final
  summary:
    name: All Tests Passed
    runs-on: ubuntu-latest
    needs: [backend, frontend]    # ✅ Attend que les DEUX réussissent

    steps:
      - name: ✅ Success
        run: |
          echo "🎉 Tous les tests sont passés !"
          echo "✅ Backend : OK"
          echo "✅ Frontend : OK"
```

**Comprendre `uses:` :**

```yaml
backend:
  uses: ./.github/workflows/backend.yml
```

- `uses:` appelle un autre workflow (comme une fonction !)
- Le chemin commence par `./` (relatif au repo)
- Le workflow appelé doit avoir `workflow_call` dans ses déclencheurs

**Comprendre `needs: [backend, frontend]` :**

```yaml
summary:
  needs: [backend, frontend]
```

- Ce job attend que **backend ET frontend** réussissent
- Si l'un des deux échoue → `summary` ne s'exécute pas

---

**Étape 3 : Tester le workflow**

```bash
git add .github/workflows/
git commit -m "ci: add CI pipeline with reusable workflows"
git push origin main
```

**Sur GitHub Actions, vous verrez maintenant :**

```
CI Pipeline
  ├─ 🔵 Backend Tests
  │   └─ ✅ Test Backend (20s)
  ├─ 🔵 Frontend Tests
  │   └─ ✅ Test Frontend (25s)
  └─ ✅ All Tests Passed (2s)
```

**Et aussi (workflows individuels toujours actifs) :**

```
Backend Tests
  └─ ✅ Test Backend (20s)

Frontend Tests
  └─ ✅ Test Frontend (25s)
```

**Avantages de cette approche :**

1. ✅ **Vue d'ensemble** : Tout regroupé dans "CI Pipeline"
2. ✅ **Workflows séparés** : Backend et Frontend restent indépendants
3. ✅ **Parallélisation** : Les deux tournent en même temps
4. ✅ **Pas de duplication** : Pas besoin de copier-coller le code
5. ✅ **Job de résumé** : Confirmation visuelle que tout est OK

---

**Étape 4 : Modifier le README avec un seul badge principal**

Modifiez `README.md` :

```markdown
# 🚀 TaskFlow - Application de Gestion de Tâches

![CI Pipeline](https://github.com/VOTRE_USERNAME/edl-starter/workflows/CI%20Pipeline/badge.svg)

> Application full-stack pour gérer vos tâches avec FastAPI et React + CI/CD automatisé

## 📊 Status CI/CD

- ✅ **CI Pipeline** : Tests backend + frontend en parallèle
- ✅ **Protection de branche** : Merge bloqué si tests échouent

<details>
<summary>Voir les workflows individuels</summary>

![Backend Tests](https://github.com/VOTRE_USERNAME/edl-starter/workflows/Backend%20Tests/badge.svg)
![Frontend Tests](https://github.com/VOTRE_USERNAME/edl-starter/workflows/Frontend%20Tests/badge.svg)

</details>
```

**Résultat :**

Un **seul badge principal** en haut qui montre l'état global. Les badges individuels sont dans un accordéon dépliable (`<details>`) !

---

### Comparaison : Avant vs Après

**Avant (workflows séparés uniquement) :**

```
❌ Dispersé : 2 onglets à surveiller
✅ Débogage : Facile de voir quelle partie échoue
✅ Simple : Facile à comprendre
```

**Après (avec CI Pipeline) :**

```
✅ Vue d'ensemble : Tout en un endroit
✅ Débogage : On voit toujours les détails
✅ Professional : C'est ce qu'on fait en production
✅ Les workflows individuels fonctionnent toujours séparément
```

**Le meilleur des deux mondes !**

---

### 💡 Cas d'Usage Réels

**Quand utiliser les Reusable Workflows :**

- ✅ Monorepos (backend, frontend, mobile dans un repo)
- ✅ Workflows complexes (lint → test → build → deploy)
- ✅ Plusieurs environnements (dev, staging, prod)
- ✅ Vue d'ensemble pour les Pull Requests

**Exemple d'une grande entreprise :**

```yaml
name: Production Deploy

jobs:
  backend:
    uses: ./.github/workflows/backend.yml
  frontend:
    uses: ./.github/workflows/frontend.yml
  mobile:
    uses: ./.github/workflows/mobile.yml

  deploy:
    needs: [backend, frontend, mobile]
    uses: ./.github/workflows/deploy.yml
```

---

## Phase 5 : Déboguer un Échec Volontaire (30 min)

### Étape 4.1 : Pourquoi Apprendre à Déboguer ?

**Dans la vraie vie :**

- ❌ Les workflows échouent souvent
- 🔍 Il faut savoir lire les logs
- 🐛 Reproduire localement pour corriger

**Apprenons en cassant quelque chose exprès !**

---

### ✍️ Exercice : Introduire un Bug (10 min)

**Objectif :** Modifier un test pour qu'il échoue volontairement.

Ouvrez `backend/tests/test_api.py` et **modifiez** le test `test_health_check` :

```python
def test_health_check(client):
    """The health endpoint should confirm the API is running."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "BROKEN"  # ❌ Volontairement faux !
```

**Pourquoi "BROKEN" ?**

- Le vrai statut est `"healthy"`
- Ce test va échouer !

**Pousser le bug :**

```bash
git add backend/tests/test_api.py
git commit -m "test: intentional failure for learning"
git push origin main
```

---

### Étape 4.2 : Observer l'Échec (5 min)

**Sur GitHub Actions :**

1. Allez dans l'onglet **Actions**
2. Vous verrez ❌ **Backend Tests** en rouge
3. Cliquez dessus

**Vous verrez :**

```
❌ Backend Tests
  └─ Test Backend
      ├─ ✅ 📥 Checkout code
      ├─ ✅ 🐍 Setup Python
      ├─ ✅ 📦 Install UV
      ├─ ✅ 📚 Install dependencies
      └─ ❌ 🧪 Run tests  ← ICI LE PROBLÈME
```

---

### Étape 4.3 : Analyser les Logs (10 min)

**Cliquez sur l'étape "🧪 Run tests".**

**Vous verrez les logs :**

```
tests/test_api.py::test_health_check FAILED

================================ FAILURES ================================
_________________________ test_health_check __________________________

client = <starlette.testclient.TestClient object at 0x...>

    def test_health_check(client):
        response = client.get("/health")
        assert response.status_code == 200
>       assert response.json()["status"] == "BROKEN"
E       AssertionError: assert 'healthy' == 'BROKEN'
E         - BROKEN
E         + healthy

tests/test_api.py:20: AssertionError
======================== short test summary info ========================
FAILED tests/test_api.py::test_health_check - AssertionError: ...
======================== 1 failed, 18 passed in 0.52s ====================
```

**Questions à se poser :**

1. **Quel test échoue ?** → `test_health_check`
2. **Quelle ligne ?** → `tests/test_api.py:20`
3. **Quelle est l'erreur ?** → Attend "BROKEN", reçoit "healthy"
4. **Comment reproduire localement ?**

---

### Étape 4.4 : Reproduire Localement (5 min)

**Même commande que dans le workflow :**

```bash
cd backend
uv run pytest tests/test_api.py::test_health_check -v
```

**Vous verrez la même erreur !**

```
FAILED tests/test_api.py::test_health_check - AssertionError: assert 'healthy' == 'BROKEN'
```

**Maintenant corrigez :**

```python
def test_health_check(client):
    """The health endpoint should confirm the API is running."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"  # ✅ Correct !
```

**Vérifiez localement :**

```bash
uv run pytest tests/test_api.py::test_health_check -v
```

✅ **Le test passe !**

---

### Étape 4.5 : Pousser la Correction (5 min)

```bash
git add backend/tests/test_api.py
git commit -m "fix: correct health check assertion"
git push origin main
```

**Sur GitHub Actions :**

```
✅ Backend Tests  ← De nouveau vert !
```

---

### Étape 4.6 : Leçons Apprises

**Ce que vous avez appris :**

1. ✅ Lire les logs GitHub Actions
2. ✅ Identifier la ligne qui échoue
3. ✅ Reproduire l'erreur localement
4. ✅ Corriger et vérifier
5. ✅ Re-pousser

**Principe clé : Si ça passe localement, ça passera sur GitHub !**

---

## Phase 5 : Vérification Finale (20 min)

### Étape 5.1 : Créer une Pull Request (10 min)

**Pourquoi une PR ?**

Les workflows s'exécutent aussi sur les Pull Requests !

**Créer une branche :**

```bash
git checkout -b feature/test-pr
```

**Faire un petit changement :**

```python
# Dans backend/src/app.py
@app.get("/")
async def root():
    return {
        "message": "Welcome to TaskFlow API v2.0",  # Changé !
        "version": "1.0.0",
        "docs": "/docs"
    }
```

**Pousser la branche :**

```bash
git add backend/src/app.py
git commit -m "feat: update welcome message"
git push origin feature/test-pr
```

**Créer la PR sur GitHub :**

1. Allez sur votre repo GitHub
2. Cliquez sur **"Compare & pull request"**
3. Créez la PR

**Vous verrez les checks s'exécuter :**

```
⏳ Backend Tests — In progress
⏳ Frontend Tests — In progress
```

Puis :

```
✅ Backend Tests — Passed
✅ Frontend Tests — Passed
✅ All checks have passed
```

**Vous pouvez maintenant merger en toute confiance !**

---

## 🎁 BONUS : Workflow Java (Optionnel - 30 min)

**Pour les étudiants qui ont terminé les 5 phases principales.**

### Objectif

Appliquer les concepts CI/CD sur les exercices Java de l'Atelier 1.

---

### Étape Bonus 1 : Rappel des Exercices Java

Si vous avez fait les exercices BONUS de l'Atelier 1, vous avez 3 projets Java :

```
java-exercises/
├── calculator/        # Calculatrice avec opérations de base
├── string-utils/      # Manipulation de chaînes
└── bank-account/      # Gestion de compte bancaire
```

---

### Étape Bonus 2 : Créer le Workflow Java

Créez `.github/workflows/java.yml` :

```yaml
name: Java Tests (Optional)

# Workflow optionnel pour les exercices bonus Java
on:
  push:
    branches: [main]
    paths:
      - 'java-exercises/**'
  pull_request:
    branches: [main]
    paths:
      - 'java-exercises/**'
  workflow_dispatch:  # Permet lancement manuel

jobs:
  test:
    name: Test Java Exercises
    runs-on: ubuntu-latest

    steps:
      # Étape 1 : Récupérer le code
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      # Étape 2 : Installer Java
      - name: ☕ Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      # Étape 3 : Tester Calculator
      - name: 🧮 Test Calculator
        working-directory: java-exercises/calculator
        run: |
          javac -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar *.java
          java -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar org.junit.runner.JUnitCore CalculatorTest

      # Étape 4 : Tester String Utils
      - name: 📝 Test String Utils
        working-directory: java-exercises/string-utils
        run: |
          javac -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar *.java
          java -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar org.junit.runner.JUnitCore StringUtilsTest

      # Étape 5 : Tester Bank Account
      - name: 🏦 Test Bank Account
        working-directory: java-exercises/bank-account
        run: |
          javac -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar *.java
          java -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar org.junit.runner.JUnitCore BankAccountTest
```

---

### Étape Bonus 3 : Comprendre les Différences

**`paths:` - Déclenchement Conditionnel**

```yaml
on:
  push:
    paths:
      - 'java-exercises/**'
```

➡️ Le workflow ne s'exécute **que** si vous modifiez des fichiers dans `java-exercises/`

**`workflow_dispatch:` - Lancement Manuel**

```yaml
on:
  workflow_dispatch:
```

➡️ Vous pouvez lancer le workflow manuellement depuis l'onglet **Actions** sur GitHub

**`working-directory:` - Répertoire de Travail**

```yaml
- name: 🧮 Test Calculator
  working-directory: java-exercises/calculator
  run: |
    javac -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar *.java
```

➡️ Définit le répertoire de travail pour toutes les commandes `run` de cette étape

**Pourquoi `working-directory` au lieu de `cd` ?**

- ✅ Plus propre et plus clair
- ✅ Fonctionne mieux avec les chemins relatifs
- ✅ Standard GitHub Actions

**`javac` et `java` - Compilation et Exécution**

```bash
javac -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar *.java
java -cp .:../lib/junit-4.13.2.jar:../lib/hamcrest-core-1.3.jar org.junit.runner.JUnitCore CalculatorTest
```

- `-cp` : Classpath (où trouver JUnit)
- `.:../lib/...` : Dossier actuel + JARs dans ../lib
- `*.java` : Compile tous les fichiers Java
- `JUnitCore` : Lance les tests JUnit

---

### Étape Bonus 4 : Tester le Workflow

**Option 1 : Push un changement Java**

```bash
# Modifier un fichier Java
echo "// Test CI" >> java-exercises/calculator/Calculator.java

git add java-exercises/
git commit -m "test: trigger Java workflow"
git push
```

**Option 2 : Lancement Manuel**

1. Allez sur **Actions** dans GitHub
2. Cliquez sur **Java Tests (Optional)**
3. Cliquez sur **Run workflow**
4. Sélectionnez la branche `main`
5. Cliquez sur **Run workflow**

---

### Étape Bonus 5 : Voir les Résultats

Vous devriez voir dans les logs :

```
🧮 Test Calculator
  Compiling...
  Running tests...
  JUnit version 4.13.2
  ..........
  Time: 0.012
  OK (10 tests)

📝 Test String Utils
  ...

🏦 Test Bank Account
  ...
```

✅ **Tous vos exercices Java sont testés automatiquement !**

---

### 🤔 Exercice de Réflexion

**Pourquoi 3 workflows séparés (backend, frontend, java) plutôt qu'un seul ?**

<details>
<summary>Cliquez pour voir la réponse</summary>

**Avantages :**

1. ✅ **Parallélisation** : Les 3 workflows s'exécutent en parallèle → plus rapide
2. ✅ **Débogage** : Si backend échoue, vous savez immédiatement où chercher
3. ✅ **Optionnel** : Java ne s'exécute que si `java-exercises/` est modifié
4. ✅ **Lisibilité** : Chaque workflow est simple et focalisé

**Inconvénient :**

1. ❌ Plus de fichiers à gérer (mais seulement 3)

**En production, on préfère souvent plusieurs workflows ciblés plutôt qu'un seul monolithique.**

</details>

---

## 🐛 Erreurs Fréquentes

### ❌ Workflow ne se déclenche pas

**Cause :** Fichier mal placé ou syntaxe YAML invalide

**Solution :** Vérifiez :

- Le fichier est dans `.github/workflows/`
- L'extension est `.yml` ou `.yaml`
- Pas d'erreurs de syntaxe (indentation !)

### ❌ `uv: command not found`

**Cause :** UV n'est pas dans le PATH après installation

**Solution :** Ajoutez `echo "$HOME/.cargo/bin" >> $GITHUB_PATH` après l'installation de UV

### ❌ `actions/checkout@v4` ne fonctionne pas

**Cause :** Problème de permissions GitHub

**Solution :** Ajoutez l'étape `actions/setup-node@v4`

### ❌ Tests qui passent localement mais échouent sur GitHub

**Causes possibles :**

1. Variable d'environnement manquante
2. Dépendance système manquante
3. Timezone différente

**Déboguer :** Reproduisez exactement les mêmes commandes localement

---

## Phase 6 : Séparer Tests Rapides et Lents (45 min)

### Problématique

**Dans un projet réel :**

- Tests unitaires : Très rapides (5-10 secondes)
- Tests d'intégration : Moyens (30 secondes - 1 minute)
- Tests E2E (End-to-End) : Très lents (5-10 minutes)

**Problème actuel :**

Tous les tests s'exécutent à chaque commit → on attend 10 minutes pour savoir si un simple changement fonctionne !

**Solution :**

Séparer les tests en plusieurs jobs avec des déclencheurs différents.

---

### ✍️ Exercice 1 : Créer des Tests E2E (15 min)

**🎯 Objectif :** Marquer certains tests comme "lents" pour pouvoir les séparer

**Étape 1 : Configurer pytest pour supporter les markers**

Ouvrez `backend/tests/conftest.py` et ajoutez :

```python
import pytest

def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "e2e: mark test as end-to-end test (slow, integration test)"
    )
```

**Étape 2 : Créer un test E2E**

Ajoutez ce test dans `backend/tests/test_api.py` :

```python
import pytest

@pytest.mark.e2e
def test_full_task_workflow(client):
    """Test E2E : Workflow complet CRUD d'une tâche."""
    # 1. Créer une tâche
    response = client.post("/tasks", json={
        "title": "Test E2E Workflow",
        "priority": "high"
    })
    assert response.status_code == 201
    task_id = response.json()["id"]

    # 2. Lire la tâche créée
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test E2E Workflow"

    # 3. Modifier la tâche
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Modified Task",
        "status": "done"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "done"

    # 4. Supprimer la tâche
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # 5. Vérifier qu'elle n'existe plus
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
```

**Étape 3 : Tester localement**

```bash
cd backend

# Lancer SEULEMENT les tests rapides (sans E2E)
uv run pytest -v -m "not e2e"

# Lancer SEULEMENT les tests E2E
uv run pytest -v -m "e2e"

# Lancer tous les tests
uv run pytest -v
```

**Résultat attendu :**

```bash
# Tests rapides (sans E2E)
$ uv run pytest -v -m "not e2e"
==================== 18 passed in 2.15s ====================

# Tests E2E uniquement
$ uv run pytest -v -m "e2e"
==================== 1 passed in 0.52s ====================
```

---

### ✍️ Exercice 2 : Workflow avec Tests Séparés (30 min)

**🎯 Objectif :** Créer un workflow où les tests rapides tournent sur chaque PR, mais les tests E2E seulement sur main

**Créer `.github/workflows/backend-split.yml` :**

```yaml
name: Backend Tests (Split)

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  # Job 1 : Tests unitaires rapides (toujours)
  unit-tests:
    name: Unit Tests (Fast)
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 📦 Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      - name: 📚 Install dependencies
        run: |
          cd backend
          uv sync

      - name: 🧪 Run unit tests only
        run: |
          cd backend
          uv run pytest -v -m "not e2e"

  # Job 2 : Tests E2E lents (seulement sur main)
  e2e-tests:
    name: E2E Tests (Slow)
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'    # ✅ CONDITION : seulement sur main

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 📦 Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      - name: 📚 Install dependencies
        run: |
          cd backend
          uv sync

      - name: 🧪 Run E2E tests only
        run: |
          cd backend
          uv run pytest -v -m "e2e"
```

**Comprendre la condition `if:` :**

```yaml
e2e-tests:
  if: github.ref == 'refs/heads/main'
```

- `github.ref` contient la référence Git complète
- Sur la branche `main` : `refs/heads/main`
- Sur une PR : `refs/pull/123/merge`
- **Résultat :** Les tests E2E ne tournent PAS sur les PRs !

**Tester le workflow :**

```bash
git add .
git commit -m "ci: add split tests workflow"
git push origin main
```

**Sur GitHub Actions, vous verrez :**

**Pour une Pull Request :**
```
Backend Tests (Split)
  └─ ✅ Unit Tests (Fast) — 15s
```

**Pour un push sur main :**
```
Backend Tests (Split)
  ├─ ✅ Unit Tests (Fast) — 15s
  └─ ✅ E2E Tests (Slow) — 45s
```

**Avantages :**

- Les développeurs obtiennent un feedback rapide sur les PRs (15s)
- La branche main est testée complètement avant déploiement (60s)
- Économise des minutes GitHub Actions

---

## Phase 7 : Protection de Branche et Pull Requests (40 min)

### ✍️ Exercice 3 : Activer la Protection de Branche (15 min)

**🎯 Objectif :** Empêcher les merges si les tests échouent

**Étape 1 : Configurer la protection sur GitHub**

1. Allez sur votre repo GitHub
2. Cliquez sur **Settings** → **Branches**
3. Cliquez sur **Add rule** (ou **Add branch protection rule**)
4. Dans "Branch name pattern", tapez : `main`
5. Cochez les options suivantes :
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
6. Dans la barre de recherche "Status checks", tapez et sélectionnez :
   - `Unit Tests (Fast)` (du workflow backend-split.yml)
   - `Test Backend` (du workflow backend.yml)
   - `Test Frontend` (du workflow frontend.yml)
7. Cliquez sur **Create** ou **Save changes**

**Note importante :** Cherchez le **nom du job**, pas le nom du workflow !

**Étape 2 : Tester la protection avec un test cassé**

Créez une nouvelle branche :

```bash
git checkout -b test/broken-check
```

Cassez volontairement un test dans `backend/tests/test_api.py` :

```python
def test_health_check(client):
    """The health endpoint should confirm the API is running."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "INTENTIONALLY_BROKEN"  # ❌ Faux !
```

Poussez la branche :

```bash
git add backend/tests/test_api.py
git commit -m "test: intentionally break health check"
git push origin test/broken-check
```

**Étape 3 : Créer une Pull Request**

1. Allez sur GitHub
2. Cliquez sur **Compare & pull request**
3. Créez la PR

**Résultat attendu :**

Vous verrez dans la PR :

```
❌ Some checks were not successful
   1 failing check

   Unit Tests (Fast) — Failed

⚠️ Merging is blocked
   Required status checks must pass before merging
```

Le bouton **Merge pull request** sera **grisé** et **non cliquable** !

**Étape 4 : Corriger et merger**

Corrigez le test :

```python
def test_health_check(client):
    """The health endpoint should confirm the API is running."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"  # ✅ Correct !
```

```bash
git add backend/tests/test_api.py
git commit -m "fix: restore correct health check"
git push origin test/broken-check
```

Maintenant sur la PR :

```
✅ All checks have passed
   3 successful checks

   Unit Tests (Fast) — Passed
   Test Backend — Passed
   Test Frontend — Passed
```

Le bouton **Merge pull request** est maintenant **vert** et **cliquable** !

---

### ✍️ Exercice 4 : Jobs avec Dépendances (needs) (25 min)

**🎯 Objectif :** Créer une chaîne de jobs : Lint → Test → Build

**Créer `.github/workflows/frontend-chain.yml` :**

```yaml
name: Frontend Chain

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  # Job 1 : Linting du code
  lint:
    name: Lint Code
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🟢 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: 📦 Install dependencies
        run: |
          cd frontend
          npm ci

      - name: 🔍 Run ESLint
        run: |
          cd frontend
          npm run lint

  # Job 2 : Tests (dépend de lint)
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint    # ✅ Attend que 'lint' réussisse

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🟢 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: 📦 Install dependencies
        run: |
          cd frontend
          npm ci

      - name: 🧪 Run tests
        run: |
          cd frontend
          npm test -- --run

  # Job 3 : Build (dépend de test)
  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: test    # ✅ Attend que 'test' réussisse

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🟢 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: 📦 Install dependencies
        run: |
          cd frontend
          npm ci

      - name: 🏗️ Build
        run: |
          cd frontend
          npm run build

      - name: 📤 Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: frontend-dist
          path: frontend/dist/
          retention-days: 7
```

**Comprendre `needs:` :**

```yaml
test:
  needs: lint    # Ce job attend que 'lint' réussisse

build:
  needs: test    # Ce job attend que 'test' réussisse
```

**Chaîne de dépendances :**

```
lint → test → build
```

- Si `lint` échoue → `test` et `build` ne s'exécutent PAS
- Si `test` échoue → `build` ne s'exécute PAS
- **Économise du temps et des ressources !**

**Comprendre `actions/upload-artifact` :**

```yaml
- name: 📤 Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: frontend-dist
    path: frontend/dist/
    retention-days: 7
```

- Sauvegarde le dossier `dist/` (résultat du build)
- Disponible pendant 7 jours
- Téléchargeable depuis l'interface GitHub Actions

**Tester le workflow :**

```bash
git add .github/workflows/frontend-chain.yml
git commit -m "ci: add frontend chain workflow"
git push origin main
```

**Sur GitHub Actions, vous verrez :**

```
Frontend Chain
  ├─ 🔍 Lint Code (1/3) → Running...
  └─ ⏳ Run Tests (2/3) → Waiting...
  └─ ⏳ Build Application (3/3) → Waiting...
```

Puis :

```
Frontend Chain
  ├─ ✅ Lint Code (15s)
  ├─ ✅ Run Tests (20s)
  └─ ✅ Build Application (25s)
```

**Pour télécharger l'artifact :**

1. Cliquez sur le workflow terminé
2. Scrollez jusqu'à "Artifacts"
3. Cliquez sur `frontend-dist` pour télécharger le ZIP

---

## Phase 8 : Optimisation avec Cache (25 min)

### Problème : Réinstaller les Dépendances à Chaque Fois

**Actuellement :**

- Chaque workflow réinstalle toutes les dépendances
- Backend : `uv sync` prend 30-60 secondes
- Frontend : `npm ci` prend 20-40 secondes

**Solution : Utiliser le cache !**

---

### ✍️ Exercice 5 : Ajouter du Cache pour UV (25 min)

**🎯 Objectif :** Réduire le temps d'installation des dépendances avec `actions/cache`

**Modifier `.github/workflows/backend.yml` :**

```yaml
name: Backend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test Backend
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 📦 Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      # ✅ NOUVEAU : Cache pour les dépendances UV
      - name: 💾 Cache UV dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/uv
          key: ${{ runner.os }}-uv-${{ hashFiles('backend/pyproject.toml', 'backend/uv.lock') }}
          restore-keys: |
            ${{ runner.os }}-uv-

      - name: 📚 Install dependencies
        run: |
          cd backend
          uv sync

      - name: 🧪 Run tests
        run: |
          cd backend
          uv run pytest -v --cov
```

**Comprendre `actions/cache@v4` :**

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('backend/pyproject.toml', 'backend/uv.lock') }}
    restore-keys: |
      ${{ runner.os }}-uv-
```

**Paramètres :**

1. **`path:`** - Dossier à mettre en cache
   - `~/.cache/uv` : Cache UV des packages Python

2. **`key:`** - Identifiant unique du cache
   - `${{ runner.os }}` : OS (ubuntu, macos, windows)
   - `${{ hashFiles(...) }}` : Hash des fichiers de dépendances
   - Si `pyproject.toml` change → Nouveau hash → Nouveau cache

3. **`restore-keys:`** - Clés de fallback
   - Si pas de correspondance exacte, cherche `ubuntu-latest-uv-*`
   - Utile si seulement `uv.lock` a changé légèrement

**Comment ça fonctionne :**

```
1ère exécution :
  ├─ Cache miss (pas de cache trouvé)
  ├─ uv sync (télécharge tout) → 60s
  └─ Sauvegarde le cache

2ème exécution (même pyproject.toml) :
  ├─ Cache hit (cache trouvé !)
  ├─ Restaure le cache → 5s
  └─ uv sync (vérifie, rien à faire) → 5s
  Total : 10s au lieu de 60s !

Si pyproject.toml change :
  ├─ Cache miss (hash différent)
  ├─ uv sync (télécharge nouveaux packages) → 60s
  └─ Sauvegarde le nouveau cache
```

**Tester le cache :**

```bash
git add .github/workflows/backend.yml
git commit -m "ci: add cache for backend dependencies"
git push origin main
```

Lancez le workflow **2 fois** et comparez les temps dans les logs !

**Résultat attendu :**

- **1ère exécution :** `Cache not found` → 60 secondes
- **2ème exécution :** `Cache restored` → 10 secondes

**Économie : 50 secondes par workflow ! 🚀**

---

**Note pour le frontend :**

Le cache est déjà activé automatiquement avec :

```yaml
- name: 🟢 Setup Node.js
  uses: actions/setup-node@v4
  with:
    cache: 'npm'    # ✅ Cache automatique pour npm !
```

Pas besoin d'ajouter `actions/cache` manuellement pour npm/yarn/pnpm.

---

## Phase 9 : Contrôle de Concurrence (15 min)

### Problème : Workflows qui s'accumulent

**Scénario :**

Vous pushez 3 commits rapides sur une PR :

```
Commit 1 → Workflow démarre (durée : 2 min)
Commit 2 → Workflow démarre (durée : 2 min)
Commit 3 → Workflow démarre (durée : 2 min)
```

Les 3 workflows tournent en parallèle, mais seul le dernier compte !

**Solution : Annuler les workflows obsolètes**

---

### ✍️ Exercice 6 : Ajouter le Contrôle de Concurrence (15 min)

**🎯 Objectif :** Annuler les anciennes exécutions quand un nouveau commit arrive

**Modifier `.github/workflows/backend.yml` :**

```yaml
name: Backend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# ✅ NOUVEAU : Contrôle de concurrence
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test Backend
    runs-on: ubuntu-latest

    steps:
      # ... (reste du workflow inchangé)
```

**Comprendre `concurrency:` :**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

- **`group:`** - Identifiant du groupe de concurrence
  - `${{ github.workflow }}` : Nom du workflow (ex: "Backend Tests")
  - `${{ github.ref }}` : Référence (ex: "refs/pull/123/merge")
  - Groupe = "Backend Tests-refs/pull/123/merge"

- **`cancel-in-progress: true`** - Annule les exécutions en cours

**Comportement :**

```
Commit 1 → Workflow A démarre
Commit 2 → Workflow A annulé, Workflow B démarre
Commit 3 → Workflow B annulé, Workflow C démarre
```

Seul le dernier workflow tourne → **économise des minutes GitHub Actions !**

**Appliquer à tous les workflows :**

Ajoutez le même bloc `concurrency:` à :
- `.github/workflows/frontend.yml`
- `.github/workflows/backend-split.yml`
- `.github/workflows/frontend-chain.yml`

**Tester :**

1. Créez une branche et une PR
2. Faites 3 commits rapides (moins de 30s entre chaque)
3. Observez sur GitHub Actions

Vous verrez les anciennes exécutions **annulées** automatiquement !

---

## Phase 10 : Badges et Documentation (15 min)

### ✍️ Exercice 7 : Ajouter des Badges de Status (15 min)

**🎯 Objectif :** Afficher l'état des workflows directement dans le README

**Les badges montrent visuellement l'état :**

- ✅ **Vert** = Tous les tests passent
- ❌ **Rouge** = Tests échouent
- 🟡 **Jaune** = En cours d'exécution

**Format du badge :**

```
https://github.com/OWNER/REPO/workflows/WORKFLOW_NAME/badge.svg
```

**Exemple concret :**

Si votre repo est `github.com/tanguyvans/edl-starter` et votre workflow s'appelle "Backend Tests" :

```
https://github.com/tanguyvans/edl-starter/workflows/Backend%20Tests/badge.svg
```

**Note :** Remplacez les espaces par `%20`

**Modifier `README.md` :**

Ajoutez en haut du fichier :

```markdown
# 🚀 TaskFlow - Application de Gestion de Tâches

![Backend Tests](https://github.com/VOTRE_USERNAME/edl-starter/workflows/Backend%20Tests/badge.svg)
![Frontend Tests](https://github.com/VOTRE_USERNAME/edl-starter/workflows/Frontend%20Tests/badge.svg)
![Java Tests](https://github.com/VOTRE_USERNAME/edl-starter/workflows/Java%20Tests%20(Optional)/badge.svg)

> Application full-stack pour gérer vos tâches avec FastAPI et React + CI/CD automatisé

## 📊 Status CI/CD

- ✅ **Backend** : Tests unitaires et d'intégration avec pytest
- ✅ **Frontend** : Tests Vitest avec couverture de code
- ✅ **CI/CD** : GitHub Actions avec protection de branche
- ✅ **Cache** : Dépendances cachées pour builds rapides
```

**Badges cliquables (optionnel) :**

```markdown
[![Backend Tests](https://github.com/VOTRE_USERNAME/edl-starter/workflows/Backend%20Tests/badge.svg)](https://github.com/VOTRE_USERNAME/edl-starter/actions)
```

**Tester :**

```bash
git add README.md
git commit -m "docs: add CI/CD status badges"
git push origin main
```

Rafraîchissez votre repo GitHub → Les badges s'affichent en haut du README !

**Autres badges utiles (shields.io) :**

```markdown
![Python](https://img.shields.io/badge/python-3.11-blue)
![Node.js](https://img.shields.io/badge/node-18-green)
![License](https://img.shields.io/badge/license-MIT-orange)
```

---

## 🎓 Récapitulatif de l'Atelier 2

**Ce que vous avez appris :**

### Phase 1-2 : Bases
- ✅ Créer des workflows GitHub Actions
- ✅ Déclencher sur push et pull_request
- ✅ Installer dépendances (Python, Node.js)

### Phase 3-5 : Tests et Débogage
- ✅ Lancer tests backend et frontend
- ✅ Déboguer les échecs de workflow
- ✅ Créer et tester des Pull Requests

### Phase 6 : Tests Séparés
- ✅ Séparer tests unitaires (rapides) et E2E (lents)
- ✅ Utiliser `if: github.ref == 'refs/heads/main'`
- ✅ Économiser du temps sur les PRs

### Phase 7 : Protection et Dépendances
- ✅ Activer la protection de branche
- ✅ Bloquer les merges si tests échouent
- ✅ Créer des chaînes de jobs avec `needs:`
- ✅ Uploader des artifacts

### Phase 8-9 : Optimisation
- ✅ Ajouter du cache pour accélérer les builds
- ✅ Contrôle de concurrence pour annuler workflows obsolètes

### Phase 10 : Documentation
- ✅ Ajouter des badges de status dans le README

**Temps total : ~4-5 heures**

---

## 📚 Ressources

- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Marketplace Actions](https://github.com/marketplace?type=actions)
- [YAML Syntax](https://yaml.org/)
- [Actions Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

---

## 🚀 Prochaine Étape : Atelier 3

Dans l'Atelier 3, vous allez **déployer votre application** :

- Migrer vers PostgreSQL (base de données réelle)
- Déployer sur Render (production)
- Configurer le CD (Continuous Deployment)

**Prêt pour la production ? 🚀**

---

**Version 2.0** - Atelier 2 CI/CD Simplifié
