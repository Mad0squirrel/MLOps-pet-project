"""Endpoints for prediction."""

from typing import Dict

from fastapi import APIRouter, Body, Request, status

from src.config import app_config
from src.exceptions import GeocodingError
from src.schemas.predict import BasePredictionIn, PredictionOut, PredictionWithAddressIn, PredictionWithCoordinatesIn
from src.utils.amenity import calculate_distances
from src.utils.feature_preparing import make_features_dataframe
from src.utils.geoapify import (
    Coordinates,
    FetchException,
    IncorrectQueryException,
    NoResultsException,
    NoTokenException,
    get_coordinates_by_address,
)

router = APIRouter(tags=['ml'])

@router.post("/predict_with_address", response_model=PredictionOut)
async def predict_with_address(request: Request, data: PredictionWithAddressIn = Body()) -> PredictionOut:
    """Prediction with address.
    
    Parameters
    ----------
     request: Request
     data: user data
    
    Returns
    -------
     prediction result: PredictionOut
    
    """
    coords = await get_coordinates_with_handling_errors(data.address, app_config.GEOAPIFY_TOKEN)
    prediction = prepare_and_predict(request, data, coords.lat, coords.lon)
    return PredictionOut(value=prediction)


@router.post("/predict_with_coordinates", response_model=PredictionOut)
async def predict_with_coordinates(request: Request, data: PredictionWithCoordinatesIn = Body()) -> PredictionOut:
    """Predict with coordinates.
    
    Parameters
    ----------
     request: Request
     data: coordinates data
    
    Returns
    -------
     prediction result: PredictionOut
    
    """
    prediction = prepare_and_predict(request, data, data.lat, data.lon)
    return PredictionOut(value=prediction)


def prepare_and_predict(request: Request, data: BasePredictionIn, lat: float, lon: float) -> float:
    """Prepare features and make prediction.
    
    Parameters
    ----------
     request: Request
     data: user data
     lat: latitude
     lon: longitude
    
    Returns
    -------
     prediction result: float
    
    """  
    distance_data = calculate_distances(lat, lon, request.app.state.amenities_data)
    df = make_features_dataframe(data, lat, lon, distance_data)
    values: list[float] = request.app.state.model.predict(df)
    return values[0]


async def get_coordinates_with_handling_errors(address: str, token: str) -> Coordinates:
    """Get coordinates and handle errors.
    
    Parameters
    ----------
     address: str
     token: str
    
    Returns
    -------
     coordinates: Coordinates
    
    """
    try:
        coords = await get_coordinates_by_address(address, token)
    except (NoResultsException, IncorrectQueryException) as ex:
        raise GeocodingError(message="Пожалуйста уточните адрес", status=status.HTTP_404_NOT_FOUND) from ex
    except NoTokenException:
        raise GeocodingError(
            message="Токен доступа к geoapify не предоставлен", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from NoTokenException
    except FetchException:
        raise GeocodingError(
            message="Возникла ошибка при обращении к geoapify", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from FetchException
    return coords