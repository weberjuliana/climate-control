import logging

from climatecontrol.src.repository.mongo_connection import MongoDB
from climatecontrol.src.entities.api_entities import WeatherForecastResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_forecast_data(weather_data: WeatherForecastResponse):
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        weather_data_dict = weather_data.model_dump(by_alias=True, exclude_none=True)
        weather_collection.insert_one(weather_data_dict)
        logger.info("Successfull saving!")

    except Exception as e:
        logger.error("Error ocurred while saving on database", exc_info=e)
        raise
