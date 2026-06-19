import csv
import time
import requests
import urllib.parse
from django.core.management.base import BaseCommand
from api.fuelApi.service.ingestion_service import get_coords_of_station

class Command(BaseCommand):
    help = "Generates a CSV with statecode, latitude, and longitude using TomTom Batch Search API."

    def handle(self, *args, **kwargs):
        input_file = 'api/fuelApi/constants/fuel-prices.csv'
        output_file = 'api/fuelApi/constants/station-locations.csv'
        failed_file = 'api/fuelApi/constants/failed-stations.csv'
        
        self.stdout.write(f"Reading from {input_file} and writing to {output_file}...")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as infile, \
                 open(output_file, 'a', newline='', encoding='utf-8') as outfile, \
                 open(failed_file, 'a', newline='', encoding='utf-8') as failfile:
                 
                reader = csv.DictReader(infile)  
                writer = csv.writer(outfile)
                fail_writer = csv.DictWriter(failfile, fieldnames=reader.fieldnames)
                
                all_rows = list(reader)
                rows = all_rows[6700:] 
                total_rows = len(rows)
                chunk_size = 100
                count = 0
                
                self.stdout.write(f"Loaded {total_rows} rows. Processing in batches of {chunk_size}...")
                
                def get_chunks(data, size):
                    for i in range(0, len(data), size):
                        yield data[i:i + size]
                
                for chunk in get_chunks(rows, chunk_size):
                    self.stdout.write(f"Sending next batch...")
                    
                    coords_list = get_coords_of_station(chunk)
                    
                    for row, (lat, lon) in zip(chunk, coords_list):
                        writer.writerow([row['State'], lat, lon])
                        
                        if lat == 0.0 and lon == 0.0:
                            fail_writer.writerow(row)
                            
                        count += 1
                        
                    outfile.flush()
                    failfile.flush()
                    
                    time.sleep(1)
                        
                self.stdout.write(self.style.SUCCESS(f"\nDone! Successfully processed {count} locations in batches."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Critical error: {e}"))
