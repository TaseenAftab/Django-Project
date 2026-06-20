from rest_framework import serializers
from api.fuelApi.models import FuelPrice, StateCoords

class FuelPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelPrice
        exclude = ['created_at','id']

class StateCoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateCoords
        exclude = ['id']

class RouteRequestSerializer(serializers.Serializer):
    start = serializers.ListField(
        child=serializers.FloatField(), min_length=2, max_length=2
    )
    end = serializers.ListField(
        child=serializers.FloatField(), min_length=2, max_length=2
    )

    def validate(self, data):
        start = data.get('start')
        end = data.get('end')
        
        from api.fuelApi.utils.path_utils import base_request
        
        try:
            base_request('direction', coordinates=[start, end], radiuses=[-1, -1])
        except ValueError as e:
            raise serializers.ValidationError({"routing_error": str(e)})
            
        return data