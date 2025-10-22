# TaskFlow : Ateliers de Gestion de Tâches

Série d'ateliers pratiques pour apprendre les méthodes CI/CD en construisant une application moderne de gestion de tâches.

## 🎯 Projet : TaskFlow
Une plateforme collaborative de gestion de tâches où vous construisez une application full-stack depuis zéro, en apprenant les pratiques de développement modernes à chaque étape.

**Résultat Final** : Un gestionnaire de tâches de type Kanban prêt pour la production, avec collaboration d'équipe et déploiement automatisé.

## 📚 Aperçu des Ateliers

### **Atelier 1 : Backend Python & Fondamentaux des Tests**
- **Focus** : TDD, FastAPI, pytest, gestion d'environnement UV
- **Domaine** : API de gestion de tâches (opérations CRUD)
- **Compétences** : APIs RESTful, tests automatisés, gestion d'erreurs
- **Livrable** : Service backend complet avec couverture de tests > 95%

### **Atelier 2 : Frontend TypeScript & Intégration**
- **Focus** : Développement React, tests inter-services, UI temps réel
- **Domaine** : Tableaux Kanban interactifs, visualisation des tâches
- **Compétences** : Tests de composants, intégration API, design responsive
- **Livrable** : Application full-stack avec frontend/backend synchronisés

### **Atelier 3 : Production & Déploiement Cloud + Base de Données**
- **Focus** : Déploiement cloud, automatisation CI/CD, intégration PostgreSQL
- **Domaine** : Configuration de production, gestion d'environnement, monitoring, persistance des données
- **Compétences** : Déploiement cloud, GitHub Actions, SQLAlchemy ORM, PostgreSQL
- **Livrable** : Application prête pour la production avec base de données PostgreSQL

## 🏗️ Architecture du Projet

```
taskflow/
├── backend/               # Service FastAPI Python
│   ├── src/              # Code de l'application
│   ├── tests/            # Tests backend
│   └── pyproject.toml    # Dépendances UV
├── frontend/             # Service React TypeScript
│   ├── src/              # Code des composants
│   ├── tests/            # Tests frontend
│   └── package.json      # Dépendances Node
├── docs/                 # Documentation des ateliers
├── .github/workflows/    # Pipelines CI/CD
└── README.md            # Ce fichier
```

## 🚀 Parcours d'Apprentissage

### **Cycle Red-Green-Refactor**
1. **Écrire des tests qui échouent (Red)** → Définir le comportement attendu
2. **Implémenter le code minimal (Green)** → Faire passer les tests
3. **Refactoriser et optimiser** → Améliorer la qualité du code
4. **Commit et CI/CD** → Automatiser les tests et le déploiement

### **Stack Technique**
- **Backend** : FastAPI + Python 3.11+ + Gestionnaire de paquets UV
- **Frontend** : React 18 + TypeScript + Tailwind CSS
- **Tests** : pytest + Jest + React Testing Library
- **Base de Données** : PostgreSQL (production) + SQLite (développement)
- **ORM** : SQLAlchemy 2.0
- **CI/CD** : GitHub Actions avec pipelines multi-services
- **Déploiement** : Render (Cloud Platform)

## 📋 Prérequis

- **Python 3.11+** et gestionnaire de paquets **uv**
- **Node.js 18+** et **npm** ou **yarn**
- **Git** et **compte GitHub**
- **Éditeur de code** (VS Code recommandé)
- Connaissances de base en Python et JavaScript

## 🎯 Objectifs des Ateliers

### **Objectifs Atelier 1**
- ✅ Configurer l'environnement UV et la structure du projet
- ✅ Implémenter l'API RESTful pour la gestion des tâches
- ✅ Écrire des tests unitaires complets avec mocking
- ✅ Configurer les tests automatisés avec GitHub Actions
- ✅ Pratiquer la méthodologie TDD et la gestion d'erreurs

### **Objectifs Atelier 2**
- ✅ Construire un frontend React/TypeScript responsive
- ✅ Implémenter une interface Kanban avec drag-and-drop
- ✅ Écrire des tests d'intégration entre services
- ✅ Ajouter des fonctionnalités de synchronisation temps réel
- ✅ Déployer l'application multi-services

### **Objectifs Atelier 3**
- ✅ Intégrer PostgreSQL avec SQLAlchemy ORM
- ✅ Configurer les pipelines CI/CD de production avec GitHub Actions
- ✅ Configurer les variables d'environnement et paramètres de production
- ✅ Ajouter des health checks et du monitoring
- ✅ Déployer sur la plateforme cloud Render avec base de données

## 🌐 Application Déployée

### **URLs de Production**
- **Backend API** : https://taskflow-backend-0dax.onrender.com
- **Frontend** : https://taskflow-frontend-[votre-id].onrender.com
- **Documentation API** : https://taskflow-backend-0dax.onrender.com/docs
- **Health Check** : https://taskflow-backend-0dax.onrender.com/health

### **Pipeline CI/CD**
- Tests automatiques sur chaque push
- Déploiement automatique sur la branche `main`
- Couverture de tests : 96%+
- GitHub Actions : [Voir les workflows](https://github.com/umons-ig/edl-tp-1/actions)

## 📖 Documentation des Ateliers

Instructions détaillées pour chaque atelier :

- **[Atelier 1 : Backend & Tests](docs/workshop-1-backend.md)** - Fondamentaux FastAPI
- **[Atelier 2 : Frontend & Intégration](docs/workshop-2-frontend.md)** - Développement React
- **[Atelier 3 : Production & DevOps](docs/workshop-3-production.md)** - CI/CD Avancé
- **[Atelier 3 (Partie 5) : Intégration PostgreSQL](docs/workshop-3-database.md)** - Base de Données 🆕

## 🛠️ Démarrage Rapide

### **Installation**
```bash
# Cloner le dépôt
git clone https://github.com/umons-ig/edl-tp-1.git
cd edl-tp-1
```

### **Configuration Backend**
```bash
cd backend
uv sync                                      # Installer les dépendances
uv run uvicorn src.app:app --reload        # Démarrer le serveur
uv run pytest                               # Lancer les tests
```

### **Configuration Frontend**
```bash
cd frontend
npm install                                 # Installer les dépendances
npm run dev                                # Démarrer le serveur dev
npm test                                   # Lancer les tests
```

## 🤝 Approche d'Apprentissage

Chaque atelier suit un format de **découverte guidée** :
- **Code de départ** avec des lacunes et TODOs intentionnels
- Approche **test-driven development**
- **Divulgation progressive** - apprendre un concept à la fois
- **Exercices pratiques** avec feedback immédiat
- **Défis réels** et cas limites

## 📊 Critères d'Évaluation

### **Excellence Technique**
- Le code suit les meilleures pratiques modernes
- Couverture de tests complète maintenue
- Gestion appropriée des erreurs et validation
- Structure de code propre et lisible

### **Implémentation CI/CD**
- Tests automatisés à chaque commit
- Vérifications cohérentes de la qualité du code
- Déploiements automatisés réussis
- Gestion appropriée des environnements

### **Résolution de Problèmes**
- Utilisation efficace des ressources disponibles
- Solutions créatives aux exigences
- Techniques de débogage appropriées
- Collaboration et communication

## 🏆 Livrables Finaux

À la fin de l'Atelier 3, vous aurez construit :

✅ **Application fonctionnelle de gestion de tâches**
✅ **Base de données PostgreSQL en production**
✅ **Pipelines CI/CD automatisés**
✅ **Capacités de déploiement en production**
✅ **Suite de tests complète (70%+ couverture)**
✅ **Architecture full-stack moderne**
✅ **Déploiement cloud fonctionnel**

## 📚 Ressources Supplémentaires

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation React](https://react.dev/)
- [Documentation pytest](https://docs.pytest.org/)
- [Guide GitHub Actions](https://docs.github.com/en/actions)
- [Gestionnaire de Paquets UV](https://docs.astral.sh/uv/)
- [Documentation Render](https://render.com/docs)

## 🤝 Contribution

Vous avez trouvé un problème ou avez une suggestion d'amélioration ? N'hésitez pas à ouvrir une issue ou soumettre une pull request.

## 📄 Licence

Matériel pédagogique pour ateliers - voir la documentation de chaque atelier pour les détails de licence.

---

**Prêt à commencer ?** Rendez-vous sur [Atelier 1 : Fondamentaux Backend](docs/workshop-1-backend.md) pour débuter votre parcours !

🚀 **Version 2.2.0** - Atelier 3 Complété avec PostgreSQL & Déploiement Cloud
