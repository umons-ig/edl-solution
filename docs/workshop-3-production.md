# Atelier 3 : Déploiement en Production & CI/CD Cloud

**Durée** : 3 heures
**Branche** : Basé sur la complétion des ateliers 1 & 2
**Niveau** : Intermédiaire à Avancé
**Prérequis** : Ateliers 1 & 2 (application full-stack) complétés

## 🎯 Objectifs

À la fin de cet atelier, vous serez capable de :

- Configurer une application avec **stockage en mémoire simplifié** pour la production
- Mettre en place des **pipelines CI/CD de production** avec GitHub Actions
- **Déployer en production** sur la plateforme cloud Render
- Configurer des **paramètres basés sur l'environnement** pour dev/staging/prod
- Implémenter des patterns de **health checks et monitoring**
- Comprendre la **gestion des secrets** et les bonnes pratiques de production
- Gérer la **configuration CORS** pour les déploiements cloud

## 📋 Prérequis

### Ateliers Précédents Complétés

- ✅ Atelier 1 : API Backend avec FastAPI et tests complets
- ✅ Atelier 2 : Application Frontend React avec intégration API
- ✅ Dépôt GitHub avec workflows CI/CD existants
- ✅ Application full-stack fonctionnelle localement

### Exigences Supplémentaires

- ✅ **Compte GitHub** avec accès au dépôt
- ✅ **Compte Render** (niveau gratuit avec 750 heures)
- ✅ Compréhension des variables d'environnement et gestion des secrets

## 🚀 Démarrage

### Évolution de l'Atelier

Cet atelier s'appuie sur les fondations des Ateliers 1 & 2 :

**Atelier 1** : Backend FastAPI + Stockage en mémoire
↓
**Atelier 2** : Frontend React + Intégration complète
↓
**Atelier 3** : Déploiement Cloud + Production Ready

### Architecture Actuelle vs Cible

**Après Atelier 2 (Local)** :

- React App (localhost:5173)
- FastAPI Backend (localhost:8000)
- Stockage en mémoire

**Après Atelier 3 (Production)** :

- React App (Déployé sur Render)
- FastAPI Backend (Déployé sur Render)
- Stockage en mémoire (simplifié pour l'atelier)
- GitHub Actions (Pipeline CI/CD)
- Configuration CORS multi-origines
- Health checks et monitoring

## 📚 Structure de l'Atelier

### Partie 1 : Configuration pour la Production (45 min)

#### 1.1 Variables d'Environnement Frontend

**Objectif** : Permettre au frontend de se connecter au backend en production

Créer `frontend/src/env.d.ts` :

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

Mettre à jour `frontend/src/api/api.ts` :

```typescript
// API Base URL - utilise variable d'environnement en production
const API_BASE = import.meta.env.VITE_API_URL || '/api';
```

Créer `frontend/.env.example` :

```bash
# Backend API URL (pour le déploiement en production)
# En développement, l'app utilise le proxy Vite vers localhost:8000
# En production (Render), définir ceci vers votre URL backend
VITE_API_URL=https://taskflow-backend-XXXX.onrender.com
```

#### 1.2 Configuration CORS Backend

**Objectif** : Permettre au frontend déployé d'accéder au backend

Dans `backend/src/app.py`, la configuration CORS permet toutes les origines pour simplifier l'atelier :

```python
# Configuration CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 1.3 Health Check et Monitoring

Vérifier le endpoint `/health` :

```python
@app.get("/health")
async def health_check():
    """Health check endpoint pour le monitoring."""
    environment = os.getenv("ENVIRONMENT", "development")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": environment,
        "version": "2.1.0",
        "storage": "in-memory"
    }
```

#### 1.4 Configuration Client-Side Routing

Créer `frontend/public/_redirects` :

```
/* /index.html 200
```

Ce fichier permet à Render de gérer correctement le routing côté client React.

### Partie 2 : Déploiement sur Render (60 min)

#### 2.1 Créer le Service Backend

1. Aller sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquer **"New +" → "Web Service"**
3. Connecter votre dépôt GitHub : `umons-ig/edl-tp-1`

**Configuration Backend** :

```yaml
Name: taskflow-backend
Branch: main
Region: Frankfurt (EU Central)
Root Directory: backend
Build Command: pip install uv && uv sync
Start Command: uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

**Variables d'Environnement** :

```bash
ENVIRONMENT=production
CORS_ORIGINS=*
PYTHON_VERSION=3.11.9
```

**Build Filters** (Important pour monorepo) :

- **Included Paths** : `backend/**`, `.github/workflows/**`
- **Ignored Paths** : `frontend/**`, `docs/**`, `*.md`

**Health Check** :

- Health Check Path : `/health`

#### 2.2 Créer le Site Statique Frontend

1. Cliquer **"New +" → "Static Site"**
2. Connecter le même dépôt GitHub

**Configuration Frontend** :

```yaml
Name: taskflow-frontend
Branch: main
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

**Variables d'Environnement** :

```bash
VITE_API_URL=https://taskflow-backend-XXXX.onrender.com
```

(Remplacer `XXXX` par votre ID de service backend)

**Build Filters** :

- **Included Paths** : `frontend/**`, `.github/workflows/**`
- **Ignored Paths** : `backend/**`, `docs/**`, `*.md`

#### 2.3 Vérifier les Déploiements

**Backend** :

```bash
curl https://taskflow-backend-XXXX.onrender.com/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "timestamp": "2025-10-11T21:22:54.902Z",
  "environment": "production",
  "version": "2.1.0",
  "storage": "in-memory"
}
```

**Frontend** :

Ouvrir `https://taskflow-frontend-XXXX.onrender.com` dans le navigateur.

### Partie 3 : CI/CD avec GitHub Actions (45 min)

#### 3.1 Workflow GitHub Actions Existant

Le fichier `.github/workflows/ci.yml` est déjà configuré avec :

```yaml
name: TaskFlow CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    # Tests backend avec pytest et couverture

  test-frontend:
    # Tests frontend avec vitest et couverture

  integration-check:
    # Tests d'intégration basiques

  deploy:
    # Déploiement vers Render (optionnel)
```

#### 3.2 Auto-Deploy Render (Recommandé)

**Option 1 : Auto-Deploy Natif Render** (Plus Simple) ✅

Render détecte automatiquement les pushs vers GitHub et redéploie :

1. Dans les paramètres du service Render → **"Build & Deploy"**
2. Vérifier que **"Auto-Deploy"** est sur **"Yes"**
3. Les build filters garantissent que seuls les changements pertinents déclenchent un rebuild

**Avantages** :

- Configuration zéro
- Fonctionne immédiatement
- Logs de déploiement dans le dashboard Render

**Option 2 : Deploy Hooks via GitHub Actions** (Avancé)

Pour un contrôle plus fin, ajouter des deploy hooks :

1. **Obtenir les Deploy Hooks de Render** :
   - Service backend → Settings → Deploy Hook → Copier l'URL
   - Site frontend → Settings → Deploy Hook → Copier l'URL

2. **Ajouter comme Secrets GitHub** :
   - Dépôt GitHub → Settings → Secrets → Actions
   - `RENDER_DEPLOY_HOOK_URL` (backend)

3. **Le workflow déclenchera automatiquement le déploiement**

#### 3.3 Tester le Pipeline CI/CD

Faire un petit changement et pusher :

```bash
# Exemple : changer le message de bienvenue
# Dans backend/src/app.py

git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

**Vérifier** :

1. **GitHub Actions** : [github.com/umons-ig/edl-tp-1/actions](https://github.com/umons-ig/edl-tp-1/actions)
   - ✅ Tests backend passent
   - ✅ Tests frontend passent
   - ✅ Tests d'intégration passent

2. **Render Dashboard** :
   - 📦 Nouveau déploiement en cours
   - 🚀 Déployé avec succès
   - ✅ Health check OK

### Partie 4 : Bonnes Pratiques de Production (30 min)

#### 4.1 Gestion des Secrets

**❌ Ne JAMAIS committer** :

```bash
.env
.env.local
.env.production
credentials.json
secrets/
```

**✅ Utiliser** :

- Variables d'environnement Render
- GitHub Secrets pour les workflows
- Fichiers `.env.example` pour la documentation

#### 4.2 Monitoring et Health Checks

**Health Check Configuration** :

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "2.1.0",
        "storage": "in-memory"
    }
```

**Render Health Check** :

- Intervalle : 30 secondes
- Path : `/health`
- Timeout : 10 secondes

#### 4.3 Gestion des Erreurs en Production

**Logging** :

```python
import logging

logger = logging.getLogger("taskflow")
logger.setLevel(logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG)

# Dans les endpoints
logger.info(f"Creating task: {task_data.title}")
logger.error(f"Failed to process request: {error}")
```

**Error Handling** :

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

#### 4.4 Optimisations de Performance

**Backend** :

```python
# CORS - en production, spécifier les origines exactes
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com,https://www.votredomaine.com

# Désactiver le mode debug
DEBUG=false
```

**Frontend** :

```bash
# Build de production optimisé
npm run build

# Variables d'environnement de production
VITE_API_URL=https://taskflow-backend-XXXX.onrender.com
```

## 🎯 Livrables de l'Atelier

À la fin de cet atelier, vous devez avoir :

### ✅ Services Déployés

- [ ] Backend API déployé sur Render
- [ ] Frontend déployé sur Render
- [ ] URLs publiques fonctionnelles
- [ ] Health checks configurés

### ✅ CI/CD Fonctionnel

- [ ] GitHub Actions exécute les tests à chaque push
- [ ] Auto-deploy configuré sur la branche main
- [ ] Build filters configurés pour le monorepo
- [ ] Tous les tests passent (96%+ couverture)

### ✅ Configuration de Production

- [ ] Variables d'environnement configurées
- [ ] CORS correctement configuré
- [ ] Secrets managés de manière sécurisée
- [ ] Logs et monitoring en place

### ✅ Documentation

- [ ] README mis à jour avec URLs de production
- [ ] Instructions de déploiement documentées
- [ ] Variables d'environnement documentées (.env.example)

## 📊 URLs de l'Application

Après déploiement, votre application sera accessible à :

**Backend** :

- API : `https://taskflow-backend-XXXX.onrender.com`
- Docs : `https://taskflow-backend-XXXX.onrender.com/docs`
- Health : `https://taskflow-backend-XXXX.onrender.com/health`

**Frontend** :

- Application : `https://taskflow-frontend-XXXX.onrender.com`

**GitHub** :

- Actions : `https://github.com/umons-ig/edl-tp-1/actions`
- Repository : `https://github.com/umons-ig/edl-tp-1`

## 🐛 Dépannage Courant

### Problème : "Connection Error" dans le frontend

**Cause** : Configuration CORS incorrecte

**Solution** :

```bash
# Dans Render backend → Environment
CORS_ORIGINS=*

# Ou spécifique :
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com
```

### Problème : Frontend ne se déploie pas

**Cause** : Mauvais Publish Directory

**Solution** :

```yaml
Root Directory: frontend
Publish Directory: dist  # PAS frontend/dist
```

### Problème : Tests échouent dans GitHub Actions

**Cause** : Tests non mis à jour après changements

**Solution** :

```bash
# Lancer les tests localement
cd backend
uv run pytest

# Mettre à jour les tests si nécessaire
# Commit et push
```

### Problème : Render "Build failed"

**Cause** : Commandes de build incorrectes

**Solution** :

```yaml
# Backend
Build Command: pip install uv && uv sync
Start Command: uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT

# Frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

## 📚 Ressources Supplémentaires

### Documentation

- [Documentation Render](https://render.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

### Tutoriels

- [Deploying FastAPI to Render](https://render.com/docs/deploy-fastapi)
- [React Static Site on Render](https://render.com/docs/deploy-create-react-app)
- [Managing Environment Variables](https://render.com/docs/environment-variables)

## 🏆 Félicitations !

Vous avez terminé l'Atelier 3 ! Votre application TaskFlow est maintenant :

✅ Déployée en production sur le cloud
✅ Testée automatiquement à chaque changement
✅ Déployée automatiquement via CI/CD
✅ Configurée avec des bonnes pratiques de production
✅ Accessible publiquement via HTTPS

**Prochaines Étapes** :

- Ajouter une base de données persistante (PostgreSQL/MongoDB)
- Implémenter l'authentification utilisateur
- Ajouter des tests end-to-end (Playwright/Cypress)
- Configurer un nom de domaine personnalisé
- Mettre en place du monitoring avancé (Sentry, DataDog)

---

**Version 2.1.0** - Atelier 3 Complété avec Succès ! 🎉
