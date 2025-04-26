from ckanapi import RemoteCKAN
from dotenv import load_dotenv
import csv
from pathlib import Path
import os
import time

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
rc = RemoteCKAN('https://dadosabertos.bndes.gov.br/', apikey=API_TOKEN)

# Initialize empty list to store all records
all_records = []
offset = 0
limit = 1000  # Fetch more records per request
total_records = None

print("Fetching data from BNDES API...")

# Loop until we've retrieved all records
while total_records is None or offset < total_records:
    result = rc.action.datastore_search(
        resource_id="d117404f-092b-435d-a229-dc72c9b27dad",
        limit=limit,
        offset=offset
    )
    
    # Get total number of records if not already set
    if total_records is None:
        total_records = result['total']
        print(f"Total records to fetch: {total_records}")
    
    # Add records to our collection
    records = result.get('records', [])
    all_records.extend(records)
    
    # Update offset for next iteration
    offset += limit
    
    # Print progress
    print(f"Fetched {len(all_records)} of {total_records} records ({(len(all_records)/total_records)*100:.1f}%)")

print(f"Successfully retrieved all {len(all_records)} records")

# Create the directory if it doesn't exist
output_dir = Path('bndes_despesas_viagens/data/raw')
output_dir.mkdir(parents=True, exist_ok=True)

# Save the result as CSV
output_file = output_dir / 'bndes_despesas_viagens.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    if all_records:
        writer = csv.DictWriter(f, fieldnames=all_records[0].keys())
        writer.writeheader()
        writer.writerows(all_records)

print(f"Data saved to {output_file}")
