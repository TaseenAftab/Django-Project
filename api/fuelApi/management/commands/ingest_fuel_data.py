from api.fuelApi.models import FuelPrice
from django.core.management.base import BaseCommand
import csv

class Command(BaseCommand):
    help = "Ingests fuel data from csv into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting fuel data ingestion...")

        with open('api/fuelApi/constants/fuel-prices.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                
                FuelPrice.objects.get_or_create(
                    opis_truckstop_id=row['OPIS Truckstop ID'],
                    truckstop_name=row['Truckstop Name'],
                    address=row['Address'],
                    city=row['City'],
                    state=row['State'],
                    rack_id=row['Rack ID'],
                    retail_price=row['Retail Price']
                )

        self.stdout.write(self.style.SUCCESS('Successfully ingested fuel data'))
        