import os
import time
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import base64
consumer_numbers = ["31000369589"]  

driver = webdriver.Chrome()

def process_consumer(consumer_number):
    driver.get("https://www.cesc.co.in/viewPrintBill")
    time.sleep(2)
    
    consumer_input = driver.find_element(By.ID, "customer_id")
    consumer_input.send_keys(consumer_number)
    
    submit_button = driver.find_element(By.ID, "btn_bill")
    submit_button.click()
    
for consumer in consumer_numbers:
    process_consumer(consumer)

driver.quit()


