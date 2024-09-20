import pandas as pd
import requests
import json

# Read data from CSV file
df = pd.read_csv('new_file.csv')

# Define API endpoint
api_url = 'https://cis-internal.test.gomatimvvnl.in/save_master_data/'

# Function to post data to API
def post_data_to_api(data):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Prepare data in the format required by the API
    data = {
        "requestId": str(row.get('requestId', '')),
        "accountId": str(row.get('accountId', '')),
        "consumerName": str(row.get('consumerName', '')),
        "address1": str(row.get('address1', '')),
        "address2": str(row.get('address2', '')),
        "address3": str(row.get('address3', '')),
        "postcode": int(row.get('postcode', 0)),
        "mobileNumber": int(row.get('mobileNumber', 0)),
        "whatsAppnumber": int(row.get('whatsAppnumber', 0)),
        "email": str(row.get('email', '')),
        "badgeNumber": str(row.get('badgeNumber', '')),
        "supplyTypecode": str(row.get('supplyTypecode', '')),
        "meterSrno": str(row.get('meterSrno', '')),
        "sanctionedLoad": float(row.get('sanctionedLoad', 0.0)),
        "loadUnit": str(row.get('loadUnit', '')),
        "meterInstalldate": str(row.get('meterInstalldate', '')),
        "customerEntrydate": str(row.get('customerEntrydate', '')),
        "connectionStatus": str(row.get('connectionStatus', '')),
        "prepaidPostpaidflag": str(row.get('prepaidPostpaidflag', '')),
        "netMeterflag": str(row.get('netMeterflag', '')),
        "shuntCapacitorflag": str(row.get('shuntCapacitorflag', '')),
        "greenEnergyflag": str(row.get('greenEnergyflag', '')),
        "powerLoomcount": int(row.get('powerLoomcount', 0)),
        "rateSchedule": str(row.get('rateSchedule', '')),
        "meterType": str(row.get('meterType', '')),
        "meterMake": str(row.get('meterMake', '')),
        "multiplyingFactor": float(row.get('multiplyingFactor', 0.0)),
        "meterStatus": str(row.get('meterStatus', '')),
        "arrears": float(row.get('arrears', 0.0)),
        "prepaidOpeningbalance": float(row.get('prepaidOpeningbalance', 0.0)),
        "divisionCode": str(row.get('divisionCode', '')),
        "subDivCode": str(row.get('subDivCode', '')),
        "dtrCode": str(row.get('dtrCode', '')),
        "feederCode": str(row.get('feederCode', '')),
        "substaionCode": str(row.get('substaionCode', '')),
        "serviceAgreementid": str(row.get('serviceAgreementid', '')),
        "billCycle": str(row.get('billCycle', '')),
        "edApplicable": str(row.get('edApplicable', '')),
        "lpsc": float(row.get('lpsc', 0.0)),
        "param1": str(row.get('param1', '')),
        "param2": str(row.get('param2', '')),
        "param3": str(row.get('param3', '')),
        "param4": str(row.get('param4', '')),
        "param5": str(row.get('param5', ''))
    }

    # Post data to API
    response = post_data_to_api(data)
    
    # Print response
    print(f"Response for row {index + 1}: {response.status_code} - {response.text}")
