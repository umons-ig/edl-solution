# Setup Guide

Complete installation and setup instructions for the Python Testing Workshops.

## Prerequisites

### 1. Python 3.11 or higher

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

**Install Python:**
- **macOS**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11` (Ubuntu/Debian) or `sudo dnf install python3.11` (Fedora)
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### 2. Git

**Check if Git is installed:**
```bash
git --version
```

**Install Git:**
- **macOS**: `brew install git` or install Xcode Command Line Tools
- **Linux**: `sudo apt install git` (Ubuntu/Debian)
- **Windows**: Download from [git-scm.com](https://git-scm.com/downloads)

### 3. Text Editor

**Recommended: VS Code**
- Download from [code.visualstudio.com](https://code.visualstudio.com/)
- Install Python extension
- Install Pylance extension (optional, for better IntelliSense)

**Alternatives:**
- PyCharm
- Sublime Text
- Vim/Neovim
- Any text editor you're comfortable with

## Installing uv

uv is a modern, fast Python package manager that replaces pip and virtualenv.

### Recommended: Standalone Installer

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternative with wget:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Alternative Installation Methods

**With pipx (recommended if you prefer pip):**
```bash
pipx install uv
```

**With pip:**
```bash
pip install uv
```

**With Homebrew (macOS):**
```bash
brew install uv
```

**With WinGet (Windows):**
```bash
winget install --id=astral-sh.uv -e
```

**With Scoop (Windows):**
```bash
scoop install main/uv
```

**With Cargo (build from source):**
```bash
cargo install --git https://github.com/astral-sh/uv uv
```

### Verify Installation

```bash
uv --version
```

You should see output like: `uv 0.x.x`

### Installing Python with uv

uv can also manage Python installations for you:

```bash
# Install Python 3.11
uv python install 3.11

# Install multiple versions
uv python install 3.11 3.12

# Check installed Python versions
uv python list
```

**Note**: uv uses standalone Python builds from Astral's `python-build-standalone` project, which are optimized for performance and compatibility.

## Setting Up the Workshop Repository

### 1. Clone the Repository

```bash
git clone https://github.com/umons-ig/edl-tp-1.git
cd edl-tp-1
```

### 2. Explore the Structure

```bash
# View available branches
git branch -a

# Main branch has overview and docs
git checkout main
cat README.md

# Examples branch has complete reference code
git checkout examples

# Workshop branches have exercises
git checkout workshop-1
```

### 3. Install Dependencies (for each workshop)

```bash
# Make sure you're on the workshop branch
git checkout workshop-1

# Sync dependencies (creates virtual environment automatically)
uv sync

# Run tests to verify setup
uv run pytest
```

## GitHub Setup

### 1. Create a GitHub Account
If you don't have one: [github.com/signup](https://github.com/signup)

### 2. Fork the Repository (Optional)
If you want to push your changes:
1. Go to [github.com/umons-ig/edl-tp-1](https://github.com/umons-ig/edl-tp-1)
2. Click "Fork" button
3. Clone your fork instead:
   ```bash
   git clone https://github.com/YOUR_USERNAME/edl-tp-1.git
   ```

### 3. Set Up Git Credentials

```bash
# Configure your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## uv Basics

### Common Commands

```bash
# Install dependencies from pyproject.toml
uv sync

# Run a Python command
uv run python app.py

# Run pytest
uv run pytest

# Run pytest with verbose output
uv run pytest -v

# Add a new dependency
uv add requests

# Add a development dependency
uv add --dev pytest-cov

# Show installed packages
uv pip list

# Create a new project
uv init my-project
```

### Understanding the Virtual Environment

uv automatically creates and manages a virtual environment in `.venv/`:

```bash
# Activate manually (usually not needed with uv run)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

**Note**: With `uv run`, you don't need to activate the virtual environment manually.

## Testing Your Setup

### Quick Test

```bash
# 1. Checkout examples branch
git checkout examples

# 2. Go to calculator example
cd calculator

# 3. Install dependencies
uv sync

# 4. Run tests
uv run pytest -v

# Expected output: All tests should pass ✅
```

If all tests pass, your setup is complete!

## Troubleshooting

### uv not found after installation

**Solution**: Restart your terminal or add uv to PATH manually.

```bash
# macOS/Linux - add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.cargo/bin:$PATH"

# Windows - add to PATH environment variable
%USERPROFILE%\.cargo\bin
```

### Python version not found

**Solution**: Ensure Python 3.11+ is installed and in PATH.

```bash
# Check available Python versions
python3 --version
python3.11 --version

# Use specific version with uv
uv python pin 3.11
```

### pytest command not found

**Solution**: Always use `uv run pytest` instead of `pytest` directly.

```bash
# ❌ Wrong
pytest

# ✅ Correct
uv run pytest
```

### Permission errors on macOS/Linux

**Solution**: Don't use `sudo` with uv. If you get permission errors:

```bash
# Fix ownership of .venv directory
chown -R $USER:$USER .venv
```

### Module not found errors

**Solution**: Make sure dependencies are installed.

```bash
# Re-sync dependencies
uv sync --reinstall
```

## Next Steps

1. Read the main [README.md](../README.md)
2. Checkout the `examples` branch to see complete code
3. Start [Workshop 1](../README.md#workshop-1-tdd-fundamentals--cicd-3-hours) by checking out `workshop-1` branch

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)