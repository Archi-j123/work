import requests
from datetime import datetime, timedelta
import time


# Set initial values
start_date = datetime.strptime("2024-06-01 00:00:00", "%Y-%m-%d %H:%M:%S")  # Start date in full format
end_date = datetime.strptime("2024-06-06 00:00:00", "%Y-%m-%d %H:%M:%S")  # End date in full format
account_id = 410014020  # Replace with your 10-digit account ID as an integer


# Iterate through each day
while start_date <= end_date:
    # Format the date in the required string format
    formatted_date = start_date.strftime("%Y-%m-%d 00:00:00")
   
    # API endpoint URL with date as path variable
    url = f"https://engineweb.gomatimvvnl.in/trigger_task/daily_ledger_task/{formatted_date}"
   
    # Prepare the query parameters with the account ID
    params = {
        "account_id": account_id  # Account ID as an integer
    }
   
    # Print the input date and account ID
    print(f"Input: Date: {formatted_date}, Account ID: {account_id}")
   
    # Send the GET request
    response = requests.get(url, params=params)
   
    # Print the response status code and text
    print(f"Response: {response.status_code} - {response.text}\n")
   
    # Move to the next day
    start_date += timedelta(days=1)


    time.sleep(10)
