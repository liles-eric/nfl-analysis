import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import time

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

# Function to clean up team names and ensure all other fields are numeric
def clean_data(df):
    # Clean team names: remove quotes, newlines, excessive spaces
    df['Team'] = df['Team'].replace('"', '', regex=True).replace(r'\s+', ' ', regex=True).str.strip()

    # Remove duplicate team names (if team name appears twice, e.g., "49ers 49ers")
    df['Team'] = df['Team'].apply(lambda x: x.split()[0] if len(set(x.split())) == 1 else x.split()[0])

    # Clean numeric columns: remove non-numeric characters, handle NaNs
    for col in df.columns:
        if col != 'Team':  # Ensure 'Team' stays as a string
            df[col] = df[col].str.extract('(\d+)', expand=False)  # Extract only numeric part
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)  # Convert to integer

    return df

# Function to fetch and parse data
def fetch_and_parse_data(url, stat_type, category):
    print(f"Fetching data from {url} for {category} {stat_type}...")
    response = fetch_with_retry(url)
    
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            headers = [header.text.strip() + f"-{category}-{stat_type}" for header in table.find_all('th')]
            rows = [[cell.text.strip() for cell in row.find_all('td')] for row in table.find_all('tr')[1:]]
            
            df = pd.DataFrame(rows, columns=headers)
            df.rename(columns={df.columns[0]: 'Team'}, inplace=True)  # Ensure team column is named 'Team'
            return clean_data(df)
        else:
            print(f"No table found for {category} {stat_type}.")
    else:
        print(f"Failed to fetch page for {category} {stat_type}.")
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
offense_dataframes = [fetch_and_parse_data(url, stat_type, "off") for stat_type, url in offense_urls.items() if fetch_and_parse_data(url, stat_type, "off") is not None]
offense_merged = merge_dataframes_by_team(offense_dataframes) if offense_dataframes else None

# Fetch and merge all defense data
defense_dataframes = [fetch_and_parse_data(url, stat_type, "def") for stat_type, url in defense_urls.items() if fetch_and_parse_data(url, stat_type, "def") is not None]
defense_merged = merge_dataframes_by_team(defense_dataframes) if defense_dataframes else None

# Add report date and time to both offense and defense data
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.now().strftime("%Y-%m-%d")

if offense_merged is not None:
    offense_merged['report_datetime'] = current_datetime
    offense_merged['report_date'] = current_date

if defense_merged is not None:
    defense_merged['report_datetime'] = current_datetime
    defense_merged['report_date'] = current_date

# Define output folders
primary_output_folder = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/nfl-stats/"
secondary_output_folder = "C:/Users/liles/OneDrive/9. sports-stats/nfl.com stats/"

os.makedirs(primary_output_folder, exist_ok=True)
os.makedirs(secondary_output_folder, exist_ok=True)

# Save merged data to CSV in both locations
if offense_merged is not None:
    offense_file = "nfl-team-stats-off-2024.csv"
    # For secondary folder, append the current date to avoid overwriting (no time in filename)
    offense_file_secondary = f"nfl-team-stats-off-2024-{current_date}.csv"
    
    # Save in primary folder (with fixed filename for weekly updates)
    offense_merged.to_csv(os.path.join(primary_output_folder, offense_file), index=False)
    
    # Save in secondary folder (with date in filename, overwriting if run again on the same day)
    offense_merged.to_csv(os.path.join(secondary_output_folder, offense_file_secondary), index=False)
    
    print(f"Offense data saved to {primary_output_folder} and {secondary_output_folder} with date in secondary filename.")

if defense_merged is not None:
    defense_file = "nfl-team-stats-def-2024.csv"
    # For secondary folder, append the current date to avoid overwriting (no time in filename)
    defense_file_secondary = f"nfl-team-stats-def-2024-{current_date}.csv"
    
    # Save in primary folder (with fixed filename for weekly updates)
    defense_merged.to_csv(os.path.join(primary_output_folder, defense_file), index=False)
    
    # Save in secondary folder (with date in filename, overwriting if run again on the same day)
    defense_merged.to_csv(os.path.join(secondary_output_folder, defense_file_secondary), index=False)
    
    print(f"Defense data saved to {primary_output_folder} and {secondary_output_folder} with date in secondary filename.")
