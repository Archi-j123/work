import csv
import requests
import json

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

# Function to read the deviceId values from CSV and post data to the API
def post_data_from_csv(csv_file):
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
                    print(f"Success: Data posted for deviceId {device_id}")
                else:
                    # Log response details for failed requests
                    print(f"Failed: Data posting failed for deviceId {device_id}. Status Code: {response.status_code}")
                    print(f"Response Content: {response.text}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error: {e} occurred for deviceId {device_id}")

# Specify the path to your CSV file
csv_file_path = 'data.csv'

# Run the function to post data from CSV
post_data_from_csv(csv_file_path)
