# 🚀 Atelier 3 : Déploiement en Production

**Durée estimée :** 3 heures
**Prérequis :** Ateliers 1 & 2 terminés (application full-stack avec CI/CD)

## 🎯 Objectifs de l'Atelier

**Objectif principal :** Déployer votre application full-stack en production sur le cloud

À la fin de cet atelier, vous aurez **déployé** :

1. ✅ Un **backend FastAPI en production** sur Render
2. ✅ Un **frontend React en production** sur Render
3. ✅ Une **configuration CORS** pour connecter frontend et backend en production
4. ✅ Des **variables d'environnement** pour gérer les différents environnements
5. ✅ Un **monitoring actif** avec health checks

---

## 📦 Architecture Cible

**Avant (Local) :**

```text
Frontend (localhost:3000) → Vite Proxy → Backend (localhost:8000)
```

**Après (Production) :**

```text
Frontend (Render)                  Backend (Render)
taskflow-frontend-XXX.onrender.com → taskflow-backend-XXX.onrender.com
     HTTPS                              HTTPS + CORS
```

---

## 📋 Phase 1 : Préparation pour la Production (30 min)

### 1.1 - Créer un Compte Render

**🎯 EXERCICE : S'inscrire sur Render**

1. Allez sur <https://render.com>
2. Cliquez sur **"Get Started"**
3. Inscrivez-vous avec votre compte GitHub
4. Autorisez Render à accéder à vos repositories

**Niveau gratuit :** 750 heures/mois gratuites (suffisant pour ce workshop)

### 1.2 - Préparer le Backend pour la Production

**🎯 EXERCICE : Configurer CORS pour la production**

Ouvrez `backend/src/app.py` et vérifiez la configuration CORS :

```python
import os
from fastapi.middleware.cors import CORSMiddleware

# Configuration CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Pourquoi c'est important ?**

- En **développement** : CORS permet `localhost:3000`
- En **production** : CORS doit permettre votre URL Render frontend

**Variables d'environnement** :

- `CORS_ORIGINS` : Liste des origines autorisées (séparées par des virgules)

### 1.3 - Préparer le Frontend pour la Production

**🎯 EXERCICE : Configurer l'URL du backend**

Le frontend doit savoir où trouver le backend en production.

Ouvrez `frontend/src/api/api.ts` :

```typescript
const API_BASE = import.meta.env.VITE_API_URL || '/api';
```

**Comment ça marche ?**

- **Développement** : `VITE_API_URL` n'est pas défini → utilise `/api` (proxy Vite)
- **Production** : `VITE_API_URL` = URL du backend Render → appels directs

**Créez `frontend/.env.example` :**

```bash
# URL du backend en production
# Exemple : VITE_API_URL=https://taskflow-backend-XXXX.onrender.com
VITE_API_URL=
```

### 1.4 - Vérifier le Health Check

**🎯 EXERCICE : Tester le endpoint de santé**

Le backend doit avoir un endpoint `/health` pour le monitoring :

```python
@app.get("/health")
async def health_check():
    """Health check endpoint pour Render."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0"
    }
```

**Testez localement :**

```bash
cd backend
uv run uvicorn src.app:app --reload

# Dans un autre terminal
curl http://localhost:8000/health
```

**Réponse attendue :**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-21T10:00:00",
  "environment": "development",
  "version": "1.0.0"
}
```

### 1.5 - Configurer le Routing Client-Side

**🎯 EXERCICE : Créer le fichier de redirects**

React Router a besoin de ce fichier pour fonctionner correctement sur Render.

Créez `frontend/public/_redirects` :

```text
/*    /index.html   200
```

**Que fait ce fichier ?**

- Redirige toutes les routes vers `index.html`
- Permet au routing React de gérer les URLs (au lieu de Render)

---

## 📋 Phase 2 : Déployer le Backend (45 min)

### 2.1 - Créer le Service Backend sur Render

**🎯 EXERCICE : Configurer le backend**

1. Connectez-vous à <https://dashboard.render.com>
2. Cliquez sur **"New +"** → **"Web Service"**
3. Connectez votre repository GitHub

**Configuration :**

```yaml
Name: taskflow-backend
Branch: main
Region: Frankfurt (ou votre région préférée)
Root Directory: backend
Runtime: Python 3

Build Command: pip install uv && uv sync
Start Command: uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT

Instance Type: Free
```

**Important :**

- `$PORT` : Variable fournie par Render (ne pas changer)
- `--host 0.0.0.0` : Écoute sur toutes les interfaces (requis pour Render)

### 2.2 - Configurer les Variables d'Environnement

**🎯 EXERCICE : Ajouter les variables d'environnement**

Dans la page de configuration Render, section **"Environment"** :

```bash
ENVIRONMENT=production
CORS_ORIGINS=*
PYTHON_VERSION=3.11
```

**Explications :**

- `ENVIRONMENT=production` : Mode production
- `CORS_ORIGINS=*` : Permet toutes les origines (à restreindre en vrai production)
- `PYTHON_VERSION=3.11` : Version Python à utiliser

**Note :** En production réelle, remplacez `*` par l'URL exacte du frontend :

```bash
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com
```

### 2.3 - Configurer les Build Filters (Monorepo)

**🎯 EXERCICE : Optimiser les déploiements**

Pour éviter de rebuilder quand seul le frontend change :

**Included Paths :**

```text
backend/**
.github/workflows/**
```

**Ignored Paths :**

```text
frontend/**
docs/**
*.md
```

### 2.4 - Configurer le Health Check

**🎯 EXERCICE : Activer le monitoring**

Dans **"Settings"** → **"Health & Alerts"** :

```yaml
Health Check Path: /health
```

Render vérifiera automatiquement que votre backend répond.

### 2.5 - Déclencher le Premier Déploiement

**🎯 EXERCICE : Déployer le backend**

1. Cliquez sur **"Create Web Service"**
2. Render va :
   - Cloner votre repository
   - Installer les dépendances (`uv sync`)
   - Démarrer le serveur
   - Vérifier le health check

**Observez les logs en temps réel** dans la console Render.

**Temps de déploiement** : 2-5 minutes

### 2.6 - Vérifier le Déploiement

**🎯 EXERCICE : Tester le backend en production**

Une fois le déploiement terminé, vous aurez une URL :

```text
https://taskflow-backend-XXXX.onrender.com
```

**Testez dans votre terminal :**

```bash
# Health check
curl https://taskflow-backend-XXXX.onrender.com/health

# Liste des tâches (vide au début)
curl https://taskflow-backend-XXXX.onrender.com/tasks

# Documentation API
# Ouvrez dans le navigateur :
# https://taskflow-backend-XXXX.onrender.com/docs
```

**✅ Checkpoint :** Le backend doit répondre à tous ces endpoints.

---

## 📋 Phase 3 : Déployer le Frontend (45 min)

### 3.1 - Créer le Site Statique sur Render

**🎯 EXERCICE : Configurer le frontend**

1. Sur Render Dashboard, cliquez **"New +"** → **"Static Site"**
2. Sélectionnez le même repository GitHub

**Configuration :**

```yaml
Name: taskflow-frontend
Branch: main
Root Directory: frontend

Build Command: npm install && npm run build
Publish Directory: dist

Instance Type: Free
```

### 3.2 - Configurer les Variables d'Environnement

**🎯 EXERCICE : Pointer vers le backend**

Dans **"Environment Variables"** :

```bash
VITE_API_URL=https://taskflow-backend-XXXX.onrender.com
```

**⚠️ IMPORTANT :** Remplacez `XXXX` par l'ID de votre backend Render !

**Comment trouver l'URL du backend ?**

- Allez sur votre service backend Render
- Copiez l'URL en haut de la page

### 3.3 - Configurer les Build Filters

**🎯 EXERCICE : Optimiser les rebuilds**

**Included Paths :**

```text
frontend/**
.github/workflows/**
```

**Ignored Paths :**

```text
backend/**
docs/**
*.md
```

### 3.4 - Déclencher le Déploiement Frontend

**🎯 EXERCICE : Déployer le frontend**

1. Cliquez sur **"Create Static Site"**
2. Render va :
   - Installer les dépendances (`npm install`)
   - Builder le projet (`npm run build`)
   - Publier les fichiers statiques du dossier `dist/`

**Temps de déploiement** : 3-7 minutes

### 3.5 - Vérifier le Déploiement

**🎯 EXERCICE : Tester l'application complète**

Votre frontend sera disponible à :

```text
https://taskflow-frontend-XXXX.onrender.com
```

**Tests à faire :**

1. **Ouvrez l'URL dans votre navigateur**
2. **Ouvrez DevTools (F12)** → Onglet Network
3. **Créez une tâche** :
   - Cliquez sur "Nouvelle Tâche"
   - Remplissez le formulaire
   - Soumettez

**Dans Network tab :**

- Vous devez voir : `POST https://taskflow-backend-XXXX.onrender.com/tasks`
- Statut : `201 Created`

4. **Rafraîchissez la page** :
   - La tâche doit toujours être là
   - Requête : `GET https://taskflow-backend-XXXX.onrender.com/tasks`

**✅ Checkpoint :** Votre application full-stack fonctionne en production !

---

## 📋 Phase 4 : Configuration Avancée (30 min)

### 4.1 - Activer le Déploiement Automatique

**🎯 EXERCICE : Auto-deploy sur GitHub push**

Par défaut, Render redéploie automatiquement quand vous pushez sur `main`.

**Vérifiez dans Settings → Build & Deploy :**

```yaml
Auto-Deploy: Yes
```

**Test :**

1. Faites un petit changement (ex: titre de l'app)
2. Committez et pushez :

```bash
git add .
git commit -m "test: verify auto-deploy"
git push origin main
```

3. Observez dans Render Dashboard :
   - ✅ GitHub Actions exécute les tests
   - ✅ Render détecte le push
   - ✅ Nouveau déploiement automatique

### 4.2 - Configurer CORS Restreint (Production Réelle)

**🎯 EXERCICE : Sécuriser le backend**

Pour une vraie production, ne laissez pas `CORS_ORIGINS=*`.

**Dans Render Backend → Environment :**

```bash
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com
```

**Pour plusieurs domaines :**

```bash
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com,https://www.votredomaine.com
```

**Redéployez manuellement** : Cliquez sur "Manual Deploy" → "Deploy latest commit"

### 4.3 - Surveiller les Logs

**🎯 EXERCICE : Déboguer en production**

**Backend logs :**

1. Allez sur votre service backend
2. Cliquez sur l'onglet **"Logs"**
3. Vous verrez toutes les requêtes en temps réel

**Frontend logs :**

1. Les logs de build sont dans l'onglet "Logs"
2. Les erreurs runtime sont dans DevTools du navigateur (F12 → Console)

**Commandes utiles :**

```bash
# Voir les logs backend en live
# (dans le dashboard Render, onglet Logs)

# Chercher une erreur
# Utilisez Ctrl+F dans les logs
```

### 4.4 - Optimiser les Performances

**🎯 EXERCICE : Configuration production**

**Backend (`backend/src/app.py`) :**

```python
# En production, ajoutez :
import logging

logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG
)
```

**Frontend (déjà optimisé par Vite) :**

- Minification automatique
- Tree-shaking
- Code splitting
- Compression gzip

---

## 📋 Phase 5 : Test et Validation (30 min)

### 5.1 - Checklist de Déploiement

**🎯 EXERCICE : Vérifier que tout fonctionne**

**Backend :**

- [ ] URL accessible : `https://taskflow-backend-XXXX.onrender.com`
- [ ] Health check : `/health` retourne `{"status":"healthy"}`
- [ ] API Docs : `/docs` fonctionne
- [ ] Endpoints API : `/tasks` répond
- [ ] CORS configuré : Requêtes du frontend acceptées

**Frontend :**

- [ ] URL accessible : `https://taskflow-frontend-XXXX.onrender.com`
- [ ] Page se charge sans erreur
- [ ] Connexion au backend fonctionne
- [ ] Création de tâches fonctionne
- [ ] Suppression de tâches fonctionne
- [ ] Modification de tâches fonctionne

**CI/CD :**

- [ ] GitHub Actions passe tous les tests
- [ ] Auto-deploy activé
- [ ] Push sur main déclenche un redéploiement

### 5.2 - Tester les Scénarios Réels

**🎯 EXERCICE : Cas d'utilisation complets**

**Scénario 1 : Créer une tâche**

1. Ouvrez votre frontend en production
2. Créez une tâche "Déploiement réussi !"
3. Priorité : High
4. Vérifiez qu'elle apparaît dans la colonne "À Faire"

**Scénario 2 : Modifier une tâche**

1. Cliquez sur "✏️" pour éditer
2. Changez le statut en "En Cours"
3. Vérifiez qu'elle se déplace dans la bonne colonne

**Scénario 3 : Partager avec un collègue**

1. Copiez l'URL de votre frontend
2. Envoyez-la à un collègue
3. Il doit voir les mêmes tâches !

**Scénario 4 : Tester sur mobile**

1. Ouvrez l'URL sur votre téléphone
2. L'interface doit être responsive

### 5.3 - Déboguer les Problèmes Courants

#### ❌ "Connection Error" dans le frontend

**Cause :** `VITE_API_URL` mal configuré

**Solution :**

1. Vérifiez dans Render Frontend → Environment
2. La variable doit être : `VITE_API_URL=https://taskflow-backend-XXXX.onrender.com`
3. Redéployez

#### ❌ CORS Error

**Cause :** Backend ne permet pas l'origine du frontend

**Solution :**

```bash
# Dans Render Backend → Environment
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com
```

#### ❌ Backend "Service Unavailable"

**Cause :** Health check échoue

**Solution :**

1. Vérifiez les logs backend
2. Assurez-vous que `/health` répond
3. Vérifiez que le port est `$PORT` (fourni par Render)

#### ❌ Frontend montre du code au lieu de l'app

**Cause :** Publish Directory incorrect

**Solution :**

```yaml
Publish Directory: dist  # PAS frontend/dist !
```

---

## ✅ Checklist de Fin d'Atelier

**Services Déployés :**

- [ ] Backend en production et accessible
- [ ] Frontend en production et accessible
- [ ] Communication frontend ↔ backend fonctionne
- [ ] Health checks configurés

**Configuration :**

- [ ] Variables d'environnement configurées
- [ ] CORS correctement configuré
- [ ] Build filters optimisés (monorepo)
- [ ] Auto-deploy activé

**Tests :**

- [ ] Création de tâches fonctionne
- [ ] Modification de tâches fonctionne
- [ ] Suppression de tâches fonctionne
- [ ] Application accessible depuis n'importe où

**Documentation :**

- [ ] URLs notées quelque part :
  - Backend : `https://taskflow-backend-XXXX.onrender.com`
  - Frontend : `https://taskflow-frontend-XXXX.onrender.com`

---

## 🎯 Ce que Vous Avez Appris

Félicitations ! 🎉 Vous avez maintenant :

✅ **Déployé une application full-stack en production**
✅ **Configuré CORS pour la production**
✅ **Utilisé des variables d'environnement**
✅ **Mis en place un monitoring avec health checks**
✅ **Configuré un déploiement automatique (CI/CD complet)**

**Votre application est accessible partout dans le monde ! 🌍**

---

## 🚀 Pour Aller Plus Loin

**Améliorations possibles :**

1. **Base de données persistante PostgreSQL** ⭐ **DISPONIBLE MAINTENANT !**
   - 📚 **[Guide complet : Intégration PostgreSQL](workshop-3-database.md)**
   - Remplacer le stockage en mémoire par une vraie base de données
   - Déployer PostgreSQL sur Render
   - Utiliser SQLAlchemy ORM
   - **Durée** : 60-90 minutes
   - **Prérequis** : Avoir complété les phases 1-5 de cet atelier

2. **Domaine personnalisé**
   - Acheter un nom de domaine
   - Le connecter à Render

3. **Authentification**
   - Ajouter un login/signup
   - Protéger les routes

4. **Monitoring avancé**
   - Intégrer Sentry pour les erreurs
   - Ajouter des metrics avec Prometheus

5. **Tests E2E**
   - Playwright ou Cypress
   - Tests automatisés sur l'environnement de production

---

## 📚 Ressources

**Atelier 3 - Extensions :**

- **[Guide PostgreSQL Database](workshop-3-database.md)** - Intégration base de données (Partie 5)
- **[Migration Checklist](MIGRATION_CHECKLIST.md)** - Guide visuel de migration
- **[Backend README](../backend/README.md)** - Documentation technique complète

**Documentation Externe :**

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [Managing Environment Variables](https://render.com/docs/environment-variables)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) (pour la base de données)

---

## 📝 Notes Finales

**Limitations du plan gratuit Render :**

- Services s'endorment après 15 min d'inactivité
- Réveil = 30-60 secondes de latence
- Pour éviter ça : Plan payant ou service de "keep-alive"

**Coûts (si vous passez au payant) :**

- Starter plan : ~7$/mois par service
- Adapté pour petits projets personnels

**Alternatives à Render :**

- Vercel (frontend)
- Railway (full-stack)
- Fly.io (backend)
- Heroku (full-stack, plus cher)

---

**Version 1.0** - Atelier 3 : Déploiement en Production 🚀
