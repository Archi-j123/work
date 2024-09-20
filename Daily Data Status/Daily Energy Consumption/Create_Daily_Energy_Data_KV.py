import requests
import csv
import random
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def fetch_parameters_from_csv(filename):
    parameters = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            parameters.append(row)
    return parameters

def generate_daily_consumption_kvah(min_val, max_val):
    return random.randint(min_val, max_val)

def post_energy_record(url, payload):
    response = requests.post(url, json=payload)
    return response

def select_csv_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return filename

def process_records():
    url = "https://engineweb.gomatimvvnl.in/daily_energy_consumption/"
    
    # Get CSV file from user
    csv_filename = select_csv_file()
    if not csv_filename:
        messagebox.showerror("Error", "No file selected. Exiting.")
        return

    # Fetch parameters from CSV
    records = fetch_parameters_from_csv(csv_filename)

    output_text = ""
    for record in records:
        # Convert dates
        try:
            start_date = datetime.strptime(record["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(record["end_date"], "%Y-%m-%d")
        except ValueError as e:
            output_text += f"Date format error in record {record['account_id']}: {e}\n"
            continue

        kvah_min = int(record.get("consumption_min", 0))
        kvah_max = int(record.get("consumption_max", 0))
        energy_consumption_export_kvah = int(record.get("energy_consumption_export_kvah", 0))
        
        # Initial parameters
        start_import_vah_previous = 0  # Initial value

        # Iterate through each day in the range
        current_date = start_date
        while current_date <= end_date:
            start_daily_datetime = current_date.strftime("%Y-%m-%dT%H:%M:%S")
            end_daily_datetime = (current_date + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

            # Generate daily consumption value in kVAh
            energy_consumption_kvah = generate_daily_consumption_kvah(kvah_min, kvah_max)
            start_import_vah = start_import_vah_previous
            end_import_vah = energy_consumption_kvah + start_import_vah

            # Define the payload
            payload = {
                "start_daily_datetime": start_daily_datetime,
                "end_daily_datetime": end_daily_datetime,
                "account_id": record["account_id"],
                "meter_number": record["meter_number"],
                "energy_consumption_kwh": "00",  
                "energy_consumption_kvah": energy_consumption_kvah,
                "energy_consumption_export_kwh": "00",
                "energy_consumption_export_kvah": energy_consumption_export_kvah,
                "start_import_wh": "00",  
                "end_import_wh": "00",    
                "start_import_vah": start_import_vah,
                "end_import_vah": end_import_vah,
                "start_export_wh": "00",
                "end_export_wh": "00",
                "start_export_vah": "00",
                "end_export_vah": "00",
                "net_metering_flag": record.get("net_metering_flag", "N"),  # Default to 'N' if missing
                "max_demand": record.get("max_demand", "00")  # Default to '00' if missing
            }

            # Post the request
            response = post_energy_record(url, payload)

            # Check the response status
            if response.status_code == 200 or response.status_code == 201:
                output_text += f"Record for {record['account_id']} on {start_daily_datetime} successfully sent.\n"
            else:
                output_text += f"Failed to send record for {record['account_id']} on {start_daily_datetime}. Status Code: {response.status_code}\n"
                output_text += response.text + "\n"  # Print the response for debugging

            # Update previous end_import_vah
            start_import_vah_previous = end_import_vah

            # Increment the date
            current_date += timedelta(days=1)

    # Display results in the output text area
    output_area.config(state=tk.NORMAL)
    output_area.delete(1.0, tk.END)
    output_area.insert(tk.END, output_text)
    output_area.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Enerygy Consumption for KV")

# Create and place widgets
select_button = tk.Button(root, text="Select CSV File", command=process_records)
select_button.pack(pady=10)

output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED)
output_area.pack(padx=10, pady=10)

# Run the application
root.mainloop()
