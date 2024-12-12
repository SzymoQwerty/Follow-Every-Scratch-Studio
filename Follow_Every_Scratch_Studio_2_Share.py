from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Replace these with your Scratch credentials
USERNAME = 'your_username'  # Replace with your username
PASSWORD = 'your_password'  # Replace with your password

# Function to set up the WebDriver
def setup_driver():
    options = Options()
    options.headless = True  # Set to True if you don't want the browser to open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to log into Scratch
def login(driver):
    driver.get("https://scratch.mit.edu/accounts/login/")
    
    # Wait for the username field to be present
    username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "id_username")))
    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "id_password")))
    
    # Input credentials
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    
    # Wait for the login button to be clickable and then click it
    try:
        login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][normalize-space(text())='Login']")))
        login_button.click()
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Wait for login to complete (you can modify this based on page content after login)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "avatar")))
    print("Login successful!")

# Function to visit studio and follow it
def follow_studio(driver, studio_id):
    try:
        driver.get(f"https://scratch.mit.edu/studios/{studio_id}")
        time.sleep(2)  # Wait for the page to load
        
        # Check if the studio exists by looking for specific elements (title or button)
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))  # Studio title
        
        if "not found" in driver.page_source.lower():  # If the studio doesn't exist
            print(f"Studio {studio_id} doesn't exist. Skipping...")
            return
        
        # Look for the Follow button
        follow_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button studio-follow-button']")))
        follow_button.click()
        print(f"Successfully followed Studio {studio_id}!")
    
    except Exception as e:
        print(f"Failed to interact with Studio {studio_id}: {e}")
        return

# Function to follow multiple studios using threads
def follow_multiple_studios(start_id, end_id):
    driver = setup_driver()
    
    # Log in first
    login(driver)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(follow_studio, driver, studio_id) for studio_id in range(start_id, end_id + 1)]
        
        for future in as_completed(futures):
            future.result()  # Ensures any exception is caught and handled
    
    # Close the driver after completion
    driver.quit()

# Start the bot to follow studios
follow_multiple_studios(1, 100)  # Adjust your range as needed (e.g., from studio 1 to studio 10)
