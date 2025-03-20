import os
import json
import re
import time
import pdfplumber
import glob
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Folder to store bills and extracted JSON file
FOLDER_NAME = "northBihar"
os.makedirs(FOLDER_NAME, exist_ok=True)

# Set Chrome options for downloading
chrome_options = Options()
prefs = {
    "download.default_directory": os.path.abspath(FOLDER_NAME),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

consumer_numbers = [
    "110101228089",
    "244210369306",
    "401590010",
    "128101635099",
    "120204163991",

]
# , "145108136878"

driver = webdriver.Chrome(options=chrome_options)

def wait_for_download(consumer_number, timeout=30):
    """Waits for the PDF to be fully downloaded."""
    download_path = os.path.abspath(FOLDER_NAME)
    pdf_pattern = os.path.join(download_path, f"{consumer_number}*.pdf")
    
    for _ in range(timeout):
        matching_files = glob.glob(pdf_pattern)
        if matching_files:
            latest_file = max(matching_files, key=os.path.getctime)
            if not latest_file.endswith(".crdownload"):  # Ensure file is fully downloaded
                return latest_file
        time.sleep(1)
    
    return None

def process_consumer(consumer_number):
    try:
        driver.get("https://nbpdcl.co.in/(S(5mzcvpgu1h1vi4qfi5pgnuwo))/frmQuickBillPaymentAll.aspx")

        # Wait for the input field and enter consumer number
        consumer_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "MainContent_txtCANO"))
        )
        consumer_input.clear()
        consumer_input.send_keys(consumer_number)

        submit_button = driver.find_element(By.ID, "MainContent_btnSubmit")
        submit_button.click()

        # Wait for the View button to appear
        try:
            view_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "MainContent_GVBillDetails_lnkView_0"))
            )
            view_button.click()
        except:
            print(f"No bill available for consumer number: {consumer_number}")
            return

        # Wait for the PDF to be fully downloaded
        pdf_filename = wait_for_download(consumer_number)
        if not pdf_filename:
            print(f"PDF download failed for {consumer_number}")
            return

        pdf_path = os.path.join(FOLDER_NAME, pdf_filename)
        bill_details = extract_bill_details(pdf_path)

        if bill_details:
            bill_date = bill_details.get("Bill Date", "unknown").replace("/", "-")
            final_pdf_name = os.path.join(FOLDER_NAME, f"{consumer_number}_{bill_date}.pdf")
            os.rename(pdf_path, final_pdf_name)

            json_path = final_pdf_name.replace(".pdf", ".json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(bill_details, json_file, indent=4)

    except Exception as e:
        print(f"Error processing {consumer_number}: {e}\n{traceback.format_exc()}")

def extract_bill_details(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

            bill_no = extract_value(text, r"fcy la\[;k (\d+)")
            bill_date = extract_value(text, r"fcy frfFk (\d{2}-\d{2}-\d{4})")
            due_date = extract_value(text, r"frfFk (\d{2}-\d{2}-\d{4})", occurrence=2)
            amount = extract_value(text, r"dqy jkf'k.*?(-?\d+\.\d{2})")

            return {
                "Bill No": bill_no,
                "Bill Date": bill_date,
                "Due Date": due_date,
                "Amount": amount
            }
    except Exception as e:
        print(f"Error extracting details from {pdf_path}: {e}\n{traceback.format_exc()}")
        return {}

def extract_value(text, pattern, occurrence=1):
    matches = re.findall(pattern, text)
    return matches[occurrence - 1] if matches else "Not found"

for consumer in consumer_numbers:
    process_consumer(consumer)

driver.quit()



# # re pattern for different bill format
# import fitz  # PyMuPDF
# import re
# import unicodedata

# def extract_bill_details(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = "\n".join([page.get_text("text") for page in doc])
    

#     text = unicodedata.normalize("NFKD", text)
    
    
#     details = {}
    
#     details["Consumer Number"] = extract_value(text, r"Kaataa saMKyaa\s*(\d{9,})")
#     details["Bill Date"] = extract_value(text, r"LT\d+\s*(\d{2}\.\d{2}\.\d{2,4})")
#     details["Due Date"] = extract_value(text, r"idnaaMk\s*(\d{2}\.\d{2}\.\d{4})(?=\s+DBCAA)")
#     details["Amount Payable"] = extract_value(text, r"kuxla AiBainaQaa-rNa \"ba\"\s*([\d\.\-]+)")
#     details["Total Consumption"] = extract_value(
#         text,
#         r"LT\d+\s*\n"            # Meter number line
#         r"\d{2}\.\d{2}\.\d{2,4}\s*\n"  # Date line (Bill Date)
#         r"\d+\s*\n"              # Current reading
#         r"\d{2}\.\d{2}\.\d{2,4}\s*\n"  # Previous reading date
#         r"\d+\s*\n"              # Previous reading
#         r"(\d+)"                 # Total consumption (difference)
#     )
#     details["Power Factor"] = extract_value(text, r"paavar fOxkTr\s*(\d+\.\d+)")
    
#     return details

# def extract_value(text, pattern):
#     match = re.search(pattern, text, re.IGNORECASE)
#     return match.group(1) if match else "Not Found"

# # Example usage
# pdf_path = "102246910_Not found.pdf"
# bill_details = extract_bill_details(pdf_path)
# for key, value in bill_details.items():
#     print(f"{key}: {value}")
# "401590010",