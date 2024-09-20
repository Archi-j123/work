import json
import re
import requests
import csv
import string
import random
import os
from typing import Dict, List
from datetime import datetime

# Function to generate a random transactionId
def generate_random_transaction_id(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to read payload data from a CSV file
def read_request_payloads_from_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        payloads = [row for row in reader]
    return payloads

# Function to send a request and get a response
def send_request(account_id: str, meter_number: str) -> requests.Response:
    url = f"https://engineweb.gomatimvvnl.in/mdms_api/recharge_history/{account_id}/{meter_number}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
    return response

# Function to extract required fields from the API response
def extract_fields_from_response(response: requests.Response) -> List[Dict[str, str]]:
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON response")
        return []

    # Check if 'data' and 'result' exist in the response JSON
    if response_json is None or "data" not in response_json or "result" not in response_json["data"]:
        print("Unexpected response structure")
        return []

    transactions = response_json["data"].get("result", {}).get("stat", [])
    
    # Prepare the list of records to be saved
    extracted_data = []
    
    for transaction in transactions:
        extracted_data.append({
            "consumer": transaction.get("consumer", ""),
            "amount": transaction.get("amount", 0),
            "date": transaction.get("date", ""),
            "time": transaction.get("time", ""),
            "receipt": transaction.get("receipt", ""),
            "message": transaction.get("message", ""),
            "status": transaction.get("status", "")
        })
    
    return extracted_data

# Main function to process rows and store results in CSV
def process_test_results_to_csv(file_path: str = 'prepaid_recharge_data.csv') -> None:
    payloads = read_request_payloads_from_csv(file_path)
    
    # Define CSV output path with timestamp (date + time) for uniqueness
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_folder = 'get_recharge_history'
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    output_file = os.path.join(output_folder, f"{timestamp}_get_recharge_history.csv")
    
    # Prepare the headers for the output CSV
    csv_headers = ["Row", "Account ID", "Meter Number", "Consumer", "Amount", "Date", "Time", "Receipt", "Message", "Status"]

    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()  # Write headers to the CSV
        
        row_number = 1  # Initialize row number
        for payload in payloads:
            account_id = payload.get("account_id", "Unknown")
            meter_number = payload.get("meter_number", "Unknown")
            
            response = send_request(account_id, meter_number)
            
            if response.status_code == 200:
                extracted_data = extract_fields_from_response(response)
                
                # If no transactions found, print and record the meter not found message
                if not extracted_data:
                    print(f"Meter Number {meter_number}: Meter not found")
                    writer.writerow({
                        "Row": row_number,
                        "Account ID": account_id,
                        "Meter Number": meter_number,
                        "Consumer": "N/A",
                        "Amount": "N/A",
                        "Date": "N/A",
                        "Time": "N/A",
                        "Receipt": "N/A",
                        "Message": "Meter not found",
                        "Status": "N/A"
                    })
                else:
                    # Write each transaction from the response into the CSV
                    for transaction in extracted_data:
                        writer.writerow({
                            "Row": row_number,
                            "Account ID": account_id,
                            "Meter Number": meter_number,
                            "Consumer": transaction["consumer"],
                            "Amount": transaction["amount"],
                            "Date": transaction["date"],
                            "Time": transaction["time"],
                            "Receipt": transaction["receipt"],
                            "Message": transaction["message"],
                            "Status": transaction["status"]
                        })
                        row_number += 1  # Increment row number for each transaction
            else:
                # Handle case where response status is not 200
                writer.writerow({
                    "Row": row_number,
                    "Account ID": account_id,
                    "Meter Number": meter_number,
                    "Consumer": "N/A",
                    "Amount": "N/A",
                    "Date": "N/A",
                    "Time": "N/A",
                    "Receipt": "N/A",
                    "Message": f"Failed with status {response.status_code}",
                    "Status": "N/A"
                })
                row_number += 1

    return (f"Test results saved to: {output_file}")

# Example usage
file_path = 'user_input\\get_recharge_history.csv'  # Replace with your CSV file path
process_test_results_to_csv(file_path)
