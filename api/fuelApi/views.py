from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.fuelApi.models import FuelPrice, StateCoords
from api.fuelApi.serializers import FuelPriceSerializer, StateCoordsSerializer
from api.fuelApi.serializers import FuelPriceSerializer, StateCoordsSerializer, RouteRequestSerializer
from api.fuelApi.types.types import Coordinates
from api.fuelApi.services.path_service import find_path, generate_segmented_geojson
from api.fuelApi.services.location_service import station_locator

@api_view(['GET'])
def fuel_price_list(request):
    fuel_data = FuelPrice.objects.all()
    serializer = FuelPriceSerializer(fuel_data, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def route(request):
    serializer = RouteRequestSerializer(data=request.data)
    if serializer.is_valid():
        start_data = serializer.validated_data['start']
        end_data = serializer.validated_data['end']
        
        start_coords = Coordinates(lat=start_data[0], long=start_data[1])
        end_coords = Coordinates(lat=end_data[0], long=end_data[1])
        
        if not station_locator.is_ready:
            station_locator.load_from_database()
            
        try:
            path_obj = find_path(start_coords, end_coords)
        except ValueError as e:
            return Response({"routing_error": str(e)}, status=400)
            
        feature_collection = generate_segmented_geojson(path_obj)
        
        response_data = {
            "geojson": feature_collection,
            "total_fuel_cost": round(path_obj.total_cost, 2),
            "stops": path_obj.stations_info
        }
        
        return Response(response_data)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def state_coords_list(request):
    state_coords = StateCoords.objects.all()
    serializer = StateCoordsSerializer(state_coords, many=True)
    return Response(serializer.data)