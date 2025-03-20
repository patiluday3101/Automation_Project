import os
import time
import json
import re
import fitz
import unicodedata
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

FOLDER_NAME = "southBihar" 
os.makedirs(FOLDER_NAME, exist_ok=True)

chrome_options = Options()
prefs = {"download.default_directory": os.path.abspath(FOLDER_NAME), 
         "download.prompt_for_download": False,
         "download.directory_upgrade": True,
         "safebrowsing.enabled": True}
chrome_options.add_experimental_option("prefs", prefs)

consumer_numbers = [ "236510069436"]

driver = webdriver.Chrome(options=chrome_options)

def process_consumer(consumer_number):
    driver.get("https://www.sbpdcl.co.in/(S(2iy0w0lt5ka0e4mqykw4iml1))/frmQuickBillPaymentAll.aspx")
    time.sleep(2)
    
    consumer_input = driver.find_element(By.ID, "MainContent_txtCANO")
    consumer_input.send_keys(consumer_number)
    
    submit_button = driver.find_element(By.ID, "MainContent_btnSubmit")
    submit_button.click()
    
    try:
        view_button = driver.find_element(By.ID, "MainContent_lnkView1")
        view_button.click()
        time.sleep(5)  
        
        # Wait for file download
        pdf_filename = find_latest_pdf(FOLDER_NAME, consumer_number)
        if not pdf_filename:
            print(f"PDF not found for {consumer_number}")
            return
        
        pdf_path = os.path.join(FOLDER_NAME, pdf_filename)
        
        # Extract bill details
        bill_details = extract_bill_details(pdf_path)
        
        if bill_details:
            bill_date = bill_details.get("Bill Date", "unknown").replace("/", "-")
            final_pdf_name = os.path.join(FOLDER_NAME, f"{consumer_number}_{bill_date}.pdf")
            os.rename(pdf_path, final_pdf_name)
            
            json_path = final_pdf_name.replace(".pdf", ".json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(bill_details, json_file, indent=4)
    except Exception as e:
        print(f"Error processing {consumer_number}: {e}")

def extract_bill_details(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            
            bill_no = extract_value(text, r"fcy la\[;k (\d+)")  
            bill_date = extract_value(text, r"fcy frfFk (\d{2}-\d{2}-\d{4})")  
            due_date = extract_value(text, r"frfFk (\d{2}-\d{2}-\d{4})", occurrence=2)
            amount = extract_value(text, r"dqy jkf'k.*?(-?\d+\.\d{2})") 
            power_factor = extract_value(text, r"ikoj QSDVj\s*(\d+\.\d+)")
            
            if power_factor == "Not found":
                power_factor = "0"
            
            return {
                "Bill No": bill_no,
                "Bill Date": bill_date,
                "Due Date": due_date,
                "Amount": amount,
                "Power Factor": power_factor
            }
    except Exception as e:
        print(f"Error extracting details from {pdf_path}: {e}")
        return {}
    

def extract_value(text, pattern, occurrence=1):
    matches = re.findall(pattern, text)
    if matches:
        return matches[occurrence - 1] if occurrence > 0 else matches[occurrence]
    return "Not found"
def find_latest_pdf(folder, consumer_number):
    files = [f for f in os.listdir(folder) if f.startswith(consumer_number) and f.endswith(".pdf")]
    if files:
        return max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
    return None

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
# "102246910",
# "244210369306",
# "108716640",
# "108717642",
# "226108860490",
# "108694572",
# "108508837",
# "108571785",
# "108694461",
# "108770574",