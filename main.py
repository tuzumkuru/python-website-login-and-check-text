import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

def send_notification(server_topic, message):
    requests.post(server_topic, data=message.encode(encoding='utf-8'))

def login(username, password, login_url):
    # Set Chrome options for headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-dev-shm-usage')  
    chrome_options.add_argument('--disable-gpu')  
    
    # Start Chrome browser in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the login page
        driver.get(login_url)
        
        # Find the username and password fields and fill them in
        driver.execute_script("document.getElementsByName('username')[0].value = arguments[0];", username)
        
        driver.execute_script("document.getElementsByName('password')[0].value = arguments[0];", password)
        
        # Submit the form
        login_form = driver.find_element(By.TAG_NAME, "form")
        login_form.submit()
    
    except Exception as e:
        print("Login failed:", str(e))
        return None
    
    return driver

def check_text(driver, text_to_check, check_url):
    try:
        # Navigate to the page
        driver.get(check_url)

        # Check if the text exists on the page
        if text_to_check in driver.page_source:
            return True
        else:
            return False
    
    except Exception as e:
        print("Error occurred while checking text:", str(e))
    
    return False

def save_page_content(driver, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(driver.page_source)

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Set your login credentials and other details
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    login_url = os.getenv("LOGIN_URL")
    check_url = os.getenv("CHECK_URL")
    text_to_check = os.getenv("TEXT_TO_CHECK")
    server_topic_login = os.getenv("SERVER_TOPIC_LOGIN")
    
    # Login
    driver = login(username, password, login_url)
    
    if driver:
        try:
            while True:
                # Check text
                if not check_text(driver, text_to_check, check_url):
                    send_notification(server_topic_login, "Text not found!")
                    save_page_content(driver, "page_content.html")
                    break
                else:
                    print("Text found!")
                time.sleep(1)  # Wait for 1 second before checking again
        finally:
            # Close the browser
            driver.quit()
    else:
        print("Login failed, exiting.")
