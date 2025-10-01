# Guide d'installation

## Prérequis

- Python 3.11+
- Git
- Éditeur de code (VS Code recommandé)

## Installation de uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Vérification:**
```bash
uv --version
```

## Configuration du projet

```bash
# Cloner le dépôt
git clone https://github.com/umons-ig/edl-tp-1.git
cd edl-tp-1

# Passer sur la branche workshop
git checkout workshop-1

# Installer les dépendances
uv sync

# Lancer les tests
uv run pytest
```

## Commandes essentielles

```bash
# Installer les dépendances
uv sync

# Lancer les tests
uv run pytest

# Lancer les tests (mode verbeux)
uv run pytest -v
```
