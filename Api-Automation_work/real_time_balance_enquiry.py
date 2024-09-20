import requests
import re
import pandas as pd

# Read accountId from CSV file
def read_account_id_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        account_ids = df['accountId'].tolist()
        return account_ids
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV file: {str(e)}")

def make_api_request(account_id):
    url = f"https://engineweb.gomatimvvnl.in/prepaid_balance_enquiry/{account_id}/"
    response = requests.get(url)
    return response

def run_check(check_func, description):
    try:
        check_func()
        return f"PASS: {description}\n"
    except AssertionError as e:
        return f"FAIL: {description}\nReason: {str(e)}\n"
    except Exception as e:
        return f"ERROR: {description}\n{str(e)}\n"

def check_status_code(response):
    expected_status_code = 200
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {actual_status_code}"

def check_account_id_not_null(response):
    json_data = response.json()
    account_id_from_response = json_data.get("accountId")
    assert account_id_from_response is not None, "accountId is null"

def check_account_id_digits_only(response):
    json_data = response.json()
    account_id_from_response = json_data.get("accountId")
    assert account_id_from_response is not None, "Cannot check digits, accountId is null"
    assert re.match(r"^\d+$", account_id_from_response), \
        f"Expected accountId to contain only digits, but got {account_id_from_response}"

def check_account_id_length(response):
    json_data = response.json()
    account_id_from_response = json_data.get("accountId")
    expected_length = 10
    assert account_id_from_response is not None, "Cannot check length, accountId is null"
    actual_length = len(account_id_from_response)
    assert actual_length == expected_length, \
        f"Expected accountId length to be {expected_length} digits, but got {actual_length} digits"

def check_account_ids(file_path):
    result = ""
    account_ids = read_account_id_from_csv(file_path)

    for account_id in account_ids:
        result += f"Expected Result: 10 digit Number only.\n\n"
        result += f"Checking accountId: {account_id}\n\n"
        
        response = make_api_request(account_id)
        
        if response.status_code == 200:
            result += run_check(lambda: check_status_code(response), "Status code is 200")
            result += run_check(lambda: check_account_id_not_null(response), "accountId is not null")
            result += run_check(lambda: check_account_id_digits_only(response), "accountId contains only digits")
            result += run_check(lambda: check_account_id_length(response), "accountId length is exactly 10 digits")
        else:
            result += f"ERROR: API request failed with status code {response.status_code}. Skipping further checks.\n"
        
        result += "\n"
    
    return result
