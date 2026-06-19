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