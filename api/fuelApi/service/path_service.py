from api.fuelApi.types import Coordinates, Path

def find_path(start_coords:Coordinates, end_coords:Coordinates) -> Path:
    path = Path(start_coords, end_coords)
    return path