import sys
import os
import csv
import time
from api.fuelApi.constants.state_codes import STATE_CODES
from api.fuelApi.service.ingestion_service import get_coords_of_state

def main():
    output_file = os.path.join(os.path.dirname(__file__), 'api', 'fuelApi', 'constants', 'state-coords.csv')
    
    print(f"Writing state coordinates to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name','code', 'latitude', 'longitude'])
        
        for code, full_name in STATE_CODES.items():
            print(f"Fetching coords for {full_name} ({code})...")
            
            response = get_coords_of_state(code)
            
            if response:
                lat = response.get('lat', '0.0')
                lon = response.get('lon', '0.0')
                
                writer.writerow([full_name, code, lat, lon])
                print(f"Success: {lat}, {lon}")
            else:
                writer.writerow([full_name, code, '0.0', '0.0'])
                print(f"Failed to get coords for {full_name}")
                
            time.sleep(1.5)
            
    print("Finished extracting all state coordinates!")

if __name__ == "__main__":
    main()
