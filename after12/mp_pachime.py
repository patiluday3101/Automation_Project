from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

consumer_numbers = ["N3688000173"]  

driver = webdriver.Chrome()

def process_consumer(consumer_number):
    driver.get("https://mpwzservices.mpwin.co.in/westdiscom/home")
    time.sleep(2)
    
    ivrs_input = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='ivrs']")
    ivrs_input.send_keys(consumer_number)  

    button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='View & Pay Energy Bill']")
    button.click()
    time.sleep(5)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View Full Bill (English)')]"))
    )
    button.click()
    time.sleep(5)  

for consumer in consumer_numbers:
    process_consumer(consumer)

driver.quit()
