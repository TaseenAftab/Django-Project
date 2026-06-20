from typing import Optional

class Coordinates:
    def __init__(self, lat: float, long: float):
        if long > 0 and lat < 0 :
            long, lat = lat, long

        if not (24.0 <= lat <= 50.0):
            raise ValueError(f"Latitude {lat} is outside the US")
        if not (-125.0 <= long <= -66.0):
            raise ValueError(f"Longitude {long} is outside the US")
            
        self.lat = lat
        self.long = long 

    def get_coords(self) -> list[float]:
        return [self.long, self.lat]

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

class Car:
    def __init__(self, start_coords: Coordinates, distance):
        self.fuel_in_tank = 50 #in gallons
        self.consumption = 10 #miles per gallon
        self.cost = 0 #in USD
        self.coords = start_coords.get_coords()
        self.distance_to_cover = distance #in miles
        self.distance_covered = 0 #in miles
        self.__max_range = 500 #in miles
        self.__safe_fuel_reserve = 5 #in gallon


    @property
    def safe_fuel_reserve(self) -> float:
        return self.__safe_fuel_reserve

    @property
    def max_range(self) -> float:
        return self.__max_range