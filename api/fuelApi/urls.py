from django.urls import path
from api.fuelApi.views import fuel_price_list, state_coords_list, route

urlpatterns = [
    path('', route, name='route'),
    path('stations', fuel_price_list, name='fuel-price-list'),
    path('states', state_coords_list, name='state-coords-list')
]
