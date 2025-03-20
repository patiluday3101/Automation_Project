# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# import re

# # Initialize WebDriver
# driver = webdriver.Chrome()
# driver.get("https://consumer.uppcl.org/wss/auth/login")

# wait = WebDriverWait(driver, 10)  

# # Select Region
# dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select")))
# dropdown.click()
# time.sleep(1)
# option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Mathura')]")))
# option.click()

# # Enter Credentials
# accountid = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
# accountid.send_keys("3774132383")

# password = wait.until(EC.presence_of_element_located((By.ID, "password")))
# password.send_keys("Buildint@123")

# # CAPTCHA Handling with Retry Mechanism
# max_attempts = 5
# attempt = 0
# captcha_solved = False

# while attempt < max_attempts and not captcha_solved:
#     attempt += 1
#     print(f"Attempt {attempt} to solve CAPTCHA")

#     # Capture and process CAPTCHA
#     captcha_element = wait.until(EC.presence_of_element_located((By.ID, "captcha")))
#     captcha_element.screenshot("captcha.png")

#     image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
#     _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
#     captcha_text = pytesseract.image_to_string(image, config='--psm 6').strip().replace("=", "").replace("?", "")
#     captcha_text = re.sub(r'[^0-9+\-*/()]', '', captcha_text) 

#     print("Extracted CAPTCHA:", captcha_text)

#     try:
#         captcha_result = eval(captcha_text)
#     except:
#         captcha_result = ""

#     print("Solved CAPTCHA:", captcha_result)

#     # Enter CAPTCHA
#     captcha_input = wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
#     captcha_input.clear()
#     captcha_input.send_keys(str(captcha_result))

#     # Click Login Button (Fix for Click Interception)
#     button = driver.find_element(By.ID, "btnSubmit")
#     driver.execute_script("arguments[0].scrollIntoView(true);", button)
#     time.sleep(1)  # Ensure visibility
#     driver.execute_script("arguments[0].click();", button) 


#     time.sleep(3)  
#     if "captchaInput" not in driver.page_source:
#         captcha_solved = True
#     else:
#         print("Incorrect CAPTCHA, retrying...")

# if not captcha_solved:
#     print("Failed to solve CAPTCHA after multiple attempts. Exiting.")
#     driver.quit()
#     exit()
    
# time.sleep(3)  
# driver.quit()
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# import re

# # Initialize WebDriver
# driver = webdriver.Chrome()
# driver.get("https://consumer.uppcl.org/wss/auth/login")

# wait = WebDriverWait(driver, 10)  

# dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select")))
# dropdown.click()
# time.sleep(1)
# option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Mathura')]")))
# option.click()

# accountid = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
# accountid.send_keys("3774132383")

# password = wait.until(EC.presence_of_element_located((By.ID, "password")))
# password.send_keys("Buildint@123")

# max_attempts = 5
# attempt = 0
# captcha_solved = False

# while attempt < max_attempts and not captcha_solved:
#     attempt += 1
#     print(f"Attempt {attempt} to solve CAPTCHA")

#     # Capture and process CAPTCHA
#     captcha_element = wait.until(EC.presence_of_element_located((By.ID, "captcha")))
#     captcha_element.screenshot("captcha.png")

#     image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)
#     _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
#     captcha_text = pytesseract.image_to_string(image, config='--psm 6').strip().replace("=", "").replace("?", "")
#     captcha_text = re.sub(r'[^0-9+\-*/()]', '', captcha_text) 

#     print("Extracted CAPTCHA:", captcha_text)

#     try:
#         captcha_result = eval(captcha_text)
#     except:
#         captcha_result = ""

#     print("Solved CAPTCHA:", captcha_result)

#     # Enter CAPTCHA
#     captcha_input = wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
#     captcha_input.clear()
#     captcha_input.send_keys(str(captcha_result))

#     # Click Login Button (Fix for Click Interception)
#     button = driver.find_element(By.ID, "btnSubmit")
#     driver.execute_script("arguments[0].scrollIntoView(true);", button)
#     time.sleep(1)  # Ensure visibility
#     driver.execute_script("arguments[0].click();", button) 

#     time.sleep(3)  
#     if "captchaInput" not in driver.page_source:
#         captcha_solved = True
#     else:
#         print("Incorrect CAPTCHA, retrying...")

# if not captcha_solved:
#     print("Failed to solve CAPTCHA after multiple attempts. Exiting.")
#     driver.quit()
#     exit()

# time.sleep(3)

# # Close driver (optional)
# time.sleep(3)
# driver.quit()

