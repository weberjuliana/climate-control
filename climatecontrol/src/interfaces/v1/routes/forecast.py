from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from climatecontrol.src.entities.api_entities import (
    SimpleForecast,
    SimpleWeatherCondition,
    WeatherForecastResponse,
)
from climatecontrol.src.interfaces.v1.authentication.token_bearer import JWTBearer
from climatecontrol.src.logic.climate_service import ClimateService
from climatecontrol.src.repository.mongo_connection import MongoDB

router = APIRouter()
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_weather_service() -> ClimateService:
    return ClimateService()


@router.get(
    "/forecast",
    response_model=WeatherForecastResponse,
    dependencies=[Depends(JWTBearer())],
)
def weather_forecast(
    city: Optional[str] = None,
    lat: Optional[float] = Query(None, description="Lat"),
    lon: Optional[float] = Query(None, description="Long"),
    weather_service: ClimateService = Depends(get_weather_service),
):
    if city and (lat is not None or lon is not None):
        raise HTTPException(
            status_code=400,
            detail="Provide either city name or both latitude and longitude, but not both.",
        )

    if city:
        forecast_data = weather_service.fetch_forecast_by_city(city)

    elif lat is not None and lon is not None:
        forecast_data = weather_service.fetch_forecast_by_coordinates(lat, lon)

    else:
        raise HTTPException(
            status_code=400,
            detail="Either city name or both latitude and longitude must be provided.",
        )

    if forecast_data is None or "list" not in forecast_data:
        raise HTTPException(
            status_code=500, detail="Error fetching data from OpenWeatherMaps"
        )

    forecasts = []
    for forecast in forecast_data["list"]:
        print(type(forecast))
        conditions = [
            SimpleWeatherCondition(main=cond.main, description=cond.description)
            for cond in forecast.weather
        ]
        simple_forecast = SimpleForecast(
            date=forecast.dt_txt,
            temperature=forecast.main.temp,
            feels_like=forecast.main.feels_like,
            conditions=conditions,
        )
        forecasts.append(simple_forecast)

    city_name = forecast_data["city"].name if forecast_data["city"] else "Unknown"
    return WeatherForecastResponse(
        city_name=city_name,
        forecasts=forecasts,
    )


def convert_objectid_to_str(data):
    if isinstance(data, list):
        logger.info(f"Converting list: {data}")
        return [convert_objectid_to_str(item) for item in data]
    if isinstance(data, dict):
        converted_dict = {
            k: convert_objectid_to_str(v) if k == "_id" else v for k, v in data.items()
        }
        logger.info(f"Converting dict: {converted_dict}")
        return converted_dict
    if isinstance(data, ObjectId):
        logger.info(f"Converting ObjectId: {str(data)}")
        return str(data)
    return data


@router.get(
    "/all", response_model=WeatherForecastResponse, dependencies=[Depends(JWTBearer())]
)
def get_all_weather_data():
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data

        weather_data = list(weather_collection.find({}))

        weather_data_converted = convert_objectid_to_str(weather_data)

        forecasts = []
        for forecast in weather_data_converted:
            for data in forecast.get("list", []):
                conditions = [
                    SimpleWeatherCondition(
                        main=cond["main"], description=cond["description"]
                    )
                    for cond in data.get("weather", [])
                ]
                simple_forecast = SimpleForecast(
                    date=data.get("dt_txt", "Unknown"),
                    temperature=data["main"].get("temp", 0),
                    feels_like=data["main"].get("feels_like", 0),
                    conditions=conditions,
                )
                forecasts.append(simple_forecast)

        return WeatherForecastResponse(
            city_name=weather_data_converted[0].get("city", {}).get("name", "Unknown")
            if weather_data_converted
            else "Unknown",
            forecasts=forecasts,
        )
    except Exception as e:
        logger.error(f"Error occurred while fetching data from the database: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/by-id/{document_id}",
    response_model=WeatherForecastResponse,
    dependencies=[Depends(JWTBearer())],
)
def get_weather_data_by_id(document_id: str):
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        document = weather_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        document = convert_objectid_to_str(document)

        forecasts = []
        for data in document["list"]:
            conditions = [
                SimpleWeatherCondition(
                    main=cond["main"], description=cond["description"]
                )
                for cond in data["weather"]
            ]
            forecast = SimpleForecast(
                date=data["dt_txt"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                conditions=conditions,
            )
            forecasts.append(forecast)

        return WeatherForecastResponse(
            city_name=document["city"]["name"], forecasts=forecasts
        )
    except Exception as e:
        logger.error("Error occurred while fetching data from the database", exc_info=e)
        raise HTTPException(status_code=500, detail="Error fetching data from db")


@router.delete("/delete-all", dependencies=[Depends(JWTBearer())])
def delete_all_weather_data():
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data

        deletion_result = weather_collection.delete_many({})
        return {"message": f"Deleted documents: {deletion_result.deleted_count}"}
    except Exception as e:
        logger.error("Error occurred while deleting data from the database", exc_info=e)
        raise HTTPException(status_code=500, detail="Error deleting data")


@router.delete("/delete-by-id/{document_id}", dependencies=[Depends(JWTBearer())])
def delete_weather_data_by_id(document_id: str):
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data

        deletion_result = weather_collection.delete_one({"_id": ObjectId(document_id)})
        if deletion_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Document not found or deleted")
        return {"message": "Document deleted successfull"}
    except Exception as e:
        logger.error("Error occurred while deleting data from the database", exc_info=e)
        raise HTTPException(status_code=500, detail="Error deleting data")
