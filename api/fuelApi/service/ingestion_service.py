import time
from api.fuelApi.constants.state_codes import STATE_CODES
import requests


import urllib.parse

def get_coords_of_station(name: str, address: str, city: str, state_code: str):
    clean_query = address.replace("&", "and")
    full_state_name = STATE_CODES.get(state_code.upper(), state_code)
    
    # Use the name, address, city, and state. 
    final_query = f"{name}, {clean_query}, {city}, {full_state_name}, USA"
    
    encoded_query = urllib.parse.quote(final_query)
    
    api_key = "aSFl8tNk0D7yW3FJuoc0SRXCm89qlwXm"
    
    # Change endpoint from /geocode/ to /search/ (Fuzzy Search)
    url = f"https://api.tomtom.com/search/2/search/{encoded_query}.json"
    
    params = {
        'key': api_key,
        'limit': 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # TomTom allows up to 5 requests per second, so we can lower the sleep
    time.sleep(1)
    
    if 'results' in data and len(data['results']) > 0:
        lat = data['results'][0]['position']['lat']
        lon = data['results'][0]['position']['lon']
        return [lat, lon]
    
    return [0.0, 0.0]