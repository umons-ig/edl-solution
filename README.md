# Workshop 1 : API Météo - Fondamentaux TDD & CI/CD

**Durée** : 3 heures
**Objectif** : Apprendre le développement piloté par les tests (TDD) en construisant une API météo

## 🎯 Ce que vous allez construire

Une API REST qui encapsule l'API météo Open-Meteo avec :
- ✅ Endpoint météo actuelle
- ✅ Comparaison météo entre deux villes
- ✅ Gestion d'erreurs
- ✅ Cache (optionnel)
- ✅ Tests automatisés avec GitHub Actions

## 🚀 Démarrage rapide

```bash
# Installer les dépendances
uv sync

# Lancer les tests (ils vont échouer - votre mission est de les faire passer !)
uv run pytest -v

# Lancer l'API (une fois implémentée)
uv run uvicorn app:app --reload
```

**Note** : Pas besoin de clé API ! Utilise Open-Meteo (gratuit, sans inscription). Tous les tests utilisent des mocks de toute façon.

## 📚 Structure du workshop

### Partie 1 : Démo calculatrice (30 min)
Introduction rapide au TDD avec un exemple de calculatrice simple.

**Consulter les exemples :**
```bash
git checkout examples
uv sync
uv run pytest calculator/test_calculator.py -v
git checkout workshop-1  # Revenir quand c'est fait
```

### Partie 2 : Exercices API Météo (120 min)

#### Exercice 2A : Endpoint météo basique (30 min)
**Objectif** : Implémenter `GET /weather/{city}`

**Test à faire passer** : `test_get_weather_success`

**Étapes** :
1. Lire le test dans `test_weather_api.py`
2. Exécuter `uv run pytest test_weather_api.py::test_get_weather_success -v` (voir l'échec)
3. Implémenter l'endpoint dans `app.py`
4. Faire passer le test ✅

#### Exercice 2B : Gestion d'erreurs (25 min)
**Objectif** : Gérer les échecs d'API gracieusement

**Tests à faire passer** :
- `test_get_weather_city_not_found` - Retourner 404 pour les villes invalides
- `test_get_weather_api_timeout` - Retourner 503 quand l'API timeout
- `test_get_weather_connection_error` - Gérer les erreurs de connexion

#### Exercice 2C : Comparaison météo (30 min)
**Objectif** : Implémenter `GET /weather/compare?city1=X&city2=Y`

**Test à faire passer** : `test_compare_weather`

Comparer la météo entre deux villes et calculer la différence de température.

#### Exercice 2D : Cache (Optionnel - 25 min)
**Objectif** : Mettre en cache les résultats pour réduire les appels API

**Test à faire passer** : `test_weather_caching`

Implémenter un cache en mémoire simple avec un TTL de 10 minutes.

### Partie 3 : GitHub Actions CI/CD (30 min)

**Objectif** : Automatiser les tests avec GitHub Actions

**Guide** : Suivre [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) pour les instructions détaillées

**Tâches** :
1. Créer `.github/workflows/test.yml`
2. Ajouter la configuration du workflow (voir le guide pour le template)
3. Commit et push sur GitHub
4. Vérifier que la CI s'exécute et passe dans l'onglet GitHub Actions

## 📖 Instructions détaillées

Voir [docs/TP1-weather-api.md](docs/TP1-weather-api.md) pour :
- Instructions pas-à-pas
- Exemples de code
- Conseils et astuces
- Dépannage

## 🧪 Exécuter les tests

```bash
# Lancer tous les tests
uv run pytest -v

# Lancer un test spécifique
uv run pytest test_weather_api.py::test_get_weather_success -v

# Lancer avec couverture de code
uv run pytest --cov=app -v

# Afficher les print statements
uv run pytest -s
```

## 🏃 Lancer l'API

### Terminal 1 : Démarrer le serveur

```bash
uv run uvicorn app:app --reload
```

Vous devriez voir :
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Gardez ce terminal ouvert !** Le serveur se rechargera automatiquement quand vous modifiez le code.

---

### Ouvrir dans le navigateur

Ouvrez maintenant ces URLs :

- 🏠 **API principale** : http://localhost:8000/
- 📚 **Documentation interactive (Swagger UI)** : http://localhost:8000/docs
- 📖 **Documentation alternative (ReDoc)** : http://localhost:8000/redoc

**Le Swagger UI (`/docs`) est le meilleur moyen de tester votre API !**

---

### Terminal 2 : Tester avec curl (Optionnel)

Ouvrez un **second terminal** et testez :

```bash
# Lister les villes disponibles (fonctionne immédiatement)
curl http://localhost:8000/cities

# Tester l'endpoint météo (404 jusqu'à implémentation)
curl http://localhost:8000/weather/Brussels

# Tester la comparaison (404 jusqu'à implémentation)
curl "http://localhost:8000/weather/compare?city1=Brussels&city2=Paris"
```

---

### Utiliser Swagger UI (Recommandé !)

1. Aller sur http://localhost:8000/docs
2. Voir tous les endpoints listés
3. Cliquer sur `GET /cities` → "Try it out" → "Execute"
4. Voir la réponse avec les villes disponibles ✅
5. Essayer `GET /weather/{city}` (affichera 404 jusqu'à implémentation)
6. Au fur et à mesure que vous implémentez les endpoints, rafraîchissez et testez-les !

## 📝 Fichiers dans cette branche

- `app.py` - Votre application FastAPI (⚠️ incomplète - à implémenter)
- `test_weather_api.py` - Suite de tests (✅ complète - guide votre implémentation)
- `pyproject.toml` - Dépendances
- `GITHUB_ACTIONS_GUIDE.md` - Guide CI/CD pas-à-pas
- `.env.example` - Template variables d'environnement
- `README.md` - Ce fichier
- `docs/` - Guides et références détaillés

## 🎓 Objectifs pédagogiques

À la fin de ce workshop, vous saurez :
- ✅ Comprendre le cycle TDD (Rouge → Vert → Refactoriser)
- ✅ Écrire des tests unitaires avec pytest
- ✅ Mocker des dépendances externes
- ✅ Construire des API REST avec FastAPI
- ✅ Gérer les erreurs correctement
- ✅ Configurer la CI/CD avec GitHub Actions

## 💡 Conseils

- **Lisez les tests en premier** - Ils vous disent quoi construire
- **Faites passer un test à la fois** - N'essayez pas de tout faire d'un coup
- **Lancez les tests fréquemment** - Voyez votre progression
- **Demandez de l'aide** - Les instructeurs sont là pour vous guider
- **Référez-vous aux exemples** - `git checkout examples` pour voir du code fonctionnel

## 🆘 Besoin d'aide ?

- **Test qui échoue ?** Lancez avec `-vv` pour plus de détails : `uv run pytest -vv`
- **Erreur d'import ?** Assurez-vous d'avoir lancé `uv sync`
- **Mock qui ne fonctionne pas ?** Vérifiez que le chemin du patch correspond à votre import
- **Bloqué ?** Voir [docs/troubleshooting.md](docs/troubleshooting.md)

## 📚 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation pytest](https://docs.pytest.org/)
- [Guide unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [API Open-Meteo](https://open-meteo.com/)

---

**Prêt à commencer ?**

```bash
uv sync
uv run pytest -v
# Voir les tests qui échouent → c'est parti pour coder !
```

**Bonne chance ! 🚀**