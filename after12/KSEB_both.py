import os
import time
import json
import re
import base64
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

consumer_numbers = ["1157323008399"]  
phone = "7400074047"

# Define the storage folder
folder_name = "KSEB_bills"
os.makedirs(folder_name, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(folder_name),  
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True 
})

driver = webdriver.Chrome(options=options)

def process_consumer(consumer_number):
    driver.get("https://old.kseb.in/billview/index.php")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "consumerno_id"))).send_keys(consumer_number)
    driver.find_element(By.ID, "regmobno_id").send_keys(phone)
    driver.find_element(By.ID, "b_submit_0").click()

    time.sleep(10)  

    try:
        download_button = driver.find_element(By.XPATH, "//a[contains(@href, '.pdf')]") 
        pdf_url = download_button.get_attribute("href")
        driver.get(pdf_url) 
        print(f"Downloading bill for {consumer_number}")

        time.sleep(5)  # Wait for download to complete
        downloaded_pdf = max([f for f in os.listdir(folder_name) if f.endswith(".pdf")], key=lambda f: os.path.getctime(os.path.join(folder_name, f)))
        
        # Extract information from PDF
        extract_bill_info(consumer_number, downloaded_pdf)
        
    except Exception as e:
        print(f"Error downloading PDF for {consumer_number}: {e}")

def extract_bill_info(consumer_number, pdf_path):
    pdf_full_path = os.path.join(folder_name, pdf_path)
    
    with open(pdf_full_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages])

    bill_date = re.search(r"Bill Date\s+([\d-]+)", text)
    bill_date = bill_date.group(1) if bill_date else "unknown"
    
    consumer_number = re.search(r"Consumer#\s+(\d+)", text).group(1)
    bill_number = re.search(r"Bill#\s+(\d+)", text).group(1)
    due_date = re.search(r"Due Date\s+([\d-]+)", text).group(1)
    amount = re.search(r"Net Payable.*?\s+([\d,]+)", text).group(1)
    total_consumption = re.search(r"KWH Cumulative Import\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+(\d+)", text).group(1)
    
    # Define new filename
    new_pdf_name = f"{consumer_number}_{bill_date}.pdf"
    new_pdf_path = os.path.join(folder_name, new_pdf_name)
    os.rename(pdf_full_path, new_pdf_path)
    
    # Save JSON data
    extracted_data = {
        "Consumer Number": consumer_number,
        "Bill Number": bill_number,
        "Bill Date": bill_date,
        "Due Date": due_date,
        "Amount": f"₹{amount}",
        "Total Consumption (kWh)": total_consumption,
    }
    
    json_path = os.path.join(folder_name, f"{consumer_number}_{bill_date}.json")
    with open(json_path, "w") as json_file:
        json.dump(extracted_data, json_file, indent=4)
    
    print(f"Extracted data saved as {json_path}")

for consumer in consumer_numbers:
    process_consumer(consumer)

driver.quit()
