import logging
from typing import Dict, List, Optional

import requests

from climatecontrol.src.config.settings import settings
from climatecontrol.src.entities.climate_models import OpenWeatherResponse
from climatecontrol.src.repository.forecast_repository import save_forecast_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimateService:
    def __init__(self) -> None:
        self.forecast_url = settings.OPEN_WEATHER_MAPS_FORECAST_URL
        self.api_key: str = settings.OPEN_WEATHER_API_KEY

    def fetch_forecast_by_city(self, city: str) -> Optional[List[Dict]]:
        try:
            logger.info(f"Retrieving weather forecast for city: {city}")
            params: Dict = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
            }

            return self._request_climate_api(params)
        except Exception as e:
            logger.error(f"Failed to retrieve weather forecast for city: {e}")
            return None

    def fetch_forecast_by_coordinates(
        self, lat: float, lon: float
    ) -> Optional[List[Dict]]:
        try:
            params: Dict = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
            }
            return self._request_climate_api(params)
        except Exception as e:
            logger.error(f"Failed to retrieve weather forecast by coordinates: {e}")
            return None

    def _request_climate_api(self, params: Dict) -> Optional[Dict]:
        try:
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            data = response.json()
            forecast_data = OpenWeatherResponse(**data)

            logger.info(f"Processed weather forecast data: {forecast_data}")

            # Saving the data to the database
            logger.info("Saving weather forecast data")
            save_forecast_data(forecast_data)
            logger.info("Weather forecast data successfully saved")

            return {"list": forecast_data.list, "city": forecast_data.city}
        except requests.RequestException as e:
            logger.error(f"Error in OpenWeather API request: {e}")
            return None
