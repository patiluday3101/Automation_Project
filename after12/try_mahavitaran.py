import os
import time
import cv2
import pytesseract
import base64
import json
import re
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_with_methods(img):
    """Applies OCR techniques to extract text from an image."""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    text = pytesseract.image_to_string(morph, config="--psm 6").strip()
    return text

def extract_bill_details(pdf_path):
    """Extracts bill details from the PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
    bill_details = {
        "Invoice Number": re.search(r"BILL NO.*?(\d+)", text, re.IGNORECASE).group(1) if re.search(r"BILL NO.*?(\d+)", text, re.IGNORECASE) else "N/A",
        "Billing Date": re.search(r"देयक िदनांक:\s*(\d{2}-[A-Z]{3}-\d{2})", text).group(1) if re.search(r"देयक िदनांक:\s*(\d{2}-[A-Z]{3}-\d{2})", text) else "N/A",
        "Due Date": re.search(r"देय िदनांक:\s*(\d{2}-[A-Z]{3}-\d{2})", text).group(1) if re.search(r"देय िदनांक:\s*(\d{2}-[A-Z]{3}-\d{2})", text) else "N/A",
        "Amount Due": re.search(r"देयक रक्कम रु:\s*([\d,.]+)", text).group(1) if re.search(r"देयक रक्कम रु:\s*([\d,.]+)", text) else "N/A",
        "Power Factor": "0"
    }
    return bill_details

def download_bill(consumer_no, driver):
    driver.get("https://wss.mahadiscom.in/wss/wss?uiActionName=getViewPayBill")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "consumerNo")))
    driver.find_element(By.ID, "consumerNo").clear()
    driver.find_element(By.ID, "consumerNo").send_keys(consumer_no)
    
    while True:
        try:
            captcha_element = driver.find_element(By.ID, "captcha")
            captcha_element.screenshot("captcha.png")
            
            image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
            captcha_text = ocr_with_methods(image)
            
            driver.find_element(By.ID, "txtInput").clear()
            driver.find_element(By.ID, "txtInput").send_keys(captcha_text)
            driver.find_element(By.ID, "lblSubmit").click()
            
            # Wait to check if captcha is accepted
            time.sleep(3)
            if "Invalid Captcha" not in driver.page_source:
                break
            
            print("Captcha incorrect, retrying...")
            driver.find_element(By.ID, "btnCaptchaRefViewpaybill").click()
            time.sleep(2)
        except Exception as e:
            print(f"Captcha processing error: {e}")
            break
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Img1")))
        driver.find_element(By.ID, "Img1").click()
        driver.find_element(By.ID, "lbllTitle").click()
        time.sleep(10)
        
        pdf_data = base64.b64decode(driver.execute_cdp_cmd("Page.printToPDF", {})['data'])
        
        temp_pdf = "temp_bill.pdf"
        with open(temp_pdf, "wb") as f:
            f.write(pdf_data)
        
        bill_details = extract_bill_details(temp_pdf)
        bill_date = bill_details["Billing Date"].replace("/", "-")
        folder_name = "Mahavitaran_Bills1"
        os.makedirs(folder_name, exist_ok=True)
        
        pdf_filename = os.path.join(folder_name, f"{consumer_no}_{bill_date}.pdf")
        json_filename = os.path.join(folder_name, f"{consumer_no}_{bill_date}.json")
        
        os.rename(temp_pdf, pdf_filename)
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(bill_details, json_file, indent=4, ensure_ascii=False)
        
        print(f"Bill saved: {pdf_filename}")
        print(f"JSON saved: {json_filename}")
        
    except Exception as e:
        print(f"Error downloading bill for {consumer_no}: {e}")

def main(consumer_numbers):
    driver = webdriver.Chrome()
    for consumer_no in consumer_numbers:
        try:
            download_bill(consumer_no, driver)
        except Exception as e:
            print(f"Failed for {consumer_no}: {e}")
    driver.quit()

if __name__ == "__main__":
    consumer_list = [
        '170054967422',
        '1622010523207',
        '300333625087',
        '490013447656',
        '850120011883',
        '337010186590',
        '122510335641',
        '490011820571',
        '297160011184',
        '396010409617',
        '415390048870',
        '610550026581',
        '049018437235',
        "410016168134",
        "162014766804",
        "110014722670",
        "000024322882",
        "080018910881",
        "490018747640",
        "173450338046",
        "370028154978",
        "094040013461",
        "366474788291",
        "410013030506",
        "510010034025",
        "366551388683",
        "356310059594",
        "410023712389",
        "352920232594",
        "293240006739",
        "330244952526",
        "284100066074",
        "370010140619",
        "266510300351",
        "450010690370",
        "330241890104",
        "049015515022",
        "419740988981",
        "162011042317",
        "593350005642",
        "611214099704",
        "571010653352",
        "180010080256",
        "049016104859"

        
    ]
    main(consumer_list)
