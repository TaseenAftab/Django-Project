import requests
from typing import Literal
import os
import dotenv
import math
from shapely.geometry import LineString
from api.fuelApi.types.types import Coordinates

dotenv.load_dotenv()

RequestType = Literal['matrix', 'direction']

# Leaving this here so that this can be tested
API_KEY = os.getenv("ORS_API_KEY") or 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImQ1MzczMzJkMTIxNDQ2OTM4NGYzZDA4MjIzYmRiMDE0IiwiaCI6Im11cm11cjY0In0='
BASE_URL = "https://api.openrouteservice.org/v2"

def base_request(req_type: RequestType, profile: str = "driving-car", *args , **kwargs) -> dict | None:
    """
    Base Request for OpenRouteService
    """
    if req_type == 'matrix':
        endpoint = f"{BASE_URL}/matrix/{profile}"
    elif req_type == 'direction':
        endpoint = f"{BASE_URL}/directions/{profile}/geojson"
    else:
        raise ValueError(f"Unsupported request type: {req_type}")
        
    headers = {
        'Accept': 'application/json, application/geo+json; charset=utf-8',
        'Authorization': API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }

    body= {**kwargs}
    
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        response.raise_for_status()

        return response.json()
        
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            try:
                error_data = e.response.json()
            except Exception:
                error_data = {}
                
            if 'error' in error_data and 'message' in error_data['error']:
                err_msg = error_data['error']['message']
                raise ValueError(err_msg)
            
            if error_data.get('error', {}).get('code') == 2010:
                raise ValueError("The road is finished or point is too far from a valid road.")
        
        raise ValueError("Failed to connect to the routing service.")

def haversine_distance(coord1: list[float], coord2: list[float]) -> float:
    R = 3958.8 # Earth radius in miles
    lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
    lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_coords_by_distance(distance_covered, total_distance, route_line):

    target_point = route_line.interpolate(
        distance_covered/total_distance,
        normalized=True
    )

    longitude = target_point.x
    latitude = target_point.y
    return Coordinates(latitude, longitude)


def get_search_corridor(distance_covered, total_distance, route_line, lookahead_miles):
    points = []
    
    step = 5.0
    d = 0.0
    while d <= lookahead_miles:
        eval_dist = distance_covered + d
        if eval_dist > total_distance:
            eval_dist = total_distance
            
        target_point = route_line.interpolate(
            eval_dist / total_distance, 
            normalized=True
        )
        
        points.append((target_point.x, target_point.y))
        
        if eval_dist == total_distance:
            break
        d += step
        
    upcoming_segment = LineString(points)
    return upcoming_segment.buffer(0.075)