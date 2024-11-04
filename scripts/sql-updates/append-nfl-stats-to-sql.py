import pandas as pd
from sqlalchemy import create_engine

# Define the database connection string
conn_str = 'mssql+pyodbc://eric:AccurateScans!@sports-stats-db-server.database.windows.net:1433/sports_stats_db?driver=ODBC+Driver+17+for+SQL+Server'

# Create the SQLAlchemy engine
engine = create_engine(conn_str)

# Paths to your CSV files
offense_csv_path = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/nfl-stats/nfl-team-stats-off-2024.csv"
defense_csv_path = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/nfl-stats/nfl-team-stats-def-2024.csv"

# Load the CSV files into pandas DataFrames
offense_df = pd.read_csv(offense_csv_path)
defense_df = pd.read_csv(defense_csv_path)

# Function to inspect and clean data
def clean_data(df):
    # Print initial state of DataFrame
    print("Initial DataFrame Head:")
    print(df.head())
    
    # Check for null values in Team column
    if 'Team' in df.columns:
        print("Null Team Values in DataFrame:")
        print(df[df['Team'].isnull()])

    # Clean non-numeric characters from columns except 'Team'
    for col in df.columns:
        if col != 'Team':  # Skip the 'Team' column for cleaning
            df[col] = df[col].replace(r'[^0-9.-]', '', regex=True)  # Remove non-numeric characters
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, setting errors to NaN
            
    return df

# Clean offense and defense DataFrames
offense_df = clean_data(offense_df)
defense_df = clean_data(defense_df)

# Add current date and time
current_time = pd.Timestamp.now()
offense_df['report_datetime'] = current_time
offense_df['report_date'] = current_time.date()

defense_df['report_datetime'] = current_time
defense_df['report_date'] = current_time.date()

# Append offense data to the offense table
try:
    offense_df.to_sql('nfl-team-stats-off', engine, if_exists='append', index=False)
    print(f"Offense data appended successfully to nfl-team-stats-off.")
except Exception as e:
    print(f"An error occurred while appending offense data: {e}")

# Append defense data to the defense table
try:
    defense_df.to_sql('nfl-team-stats-def', engine, if_exists='append', index=False)
    print(f"Defense data appended successfully to nfl-team-stats-def.")
except Exception as e:
    print(f"An error occurred while appending defense data: {e}")
   