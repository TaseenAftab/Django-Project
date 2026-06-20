from django.contrib import admin
from .models import FuelPrice, StateCoords

@admin.register(FuelPrice)
class FuelPriceAdmin(admin.ModelAdmin):
    list_display = ('id','opis_truckstop_id', 'truckstop_name', 'address', 'city', 'state', 'rack_id', 'retail_price', 'lat', 'long')
    list_filter = ('state', 'city')
    search_fields = ('truckstop_name', 'address', 'city', 'state')
    ordering = ('state', 'city')
    

@admin.register(StateCoords)
class StateCoordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'lat', 'long')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name', 'code')
    
    