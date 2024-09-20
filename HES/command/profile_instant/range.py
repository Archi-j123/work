import pandas as pd
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Function to read meter number, command name, and range from CSV file
def get_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('meter_number'), row.get('command_name'), row.get('aria_min'), row.get('aria_now')

# Function to update slider value using ActionChains to move the slider
def update_slider_value(driver, aria_min, aria_now):
    # Locate the slider handle element
    slider_handle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "noUi-handle-upper"))
    )
    
    # Get the current position of the slider
    initial_position = slider_handle.get_attribute('aria-valuenow')
    
    # Calculate the offset based on the difference between current and target aria_now
    offset = float(aria_now) - float(initial_position)
    
    # Use ActionChains to click and drag the slider handle
    action = ActionChains(driver)
    action.click_and_hold(slider_handle).move_by_offset(offset, 0).release().perform()
    
    print(f"Slider moved to aria-valuenow: {aria_now}")
    
    # Optionally, verify the updated value
    updated_value = slider_handle.get_attribute('aria-valuenow')
    if updated_value == aria_now:
        print(f"Slider value updated successfully to {updated_value}")
    else:
        print(f"Failed to update slider. Current value is {updated_value}")

# Setup WebDriver with ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Step 1: Open the website
    driver.get('https://avdhaan-new.gomatimvvnl.in/')

    # Step 2: Wait for the login page elements to load
    print("Waiting for login page...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Step 3: Enter the user ID
    print("Entering username...")
    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys('krishankantyadav@polarisgrids.com')

    # Step 4: Enter the password
    print("Entering password...")
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('Krish2002@')

    # Step 5: Submit the form
    print("Submitting login form...")
    password_field.send_keys(Keys.RETURN)

    # Step 6: Wait for the MDMS page to load after login
    print("Waiting for MDMS page to load...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
    )
    print("MDMS page loaded successfully")

    # Step 7: Navigate to the HES page
    print("Navigating to the HES page...")
    driver.get('https://avdhaan-new.gomatimvvnl.in/#/utility/uppcl/hes')

    # Step 8: Wait for the HES page to load
    print("Waiting for the HES page to load...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
    )
    print("HES page loaded successfully")

    # Loop through each row in the CSV file
    for meter_number, command_name, aria_min, aria_now in get_meter_data_from_csv('range1.csv'):
        # Step 9: Click the dropdown button
        print("Clicking on the dropdown button...")
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[2]'))
        )
        dropdown_button.click()

        # Step 10: Click the meter option from the dropdown
        print("Clicking on the meter option...")
        meter_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]/a'))
        )
        meter_option.click()

        # Step 11: Enter the meter number from the CSV file
        print(f"Entering meter number: {meter_number}")
        meter_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/form/div/input'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", meter_input)
        meter_input.clear()
        meter_input.send_keys(meter_number)

        # Step 12: Click the search button
        print("Clicking on the search button...")
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/form/div/button'))
        )
        search_button.click()

        # Add a 5-second delay to ensure the search result is processed
        time.sleep(5)
        
        # Step 13: Click the next button
        print("Clicking on the next button...")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="meter-next"]'))  # Use the ID without the # symbol
        )
        next_button.click()

        # Step 14: Enter the command from CSV and press Enter
        print(f"Entering command: {command_name}")
        command_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/input'))
        )
        command_input.clear()
        command_input.send_keys(command_name)
        command_input.send_keys(Keys.RETURN)

        # Step 15: Wait for 5 seconds before applying the command
        time.sleep(5)

        # Step 16: Update slider aria values using ActionChains
        print(f"Updating slider with aria-min={aria_min} and aria-now={aria_now}")
        update_slider_value(driver, aria_min, aria_now)
        
        time.sleep(10)

        # Step 17: Click the apply button
        print("Clicking on the apply button...")
        apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="meter-cmd-apply"]'))
        )
        apply_button.click()

        # Add a small delay before moving to the next row
        print(f"Meter number {meter_number} processed successfully with range {aria_min}-{aria_now}.")
        time.sleep(10)

finally:
    time.sleep(10)
    driver.quit()
