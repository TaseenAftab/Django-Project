import requests
import json

url = 'http://127.0.0.1:8000/api/route'
data = {
    "start": [36.705289, -118.882689],
    "end": [27.7567667,-81.4639835]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("API SUCCESS!")
    geojson = response.json()
    print(f"Returned GeoJSON type: {geojson.get('type')}")
    print(f"Number of Segments (Features): {len(geojson.get('features', []))}")
    
    with open('api_response.geojson', 'w') as f:
        json.dump(geojson, f, indent=2)
    print("Saved to api_response.geojson")
else:
    print("API FAILED!")
    print(response.status_code)
    print(response.text)
