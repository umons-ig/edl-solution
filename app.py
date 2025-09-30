"""
Weather API - FastAPI Application

Your task: Implement the endpoints to make the tests pass!

This is a TDD exercise - read the tests in test_weather_api.py to understand
what each endpoint should do, then implement the functionality here.
"""

from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI(title="Weather API", version="1.0.0")

# Open-Meteo API configuration (No API key needed!)
# Open-Meteo is a free, open-source weather API
# Docs: https://open-meteo.com/
WEATHER_API_BASE_URL = 'https://api.open-meteo.com/v1/forecast'

# City coordinates (simplified - in real app, use geocoding)
CITY_COORDINATES = {
    'Brussels': {'latitude': 50.8503, 'longitude': 4.3517},
    'Paris': {'latitude': 48.8566, 'longitude': 2.3522},
    'London': {'latitude': 51.5074, 'longitude': -0.1278},
    'Berlin': {'latitude': 52.52, 'longitude': 13.41},
}


@app.get("/")
def root():
    """Root endpoint - already implemented as an example"""
    return {
        "message": "Weather API",
        "version": "1.0.0",
        "endpoints": [
            "GET /weather/{city}",
            "GET /weather/compare?city1=X&city2=Y"
        ]
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


# TODO: Exercise 2D (Optional) - Add caching
# You may want to create a simple cache using a dictionary
# Example:
# cache = {}  # Store: {city: (data, timestamp)}
# CACHE_TTL = 600  # 10 minutes
#
# def get_cached_weather(city):
#     # Check if data exists and is not expired
#     pass
#
# def cache_weather(city, data):
#     # Store weather data with timestamp
#     pass