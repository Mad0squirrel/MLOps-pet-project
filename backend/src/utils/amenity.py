"""Module for working with amenities."""

import json
import os
from math import asin, cos, pi, sin, sqrt
from typing import Dict, List

DISTANCES = [500, 1500, 3000]


def calculate_distances(lat: float, lon: float, amenities: List[Dict[str, float | str]]) -> Dict[str, int]:
    """Calculate distances from point to all amenities.
    
    Parameters
    ----------
     lat: float
     lon: float
     amenities: List[Dict[str, float | str]]
    
    Returns
    -------
     distances: Dict[str, int]
    
    """
    distance_data: Dict[str, int] = dict()
    for amenity_item in amenities:
        calculated_distance = get_distance(lon, lat, float(amenity_item['lon']), float(amenity_item['lat']))
        for distance in DISTANCES:
            key: str = str(amenity_item['type']) + '_' + str(distance)
            distance_data[key] = distance_data.get(key, 0)
            if calculated_distance < distance:
                distance_data[key] += 1
    return distance_data


def get_distance(llong1: float, llat1: float, llong2: float, llat2: float) -> float:
    """Calculate distance.
    
    Parameters
    ----------
     llong1: float
     llat1: float
     llon2: float
     llat2: float
    
    Returns
    -------
     distance in meters: float
    
    """
    rad = 6372795
    lat1 = llat1 * pi / 180.0
    lat2 = llat2 * pi / 180.0
    long1 = llong1 * pi / 180.0
    long2 = llong2 * pi / 180.0
    delta_long = long2 - long1
    delta_lat = lat2 - lat1
    ad = 2 * asin(sqrt(sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2))
    dist = ad * rad
    return dist


def load_amenities_data(dir_path: str) -> List[Dict[str, float]]:
    """Load amenities.
    
    Parameters
    ----------
     dir_path: str
    
    Returns
    -------
     dict with amenities: List[Dict[str, float]]
    
    """
    amenities = []
    for root, _, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            name, _ = os.path.splitext(filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                amenitiy_data = json.load(f)
            for item in amenitiy_data:
                amenitiy_item = dict(lon=item['lon'], lat=item['lat'], type=name)
                amenities.append(amenitiy_item)
    return amenities