from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chromedriver_path = "C:\\Windows\\chromedriver.exe"

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://www.apeasternpower.com/viewBillDetailsMain")

wait = WebDriverWait(driver, 10)

ivrs_number = "131102A200010307"

phone_no = wait.until(EC.presence_of_element_located((By.ID, "ltscno")))
phone_no.send_keys(ivrs_number)

captcha_text = wait.until(EC.presence_of_element_located((By.ID, "Billquestion"))).text.strip()
captcha_text = captcha_text.replace("=", "").strip()

try:
    captcha_answer = eval(captcha_text)
except Exception as e:
    print("Error solving CAPTCHA:", e)
    driver.quit()
    exit()

captcha_input = wait.until(EC.presence_of_element_located((By.ID, "Billans")))  
captcha_input.send_keys(str(captcha_answer))

submit_button = wait.until(EC.element_to_be_clickable((By.ID, "Billsignin")))
submit_button.click()

bill_link_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Click Here')]")))

main_window = driver.current_window_handle  

bill_link_element.click()
wait.until(EC.new_window_is_opened(driver.window_handles))
new_window = [window for window in driver.window_handles if window != main_window][0]
driver.switch_to.window(new_window)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
driver.quit()
