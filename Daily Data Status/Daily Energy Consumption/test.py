import csv
import requests
from datetime import datetime

# Define the API endpoint
API_ENDPOINT = 'https://engineweb.gomatimvvnl.in/daily_energy_consumption/'

def post_data_to_api(data):
    try:
        response = requests.post(API_ENDPOINT, json=data)
        response.raise_for_status()
        print(f"Success: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def process_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Validate and prepare data
            try:
                data = {
                    "start_daily_datetime": datetime.now().isoformat(),  # Use current datetime for demo purposes
                    "end_daily_datetime": datetime.now().isoformat(),
                    "account_id": row['account_id'],
                    "meter_number": row['meter_number'],
                    "energy_consumption_kwh": float(row['consumption_min']),
                    "energy_consumption_kvah": float(row['consumption_max']),
                    "energy_consumption_export_kwh": 0,
                    "energy_consumption_export_kvah": float(row['energy_consumption_export_kvah']),
                    "start_import_wh": 0,
                    "end_import_wh": 0,
                    "start_import_vah": 0,
                    "end_import_vah": 0,
                    "start_export_wh": 0,
                    "end_export_wh": 0,
                    "start_export_vah": 0,
                    "end_export_vah": 0,
                    "net_metering_flag": row['net_metering_flag'].upper(),
                    "max_demand": float(row['max_demand']),
                    "multiplying_factor": 1
                }
                
                # Ensure net_metering_flag is valid
                if data["net_metering_flag"] not in ["Y", "N"]:
                    print(f"Invalid net_metering_flag value: {data['net_metering_flag']} for account_id: {data['account_id']}")
                    continue
                
                post_data_to_api(data)
            except ValueError as e:
                print(f"Data Error: {e} for row: {row}")

# Replace 'your_file.csv' with the path to your CSV file
process_csv('your_file.csv')
