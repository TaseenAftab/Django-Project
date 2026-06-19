class Coordinates:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long 

    def get_coords(self) -> list[float]:
        return [self.lat, self.long]

class Path:
    def __init__(self, start_coords:Coordinates, end_coords:Coordinates):
        self.start_coords = start_coords
        self.end_coords = end_coords

    def get_path(self):
        return [self.start_coords, self.end_coords]