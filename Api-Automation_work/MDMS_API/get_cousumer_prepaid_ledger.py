import csv
import json
import requests
import datetime
import re
import string
import random
from typing import Dict, List

# Function to generate a random transactionId
def generate_random_transaction_id(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to read request payloads from a CSV file
def read_request_payloads_from_csv(file_path: str) -> List[Dict[str, str]]:
    payloads = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            payloads.append(row)
    return payloads

# Function to send a request and get a response
def send_request(account_id: str, meter_number: str) -> requests.Response:
    url = f"https://engineweb.gomatimvvnl.in/mdms_api/prepaid_ledger/{account_id}/{meter_number}"
    response = requests.get(url)
    return response

# Function to extract relevant data from the JSON response
def extract_data_from_response(response: requests.Response) -> Dict[str, str]:
    data = response.json()
    
    # Filtering out unwanted parts
    result = data.get("data", {}).get("result", {}).get("stat", [{}])[0]
    
    # Extracting relevant fields
    extracted_data = {
        "Account ID": data.get("data", {}).get("result", {}).get("account_id", ""),
        "Meter Number": data.get("data", {}).get("result", {}).get("meter_number", ""),
        "Test Result": "PASS",
        "Response Status Code": response.status_code,
        "id": result.get("id", ""),
        "created_at": result.get("created_at", ""),
        "start_date_time": result.get("start_date_time", ""),
        "end_date_time": result.get("end_date_time", ""),
        "daily_consumption": result.get("daily_consumption", ""),
        "daily_consumption_in_rupees": result.get("daily_consumption_in_rupees", ""),
        "cumm_daily_consumption_mtd": result.get("cumm_daily_consumption_mtd", ""),
        "cumm_daily_consumption_rupees_mtd": result.get("cumm_daily_consumption_rupees_mtd", ""),
        "daily_consumption_export": result.get("daily_consumption_export", ""),
        "daily_consumption_export_in_rupees": result.get("daily_consumption_export_in_rupees", ""),
        "cumm_daily_consumption_export_mtd": result.get("cumm_daily_consumption_export_mtd", ""),
        "cumm_daily_consumption_export_rupees_mtd": result.get("cumm_daily_consumption_export_rupees_mtd", ""),
        "daily_consumption_export_carry_forward": result.get("daily_consumption_export_carry_forward", ""),
        "cumm_daily_consumption_export_carry_forward_mtd": result.get("cumm_daily_consumption_export_carry_forward_mtd", ""),
        "daily_green_energy_consumption_in_rupees": result.get("daily_green_energy_consumption_in_rupees", ""),
        "cumm_daily_green_energy_consumption_rupees_mtd": result.get("cumm_daily_green_energy_consumption_rupees_mtd", ""),
        "cumm_ec_charges_mtd": result.get("cumm_ec_charges_mtd", ""),
        "cumm_ec_charges_mtd_conversion": result.get("cumm_ec_charges_mtd_conversion", ""),
        "daily_fixed_charges": result.get("daily_fixed_charges", ""),
        "cumm_daily_fixed_charges_mtd": result.get("cumm_daily_fixed_charges_mtd", ""),
        "cumm_daily_fixed_charges_mtd_conversion": result.get("cumm_daily_fixed_charges_mtd_conversion", ""),
        "daily_ec_discount": result.get("daily_ec_discount", ""),
        "cumm_daily_ec_discount_mtd": result.get("cumm_daily_ec_discount_mtd", ""),
        "daily_fc_discount": result.get("daily_fc_discount", ""),
        "cumm_daily_fc_discount_mtd": result.get("cumm_daily_fc_discount_mtd", ""),
        "daily_ec_rebate": result.get("daily_ec_rebate", ""),
        "cumm_daily_ec_rebate_mtd": result.get("cumm_daily_ec_rebate_mtd", ""),
        "daily_fc_rebate": result.get("daily_fc_rebate", ""),
        "cumm_daily_fc_rebate_mtd": result.get("cumm_daily_fc_rebate_mtd", ""),
        "cumm_ed_charges_mtd": result.get("cumm_ed_charges_mtd", ""),
        "cumm_dmc_mtd": result.get("cumm_dmc_mtd", ""),
        "daily_recharges": result.get("daily_recharges", ""),
        "cumm_daily_recharges_mtd": result.get("cumm_daily_recharges_mtd", ""),
        "daily_arrear_charge": result.get("daily_arrear_charge", ""),
        "cumm_daily_arrear_charge_mtd": result.get("cumm_daily_arrear_charge_mtd", ""),
        "daily_lpsc_charge": result.get("daily_lpsc_charge", ""),
        "cumm_daily_lpsc_charge_mtd": result.get("cumm_daily_lpsc_charge_mtd", ""),
        "daily_late_payment_surcharge": result.get("daily_late_payment_surcharge", ""),
        "cumm_daily_late_payment_surcharge_mtd": result.get("cumm_daily_late_payment_surcharge_mtd", ""),
        "daily_credit_debit": result.get("daily_credit_debit", ""),
        "cumm_daily_credit_debit_mtd": result.get("cumm_daily_credit_debit_mtd", ""),
        "max_demand": result.get("max_demand", ""),
        "daily_max_demand_adjustment": result.get("daily_max_demand_adjustment", ""),
        "cumm_daily_max_demand_adjustment_mtd": result.get("cumm_daily_max_demand_adjustment_mtd", ""),
        "daily_max_demand_penalty": result.get("daily_max_demand_penalty", ""),
        "cumm_daily_max_demand_penalty_mtd": result.get("cumm_daily_max_demand_penalty_mtd", ""),
        "actual_cumm_daily_consumption": result.get("actual_cumm_daily_consumption", ""),
        "opening_balance": result.get("opening_balance", ""),
        "closing_balance": result.get("closing_balance", ""),
        "ledger_reset_flag": result.get("ledger_reset_flag", ""),
        "remarks": result.get("remarks", "")
    }
    
    return extracted_data

# Function to save data to a CSV file
def save_data_to_csv(data: List[Dict[str, str]], file_name: str) -> None:
    fieldnames = [
        "Account ID", "Meter Number", "Test Result", "Response Status Code", "id", "created_at",
        "start_date_time", "end_date_time", "daily_consumption",
        "daily_consumption_in_rupees", "cumm_daily_consumption_mtd", "cumm_daily_consumption_rupees_mtd",
        "daily_consumption_export", "daily_consumption_export_in_rupees", "cumm_daily_consumption_export_mtd",
        "cumm_daily_consumption_export_rupees_mtd", "daily_consumption_export_carry_forward",
        "cumm_daily_consumption_export_carry_forward_mtd", "daily_green_energy_consumption_in_rupees",
        "cumm_daily_green_energy_consumption_rupees_mtd", "cumm_ec_charges_mtd",
        "cumm_ec_charges_mtd_conversion", "daily_fixed_charges", "cumm_daily_fixed_charges_mtd",
        "cumm_daily_fixed_charges_mtd_conversion", "daily_ec_discount", "cumm_daily_ec_discount_mtd",
        "daily_fc_discount", "cumm_daily_fc_discount_mtd", "daily_ec_rebate", "cumm_daily_ec_rebate_mtd",
        "daily_fc_rebate", "cumm_daily_fc_rebate_mtd", "cumm_ed_charges_mtd", "cumm_dmc_mtd",
        "daily_recharges", "cumm_daily_recharges_mtd", "daily_arrear_charge", "cumm_daily_arrear_charge_mtd",
        "daily_lpsc_charge", "cumm_daily_lpsc_charge_mtd", "daily_late_payment_surcharge",
        "cumm_daily_late_payment_surcharge_mtd", "daily_credit_debit", "cumm_daily_credit_debit_mtd",
        "max_demand", "daily_max_demand_adjustment", "cumm_daily_max_demand_adjustment_mtd",
        "daily_max_demand_penalty", "cumm_daily_max_demand_penalty_mtd", "actual_cumm_daily_consumption",
        "opening_balance", "closing_balance", "ledger_reset_flag", "remarks"
    ]
    
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Function to capture test results
def capture_test_results(test_func: callable, description: str, row_number: int, response=None, request_payload=None) -> str:
    try:
        # Check which arguments the test function expects and call it accordingly
        if test_func == test_account_no_format_and_type or test_func == test_meter_number_format_and_type:
            test_func(request_payload=request_payload)
        else:
            test_func(response=response)
        return f"PASS : Row {row_number} : {description}"
    except AssertionError as e:
        return f"FAIL : Row {row_number} : {description} - {str(e)}"

# Test functions
def test_status_code(response: requests.Response) -> None:
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

def test_response_is_json(response: requests.Response) -> None:
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8', "Response is not in JSON format"

def test_account_no_format_and_type(request_payload: Dict[str, str]) -> None:
    assert isinstance(request_payload['account_id'], str), f"Expected type 'string', but got {type(request_payload['account_id'])}"
    assert len(request_payload['account_id']) == 10, f"'account_id' should be 10 characters long, but got {len(request_payload['account_id'])}"
    assert re.match(r"^\d+$", request_payload['account_id']), "'account_id' should only contain digits"

def test_meter_number_format_and_type(request_payload: Dict[str, str]) -> None:
    assert isinstance(request_payload['meter_number'], str), f"Expected type 'string', but got {type(request_payload['meter_number'])}"
    assert len(request_payload['meter_number']) == 12, f"'meter_number' should be 12 characters long, but got {len(request_payload['meter_number'])}"
    assert re.match(r"^\d+$", request_payload['meter_number']), "'meter_number' should only contain digits"

# Main code to run the tests
def run_tests(csv_file: str):
    payloads = read_request_payloads_from_csv(csv_file)
    results = []
    for row_number, payload in enumerate(payloads, start=1):
        transaction_id = generate_random_transaction_id()
        response = send_request(payload['account_id'], payload['meter_number'])
        data = extract_data_from_response(response)
        
        # Capture and store test results
        results.append({
            "Account ID": payload['account_id'],
            "Meter Number": payload['meter_number'],
            "Test Result": capture_test_results(test_status_code, "Status code is 200", row_number, response=response),
            "Response Status Code": response.status_code,
            "id": data["id"],
            "created_at": data["created_at"],
            "start_date_time": data["start_date_time"],
            "end_date_time": data["end_date_time"],
            "daily_consumption": data["daily_consumption"],
            "daily_consumption_in_rupees": data["daily_consumption_in_rupees"],
            "cumm_daily_consumption_mtd": data["cumm_daily_consumption_mtd"],
            "cumm_daily_consumption_rupees_mtd": data["cumm_daily_consumption_rupees_mtd"],
            "daily_consumption_export": data["daily_consumption_export"],
            "daily_consumption_export_in_rupees": data["daily_consumption_export_in_rupees"],
            "cumm_daily_consumption_export_mtd": data["cumm_daily_consumption_export_mtd"],
            "cumm_daily_consumption_export_rupees_mtd": data["cumm_daily_consumption_export_rupees_mtd"],
            "daily_consumption_export_carry_forward": data["daily_consumption_export_carry_forward"],
            "cumm_daily_consumption_export_carry_forward_mtd": data["cumm_daily_consumption_export_carry_forward_mtd"],
            "daily_green_energy_consumption_in_rupees": data["daily_green_energy_consumption_in_rupees"],
            "cumm_daily_green_energy_consumption_rupees_mtd": data["cumm_daily_green_energy_consumption_rupees_mtd"],
            "cumm_ec_charges_mtd": data["cumm_ec_charges_mtd"],
            "cumm_ec_charges_mtd_conversion": data["cumm_ec_charges_mtd_conversion"],
            "daily_fixed_charges": data["daily_fixed_charges"],
            "cumm_daily_fixed_charges_mtd": data["cumm_daily_fixed_charges_mtd"],
            "cumm_daily_fixed_charges_mtd_conversion": data["cumm_daily_fixed_charges_mtd_conversion"],
            "daily_ec_discount": data["daily_ec_discount"],
            "cumm_daily_ec_discount_mtd": data["cumm_daily_ec_discount_mtd"],
            "daily_fc_discount": data["daily_fc_discount"],
            "cumm_daily_fc_discount_mtd": data["cumm_daily_fc_discount_mtd"],
            "daily_ec_rebate": data["daily_ec_rebate"],
            "cumm_daily_ec_rebate_mtd": data["cumm_daily_ec_rebate_mtd"],
            "daily_fc_rebate": data["daily_fc_rebate"],
            "cumm_daily_fc_rebate_mtd": data["cumm_daily_fc_rebate_mtd"],
            "cumm_ed_charges_mtd": data["cumm_ed_charges_mtd"],
            "cumm_dmc_mtd": data["cumm_dmc_mtd"],
            "daily_recharges": data["daily_recharges"],
            "cumm_daily_recharges_mtd": data["cumm_daily_recharges_mtd"],
            "daily_arrear_charge": data["daily_arrear_charge"],
            "cumm_daily_arrear_charge_mtd": data["cumm_daily_arrear_charge_mtd"],
            "daily_lpsc_charge": data["daily_lpsc_charge"],
            "cumm_daily_lpsc_charge_mtd": data["cumm_daily_lpsc_charge_mtd"],
            "daily_late_payment_surcharge": data["daily_late_payment_surcharge"],
            "cumm_daily_late_payment_surcharge_mtd": data["cumm_daily_late_payment_surcharge_mtd"],
            "daily_credit_debit": data["daily_credit_debit"],
            "cumm_daily_credit_debit_mtd": data["cumm_daily_credit_debit_mtd"],
            "max_demand": data["max_demand"],
            "daily_max_demand_adjustment": data["daily_max_demand_adjustment"],
            "cumm_daily_max_demand_adjustment_mtd": data["cumm_daily_max_demand_adjustment_mtd"],
            "daily_max_demand_penalty": data["daily_max_demand_penalty"],
            "cumm_daily_max_demand_penalty_mtd": data["cumm_daily_max_demand_penalty_mtd"],
            "actual_cumm_daily_consumption": data["actual_cumm_daily_consumption"],
            "opening_balance": data["opening_balance"],
            "closing_balance": data["closing_balance"],
            "ledger_reset_flag": data["ledger_reset_flag"],
            "remarks": data["remarks"]
        })
    
    today_date = datetime.datetime.now().strftime("%d-%m-%Y")
    file_name = f"get_cousumer_prepaid_ledger//get_cousumer_prepaid_ledger_{today_date}_get_cousumer_prepaid_ledger1.csv" 
    save_data_to_csv(results, file_name)
    print(f"Data saved to {file_name}")

# Run the tests with a specified CSV file
if __name__ == "__main__":
    run_tests("user_input//get_cousumer_prepaid_ledger.csv")
