"""
Test suite for Weather API

These tests guide your implementation. Make them pass one by one!

How to run:
    uv run pytest test_weather_api.py -v
    uv run pytest test_weather_api.py::test_get_weather_success -v  # Run specific test
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import requests

from app import app

client = TestClient(app)


class TestBasicEndpoint:
    """Test the basic root endpoint (already implemented)"""

    def test_root_endpoint(self):
        """✅ This test should pass - it's an example"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'message' in response.json()


class TestWeatherEndpoint:
    """Exercise 2A: Basic weather endpoint"""

    def test_get_weather_success(self):
        """
        Test successful weather fetch

        Your task: Implement GET /weather/{city} to make this pass
        Hint: Mock the external API call to avoid real network requests
        """
        with patch('app.requests.get') as mock_get:
            # Setup mock response (Open-Meteo format)
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'current': {
                    'temperature_2m': 20,
                    'time': '2025-09-30T10:00'
                },
                'current_units': {
                    'temperature_2m': '°C'
                }
            }
            mock_get.return_value = mock_response

            # Call our API
            response = client.get('/weather/Brussels')

            # Assertions
            assert response.status_code == 200, "Expected 200 OK"

            data = response.json()
            assert 'city' in data, "Response should include 'city'"
            assert 'temperature' in data, "Response should include 'temperature'"

            assert data['city'] == 'Brussels'
            assert data['temperature'] == 20


class TestErrorHandling:
    """Exercise 2B: Error handling"""

    def test_get_weather_city_not_found(self):
        """
        Test 404 error when city doesn't exist

        Your task: Check if city exists in CITY_COORDINATES
        Hint: If city not found, raise HTTPException(status_code=404, detail="City not found")
        """
        # No mock needed - city won't be in CITY_COORDINATES
        response = client.get('/weather/InvalidCityName')

        assert response.status_code == 404, "Should return 404 for invalid city"
        assert 'detail' in response.json()

    def test_get_weather_api_timeout(self):
        """
        Test timeout handling

        Your task: Catch requests.Timeout exception
        Hint: Use try/except and raise HTTPException(status_code=503)
        """
        with patch('app.requests.get') as mock_get:
            mock_get.side_effect = requests.Timeout()

            response = client.get('/weather/Brussels')

            assert response.status_code == 503, "Should return 503 on timeout"
            assert 'detail' in response.json()

    def test_get_weather_connection_error(self):
        """
        Test connection error handling

        Your task: Catch requests.ConnectionError exception
        """
        with patch('app.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError()

            response = client.get('/weather/Brussels')

            assert response.status_code == 503, "Should return 503 on connection error"
            assert 'detail' in response.json()


class TestWeatherComparison:
    """Exercise 2C: Weather comparison endpoint"""

    def test_compare_weather(self):
        """
        Test comparing weather between two cities

        Your task: Implement GET /weather/compare?city1=X&city2=Y
        Hint: Mock should return different data based on city parameter
        """
        with patch('app.requests.get') as mock_get:
            def mock_api_response(url, params=None, timeout=None):
                """Return different data based on coordinates (Open-Meteo format)"""
                mock_response = Mock()
                mock_response.status_code = 200

                # Brussels coordinates: 50.8503, 4.3517
                if params and params.get('latitude') == 50.8503:
                    mock_response.json.return_value = {
                        'current': {
                            'temperature_2m': 15,
                            'time': '2025-09-30T10:00'
                        }
                    }
                # Paris coordinates: 48.8566, 2.3522
                elif params and params.get('latitude') == 48.8566:
                    mock_response.json.return_value = {
                        'current': {
                            'temperature_2m': 20,
                            'time': '2025-09-30T10:00'
                        }
                    }

                return mock_response

            mock_get.side_effect = mock_api_response

            # Call comparison endpoint
            response = client.get('/weather/compare?city1=Brussels&city2=Paris')

            assert response.status_code == 200, "Expected 200 OK"

            data = response.json()

            # Check structure
            assert 'city1' in data
            assert 'city2' in data
            assert 'temperature_difference' in data
            assert 'warmer_city' in data

            # Check data
            assert data['city1']['name'] == 'Brussels'
            assert data['city1']['temperature'] == 15

            assert data['city2']['name'] == 'Paris'
            assert data['city2']['temperature'] == 20

            assert data['temperature_difference'] == 5
            assert data['warmer_city'] == 'Paris'


class TestCaching:
    """Exercise 2D (Optional): Caching"""

    def test_weather_caching(self):
        """
        Test that weather data is cached

        Your task: Implement caching to avoid multiple API calls for same city
        Hint: Store data in dictionary with timestamp, check age before calling API
        """
        with patch('app.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'current': {
                    'temperature_2m': 20,
                    'time': '2025-09-30T10:00'
                }
            }
            mock_get.return_value = mock_response

            # First call
            response1 = client.get('/weather/Brussels')
            assert response1.status_code == 200

            # Second call (should use cache)
            response2 = client.get('/weather/Brussels')
            assert response2.status_code == 200

            # Verify API was only called once (cache hit on second call)
            assert mock_get.call_count == 1, "API should only be called once due to caching"