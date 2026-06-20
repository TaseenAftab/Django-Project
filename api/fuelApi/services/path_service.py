from api.fuelApi.types.types import Coordinates, Path, Car
from api.fuelApi.utils.path_utils import base_request, get_coords_by_distance, get_search_corridor
from shapely.geometry import shape
from api.fuelApi.services.location_service import station_locator


def find_path(start_coords: Coordinates, end_coords: Coordinates) -> Path:
    path = Path(start_coords, end_coords)

    #Get distance
    coords = [start_coords.get_coords(), end_coords.get_coords()]
    data = base_request('direction', coordinates=coords, radiuses=[-1] * len(coords))
    
    distance = data['features'][0]['properties']['summary']['distance']*0.000621371
    route_geometry = shape(data['features'][0]['geometry'])

    car = Car(start_coords, distance)  
    refills_made = 0
    
    entire_corridor = get_search_corridor(0, car.distance_to_cover, route_geometry, car.distance_to_cover)
    route_stations = station_locator.get_stations_in_polygon(entire_corridor)

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
            current_coords = get_coords_by_distance(car.distance_covered, car.distance_to_cover, route_geometry)
            
            corridor_polygon = get_search_corridor(car.distance_covered, car.distance_to_cover, route_geometry, 50.0)
            
            # Use the pre-filtered stations instead of the entire KDTree
            from shapely.geometry import Point
            from api.fuelApi.utils.path_utils import haversine_distance
            
            best_station = None
            min_dist = float('inf')
            fallback_station = None
            fallback_min_dist = float('inf')
            
            current_lon, current_lat = current_coords.get_coords()
            current_proj_norm = car.distance_covered / car.distance_to_cover
            
            for station in route_stations:
                stat_lon, stat_lat = station['coordinates']
                station_point = Point(stat_lon, stat_lat)
                
                # Ensure the station is in the 50-mile lookahead polygon
                if station_point.within(corridor_polygon):
                    dist = haversine_distance([current_lon, current_lat], [stat_lon, stat_lat])
                    
                    # Keep track of the absolute closest station as a fallback
                    if dist < fallback_min_dist:
                        fallback_min_dist = dist
                        fallback_station = station
                    
                    # Prevent U-turns by ensuring the station is mathematically AHEAD of us on the route
                    # We subtract a tiny bit (0.0001) to allow for stations exactly adjacent to us
                    station_proj_norm = route_geometry.project(station_point, normalized=True)
                    if station_proj_norm < current_proj_norm - 0.0001:
                        continue
                        
                    if dist < min_dist:
                        min_dist = dist
                        best_station = station
            
            # If there are literally 0 gas stations ahead of us, fallback to the one behind us
            if not best_station:
                best_station = fallback_station
            
            # Format as a list to match previous output style
            station_coords = [best_station] if best_station else []

            print(station_coords)

            print(f'current_coords: {current_coords.get_coords()}')
            print(f"Drove {distance_can_cover:.2f} miles. Total covered: {car.distance_covered:.2f}/{car.distance_to_cover:.2f} miles. Hit safe reserve ({car.fuel_in_tank:.2f} gal)! Refilling tank to 50 gal...")

            car.fuel_in_tank = 50
            refills_made += 1

    print(f"\n--- Trip Summary ---")
    print(f"Total distance: {car.distance_covered:.4f} miles")
    print(f"Total refills made: {refills_made}")
    print(f"Final fuel remaining: {car.fuel_in_tank:.2f} gallons")

    return path