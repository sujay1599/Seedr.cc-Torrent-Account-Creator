from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time
import re
import random

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

# Step 1: Navigate directly to the Seedr login page
driver.get("https://www.seedr.cc/auth/pages/login")

# Step 2: Wait until the username field is present
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[1]/div[6]/label/input"))
)

# Step 3: Retrieve the last created credentials from the CSV file
with open("credentials.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    credentials = list(csv_reader)[-1]  # Get the last row
    email = credentials[0]
    password = credentials[1]
    print(f"Using Email: {email} for login.")

# Step 4: Fill out the username (email) field using the provided XPath
try:
    email_input = driver.find_element(By.XPATH, "/html/body/form/div[1]/div[6]/label/input")
    email_input.send_keys(email)
except Exception as e:
    print("Error: Unable to locate username input field. ", e)
    driver.quit()
    exit()

# Step 5: Fill out the password field using the provided XPath
try:
    password_input = driver.find_element(By.XPATH, "/html/body/form/div[1]/div[7]/label/input")
    password_input.send_keys(password)
except Exception as e:
    print("Error: Unable to locate password input field. ", e)
    driver.quit()
    exit()

# Step 6: Click the login button using the provided XPath
try:
    login_button = driver.find_element(By.XPATH, "/html/body/form/div[1]/button")
    login_button.click()
except Exception as e:
    print("Error: Unable to locate login button. ", e)
    driver.quit()
    exit()

# Step 7: Wait for a moment to ensure the login process starts
time.sleep(2)

# Step 8: Open a new tab and navigate to the Seedr homepage
driver.execute_script("window.open('https://www.seedr.cc/', '_blank');")

# Step 9: Switch to the new tab
driver.switch_to.window(driver.window_handles[-1])

# Step 10: Wait for the homepage to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='top_bar_text']"))
    )
    print("Navigation to Seedr homepage successful! You are now on the Seedr homepage.")
except Exception as e:
    print("Error: Navigation to Seedr homepage failed. ", e)

# Step 11: Close the black box using the provided XPath
try:
    close_black_box_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[45]/div/a[2]"))
    )
    close_black_box_button.click()
    print("Black box closed successfully.")
except Exception as e:
    print("Error: Unable to close the black box. ", e)

# Step 12: Function to check storage and delete files if needed
def check_and_free_space():
    try:
        storage_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "top-storage-span"))
        )
        storage_text = storage_span.text
        print(f"Current Storage: {storage_text}")

        # Extract the current storage used in GB or MB
        storage_match = re.search(r"([\d.,]+)\s*([A-Za-z]+)", storage_text)
        if storage_match:
            used_storage_value = float(storage_match.group(1).replace(',', ''))
            used_storage_unit = storage_match.group(2).strip()

            if used_storage_unit == 'GB':
                used_storage_gb = used_storage_value
            elif used_storage_unit == 'MB':
                used_storage_gb = used_storage_value / 1024
            else:
                raise ValueError("Unexpected storage unit encountered.")

            if used_storage_gb > 1.50:  # If storage is greater than 1.50 GB
                print("Storage is greater than 1.50 GB, deleting files to free up space...")
                
                # Select all files
                try:
                    select_all_checkbox = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/div[1]"))
                    )
                    select_all_checkbox.click()
                    print("All files selected.")

                    # Simulate pressing the DELETE key
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DELETE)
                    print("Delete key pressed successfully.")
                    
                    # Wait for 5 seconds
                    time.sleep(5)
                    
                    # Simulate pressing the ENTER key
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                    print("ENTER key pressed successfully.")

                except Exception as e:
                    print(f"Error: Unable to delete files. {e}")

            else:
                print("Storage is within limits, no need to delete files.")

        else:
            raise ValueError("Could not extract storage information.")

    except Exception as e:
        print(f"Error: {e}")

# Step 13: Function to place a single magnet link
def place_single_magnet_link():
    with open("sorted_torrents.csv", "r") as csv_file:
        csv_reader = list(csv.DictReader(csv_file))
        random.shuffle(csv_reader)  # Shuffle the list to pick random links
        
        for row in csv_reader:
            size_str = row['Size']

            # Use regular expressions to extract the correct numeric part and unit
            size_match = re.match(r"([0-9,.]+)\s*([A-Za-z]+)", size_str)
            if size_match:
                size_value = float(size_match.group(1).replace(',', '').strip())  # Numeric part
                size_unit = size_match.group(2).strip()  # Unit part
                
                if size_unit == 'GB':
                    size_in_mb = size_value * 1024
                elif size_unit == 'MB':
                    size_in_mb = size_value
                else:
                    continue  # Skip if the size is not in MB or GB

                if size_in_mb < 1500:
                    magnet_link = row['Magnet Link']
                    
                    try:
                        magnet_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "link"))
                        )
                        magnet_input.clear()
                        magnet_input.send_keys(magnet_link)
                        print(f"Placed magnet link: {magnet_link}")
                        
                        # Step 14: Click the upload button after inserting the magnet link
                        upload_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#upload-button > i"))
                        )
                        upload_button.click()
                        print("Upload button clicked successfully.")
                        
                        # Wait for the download to start
                        time.sleep(10)  # Adjust the sleep time as needed
                        
                        # Step 15: Check storage after placing the magnet link
                        check_and_free_space()

                        # Ask if the user wants to add another link if storage allows
                        remaining_storage_span = driver.find_element(By.ID, "top-storage-span").text
                        remaining_storage_match = re.search(r"([\d.,]+)\s*([A-Za-z]+)", remaining_storage_span)
                        if remaining_storage_match:
                            remaining_storage_value = float(remaining_storage_match.group(1).replace(',', ''))
                            remaining_storage_unit = remaining_storage_match.group(2).strip()

                            if remaining_storage_unit == 'GB':
                                remaining_storage_gb = remaining_storage_value
                            elif remaining_storage_unit == 'MB':
                                remaining_storage_gb = remaining_storage_value / 1024
                            else:
                                raise ValueError("Unexpected storage unit encountered.")

                            if remaining_storage_gb < 2.00:  # Less than 2.00 GB
                                add_another = input(f"Do you want to add another magnet link under {2.00 - remaining_storage_gb:.2f} GB? (yes/no/clear): ").strip().lower()
                                if add_another == 'yes':
                                    continue  # Go to the next magnet link
                                elif add_another == 'clear':
                                    check_and_free_space()  # Delete files if needed
                                    break  # Exit the loop after clearing
                                else:
                                    break  # Exit the loop
                            else:
                                print("Storage is full or above the limit. No more magnet links can be added.")
                                break
                        
                    except Exception as e:
                        print(f"Error: Unable to place magnet link. {e}")
                        break
            else:
                print(f"Error: Could not parse size from string '{size_str}'")

# Call the function to place a single magnet link
place_single_magnet_link()

# Keep the browser open
input("Press Enter to close the browser...")
