import json
import re
import requests
import csv
import string
import random
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
    url = f"https://engineweb.gomatimvvnl.in/mdms_api/recharge_history_new/{account_id}/{meter_number}"
    response = requests.get(url)
    return response

# Function to capture test results
def capture_test_results(test_func: callable, description: str, row_number: int, response=None, request_payload=None) -> str:
    result = f"Row {row_number} : {description}"
    try:
        if response:
            test_func(response)
        elif request_payload:
            test_func(request_payload)
        result = f"PASS : {result}"
    except AssertionError as e:
        result = f"FAIL : {result}\nReason: {str(e)}"
        if response:
            result += f"\nResponse Status Code: {response.status_code}\nResponse Body: {response.text}"
    return result

# Test functions
def test_status_code(response: requests.Response) -> None:
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response body: {response.text}"

def test_response_is_json(response: requests.Response) -> None:
    assert response.headers["Content-Type"] == "application/json", f"Expected content type to be 'application/json', but got '{response.headers['Content-Type']}'"
    response_json = response.json()
    assert response_json is not None, "Response JSON is None"

def test_account_no_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "account_id" in request_payload, "'account_id' key not found in request payload"
    assert isinstance(request_payload["account_id"], str), f"'account_id' should be of type 'string', but got {type(request_payload['account_id'])}"
    assert len(request_payload["account_id"]) == 10, f"'account_id' should be 10 characters long, but got {len(request_payload['account_id'])}"
    assert re.match(r"^\d+$", request_payload["account_id"]), "'account_id' should only contain digits"

def test_meter_number_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "meter_number" in request_payload, "'meter_number' key not found in request payload"
    assert isinstance(request_payload["meter_number"], str), f"'meter_number' should be of type 'string', but got {type(request_payload['meter_number'])}"
    assert len(request_payload["meter_number"]) <= 16, f"'meter_number' should be at most 16 characters long, but got {len(request_payload['meter_number'])}"
    assert re.match(r"^[a-zA-Z0-9]*$", request_payload["meter_number"]), "'meter_number' should only contain alphanumeric characters"

# Function to process JSON response and format the results
def process_json_response(response_json: Dict, account_id: str, meter_number: str) -> List[Dict[str, str]]:
    result_stat = response_json.get("data", {}).get("result", {}).get("stat", [])
    csv_data = []
    for entry in result_stat:
        csv_data.append({
            "Account ID": account_id,
            "Meter Number": meter_number,
            "Test Result": "PASS",
            "Response Status Code": response_json.get("responseCode", "Unknown"),
            "consumer": entry.get("consumer"),
            "recharge_amount": entry.get("recharge_amount"),
            "arrear_deducted": entry.get("arrear_deducted"),
            "lpsc_deducted": entry.get("lpsc_deducted"),
            "datetime": entry.get("datetime"),
            "message": entry.get("message"),
            "status": entry.get("status"),
            "Fail Reason": ""  # Placeholder for any fail reason, if needed
        })
    return csv_data

# Function to handle cases where meter ID is not found
def handle_meter_not_found(account_id: str, meter_number: str) -> List[Dict[str, str]]:
    return [{
        "Account ID": account_id,
        "Meter Number": meter_number,
        "Test Result": "FAIL",
        "Response Status Code": "N/A",
        "consumer": "N/A",
        "recharge_amount": "N/A",
        "arrear_deducted": "N/A",
        "lpsc_deducted": "N/A",
        "datetime": "N/A",
        "message": "meter not found",
        "status": "FAIL",
        "Fail Reason": "Meter number not found in response"
    }]

# Function to save data to a CSV file
def save_to_csv(data: List[Dict[str, str]], file_name: str) -> None:
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Main function to iterate over each row in the CSV and store results
def process_test_results(file_path: str = 'user_input/get_recharge_history_new.csv') -> str:
    payloads = read_request_payloads_from_csv(file_path)
    all_results = []
    response_data = []

    for row_number, payload in enumerate(payloads, start=1):
        account_id = payload.get("account_id", "Unknown")
        meter_number = payload.get("meter_number", "Unknown")
        
        response = send_request(account_id, meter_number)
        response_json = response.json()
        
        if not response_json.get("data", {}).get("result", {}).get("stat"):
            # Handle meter not found case
            all_results.append(f"Row {row_number} - Account ID: {account_id}, Meter Number: {meter_number}\n")
            all_results.append(f"FAIL : Row {row_number} : Meter not found\n")
            response_data.extend(handle_meter_not_found(account_id, meter_number))
        else:
            # Include account_id and meter_number in the results
            all_results.append(f"Row {row_number} - Account ID: {account_id}, Meter Number: {meter_number}\n")

            all_results.append(capture_test_results(lambda resp: test_status_code(resp), "Status code is 200", row_number, response=response))
            all_results.append(capture_test_results(lambda resp: test_response_is_json(resp), "Response is in JSON format", row_number, response=response))
            all_results.append(capture_test_results(lambda req_payload: test_account_no_format_and_type(req_payload), "Validate account_id format and type", row_number, request_payload=payload))
            all_results.append(capture_test_results(lambda req_payload: test_meter_number_format_and_type(req_payload), "Validate meter_number format and type", row_number, request_payload=payload))

            # Include response data in the results
            filtered_data = process_json_response(response_json, account_id, meter_number)
            response_data.extend(filtered_data)

            all_results.append(f"Response Status Code: {response.status_code}\nResponse Body:\n{response.text}\n")

        all_results.append("\n\n")  # Add two newlines after each row iteration

    # Save the response data to CSV with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"get_recharge_history_new//get_recharge_history_new_{timestamp}.csv"
    save_to_csv(response_data, file_name)

    return "\n".join(all_results)

# Example usage
if __name__ == "__main__":
    file_path = 'user_input/get_recharge_history_new.csv'  # Replace with your CSV file path
    test_results = process_test_results(file_path)
    print(test_results)
