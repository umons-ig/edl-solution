# Exercices Java - SOLUTIONS COMPLÈTES

**⚠️ Ceci contient les solutions. Les étudiants doivent utiliser `edl-starter/java-exercises/`**

## 📝 Objectif

Solutions complètes des exercices basés sur Workshop-1.pdf

## 🎯 Concepts Couverts

- ✅ Tests unitaires avec JUnit 4
- ✅ Pattern Arrange-Act-Assert (AAA)
- ✅ Assertions (`assertEquals`, `assertTrue`, `assertFalse`)
- ✅ Gestion des exceptions avec `@Test(expected = ...)`
- ✅ Fixtures avec `@Before`
- ✅ Validation des entrées
- ✅ Tests de cas limites (edge cases)

## 📚 Les 3 Exercices

### Exercice 1 : Calculator (15-20 min)
**Dossier:** `calculator/`

Opérations arithmétiques simples avec gestion de la division par zéro.

**Méthodes à implémenter:**
- ✅ `add(int a, int b)` - Déjà implémentée
- ⚠️ `subtract(int a, int b)`
- ⚠️ `multiply(int a, int b)`
- ⚠️ `divide(int a, int b)` - Lever `ArithmeticException` si b == 0

**Tests à écrire:**
- Tests des 4 opérations
- Test de division par zéro

---

### Exercice 2 : StringUtils (20-25 min)
**Dossier:** `string-utils/`

Manipulation de chaînes de caractères avec validation null.

**Méthodes à implémenter:**
- ✅ `reverse(String str)` - Déjà implémentée
- ⚠️ `isPalindrome(String str)`
- ⚠️ `countVowels(String str)`
- ⚠️ `countWords(String str)`

**Tests à écrire:**
- Tests des méthodes avec cas normaux
- Tests avec chaîne vide
- Tests avec `null` (doivent lever `IllegalArgumentException`)

---

### Exercice 3 : BankAccount (25-30 min)
**Dossier:** `bank-account/`

Gestion de compte bancaire avec validation de solde et transferts.

**Méthodes à implémenter:**
- ✅ Constructeur avec validation - Déjà implémenté
- ⚠️ `deposit(double amount)`
- ⚠️ `withdraw(double amount)`
- ⚠️ `transfer(BankAccount destination, double amount)`

**Tests à écrire:**
- Tests du constructeur avec validation
- Tests deposit/withdraw
- Test de solde insuffisant (`IllegalStateException`)
- Tests de transfert entre comptes

## 🚀 Comment Lancer les Tests

### Option 1 : Avec VSCode (Recommandé pour ce TP)

**⚠️ IMPORTANT - Extensions requises :**

Dans VSCode, installez ces 2 extensions :
1. **Language Support for Java(TM) by Red Hat**
2. **Extension Pack for Java** (par Microsoft)

**Installation rapide :**
```bash
code --install-extension redhat.java
code --install-extension vscjava.vscode-java-pack
```

**Ensuite :**
1. **Ouvrir le dossier** : File → Open Folder → `java-exercises/`
2. **Attendre 30 secondes** que VSCode indexe les fichiers
3. **Ouvrir un test** (ex: `calculator/CalculatorTest.java`)
4. **Cliquer sur l'icône ▶️** à côté de `@Test`

**VSCode détecte automatiquement JUnit !** ✨

### Option 2 : Avec IntelliJ IDEA

1. Ouvrir IntelliJ IDEA
2. File → Open → Sélectionner un dossier d'exercice (ex: `calculator/`)
3. Clic droit sur le fichier `*Test.java`
4. Sélectionner "Run '*Test'"

### Option 3 : Avec ligne de commande Java

```bash
# Compiler
javac -cp .:junit-4.13.2.jar:hamcrest-core-1.3.jar Calculator.java CalculatorTest.java

# Lancer les tests
java -cp .:junit-4.13.2.jar:hamcrest-core-1.3.jar org.junit.runner.JUnitCore CalculatorTest
```

## 📦 Prérequis

- **Java 21 (LTS)** installé - [Télécharger ici](https://adoptium.net/)
- **VSCode** avec extension `Extension Pack for Java` (recommandé)
  - OU **IntelliJ IDEA** (alternative)
- **JUnit 4.13.2** (automatiquement géré par VSCode/IntelliJ)

**Vérifier votre version Java :**
```bash
java -version  # Doit afficher version 21.x.x
```

### Installation rapide pour VSCode

```bash
# 1. Installer les 2 extensions nécessaires
code --install-extension redhat.java
code --install-extension vscjava.vscode-java-pack

# 2. Recharger VSCode (Cmd+Shift+P → Reload Window)

# 3. Ouvrir le dossier
code java-exercises/

# 4. VSCode télécharge JUnit automatiquement !
```

**Extensions requises :**
- ✅ `Language Support for Java(TM) by Red Hat`
- ✅ `Extension Pack for Java` (Microsoft)

### Si JUnit n'est pas détecté automatiquement

Télécharger dans le dossier `lib/` :
- [junit-4.13.2.jar](https://search.maven.org/artifact/junit/junit/4.13.2/jar)
- [hamcrest-core-1.3.jar](https://search.maven.org/artifact/org.hamcrest/hamcrest-core/1.3/jar)

## 💡 Exemple de Test (Pattern AAA)

```java
@Test
public void testAdd() {
    // Arrange (préparer les données)
    int a = 2;
    int b = 3;

    // Act (exécuter l'action)
    int result = Calculator.add(a, b);

    // Assert (vérifier le résultat)
    assertEquals(5, result);
}
```

## 🔄 Comparaison Python vs Java

| Concept | Python (pytest) | Java (JUnit) |
|---------|----------------|--------------|
| Annotation de test | `def test_xxx():` | `@Test public void testXxx()` |
| Assertion | `assert x == 5` | `assertEquals(5, x)` |
| Exception attendue | `pytest.raises(ValueError)` | `@Test(expected = IllegalArgumentException.class)` |
| Setup avant test | `@pytest.fixture` | `@Before` |
| Lancer les tests | `pytest` | Clic droit → Run |

## ✅ Résultat Attendu

Pour chaque exercice, tous les tests doivent passer :

```
Tests run: X, Failures: 0, Errors: 0, Skipped: 0

BUILD SUCCESS
```

## 📖 Ressources

- [JUnit 4 Documentation](https://junit.org/junit4/)
- [Guide des Assertions JUnit](https://junit.org/junit4/javadoc/latest/org/junit/Assert.html)
- [Bonnes pratiques TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

## ⏱️ Durée Totale Estimée

**1h - 1h15** pour les 3 exercices

---

**Bon courage ! 🚀**
