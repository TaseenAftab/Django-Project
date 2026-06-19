import requests
from typing import Literal
import os
import dotenv

dotenv.load_dotenv()

RequestType = Literal['isochrone', 'direction']

API_KEY = os.getenv("ORS_API_KEY")
BASE_URL = "https://api.openrouteservice.org/v2"

def base_request(req_type: RequestType, profile: str = "driving-car", *args , **kwargs) -> dict | None:
    """
    Base Request for OpenRouteService
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

    body= {**kwargs}
    
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        response.raise_for_status()

        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"API Request failed for {req_type}: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None
