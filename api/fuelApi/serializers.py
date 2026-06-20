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