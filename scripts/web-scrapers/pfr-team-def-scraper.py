from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up options for Selenium (to specify where to download the file)
chrome_options = Options()
download_dir = "C:/Users/liles/OneDrive/9. sports-stats/nfl.com stats/"  # Specify your desired download path
prefs = {"download.default_directory": download_dir}
chrome_options.add_experimental_option("prefs", prefs)

# Setup Selenium WebDriver with ChromeDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the Pro-Football-Reference page
url = "https://www.pro-football-reference.com/years/2024/index.htm#drives"
driver.get(url)

# Let the page fully load
time.sleep(5)  # Wait for the page to load, adjust this time if necessary

try:
    # Locate the export button or link and click on it to download the file
    export_button = driver.find_element(By.LINK_TEXT, 'Get table as CSV (for Excel)')  # Adjust the text if needed
    export_button.click()

    print(f"File will be downloaded to {download_dir}")

    # Wait for the file to download
    time.sleep(10)  # Adjust time as needed based on your download speed
except Exception as e:
    print(f"Error: {e}")

# Close the WebDriver
driver.quit()
