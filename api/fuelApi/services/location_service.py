from scipy.spatial import cKDTree
from api.fuelApi.types.types import Coordinates

class NearestStationService:
    def __init__(self):
        self.station_ids = []  
        self.coordinates = []
        self.spatial_tree = None
        self.is_ready = False

    def load_from_database(self):
        from api.fuelApi.models import FuelPrice

        stations = FuelPrice.objects.values_list('id', 'lat', 'long')
        self.station_ids = []
        self.coordinates = []

        for station_id, lon, lat in stations:
            self.station_ids.append(station_id)
            self.coordinates.append([lat, lon])

        if self.coordinates:
            self.spatial_tree = cKDTree(self.coordinates)
            self.is_ready = True

    def find_nearest_station(self, coord: Coordinates) -> dict:
        if not self.is_ready:
            raise RuntimeError("Spatial index has not been initialized.")

        current_lon , current_lat = coord.get_coords()
        query_point = [current_lon, current_lat]

        distances, indices = self.spatial_tree.query(query_point, k=30)

        unique_candidates = []
        seen_coordinates = set()

        for i, index in enumerate(indices):
            pass

station_locator = NearestStationService()
