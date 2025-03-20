import os
import re
import time
import json
import cv2
import numpy as np
import pdfplumber
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

def extract_bill_details(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
    bill_date = extract_value(text, r"Bill Date[:\s]*(\d{2}/\d{2}/\d{4})")
    bill_details = {
        "Bill Date": bill_date,
        "Due Date": extract_value(text, r"Due Date[:\s]*(\d{2}/\d{2}/\d{4})"),
        "Due Amount": extract_value(text, r"Total Amount Payable[:\s]Rs\.\s([\d,]+\.\d{2})"),
        "Penalty": extract_penalty_or_delay(text, "Penalty"),
        "Contracted Demand": extract_value(text, r"Contract Demand[:\s]*(\d+\.\d+)") + " KW",
        "Total KWh Consumption": extract_kwh_consumption(text),
        "Delay Amount": extract_penalty_or_delay(text, "Delay Amount"),
        "Net Current Payment after Rebate": extract_value(text, r"Net Current Payment after Rebate[:\s]Rs\.\s([\d,]+\.\d{2})")
    }
    return bill_date, bill_details

def extract_value(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else "Not Found"

def extract_kwh_consumption(text):
    match = re.search(r"KWH\s+(\d{1,3}[,\d]\.\d+)\s+(\d{1,3}[,\d]\.\d+)\s+(\d{1,3}[,\d]\.\d+)\s+(\d{1,3}[,\d]\.\d+)\s+(\d{1,3}[,\d]\.\d+)\s+(\d{1,3}[,\d]\.\d+)", text)
    return f"{match.group(4).replace(',', '')} KWh" if match else "Not Found"

def extract_penalty_or_delay(text, label):
    match = re.search(fr"{label}[:\s]Rs\.\s([\d,]+\.\d{2})", text)
    return match.group(1) if match else "0.00"

def download_bill(consumer_no, mobile_no):
    driver = webdriver.Chrome()
    driver.get("https://www.tpcentralodisha.com/customer-zone/bill-payment/energy-bill.aspx")
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.presence_of_element_located((By.ID, "txtCANo"))).send_keys(consumer_no)
    wait.until(EC.presence_of_element_located((By.ID, "txtMobile"))).send_keys(mobile_no)
    
    captcha_solved = False
    attempts = 0
    while not captcha_solved and attempts < 5:
        attempts += 1
        captcha_element = wait.until(EC.presence_of_element_located((By.ID, "Img")))
        captcha_element.screenshot("captcha.png")
        
        image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
        _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        captcha_text = pytesseract.image_to_string(image, config='--psm 6').strip()
        captcha_text = re.sub(r'[^0-9+\-*/()]', '', captcha_text)
        
        try:
            captcha_result = eval(captcha_text)
        except:
            captcha_result = ""
        
        captcha_input = wait.until(EC.presence_of_element_located((By.ID, "TxtImgVer")))
        captcha_input.clear()
        captcha_input.send_keys(str(captcha_result))
        driver.find_element(By.ID, "btnSave").click()
        time.sleep(3)
        
        if not driver.find_elements(By.XPATH, "//*[contains(text(),'Invalid Captcha')]"):
            captcha_solved = True
    
    if not captcha_solved:
        driver.quit()
        return None
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Pay Now']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-custom') and @onclick='weekPay()']"))).click()
    latest_bill_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#' and @onclick='eBill()']")))
    latest_bill_link.click()
    
    time.sleep(5)
    driver.quit()
    return "downloaded_bill.pdf"

def process_bill(consumer_no, mobile_no):
    output_folder = "TPCODL"
    os.makedirs(output_folder, exist_ok=True)
    pdf_path = download_bill(consumer_no, mobile_no)
    if pdf_path:
        bill_date, bill_details = extract_bill_details(pdf_path)
        new_pdf_name = f"{consumer_no}_{bill_date.replace('/', '-')}.pdf"
        new_pdf_path = os.path.join(output_folder, new_pdf_name)
        os.rename(pdf_path, new_pdf_path)
        
        json_filename = f"{consumer_no}_{bill_date.replace('/', '-')}.json"
        json_path = os.path.join(output_folder, json_filename)
        
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(bill_details, json_file, indent=4)
        
        print(f"Bill saved as: {new_pdf_path}")
        print(f"Extracted details saved to: {json_path}")

if __name__ == "__main__":
    CONSUMER_NUMBER = "80004265270"
    MOBILE_NUMBER = "7400074047"
    process_bill(CONSUMER_NUMBER, MOBILE_NUMBER)