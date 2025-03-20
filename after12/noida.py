import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL of the bill page
bill_url = "https://iwebapps.noidapower.com:8032/consumer/ViewSAPBill.aspx?cono=namjoigfhhkfikcedlmm&InvoNo=nknegohdgphhglbodmpdajid"

# Set up download directory
download_path = os.path.join(os.getcwd(), "NOIDA_Bills")
os.makedirs(download_path, exist_ok=True)  # Create the folder if not exists

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# Automatically download and set up the correct ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the bill page
    driver.get(bill_url)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)

    # Find the download button (modify the selector if needed)
    try:
        download_button = wait.until(EC.element_to_be_clickable((By.ID, "btnDownload")))  # Update ID if necessary
        download_button.click()
        print("Bill download initiated!")
        time.sleep(5)  # Wait for the download to complete
    except:
        print("Download button not found. Attempting direct PDF retrieval...")

        # Try to fetch the bill as a PDF directly
        response = requests.get(bill_url, stream=True)
        if response.status_code == 200:
            pdf_path = os.path.join(download_path, "Electricity_Bill.pdf")
            with open(pdf_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Bill downloaded successfully: {pdf_path}")
        else:
            print("Failed to retrieve the bill PDF.")

finally:
    driver.quit()