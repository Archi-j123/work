import csv
import requests
import json
from datetime import datetime

# Define the static data payload (excluding deviceId)
payload_template = {
    "dtrId": "S1_LongRun_20240215_213023",
    "dtrName": "UPLongRunTesting",
    "pssId": "Pss_sagarsingh_20240711_171455",
    "pssName": "Pss LongRun testing",
    "feederId": "Feeder_testing_20240215_213023",
    "feederName": "LongRunFeeder",
    "latitude": 0,
    "longitude": 0  # Add the longitude field here
}

# Define the API endpoint
api_url = "https://hes.integration.test.gomatimvvnl.in/api/hes/meter-post-installation"

# Function to read deviceId values from CSV, post data, and log results in separate CSVs
def post_data_from_csv(csv_file):
    # Create files to store successful and failed deviceIds
    success_file = f'meter_updated_successfully_{datetime.today().strftime("%Y-%m-%d")}.csv'
    failure_file = f'meter_not_found_{datetime.today().strftime("%Y-%m-%d")}.csv'
    
    # Open files to write results
    with open(success_file, mode='w', newline='') as success_csv, open(failure_file, mode='w', newline='') as failure_csv:
        success_writer = csv.writer(success_csv)
        failure_writer = csv.writer(failure_csv)
        
        # Write headers
        success_writer.writerow(['deviceId', 'status'])
        failure_writer.writerow(['deviceId', 'status'])
        
        # Read the input CSV file
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                device_id = row['deviceId']  # Extract the deviceId from CSV
                payload = payload_template.copy()  # Make a copy of the template
                payload['deviceId'] = device_id  # Set the deviceId in the payload
                
                try:
                    # Send the POST request with JSON payload
                    response = requests.post(api_url, json=payload)
                    
                    # Check if the request was successful
                    if response.status_code == 200:
                        success_writer.writerow([device_id, 'Success'])
                        print(f"Success: Data posted for deviceId {device_id}")
                    elif response.status_code == 404:  # Example of handling "Not Found"
                        failure_writer.writerow([device_id, 'Meter Not Found'])
                        print(f"Meter Not Found: {device_id}")
                    else:
                        failure_writer.writerow([device_id, f"Failed (Status {response.status_code})"])
                        print(f"Failed: Data posting failed for deviceId {device_id}. Status Code: {response.status_code}")
                        print(f"Response Content: {response.text}")
                
                except requests.exceptions.RequestException as e:
                    # Log network-related exceptions to the failure CSV
                    failure_writer.writerow([device_id, f"Error: {e}"])
                    print(f"Error: {e} occurred for deviceId {device_id}")

# Specify the path to your input CSV file
csv_file_path = 'data.csv'

# Run the function to post data from CSV and log results in separate CSV files
post_data_from_csv(csv_file_path)
