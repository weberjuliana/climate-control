from unittest.mock import MagicMock, patch

import pytest
import requests

from climatecontrol.src.entities.climate_models import OpenWeatherResponse
from climatecontrol.src.logic.climate_service import ClimateService, save_forecast_data

VALID_CITY = "Tokyo"
VALID_LAT = 35.6895
VALID_LON = 139.6917
INVALID_CITY = "X"
INVALID_LAT = -1000.0
INVALID_LON = -1000.0
API_KEY = "ff75b5f2772d73bb5b97fb1cc01e4a26"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

SAMPLE_WEATHER_DATA = {
    "cod": "200",
    "message": 0,
    "cnt": 7,
    "list": [
        {
            "dt": 1618317040,
            "main": {
                "temp": 31.1,
                "feels_like": 36.4,
                "temp_min": 30.0,
                "temp_max": 32.0,
                "pressure": 1012,
                "humidity": 80,
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clouds",
                    "description": "scattered clouds",
                    "icon": "01d",
                }
            ],
            "clouds": {"all": 10},
            "wind": {"speed": 5.0, "deg": 220},
            "sys": {"pod": "d"},
            "dt_txt": "2023-12-01 21:00:00",
        },
    ],
    "city": {
        "id": 123,
        "name": "Canoas",
        "coord": {"lat": 52.52, "lon": 13.405},
        "country": "DE",
        "population": 1000000,
        "timezone": 3600,
        "sunrise": 1618288262,
        "sunset": 1618334863,
    },
}


@pytest.mark.parametrize(
    "test_id, city, expected_result",
    [
        ("happy_path_valid_city", VALID_CITY, SAMPLE_WEATHER_DATA),
        ("edge_case_empty_city", "", None),
        ("error_case_invalid_city", INVALID_CITY, None),
    ],
)
@pytest.fixture
def open_weather_api():
    api = ClimateService()
    api.open_weather_maps_api_key = API_KEY
    api.open_weather_maps_forecast_url = FORECAST_URL
    return api


def test_network_failure(open_weather_api):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError

        result = open_weather_api.fetch_forecast_by_city(VALID_CITY)
        assert result is None

        result = open_weather_api.fetch_forecast_by_coordinates(VALID_LAT, VALID_LON)
        assert result is None


def test_response_validation(open_weather_api):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"invalid": "data"}
        mock_get.return_value = mock_response

        result = open_weather_api.fetch_forecast_by_city(VALID_CITY)
        assert result is None


# def test_process_weather_forecast_by_city(open_weather_api):
#     with patch("requests.get") as mock_get:
#         mock_response = MagicMock()
#         mock_response.json.return_value = SAMPLE_WEATHER_DATA
#         mock_get.return_value = mock_response

#         with patch("climatecontrol.src.repository.forecast_repository.save_forecast_data") as mock_save:
#             result = open_weather_api.fetch_forecast_by_city(VALID_CITY)
#             print(result)
#             assert result is not None
#             assert result["city"].name == "Canoas"
#             mock_save.assert_called_once()


@pytest.mark.parametrize(
    "test_id, city, expected_result",
    [
        ("happy_path_valid_city", VALID_CITY, SAMPLE_WEATHER_DATA),
        ("edge_case_empty_city", "", None),
        ("error_case_invalid_city", INVALID_CITY, None),
    ],
)
def test_fetch_forecast_by_city(test_id, city, expected_result, open_weather_api):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        if expected_result:
            mock_response.json.return_value = expected_result
            mock_response.raise_for_status = MagicMock()
        else:
            mock_response.raise_for_status.side_effect = (
                requests.exceptions.RequestException("Error")
            )
        mock_get.return_value = mock_response

        result = open_weather_api.fetch_forecast_by_city(city)
        print(f"Resultado do teste_fetch_forecast_by_city ({test_id}): {result}")

        if expected_result:
            result_converted = {
                "list": [forecast.model_dump() for forecast in result["list"]],
                "city": result["city"].model_dump(),
            }
            expected_result_converted = {
                "list": expected_result["list"],
                "city": expected_result["city"],
            }
            assert result_converted == expected_result_converted
        else:
            assert result is None


def test_save_forecast_data():
    with patch(
        "climatecontrol.src.repository.mongo_connection.MongoDB.get_database"
    ) as mock_get_database:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.weather_data = mock_collection
        mock_get_database.return_value = mock_db

        weather_data = OpenWeatherResponse(**SAMPLE_WEATHER_DATA)
        save_forecast_data(weather_data)

        mock_collection.insert_one.assert_called_once()
