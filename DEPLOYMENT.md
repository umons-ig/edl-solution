# 🚀 Guide de Déploiement TaskFlow sur Render

Ce guide explique comment déployer l'application TaskFlow (backend + frontend) sur Render.

## 📋 Prérequis

- Un compte GitHub avec le projet TaskFlow
- Un compte Render (gratuit) : https://render.com
- Les ateliers 1 et 2 terminés (tests + CI/CD fonctionnels)

## 🎯 Architecture de Déploiement

```
Frontend (Static Site)          Backend (Web Service)
taskflow-frontend.onrender.com ← → taskflow-backend.onrender.com
     │                                    │
     ├─ React + Vite build              ├─ FastAPI + UV
     ├─ Served via CDN                  ├─ Python 3.11
     └─ HTTPS automatique               └─ HTTPS automatique
```

## 🚀 Méthode 1 : Déploiement Automatique (Recommandé)

### Étape 1 : Préparer render.yaml

Le fichier `render.yaml` à la racine définit l'infrastructure complète.

```yaml
services:
  - type: web
    name: taskflow-backend
    ...
  - type: web
    name: taskflow-frontend
    ...
```

### Étape 2 : Déployer via Render Dashboard

1. Connectez-vous à [Render Dashboard](https://dashboard.render.com)
2. Cliquez sur **"New +" → "Blueprint"**
3. Connectez votre repository GitHub
4. Render détecte automatiquement `render.yaml`
5. Cliquez sur **"Apply"**

### Étape 3 : Configurer les Variables d'Environnement

Une fois les services créés :

**Backend :**
- `CORS_ORIGINS` = URL de votre frontend (ex: `https://taskflow-frontend-xxx.onrender.com`)

**Frontend :**
- `VITE_API_URL` = URL de votre backend (ex: `https://taskflow-backend-xxx.onrender.com`)

**Important :** Après avoir configuré les variables, redéployez les deux services.

## 🛠️ Méthode 2 : Déploiement Manuel

### Étape 1 : Déployer le Backend

1. **New + → Web Service**
2. Connectez votre repository GitHub
3. Configuration :
   - **Name** : `taskflow-backend`
   - **Region** : `Frankfurt` (ou plus proche de vous)
   - **Branch** : `main`
   - **Root Directory** : `backend`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install uv && uv sync`
   - **Start Command** : `uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables** :
   - `PYTHON_VERSION` = `3.11`
   - `CORS_ORIGINS` = (à configurer après frontend)
5. Cliquez sur **"Create Web Service"**

### Étape 2 : Déployer le Frontend

1. **New + → Static Site**
2. Connectez le même repository
3. Configuration :
   - **Name** : `taskflow-frontend`
   - **Region** : `Frankfurt`
   - **Branch** : `main`
   - **Root Directory** : `frontend`
   - **Build Command** : `npm ci && npm run build`
   - **Publish Directory** : `dist`
4. **Environment Variables** :
   - `VITE_API_URL` = URL du backend (ex: `https://taskflow-backend-xxx.onrender.com`)
5. Cliquez sur **"Create Static Site"**

### Étape 3 : Mettre à Jour les CORS

1. Allez dans **backend → Environment**
2. Ajoutez/modifiez :
   - `CORS_ORIGINS` = `https://taskflow-frontend-xxx.onrender.com`
3. Cliquez sur **"Save Changes"** → Le service redéploie automatiquement

## ✅ Vérification

### Backend

Visitez : `https://taskflow-backend-xxx.onrender.com/health`

Vous devriez voir :
```json
{
  "status": "healthy",
  "tasks_count": 0
}
```

### Frontend

Visitez : `https://taskflow-frontend-xxx.onrender.com`

L'interface devrait charger et pouvoir créer/lister des tâches.

### Logs

- **Backend** : Dashboard → taskflow-backend → Logs
- **Frontend** : Dashboard → taskflow-frontend → Logs

## 🐛 Troubleshooting

### Erreur : "CORS policy blocked"

**Cause** : Backend n'autorise pas l'origine du frontend

**Solution** :
1. Vérifiez `CORS_ORIGINS` dans backend
2. Format : `https://taskflow-frontend-xxx.onrender.com` (sans `/` à la fin)
3. Redéployez le backend

### Erreur : "Failed to fetch"

**Cause** : Frontend utilise la mauvaise URL backend

**Solution** :
1. Vérifiez `VITE_API_URL` dans frontend
2. Format : `https://taskflow-backend-xxx.onrender.com` (sans `/` à la fin)
3. Redéployez le frontend

### Backend timeout après 50 secondes

**Cause** : Plan gratuit de Render met les services en veille après inactivité

**Solution** :
- Première requête prend ~30-50 secondes (cold start)
- Ensuite rapide pendant 15 minutes d'activité
- Normal sur plan gratuit

## 🔄 Continuous Deployment

Avec `render.yaml` configuré :

1. **Push vers main** → Render redéploie automatiquement
2. **CI/CD GitHub Actions** → Tests passent → Merge → Deploy
3. **Zero downtime** : Render déploie la nouvelle version progressivement

## 📊 Monitoring

### Health Checks

Render vérifie automatiquement `/health` toutes les 30 secondes.

### Logs en Temps Réel

```bash
# Via Render Dashboard
Dashboard → Service → Logs → Auto-scroll
```

### Métriques

Dashboard → Service → Metrics :
- CPU usage
- Memory usage
- Request count
- Response time

## 💰 Coûts

**Plan Gratuit (Hobby) :**
- ✅ 750 heures/mois (services web)
- ✅ 100 GB bandwidth/mois (static sites)
- ✅ HTTPS automatique
- ✅ Domaines personnalisés
- ⚠️ Services se mettent en veille après 15 min d'inactivité
- ⚠️ Cold start ~30-50 secondes

Suffisant pour ce workshop et projets personnels !

## 🚀 Pour Aller Plus Loin

### Domaine Personnalisé

1. Dashboard → Service → Settings → Custom Domain
2. Ajoutez votre domaine (ex: `taskflow.example.com`)
3. Configurez les DNS selon instructions Render

### PostgreSQL Database

**Avec render.yaml, PostgreSQL est automatiquement créé ! 🎉**

Le fichier `render.yaml` inclut déjà la database :

```yaml
databases:
  - name: taskflow-db
    databaseName: taskflow
    region: frankfurt
    plan: free
    user: taskflow
```

**Configuration automatique :**
- ✅ Database créée automatiquement
- ✅ `DATABASE_URL` injectée dans le backend
- ✅ Connexion sécurisée automatique
- ✅ 256 MB RAM, 1 GB storage (plan gratuit)

**Migrer de In-Memory vers PostgreSQL :**

Le backend supporte les deux modes automatiquement :

```python
# backend/src/database.py détecte automatiquement DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")
```

- **Sans DATABASE_URL** : Utilise SQLite local (développement)
- **Avec DATABASE_URL** : Utilise PostgreSQL (production)

**Pour activer PostgreSQL :**

Le backend a déjà les fichiers nécessaires :
- `backend/src/database.py` - Configuration SQLAlchemy
- `backend/src/models.py` - Modèles ORM

Il suffit de déployer avec le `render.yaml` et PostgreSQL sera automatiquement utilisé !

### Monitoring Avancé

- Intégrez avec [Sentry](https://sentry.io) pour error tracking
- Utilisez [LogTail](https://logtail.com) pour logs centralisés

## 📚 Ressources

- [Render Docs](https://render.com/docs)
- [Blueprint Spec](https://render.com/docs/blueprint-spec)
- [Python on Render](https://render.com/docs/deploy-fastapi)
- [Static Sites on Render](https://render.com/docs/static-sites)

---

**Prêt pour la production !** 🚀
