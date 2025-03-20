import os
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf2image import convert_from_path
import pytesseract

# Configuration
chromedriver_path = "C:\\Windows\\chromedriver.exe"
bills_folder = "APEPDCL"  # Folder to save PDFs and JSONs
os.makedirs(bills_folder, exist_ok=True)

# Function to extract text from PDF using OCR
def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = "".join(pytesseract.image_to_string(image) for image in images)
    return text

# Function to extract bill information
def extract_bill_info(pdf_path):
    bill_info = {
        "consumer_number": None,
        "bill_date": None,
        "due_date": None,
        "amount": None,
        "power_factor": None,
        "total_consumption": None
    }
    text = extract_text_with_ocr(pdf_path)
    
    # Regular expressions
    consumer_match = re.search(r"Unique Service Number\s*(\d+)", text, re.IGNORECASE)
    bill_date_match = re.search(r"Bill Date Due Date Disconnection Date\s*\n(\d{2}-[A-Za-z]{3}-\d{4}) (\d{2}-[A-Za-z]{3}-\d{4})", text, re.IGNORECASE)
    amount_match = re.search(r"Total Amount\s*([\d,]+\.\d{2})", text, re.IGNORECASE)
    power_factor_match = re.search(r"RMD\.\s*([\d\.]+)", text, re.IGNORECASE)
    consumption_match = re.search(r"Billed Units\s*(\d+)", text, re.IGNORECASE)
    
    # Extracted values
    if consumer_match:
        bill_info["consumer_number"] = consumer_match.group(1).strip()
    if bill_date_match:
        bill_info["bill_date"] = bill_date_match.group(1).strip()
        bill_info["due_date"] = bill_date_match.group(2).strip()
    if amount_match:
        bill_info["amount"] = float(amount_match.group(1).replace(",", ""))
    if power_factor_match:
        bill_info["power_factor"] = float(power_factor_match.group(1).strip())
    if consumption_match:
        bill_info["total_consumption"] = int(consumption_match.group(1).strip())
    
    return bill_info

def download_bill(consumer_number):
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.apeasternpower.com/viewBillDetailsMain")
    wait = WebDriverWait(driver, 10)
    
    phone_no = wait.until(EC.presence_of_element_located((By.ID, "ltscno")))
    phone_no.send_keys(consumer_number)
    
    captcha_text = wait.until(EC.presence_of_element_located((By.ID, "Billquestion"))).text.strip()
    captcha_text = captcha_text.replace("=", "").strip()
    try:
        captcha_answer = eval(captcha_text)
    except Exception as e:
        print("CAPTCHA Error:", e)
        driver.quit()
        return None
    
    captcha_input = wait.until(EC.presence_of_element_located((By.ID, "Billans")))  
    captcha_input.send_keys(str(captcha_answer))
    
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "Billsignin")))
    submit_button.click()
    
    bill_link_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Click Here')]")))
    bill_link_element.click()
    time.sleep(5)  
    driver.quit()
    

    download_dir = os.path.expanduser("~/Downloads")
    downloaded_files = sorted(os.listdir(download_dir), key=lambda f: os.path.getctime(os.path.join(download_dir, f)), reverse=True)
    for file in downloaded_files:
        if file.endswith(".pdf"):
            return os.path.join(download_dir, file)
    
    return None

def main(consumer_number):
    pdf_path = download_bill(consumer_number)
    if not pdf_path:
        print("Bill download failed!")
        return
    
    bill_info = extract_bill_info(pdf_path)
    if not bill_info["consumer_number"] or not bill_info["bill_date"]:
        print("Failed to extract bill info!")
        return
    

    new_filename = f"{bill_info['consumer_number']}_{bill_info['bill_date']}.pdf"
    new_pdf_path = os.path.join(bills_folder, new_filename)
    os.rename(pdf_path, new_pdf_path)
    

    json_filename = new_filename.replace(".pdf", ".json")
    json_path = os.path.join(bills_folder, json_filename)
    with open(json_path, "w") as json_file:
        json.dump(bill_info, json_file, indent=4)
    
    print(f"Bill saved: {new_pdf_path}")
    print(f"Info saved: {json_path}")

if __name__ == "__main__":
    consumer_no = "1433055105136360" #131102A200010307
    main(consumer_no)
