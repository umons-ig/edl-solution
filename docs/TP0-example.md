# TP0: Exemple Calculatrice - Introduction au TDD

Ce document explique l'exemple de la calculatrice utilisé pour introduire les concepts du développement piloté par les tests (TDD).

## Objectif

L'exemple de la calculatrice est une **démonstration rapide** (30 minutes) pour montrer:
- Comment pytest fonctionne
- Le cycle TDD (Red → Green → Refactor)
- Écrire les tests avant le code
- Comment les tests guident l'implémentation

Après cette démo, les étudiants travailleront sur le projet principal (API Météo).

## Où le Trouver

L'exemple complet de la calculatrice se trouve dans la branche `examples`:

```bash
git checkout examples
cd calculator/
uv sync
uv run pytest -v
```

## Le Cycle TDD

### 🔴 Red: Écrire un Test qui Échoue

```python
# test_calculator.py
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

Lancer le test:
```bash
uv run pytest test_calculator.py::test_divide_by_zero -v
```

**Résultat**: Le test échoue ❌ (ZeroDivisionError n'est pas levée)

### 🟢 Green: Écrire le Code Minimal pour Passer

```python
# calculator.py
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

Relancer le test:
```bash
uv run pytest test_calculator.py::test_divide_by_zero -v
```

**Résultat**: Le test passe ✅

### 🔵 Refactor: Améliorer la Qualité du Code

Dans ce cas simple, le code est déjà propre. Pour des scénarios plus complexes:
- Extraire la logique dupliquée
- Améliorer le nommage
- Ajouter des commentaires si nécessaire
- **Garder les tests verts**

### 🔁 Répéter

Continuez avec le test suivant!

## Exemples de Fonctions dans la Calculatrice

### 1. Division avec Vérification de Zéro

**Fonction**: `divide(a, b)`

**Test**:
```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

**Points d'Enseignement**:
- Gestion des exceptions
- Tester les exceptions avec `pytest.raises`
- Les messages d'erreur sont importants

---

### 2. Puissance avec Exposants Négatifs

**Fonction**: `power(base, exponent)`

**Test**:
```python
def test_power_negative_exponent():
    assert power(2, -1) == 0.5
    assert power(4, -2) == 0.0625
```

**Points d'Enseignement**:
- Récursion
- Cas limites (entrées négatives)
- Opérations mathématiques

**Implémentation**:
```python
def power(base, exponent):
    if exponent == 0:
        return 1
    elif exponent < 0:
        return 1 / power(base, -exponent)
    else:
        result = base
        for _ in range(exponent - 1):
            result *= base
        return result
```

---

### 3. Factorielle avec Validation

**Fonction**: `factorial(n)`

**Tests**:
```python
@pytest.mark.parametrize("n, expected", [
    (0, 1),      # Cas spécial: 0! = 1
    (1, 1),
    (3, 6),
    (5, 120),
])
def test_factorial_valid(n, expected):
    assert factorial(n) == expected

def test_factorial_negative():
    with pytest.raises(ValueError, match="negative"):
        factorial(-1)
```

**Points d'Enseignement**:
- Tests paramétrés (plusieurs cas de test en un)
- Validation des entrées
- Cas spéciaux (0! = 1)

---

### 4. Moyenne d'une Liste Vide

**Fonction**: `average(numbers)`

**Test**:
```python
def test_average_empty_list():
    with pytest.raises(ValueError, match="empty list"):
        average([])
```

**Points d'Enseignement**:
- Gestion des collections vides
- Validation avant calcul
- Messages d'erreur descriptifs

**Implémentation**:
```python
def average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

## Déroulement de l'Atelier

### Phase 1: Démo de l'Instructeur (15 minutes)

1. **Montrer le test qui échoue** (Red)
   ```bash
   uv run pytest test_calculator.py::test_divide_by_zero -v
   ```

2. **Coder la correction en direct** (Green)
   - Ajouter la vérification `if b == 0:`
   - Lever l'exception
   - Montrer le test qui passe

3. **Expliquer le processus**
   - Le test indique quoi construire
   - Le test confirme que ça fonctionne
   - Répéter pour toutes les fonctionnalités

### Phase 2: Les Étudiants Explorent (15 minutes)

Les étudiants passent sur la branche `examples` et:
- Lancent tous les tests de la calculatrice
- Lisent le code
- Comprennent les patterns
- Posent des questions

```bash
git checkout examples
cd calculator/
uv sync
uv run pytest -v
```

### Phase 3: Transition vers le Projet Principal (5 minutes)

- "Maintenant vous comprenez les bases"
- "Appliquons cela à un vrai projet: l'API Météo"
- "Vous allez écrire des tests et du code pour les faire passer"

```bash
git checkout workshop-1
uv sync
uv run pytest
# Voir les tests qui échouent → c'est parti!
```

## Points Clés à Retenir

Après cet exemple, les étudiants devraient comprendre:

1. ✅ **Cycle TDD**: Red → Green → Refactor
2. ✅ **Bases de pytest**:
   - Instructions `assert`
   - `pytest.raises` pour les exceptions
   - `@pytest.mark.parametrize` pour plusieurs cas
3. ✅ **Lancer les tests**: `uv run pytest -v`
4. ✅ **Lire la sortie des tests**: Ce qui a échoué, pourquoi, et comment corriger
5. ✅ **Les tests comme documentation**: Les tests montrent comment le code doit se comporter

## Questions Fréquentes

### Q: Pourquoi écrire les tests en premier?
**R**: Les tests définissent ce que signifie "terminé". Ils guident l'implémentation et préviennent la sur-ingénierie.

### Q: N'est-ce pas plus lent?
**R**: Au début oui, mais vous gagnez du temps en débogage et gagnez en confiance lors des changements.

### Q: Est-ce que je teste tout?
**R**: Testez le comportement, pas l'implémentation. Concentrez-vous sur les cas limites et les chemins critiques.

### Q: Et si les exigences changent?
**R**: Mettez à jour les tests d'abord, puis le code. Les tests s'adaptent avec les exigences.

## Prochaines Étapes

Après avoir terminé la démo de la calculatrice:
1. Les étudiants doivent passer sur la branche `workshop-1`
2. Lire le README du workshop
3. Commencer à construire l'API Météo
4. Appliquer les principes TDD appris ici

---

**Allocation de temps**: 30 minutes au total
- Démo: 15 min
- Les étudiants explorent: 15 min
- Questions tout au long
