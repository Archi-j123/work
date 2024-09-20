import tkinter as tk
from tkinter import scrolledtext

# Import the modules
import get_cousumer_prepaid_ledger
import get_recharge_history_new
import get_recharge_history
import get_wallet_details

# Store the results in a list
results = []

# Function to run a Python script and return its output
def run_script(script_func, result_text, *args):
    global results
    try:
        result = script_func(*args)  # Call the function and get the output

        # Clear previous results
        result_text.delete(1.0, tk.END)

        # Display output in the text area
        result_text.insert(tk.END, "Running script\n")
        
        # Update the text color based on success or failure
        result_text.tag_configure("PASS", foreground="green")
        result_text.tag_configure("FAIL", foreground="red")
        result_text.tag_configure("ERROR", foreground="red")

        # Store results in the global list
        results = []

        # Filter and color-code the relevant output lines
        for line in result.splitlines():
            if "PASS" in line:
                result_text.insert(tk.END, line + '\n', "PASS")
                results.append((line, "PASS"))
            elif "FAIL" in line:
                result_text.insert(tk.END, line + '\n', "FAIL")
                results.append((line, "FAIL"))
            elif "ERROR" in line:
                result_text.insert(tk.END, line + '\n', "ERROR")
                results.append((line, "ERROR"))
            else:
                result_text.insert(tk.END, line + '\n')
                results.append((line, None))

        result_text.insert(tk.END, "\n\n")

        # Print the same result to the terminal
        for line, status in results:
            print(line)

    except Exception as e:
        result_text.insert(tk.END, f"Error running script: {str(e)}\n", "ERROR")
        print(f"Error running script: {str(e)}")

# Functions to run specific scripts
def run_get_wallet_details():
    run_script(get_wallet_details.process_test_results1, result_text, 'user_input\\get_wallet_details.csv')

def run_get_recharge_history():
    run_script(get_recharge_history.process_test_results_to_csv, result_text, 'user_input\\get_recharge_history.csv')

def run_get_recharge_history_new():
    run_script(get_recharge_history_new.process_test_results3, result_text, 'get_wallet_details.csv')

def run_get_cousumer_prepaid_ledger():
    run_script(get_cousumer_prepaid_ledger.process_test_results4, result_text, 'user_input\\get_cousumer_prepaid_ledger.csv')

def run_both_scripts():
    result_text.delete(1.0, tk.END)
    run_get_recharge_history()
    run_get_wallet_details()
    run_get_recharge_history_new()
    run_get_cousumer_prepaid_ledger()

# Creating the main window
root = tk.Tk()
root.title("API Testing")

# Creating buttons with unique variable names
btn_all = tk.Button(root, text="All Scripts", command=run_both_scripts)
btn_recharge_history = tk.Button(root, text="Run get recharge history", command=run_get_recharge_history)
btn_wallet_details = tk.Button(root, text="Run get wallet details", command=run_get_wallet_details)
btn_cousumer_prepaid_ledger = tk.Button(root, text="Run get cousumer prepaid ledger", command=run_get_cousumer_prepaid_ledger)
btn_recharge_history_new = tk.Button(root, text="Run get recharge history new", command=run_get_recharge_history_new)

# Removing filter buttons
# btn_passed = tk.Button(root, text="Show Passed Cases", command=show_passed_cases)
# btn_failed = tk.Button(root, text="Show Failed Cases", command=show_failed_cases)

# Positioning buttons on the left
btn_all.grid(row=6, column=0, padx=10, pady=10, sticky="w")
btn_recharge_history.grid(row=0, column=0, padx=10, pady=10, sticky="w")
btn_wallet_details.grid(row=1, column=0, padx=10, pady=10, sticky="w")
btn_cousumer_prepaid_ledger.grid(row=2, column=0, padx=10, pady=10, sticky="w")
btn_recharge_history_new.grid(row=3, column=0, padx=10, pady=10, sticky="w")

# Positioning filter buttons
# btn_passed.grid(row=4, column=0, padx=10, pady=10, sticky="w")
# btn_failed.grid(row=5, column=0, padx=10, pady=10, sticky="w")

# Creating a text area to display results on the right
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
result_text.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

# Configuring grid to make the result area expandable
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Starting the GUI event loop
root.mainloop()
