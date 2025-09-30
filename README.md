# Examples Branch - Complete Reference Implementations

This branch contains **complete, working examples** demonstrating Test-Driven Development and testing best practices.

## 📚 Available Examples

### 1. Calculator
**Location**: `calculator/`

A complete TDD example showing:
- ✅ All tests passing
- ✅ Exception handling
- ✅ Parameterized tests
- ✅ Test organization with classes
- ✅ Clear documentation

```bash
# From root directory
uv sync
uv run pytest calculator/test_calculator.py -v
uv run python calculator/calculator.py
```

**What to learn**:
- Basic pytest syntax
- Testing exceptions with `pytest.raises`
- Using `@pytest.mark.parametrize`
- Error handling patterns

📖 See [calculator/README.md](calculator/README.md) for details

---

## 🎯 How to Use These Examples

These examples are **reference material** for the workshops. They show the complete, working code so you can:

1. **Understand the patterns** before implementing them yourself
2. **Reference when stuck** during workshop exercises
3. **See best practices** in action

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/umons-ig/edl-tp-1.git
cd edl-tp-1

# Checkout examples branch
git checkout examples

# Install dependencies (from root)
uv sync

# Run calculator tests
uv run pytest calculator/test_calculator.py -v

# Run calculator demo
uv run python calculator/calculator.py
```

## 📖 Workshop Flow

1. **Instructor demos** using code from this branch
2. **Students explore** these examples to understand patterns
3. **Students switch to workshop branch** to implement from scratch
4. **Students can reference back** to these examples when needed

## 🔄 Switching to Workshops

After exploring examples, start the actual workshops:

```bash
# Workshop 1: Weather API
git checkout workshop-1
uv sync
uv run pytest
# Follow the README in that branch

# Workshop 2: URL Shortener
git checkout workshop-2
uv sync
# Coming soon...
```

## 📝 Note

**These examples are COMPLETE**.
The workshop branches have **incomplete starter code** that you'll implement yourself.

---

## 🤝 Adding More Examples

To add more examples to this branch:

```bash
git checkout examples

# Create new example directory
mkdir new-example/

# Add code, tests to new-example/
# Update pyproject.toml at root if needed
# Commit changes
```

## 📚 Resources

- [Main README](../main/README.md) - Workshop overview
- [Setup Guide](../main/docs/setup-guide.md) - Installation instructions
- [pytest Cheatsheet](../main/docs/pytest-cheatsheet.md) - Testing reference

---

**Ready to start the workshops?**

```bash
git checkout workshop-1
```