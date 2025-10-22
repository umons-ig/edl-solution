# Migration Checklist: In-Memory → PostgreSQL

## 🎯 Quick Reference: What to Delete vs What to Keep

### ❌ À SUPPRIMER de `app.py`

```python
# 1. Supprimer les Enums (lignes ~27-37)
class TaskStatus(str, Enum):          # ❌ DELETE
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, Enum):        # ❌ DELETE
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# 2. Supprimer le stockage en mémoire (ligne ~71)
tasks_storage: List[Task] = []        # ❌ DELETE

# 3. Supprimer l'import Enum (ligne ~14)
from enum import Enum                  # ❌ DELETE
```

### ✅ À GARDER dans `app.py`

```python
# GARDER tous les modèles Pydantic pour la validation API
class TaskBase(BaseModel):             # ✅ KEEP
    model_config = ConfigDict(use_enum_values=True)
    title: str = Field(...)
    # ...

class TaskCreate(TaskBase):           # ✅ KEEP
    pass

class TaskUpdate(BaseModel):          # ✅ KEEP
    # ...

class Task(TaskBase):                 # ✅ KEEP
    model_config = ConfigDict(from_attributes=True)
    id: str
    # ...
```

### 📝 Modifications dans les Endpoints

#### Avant (Atelier 1-3)

```python
@app.get("/tasks")
async def list_tasks():
    tasks = tasks_storage.copy()      # ❌ Ancienne méthode
    return tasks

@app.post("/tasks", status_code=201)
async def create_task(task_data: TaskCreate):
    task = Task(                      # ❌ Ancienne méthode
        id=str(uuid4()),
        created_at=now,
        **task_data.model_dump()
    )
    tasks_storage.append(task)        # ❌ Ancienne méthode
    return task
```

#### Après (Atelier 3 - Partie 5)

```python
@app.get("/tasks")
async def list_tasks(db: Session = Depends(get_db)):  # ✅ Ajouter db
    tasks = db.query(TaskModel).all()                  # ✅ Nouvelle méthode
    return tasks

@app.post("/tasks", status_code=201)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):  # ✅ Ajouter db
    db_task = TaskModel(                               # ✅ Nouvelle méthode
        id=str(uuid4()),
        **task_data.model_dump()
    )
    db.add(db_task)                                   # ✅ Nouvelle méthode
    db.commit()
    db.refresh(db_task)
    return db_task
```

## 📋 Checklist Détaillée

### Étape 1: Modifications de `app.py`

- [ ] **Ligne ~14**: Supprimer `from enum import Enum`
- [ ] **Ligne ~27-37**: Supprimer `class TaskStatus` et `class TaskPriority`
- [ ] **Ligne ~71**: Supprimer `tasks_storage: List[Task] = []`
- [ ] **Ligne ~7**: Ajouter imports database:
  ```python
  from fastapi import Depends
  from fastapi.responses import JSONResponse
  from sqlalchemy.orm import Session
  from sqlalchemy import text
  from .database import get_db, init_db
  from .models import TaskModel, TaskStatus, TaskPriority
  ```

### Étape 2: Modifications des Endpoints

Pour **chaque endpoint**, ajouter `db: Session = Depends(get_db)` :

- [ ] `list_tasks()` - Remplacer `tasks_storage` par `db.query(TaskModel).all()`
- [ ] `create_task()` - Remplacer append par `db.add()`, `db.commit()`, `db.refresh()`
- [ ] `get_task()` - Remplacer boucle for par `db.query(TaskModel).filter().first()`
- [ ] `update_task()` - Ajouter `db.commit()` et `db.refresh()`
- [ ] `delete_task()` - Remplacer pop par `db.delete()` et `db.commit()`

### Étape 3: Modifications de `conftest.py`

- [ ] **Ligne ~10**: Supprimer import `tasks_storage` de `from src.app import app, tasks_storage`
- [ ] **Lignes ~13-23**: Supprimer complètement la fixture `reset_storage()`
- [ ] **Remplacer** tout le fichier par le nouveau contenu (voir guide complet)

### Étape 4: Vérification

Après les modifications:

```bash
# Les tests doivent passer
uv run pytest -v
# Output attendu: 19 passed

# Le serveur doit démarrer
uv run uvicorn src.app:app --reload
# Vérifier: un fichier taskflow.db est créé

# Health check doit montrer database
curl http://localhost:8000/health
# Output attendu: "database": "connected"
```

## 🔍 Où Trouver les Sections à Modifier

### Dans `app.py` (ordre d'apparition)

1. **Imports** (lignes 1-20) → Modifier pour ajouter database imports
2. **Enums** (lignes 27-37) → SUPPRIMER complètement
3. **Pydantic Models** (lignes 40-70) → GARDER (ne pas toucher)
4. **Storage** (ligne 71) → SUPPRIMER `tasks_storage: List[Task] = []`
5. **Lifespan** (lignes 74-82) → Ajouter `init_db()`
6. **Health Check** (lignes 121-132) → Ajouter paramètre `db` et vérification
7. **List Tasks** (lignes 135-161) → Ajouter `db` et remplacer par query
8. **Create Task** (lignes 164-184) → Ajouter `db` et utiliser ORM
9. **Get Task** (lignes 187-199) → Ajouter `db` et utiliser query
10. **Update Task** (lignes 202-225) → Ajouter `db`, commit, refresh
11. **Delete Task** (lignes 228-243) → Ajouter `db`, delete, commit
12. **Exception Handler** (lignes 247-256) → Retourner JSONResponse

### Dans `conftest.py`

- **Tout remplacer** par le nouveau code (voir guide)
- L'ancien fichier fait ~37 lignes
- Le nouveau fait ~74 lignes

## ⚠️ Erreurs Communes

### Erreur 1: Oublier de supprimer `tasks_storage`

```python
# ❌ Erreur
tasks_storage: List[Task] = []  # Ligne encore présente
# Symptôme: NameError lors de l'import

# ✅ Solution
# Supprimer complètement cette ligne
```

### Erreur 2: Oublier le paramètre `db`

```python
# ❌ Erreur
@app.get("/tasks")
async def list_tasks():  # Manque db parameter
    tasks = db.query(TaskModel).all()  # db n'est pas défini

# ✅ Solution
@app.get("/tasks")
async def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
```

### Erreur 3: Supprimer les modèles Pydantic

```python
# ❌ Ne PAS faire ça!
# class TaskBase(BaseModel):  # ❌ NE PAS SUPPRIMER
#     ...

# ✅ Les modèles Pydantic doivent rester!
class TaskBase(BaseModel):  # ✅ GARDER
    model_config = ConfigDict(use_enum_values=True)
    # ...
```

## 📊 Résumé Visuel

```
app.py (AVANT)                      app.py (APRÈS)
├── Imports                   →     ├── Imports + database imports
├── Enum TaskStatus          ❌     │
├── Enum TaskPriority        ❌     │
├── TaskBase (Pydantic)      ✅     ├── TaskBase (Pydantic) ✅
├── TaskCreate               ✅     ├── TaskCreate ✅
├── TaskUpdate               ✅     ├── TaskUpdate ✅
├── Task                     ✅     ├── Task ✅
├── tasks_storage = []       ❌     │
├── lifespan()               🔧     ├── lifespan() + init_db() 🔧
├── health_check()           🔧     ├── health_check(db) 🔧
├── list_tasks()             🔧     ├── list_tasks(db) 🔧
├── create_task()            🔧     ├── create_task(db) 🔧
├── get_task()               🔧     ├── get_task(db) 🔧
├── update_task()            🔧     ├── update_task(db) 🔧
└── delete_task()            🔧     └── delete_task(db) 🔧

Légende:
✅ GARDER (ne pas modifier)
❌ SUPPRIMER complètement
🔧 MODIFIER (ajouter paramètre db)
```

## 🎯 Guide Rapide: 5 Minutes

Si vous avez déjà lu le guide complet et voulez juste un rappel:

1. **Ouvrir** `backend/src/app.py`
2. **Chercher** `class TaskStatus` → **Supprimer** les 2 enums
3. **Chercher** `tasks_storage` → **Supprimer** cette ligne
4. **Chercher** `from enum import Enum` → **Supprimer**
5. **Ajouter** en haut:
   ```python
   from sqlalchemy.orm import Session
   from sqlalchemy import text
   from .database import get_db, init_db
   from .models import TaskModel, TaskStatus, TaskPriority
   ```
6. **Pour chaque fonction** (list_tasks, create_task, etc.):
   - Ajouter `db: Session = Depends(get_db)` comme paramètre
   - Remplacer `tasks_storage` par requêtes DB
7. **Remplacer** `backend/tests/conftest.py` entièrement
8. **Tester**: `uv run pytest -v`

---

**Temps total**: 30-45 minutes si vous suivez ce guide pas à pas
**Difficulté**: Intermédiaire
**Prérequis**: Ateliers 1, 2, et 3 (parties 1-4) complétés
