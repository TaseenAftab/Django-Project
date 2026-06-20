import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from api.fuelApi.services.location_service import station_locator
station_locator.load_from_database()

from api.fuelApi.services.path_service import find_path
from api.fuelApi.types.types import Coordinates


list = [[36.705289, -118.882689], [27.7567667,-81.4639835]]
coords = [ Coordinates(*item) for item in  list ]
find_path(start_coords=coords[0], end_coords=coords[1])