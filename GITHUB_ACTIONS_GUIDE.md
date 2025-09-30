# GitHub Actions CI/CD Setup Guide

This guide will walk you through setting up automated testing with GitHub Actions.

## What is CI/CD?

**Continuous Integration (CI)** automatically runs tests every time you push code to GitHub. This helps catch bugs early and ensures your code always works.

## Step-by-Step Instructions

### Step 1: Create the Workflow Directory

```bash
mkdir -p .github/workflows
```

### Step 2: Create the Workflow File

Create a new file `.github/workflows/test.yml`:

```bash
touch .github/workflows/test.yml
```

### Step 3: Add the Workflow Configuration

Open `.github/workflows/test.yml` and paste the following content:

```yaml
name: Weather API Tests

on:
  push:
    branches: ['*']
  pull_request:
    branches: ['main']

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Install uv
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"

    - name: Set up Python
      run: uv python install 3.11

    - name: Install dependencies
      run: uv sync

    - name: Run tests
      run: uv run pytest -v

    - name: Run tests with coverage
      run: uv run pytest --cov=app --cov-report=term -v
```

### Step 4: Understand the Configuration

Let's break down what each part does:

#### Trigger Configuration
```yaml
on:
  push:
    branches: ['*']       # Run on pushes to any branch
  pull_request:
    branches: ['main']    # Run on PRs to main branch
```

#### Job Configuration
```yaml
jobs:
  test:
    runs-on: ubuntu-latest  # Use Ubuntu Linux VM
```

#### Steps

1. **Checkout code** - Downloads your repository
   ```yaml
   - uses: actions/checkout@v4
   ```

2. **Install uv** - Sets up the uv package manager
   ```yaml
   - uses: astral-sh/setup-uv@v3
   ```

3. **Set up Python** - Installs Python 3.11
   ```yaml
   - run: uv python install 3.11
   ```

4. **Install dependencies** - Installs your project dependencies
   ```yaml
   - run: uv sync
   ```

5. **Run tests** - Executes your test suite
   ```yaml
   - run: uv run pytest -v
   ```

6. **Run tests with coverage** - Shows code coverage
   ```yaml
   - run: uv run pytest --cov=app --cov-report=term -v
   ```

### Step 5: Commit and Push

```bash
git add .github/workflows/test.yml
git commit -m "ci: add GitHub Actions workflow for automated testing"
git push origin workshop-1
```

### Step 6: Verify on GitHub

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see your workflow running
4. Click on the workflow run to see detailed logs
5. Wait for it to complete - green ✅ means tests passed!

## Viewing Results

### In the GitHub UI

Navigate to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

You'll see:
- ✅ Green checkmark = All tests passed
- ❌ Red X = Tests failed
- 🟡 Yellow circle = Tests running

Click on any run to see:
- Which tests passed/failed
- Complete logs
- Code coverage report

### In Pull Requests

When you create a PR, GitHub will automatically:
1. Run the tests
2. Show the status in the PR
3. Block merging if tests fail (optional, requires branch protection)

## Troubleshooting

### Workflow not running?

1. **Check file location**: Must be exactly `.github/workflows/test.yml`
2. **Check YAML syntax**: Use https://www.yamllint.com/ to validate
3. **Check branch name**: Make sure you're pushing to the right branch

### Tests failing in CI but passing locally?

1. **Check Python version**: CI uses 3.11, make sure local matches
2. **Check dependencies**: Ensure `pyproject.toml` has all dependencies
3. **Check environment variables**: CI doesn't have your local `.env` file

### Need to see detailed logs?

```yaml
# Add this step for debugging
- name: Debug info
  run: |
    uv python list
    uv pip list
    ls -la
```

## Optional Enhancements

### Test on Multiple Python Versions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']

    steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v3
    - run: uv python install ${{ matrix.python-version }}
    - run: uv sync
    - run: uv run pytest -v
```

### Add Code Coverage Badge

Add to your README.md:
```markdown
![Tests](https://github.com/USERNAME/REPO/actions/workflows/test.yml/badge.svg)
```

### Cache Dependencies for Faster Builds

```yaml
- name: Cache uv dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}
```

## What Happens When CI Fails?

When tests fail in CI:

1. **Don't panic!** This is normal and helpful
2. **Read the logs** - They tell you exactly what failed
3. **Fix locally** - Make tests pass on your machine first
4. **Push again** - CI will automatically re-run

Example workflow:
```bash
# Tests failed in CI - check locally
uv run pytest -v

# Fix the issue
# ... edit code ...

# Verify fix
uv run pytest -v

# Push fixed code
git add .
git commit -m "fix: resolve test failures"
git push
```

## Best Practices

1. ✅ **Always push working code** - Run tests locally before pushing
2. ✅ **Keep tests fast** - CI should complete in a few minutes
3. ✅ **Fix failing tests immediately** - Don't let them accumulate
4. ✅ **Review CI logs** - Even when tests pass, check for warnings
5. ✅ **Use branch protection** - Require CI to pass before merging

## Next Steps

After setting up CI:

1. Make all tests pass locally
2. Push to GitHub
3. Verify CI passes
4. Create a pull request
5. See CI run automatically on your PR
6. Merge when green ✅

---

**Congratulations!** You now have automated testing set up. Every push will automatically run your tests and tell you if something broke. This is how professional software teams work! 🎉