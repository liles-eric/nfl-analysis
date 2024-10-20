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

# Define the SQL table names
offense_table_name = "nfl-team-stats-off"
defense_table_name = "nfl-team-stats-def"

# Append offense data to the offense table
try:
    offense_df.to_sql(offense_table_name, engine, if_exists='append', index=False)
    print(f"Offense data appended successfully to {offense_table_name}.")
except Exception as e:
    print(f"An error occurred while appending offense data: {e}")

# Append defense data to the defense table
try:
    defense_df.to_sql(defense_table_name, engine, if_exists='append', index=False)
    print(f"Defense data appended successfully to {defense_table_name}.")
except Exception as e:
    print(f"An error occurred while appending defense data: {e}")

# No need to explicitly close the connection as SQLAlchemy manages it

