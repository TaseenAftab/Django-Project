from api.fuelApi.models import FuelPrice, StateCoords
from django.core.management.base import BaseCommand
import csv

class Command(BaseCommand):
    help = "Ingests fuel data from csv into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting fuel data ingestion...")

        with open('api/fuelApi/constants/fuel-prices-updated.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                
                FuelPrice.objects.get_or_create(
                    opis_truckstop_id=row['OPIS Truckstop ID'],
                    truckstop_name=row['Truckstop Name'].strip(),
                    address=row['Address'].strip(),
                    city=row['City'].strip(),
                    state=row['State'].strip(),
                    rack_id=row['Rack ID'],
                    retail_price=row['Retail Price'],
                    lat=row['Latitude'],
                    long=row['Longitude']
                )

        self.stdout.write(self.style.SUCCESS('Successfully ingested fuel data'))

        with open('api/fuelApi/constants/state-coords.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StateCoords.objects.get_or_create(
                    name=row['name'].strip(),
                    code=row['code'].strip(),
                    lat=row['latitude'],
                    long=row['longitude']
                )

        self.stdout.write(self.style.SUCCESS('Successfully ingested state coordinates'))
        