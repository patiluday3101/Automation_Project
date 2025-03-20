from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chromedriver_path = "C:\Windows\chromedriver.exe"

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://services.mpcz.in/Consumer/#/ViewPayBillApp/bill-Payment")

wait = WebDriverWait(driver, 10)

ivrs_number = "2433005820"

ivrs_input = wait.until(EC.presence_of_element_located((By.NAME, "idNumber")))
ivrs_input.send_keys(ivrs_number)

submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Submit']")))
submit_button.click()
time.sleep(5)

# Scroll down to make the "English" button visible
driver.execute_script("window.scrollBy(0, 500);")

# Wait for the "English" button to be clickable
english_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' English ']")))

# Click the "English" button
english_button.click()

# Wait for some time (Adjust if needed)
time.sleep(3)
driver.quit()
