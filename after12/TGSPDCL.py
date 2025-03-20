# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import time
# import os
# import base64

# # 🔹 Get script directory & create dynamic folder
# script_dir = os.path.dirname(os.path.abspath(__file__))
# dynamic_folder = os.path.join(script_dir, f"TSSPDCL_bills")
# os.makedirs(dynamic_folder, exist_ok=True)  # Create folder

# # 🔹 Consumer number (replace dynamically)
# consumer_number = "105377244"
# bill_url = f"https://tgsouthernpower.org/ops/DuplicateBill4Login.jsp?ctscno={consumer_number}"

# # 🔹 Set filename
# pdf_file_path = os.path.join(dynamic_folder, f"TSSPDCL_Bill_{consumer_number}.pdf")

# # 🔹 Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # Use new headless mode
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--kiosk-printing")  # Auto-save without prompt

# # 🔹 Start WebDriver
# driver = webdriver.Chrome(options=chrome_options)
# try:
#     print("Opening bill page...")
#     driver.get(bill_url)
#     time.sleep(5)  # Allow page to load

#     # 🔹 Print to PDF using Chrome DevTools (returns Base64)
#     pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"format": "A4"})

#     # 🔹 Decode and save the PDF file
#     with open(pdf_file_path, "wb") as f:
#         f.write(base64.b64decode(pdf_data["data"]))

#     print(f"Bill saved: {pdf_file_path}")
# finally:
#     driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import base64

consumer_numbers = ["113863520",
"113534861",
"111463268",
"113053656",
"112020857",
"114504865",
"114621197"
]

script_dir = os.path.dirname(os.path.abspath(__file__))
dynamic_folder = os.path.join(script_dir, f"TSSPDCL_bills")
os.makedirs(dynamic_folder, exist_ok=True)  # Create folder

chrome_options = Options()
chrome_options.add_argument("--headless=new")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--kiosk-printing")  

driver = webdriver.Chrome(options=chrome_options)

try:
    for consumer_number in consumer_numbers:
        bill_url = f"https://tgsouthernpower.org/ops/DuplicateBill4Login.jsp?ctscno={consumer_number}"
        pdf_file_path = os.path.join(dynamic_folder, f"TSSPDCL_Bill_{consumer_number}.pdf")

        print(f"Opening bill page for {consumer_number}...")
        driver.get(bill_url)
        time.sleep(5)  # Allow page to load

        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"format": "A4"})

        # 🔹 Decode and save the PDF file
        with open(pdf_file_path, "wb") as f:
            f.write(base64.b64decode(pdf_data["data"]))

        print(f"Bill saved: {pdf_file_path}")

finally:
    driver.quit()
    print(f"All bills saved in: {dynamic_folder}")
