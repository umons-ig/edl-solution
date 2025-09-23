# Calculator Workshop - PyTest Demo

A workshop project demonstrating Test-Driven Development with pytest and git workflow.

## Quick Start

```bash
# Run tests (simplest command)
pytest

# Run calculator demo
python calculator.py

# Commit and push to trigger automatic tests
git add .
git commit -m "Fix calculator functions"
git push
```

## Project Structure

```text
calculator.py          # Calculator functions (some have bugs to fix!)
test_calculator.py     # Test cases for workshop
```

## Workshop Tasks

1. Fix `divide()` - handle division by zero
2. Fix `power()` - support negative exponents  
3. Implement `factorial()` function
4. Fix `average()` - handle empty lists
5. Push to GitHub and see tests run automatically! ✅

## GitHub Actions

The repository includes automated testing that runs on every push. Check the "Actions" tab on GitHub to see test results.

## Installation

### Install uv

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv

# With conda
conda install -c conda-forge uv

# With homebrew (macOS)
brew install uv
```