from api.fuelApi.types.types import Coordinates, Path, Car
from api.fuelApi.utils.path_utils import base_request, get_coords_by_distance, get_search_corridor
from shapely.geometry import shape, Point
import math
import heapq
from api.fuelApi.models import FuelPrice
from api.fuelApi.services.location_service import station_locator


def find_path(start_coords: Coordinates, end_coords: Coordinates) -> Path:
    path = Path(start_coords, end_coords)

    #Get distance
    coords = [start_coords.get_coords(), end_coords.get_coords()]
    data = base_request('direction', coordinates=coords, radiuses=[-1] * len(coords))
    
    distance = data['features'][0]['properties']['summary']['distance']*0.000621371
    route_geometry = shape(data['features'][0]['geometry'])

    car = Car(start_coords, distance)  
    
    entire_corridor = get_search_corridor(0, distance, route_geometry, distance)
    route_stations = station_locator.get_stations_in_polygon(entire_corridor)

    valid_stations = []
    for station in route_stations:
        stat_lon, stat_lat = station['coordinates']
        pt = Point(stat_lon, stat_lat)

        proj_norm = route_geometry.project(pt, normalized=True)
        station['proj_dist'] = proj_norm * distance
        valid_stations.append(station)
        
    valid_stations.sort(key=lambda x: x['proj_dist'])
    
    nodes = [{'id': 'start', 'proj_dist': 0.0}] + valid_stations + [{'id': 'end', 'proj_dist': distance}]
    
    abs_max_range = car.fuel_in_tank * car.consumption
    safe_max_range = (car.fuel_in_tank - car.safe_fuel_reserve) * car.consumption 
    
    min_tanks = math.ceil(distance / safe_max_range)
    total_tanks = min_tanks + 1
    ideal_spacing = distance / total_tanks
    
    n = len(nodes)
    min_cost = {0: 0.0}
    previous = {0: None}
    pq = [(0.0, 0)]
    
    while pq:
        cost, u = heapq.heappop(pq)
        
        if u == n - 1:
            break
            
        if cost > min_cost.get(u, float('inf')):

            continue
            
        for v in range(u + 1, n):
            dist_uv = nodes[v]['proj_dist'] - nodes[u]['proj_dist']
            
            if dist_uv > abs_max_range:
                break
            
            if dist_uv <= 0:
                continue
                
            edge_cost = abs(dist_uv - ideal_spacing) ** 2
            
            if dist_uv > safe_max_range:
                edge_cost += 1000000 + (dist_uv - safe_max_range) ** 2
                
            new_cost = cost + edge_cost
            
            if new_cost < min_cost.get(v, float('inf')):
                min_cost[v] = new_cost
                previous[v] = u
                heapq.heappush(pq, (new_cost, v))
                
    if n - 1 not in previous:
        print(f"ERROR: Cannot find a path! The gas desert is greater than {abs_max_range} miles.")
        return path
        
    path_indices = []
    curr = n - 1
    while curr is not None:
        path_indices.append(curr)
        curr = previous.get(curr)
        
    path_indices.reverse()
    
    refills_made = 0
    current_fuel = car.fuel_in_tank
    car.distance_covered = 0.0
    
    print(f"Total distance: {distance:.2f} miles")
    print(f"Ideal spacing calculated: {ideal_spacing:.2f} miles ({total_tanks} legs)")
    
    for i in range(1, len(path_indices)):
        u = path_indices[i-1]
        v = path_indices[i]
        leg_distance = nodes[v]['proj_dist'] - nodes[u]['proj_dist']
        
        fuel_consumed = leg_distance / car.consumption
        current_fuel -= fuel_consumed
        car.distance_covered += leg_distance
        
        if v == n - 1:
            print(f"Reached destination! Leg: {leg_distance:.2f} mi. Total covered: {car.distance_covered:.2f}/{distance:.2f} miles. Fuel left: {current_fuel:.2f} gal")
        else:
            station = nodes[v]
            stat_lon, stat_lat = station['coordinates']
            
            from api.fuelApi.models import FuelPrice
            db_station = FuelPrice.objects.get(id=station.get('database_id'))
            retail_price = float(db_station.retail_price)
            
            path.add_station(Coordinates(stat_lat, stat_lon), info={
                "name": db_station.truckstop_name,
                "address": db_station.address,
                "city": db_station.city,
                "state": db_station.state,
                "retail_price": retail_price,
                "coordinates": [float(stat_lon), float(stat_lat)]
            })
            
            refill_amount = 50.0 - current_fuel
            cost_for_stop = refill_amount * retail_price
            path.total_cost += cost_for_stop
            
            print(f"Stop {refills_made + 1} at Station {db_station.truckstop_name} ({db_station.city}, {db_station.state})")
            print(f"Drove {leg_distance:.2f} miles. Arrived with {current_fuel:.2f} gal.")
            print(f"Refilled {refill_amount:.2f} gal @ ${retail_price:.2f}/gal = ${cost_for_stop:.2f}")
            
            current_fuel = 50.0
            refills_made += 1
            
    print(f"\n--- Trip Summary ---")
    print(f"Total distance: {distance:.4f} miles")
    print(f"Total refills made: {refills_made}")
    print(f"Final fuel remaining: {current_fuel:.2f} gallons")
    print(f"Total fuel cost: ${path.total_cost:.2f}")

    return path