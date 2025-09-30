# Calculator Example - Complete TDD Demo

This is a **complete, working example** demonstrating Test-Driven Development principles.

## Purpose

This example shows:
- ✅ How tests guide implementation
- ✅ Testing exceptions with `pytest.raises`
- ✅ Parameterized tests
- ✅ Error handling
- ✅ All tests passing

## Running the Example

```bash
# Install dependencies (from root directory)
uv sync

# Run all tests
uv run pytest calculator/test_calculator.py -v

# Run specific test
uv run pytest calculator/test_calculator.py::TestDivision::test_divide_by_zero -v

# Run the demo
uv run python calculator/calculator.py
```

## What to Learn

### 1. Basic Assertions
```python
def test_add():
    assert add(2, 3) == 5
```

### 2. Testing Exceptions
```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

### 3. Parameterized Tests
```python
@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (5, 120),
])
def test_factorial(n, expected):
    assert factorial(n) == expected
```

## Files

- `calculator/calculator.py` - Implementation (all functions working)
- `calculator/test_calculator.py` - Complete test suite
- `pyproject.toml` - Dependencies (at root level)

## Next Steps

After understanding this example:
1. Go back to main branch: `git checkout main`
2. Start Workshop 1: `git checkout workshop-1`
3. Apply these TDD principles to the Weather API project