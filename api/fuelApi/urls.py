from django.urls import path
from api.fuelApi.views import fuel_price_list, state_coords_list

urlpatterns = [
    path('', fuel_price_list, name='fuel-price-list'),
    path('state', state_coords_list, name='state-coords-list')
]
