# Workshop 1: Weather API - TDD Fundamentals & CI/CD

**Duration**: 3 hours
**Goal**: Learn Test-Driven Development by building a Weather API

## 🎯 What You'll Build

A REST API that wraps the Open-Meteo weather API with:
- ✅ Current weather endpoint
- ✅ Weather comparison between cities
- ✅ Error handling
- ✅ Caching (optional)
- ✅ Automated testing with GitHub Actions

## 🚀 Quick Start

```bash
# Install dependencies
uv sync

# Run tests (they will fail - your job is to make them pass!)
uv run pytest -v

# Run the API (once implemented)
uv run uvicorn app:app --reload
```

**Note**: No API key needed! Uses Open-Meteo (free, no signup). All tests use mocks anyway.

## 📚 Workshop Structure

### Part 1: Calculator Demo (30 min)
Quick introduction to TDD with a simple calculator example.

**Check out the examples:**
```bash
git checkout examples
uv sync
uv run pytest calculator/test_calculator.py -v
git checkout workshop-1  # Come back when done
```

### Part 2: Weather API Exercises (120 min)

#### Exercise 2A: Basic Weather Endpoint (30 min)
**Goal**: Implement `GET /weather/{city}`

**Test to pass**: `test_get_weather_success`

**What to do**:
1. Read the test in `test_weather_api.py`
2. Run `uv run pytest test_weather_api.py::test_get_weather_success -v` (see it fail)
3. Implement the endpoint in `app.py`
4. Make the test pass ✅

#### Exercise 2B: Error Handling (25 min)
**Goal**: Handle API failures gracefully

**Tests to pass**:
- `test_get_weather_city_not_found` - Return 404 for invalid cities
- `test_get_weather_api_timeout` - Return 503 when API times out
- `test_get_weather_connection_error` - Handle connection errors

#### Exercise 2C: Weather Comparison (30 min)
**Goal**: Implement `GET /weather/compare?city1=X&city2=Y`

**Test to pass**: `test_compare_weather`

Compare weather between two cities and calculate the temperature difference.

#### Exercise 2D: Caching (Optional - 25 min)
**Goal**: Cache results to reduce API calls

**Test to pass**: `test_weather_caching`

Implement simple in-memory caching with a 10-minute TTL.

### Part 3: GitHub Actions CI/CD (30 min)

**Goal**: Automate testing with GitHub Actions

**Guide**: Follow [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) for step-by-step instructions

**Tasks**:
1. Create `.github/workflows/test.yml`
2. Add workflow configuration (see guide for template)
3. Commit and push to GitHub
4. Verify CI runs and passes on GitHub Actions tab

## 📖 Detailed Instructions

See [docs/TP1-weather-api.md](docs/TP1-weather-api.md) for:
- Step-by-step instructions
- Code examples
- Tips and hints
- Troubleshooting

## 🧪 Running Tests

```bash
# Run all tests
uv run pytest -v

# Run specific test
uv run pytest test_weather_api.py::test_get_weather_success -v

# Run with coverage
uv run pytest --cov=app -v

# Show print statements
uv run pytest -s
```

## 🏃 Running the API

### Terminal 1: Start the Server

```bash
uv run uvicorn app:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!** The server will auto-reload when you change code.

---

### Open in Browser

Now open these URLs:

- 🏠 **Main API**: http://localhost:8000/
- 📚 **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- 📖 **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

**The Swagger UI (`/docs`) is the best way to test your API!**

---

### Terminal 2: Test with curl (Optional)

Open a **second terminal** and test:

```bash
# List available cities (works immediately)
curl http://localhost:8000/cities

# Test weather endpoint (404 until you implement it)
curl http://localhost:8000/weather/Brussels

# Test comparison (404 until you implement it)
curl "http://localhost:8000/weather/compare?city1=Brussels&city2=Paris"
```

---

### Using Swagger UI (Recommended!)

1. Go to http://localhost:8000/docs
2. See all endpoints listed
3. Click `GET /cities` → "Try it out" → "Execute"
4. See the response with available cities ✅
5. Try `GET /weather/{city}` (will show 404 until implemented)
6. As you implement endpoints, refresh and test them!

## 📝 Files in This Branch

- `app.py` - Your FastAPI application (⚠️ incomplete - you'll implement this)
- `test_weather_api.py` - Test suite (✅ complete - guides your implementation)
- `pyproject.toml` - Dependencies
- `GITHUB_ACTIONS_GUIDE.md` - Step-by-step CI/CD setup guide
- `.env.example` - Environment variables template
- `README.md` - This file
- `docs/` - Detailed guides and references

## 🎓 Learning Objectives

By the end of this workshop, you will:
- ✅ Understand the TDD cycle (Red → Green → Refactor)
- ✅ Write unit tests with pytest
- ✅ Mock external dependencies
- ✅ Build REST APIs with FastAPI
- ✅ Handle errors properly
- ✅ Set up CI/CD with GitHub Actions

## 💡 Tips

- **Read the tests first** - They tell you what to build
- **Make one test pass at a time** - Don't try to do everything at once
- **Run tests frequently** - See your progress
- **Ask for help** - Instructors are here to guide you
- **Reference the examples** - `git checkout examples` to see working code

## 🆘 Need Help?

- **Test failing?** Run with `-vv` for more details: `uv run pytest -vv`
- **Import error?** Make sure you ran `uv sync`
- **Mock not working?** Check the patch path matches your import
- **Stuck?** See [docs/troubleshooting.md](docs/troubleshooting.md)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [Open-Meteo API](https://open-meteo.com/)

---

**Ready to start?**

```bash
uv sync
uv run pytest -v
# See the failing tests → time to code!
```

**Good luck! 🚀**