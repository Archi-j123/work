from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open the website (replace with your actual URL)
driver.get('https://avdhaan-new.gomatimvvnl.in/#/utility/uppcl/hes')

# Wait until the table is loaded
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rdt_Table')))

# Locate the rows in the table body
rows = table.find_elements(By.CLASS_NAME, 'rdt_TableRow')

# Iterate over each row and extract the desired data
for row in rows:
    sr_no = row.find_element(By.CSS_SELECTOR, '[data-column-id="1"]').text
    meter_number = row.find_element(By.CSS_SELECTOR, '[data-column-id="2"]').text
    start_time = row.find_element(By.CSS_SELECTOR, '[data-column-id="3"]').text
    response_time = row.find_element(By.CSS_SELECTOR, '[data-column-id="4"]').text
    command_name = row.find_element(By.CSS_SELECTOR, '[data-column-id="5"]').text
    updated_at = row.find_element(By.CSS_SELECTOR, '[data-column-id="6"]').text
    status = row.find_element(By.CSS_SELECTOR, '[data-column-id="7"]').text
    command_params = row.find_element(By.CSS_SELECTOR, '[data-column-id="8"]').text
    username = row.find_element(By.CSS_SELECTOR, '[data-column-id="9"]').text

    # Print the extracted data
    print(f'Sr No: {sr_no}, Meter Number: {meter_number}, Start Time: {start_time}, Response Time: {response_time}')
    print(f'Command Name: {command_name}, Updated At: {updated_at}, Status: {status}, Command Params: {command_params}')
    print(f'Username: {username}')
    print('-' * 50)

# Close the WebDriver
driver.quit()
