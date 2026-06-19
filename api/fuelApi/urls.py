from django.urls import path
from api.fuelApi.views import fuel_price_list

urlpatterns = [
    path('', fuel_price_list, name='fuel-price-list'),
]
