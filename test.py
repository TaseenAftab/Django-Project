from api.fuelApi.utils.path_utils import base_request
from api.fuelApi.types.types import Coordinates

coords : list[Coordinates] = [Coordinates(8.681495,49.41461),Coordinates(8.686507,49.41943),Coordinates(8.687872,49.420318)]
print(base_request(req_type='direction', profile='driving-car', coordinates=[c.get_coords() for c in coords] ))