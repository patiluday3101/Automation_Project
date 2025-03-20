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
driver.get("https://consumer.uppcl.org/wss/auth/login")

wait = WebDriverWait(driver, 10)  


dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select")))
dropdown.click()
time.sleep(1)
district = "Mathura"
number=['3774132383']
password1="Buildint@123"

option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{district}')]")))
option.click()


# Enter login details
accountid = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
accountid.send_keys(number)

password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys(password1)

# Solve CAPTCHA
max_attempts = 5
attempt = 0
captcha_solved = False

while attempt < max_attempts and not captcha_solved:
    attempt += 1
    print(f"Attempt {attempt} to solve CAPTCHA")

    captcha_element = wait.until(EC.presence_of_element_located((By.ID, "captcha")))
    captcha_element.screenshot("captcha.png")

    image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
    _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    captcha_text = pytesseract.image_to_string(image, config='--psm 6').strip().replace("=", "").replace("?", "")
    captcha_text = re.sub(r'[^0-9+\-*/()]', '', captcha_text)

    print("Extracted CAPTCHA:", captcha_text)

    try:
        captcha_result = eval(captcha_text)
    except:
        captcha_result = ""

    print("Solved CAPTCHA:", captcha_result)

    captcha_input = wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
    captcha_input.clear()
    captcha_input.send_keys(str(captcha_result))

    button = driver.find_element(By.ID, "btnSubmit")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", button)

    time.sleep(3)
    if "captchaInput" not in driver.page_source:
        captcha_solved = True
    else:
        print("Incorrect CAPTCHA, retrying...")

if not captcha_solved:
    print("Failed to solve CAPTCHA after multiple attempts. Exiting.")
    driver.quit()
    exit()

time.sleep(3)

bill_history_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Bill Payment History')]")))
driver.execute_script("arguments[0].click();", bill_history_tab)

pdf_icon = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fa-file-pdf")))
driver.execute_script("arguments[0].click();", pdf_icon)
time.sleep(3)
driver.quit()