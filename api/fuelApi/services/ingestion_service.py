import time
from api.fuelApi.constants.state_codes import STATE_CODES
import requests
import urllib.parse
import requests
from api.fuelApi.constants.state_codes import STATE_CODES

def get_coords_of_station(chunk):
    """
    Takes a list of rows (chunk) and hits the TomTom Batch Search API.
    Returns a list of (lat, lon) tuples corresponding to each row.
    """
    api_key = "A9wdrcTAEmItoldDqTuXZQznv6sMy6uy"
    batch_url = f"https://api.tomtom.com/search/2/batch/sync.json?key={api_key}"
    
    batch_items = []
    
    for row in chunk:
        name = row['Truckstop Name'].replace("/", " ").split('#')[0].strip()
        address = row['Address'].replace("&", "and").replace("/", " ").split('#')[0].strip()
        city = row['City']
        state_code = row['State']
        full_state_name = STATE_CODES.get(state_code.upper(), state_code)
        
        final_query = f"{name.strip()}, {address.strip()}, {city.strip()}, {full_state_name.strip()}, USA"
        encoded_query = urllib.parse.quote(final_query)
        
        query_url = f"/search/{encoded_query}.json?limit=1"
        batch_items.append({"query": query_url})
        
    payload = {"batchItems": batch_items}
    
    try:
        response = requests.post(batch_url, json=payload)
        coords = []
        
        if response.status_code == 200:
            data = response.json()
            responses = data.get('batchItems', [])
            
            for item in responses:
                lat, lon = 0.0, 0.0
                if item.get('statusCode') == 200:
                    results = item.get('response', {}).get('results', [])
                    if results:
                        pos = results[0]['position']
                        lat, lon = pos['lat'], pos['lon']
                coords.append((lat, lon))
        else:
            coords = [(0.0, 0.0) for _ in chunk]
            print(f"Batch failed: {response.status_code}")
            
        return coords
    except Exception as e:
        print(f"Error calling batch API: {e}")
        return [(0.0, 0.0) for _ in chunk]

def get_coords_of_state(state_code):

    full_state_name = STATE_CODES.get(state_code.upper(), state_code)
    query = urllib.parse.quote(f"{full_state_name}, USA")
    url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&polygon_geojson=1'
    
    headers = {
        'User-Agent': 'FuelTrackerApp/1.0'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]

            else:
                print(f"No results found for state: {full_state_name}")
                return None

            time.sleep(1)
        else:
            print(f"Failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching coordinates for state {state_code}: {e}")
        return None
