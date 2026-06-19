from api.fuelApi.types.types import Coordinates, Path, Car
from api.fuelApi.utils.path_utils import base_request, haversine_distance
from shapely.geometry import Point, LineString
from math import ceil

import math



def find_path(start_coords: Coordinates, end_coords: Coordinates) -> Path:
    path = Path(start_coords, end_coords)

    car = Car()
    max_range = car.safe_max

    #Get distance
    coords = [start_coords.get_coords(), end_coords.get_coords()]
    distance_res = base_request(req_type='direction', coordinates=coords, radiuses=[-1] * len(coords))
    
    if not distance_res:
        print("Warning: Could not find a drivable road. Falling back to straight-line 'as the crow flies' distance.")
        distance = haversine_distance(coords[0], coords[1])
    else:
        distance = distance_res['features'][0]['properties']['summary']['distance']*0.000621371

    #Calculate refills needed
    refills_needed = ceil(distance / (max_range - 50)) - 1
    car.fuel_in_tank = car.fuel_in_tank - (distance / car.consumption)    

    print(f"Distance is equal to {distance:.4f} miles")
    print("this distance can be covered with {:.0f} refills".format(refills_needed))
    print(f"Fuel remaining: {car.fuel_in_tank:.2f} gallons")
    print(car.safe_max)

    return path