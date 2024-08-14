from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
import csv
from datetime import datetime
import subprocess

# Setup Chrome options to suppress logging and run in incognito mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--log-level=3")  # Suppress errors and warnings
chrome_options.add_argument("--incognito")  # Run in incognito mode

# Define the path to the chromedriver executable
chrome_driver_path = "C:/Users/sujay/Desktop/Python/Seedr.cc-Torrent-Account-Creator-main/Seedr.cc-Torrent-Account-Creator-main/chromedriver.exe"

# Set up the Service object
service = Service(executable_path=chrome_driver_path)

# Initialize the Chrome WebDriver with the Service object and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Step 1: Navigate to 1secmail to generate a temporary email
driver.get("https://www.1secmail.com/")
time.sleep(5)  # Wait for the page to load

# Step 2: Trigger the "Copy" button to copy the email to the clipboard
try:
    copy_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'copyEmailToClipboard')]"))
    )
    copy_button.click()
    time.sleep(1)  # Give a brief moment for the clipboard operation to complete
except Exception as e:
    print("Error: Unable to click the copy button. ", e)
    driver.quit()
    exit()

# Step 3: Retrieve the email from the clipboard
email = pyperclip.paste()
password = "Password123$$$"
print(f"Copied Email: {email}")

# Log the credentials to a CSV file with the current date and time
with open("credentials.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([email, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# Step 4: Open Seedr sign-up page in a new tab
driver.execute_script("window.open('https://www.seedr.cc/auth/pages/signup', '_blank');")

# Step 5: Switch to the new tab
driver.switch_to.window(driver.window_handles[-1])
time.sleep(5)  # Wait for the page to load

# Step 6: Fill out the email field
email_input = driver.find_element(By.NAME, "username")
email_input.send_keys(email)

# Step 7: Fill out the password field
password_input = driver.find_element(By.NAME, "password")
password_input.send_keys(password)

# Step 8: Select the radio button for opt-in
optin_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @name='optin' and @value='1']")
optin_radio.click()

# Step 9: Check the Terms and Privacy Policy checkbox
terms_checkbox = driver.find_element(By.NAME, "accept_terms")
terms_checkbox.click()

# Step 10: Press the Continue button to submit the form
continue_button = driver.find_element(By.ID, "submit-email")
continue_button.click()

# Step 11: Pause the script for the user to complete the captcha
print("Please complete the captcha in the browser.")
input("Press Enter after you have completed the captcha...")

# Step 12: Switch back to the 1secmail tab
driver.switch_to.window(driver.window_handles[0])
print("Please wait for the activation email to arrive. Do not refresh the page.")

# Step 13: Wait and check for the email from Seedr and click on it
email_received = False
while not email_received:
    try:
        email_row = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'reply@seedr.cc')]"))
        )
        email_row.click()  # Open the email
        email_received = True
    except Exception as e:
        print("Error: Unable to find the email. ", e)
        driver.quit()
        exit()

# Step 14: Find the "Start" button in the email and click it using the provided XPath
try:
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='messageBody']/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/center/a"))
    )
    start_button.click()
    print("Start button clicked.")
except Exception as e:
    print("Error: Unable to find the Start button. ", e)

# Step 15: Switch to the new tab opened by the "Start" button
driver.switch_to.window(driver.window_handles[-1])
time.sleep(5) 

# Step 16: Wait for the "Activate Account" button to be clickable and then click it
try:
    activate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Activate Account')]"))
    )
    activate_button.click()
    print("Activate Account button clicked.")
except Exception as e:
    print("Error: Unable to find the Activate Account button. ", e)

time.sleep(15) 

# Close the black box using the provided XPath
try:
    close_black_box_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[45]/div/a[2]"))
    )
    close_black_box_button.click()
    print("Black box closed successfully.")
except Exception as e:
    print("Error: Unable to close the black box. ", e)
time.sleep(15) 

# Step 18: Run the scraper script
print("Running the scraper script...")
try:
    # subprocess.run(["python", "scraper.py"], check=True)
    subprocess.run([r"C:\Users\sujay\Desktop\Python\Seedr.cc-Torrent-Account-Creator-main SFW\Seedr.cc-Torrent-Account-Creator Scrapper and Downloader\.venv\Scripts\python.exe", "scraper.py"], check=True)

    print("Scraper script completed.")
except subprocess.CalledProcessError as e:
    print(f"Error running scraper script: {e}")
    driver.quit()
    exit()

# The browser will remain open after the script completes
print("Script completed. The browser will remain open.")
