import os
import time
import json
import re
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

consumer_numbers = ["N3688000173"]

folder_name = "MP_bills"
os.makedirs(folder_name, exist_ok=True)

chrome_options = Options()
prefs = {
    "download.default_directory": os.path.abspath(folder_name),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def download_bill(consumer_number):
    driver.get("https://mpwzservices.mpwin.co.in/westdiscom/home")

    try:
        # Wait for IVRS input field and enter consumer number
        ivrs_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='ivrs']"))
        )
        ivrs_input.send_keys(consumer_number)

        # Click on 'View & Pay Energy Bill'
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='View & Pay Energy Bill']"))
        )
        submit_button.click()

        # Click 'View Full Bill (English)'
        view_bill_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'View Full Bill (English)')]"))
        )

        # Solve "element click intercepted" issue
        driver.execute_script("arguments[0].scrollIntoView();", view_bill_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", view_bill_button)

        print(f"Downloading bill for Consumer: {consumer_number}")

        time.sleep(5)  

        # Find the latest downloaded file
        downloaded_files = sorted(os.listdir(folder_name), key=lambda x: os.path.getmtime(os.path.join(folder_name, x)), reverse=True)
        for file in downloaded_files:
            if file.endswith(".pdf"):
                return os.path.join(folder_name, file)

        print(f"Error: No PDF found for {consumer_number}")
        return None

    except Exception as e:
        print(f"Error processing {consumer_number}: {e}")
        return None

def extract_bill_details(pdf_path):
    details = {}
    bill_date = "Unknown"

    if not pdf_path or not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return details, bill_date

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                match = re.search(r"IVRS\s*[:\-]?\s*([A-Z0-9]+)", text)
                if match:
                    details["Consumer Number"] = match.group(1)

                match = re.search(r"Bill Number\s*[:\-]?\s*([A-Z0-9]+)", text)
                if match:
                    details["Bill Number"] = match.group(1)
                    
                match = re.search(r"(\d{1,2}-[A-Za-z]+-\d{4})", text)
                if match:
                    bill_date = match.group(1)
                    details["Bill Date"] = bill_date


                match = re.search(r"Pole Number Phase Given THREE\s+(\d{1,2}-[A-Za-z]+-\d{4})", text)
                if match:
                    due_date = match.group(1)
                    details["Due Date"] = due_date

                match = re.search(r"TotalAmountPayableAfterDueDate\s*[:\-]?\s*₹?([0-9,.]+)", text)
                if match:
                    details["Total Amount"] =  match.group(1)

                # Extract Sanction Load
                match = re.search(r"Load Sanctioned\s*[:\-]?\s*([0-9.]+)\s*KW", text)
                if match:
                    details["Sanction Load"] = match.group(1) + " KW"

                # Extract Penalty of PF
                match = re.search(r"(?:Power Factor Surcharge|PF Surcharge)\s*[:\-]?\s*₹?([0-9,.]+)", text, re.IGNORECASE)
                if match:
                    details["PF Surcharge"] = match.group(1)

    return details, bill_date

for consumer in consumer_numbers:
    pdf_path = download_bill(consumer)
    if pdf_path:
        details, bill_date = extract_bill_details(pdf_path)

        if bill_date != "Unknown":
            pdf_filename = f"{consumer}_{bill_date}.pdf"
        else:
            pdf_filename = f"{consumer}_unknown.pdf"
        final_pdf_path = os.path.join(folder_name, pdf_filename)
        os.rename(pdf_path, final_pdf_path)

        json_path = os.path.join(folder_name, f"{consumer}_{bill_date}.json")
        with open(json_path, "w") as json_file:
            json.dump(details, json_file, indent=4)

        print(f"Bill saved: {final_pdf_path}")
        print(f"JSON saved: {json_path}")

driver.quit()
