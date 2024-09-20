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

# Function to read the meter number from the CSV file
def get_meter_number_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        # Assuming we need the first row's meter number
        for row in reader:
            return row.get('meter_number')  # Replace 'meter_number' with the actual column name


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
    WebDriverWait(driver, 20).until(
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

    # Step 9: Click on the filter SVG element using JavaScript
    print("Clicking on the filter button...")
    try:
        filter_svg_xpath = '//*[@id="filter_table"]'
        
        filter_svg = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, filter_svg_xpath))
        )
        print("Filter SVG element found.")
        
        # Click the element using Selenium's click method
        filter_svg.click()
        print("Clicked on the filter button.")
    except Exception as e:
        print(f"Error finding or clicking the filter SVG element: {e}")
        driver.quit()
        raise

    # Step 10: Select the meter type radio button
    print("Selecting meter type...")
    meter_radio_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'asset_meter'))
    )
    meter_radio_button.click()

    # Step 11: Read the meter number from the CSV file
    csv_file_path = 'data.csv'  # Replace with the path to your CSV file
    meter_number = get_meter_number_from_csv(csv_file_path)
    if meter_number:
        print(f"Filling in meter number: {meter_number}")

        # Step 12: Fill in the meter number form
        meter_number_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'textInput'))
        )
        meter_number_field.send_keys(meter_number)

        # Step 13: Click the "Apply" button
        print("Clicking the Apply button...")
        apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'submit-form'))
        )
        apply_button.click()

        

    print("Process completed.")

finally:
    # Step 16: Close the browser
    driver.quit()
