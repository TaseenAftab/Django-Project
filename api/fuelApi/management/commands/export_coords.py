import csv
import time
from django.core.management.base import BaseCommand
from api.fuelApi.service.ingestion_service import get_coords_of_station

class Command(BaseCommand):
    help = "Generates an updated CSV with all original data plus latitude and longitude using TomTom Batch Search API."

    def handle(self, *args, **kwargs):
        input_file = 'api/fuelApi/constants/fuel-prices.csv'
        output_file = 'api/fuelApi/constants/fuel-prices-updated.csv'
        failed_file = 'api/fuelApi/constants/failed-stations.csv'
        
        self.stdout.write(f"Reading from {input_file} and writing to {output_file}...")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as infile, \
                 open(output_file, 'a', newline='', encoding='utf-8') as outfile, \
                 open(failed_file, 'a', newline='', encoding='utf-8') as failfile:
                 
                reader = csv.DictReader(infile)
                
                out_fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
                writer = csv.DictWriter(outfile, fieldnames=out_fieldnames)
                # No writeheader() because we are appending
                
                fail_writer = csv.DictWriter(failfile, fieldnames=reader.fieldnames)
                # No writeheader() because we are appending
                
                all_rows = list(reader)
                total_rows = len(all_rows)
                chunk_size = 100
                count = 0
                
                self.stdout.write(f"Loaded {total_rows} rows. Processing in batches of {chunk_size}...")
                
                def get_chunks(data, size):
                    for i in range(0, len(data), size):
                        yield data[i:i + size]
                
                for chunk in get_chunks(all_rows, chunk_size):
                    self.stdout.write(f"Sending next batch...")
                    
                    coords_list = get_coords_of_station(chunk)
                    
                    for row, (lat, lon) in zip(chunk, coords_list):
                        # Create a copy of the row to add the lat/lon
                        row_out = dict(row)
                        row_out['Latitude'] = lat
                        row_out['Longitude'] = lon
                        
                        writer.writerow(row_out)
                        
                        if lat == 0.0 and lon == 0.0:
                            fail_writer.writerow(row)
                            
                        count += 1
                        
                    outfile.flush()
                    failfile.flush()
                    
                    time.sleep(1)
                    
            self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} records!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading or writing file: {e}"))
