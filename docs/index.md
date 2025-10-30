# 🎓 EDL - Ateliers de Développement Logiciel

Bienvenue dans les ateliers pratiques d'**Évolution et Déploiement Logiciel** de l'UMONS!

## 🎯 Objectifs du Cours

Ces ateliers vous apprendront les **pratiques professionnelles** du développement logiciel moderne :

- ✅ **Tests automatisés** (unitaires, intégration, E2E)
- ✅ **CI/CD** (Intégration et Déploiement Continus)
- ✅ **GitHub Actions** (workflows automatisés)
- ✅ **Déploiement en production** (avec bases de données réelles)
- ✅ **Bonnes pratiques** (TDD, protection de branche, code review)

---

## 📚 Les 3 Ateliers

### [Atelier 1 : Tests Unitaires Backend & Frontend](ATELIER-1.md)

**Durée :** 4-5 heures
**Objectif :** Maîtriser les tests unitaires avec pytest (Python) et Vitest (TypeScript)

**Ce que vous allez apprendre :**

- 🐍 Tests backend avec **pytest** et **FastAPI**
- ⚛️ Tests frontend avec **Vitest** et **React**
- 🎭 **Mocking** : simuler des API, des bases de données
- ☕ **Bonus Java** : Tests avec JUnit 4

**Technologies :**
`Python` · `TypeScript` · `pytest` · `Vitest` · `FastAPI` · `React` · `JUnit`

---

### [Atelier 2 : CI/CD avec GitHub Actions](ATELIER-2.md)

**Durée :** 4-5 heures
**Objectif :** Automatiser les tests et le déploiement avec GitHub Actions

**Ce que vous allez apprendre :**

- 🔄 **Workflows GitHub Actions** (backend, frontend, full-stack)
- 🚀 **CI Pipeline** : Tests automatiques à chaque commit
- 🔒 **Protection de branche** : Bloquer les merges si tests échouent
- ⚡ **Optimisation** : Cache, jobs parallèles, tests rapides/lents
- 🎯 **Reusable Workflows** : Orchestrer plusieurs workflows

**Technologies :**
`GitHub Actions` · `YAML` · `CI/CD` · `Workflows`

---

### [Atelier 3 : Déploiement en Production](ATELIER-3.md)

**Durée :** 3-4 heures
**Objectif :** Déployer l'application sur Render avec PostgreSQL

**Ce que vous allez apprendre :**

- 🐘 **PostgreSQL** : Migrer de la mémoire à une vraie base de données
- 🚀 **Render** : Déployer backend + frontend + base de données
- 🔐 **Variables d'environnement** et secrets
- 📊 **Monitoring** : Logs, métriques, santé de l'application
- ♻️ **CD** : Déploiement automatique après chaque merge

**Technologies :**
`PostgreSQL` · `Render` · `Environment Variables` · `CD`

---

## 🚀 Commencer

### Prérequis

- ✅ Git installé
- ✅ Python 3.11+ ou UV
- ✅ Node.js 18+
- ✅ Compte GitHub
- ✅ (Optionnel) Java 17+ pour les exercices bonus

### Installation

1. **Forker le repository** : [github.com/umons-ig/edl-starter](https://github.com/umons-ig/edl-starter)

2. **Cloner votre fork** :
   ```bash
   git clone https://github.com/VOTRE_NOM/edl-starter
   cd edl-starter
   ```

3. **Suivre l'Atelier 1** pour installer les dépendances

---

## 📖 Navigation

Utilisez le menu de gauche pour naviguer entre les différents ateliers.

Chaque atelier est **indépendant** mais suit une progression logique :

```
Atelier 1 (Tests) → Atelier 2 (CI/CD) → Atelier 3 (Déploiement)
```

---

## 🛠️ Stack Technique

**Backend :**
- FastAPI (Python)
- pytest pour les tests
- UV pour la gestion des dépendances
- PostgreSQL en production

**Frontend :**
- React + TypeScript
- Vite pour le build
- Vitest pour les tests
- TailwindCSS pour le style

**DevOps :**
- GitHub Actions pour CI/CD
- Render pour le déploiement
- MkDocs pour la documentation

---

## 💡 Conseils

!!! tip "Organisation"
    - Prévoyez 12-15 heures au total pour les 3 ateliers
    - Faites des pauses régulières
    - N'hésitez pas à demander de l'aide

!!! warning "Attention"
    - Lisez **toutes** les instructions avant de commencer
    - Testez localement avant de pousser sur GitHub
    - Ne commitez jamais de secrets (API keys, mots de passe)

!!! success "Objectif"
    À la fin de ces ateliers, vous saurez :

    - Écrire des tests automatisés professionnels
    - Configurer un pipeline CI/CD complet
    - Déployer une application full-stack en production

---

## 📞 Support

- **Documentation GitHub Actions** : [docs.github.com/actions](https://docs.github.com/en/actions)
- **Documentation Render** : [render.com/docs](https://render.com/docs)
- **Issues GitHub** : Pour signaler des bugs dans les exercices

---

**Prêt à commencer ?** 👉 [Atelier 1 : Tests Unitaires](ATELIER-1.md)
