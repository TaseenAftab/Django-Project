from typing import Optional

class Coordinates:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long 

    def get_coords(self) -> list[float]:
        return [self.lat, self.long]

class Path:
    def __init__(self, start_coords: Coordinates, end_coords: Coordinates, station_coords: Optional[Coordinates] = None):
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.station_coords = station_coords

    def get_path(self):
        coords = [self.start_coords.get_coords()]
        coords.append(self.end_coords.get_coords())
        coords.append(self.station_coords.get_coords()) if self.station_coords else None
        
        return coords