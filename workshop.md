# Python Testing Workshop: Test-Driven Development with PyTest

## Workshop Overview

This workshop introduces students to **Test-Driven Development (TDD)** and **Continuous Integration (CI)** practices using Python, pytest, and GitHub Actions. Students will learn to write robust code by fixing bugs guided by failing tests.

## Learning Goals

### Primary Objectives

- **Test-Driven Development**: Understand the TDD cycle (Red → Green → Refactor)
- **Unit Testing**: Write and understand unit tests using pytest
- **Continuous Integration**: Set up automated testing with GitHub Actions
- **Error Handling**: Implement proper exception handling in Python
- **Code Quality**: Write clean, testable, and maintainable code

### Technical Skills

- Using pytest for unit testing
- Git workflow with feature branches
- GitHub Actions for CI/CD
- Python error handling with exceptions
- Code debugging and problem-solving

## Workshop Structure

### Exercise 1: Unit Testing Fundamentals

**Branch**: `exercice-1-test-unitaire`

**Goal**: Fix calculator functions to make unit tests pass

**Tasks**:

1. **Division Function** (`divide()`)
   - Handle division by zero
   - Raise `ZeroDivisionError` with appropriate message

2. **Power Function** (`power()`)
   - Support negative exponents
   - Return correct fractional results

3. **Factorial Function** (`factorial()`)
   - Complete implementation for all test cases
   - Handle edge cases (0!, 1!, negative numbers)

4. **Average Function** (`average()`)
   - Handle empty list input
   - Raise `ValueError` for invalid input

**Success Criteria**: All unit tests in `test_calculator.py` pass locally

### Exercise 2: Integration Testing & CI

**Branch**: `exercice-2-test-integration`

**Goal**: Implement continuous integration with GitHub Actions

**Tasks**:

1. **GitHub Actions Setup**
   - Configure workflow to run on multiple branches
   - Set up Python environment with `uv`
   - Run pytest automatically on push/PR

2. **Integration Testing**
   - Ensure all functions work together
   - Test edge cases and error conditions
   - Verify CI pipeline runs successfully

3. **Git Workflow**
   - Practice feature branch workflow
   - Create pull requests with passing tests
   - Merge only when CI passes

**Success Criteria**: Green CI pipeline with all tests passing

### Exercise 3: Building the Backend API
**Branch**: `exercice-3-backend-api`

**Goal**: Expose the calculator's functionality through a web API using FastAPI.

**Tasks**:
1.  **API Creation**
    *   Create a new file `api.py`.
    *   Use FastAPI to define endpoints for each calculator function (e.g., `/add`, `/divide`).
    *   Implement logic to call the existing `calculator.py` functions.
2.  **Error Handling**
    *   Ensure the API correctly propagates errors from the calculator, returning appropriate HTTP status codes (e.g., 400 for bad requests like division by zero).
3.  **API Testing (Optional)**
    *   Add tests for the API endpoints to ensure they work as expected.

**Success Criteria**:
*   A running FastAPI application serving the calculator functions.
*   API endpoints are tested and handle errors gracefully.

### Exercise 4: Building and Testing the Frontend
**Branch**: `exercice-4-frontend-ui`

**Goal**: Develop a user interface for the calculator using React and TypeScript, and write unit tests for the components.

**Tasks**:
1.  **Project Setup**
    *   In a new `frontend/` directory, initialize a React project using Vite with the TypeScript template.
2.  **Component Development**
    *   Build the UI components: a display screen, number buttons, and operation buttons.
3.  **Frontend Unit Testing**
    *   Write unit tests for your components using Vitest.
    *   **Test Scenarios**:
        *   Ensure all buttons render correctly.
        *   Simulate button clicks and verify the display updates as expected.
        *   Test the component's behavior with different inputs.

**Success Criteria**:
*   A visually complete calculator interface built with React and TypeScript.
*   All frontend unit tests pass, ensuring UI components are reliable.

### Exercise 5: Full-Stack Integration with Custom Hooks
**Branch**: `exercice-5-full-stack-integration`

**Goal**: Connect the React frontend to the FastAPI backend to create a fully functional web application.

**Tasks**:
1.  **API Client Hook**
    *   Create a custom React hook (e.g., `useCalculatorApi.ts`) to encapsulate the logic for making API calls to the backend.
    *   This hook should manage loading, error, and data states.
2.  **Integration**
    *   Use the custom hook in your components to perform calculations by calling the backend API.
    *   Display the results or any errors returned by the API on the screen.
3.  **CI Pipeline Update**
    *   Modify the GitHub Actions workflow (`.github/workflows/test.yml`) to install Node.js, install frontend dependencies, and run the frontend tests in addition to the backend tests.

**Success Criteria**:
*   The web application can successfully perform calculations using the backend API.
*   Frontend code is clean and reusable due to the custom hook.
*   The CI pipeline automatically verifies both backend (Python) and frontend (TypeScript) tests.

## Technical Requirements

### Environment Setup

- **Python**: 3.8+ recommended
- **Package Manager**: `uv` (modern Python package manager)
- **Testing Framework**: `pytest`
- **CI Platform**: GitHub Actions
- **Git**: For version control and collaboration

### Dependencies

```toml
[project]
dependencies = [
    "pytest>=7.0.0"
]
```

### Project Structure

```
edl-tp-1/
├── calculator.py          # Main calculator functions (with bugs!)
├── test_calculator.py     # Test suite (your guide to success)
├── main.py               # Demo script
├── pyproject.toml        # Project configuration
├── .github/workflows/    # CI configuration
└── README.md             # Quick start guide
```

## Testing Strategies

### 1. Test-Driven Development Cycle

1. **Red**: Run tests → See failures
2. **Green**: Write minimal code to pass tests  
3. **Refactor**: Improve code while keeping tests green
4. **Repeat**: Continue until all tests pass

### 2. Test Categories

- **Happy Path**: Normal, expected inputs
- **Edge Cases**: Boundary conditions (0, empty lists)
- **Error Cases**: Invalid inputs that should raise exceptions
- **Parameterized Tests**: Multiple input/output combinations

### 3. Exception Handling Strategy

- Use specific exception types (`ZeroDivisionError`, `ValueError`)
- Include descriptive error messages
- Test both the exception type and message content

## GitHub Actions Workflow

### Trigger Configuration

```yaml
on:
  push:                    # Run on all branches
  pull_request:
    branches: [ main ]     # Run on PRs to main
```

### Pipeline Steps

1. **Environment Setup**: Install Python and uv
2. **Dependency Installation**: `uv sync`
3. **Test Execution**: `uv run pytest`
4. **Status Reporting**: Pass/fail status visible in GitHub

## Workshop Timeline

### Session 1 (90 minutes)
- **Setup** (15 min): Environment and tools
- **Theory** (20 min): TDD principles and pytest basics
- **Exercise 1** (45 min): Fix calculator functions
- **Wrap-up** (10 min): Test results and questions

### Session 2 (90 minutes)  
- **Review** (10 min): Previous session recap
- **CI/CD** (20 min): GitHub Actions theory and setup (Exercise 2)
- **Backend API** (50 min): Build the FastAPI service (Exercise 3)
- **Wrap-up** (10 min): Demo API and Q&A

### Session 3 (90 minutes)
- **Frontend UI** (45 min): Build and test React components (Exercise 4)
- **Integration** (35 min): Connect frontend and backend with hooks (Exercise 5)
- **Final Demo** (10 min): Showcase the full-stack application

## Common Pitfalls & Solutions

### Pitfall 1: Division by Zero

**Problem**: Not handling `b == 0` in divide function
**Solution**: Add explicit check and raise `ZeroDivisionError`

### Pitfall 2: Negative Exponents

**Problem**: Power function doesn't handle negative exponents
**Solution**: Use recursion: `1 / power(base, -exponent)`

### Pitfall 3: Empty List Average

**Problem**: `sum([]) / len([])` causes division by zero
**Solution**: Check `if not numbers:` before calculation

### Pitfall 4: CI Not Running

**Problem**: Workflow only runs on main branch
**Solution**: Configure `on: push` for all branches

## Extension Challenges

### For Advanced Students

1. **Performance Testing**: Add timing tests for large inputs
2. **Property-Based Testing**: Use Hypothesis for random test generation
3. **Code Coverage**: Measure and improve test coverage
4. **Type Hints**: Add static typing with mypy
5. **Documentation**: Generate docs with Sphinx

### Real-World Applications

- **Calculator Library**: Package for distribution
- **Web API**: Flask/FastAPI wrapper
- **CLI Tool**: Command-line calculator interface
- **Mobile Integration**: Python backend for mobile apps
