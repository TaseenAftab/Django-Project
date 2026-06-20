from scipy.spatial import cKDTree
from api.fuelApi.types.types import Coordinates
from shapely.geometry import Point
from api.fuelApi.models import FuelPrice

class NearestStationService:
    def __init__(self):
        self.station_ids = []  
        self.coordinates = []
        self.spatial_tree = None
        self.is_ready = False

    def load_from_database(self):


        stations = FuelPrice.objects.values_list('id', 'lat', 'long')
        self.station_ids = []
        self.coordinates = []

        for station_id, lon, lat in stations:
            self.station_ids.append(station_id)
            self.coordinates.append([lat, lon])

        if self.coordinates:
            self.spatial_tree = cKDTree(self.coordinates)
            self.is_ready = True

    def find_nearest_station(self, coord: Coordinates, search_polygon=None) -> dict:
        if not self.is_ready:
            raise RuntimeError("Spatial index has not been initialized.")

        current_lon , current_lat = coord.get_coords()
        query_point = [current_lon, current_lat]

        # Query 100 nearest to ensure we have enough candidates that might fall inside the bounding box
        distances, indices = self.spatial_tree.query(query_point, k=100)

        unique_candidates = []
        seen_coordinates = set()

        for i, tree_index in enumerate(indices):
            coord_tuple = tuple(self.coordinates[tree_index])

            if coord_tuple not in seen_coordinates:
                if search_polygon:

                    if not Point(coord_tuple).within(search_polygon):
                        continue

                seen_coordinates.add(coord_tuple)
            
                unique_candidates.append({
                    "database_id": self.station_ids[tree_index],
                    "coordinates": self.coordinates[tree_index],
                    "distance_degrees": distances[i]
                })

            if len(unique_candidates) == 1:
                break
        
        return unique_candidates

    def get_stations_in_polygon(self, polygon) -> list:
        if not self.is_ready:
            raise RuntimeError("Spatial index has not been initialized.")
            

        minx, miny, maxx, maxy = polygon.bounds
        
        valid_stations = []
        for i, coord in enumerate(self.coordinates):
            lon, lat = coord
            if minx <= lon <= maxx and miny <= lat <= maxy:
                if Point(lon, lat).within(polygon):
                    valid_stations.append({
                        "database_id": self.station_ids[i],
                        "coordinates": coord
                    })
        return valid_stations
    
station_locator = NearestStationService()
