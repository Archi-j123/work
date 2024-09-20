import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Function to read meter number, command name, and status from CSV file
def get_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('meter_number'), row.get('command_name'), row.get('status')  # Replace with actual column names

# Base download directory
base_download_dir = r"C:\Users\krishankanty\Desktop\polaris\prince\data"

# Create a folder named with today's date
today_date = datetime.today().strftime('%d-%m-%Y')
dated_folder = os.path.join(base_download_dir, today_date)

# Ensure the folder for today's date exists
if not os.path.exists(dated_folder):
    os.makedirs(dated_folder)

# Set up the Chrome driver with download preferences
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": dated_folder,  # Set the default download directory to the dated folder
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Setup WebDriver with ChromeDriverManager
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Step 1: Open the website
    driver.get('https://avdhaan-new.gomatimvvnl.in/')

    # Step 2: Wait for the login page elements to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Step 3: Enter the user ID
    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys('krishankantyadav@polarisgrids.com')

    # Step 4: Enter the password
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('Krish2002@')

    # Step 5: Submit the form
    password_field.send_keys(Keys.RETURN)

    # Step 6: Wait for the MDMS page to load after login
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
    )

    # Step 7: Navigate to the HES page
    driver.get('https://avdhaan-new.gomatimvvnl.in/#/utility/uppcl/hes')

    # Step 8: Wait for the HES page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
    )

    # Loop through each row in the CSV file
    for meter_number, command_name, status in get_meter_data_from_csv('data.csv'):
        # Step 17: Click on the filter SVG element using JavaScript
        filter_svg_xpath = '//*[@id="filter_table"]'
        filter_svg = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, filter_svg_xpath))
        )
        filter_svg.click()

        # Step 18: Select the meter type radio button
        meter_radio_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'asset_meter'))
        )
        meter_radio_button.click()

        # Step 19: Enter the meter number after the filter
        meter_number_input_xpath = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div[2]/input'
        meter_number_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, meter_number_input_xpath))
        )
        meter_number_input.clear()
        meter_number_input.send_keys(meter_number)

        # Step 20: Enter the command after filter
        command_input_xpath = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div[3]/div/div/div[1]/div[2]/input'
        command_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, command_input_xpath))
        )
        command_input.clear()
        command_input.send_keys(command_name)

        # Step 21: Enter the status after filter
        status_input_xpath = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/div[2]/input'  # Update this XPath based on actual form
        status_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, status_input_xpath))
        )
        status_input.clear()
        status_input.send_keys(status)

        # Apply the filter
        command_input.send_keys(Keys.RETURN)

        # Step 22: Click the "Apply" button after filter
        apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'submit-form'))
        )
        apply_button.click()

        time.sleep(5)

        # Step 23: Click the refresh button multiple times
        for i in range(1, 2):
            refresh_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'refresh_table'))
            )
            refresh_button.click()
            time.sleep(3)
        
        # Step 24: Click the row button
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[10]'))
        )
        download_button.click()

        # Step 25: Click the download button
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'csv_download'))
        )
        download_button.click()

        # Wait for the file to download
        time.sleep(3)  # Increased time to ensure file is downloaded

        # Rename the downloaded file to include today's date and meter number
        csv_files = [f for f in os.listdir(dated_folder) if f.endswith(".csv")]

        if csv_files:
            downloaded_file = max(csv_files, key=lambda f: os.path.getctime(os.path.join(dated_folder, f)))
            new_file_name = f"{today_date}_{meter_number}.csv"
            new_file_path = os.path.join(dated_folder, new_file_name)
            os.rename(os.path.join(dated_folder, downloaded_file), new_file_path)
            print(f"Downloaded file renamed to {new_file_name}")
        else:
            print("No CSV files found for renaming.")

        # time.sleep(5)
        
        # Step 26: Click the CSV button
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/span/div/div/button[1]'))
        )
        download_button.click()

finally:
    time.sleep(10)
    driver.quit()
