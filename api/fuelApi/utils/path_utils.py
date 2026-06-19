import requests
from typing import Literal
import os
import dotenv

dotenv.load_dotenv()

RequestType = Literal['isochrone', 'direction']

# TODO: Replace with your actual OpenRouteService API Key
API_KEY = os.getenv("ORS_API_KEY")
BASE_URL = "https://api.openrouteservice.org/v2"

def base_request(req_type: RequestType, params: dict, profile: str = "driving-car") -> dict | None:
    """
    Hits the OpenRouteService endpoint (isochrone or direction) with the given parameters.
    Accepts both standard JSON and GeoJSON by default.
    Returns the parsed response as a dictionary, or None if the request fails.
    """
    if req_type == 'isochrone':
        endpoint = f"{BASE_URL}/isochrones/{profile}"
    elif req_type == 'direction':
        endpoint = f"{BASE_URL}/directions/{profile}/geojson"
    else:
        raise ValueError(f"Unsupported request type: {req_type}")
        
    headers = {
        'Accept': 'application/json, application/geo+json; charset=utf-8',
        'Authorization': API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    try:
        # OpenRouteService expects POST requests for JSON payloads
        response = requests.post(endpoint, json=params, headers=headers)
        
        # Raise an exception if the status code is 4xx or 5xx
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"API Request failed for {req_type}: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None
