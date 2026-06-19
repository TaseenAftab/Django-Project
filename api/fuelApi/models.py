from django.db import models

class FuelPrice(models.Model):
    opis_truckstop_id = models.IntegerField(help_text="OPIS Truckstop Identification Number")
    truckstop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    rack_id = models.IntegerField(help_text="Rack ID")
    retail_price = models.DecimalField(max_digits=12, decimal_places=8, help_text="Retail Price")
    created_at = models.DateTimeField(auto_now_add=True)
    long = models.DecimalField(max_digits=12, decimal_places=8, help_text="Longitude")
    lat = models.DecimalField(max_digits=12, decimal_places=8, help_text="Latitude")

    def __str__(self):
        return f"{self.truckstop_name} ({self.city}, {self.state}) - ${self.retail_price}"

