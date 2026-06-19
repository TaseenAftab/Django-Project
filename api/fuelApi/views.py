from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.fuelApi.models import FuelPrice
from api.fuelApi.serializers import FuelPriceSerializer

@api_view(['GET'])
def fuel_price_list(request):
    fuel_data = FuelPrice.objects.all()
    serializer = FuelPriceSerializer(fuel_data, many=True)
    return Response(serializer.data)
