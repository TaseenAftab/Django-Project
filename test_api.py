import requests
import json

url = 'http://127.0.0.1:8000/api/'
data = {
    "start": [36.705289, -118.882689],
    "end": [27.7567667,-81.4639835]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("API SUCCESS!")
    data = response.json()
    
    actual_geojson = data.get('geojson', {})
    
    print(f"Number of Segments (Features): {len(actual_geojson.get('features', []))}")
    print(f"Total Fuel Cost: ${data.get('total_fuel_cost')}")
    print(f"Number of Stops: {len(data.get('stops', []))}")
    
    with open('api_response.geojson', 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved to api_response.geojson")
else:
    print("API FAILED!")
    print(response.status_code)
    print(response.text)
