from unittest.mock import patch
from datetime import datetime


# testing Flask app behavior, not the API or DB internals
def test_post_index_success(client):
    with patch("app.fetch_weather") as mock_fetch, patch("app.save_query") as mock_save:
        mock_fetch.return_value = (
            {
                "temperature": 20,
                "weather_description": "sunny",
                "humidity": 50,
                "wind_speed": 3,
            },
            None,
        )
        response = client.post("/", data={"city": "London"}, follow_redirects=True)
        assert b"Weather for London" in response.data
        mock_save.assert_called_once()


def test_post_index_empty_city(client):
    response = client.post("/", data={"city": ""}, follow_redirects=True)
    assert b"City name cannot be empty" in response.data


def test_post_index_api_error(client):
    with patch("app.fetch_weather") as mock_fetch:
        mock_fetch.return_value = (None, "API error")
        response = client.post("/", data={"city": "UnknownCity"}, follow_redirects=True)
        assert b"Could not retrieve weather data:" in response.data


def test_history_route(client):
    with patch("app.get_query_history") as mock_history:
        mock_history.return_value = [
            ("London", 20, "sunny", 50, 3, datetime(2025, 7, 17, 0, 0))
        ]
        response = client.get("/history")
        assert b"London" in response.data
