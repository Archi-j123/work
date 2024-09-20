import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/main'))
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

    # Step 9: Click on the filter SVG element
    print("Clicking on the filter button...")
    filter_svg = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//svg[@id="filter_table"]'))
    )
    filter_svg.click()

    print("Clicking process completed...")

    # Optional: Add additional wait time if necessary to ensure the filter is applied and data is updated
    time.sleep(2)

finally:
    # Step 10: Close the browser
    driver.quit()
