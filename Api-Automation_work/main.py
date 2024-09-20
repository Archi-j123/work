import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

# Import the real_time_balance_enquiry module
import prepaid_recharge_sync
import real_time_balance_enquiry

# Function to run a Python script and return its output
def run_script(script_func, result_text, *args):
    try:
        result = script_func(*args)  # Call the function and get the output

        # Display output in the text area
        result_text.insert(tk.END, "Running script\n")
        
        # Update the text color based on success or failure
        result_text.tag_configure("PASS", foreground="green")
        result_text.tag_configure("FAIL", foreground="red")
        result_text.tag_configure("ERROR", foreground="red")

        # Filter and color-code the relevant output lines
        for line in result.splitlines():
            if "PASS" in line:
                result_text.insert(tk.END, line + '\n', "PASS")
            elif "FAIL" in line:
                result_text.insert(tk.END, line + '\n', "FAIL")
            elif "ERROR" in line:
                result_text.insert(tk.END, line + '\n', "ERROR")
            else:
                result_text.insert(tk.END, line + '\n')

        result_text.insert(tk.END, "\n\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error running script: {str(e)}\n", "ERROR")

# Functions to run specific scripts
def run_real_time_balance_enquiry():
    # result_text.delete(1.0, tk.END)
    run_script(real_time_balance_enquiry.check_account_ids, result_text, 'real_time_balance_enquiry_data.csv')

def run_prepaid_recharge_sync():
    # result_text.delete(1.0, tk.END)
    # Call the process_test_results function from prepaid_recharge_sync
    run_script(prepaid_recharge_sync.process_test_results, result_text, 'prepaid_recharge_data.csv')

def run_both_scripts():
    result_text.delete(1.0, tk.END)
    run_prepaid_recharge_sync()
    run_real_time_balance_enquiry()


# Creating the main window
root = tk.Tk()
root.title("API Testing")

# Creating buttons
btn_both = tk.Button(root, text="All Scripts", command=run_both_scripts)
btn_prepaid = tk.Button(root, text="Run Prepaid Recharge Sync", command=run_prepaid_recharge_sync)
btn_balance = tk.Button(root, text="Run Real-Time Balance Enquiry", command=run_real_time_balance_enquiry)

# Positioning buttons on the left
btn_both.grid(row=2, column=0, padx=10, pady=10, sticky="w")
btn_prepaid.grid(row=0, column=0, padx=10, pady=10, sticky="w")
btn_balance.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Creating a text area to display results on the right
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
result_text.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

# Configuring grid to make the result area expandable
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Starting the GUI event loop
root.mainloop()
