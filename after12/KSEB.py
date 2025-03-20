import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

consumer_numbers = ["1157323008399"]  
phone = "7400074047"

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd(),  
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

    except Exception as e:
        print(f"Error downloading PDF for {consumer_number}: {e}")

for consumer in consumer_numbers:
    process_consumer(consumer)

driver.quit()
