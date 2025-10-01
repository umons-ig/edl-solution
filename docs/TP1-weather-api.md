# TP1: API Météo - TDD & CI/CD

**Durée**: 3 heures  
**Branche**: `workshop-1`

## Objectifs

À la fin de ce TP, vous serez capable de:
- Appliquer les principes du développement piloté par les tests (TDD)
- Écrire des tests unitaires avec pytest
- Simuler des dépendances externes avec mock
- Construire une API REST avec FastAPI
- Configurer GitHub Actions pour l'intégration continue
- Gérer les erreurs et cas limites dans les tests

## Prérequis

- Python 3.11+ installé
- uv installé ([voir guide d'installation](setup-guide.md))
- Bases de Git
- Dépôt cloné localement

## Démarrage

```bash
# Passer sur la branche workshop-1
git checkout workshop-1

# Installer les dépendances
uv sync

# Lancer les tests (ils échoueront au début)
uv run pytest -v
```

---

## Partie 1: Projet API Météo (150 minutes)

### Aperçu

Vous allez construire une API REST qui encapsule l'API OpenWeatherMap, fournissant:
- Météo actuelle pour n'importe quelle ville
- Comparaison météo entre villes
- Gestion d'erreurs appropriée
- Cache (optionnel)

### Structure du projet

```
workshop-1/
├── app.py                    # Application FastAPI (incomplet)
├── test_weather_api.py       # Tests (vous guideront)
├── pyproject.toml            # Dépendances
└── .github/workflows/        # Configuration CI (à créer)
```

---

### Exercice 1A: Endpoint Météo de Base (30 minutes)

**Objectif**: Créer un endpoint qui récupère la météo depuis OpenWeatherMap

#### Étape 1: Comprendre le Test (5 min)

Lisez le test dans `test_weather_api.py`:

```python
def test_get_weather_success():
    with patch('app.requests.get') as mock_get:
        # Configuration du mock
        mock_response = Mock()
        mock_response.json.return_value = {
            'main': {'temp': 20},
            'weather': [{'description': 'clear sky'}],
            'name': 'Brussels'
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test
        response = client.get('/weather/Brussels')

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['city'] == 'Brussels'
        assert data['temperature'] == 20
        assert data['description'] == 'clear sky'
```

**Concepts clés**:
- `patch()` - Remplace `requests.get` par un mock
- `Mock()` - Objet de réponse factice
- Pourquoi? On ne veut pas appeler la vraie API dans les tests

#### Étape 2: Lancer le Test (Red) (2 min)

```bash
uv run pytest test_weather_api.py::test_get_weather_success -v
```

**Attendu**: Le test échoue ❌ (l'endpoint n'existe pas)

#### Étape 3: Implémenter l'Endpoint (Green) (20 min)

Ouvrez `app.py` et implémentez l'endpoint `/weather/{city}`:

**Indices**:
- Utilisez le décorateur `@app.get()` de FastAPI
- Appelez l'API OpenWeatherMap avec `requests.get()`
- Parsez la réponse JSON
- Retournez les données formatées

**Détails de l'API**:
- URL: `https://api.openweathermap.org/data/2.5/weather`
- Paramètres: `q` (ville), `appid` (clé API), `units` (metric)
- Vous pouvez utiliser une clé de démo pour les tests (les vrais appels seront mockés)

#### Étape 4: Vérifier que le Test Passe (3 min)

```bash
uv run pytest test_weather_api.py::test_get_weather_success -v
```

**Attendu**: Le test passe ✅

---

### ☕ Pause (10 minutes)

---

### Exercice 1B: Gestion d'Erreurs (25 minutes)

**Objectif**: Gérer les cas où l'API externe échoue

#### Tests à Passer

```python
def test_get_weather_city_not_found():
    # Doit retourner 404 quand la ville n'existe pas
    ...

def test_get_weather_api_timeout():
    # Doit retourner 503 quand l'API expire
    ...

def test_get_weather_connection_error():
    # Doit retourner 503 quand la connexion échoue
    ...
```

#### Vos Tâches

1. **Lire les tests** - Comprendre ce qu'ils attendent
2. **Lancer les tests** - Les voir échouer
3. **Ajouter la gestion d'erreurs**:
   - Capturer `requests.Timeout`
   - Capturer `requests.ConnectionError`
   - Gérer les réponses 404 de l'API
   - Retourner les codes HTTP appropriés
4. **Vérifier que les tests passent**

**Indices**:
- Utilisez des blocs `try/except`
- Utilisez `response.raise_for_status()`
- Levez `HTTPException` de FastAPI
- Ajoutez le paramètre `timeout` à `requests.get()`

```bash
uv run pytest test_weather_api.py::test_get_weather_city_not_found -v
uv run pytest test_weather_api.py::test_get_weather_api_timeout -v
```

---

### Exercice 1C: Comparaison Météo (30 minutes)

**Objectif**: Comparer la météo entre deux villes

#### Design de l'API

```
GET /weather/compare?city1=Brussels&city2=Paris
```

**Réponse attendue**:
```json
{
  "city1": {
    "name": "Brussels",
    "temperature": 15,
    "description": "rainy"
  },
  "city2": {
    "name": "Paris",
    "temperature": 20,
    "description": "sunny"
  },
  "temperature_difference": 5,
  "warmer_city": "Paris"
}
```

#### Vos Tâches

1. **Lire le test** dans `test_weather_api.py::test_compare_weather`
2. **Comprendre la configuration du mock** - Il retourne des données différentes pour chaque ville
3. **Implémenter l'endpoint**:
   - Accepter deux paramètres de requête
   - Récupérer la météo pour les deux villes
   - Calculer la différence de température
   - Déterminer la ville la plus chaude
4. **Lancer le test et vérifier qu'il passe**

**Bonus**: Refactoriser le code commun dans une fonction helper

```bash
uv run pytest test_weather_api.py::test_compare_weather -v
```

---

### Exercice 1D: Cache (Optionnel - 25 minutes)

**Objectif**: Mettre en cache les données météo pour réduire les appels API

#### Pourquoi un Cache?

- Les API externes ont des limites de taux
- Réduire la latence
- Économiser des coûts
- La météo ne change pas toutes les secondes

#### Vos Tâches

1. **Lire le test de cache**
2. **Implémenter un cache en mémoire simple**:
   - Dictionnaire pour stocker ville → (données, timestamp)
   - Vérifier le cache avant d'appeler l'API
   - Mettre en cache les résultats pendant 10 minutes
3. **Vérifier que le test passe**

**Indice**: Utilisez un dictionnaire et `datetime` pour les timestamps

```bash
uv run pytest test_weather_api.py::test_weather_caching -v
```

---

### ☕ Pause (10 minutes)

---

## Partie 2: GitHub Actions CI/CD (30 minutes)

**Objectif**: Automatiser les tests avec GitHub Actions

### Étape 1: Créer le Fichier Workflow (10 min)

Créez `.github/workflows/test.yml`:

```yaml
name: Weather API Tests

on:
  push:
    branches: ['*']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Install uv
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"

    - name: Set up Python
      run: uv python install 3.11

    - name: Install dependencies
      run: uv sync

    - name: Run tests
      run: uv run pytest -v --cov=app
```

### Étape 2: Commit et Push (5 min)

```bash
git add .github/workflows/test.yml
git commit -m "Add GitHub Actions CI workflow"
git push origin workshop-1
```

### Étape 3: Voir les Résultats sur GitHub (5 min)

1. Allez sur votre dépôt GitHub
2. Cliquez sur l'onglet **Actions**
3. Voyez votre workflow s'exécuter
4. Explorez les logs
5. Vérifiez que tous les tests passent ✅

### Étape 4: Créer une Pull Request (10 min)

```bash
# Créer une nouvelle branche pour un petit changement
git checkout -b add-documentation

# Faire un petit changement (ex: ajouter un commentaire)
# Commit et push
git add .
git commit -m "Add documentation"
git push origin add-documentation

# Créer une PR
gh pr create --title "Add documentation" --body "Testing CI workflow"
```

**Observez**:
- GitHub Actions s'exécute automatiquement
- La PR montre l'état des vérifications
- Impossible de merger tant que les vérifications ne passent pas (optionnel: activer la protection de branche)

---

## Partie 3: Conclusion & Révision (10 minutes)

### Ce que Vous Avez Construit

✅ API Météo avec FastAPI  
✅ Tests unitaires avec mocking  
✅ Gestion d'erreurs  
✅ Endpoint de comparaison météo  
✅ Optionnel: Cache  
✅ CI/CD avec GitHub Actions

### Concepts Clés Appris

1. **Développement Piloté par les Tests**
   - Écrire les tests en premier
   - Laisser les tests guider l'implémentation
   - Red → Green → Refactor

2. **Mocking**
   - Simuler les dépendances externes
   - Contrôler le comportement des tests
   - Tester en isolation

3. **Tests d'API**
   - Tester les codes de statut
   - Tester les données de réponse
   - Tester les cas d'erreur

4. **Intégration Continue**
   - Automatiser les tests
   - Détecter les bugs tôt
   - Maintenir la qualité du code

### Prochaines Étapes

**Devoir (Optionnel)**:
1. Ajouter un endpoint de prévisions à 5 jours
2. Ajouter la conversion d'unités de température (°F, °C, K)
3. Améliorer le cache (utiliser Redis)
4. Ajouter plus de gestion d'erreurs
5. Déployer sur une plateforme cloud

**Aperçu du TP 2**:
- Raccourcisseur d'URL avec base de données
- Stratégies de tests d'intégration
- Patterns de tests de base de données
- Fonctionnalités avancées de pytest

---

## Dépannage

### Tests qui Échouent?

```bash
# Lancer avec sortie détaillée
uv run pytest -vv

# Lancer un test spécifique
uv run pytest test_weather_api.py::test_name -v

# Afficher les instructions print
uv run pytest -s
```

### Erreurs d'Import?

```bash
# Réinstaller les dépendances
uv sync --reinstall

# Vérifier la version Python
uv python list
```

### Mock qui ne Fonctionne Pas?

- Vérifiez le chemin du patch: `@patch('app.requests.get')` et non `@patch('requests.get')`
- Assurez-vous que le mock est configuré avant d'appeler la fonction
- Affichez les appels du mock: `print(mock_get.call_args_list)`

📖 **Guide complet de dépannage**: [troubleshooting.md](troubleshooting.md)

---

## Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Guide unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation API OpenWeatherMap](https://openweathermap.org/api)

## Critères d'Évaluation

- [ ] Tous les tests passent localement
- [ ] Le workflow GitHub Actions passe
- [ ] Le code est propre et lisible
- [ ] La gestion d'erreurs est implémentée
- [ ] Le mocking est utilisé correctement
- [ ] L'endpoint de comparaison fonctionne
- [ ] (Optionnel) Le cache est implémenté

---

**Des questions? Demandez à votre instructeur ou consultez le guide de dépannage!**
