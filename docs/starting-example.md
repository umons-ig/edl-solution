# Starting Example: Calculator with TDD

This document explains the calculator example used to introduce Test-Driven Development concepts.

## Purpose

The calculator example is a **quick demonstration** (30 minutes) to show:
- How pytest works
- The TDD cycle (Red → Green → Refactor)
- Writing tests before code
- How tests guide implementation

After this demo, students will work on the main workshop project (Weather API).

## Where to Find It

The complete calculator example is in the `examples` branch:

```bash
git checkout examples
cd calculator/
uv sync
uv run pytest -v
```

## The TDD Cycle

### 🔴 Red: Write a Failing Test

```python
# test_calculator.py
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

Run the test:
```bash
uv run pytest test_calculator.py::test_divide_by_zero -v
```

**Result**: Test fails ❌ (ZeroDivisionError not raised)

### 🟢 Green: Write Minimal Code to Pass

```python
# calculator.py
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

Run the test again:
```bash
uv run pytest test_calculator.py::test_divide_by_zero -v
```

**Result**: Test passes ✅

### 🔵 Refactor: Improve Code Quality

In this simple case, the code is already clean. For more complex scenarios:
- Extract duplicate logic
- Improve naming
- Add comments if needed
- **Keep tests green**

### 🔁 Repeat

Continue with the next test!

## Example Functions in Calculator

### 1. Division with Zero Check

**Function**: `divide(a, b)`

**Test**:
```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

**Teaching Points**:
- Exception handling
- Testing exceptions with `pytest.raises`
- Error messages matter

---

### 2. Power with Negative Exponents

**Function**: `power(base, exponent)`

**Test**:
```python
def test_power_negative_exponent():
    assert power(2, -1) == 0.5
    assert power(4, -2) == 0.0625
```

**Teaching Points**:
- Recursion
- Edge cases (negative inputs)
- Mathematical operations

**Implementation**:
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

### 3. Factorial with Validation

**Function**: `factorial(n)`

**Tests**:
```python
@pytest.mark.parametrize("n, expected", [
    (0, 1),      # Special case: 0! = 1
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

**Teaching Points**:
- Parameterized tests (multiple test cases in one)
- Input validation
- Special cases (0! = 1)

---

### 4. Average of Empty List

**Function**: `average(numbers)`

**Test**:
```python
def test_average_empty_list():
    with pytest.raises(ValueError, match="empty list"):
        average([])
```

**Teaching Points**:
- Empty collection handling
- Validation before computation
- Descriptive error messages

**Implementation**:
```python
def average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

## Workshop Flow

### Phase 1: Instructor Demo (15 minutes)

1. **Show the failing test** (Red)
   ```bash
   uv run pytest test_calculator.py::test_divide_by_zero -v
   ```

2. **Live code the fix** (Green)
   - Add the `if b == 0:` check
   - Raise the exception
   - Show test passing

3. **Explain the process**
   - Test tells you what to build
   - Test confirms it works
   - Repeat for all features

### Phase 2: Students Explore (15 minutes)

Students checkout the `examples` branch and:
- Run all calculator tests
- Read the code
- Understand the patterns
- Ask questions

```bash
git checkout examples
cd calculator/
uv sync
uv run pytest -v
```

### Phase 3: Transition to Main Project (5 minutes)

- "Now you understand the basics"
- "Let's apply this to a real project: Weather API"
- "You'll write tests and code to make them pass"

```bash
git checkout workshop-1
uv sync
uv run pytest
# See failing tests → time to work!
```

## Key Takeaways

After this example, students should understand:

1. ✅ **TDD Cycle**: Red → Green → Refactor
2. ✅ **pytest basics**:
   - `assert` statements
   - `pytest.raises` for exceptions
   - `@pytest.mark.parametrize` for multiple cases
3. ✅ **Running tests**: `uv run pytest -v`
4. ✅ **Reading test output**: What failed, why, and how to fix it
5. ✅ **Tests as documentation**: Tests show how code should behave

## Common Questions

### Q: Why write tests first?
**A**: Tests define what "done" means. They guide implementation and prevent over-engineering.

### Q: Isn't this slower?
**A**: Initially yes, but you save time debugging and gain confidence in changes.

### Q: Do I test everything?
**A**: Test behavior, not implementation. Focus on edge cases and critical paths.

### Q: What if requirements change?
**A**: Update tests first, then code. Tests adapt with requirements.

## Next Steps

After completing the calculator demo:
1. Students should checkout `workshop-1` branch
2. Read the workshop README
3. Start building the Weather API
4. Apply TDD principles learned here

---

**Time allocation**: 30 minutes total
- Demo: 15 min
- Students explore: 15 min
- Questions throughout