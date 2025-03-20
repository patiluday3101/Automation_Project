import os
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

consumer_numbers = ["402209888"]
installation_numbers = ["21761523"]

driver = webdriver.Chrome()
driver.implicitly_wait(10)  # Allow elements to load

def process_consumer(consumer_number, installation_number):
    driver.get("https://portal.wbsedcl.in/irj/go/km/docs/bills/IFRAME/ViewBillWithoutLogin.html")

    # Wait for the page to load and check if there's an iframe
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)  # Switch to iframe if found
    except:
        print("No iframe detected, proceeding normally.")

    try:
        # Wait until input fields are available
        consumer_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BIEI.WBViewBillWLCompView.InputField"))
        )
        consumer_input.send_keys(consumer_number)

        installation_input = driver.find_element(By.ID, "BIEI.WBViewBillWLCompView.InputField1")
        installation_input.send_keys(installation_number)

        # Capture and Process CAPTCHA
        captcha_element = driver.find_element(By.ID, "BIEI.WBViewBillWLCompView.Image2")
        captcha_element.screenshot("captcha.png")

        image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
        captcha_text = pytesseract.image_to_string(image, config="--psm 7").strip()

        if not captcha_text:
            print("CAPTCHA recognition failed. Try manual input.")
            return

        # Enter CAPTCHA
        captcha_input = driver.find_element(By.ID, "BIEI.WBViewBillWLCompView.InputField2")
        captcha_input.send_keys(captcha_text)

        # Submit Form
        submit_button = driver.find_element(By.ID, "BIEI.WBViewBillWLCompView.Button")
        submit_button.click()

        # Wait for PDF button to be clickable
        try:
            pdf_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "BIEI.WBViewBillWLCompView.Image3.0"))
            )
            pdf_button.click()
            print(f"PDF downloaded for Consumer: {consumer_number}")
        except:
            print(f"Failed to download PDF for Consumer: {consumer_number}")

    except Exception as e:
        print(f"Error processing {consumer_number}: {e}")

for consumer, installation in zip(consumer_numbers, installation_numbers):
    process_consumer(consumer, installation)

driver.quit()
