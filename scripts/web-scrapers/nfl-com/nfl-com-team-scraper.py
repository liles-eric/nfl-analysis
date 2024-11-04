import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import time
import shutil

# URLs for Offense and Defense Stats
offense_urls = {
    "passing": "https://www.nfl.com/stats/team-stats/offense/passing/2024/reg/all",
    "rushing": "https://www.nfl.com/stats/team-stats/offense/rushing/2024/reg/all",
    "receiving": "https://www.nfl.com/stats/team-stats/offense/receiving/2024/reg/all",
    "scoring": "https://www.nfl.com/stats/team-stats/offense/scoring/2024/reg/all",
    "downs": "https://www.nfl.com/stats/team-stats/offense/downs/2024/reg/all"
}

defense_urls = {
    "passing": "https://www.nfl.com/stats/team-stats/defense/passing/2024/reg/all",
    "rushing": "https://www.nfl.com/stats/team-stats/defense/rushing/2024/reg/all",
    "receiving": "https://www.nfl.com/stats/team-stats/defense/receiving/2024/reg/all",
    "scoring": "https://www.nfl.com/stats/team-stats/defense/scoring/2024/reg/all",
    "tackles": "https://www.nfl.com/stats/team-stats/defense/tackles/2024/reg/all",
    "downs": "https://www.nfl.com/stats/team-stats/defense/downs/2024/reg/all",
    "fumbles": "https://www.nfl.com/stats/team-stats/defense/fumbles/2024/reg/all",
    "interceptions": "https://www.nfl.com/stats/team-stats/defense/interceptions/2024/reg/all"
}

# Retry mechanism for fetching data
def fetch_with_retry(url, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print(f"Attempt {i+1}: Failed with status code {response.status_code}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i+1}: Error fetching data - {e}. Retrying...")
        time.sleep(3)
    return None

# Function to fetch and parse data
def fetch_and_parse_data(url, stat_type, category):
    print(f"Fetching data from {url} for {category} {stat_type}...")
    response = fetch_with_retry(url)
    
    if response is not None:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            headers = [header.text.strip() + f"-{category}-{stat_type}" for header in table.find_all('th')]
            rows = []
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                data = [cell.text.strip() for cell in cells]
                rows.append(data)
            
            df = pd.DataFrame(rows, columns=headers)
            df.rename(columns={df.columns[0]: 'Team'}, inplace=True)
            df['Team'] = df['Team'].str.replace(r'\s+', ' ', regex=True).str.strip().str.title()
            df['Team'] = df['Team'].apply(lambda x: '49ers' if '49ers' in x else ' '.join(sorted(set(x.split()), key=x.split().index)))
            return df
        else:
            print(f"No table found for {category} {stat_type}!")
            return None
    else:
        print(f"Failed to fetch page for {category} {stat_type}. Giving up.")
        return None

# Function to merge multiple dataframes by team name
def merge_dataframes_by_team(dataframes):
    if not dataframes:
        return None
    merged_df = dataframes.pop(0)
    for df in dataframes:
        merged_df = pd.merge(merged_df, df, on='Team', how='outer')
    return merged_df

# Fetch and merge all offense data
offense_dataframes = []
for stat_type, url in offense_urls.items():
    df = fetch_and_parse_data(url, stat_type, "off")
    if df is not None:
        offense_dataframes.append(df)

if offense_dataframes:
    offense_merged = merge_dataframes_by_team(offense_dataframes)

# Fetch and merge all defense data
defense_dataframes = []
for stat_type, url in defense_urls.items():
    df = fetch_and_parse_data(url, stat_type, "def")
    if df is not None:
        defense_dataframes.append(df)

if defense_dataframes:
    defense_merged = merge_dataframes_by_team(defense_dataframes)

# Add report date and time to both offense and defense data
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.now().strftime("%Y-%m-%d")

if offense_dataframes:
    offense_merged['report_datetime'] = current_datetime
    offense_merged['report_date'] = current_date

if defense_dataframes:
    defense_merged['report_datetime'] = current_datetime
    defense_merged['report_date'] = current_date

# Define the output and backup folders
output_folder = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/nfl-stats/"
backup_folder = "C:/Users/liles/OneDrive/9. sports-stats/nfl.com stats"

# Ensure directories exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

# Save primary files and backup copies with date
if offense_dataframes:
    offense_file = os.path.join(output_folder, "nfl-team-stats-off-2024.csv")
    offense_merged.to_csv(offense_file, index=False)
    print(f"Offense data saved to {offense_file}")
    
    offense_backup_file = os.path.join(backup_folder, f"nfl-team-stats-off-2024-{current_date}.csv")
    shutil.copy(offense_file, offense_backup_file)
    print(f"Offense backup data saved to {offense_backup_file}")

if defense_dataframes:
    defense_file = os.path.join(output_folder, "nfl-team-stats-def-2024.csv")
    defense_merged.to_csv(defense_file, index=False)
    print(f"Defense data saved to {defense_file}")
    
    defense_backup_file = os.path.join(backup_folder, f"nfl-team-stats-def-2024-{current_date}.csv")
    shutil.copy(defense_file, defense_backup_file)
    print(f"Defense backup data saved to {defense_backup_file}")
