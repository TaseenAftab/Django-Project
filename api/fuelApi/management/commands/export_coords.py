import csv
import requests
import urllib.parse
from django.core.management.base import BaseCommand
from api.fuelApi.constants.state_codes import STATE_CODES

class Command(BaseCommand):
    help = "Makes a csv with coordinates of truck stops"

    def handle(self, *args, **kwargs):
        input_file = 'api/fuelApi/constants/fuel-prices.csv'
        output_file = 'api/fuelApi/constants/station-locations.csv'
        
        api_key = "kg4ZQBmtXswSHQTWH7GT49Us4XBDjFGw"
        batch_url = f"https://api.tomtom.com/search/2/batch/sync.json?key={api_key}"
        
        self.stdout.write(f"Reading from {input_file} and writing to {output_file}...")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as infile, \
                 open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                 
                reader = csv.DictReader(infile)
                writer = csv.writer(outfile)
                writer.writerow(['statecode','latitude', 'longitude'])
                
                rows = list(reader)
                total_rows = len(rows)
                chunk_size = 100
                count = 0
                
                self.stdout.write(f"Loaded {total_rows} rows. Processing in batches of {chunk_size}...")
                
                for i in range(0, total_rows, chunk_size):
                    chunk = rows[i:i + chunk_size]
                    batch_items = []
                    
                    for row in chunk:
                        name = row['Truckstop Name']
                        address = row['Address'].replace("&", "and")
                        city = row['City']
                        state_code = row['State']
                        full_state_name = STATE_CODES.get(state_code.upper(), state_code)
                        
                        final_query = f"{name}, {address}, {city}, {full_state_name}, USA"
                        encoded_query = urllib.parse.quote(final_query)
                        
                        query_url = f"/search/2/search/{encoded_query}.json?limit=1"
                        batch_items.append({"query": query_url})
                        
                    payload = {"batchItems": batch_items}
                    
                    self.stdout.write(f"Sending batch {i // chunk_size + 1}...")
                    response = requests.post(batch_url, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        responses = data.get('batchItems', [])
                        
                        for idx, item in enumerate(responses):
                            row = chunk[idx]
                            lat, lon = 0.0, 0.0
                            
                            if item['statusCode'] == 200:
                                res_body = item.get('response', {})
                                results = res_body.get('results', [])
                                if results:
                                    lat = results[0]['position']['lat']
                                    lon = results[0]['position']['lon']
                                    
                            writer.writerow([row['State'], lon, lat])
                            count += 1
                    else:
                        self.stdout.write(self.style.ERROR(f"Batch failed with status {response.status_code}. Using fallback [0.0, 0.0]"))
                        for row in chunk:
                            writer.writerow([row['State'], 0.0, 0.0])
                            count += 1
                            
                    outfile.flush()
                        
                self.stdout.write(self.style.SUCCESS(f"\nDone! Successfully processed {count} locations in batches."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Critical error: {e}"))
