import json
import re
import requests
import random
import csv
import string
from typing import Dict, List

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
def send_request(payload: Dict[str, str]) -> requests.Response:
    response = requests.post("https://engineweb.gomatimvvnl.in/prepaid_recharge_sync/", json=payload)
    return response

# Function to capture test results
def capture_test_results(test_func: callable, description: str, row_number: int, response=None, request_payload=None, response_json=None) -> str:
    result = f"Row {row_number} : {description}"
    try:
        if response:
            test_func(response)
        elif request_payload:
            test_func(request_payload)
        elif response_json:
            test_func(response_json)
        result = f"PASS : {result}"
    except AssertionError as e:
        result = f"FAIL : {result}\nReason: {str(e)}"
        if response:
            result += f"\nResponse Status Code: {response.status_code}\nResponse Body: {response.text}"
    return result

# Test functions
def test_status_code(response: requests.Response) -> None:
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response body: {response.text}"

def test_response_is_json(response: requests.Response) -> None:
    assert response.headers["Content-Type"] == "application/json", f"Expected content type to be 'application/json', but got '{response.headers['Content-Type']}'"
    response_json = response.json()
    assert response_json is not None, "Response JSON is None"

def test_request_payload_is_json(request_payload: Dict[str, str]) -> None:
    try:
        json.dumps(request_payload)  # Attempt to serialize request_payload to JSON
    except (TypeError, ValueError) as e:
        raise AssertionError(f"Request payload is not in valid JSON format. Reason: {str(e)}")

def test_account_no_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "accountNo" in request_payload, "'accountNo' key not found in request payload"
    assert isinstance(request_payload["accountNo"], str), f"'accountNo' should be of type 'string', but got {type(request_payload['accountNo'])}"
    assert len(request_payload["accountNo"]) == 10, f"'accountNo' should be 10 characters long, but got {len(request_payload['accountNo'])}"
    assert re.match(r"^\d+$", request_payload["accountNo"]), "'accountNo' should only contain digits"

def test_amount_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "amount" in request_payload, "'amount' key not found in request payload"
    assert isinstance(request_payload["amount"], str), f"'amount' should be of type 'string', but got {type(request_payload['amount'])}"
    assert re.match(r"^\d+(\.\d+)?$", request_payload["amount"]), "'amount' should only contain digits"

def test_meter_number_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "meterNumber" in request_payload, "'meterNumber' key not found in request payload"
    assert isinstance(request_payload["meterNumber"], str), f"'meterNumber' should be of type 'string', but got {type(request_payload['meterNumber'])}"
    assert len(request_payload["meterNumber"]) <= 16, f"'meterNumber' should be at most 16 characters long, but got {len(request_payload['meterNumber'])}"
    assert re.match(r"^\d+$", request_payload["meterNumber"]), "'meterNumber' should only contain digits"

def test_payment_date_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "paymentDate" in request_payload, "'paymentDate' key not found in request payload"
    assert isinstance(request_payload["paymentDate"], str), f"'paymentDate' should be of type 'string', but got {type(request_payload['paymentDate'])}"
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", request_payload["paymentDate"]), "'paymentDate' format should be 'YYYY-MM-DDTHH:MM:SS'"

def test_source_of_recharge_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "sourceOfRecharge" in request_payload, "'sourceOfRecharge' key not found in request payload"
    assert isinstance(request_payload["sourceOfRecharge"], str), f"'sourceOfRecharge' should be of type 'string', but got {type(request_payload['sourceOfRecharge'])}"
    assert request_payload["sourceOfRecharge"] in ["ONLINE", "OFFLINE"], f"'sourceOfRecharge' should be 'ONLINE' or 'OFFLINE', but got {request_payload['sourceOfRecharge']}"

def test_transaction_id_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "transactionId" in request_payload, "'transactionId' key not found in request payload"
    assert isinstance(request_payload["transactionId"], str), f"'transactionId' should be of type 'string', but got {type(request_payload['transactionId'])}"
    assert 1 <= len(request_payload["transactionId"]) <= 12, f"'transactionId' should be between 1 and 12 characters long, but got {len(request_payload['transactionId'])}"
    assert re.match(r"^[a-zA-Z0-9]+$", request_payload["transactionId"]), "'transactionId' should only contain alphanumeric characters"

def test_param1_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "param1" in request_payload, "'param1' key not found in request payload"
    assert isinstance(request_payload["param1"], str), f"'param1' should be of type 'string', but got {type(request_payload['param1'])}"

def test_param2_format_and_type(request_payload: Dict[str, str]) -> None:
    assert "param2" in request_payload, "'param2' key not found in request payload"
    assert isinstance(request_payload["param2"], str), f"'param2' should be of type 'string', but got {type(request_payload['param2'])}"

def test_response_message_and_status_code(response_json: Dict[str, any]) -> None:
    assert "message" in response_json, f"'message' key not found in response JSON. Response body: {response_json}"
    assert isinstance(response_json["message"], str), f"'message' should be of type 'string', but got {type(response_json['message'])}"
    assert "Prepaid Recharge Sync successful for Account ID :" in response_json["message"], "'message' does not contain the expected text"

    assert "status_code" in response_json, f"'status_code' key not found in response JSON. Response body: {response_json}"
    assert isinstance(response_json["status_code"], int), f"'status_code' should be of type 'int', but got {type(response_json['status_code'])}"
    assert response_json["status_code"] == 201, f"Expected status code 201, but got {response_json['status_code']}"

# Main function to iterate over each row in the CSV and store results
def process_test_results(file_path: str = 'prepaid_recharge_data.csv') -> str:
    payloads = read_request_payloads_from_csv(file_path)
    all_results = []

    for row_number, payload in enumerate(payloads, start=1):
        request_payload = payload
        request_payload["transactionId"] = generate_random_transaction_id()
        
        # Extract accountId
        account_id = request_payload.get("accountNo", "Unknown")
        
        response = send_request(request_payload)
        response_json = response.json()
        
        # Include accountId in the results
        all_results.append(f"Row {row_number} - Account ID: {account_id}\n")

        all_results.append(capture_test_results(lambda resp: test_status_code(resp), "Status code is 201", row_number, response=response))
        all_results.append(capture_test_results(lambda resp: test_response_is_json(resp), "Response is in JSON format", row_number, response=response))
        all_results.append(capture_test_results(lambda req_payload: test_request_payload_is_json(req_payload), "Request payload is in JSON format", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_account_no_format_and_type(req_payload), "Validate accountNo format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_amount_format_and_type(req_payload), "Validate amount format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_meter_number_format_and_type(req_payload), "Validate meterNumber format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_payment_date_format_and_type(req_payload), "Validate paymentDate format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_source_of_recharge_format_and_type(req_payload), "Validate sourceOfRecharge format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_transaction_id_format_and_type(req_payload), "Validate transactionId format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_param1_format_and_type(req_payload), "Validate param1 format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda req_payload: test_param2_format_and_type(req_payload), "Validate param2 format and type", row_number, request_payload=request_payload))
        all_results.append(capture_test_results(lambda resp_json: test_response_message_and_status_code(resp_json), "Validate response message and status_code", row_number, response_json=response_json))
        
        all_results.append("\n\n")  # Add two newlines after each row iteration

    return "\n".join(all_results)
