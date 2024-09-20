import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Function to read meter number and command name from CSV file
def get_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('meter_number'), row.get('command_name')  # Replace with actual column names

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
    for meter_number, command_name in get_meter_data_from_csv('profile.csv'):
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

        time.sleep(5)

        # Step 12: Click the search button
        print("Clicking on the search button...")
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/form/div/button'))
        )
        search_button.click()

        time.sleep(5)

        # Step 13: Click the next button
        print("Clicking on the next button...")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="meter-next"]'))
        )
        next_button.click()

        time.sleep(10)
        
        print("Clicking on select button button...")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]'))
        )
        next_button.click()

        # Step 14: Enter the command from the CSV file and press Enter
        print(f"Entering command: {command_name}")
        command_input = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/input'))
        )
        command_input.clear()
        command_input.send_keys(command_name)
        command_input.send_keys(Keys.RETURN)

        time.sleep(5)

        # Step 16: Click the apply button
        print("Clicking on the apply button...")
        apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="meter-cmd-apply"]'))
        )
        apply_button.click()

        print(f"Meter number {meter_number} processed successfully.")
        time.sleep(5)

        # Step 17: Click on the filter SVG element using JavaScript
        print("Clicking on the filter button...")
        try:
            filter_svg_xpath = '//*[@id="filter_table"]'
            filter_svg = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, filter_svg_xpath))
            )
            filter_svg.click()
        except Exception as e:
            print(f"Error clicking filter SVG element: {e}")
            driver.quit()
            raise

        # Step 18: Select the meter type radio button
        print("Selecting meter type...")
        meter_radio_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'asset_meter'))
        )
        meter_radio_button.click()

        # Step 19: Enter the meter number after the filter
        print(f"Entering meter number after filter: {meter_number}")
        meter_number_input_xpath = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div[2]/input'
        meter_number_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, meter_number_input_xpath))
        )
        meter_number_input.clear()
        meter_number_input.send_keys(meter_number)

        # Step 20: Enter the command after filter
        print(f"Entering command after filter: {command_name}")
        command_input_xpath = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div[3]/div/div/div[1]/div[2]/input'
        command_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, command_input_xpath))
        )
        command_input.clear()
        command_input.send_keys(command_name)
        command_input.send_keys(Keys.RETURN)

        # Step 21: Click the "Apply" button after filter
        print("Clicking the Apply button...")
        apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'submit-form'))
        )
        apply_button.click()

        time.sleep(5)

        # Step 22: Click the refresh button multiple times
        for i in range(1, 9):
            print(f"Clicking the refresh button {i}...")
            refresh_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'refresh_table'))
            )
            refresh_button.click()
            time.sleep(5)

        # Step 23: Click the download button
        print("Clicking the download button...")
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'Download'))
        )
        download_button.click()

        # Step 24: Click the CSV button to download the table data
        print("Clicking the CSV button...")
        csv_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/div/div/button[1]'))
        )
        csv_button.click()

        # Rename the downloaded file to include today's date
        today_date = datetime.today().strftime('%d-%m-%Y')
        new_file_name = f"{today_date}.csv"
        print(f"Downloaded file renamed to {new_file_name}")

        print(f"Process completed for meter number {meter_number}")
        time.sleep(5)

finally:
    print("Closing browser...")
    driver.quit()
