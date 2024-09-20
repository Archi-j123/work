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



finally:
    # Step 18: Close the browser
    time.sleep(5)
    driver.quit()
