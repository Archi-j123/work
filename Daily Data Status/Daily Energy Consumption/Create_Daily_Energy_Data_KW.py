import requests
import csv
import random
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def fetch_parameters_from_csv(filename):
    parameters = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            parameters.append(row)
    return parameters

def generate_daily_consumption(consumption_min, consumption_max):
    return random.randint(consumption_min, consumption_max)

def post_energy_record(url, payload):
    response = requests.post(url, json=payload)
    return response

def process_records():
    # Get the selected file
    csv_filename = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    
    if not csv_filename:
        messagebox.showwarning("Warning", "No file selected!")
        return

    # Fetch records from the CSV file
    records = fetch_parameters_from_csv(csv_filename)

    # Clear the text area
    output_text.delete(1.0, tk.END)

    # API endpoint URL
    url = "https://engineweb.gomatimvvnl.in/daily_energy_consumption/"

    # Process each record
    for record in records:
        # Convert dates
        start_date = datetime.strptime(record["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(record["end_date"], "%Y-%m-%d")
        consumption_min = int(record["consumption_min"])
        consumption_max = int(record["consumption_max"])

        # Extract additional parameters
        energy_consumption_export_kvah = record["energy_consumption_export_kvah"]
        net_metering_flag = record["net_metering_flag"]  # Read from CSV
        max_demand = record["max_demand"]

        # Initial parameters
        start_import_wh_previous = 0  # Initial value

        # Iterate through each day in the range
        current_date = start_date
        while current_date <= end_date:
            start_daily_datetime = current_date.strftime("%Y-%m-%d 00:00:00")
            end_daily_datetime = (current_date + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

            # Generate daily consumption value
            energy_consumption_kwh = generate_daily_consumption(consumption_min, consumption_max)
            start_import_wh = start_import_wh_previous
            end_import_wh = energy_consumption_kwh + start_import_wh

            # Define the payload
            payload = {
                "start_daily_datetime": start_daily_datetime,
                "end_daily_datetime": end_daily_datetime,
                "account_id": record["account_id"],
                "meter_number": record["meter_number"],
                "energy_consumption_kwh": energy_consumption_kwh,
                "energy_consumption_kvah": 0,
                "energy_consumption_export_kwh": energy_consumption_export_kvah,
                "energy_consumption_export_kvah": 0,
                "start_import_wh": start_import_wh,
                "end_import_wh": end_import_wh,
                "start_import_vah": "00",
                "end_import_vah": "00",
                "start_export_wh": "00",
                "end_export_wh": "00",
                "start_export_vah": "00",
                "end_export_vah": "00",
                "net_metering_flag": net_metering_flag,  # Use the flag from CSV
                "max_demand": max_demand
            }

            # Post the request
            response = post_energy_record(url, payload)

            # Check the response status
            if response.status_code == 200 or response.status_code == 201:
                message = f"Record for {record['account_id']} on {start_daily_datetime} successfully sent.\n"
            else:
                message = f"Failed to send record for {record['account_id']} on {start_daily_datetime}. Status Code: {response.status_code}\n"
                message += f"Response: {response.text}\n"

            # Display the message in the text area
            output_text.insert(tk.END, message)
            output_text.see(tk.END)

            # Update previous end_import_wh
            start_import_wh_previous = end_import_wh

            # Increment the date
            current_date += timedelta(days=1)

            time.sleep(2)

# Set up the GUI
root = tk.Tk()
root.title("Enerygy Consumption for KW")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Button to select CSV file and process records
select_button = tk.Button(frame, text="Select CSV File and Process Records", command=process_records)
select_button.pack(pady=10)

# ScrolledText widget to display the output
output_text = scrolledtext.ScrolledText(frame, width=80, height=20, wrap=tk.WORD)
output_text.pack(padx=10, pady=10)

root.mainloop()
