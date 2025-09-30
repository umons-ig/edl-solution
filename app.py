from fastapi import FastAPI

app = FastAPI(title="Weather API", version="1.0.0")

WEATHER_API_BASE_URL = 'https://api.open-meteo.com/v1/forecast'

CITY_COORDINATES = {
    'Brussels': {'latitude': 50.8503, 'longitude': 4.3517},
    'Paris': {'latitude': 48.8566, 'longitude': 2.3522},
    'London': {'latitude': 51.5074, 'longitude': -0.1278},
    'Berlin': {'latitude': 52.52, 'longitude': 13.41},
}

@app.get("/")
def root():
    """
    Root endpoint - already implemented as an example

    Returns API information and available endpoints.

    To see interactive API documentation, visit:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    """
    return {
        "message": "Weather API Workshop",
        "version": "1.0.0",
        "description": "Learn TDD by building a weather API",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "GET /": "This endpoint (API info)",
            "GET /weather/{city}": "Get weather for a city (TODO: implement)",
            "GET /weather/compare": "Compare weather between two cities (TODO: implement)",
            "GET /cities": "List available cities"
        },
        "available_cities": list(CITY_COORDINATES.keys())
    }


@app.get("/cities")
def list_cities():
    """
    List all available cities

    This endpoint is already implemented to help students test their code.
    """
    return {
        "cities": list(CITY_COORDINATES.keys()),
        "count": len(CITY_COORDINATES)
    }


# TODO: Exercise 2A - Implement the weather endpoint
# @app.get('/weather/{city}')
# def get_weather(city: str):
#     """
#     Get current weather for a city
#
#     Args:
#         city: Name of the city
#
#     Returns:
#         dict: Weather data with city, temperature, and description
#
#     Raises:
#         HTTPException: 404 if city not found, 503 if service unavailable
#     """
#     # TODO: Implement this endpoint
#     # Hints:
#     # 1. Get coordinates from CITY_COORDINATES (or raise 404 if not found)
#     # 2. Call Open-Meteo API: requests.get(WEATHER_API_BASE_URL, params={...})
#     #    params: latitude, longitude, current='temperature_2m,weather_code'
#     # 3. Handle errors (404 for unknown city, 503 for timeouts/connection errors)
#     # 4. Parse response and return: {city, temperature, description}
#     # 5. Use try/except to catch requests exceptions
#     pass


# TODO: Exercise 2C - Implement the comparison endpoint
# @app.get('/weather/compare')
# def compare_weather(city1: str, city2: str):
#     """
#     Compare weather between two cities
#
#     Args:
#         city1: First city name
#         city2: Second city name
#
#     Returns:
#         dict: Weather data for both cities plus comparison
#     """
#     # TODO: Implement this endpoint
#     # Hints:
#     # 1. Get weather for both cities (reuse code or create helper function)
#     # 2. Calculate temperature difference
#     # 3. Determine which city is warmer
#     pass