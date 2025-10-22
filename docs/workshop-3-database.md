# Atelier 3 - Partie 5 : Intégration de Base de Données PostgreSQL

**Durée** : 60-90 minutes
**Prérequis** : Atelier 3 (Parties 1-4) complété
**Niveau** : Intermédiaire

⚠️ **IMPORTANT** : Cette partie est **optionnelle** et s'ajoute après l'Atelier 3. Les Ateliers 1 et 2 utilisent le stockage en mémoire. Vous allez maintenant migrer vers une vraie base de données !

## 📚 Documents Disponibles

Ce guide est le **document principal** pour l'intégration de la base de données. Deux ressources sont disponibles :

1. **[workshop-3-database.md](workshop-3-database.md)** (ce document) - **Tutorial complet** avec explications détaillées
2. **[MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md)** - **Checklist visuelle rapide** pour référence

💡 **Astuce** : Lisez d'abord ce document en entier, puis utilisez la checklist pendant l'implémentation.

## 🎯 Objectifs

À la fin de cette section, vous serez capable de :

- Comprendre pourquoi utiliser une base de données persistante vs stockage en mémoire
- Configurer **PostgreSQL avec Render** pour la production
- Implémenter **SQLAlchemy ORM** pour l'accès aux données
- Migrer du stockage en mémoire vers une base de données relationnelle
- Adapter les tests pour fonctionner avec la base de données
- Déployer l'application avec PostgreSQL en production

## 📋 Pourquoi PostgreSQL ?

### Limitations du Stockage en Mémoire

L'implémentation actuelle utilise une simple liste Python :

```python
tasks_storage: List[Task] = []
```

**Problèmes** :
- ❌ Les données sont perdues à chaque redémarrage du serveur
- ❌ Ne supporte pas le scaling horizontal (plusieurs instances)
- ❌ Pas de requêtes complexes ni de relations
- ❌ Pas de transactions ni d'intégrité des données

### Avantages de PostgreSQL

- ✅ **Persistance** : Les données survivent aux redémarrages
- ✅ **Scalabilité** : Supporte plusieurs instances de l'application
- ✅ **ACID** : Transactions atomiques, cohérence des données
- ✅ **Requêtes complexes** : Filtrage, jointures, agrégations
- ✅ **Intégrité** : Contraintes, clés étrangères, validations
- ✅ **Standard industriel** : Utilisé en production partout

## ⚙️ Vue d'Ensemble de la Migration

Cette partie va transformer votre application pour utiliser PostgreSQL au lieu du stockage en mémoire.

### Ce que vous allez faire

**Étape 1** : Ajouter les dépendances PostgreSQL
**Étape 2** : Créer les nouveaux fichiers (database.py, models.py)
**Étape 3** : Modifier app.py pour utiliser la base de données
**Étape 4** : Adapter les tests
**Étape 5** : Déployer sur Render avec PostgreSQL

**Temps estimé** : 60-90 minutes

## 🏗️ Architecture de la Solution

### Fichiers à CRÉER (nouveaux)

```text
backend/
├── src/
│   ├── database.py         # ✨ NOUVEAU - Configuration SQLAlchemy
│   ├── models.py           # ✨ NOUVEAU - Modèles ORM
│   └── db_init.py          # ✨ NOUVEAU - Scripts d'initialisation
├── .env.example            # ✨ NOUVEAU - Template variables d'environnement
└── .gitignore              # ✨ NOUVEAU - Fichiers à ignorer
```

### Fichiers à MODIFIER (existants)

```text
backend/
├── src/
│   └── app.py              # 🔧 MODIFIER - Remplacer tasks_storage par DB
├── tests/
│   └── conftest.py         # 🔧 MODIFIER - Ajouter fixtures de test DB
└── pyproject.toml          # 🔧 MODIFIER - Ajouter SQLAlchemy, psycopg2
```

### Stack Technique

- **SQLAlchemy 2.0** : ORM Python moderne
- **psycopg2** : Driver PostgreSQL pour Python
- **PostgreSQL 15** : Base de données relationnelle
- **Render Postgres** : Service managé cloud

## 📝 Étape 0 : Point de Départ

Avant de commencer, assurez-vous que :

- ✅ Vous avez complété les Ateliers 1, 2 et 3 (parties 1-4)
- ✅ Votre application utilise actuellement `tasks_storage: List[Task] = []`
- ✅ Tous vos tests passent
- ✅ Votre application est déployée sur Render

**Si vous n'avez pas fait les ateliers précédents**, cette partie ne fonctionnera pas seule !

### 📋 Aide-Mémoire Rapide

Si vous voulez une **checklist visuelle** de ce qu'il faut supprimer/garder/modifier, consultez:

👉 **[MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md)** - Vue d'ensemble avec diagrammes

Ce guide ci-dessous vous montre **tous les détails** étape par étape. La checklist est un résumé visuel pour vous aider à vous repérer.

## 📚 Partie 1 : Comprendre les Fichiers Ajoutés

### 1.1 Configuration de la Base de Données (`database.py`)

Ce module gère la connexion à la base de données :

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Créer une factory de sessions
SessionLocal = sessionmaker(bind=engine)

# Base pour les modèles ORM
Base = declarative_base()
```

**Points clés** :
- `DATABASE_URL` : Render fournit automatiquement cette variable
- `engine` : Gère le pool de connexions
- `SessionLocal` : Crée des sessions pour les transactions
- `Base` : Classe parente pour tous les modèles

### 1.2 Modèles de Données (`models.py`)

Définit le schéma de la base de données :

```python
from sqlalchemy import Column, String, DateTime, Enum
from .database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    status = Column(Enum(TaskStatus))
    priority = Column(Enum(TaskPriority))
    assignee = Column(String(100))
    due_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
```

**Points clés** :
- `__tablename__` : Nom de la table SQL
- `Column` : Définit les colonnes avec types et contraintes
- `server_default` : Valeur par défaut gérée par la DB
- `onupdate` : Mise à jour automatique du timestamp

### 1.3 Dependency Injection

FastAPI utilise `Depends()` pour injecter la session DB :

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db

@app.get("/tasks")
async def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return tasks
```

**Avantages** :

- Session créée automatiquement pour chaque requête
- Fermée automatiquement après la requête
- Facile à mocker pour les tests

## 🔨 Partie 2 : Implémentation Étape par Étape

**🎯 Objectif** : Migrer du stockage en mémoire vers PostgreSQL en modifiant votre code existant.

### Étape 2.1 : Ajouter les Dépendances

**Fichier à modifier** : `backend/pyproject.toml`

Trouvez la section `dependencies` et ajoutez SQLAlchemy et psycopg2 :

```toml
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "httpx>=0.25.2",
    "sqlalchemy>=2.0.23",      # ✨ AJOUTER CETTE LIGNE
    "psycopg2-binary>=2.9.9",  # ✨ AJOUTER CETTE LIGNE
]
```

**Installer les dépendances** :

```bash
cd backend
uv sync
```

**Ajuster la couverture de tests** (optionnel) :

Dans `pyproject.toml`, trouvez `--cov-fail-under=90` et changez-le à `70` (car on ajoute de nouveaux fichiers) :

```toml
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=70",  # 🔧 MODIFIER de 90 à 70
]
```

### Étape 2.2 : Créer le Module de Configuration Database

**Fichier à créer** : `backend/src/database.py`

Créez ce nouveau fichier avec le contenu suivant :

```python
"""
Database configuration and session management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator
import logging

logger = logging.getLogger("taskflow")

# Database URL - Render provides DATABASE_URL automatically
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./taskflow.db"  # Local SQLite fallback
)

# Fix for Render's postgres:// URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

logger.info(f"Connecting to database: {DATABASE_URL.split('@')[0]}...")

# Create engine
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency function to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize the database by creating all tables."""
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")


def drop_db() -> None:
    """Drop all database tables. WARNING: This will delete all data!"""
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("All tables dropped!")
```

### Étape 2.3 : Créer les Modèles ORM

**Fichier à créer** : `backend/src/models.py`

```python
"""
Database models for TaskFlow application.
"""

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from .database import Base
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskModel(Base):
    """SQLAlchemy model for tasks table."""
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(
        SQLEnum(TaskStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskStatus.TODO.value
    )
    priority = Column(
        SQLEnum(TaskPriority, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskPriority.MEDIUM.value
    )
    assignee = Column(String(100), nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
```

### Étape 2.4 : Modifier app.py pour Utiliser la Base de Données

**Fichier à modifier** : `backend/src/app.py`

**Changement 1** : Modifier les imports (début du fichier)

```python
# AVANT (Atelier 1-3)
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

# APRÈS (avec Database)
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends  # ✨ Ajouter Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # ✨ Ajouter JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session  # ✨ NOUVEAU
from sqlalchemy import text  # ✨ NOUVEAU

# Import database and models  # ✨ NOUVEAU
from .database import get_db, init_db  # ✨ NOUVEAU
from .models import TaskModel, TaskStatus, TaskPriority  # ✨ NOUVEAU
```

**Changement 2** : Supprimer les enums Pydantic et le stockage en mémoire

**⚠️ IMPORTANT** : Trouvez et supprimez ces sections dans votre `app.py` :

**a) Supprimer les définitions d'Enum** (autour de la ligne 27-37) :

```python
# ❌ TROUVEZ ET SUPPRIMEZ COMPLÈTEMENT CES LIGNES
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

**Raison** : Ces enums sont maintenant dans `models.py` et seront importés depuis là.

**b) Supprimer le stockage en mémoire** (autour de la ligne 71) :

```python
# ❌ TROUVEZ ET SUPPRIMEZ CETTE LIGNE
tasks_storage: List[Task] = []
```

**Raison** : On n'utilise plus de liste en mémoire, on utilise la base de données.

**c) Supprimer la fixture reset_storage des imports** (si présente dans conftest.py) :

```python
# ❌ DANS conftest.py, SUPPRIMEZ CES LIGNES SI PRÉSENTES
from src.app import app, tasks_storage  # ❌ ENLEVER tasks_storage

@pytest.fixture(autouse=True)
def reset_storage():
    """Clean the task storage..."""
    tasks_storage.clear()  # ❌ TOUT CE BLOC À SUPPRIMER
    yield
    tasks_storage.clear()
```

**Après suppression**, votre `app.py` devrait ressembler à :

```python
# Début du fichier
from contextlib import asynccontextmanager
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
import os

# Import database and models
from .database import get_db, init_db
from .models import TaskModel, TaskStatus, TaskPriority

# Configure logging
logging.basicConfig(...)

# Pydantic Models (for API validation) - GARDER CECI
class TaskBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    title: str = Field(..., min_length=1, max_length=200)
    # ... reste des champs
```

**Note** : Les modèles Pydantic (`TaskBase`, `TaskCreate`, `TaskUpdate`, `Task`) doivent être **conservés** - on les utilise toujours pour la validation de l'API !

**Changement 3** : Modifier la fonction lifespan

```python
# AVANT
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 TaskFlow backend starting up...")
    yield
    logger.info("🛑 TaskFlow backend shutting down...")

# APRÈS
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 TaskFlow backend starting up...")

    # ✨ AJOUTER ces lignes
    if not app.dependency_overrides:
        logger.info("Initializing database...")
        init_db()
        logger.info("✅ Database ready!")
    else:
        logger.info("Test mode - skipping database initialization")

    yield
    logger.info("🛑 TaskFlow backend shutting down...")
```

**Changement 4** : Modifier le health check

```python
# AVANT
@app.get("/health")
async def health_check():
    environment = os.getenv("ENVIRONMENT", "development")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": environment,
        "version": "2.1.0",
        "storage": "in-memory"
    }

# APRÈS
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):  # ✨ Ajouter db parameter
    environment = os.getenv("ENVIRONMENT", "development")

    # ✨ AJOUTER: Check database connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": environment,
        "version": "2.2.0",  # ✨ Mettre à jour la version
        "storage": "postgresql" if "postgresql" in os.getenv("DATABASE_URL", "") else "sqlite",
        "database": db_status  # ✨ AJOUTER
    }
```

**Changement 5** : Modifier les endpoints CRUD

Je vais vous montrer les changements pour chaque endpoint. **Remplacez** vos endpoints existants par ces versions :

**a) List Tasks**

```python
# APRÈS
@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
    db: Session = Depends(get_db)  # ✨ AJOUTER ce paramètre
):
    """List all tasks with optional filtering."""
    query = db.query(TaskModel)  # ✨ Utiliser DB au lieu de tasks_storage

    if status:
        query = query.filter(TaskModel.status == status.value)
    if priority:
        query = query.filter(TaskModel.priority == priority.value)
    if assignee:
        query = query.filter(TaskModel.assignee == assignee)

    tasks = query.all()
    return tasks
```

**b) Create Task**

```python
# APRÈS
@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):  # ✨ AJOUTER db
    """Create a new task."""
    logger.info(f"Creating task: {task_data.title}")

    # ✨ Créer un modèle DB au lieu d'un objet Pydantic
    db_task = TaskModel(
        id=str(uuid4()),
        **task_data.model_dump()
    )

    # ✨ Sauvegarder en base de données
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    logger.info(f"Task created successfully: {db_task.id}")
    return db_task
```

**c) Get Task**

```python
# APRÈS
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, db: Session = Depends(get_db)):  # ✨ AJOUTER db
    """Get a specific task by ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

    return task
```

**d) Update Task**

```python
# APRÈS
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    update_data: TaskUpdate,
    db: Session = Depends(get_db)  # ✨ AJOUTER db
):
    """Update an existing task."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    db.commit()  # ✨ Commit les changements
    db.refresh(task)

    return task
```

**e) Delete Task**

```python
# APRÈS
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, db: Session = Depends(get_db)):  # ✨ AJOUTER db
    """Delete a task by ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

    db.delete(task)  # ✨ Supprimer de la DB
    db.commit()

    return
```

**Changement 6** : Fixer le global exception handler

```python
# APRÈS
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(  # ✨ Retourner JSONResponse au lieu de dict
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### Étape 2.5 : Adapter les Tests

**Fichier à modifier** : `backend/tests/conftest.py`

**Remplacez tout le contenu** par :

```python
"""
Test Configuration for TaskFlow with database support.
"""

import pytest
import tempfile
import os as os_module
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import app
from src.database import Base, get_db
from src.models import TaskModel

# Use SQLite file-based database for testing
TEST_DB_FILE = tempfile.mktemp(suffix=".db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create database tables once for the entire test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    if os_module.path.exists(TEST_DB_FILE):
        os_module.remove(TEST_DB_FILE)


@pytest.fixture(autouse=True)
def clean_database():
    """Clean all data between tests."""
    yield
    session = TestSessionLocal()
    try:
        session.query(TaskModel).delete()
        session.commit()
    finally:
        session.close()


@pytest.fixture
def db_session():
    """Provide a database session for tests."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """Provide a test client with test database."""
    def override_get_db():
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
```

### Étape 2.6 : Créer les Fichiers de Configuration

**Fichier à créer** : `backend/.env.example`

```bash
# TaskFlow Backend Environment Variables
ENVIRONMENT=development
DATABASE_URL=sqlite:///./taskflow.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=true
LOG_LEVEL=INFO
```

**Fichier à créer** : `backend/.gitignore`

```text
__pycache__/
*.py[cod]
*.db
*.sqlite
.env
.env.local
htmlcov/
.coverage
.pytest_cache/
.venv/
```

### Étape 2.7 : Tester Localement

```bash
cd backend

# Installer les dépendances
uv sync

# Lancer les tests
uv run pytest -v

# Démarrer le serveur
uv run uvicorn src.app:app --reload
```

**Vérifier** :

- ✅ Tous les tests passent (19/19)
- ✅ Le serveur démarre sans erreur
- ✅ Le health check retourne `"database": "connected"`
- ✅ Un fichier `taskflow.db` est créé

**Tester l'API** :

```bash
# Health check
curl http://localhost:8000/health

# Créer une tâche
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test DB", "status": "todo", "priority": "high"}'

# Lister les tâches
curl http://localhost:8000/tasks
```

## 📚 Partie 3 : Créer la Base de Données sur Render

### 2.1 Créer l'Instance PostgreSQL

1. Aller sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquer **"New +" → "PostgreSQL"**

**Configuration** :

```yaml
Name: taskflow-db
Database: taskflow_prod
User: taskflow_user
Region: Frankfurt (même région que le backend!)
PostgreSQL Version: 17 (ou 16, 15 - toutes fonctionnent)
Plan: Free (1GB de stockage)
```

**Note** : PostgreSQL 17, 16, et 15 sont toutes compatibles avec notre code. Utilisez la version la plus récente disponible sur Render.

3. Cliquer **"Create Database"**

### 2.2 Récupérer les Informations de Connexion

Une fois créée, Render fournit :

- **Internal Database URL** : Pour se connecter depuis le backend Render
- **External Database URL** : Pour se connecter localement (debugging)
- **PSQL Command** : Pour accéder via terminal

**Important** : Utilisez l'**Internal Database URL** en production (pas de frais d'egress).

### 2.3 Configurer le Backend pour Utiliser PostgreSQL

Dans votre service backend Render :

1. Aller dans **Environment**
2. Ajouter/modifier la variable :

```bash
DATABASE_URL=<votre-internal-database-url-de-render>
```

**Note** : Render remplace automatiquement `postgres://` par `postgresql://` pour SQLAlchemy.

## 📚 Partie 3 : Développement Local avec PostgreSQL

### Option A : Utiliser SQLite Localement (Plus Simple)

SQLite est utilisé automatiquement si `DATABASE_URL` n'est pas défini :

```bash
cd backend
uv sync  # Installer les nouvelles dépendances
uv run uvicorn src.app:app --reload
```

Les données sont stockées dans `taskflow.db` (fichier local).

### Option B : Utiliser PostgreSQL Localement (Plus Proche de la Prod)

#### Avec Docker :

```bash
docker run --name taskflow-postgres \
  -e POSTGRES_DB=taskflow_dev \
  -e POSTGRES_USER=taskflow \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  -d postgres:15
```

#### Configurer l'Application :

Créer `backend/.env` :

```bash
DATABASE_URL=postgresql://taskflow:dev_password@localhost:5432/taskflow_dev
```

#### Démarrer l'Application :

```bash
uv run uvicorn src.app:app --reload
```

Les tables sont créées automatiquement au démarrage !

## 📚 Partie 4 : Opérations CRUD avec SQLAlchemy

### 4.1 Créer (Create)

```python
@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    # Créer l'instance du modèle
    db_task = TaskModel(
        id=str(uuid4()),
        **task_data.model_dump()
    )

    # Ajouter à la session
    db.add(db_task)

    # Sauvegarder en base de données
    db.commit()

    # Rafraîchir pour obtenir les valeurs générées (timestamps)
    db.refresh(db_task)

    return db_task
```

### 4.2 Lire (Read)

```python
@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    db: Session = Depends(get_db)
):
    # Construire la requête
    query = db.query(TaskModel)

    # Filtrer si nécessaire
    if status:
        query = query.filter(TaskModel.status == status.value)

    # Exécuter et retourner
    tasks = query.all()
    return tasks
```

### 4.3 Mettre à Jour (Update)

```python
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    update_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    # Trouver la tâche
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Mettre à jour les champs
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(task, field, value)

    # Sauvegarder
    db.commit()
    db.refresh(task)

    return task
```

### 4.4 Supprimer (Delete)

```python
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return
```

## 📚 Partie 5 : Tests avec Base de Données

### 5.1 Configuration des Tests (`conftest.py`)

Les tests utilisent une **base SQLite en mémoire** :

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base de données de test en mémoire
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture(autouse=True)
def setup_database():
    """Créer les tables avant chaque test."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
```

### 5.2 Override de la Dépendance

```python
@pytest.fixture
def client(db_session):
    """Client de test avec base de données de test."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
```

### 5.3 Lancer les Tests

```bash
cd backend
uv run pytest -v
```

Les tests utilisent SQLite en mémoire, donc pas besoin de PostgreSQL local !

## 📚 Partie 6 : Déploiement sur Render

### 6.1 Workflow de Déploiement

1. **Commit les changements** :

```bash
git add .
git commit -m "feat: add PostgreSQL database integration"
git push origin main
```

2. **GitHub Actions** exécute les tests automatiquement

3. **Render détecte le push** et redéploie le backend

4. **Render injecte automatiquement** `DATABASE_URL`

5. **L'application démarre** et crée les tables automatiquement

### 6.2 Vérifier le Déploiement

#### Health Check :

```bash
curl https://taskflow-backend-XXXX.onrender.com/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T...",
  "environment": "production",
  "version": "2.1.0",
  "storage": "postgresql",
  "database": "connected"
}
```

#### Créer une Tâche :

```bash
curl -X POST https://taskflow-backend-XXXX.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test from Production",
    "status": "todo",
    "priority": "high"
  }'
```

#### Lister les Tâches :

```bash
curl https://taskflow-backend-XXXX.onrender.com/tasks
```

### 6.3 Accéder à la Base de Données (Debug)

Via le dashboard Render :

1. Aller dans votre service PostgreSQL
2. Cliquer sur **"Connect"**
3. Copier la commande PSQL

Ou via le PSQL Command fourni :

```bash
PGPASSWORD=<password> psql -h <host> -U <user> <database>
```

Puis exécuter des requêtes SQL :

```sql
-- Voir toutes les tables
\dt

-- Compter les tâches
SELECT COUNT(*) FROM tasks;

-- Voir les tâches
SELECT id, title, status FROM tasks LIMIT 10;
```

## 📚 Partie 7 : Migrations de Base de Données (Avancé)

Pour des projets plus complexes, utilisez **Alembic** pour les migrations :

### Installation :

```bash
uv add alembic
```

### Initialisation :

```bash
cd backend
alembic init migrations
```

### Créer une Migration :

```bash
alembic revision --autogenerate -m "Initial tables"
```

### Appliquer les Migrations :

```bash
alembic upgrade head
```

**Note** : Pour cet atelier, nous utilisons `Base.metadata.create_all()` pour plus de simplicité.

## 🎯 Exercices Pratiques

### Exercice 1 : Ajouter un Index

Optimiser les requêtes par status :

```python
class TaskModel(Base):
    # ...
    status = Column(Enum(TaskStatus), index=True)  # Ajouter index=True
```

### Exercice 2 : Ajouter une Relation

Créer un modèle `User` et lier les tâches :

```python
class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String(100))
    tasks = relationship("TaskModel", back_populates="user")

class TaskModel(Base):
    # ...
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="tasks")
```

### Exercice 3 : Requête Complexe

Compter les tâches par statut :

```python
from sqlalchemy import func

@app.get("/tasks/stats")
async def get_stats(db: Session = Depends(get_db)):
    stats = db.query(
        TaskModel.status,
        func.count(TaskModel.id).label("count")
    ).group_by(TaskModel.status).all()

    return [{"status": s, "count": c} for s, c in stats]
```

## 🐛 Dépannage

### Problème : "Relation 'tasks' does not exist"

**Solution** : Les tables ne sont pas créées. Redémarrer l'application pour déclencher `init_db()`.

### Problème : "Connection refused"

**Solution** : Vérifier que `DATABASE_URL` est correctement définie et accessible.

### Problème : Tests échouent avec "no such table"

**Solution** : Vérifier que `setup_database` fixture est bien utilisée dans `conftest.py`.

### Problème : "Passwords do not match" sur Render

**Solution** : Copier exactement l'**Internal Database URL** sans modification.

## 📊 Checklist de Complétion

- [ ] Base PostgreSQL créée sur Render
- [ ] `DATABASE_URL` configurée dans l'environnement backend
- [ ] Application démarre localement avec la base de données
- [ ] Tests passent avec la base de test en mémoire
- [ ] Application déployée sur Render avec PostgreSQL
- [ ] Health check indique `"storage": "postgresql"`
- [ ] Données persistent après redémarrage de l'application

## 📚 Ressources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [FastAPI with Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Render PostgreSQL](https://render.com/docs/databases)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

## 🏆 Félicitations !

Vous avez maintenant une application **production-ready** avec :

✅ Base de données persistante
✅ ORM moderne avec SQLAlchemy
✅ Tests isolés et reproductibles
✅ Déploiement cloud avec PostgreSQL managé
✅ Architecture scalable et maintenable

**Prochaines étapes** :
- Ajouter l'authentification utilisateur
- Implémenter des migrations avec Alembic
- Ajouter des sauvegardes automatiques
- Configurer un monitoring de la base de données

---

**Version 2.2.0** - Atelier 3 avec Base de Données PostgreSQL 🚀
