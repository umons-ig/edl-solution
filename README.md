# Python Testing Workshops

A hands-on workshop series teaching Test-Driven Development (TDD), unit testing with pytest, and CI/CD with GitHub Actions.

## 🎯 Workshop Goals

By completing this workshop series, you will:
- Master modern Python dependency management with **uv**
- Write effective unit tests with **pytest**
- Apply Test-Driven Development principles
- Mock external dependencies in tests
- Set up Continuous Integration with **GitHub Actions**
- Build and test real-world applications

## 📚 Workshop Series

### Workshop 1: TDD Fundamentals & CI/CD (3 hours)
**Project**: Weather API Wrapper

Learn the basics of test-driven development by building a weather API that wraps OpenWeatherMap.

**Topics covered**:
- Introduction to TDD (Red-Green-Refactor cycle)
- Writing unit tests with pytest
- Mocking external API calls
- Error handling and edge cases
- Setting up GitHub Actions CI/CD

**Branch**: `workshop-1`

---

### Workshop 2: Database Testing & Integration (3 hours)
**Project**: URL Shortener

Build a URL shortener service with database persistence and learn integration testing strategies.

**Topics covered**:
- Database testing with SQLite/Postgres
- Integration vs unit testing
- Test fixtures and setup/teardown
- Testing CRUD operations
- Advanced pytest features

**Branch**: `workshop-2`

---

### Workshop 3: Advanced Testing Patterns (3 hours)
**Project**: TBD

Advanced testing techniques for production applications.

**Topics covered**:
- Property-based testing
- Performance testing
- Code coverage analysis
- Testing async code
- Best practices and patterns

**Branch**: `workshop-3`

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Git**
- **uv** (modern Python package manager)
- **GitHub account**
- **Text editor** (VS Code recommended)

### Installation

1. **Install uv**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Verify installation
   uv --version
   ```

2. **Clone this repository**
   ```bash
   git clone https://github.com/umons-ig/edl-tp-1.git
   cd edl-tp-1
   ```

3. **(Optional) Explore examples**
   ```bash
   git checkout examples
   # Browse complete examples (calculator demo, mocking examples)
   ```

4. **Start Workshop 1**
   ```bash
   git checkout workshop-1
   uv sync
   uv run pytest
   # Follow the README.md in that branch
   ```

## 📖 Branch Structure

- **`main`** - This overview page and documentation
- **`examples`** - Complete reference implementations (calculator demo, mocking examples)
- **`workshop-1`** - Weather API exercises (incomplete starter code)
- **`workshop-2`** - URL Shortener exercises (incomplete starter code)
- **`workshop-3`** - Advanced testing exercises (incomplete starter code)

## 💡 How to Use This Repository

Each workshop is on its own branch with:
- Incomplete starter code (with TODOs)
- Test files that guide your implementation
- README with detailed instructions
- GitHub Actions workflow for CI/CD

**Workflow**:
1. Checkout the workshop branch
2. Read the README
3. Run tests to see what's failing
4. Implement code to make tests pass
5. Push and see CI/CD in action

## 📝 Learning Path

```
examples branch (optional)
    ↓
workshop-1: TDD basics + mocking
    ↓
workshop-2: Database + integration tests
    ↓
workshop-3: Advanced patterns
```

## 🛠️ Tools & Technologies

- **uv** - Fast Python package manager
- **pytest** - Testing framework
- **FastAPI** - Modern web framework
- **GitHub Actions** - CI/CD platform
- **SQLite/Postgres** - Database (workshop 2+)

## 📚 Additional Resources

See the [`docs/`](docs/) folder for:
- [Setup Guide](docs/setup-guide.md) - Detailed installation instructions
- [pytest Cheatsheet](docs/pytest-cheatsheet.md) - Quick reference
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## 🤝 Contributing

Found an issue or have a suggestion? Please open an issue or submit a pull request!

## 📄 License

This workshop material is for educational purposes.

## 👨‍🏫 Instructors

Created for UMONS software engineering courses.

---

**Ready to start?**
```bash
git checkout workshop-1
```