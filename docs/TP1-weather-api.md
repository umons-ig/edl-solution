# TP1: Weather API - TDD Fundamentals & CI/CD

**Duration**: 3 hours
**Branch**: `workshop-1`

## Learning Objectives

By the end of this workshop, you will be able to:
- Apply Test-Driven Development (TDD) principles
- Write unit tests with pytest
- Mock external API dependencies
- Build a REST API with FastAPI
- Set up GitHub Actions for continuous integration
- Handle errors and edge cases in tests

## Prerequisites

- Python 3.11+ installed
- uv installed ([see setup guide](setup-guide.md))
- Git basics
- Repository cloned locally

## Getting Started

```bash
# Switch to workshop-1 branch
git checkout workshop-1

# Install dependencies
uv sync

# Run tests (they will fail initially)
uv run pytest -v
```

---

## Part 1: Introduction & Calculator Demo (30 minutes)

### Setup (5 min)

Ensure your environment is ready:
```bash
uv --version
python --version
git status
```

### Calculator Demo (25 min)

See the calculator example to understand TDD basics:

```bash
# Checkout examples branch
git checkout examples
cd calculator/

# Install and run tests
uv sync
uv run pytest -v
```

**Instructor will demonstrate**:
1. Running a failing test (Red)
2. Writing code to pass the test (Green)
3. The TDD cycle

**Your task**: Explore the code and understand:
- How tests are structured
- How `pytest.raises` works
- How to run specific tests

📖 **Reference**: [Starting Example Guide](starting-example.md)

---

## Part 2: Weather API Project (120 minutes)

**Switch back to workshop branch:**
```bash
git checkout workshop-1
uv sync
```

### Overview

You will build a REST API that wraps the OpenWeatherMap API, providing:
- Current weather for any city
- Weather comparison between cities
- Proper error handling
- Caching (optional)

### Project Structure

```
workshop-1/
├── app.py                    # Your FastAPI application (incomplete)
├── test_weather_api.py       # Tests (will guide you)
├── pyproject.toml            # Dependencies
└── .github/workflows/        # CI configuration (to be created)
```

---

### Exercise 2A: Basic Weather Endpoint (30 minutes)

**Goal**: Create an endpoint that fetches weather from OpenWeatherMap

#### Step 1: Understand the Test (5 min)

Read the test in `test_weather_api.py`:

```python
def test_get_weather_success():
    with patch('app.requests.get') as mock_get:
        # Mock setup
        mock_response = Mock()
        mock_response.json.return_value = {
            'main': {'temp': 20},
            'weather': [{'description': 'clear sky'}],
            'name': 'Brussels'
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test
        response = client.get('/weather/Brussels')

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['city'] == 'Brussels'
        assert data['temperature'] == 20
        assert data['description'] == 'clear sky'
```

**Key concepts**:
- `patch()` - Replaces `requests.get` with a mock
- `Mock()` - Fake response object
- Why? We don't want to call the real API in tests

#### Step 2: Run the Test (Red) (2 min)

```bash
uv run pytest test_weather_api.py::test_get_weather_success -v
```

**Expected**: Test fails ❌ (endpoint doesn't exist)

#### Step 3: Implement the Endpoint (Green) (20 min)

Open `app.py` and implement the `/weather/{city}` endpoint:

**Hints**:
- Use FastAPI's `@app.get()` decorator
- Call OpenWeatherMap API with `requests.get()`
- Parse the JSON response
- Return formatted data

**API Details**:
- URL: `https://api.openweathermap.org/data/2.5/weather`
- Parameters: `q` (city), `appid` (API key), `units` (metric)
- You can use a demo key for testing (real calls will be mocked in tests)

#### Step 4: Verify Test Passes (3 min)

```bash
uv run pytest test_weather_api.py::test_get_weather_success -v
```

**Expected**: Test passes ✅

---

### ☕ Break (10 minutes)

---

### Exercise 2B: Error Handling (25 minutes)

**Goal**: Handle cases when the external API fails

#### Tests to Pass

```python
def test_get_weather_city_not_found():
    # Should return 404 when city doesn't exist
    ...

def test_get_weather_api_timeout():
    # Should return 503 when API times out
    ...

def test_get_weather_connection_error():
    # Should return 503 when connection fails
    ...
```

#### Your Tasks

1. **Read the tests** - Understand what they expect
2. **Run the tests** - See them fail
3. **Add error handling**:
   - Catch `requests.Timeout`
   - Catch `requests.ConnectionError`
   - Handle 404 responses from API
   - Return appropriate HTTP status codes
4. **Verify tests pass**

**Hints**:
- Use `try/except` blocks
- Use `response.raise_for_status()`
- Raise `HTTPException` from FastAPI
- Add `timeout` parameter to `requests.get()`

```bash
uv run pytest test_weather_api.py::test_get_weather_city_not_found -v
uv run pytest test_weather_api.py::test_get_weather_api_timeout -v
```

---

### Exercise 2C: Weather Comparison (30 minutes)

**Goal**: Compare weather between two cities

#### API Design

```
GET /weather/compare?city1=Brussels&city2=Paris
```

**Expected Response**:
```json
{
  "city1": {
    "name": "Brussels",
    "temperature": 15,
    "description": "rainy"
  },
  "city2": {
    "name": "Paris",
    "temperature": 20,
    "description": "sunny"
  },
  "temperature_difference": 5,
  "warmer_city": "Paris"
}
```

#### Your Tasks

1. **Read the test** in `test_weather_api.py::test_compare_weather`
2. **Understand the mock setup** - It returns different data for each city
3. **Implement the endpoint**:
   - Accept two query parameters
   - Fetch weather for both cities
   - Calculate temperature difference
   - Determine warmer city
4. **Run test and verify it passes**

**Bonus**: Refactor common code into a helper function

```bash
uv run pytest test_weather_api.py::test_compare_weather -v
```

---

### Exercise 2D: Caching (Optional - 25 minutes)

**Goal**: Cache weather data to reduce API calls

#### Why Cache?

- External APIs have rate limits
- Reduce latency
- Save costs
- Weather doesn't change every second

#### Your Tasks

1. **Read the caching test**
2. **Implement simple in-memory cache**:
   - Dictionary to store city → (data, timestamp)
   - Check cache before calling API
   - Cache results for 10 minutes
3. **Verify test passes**

**Hint**: Use a dictionary and `datetime` for timestamps

```bash
uv run pytest test_weather_api.py::test_weather_caching -v
```

---

### ☕ Break (10 minutes)

---

## Part 3: GitHub Actions CI/CD (30 minutes)

**Goal**: Automate testing with GitHub Actions

### Step 1: Create Workflow File (10 min)

Create `.github/workflows/test.yml`:

```yaml
name: Weather API Tests

on:
  push:
    branches: ['*']
  pull_request:
    branches: [main]

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
      run: uv run pytest -v --cov=app
```

### Step 2: Commit and Push (5 min)

```bash
git add .github/workflows/test.yml
git commit -m "Add GitHub Actions CI workflow"
git push origin workshop-1
```

### Step 3: View Results on GitHub (5 min)

1. Go to your repository on GitHub
2. Click **Actions** tab
3. See your workflow running
4. Explore the logs
5. Verify all tests pass ✅

### Step 4: Create a Pull Request (10 min)

```bash
# Create a new branch for a small change
git checkout -b add-documentation

# Make a small change (e.g., add a comment)
# Commit and push
git add .
git commit -m "Add documentation"
git push origin add-documentation

# Create PR
gh pr create --title "Add documentation" --body "Testing CI workflow"
```

**Observe**:
- GitHub Actions runs automatically
- PR shows check status
- Can't merge until checks pass (optional: enable branch protection)

---

## Part 4: Wrap-up & Review (10 minutes)

### What You Built

✅ Weather API with FastAPI
✅ Unit tests with mocking
✅ Error handling
✅ Weather comparison endpoint
✅ Optional: Caching
✅ CI/CD with GitHub Actions

### Key Concepts Learned

1. **Test-Driven Development**
   - Write tests first
   - Let tests guide implementation
   - Red → Green → Refactor

2. **Mocking**
   - Mock external dependencies
   - Control test behavior
   - Test in isolation

3. **API Testing**
   - Test status codes
   - Test response data
   - Test error cases

4. **Continuous Integration**
   - Automate testing
   - Catch bugs early
   - Maintain code quality

### Next Steps

**Homework (Optional)**:
1. Add 5-day forecast endpoint
2. Add temperature unit conversion (°F, °C, K)
3. Improve caching (use Redis)
4. Add more error handling
5. Deploy to a cloud platform

**Workshop 2 Preview**:
- URL Shortener with database
- Integration testing strategies
- Database testing patterns
- Advanced pytest features

---

## Troubleshooting

### Tests Failing?

```bash
# Run with verbose output
uv run pytest -vv

# Run specific test
uv run pytest test_weather_api.py::test_name -v

# Show print statements
uv run pytest -s
```

### Import Errors?

```bash
# Reinstall dependencies
uv sync --reinstall

# Check Python version
uv python list
```

### Mock Not Working?

- Check the patch path: `@patch('app.requests.get')` not `@patch('requests.get')`
- Ensure mock is configured before calling function
- Print mock calls: `print(mock_get.call_args_list)`

📖 **Full troubleshooting guide**: [troubleshooting.md](troubleshooting.md)

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenWeatherMap API Docs](https://openweathermap.org/api)

## Evaluation Criteria

- [ ] All tests pass locally
- [ ] GitHub Actions workflow passes
- [ ] Code is clean and readable
- [ ] Error handling is implemented
- [ ] Mocking is used correctly
- [ ] Comparison endpoint works
- [ ] (Optional) Caching implemented

---

**Questions? Ask your instructor or check the troubleshooting guide!**