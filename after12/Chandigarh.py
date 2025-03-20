import time
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import base64

options = Options()
options.headless = True  
driver = webdriver.Chrome(options=options)

def preprocess_captcha(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
    img = cv2.GaussianBlur(img, (3, 3), 0) 
    return img

def solve_captcha(image_path):
    img = preprocess_captcha(image_path)
    return pytesseract.image_to_string(img, config="--psm 7").strip()

def login_with_captcha():
    driver.get("https://sampark.chd.nic.in/Epayment/NonStaticPages/BillView.aspx")
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtAccountNo"))).send_keys("084881421WQ")
    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtMeterNo"))).send_keys("CHEP1089")
    
    for _ in range(3):  
        captcha_element = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ImgCaptcha")))
        captcha_element.screenshot("captcha.png")
        captcha_text = solve_captcha("captcha.png")

        if captcha_text:
            print("Using CAPTCHA text:", captcha_text)
            captcha_input = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtCaptcha")))
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)

            # Click Submit
            wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnShow"))).click()
            time.sleep(2)  # Allow page to load

            # Check if CAPTCHA was successful
            if "Invalid captcha" not in driver.page_source:
                print("Login successful!")
                return True
        print("Retrying CAPTCHA...")
        driver.refresh()  
        time.sleep(2)
    
    print("Failed to solve CAPTCHA.")
    return False



# Run login attempt
success = login_with_captcha()
driver.quit()

if success:
    print("Proceeding with data extraction...")
else:
    print("Login failed due to CAPTCHA issues.")
