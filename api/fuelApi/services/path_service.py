from api.fuelApi.types.types import Coordinates, Path, Car
from api.fuelApi.utils.path_utils import base_request, get_coords_by_distance
from shapely.geometry import Point, LineString, shape
from math import ceil



def find_path(start_coords: Coordinates, end_coords: Coordinates) -> Path:
    path = Path(start_coords, end_coords)

    #Get distance
    coords = [start_coords.get_coords(), end_coords.get_coords()]
    data = base_request('direction', coordinates=coords, radiuses=[-1] * len(coords))
    
    distance = data['features'][0]['properties']['summary']['distance']*0.000621371
    route_geometry = shape(data['features'][0]['geometry'])
    route_length = route_geometry.length * 0.000621371

    car = Car(start_coords, distance)  
    refills_made = 0

    while car.distance_covered < car.distance_to_cover:
        usable_fuel = car.fuel_in_tank - car.safe_fuel_reserve
        distance_can_cover = usable_fuel * car.consumption
        remaining_distance = car.distance_to_cover - car.distance_covered

        if remaining_distance <= distance_can_cover:
            car.distance_covered += remaining_distance
            car.fuel_in_tank -= remaining_distance / car.consumption
            print(f"Reached the destination, Total covered: {car.distance_covered:.2f}/{car.distance_to_cover:.2f} miles. Fuel left: {car.fuel_in_tank:.2f} gal")
            break
        else:
            car.distance_covered += distance_can_cover
            car.fuel_in_tank -= distance_can_cover / car.consumption
            current_coords = get_coords_by_distance(car.distance_covered, route_length, route_geometry)

            print(f'current_coords: {current_coords}')
            print(f"Drove {distance_can_cover:.2f} miles. Total covered: {car.distance_covered:.2f}/{car.distance_to_cover:.2f} miles. Hit safe reserve ({car.fuel_in_tank:.2f} gal)! Refilling tank to 50 gal...")

            car.fuel_in_tank = 50
            refills_made += 1

    print(f"\n--- Trip Summary ---")
    print(f"Total distance: {car.distance_covered:.4f} miles")
    print(f"Total refills made: {refills_made}")
    print(f"Final fuel remaining: {car.fuel_in_tank:.2f} gallons")

    return path