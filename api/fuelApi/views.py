from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.fuelApi.models import FuelPrice, StateCoords
from api.fuelApi.serializers import FuelPriceSerializer, StateCoordsSerializer

@api_view(['GET'])
def fuel_price_list(request):
    fuel_data = FuelPrice.objects.all()
    serializer = FuelPriceSerializer(fuel_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def path(request):
    pass

@api_view(['GET'])
def state_coords_list(request):
    state_coords = StateCoords.objects.all()
    serializer = StateCoordsSerializer(state_coords, many=True)
    return Response(serializer.data)