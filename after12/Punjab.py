import time
import requests
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from PIL import Image

# Set Tesseract-OCR Path (Modify this as per your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Selenium Setup
chrome_driver_path = "path/to/chromedriver"  # Update with the correct path
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)

driver = webdriver.Chrome(service=service, options=options)

# Open PSPCL bill payment page
driver.get("https://billpayment.pspcl.in/pgBillPay.aspx?uc=ViewBillDetail_SimpliFormat")

# Solve CAPTCHA (if present)
captcha_img = driver.find_element(By.ID, "captchaImageId")  # Update this ID if different
captcha_img.screenshot("captcha.png")

# Extract CAPTCHA text
captcha_text = pytesseract.image_to_string(Image.open("captcha.png")).strip()
print(f"Extracted CAPTCHA: {captcha_text}")

# Enter CAPTCHA
captcha_input = driver.find_element(By.ID, "captchaInputId")  # Update this ID if different
captcha_input.send_keys(captcha_text)

# Submit the form
submit_button = driver.find_element(By.ID, "submitButtonId")  # Update this ID if different
submit_button.click()

# Wait for the bill page to load
time.sleep(3)

# Extract session cookies
cookies = driver.get_cookies()
session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

# Close Selenium
driver.quit()

# Prepare headers & session for Requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": "https://billpayment.pspcl.in/pgBillPay.aspx?uc=ViewBillDetail_SimpliFormat",
}

# Send POST request to fetch PDF
pdf_url = "https://billpayment.pspcl.in/pgBillPay.aspx?uc=ViewBillDetail_SimpliFormat"
session = requests.Session()
session.cookies.update(session_cookies)

response = session.post(pdf_url, headers=headers)

# Save the PDF if response is valid
if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
    with open("PSPCL_Bill.pdf", "wb") as file:
        file.write(response.content)
    print("Bill downloaded successfully as 'PSPCL_Bill.pdf'")
else:
    print("Failed to download bill. Check login and cookies.")

