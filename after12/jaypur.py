# import os
# import json
# import time
# import re
# import cv2
# import pdfplumber
# import pytesseract
# import glob
# import shutil
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
# driver.get("https://www.bijlimitra.com/custumerLoginPage")
# time.sleep(2)

# driver.find_element(By.ID, "urLoginName").send_keys("cbmssmfg")
# driver.find_element(By.ID, "password").send_keys("Buildint@123")

# captcha_element = driver.find_element(By.ID, "mainCaptcha")
# captcha_element.screenshot("captcha.png")

# image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
# _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 

# captcha_text = pytesseract.image_to_string(thresh, config='--psm 8').strip()
# captcha_text = ''.join(filter(str.isalnum, captcha_text))  

# driver.find_element(By.ID, "txtInput").send_keys(captcha_text)

# driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

# dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-selection")))
# dropdown.click()

# # Select the option containing "211541014472"
# option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and contains(text(),'211541014472')]")))
# option.click()

# time.sleep(5)
# driver.quit()
import os
import time
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Selenium Options
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd(),
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # Open URL
    driver.get("https://www.bijlimitra.com/custumerLoginPage")
    time.sleep(2)

    # Enter login credentials
    driver.find_element(By.ID, "urLoginName").send_keys("cbmssmfg")
    driver.find_element(By.ID, "password").send_keys("Buildint@123")

    # Solve CAPTCHA
    captcha_element = driver.find_element(By.ID, "mainCaptcha")
    captcha_element.screenshot("captcha.png")

    image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    captcha_text = pytesseract.image_to_string(thresh, config='--psm 6').strip()
    captcha_text = ''.join(filter(str.isalnum, captcha_text))

    driver.find_element(By.ID, "txtInput").send_keys(captcha_text)
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(3)

    # Validate Login
    try:
        error_msg = driver.find_element(By.ID, "error-message")  # Update with actual error element
        print("Login failed due to incorrect CAPTCHA.")
        driver.quit()
        exit()
    except NoSuchElementException:
        print("Login successful!")

    # Select Consumer Number
    consumer_number = "211722039527"
    select_element = wait.until(EC.presence_of_element_located((By.ID, "knumber")))
    select = Select(select_element)
    
    found = False
    for option in select.options:
        if consumer_number in option.text:
            select.select_by_visible_text(option.text)
            found = True
            break
    
    if not found:
        print("Consumer number not found.")
        driver.quit()
        exit()
    
    # Click Download Button
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Download Latest Bill')]")))
    download_button.click()
    time.sleep(5)  # Wait for download
    
    print("Bill downloaded successfully.")

except TimeoutException:
    print("Error: Timeout occurred while interacting with the website.")

finally:
    driver.quit()


