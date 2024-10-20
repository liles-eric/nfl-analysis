# Scripts Folder

This folder contains all the Python scripts necessary for collecting, processing, and integrating NFL data. The scripts are divided into several subcategories depending on their function: fetching data, combining data, and uploading to SQL databases.

## Structure

### 1. all-master-scripts/
  - **nfl-stats-and-weather-all.py**
    - Master script that coordinates the running of all data processing scripts.
    - Fetches weather data and NFL team statistics, then combines them for further analysis.

### 2. sql-updates/
  - **append-nfl-stats-to-sql.py**
    - Appends NFL stats data to an SQL database.
    - Uses SQLAlchemy to handle database connections and data insertion.
    - Before running, ensure the database credentials are properly set up.
    
### 3. weather/
  - **all-nfl-stadiums-weather.py**
    - Combines all weather data files from individual stadiums into one master CSV.
    - This is useful for generating combined datasets to use in analysis.
  
  - **nfl-stadiums-weather-api.py**
    - Fetches weather data for NFL stadiums using the National Weather Service API.
    - Saves data to individual CSV files for each stadium based on the current date.

### 4. web-scrapers/
  - **nfl-com-players-scraper.py**
    - Scrapes player statistics from the NFL website.
    - Outputs CSV files with data relevant to individual player performance.
    
  - **nfl-com-team-scraper.py**
    - Scrapes team statistics from the NFL website.
    - Outputs CSV files for both team offense and team defense statistics.

  - **pro-football-reference**
    - This subfolder will contain additional scripts aimed at scraping data from the Pro Football Reference website for more comprehensive historical data.

## Usage

1. **Data Collection**:
    - Run the individual scrapers under `web-scrapers/` to fetch the latest team and player stats.
    - Run `nfl-stadiums-weather-api.py` to fetch weather data for NFL stadiums.

2. **Data Combination**:
    - Once the individual datasets are fetched, run `all-nfl-stadiums-weather.py` to combine weather data.
    - The `nfl-stats-and-weather-all.py` script can then be used to combine all data, including team stats, weather, and other datasets.

3. **SQL Integration**:
    - Use `append-nfl-stats-to-sql.py` to upload the generated CSV data into an SQL database.
    - Ensure that the SQLAlchemy connection string is correctly set up for the target SQL database.

## Notes

- The scripts are designed to be run sequentially or as part of a pipeline.
- For specifics on each category of script, refer to the individual README files located in the respective subdirectories.
