# import requests
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# consumer_number = "912121181661"
# mobile_number = "7400074047"
# month = 2   
# year = 2025
# # 712301010605
# project_path = os.path.dirname(os.path.abspath(__file__))

# download_path = os.path.join(project_path, "E-Bill Downloader")
# os.makedirs(download_path, exist_ok=True)

# pdf_filename = f"Bill_{consumer_number}{month}{year}.pdf"
# pdf_filepath = os.path.join(download_path, pdf_filename)

# pdf_url = f"https://tpwodlcis.tpodisha.com/billing/getivewbill/{month},{year},{consumer_number},EN"

# def download_bill_direct():
#     print(f"Attempting direct download for Consumer Number: {consumer_number}...")

#     try:
#         response = requests.get(pdf_url, stream=True)
#         if response.status_code == 200:
#             with open(pdf_filepath, "wb") as pdf_file:
#                 pdf_file.write(response.content)
#             print(f"Bill downloaded successfully: {pdf_filepath}")
#             return True
#         else:
#             print(f"Direct download failed. HTTP Status: {response.status_code}")
#             return False
#     except Exception as e:
#         print(f"Direct download error: {str(e)}")
#         return False

# def download_bill_selenium():
#     print("Trying Selenium automation as a fallback...")

#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_experimental_option("prefs", {
#         "download.default_directory": download_path,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "plugins.always_open_pdf_externally": True  
#     })

#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         print("Opening TPNODL website...")
#         driver.get("https://www.tpsouthernodisha.com/customer-zone/bill-payment/energy-bill.aspx")
#         time.sleep(5)  

#         driver.find_element(By.ID, "consumerNumber").send_keys(consumer_number)

#         driver.find_element(By.ID, "mobileNumber").send_keys(mobile_number)

#         driver.find_element(By.XPATH, "//input[@value='Paynow']").click()
#         time.sleep(10)  

#         wait = WebDriverWait(driver, 15)
#         pdf_icon = wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//span[contains(@class, 'material-icons') and contains(@class, 'likeAnchor')]"))
#         )

#         try:
#             pdf_icon.click()
#             print("Clicked the PDF icon successfully.")
#         except:
#             print("Direct click failed, trying JavaScript...")

#             try:
#                 parent_element = pdf_icon.find_element(By.XPATH, "./ancestor::a | ./ancestor::button | ./ancestor::td")
#                 driver.execute_script("arguments[0].click();", parent_element)
#                 print("Clicked the parent element of the PDF button.")
#             except:
#                 driver.execute_script("arguments[0].click();", pdf_icon)
#                 print("Clicked the PDF icon using JavaScript.")

#         time.sleep(10) 
#         print(f"Bill downloaded successfully for Consumer Number: {consumer_number}")

#     except Exception as e:
#         print(f"Selenium Automation Error: {str(e)}")

#     finally:
#         driver.quit()

# if not download_bill_direct():
#     download_bill_selenium()
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

consumer_numbers = ["811001111174","912311030691","911112080585","903514020318","14135002750","912211060386","515101130814","413512010939"]
mobile_number = "7400074047"
month = 1
year = 2025

project_path = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(project_path, "E-Bill Downloader1")
os.makedirs(download_path, exist_ok=True)

def download_bill_direct(consumer_number):
    pdf_filename = f"Bill_{consumer_number}_{month}_{year}.pdf"
    pdf_filepath = os.path.join(download_path, pdf_filename)
    pdf_url = f"https://tpwodlcis.tpodisha.com/billing/getivewbill/{month},{year},{consumer_number},EN"
    
    print(f"Attempting direct download for Consumer Number: {consumer_number}...")
    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            with open(pdf_filepath, "wb") as pdf_file:
                pdf_file.write(response.content)
            print(f"Bill downloaded successfully: {pdf_filepath}")
            return True
        else:
            print(f"Direct download failed for {consumer_number}. HTTP Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Direct download error for {consumer_number}: {str(e)}")
        return False

def download_bill_selenium(consumer_number):
    print(f"Trying Selenium automation for Consumer Number: {consumer_number}...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  
    })

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://www.tpwesternodisha.com/customer-zone/bill-payment/energy-bill.aspx")
        time.sleep(5)
        driver.find_element(By.ID, "consumerNumber").send_keys(consumer_number)
        driver.find_element(By.ID, "mobileNumber").send_keys(mobile_number)
        driver.find_element(By.XPATH, "//input[@value='Paynow']").click()
        time.sleep(10)
        
        wait = WebDriverWait(driver, 15)
        pdf_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'material-icons') and contains(@class, 'likeAnchor')]")))
        pdf_icon.click()
        print(f"Bill downloaded successfully for Consumer Number: {consumer_number}")
        time.sleep(10)
    except Exception as e:
        print(f"Selenium Automation Error for {consumer_number}: {str(e)}")
    finally:
        driver.quit()

for consumer_number in consumer_numbers:
    if not download_bill_direct(consumer_number):
        download_bill_selenium(consumer_number)