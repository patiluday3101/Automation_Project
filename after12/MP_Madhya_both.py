from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pdfplumber
import re
import json
import os

chromedriver_path = "C:\\Windows\\chromedriver.exe"
download_folder = "MP_Madhya_bills"  
ivrs_number = "2482001203"

if not os.path.exists(download_folder):
    os.makedirs(download_folder)


options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.abspath(download_folder),
    "plugins.always_open_pdf_externally": True, 
    "download.prompt_for_download": False
}
options.add_experimental_option("prefs", prefs)

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://services.mpcz.in/Consumer/#/ViewPayBillApp/bill-Payment")
wait = WebDriverWait(driver, 10)

ivrs_input = wait.until(EC.presence_of_element_located((By.NAME, "idNumber")))
ivrs_input.send_keys(ivrs_number)

# Click Submit Button
submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Submit']")))
submit_button.click()
time.sleep(5)

# Scroll down to ensure visibility
driver.execute_script("window.scrollBy(0, 500);")

english_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' English ']")))
english_button.click()
time.sleep(5)  # Adjust if needed

print("Waiting for the bill to be downloaded...")
time.sleep(10) 
driver.quit()

pdf_files = [f for f in os.listdir(download_folder) if f.endswith(".pdf")]
pdf_path = os.path.join(download_folder, pdf_files[0]) if pdf_files else None

if pdf_path:
    def extract_bill_details(pdf_path):
        details = {}
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    details['Consumer No'] = re.search(r'\b(\d{10})\b', text)
                    details['Bill Date'] = re.search(r'Bill Date\s*(\d{2}-[A-Za-z]+-\d{4}|\d{2}-[A-Za-z]+-\d{2,4})', text)
                    details['Due Date'] = re.search(r'Phase Given\s+SINGLE\s+(\d{2}-[A-Za-z]+-\d{4})', text)
                    details['Amount'] = re.search(r'CurrentMonthBill\s*(\d+\.\d+|\d+)', text)
                    details['Power Factor'] = re.search(r'\b423\.00\s+289\.00\s+1\s+(0\.\d{2})\b', text)
        return {key: match.group(1) if match else 'Not Found' for key, match in details.items()}
    
    details = extract_bill_details(pdf_path)
    consumer_no = details.get('Consumer No', ivrs_number)
    bill_date = details.get('Bill Date', 'Unknown').replace("-", "_")
    
    new_pdf_name = f"{consumer_no}_{bill_date}.pdf"
    new_pdf_path = os.path.join(download_folder, new_pdf_name)
    os.rename(pdf_path, new_pdf_path)
    
    json_path = os.path.join(download_folder, f"{consumer_no}_{bill_date}.json")
    with open(json_path, "w") as json_file:
        json.dump(details, json_file, indent=4)
    
    print(f"Bill saved as: {new_pdf_name}")
    print(f"Extracted details saved as: {json_path}")
else:
    print("No PDF found. Check if the bill was downloaded correctly.")

