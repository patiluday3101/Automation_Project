from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

driver = webdriver.Chrome()
driver.get("https://www.tpcentralodisha.com/customer-zone/bill-payment/energy-bill.aspx")
wait = WebDriverWait(driver, 10)  
CONSUMER_NUMBER = "80000651366"
MOBILE_NUMBER = "7400074047"

accountid = wait.until(EC.presence_of_element_located((By.ID, "txtCANo")))
accountid.send_keys(CONSUMER_NUMBER)

password_input = wait.until(EC.presence_of_element_located((By.ID, "txtMobile")))
password_input.send_keys(MOBILE_NUMBER)

max_attempts = 5
attempt = 0
captcha_solved = False

while attempt < max_attempts and not captcha_solved:
    attempt += 1
    print(f"Attempt {attempt} to solve CAPTCHA")

    captcha_element = wait.until(EC.presence_of_element_located((By.ID, "Img")))
    captcha_element.screenshot("captcha.png")

    image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    captcha_text = pytesseract.image_to_string(image, config='--psm 6').strip()
    captcha_text = re.sub(r'[^0-9+\-*/()]', '', captcha_text)

    print("Extracted CAPTCHA:", captcha_text)
    
    try:
        captcha_result = eval(captcha_text)
    except:
        captcha_result = ""
    
    print("Solved CAPTCHA:", captcha_result)

    captcha_input = wait.until(EC.presence_of_element_located((By.ID, "TxtImgVer")))
    captcha_input.clear()
    captcha_input.send_keys(str(captcha_result))

    button = driver.find_element(By.ID, "btnSave")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", button)

    time.sleep(3)
    error_message = driver.find_elements(By.XPATH, "//*[contains(text(),'Invalid Captcha')]" )
    if not error_message:
        captcha_solved = True
    else:
        print("Incorrect CAPTCHA, retrying...")

if not captcha_solved:
    print("Failed to solve CAPTCHA after multiple attempts. Exiting.")
    driver.quit()
    exit()

try:
    pay_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Pay Now']")))
    driver.execute_script("arguments[0].click();", pay_now_button)
    
    bill_download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-custom') and @onclick='weekPay()']")))
    driver.execute_script("arguments[0].click();", bill_download_button)
    
    latest_bill_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#' and @onclick='eBill()']")))
    latest_bill_link.click()
    
    print("Bill download initiated.")
    time.sleep(3)
except Exception as e:
    print("Error occurred during bill download:", str(e))
driver.quit()
