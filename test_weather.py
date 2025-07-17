from unittest.mock import patch

import pytest

from weather import fetch_weather


@pytest.fixture
def sample_api_response():
    return {
        "cod": 200,
        "main": {"temp": 22, "humidity": 60},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 3.5},
    }


@patch("weather.requests.get")
# The goal is to verify that the fetch_weather correctly patses successful response
def test_fetch_weather_success(mock_get, sample_api_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = sample_api_response
    mock_get.return_value.raise_for_status = lambda: None

    data, err = fetch_weather("London")
    assert err is None
    assert data["temperature"] == 22
    assert data["weather_description"] == "clear sky"
