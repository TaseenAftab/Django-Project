from api.fuelApi.service.path_service import find_path
from api.fuelApi.utils.path_utils import base_request
from api.fuelApi.types.types import Coordinates



list = [[36.7014631,-118.7559970], [27.7567667,-81.4639835]]
coords = [ Coordinates(*item) for item in  list ]
find_path(start_coords=coords[0], end_coords=coords[1])