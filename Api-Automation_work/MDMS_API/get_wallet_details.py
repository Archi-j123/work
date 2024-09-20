import os
import json
import re
import requests
import csv
import string
import random
from typing import Dict, List
from tabulate import tabulate
from datetime import datetime

# Function to generate a random transaction ID
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
    url = f"https://engineweb.gomatimvvnl.in/mdms_api/wallet_details/{account_id}/{meter_number}"
    response = requests.get(url)
    return response

# Function to capture test results and print validations
def capture_test_results(test_func: callable, description: str, row_number: int, response=None, request_payload=None) -> str:
    result = f"Row {row_number} : {description}"
    try:
        if response:
            test_func(response)
        elif request_payload:
            test_func(request_payload)
        print(f"{result} -> PASS")  # Print the validation result as PASS
        return "PASS"
    except AssertionError as e:
        print(f"{result} -> FAIL. Reason: {str(e)}")  # Print the validation result as FAIL with reason
        return f"FAIL: {description}. Reason: {str(e)}"

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

# Function to format JSON response into a table with specific fields
def format_response_as_table(response_json: Dict[str, any]) -> Dict[str, str]:
    fields_of_interest = {
        'recharge_amount': 'Recharge Amount',
        'wallet_balance': 'Wallet Balance'
    }
    
    stat_list = response_json.get("data", {}).get("result", {}).get("stat", [])
    
    result = {}
    for item in stat_list:
        name = item.get("name")
        value = item.get("value")
        if name in fields_of_interest:
            result[name] = value
    
    return result

# Function to get the next available filename with incrementing number
def get_next_available_filename(base_path: str, base_filename: str) -> str:
    counter = 1
    while True:
        file_name = f"{base_filename}({counter}).csv"
        full_path = os.path.join(base_path, file_name)
        if not os.path.exists(full_path):
            return full_path
        counter += 1

# Main function to iterate over each row in the CSV and store results
def process_test_results1(file_path: str = 'user_input//get_wallet_details.csv') -> str:
    payloads = read_request_payloads_from_csv(file_path)
    
    today_date = datetime.now().strftime('%d-%m-%Y')
    base_filename = f"{today_date}_get_wallet_details"

    # Create 'get_wallet_details' folder if not exists
    folder_name = 'get_wallet_details'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Get next available filename
    output_file_name = get_next_available_filename(folder_name, base_filename)

    csv_data = []

    for row_number, payload in enumerate(payloads, start=1):
        account_id = payload.get("account_id", "Unknown")
        meter_number = payload.get("meter_number", "Unknown")
        
        response = send_request(account_id, meter_number)
        
        # Run all tests and capture results
        test_results = []
        fail_reasons = []
        
        # Capture individual test results
        status_code_result = capture_test_results(lambda resp: test_status_code(resp), "Status code is 200", row_number, response=response)
        if "FAIL" in status_code_result:
            fail_reasons.append(status_code_result)
        test_results.append(status_code_result)

        response_is_json_result = capture_test_results(lambda resp: test_response_is_json(resp), "Response is in JSON format", row_number, response=response)
        if "FAIL" in response_is_json_result:
            fail_reasons.append(response_is_json_result)
        test_results.append(response_is_json_result)

        account_no_format_result = capture_test_results(lambda req_payload: test_account_no_format_and_type(req_payload), "Validate account_id format and type", row_number, request_payload=payload)
        if "FAIL" in account_no_format_result:
            fail_reasons.append(account_no_format_result)
        test_results.append(account_no_format_result)

        meter_number_format_result = capture_test_results(lambda req_payload: test_meter_number_format_and_type(req_payload), "Validate meter_number format and type", row_number, request_payload=payload)
        if "FAIL" in meter_number_format_result:
            fail_reasons.append(meter_number_format_result)
        test_results.append(meter_number_format_result)

        # If all tests passed, mark it as PASS, otherwise FAIL
        if all(result == "PASS" for result in test_results):
            final_result = "PASS"
            fail_reason = ""
        else:
            final_result = "FAIL"
            fail_reason = "; ".join(fail_reasons)

        # Format the JSON response into a dictionary
        try:
            response_json = response.json()
            response_fields = format_response_as_table(response_json)
            recharge_amount = response_fields.get('recharge_amount', 'N/A')
            wallet_balance = response_fields.get('wallet_balance', 'N/A')
        except json.JSONDecodeError:
            recharge_amount = 'N/A'
            wallet_balance = 'N/A'
        
        # Append results to CSV data
        csv_data.append([
            account_id,
            meter_number,
            final_result,
            recharge_amount,
            wallet_balance,
            fail_reason
        ])
        
        # Print the completion message
        print(f"Row {row_number}: Account ID [{account_id}] and Meter Number [{meter_number}] process is successfully completed.")

    # Write to CSV with UTF-8 encoding
    with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Account ID', 'Meter Number', 'Test Result', 
            'Recharge Amount', 'Wallet Balance', 'Fail Reason'
        ])
        writer.writerows(csv_data)
    
    # Print table of results to the terminal
    headers = ['Account ID', 'Meter Number', 'Test Result', 'Recharge Amount', 'Wallet Balance', 'Fail Reason']
    print(tabulate(csv_data, headers=headers, tablefmt='grid'))

    return f"Results saved to {output_file_name}"

# Example usage
file_path = 'user_input//get_wallet_details.csv'  # Replace with your CSV file path
# Uncomment the line below to run the test
# test_results = process_test_results1(file_path)
# print(test_results)
