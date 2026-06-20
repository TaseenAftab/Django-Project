import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from api.fuelApi.services.location_service import station_locator
from api.fuelApi.utils.path_utils import base_request
station_locator.load_from_database()

from api.fuelApi.services.path_service import find_path
from api.fuelApi.types.types import Coordinates


list = [[36.705289, -118.882689], [27.7567667,-81.4639835]]
coords = [ Coordinates(*item) for item in  list ]
path = find_path(start_coords=coords[0], end_coords=coords[1])
all_coords = path.get_path()

# Fetch the final geojson connecting all points
data = base_request('direction', coordinates=all_coords, radiuses=[-1] * len(all_coords))

# Print a tiny summary so the terminal doesn't get flooded with millions of coordinates
print(f"\nSuccessfully retrieved GeoJSON!")
print(f"Total Waypoints Connected: {len(all_coords)}")
print(f"GeoJSON Type: {data['type']}")

import json
with open('route.geojson', 'w') as f:
    json.dump(data, f, indent=2)
print("Saved full GeoJSON to route.geojson!")