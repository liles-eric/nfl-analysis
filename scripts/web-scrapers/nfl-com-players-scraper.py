import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

# URLs for Player Stats (Passing, Rushing, Receiving, Fumbles, Tackles, Interceptions)
player_stats_urls = {
    "passing": "https://www.nfl.com/stats/player-stats/category/passing/2024/reg/all/passingyards/desc",
    "rushing": "https://www.nfl.com/stats/player-stats/category/rushing/2024/reg/all/rushingyards/desc",
    "receiving": "https://www.nfl.com/stats/player-stats/category/receiving/2024/reg/all/receivingreceptions/desc",
    "fumbles": "https://www.nfl.com/stats/player-stats/category/fumbles/2024/reg/all/defensiveforcedfumble/desc",
    "tackles": "https://www.nfl.com/stats/player-stats/category/tackles/2024/reg/all/defensivecombinetackles/desc",
    "interceptions": "https://www.nfl.com/stats/player-stats/category/interceptions/2024/reg/all/defensiveinterceptions/desc"
}

# Function to fetch and parse data for player stats
def fetch_and_parse_player_data(url, stat_type):
    print(f"Fetching data from {url} for player {stat_type}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            # Extract headers and rows
            headers = [header.text.strip() + f"-{stat_type}" for header in table.find_all('th')]
            rows = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                cells = row.find_all('td')
                data = [cell.text.strip() for cell in cells]
                rows.append(data)
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)
            
            # Ensure the first column is named 'Player'
            df.rename(columns={df.columns[0]: 'Player'}, inplace=True)
            
            return df
        else:
            print(f"No table found for player {stat_type}!")
            return None
    else:
        print(f"Failed to fetch page for player {stat_type}: {response.status_code}")
        return None

# Fetch and save player stats to individual CSVs
for stat_type, url in player_stats_urls.items():
    df = fetch_and_parse_player_data(url, stat_type)
    
    if df is not None:
        # Add report date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        df['report_datetime'] = current_datetime
        df['report_date'] = current_date
        
        # Save to CSV
        output_folder = "C:/Users/liles/OneDrive/9. sports-stats/nfl.com stats/"
        file_name = f"nfl-player-stats-{stat_type}-2024.csv"
        file_path = os.path.join(output_folder, file_name)
        df.to_csv(file_path, index=False)
        print(f"{stat_type.capitalize()} stats saved to {file_path}")

