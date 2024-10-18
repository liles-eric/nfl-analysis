import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup options for headless scraping (no browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to scrape the table
def fetch_and_parse_stats(url, stat_type):
    driver.get(url)

    try:
        # Wait for the table or some specific content to load (increase the wait time if needed)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))  # Adjust this selector as needed
        )

        # Scrape the table (adjust the selector for the table based on page structure)
        table = driver.find_element(By.TAG_NAME, "table")
        df = pd.read_html(table.get_attribute("outerHTML"))[0]

        # Return the dataframe with the stat_type
        print(f"Data for {stat_type} fetched successfully!")
        return df
    except Exception as e:
        print(f"Error fetching data for {stat_type}: {str(e)}")
        return None

# Save the dataframe to CSV with current date and time
def save_to_csv_with_date(df, file_name, output_folder):
    current_date = time.strftime("%Y-%m-%d")
    file_path = os.path.join(output_folder, file_name)

    # Add report date columns
    df['report_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S")
    df['report_date'] = current_date

    # Save to CSV
    df.to_csv(file_path, index=False)
    print(f"Data for {file_name} saved successfully to {file_path}.")

# Main processing loop
def process_advanced_stats():
    output_folder = "C:/Users/liles/OneDrive/9. sports-stats/nfl.com stats"

    # URLs and stat types
    advanced_stats_urls = {
        "passing": "https://nextgenstats.nfl.com/stats/passing/2024/REG/all#yards",
        "rushing": "https://nextgenstats.nfl.com/stats/rushing#yards",
        "receiving": "https://nextgenstats.nfl.com/stats/receiving#yards"
    }

    for stat_type, url in advanced_stats_urls.items():
        df = fetch_and_parse_stats(url, stat_type)
        if df is not None:
            file_name = f"nfl-next-gen-{stat_type}-advanced-2024.csv"
            save_to_csv_with_date(df, file_name, output_folder)

# Call the function to process advanced stats
process_advanced_stats()

# Close the WebDriver after scraping
driver.quit()
