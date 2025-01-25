"""Module for interaction with Geoapify."""

from dataclasses import dataclass
from typing import Any, Dict

import aiohttp

URL = "https://api.geoapify.com/v1/geocode/search"

class NoTokenException(Exception):
    """Exception if no token."""

    pass


class FetchException(Exception):
    """Exception if error in fetch."""

    pass


class IncorrectQueryException(Exception):
    """Exception if error in request."""

    pass


class NoResultsException(Exception):
    """Exception if not results."""

    pass


@dataclass
class Coordinates:
    """Dataclass for coordinates."""
    
    lon: float
    lat: float


def build_params(address: str, token: str) -> Dict[str, str]:
    """Build query params.
    
    Parameters
    ----------
     address: str
     token: str
    
    Returns
    -------
     query params: Dict[str, str]
    
    """
    if not token:
        raise NoTokenException()
    return {
        'text': address,
        'lang': 'en',
        'filter': "circle:37.62354,55.75197,40000",
        'format': 'json',
        'apiKey': token,
    }
    

async def send_request(url: str, params: Dict[str, str]) -> Dict[str, Any]:
    """Get nearest by address points.
    
    Parameters
    ----------
     url: str
     params: Dict[str, str]
    
    Returns
    -------
     data: Dict[str, Any]
    
    """
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url, params=params)
            if response.status != 200:
                raise IncorrectQueryException()
            data: Dict[str, Any] = await response.json(encoding='UTF-8')
            return data
    except aiohttp.ClientError:
        raise FetchException() from aiohttp.ClientError
    
    
async def get_coordinates_by_address(address: str, token: str) -> Coordinates:
    """Get coordinates by address.
    
    Parameters
    ----------
     address: str
     token: str
    
    Returns
    -------
     coordinates: Coordinates
     
    """
    params = build_params(address, token)
    response_data = await send_request(URL, params)
    for item in response_data['results']:
        if item['rank']['match_type'] == 'full_match':
            return Coordinates(lat=item['lat'], lon=item['lon'])
    raise NoResultsException()