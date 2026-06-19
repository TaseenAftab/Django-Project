from api.fuelApi.service.ingestion_service import get_coords_of_station
from api.fuelApi.constants.state_codes import STATE_CODES
import csv

def main():
    with open('api/fuelApi/constants/fuel-prices.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            c = get_coords_of_station(
                row['Truckstop Name'], 
                row['Address'], 
                row['City'], 
                row['State']
            )
            print(c)


if __name__ == "__main__":
    main()