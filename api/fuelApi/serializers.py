from rest_framework import serializers
from api.fuelApi.models import FuelPrice

class FuelPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelPrice
        exclude = ['created_at','id']