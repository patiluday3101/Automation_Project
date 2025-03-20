import os
import json
import time
import re
import cv2
import pdfplumber
import pytesseract
import glob
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create folder for storing bills
folder_name = "UP_bills"
os.makedirs(folder_name, exist_ok=True)

driver = webdriver.Chrome()
driver.get("https://consumer.uppcl.org/wss/auth/login")

wait = WebDriverWait(driver, 10)

dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select")))
dropdown.click()
time.sleep(1)
# "Mathura"
district = "Mathura"
consumer_numbers = ["3774132383"]  
password = "Buildint@123"

option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{district}')]")))
option.click()

def get_latest_downloaded_pdf(download_path):
    time.sleep(3)  # Ensure file is downloaded
    pdf_files = glob.glob(os.path.join(download_path, "*.pdf"))
    if not pdf_files:
        return None
    return max(pdf_files, key=os.path.getctime)

for number in consumer_numbers:
    # Enter login details
    accountid = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
    accountid.send_keys(number)
    
    password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys(password)

    # Solve CAPTCHA
    max_attempts = 5
    captcha_solved = False
    
    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1} to solve CAPTCHA")
        captcha_element = wait.until(EC.presence_of_element_located((By.ID, "captcha")))
        captcha_element.screenshot("captcha.png")

        image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
        _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        captcha_text = pytesseract.image_to_string(image, config='--psm 6').strip().replace("=", "").replace("?", "")
        captcha_text = re.sub(r'[^0-9+\-*/()]', '', captcha_text)

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
            break
        else:
            print("Incorrect CAPTCHA, retrying...")

    if not captcha_solved:
        print("Failed to solve CAPTCHA. Skipping consumer number", number)
        continue

    # Navigate to bill history and download bill
    time.sleep(3)
    bill_history_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Bill Payment History')]")))
    driver.execute_script("arguments[0].click();", bill_history_tab)

    pdf_icon = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fa-file-pdf")))
    driver.execute_script("arguments[0].click();", pdf_icon)
    
    download_folder = os.path.expanduser("~/Downloads")
    latest_pdf = get_latest_downloaded_pdf(download_folder)

    if not latest_pdf:
        print(f"Bill PDF not found for Consumer No: {number}")
        continue
    
    # Extract info from the bill
    with pdfplumber.open(latest_pdf) as pdf:
        pdf_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    patterns = {
        "Consumer Number": r"Account No\.: (\d+)",
        "Bill Number": r"Bill Number : (\d+)",
        "Bill Date": r"Bill Date (\d{2}-[A-Z]{3}-\d{4})",
        "Due Date": r"Due Date (\d{2}-[A-Z]{3}-\d{4})",
        "Sanction Load": r"Sanction Load : ([\d.]+) kW",
        "Penalty Amount": r"Excess Demand Penalty\s+([\d.]+)",
        "Payable Amount": r"Payable Amount\s+([\d,]+)",
        # "Total Consumption": r"GOE[A-Z0-9]+\s+KWH\s+A\s+\d+\s+\d+\s+\d+\s+(\d+)"
    }

    extracted_details = {key: re.search(pattern, pdf_text).group(1) if re.search(pattern, pdf_text) else "Not Found" for key, pattern in patterns.items()}
    
    # Extract Bill Date for filename
    bill_date_match = re.search(patterns["Bill Date"], pdf_text)
    bill_date = bill_date_match.group(1) if bill_date_match else "UnknownDate"
    bill_date = bill_date.replace("-", "-")  # Remove dashes for filename compatibility

    # Construct new filename
    pdf_filename = f"{number}_{bill_date}.pdf"
    pdf_path = os.path.join(folder_name, pdf_filename)

    # Rename downloaded PDF
    shutil.move(latest_pdf, pdf_path)  
    print(f"Saved as: {pdf_filename}")

    # Save extracted details to JSON
    extracted_details["File Name"] = pdf_filename
    json_path = os.path.join(folder_name, f"{number}_{bill_date}.json")

    with open(json_path, "w") as json_file:
        json.dump(extracted_details, json_file, indent=4)
    
    print(f"Bill and details saved for Consumer No: {number}")

driver.quit()
