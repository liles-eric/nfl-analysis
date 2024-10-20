import requests
import csv
from datetime import datetime, timedelta
import os

# Step 1: Define NFL stadiums, coordinates, and team names by division
nfl_stadiums = {
    # NFC North
    "Lambeau Field": {"lat": 44.5013, "lon": -88.0622, "team": "Packers"},  # Green Bay Packers
    "Soldier Field": {"lat": 41.8625, "lon": -87.6166, "team": "Bears"},  # Chicago Bears
    "U.S. Bank Stadium": {"lat": 44.9737, "lon": -93.2575, "team": "Vikings"},  # Minnesota Vikings
    "Ford Field": {"lat": 42.3400, "lon": -83.0456, "team": "Lions"},  # Detroit Lions

    # AFC North
    "M&T Bank Stadium": {"lat": 39.2779, "lon": -76.6227, "team": "Ravens"},  # Baltimore Ravens
    "Paycor Stadium": {"lat": 39.0955, "lon": -84.5160, "team": "Bengals"},  # Cincinnati Bengals
    "FirstEnergy Stadium": {"lat": 41.5061, "lon": -81.6995, "team": "Browns"},  # Cleveland Browns
    "Acrisure Stadium": {"lat": 40.4468, "lon": -80.0158, "team": "Steelers"},  # Pittsburgh Steelers

    # NFC South
    "Mercedes-Benz Stadium": {"lat": 33.7550, "lon": -84.4009, "team": "Falcons"},  # Atlanta Falcons
    "Bank of America Stadium": {"lat": 35.2251, "lon": -80.8531, "team": "Panthers"},  # Carolina Panthers
    "Caesars Superdome": {"lat": 29.9511, "lon": -90.0812, "team": "Saints"},  # New Orleans Saints
    "Raymond James Stadium": {"lat": 27.9759, "lon": -82.5033, "team": "Buccaneers"},  # Tampa Bay Buccaneers

    # AFC South
    "NRG Stadium": {"lat": 29.6847, "lon": -95.4107, "team": "Texans"},  # Houston Texans
    "Lucas Oil Stadium": {"lat": 39.7601, "lon": -86.1639, "team": "Colts"},  # Indianapolis Colts
    "TIAA Bank Field": {"lat": 30.3239, "lon": -81.6373, "team": "Jaguars"},  # Jacksonville Jaguars
    "Nissan Stadium": {"lat": 36.1665, "lon": -86.7713, "team": "Titans"},  # Tennessee Titans

    # NFC East
    "AT&T Stadium": {"lat": 32.7473, "lon": -97.0945, "team": "Cowboys"},  # Dallas Cowboys
    "MetLife Stadium (NFC)": {"lat": 40.8135, "lon": -74.0744, "team": "Giants"},  # New York Giants
    "Lincoln Financial Field": {"lat": 39.9007, "lon": -75.1675, "team": "Eagles"},  # Philadelphia Eagles
    "FedExField": {"lat": 38.9078, "lon": -76.8645, "team": "Commanders"},  # Washington Commanders

    # AFC East
    "Highmark Stadium": {"lat": 42.7738, "lon": -78.7868, "team": "Bills"},  # Buffalo Bills
    "Hard Rock Stadium": {"lat": 25.9580, "lon": -80.2389, "team": "Dolphins"},  # Miami Dolphins
    "Gillette Stadium": {"lat": 42.0909, "lon": -71.2643, "team": "Patriots"},  # New England Patriots
    "MetLife Stadium (AFC)": {"lat": 40.8135, "lon": -74.0744, "team": "Jets"},  # New York Jets

    # NFC West
    "State Farm Stadium": {"lat": 33.5276, "lon": -112.2637, "team": "Cardinals"},  # Arizona Cardinals
    "SoFi Stadium (NFC)": {"lat": 33.9535, "lon": -118.3392, "team": "Rams"},  # Los Angeles Rams
    "Levi's Stadium": {"lat": 37.4030, "lon": -121.9702, "team": "49ers"},  # San Francisco 49ers
    "Lumen Field": {"lat": 47.5952, "lon": -122.3316, "team": "Seahawks"},  # Seattle Seahawks

    # AFC West
    "Empower Field at Mile High": {"lat": 39.7439, "lon": -105.0201, "team": "Broncos"},  # Denver Broncos
    "GEHA Field at Arrowhead Stadium": {"lat": 39.0490, "lon": -94.4839, "team": "Chiefs"},  # Kansas City Chiefs
    "Allegiant Stadium": {"lat": 36.0909, "lon": -115.1830, "team": "Raiders"},  # Las Vegas Raiders
    "SoFi Stadium (AFC)": {"lat": 33.9535, "lon": -118.3392, "team": "Chargers"},  # Los Angeles Chargers
}

# Step 2: Set up headers (NWS requires a User-Agent header)
headers = {
    "User-Agent": "(myweatherapp.com, contact@myweatherapp.com)"  # Customize as needed
}

# Step 3: Get current date and time for filenames and columns
current_datetime = datetime.now()
current_date = current_datetime.strftime('%Y-%m-%d')
current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Create output folders if they don't exist
primary_output_folder = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/weather/"
secondary_output_folder = "C:/Users/liles/OneDrive/9. sports-stats/weather/"
os.makedirs(primary_output_folder, exist_ok=True)
os.makedirs(secondary_output_folder, exist_ok=True)

# Helper function to get period date and time (with the proper day calculation)
def get_period_date_and_time(period_name):
    """
    Determines the actual date and time based on the period name (e.g., "Tonight", "Sunday Night").
    Handles day and night differentiation. Sets time to 10:00 AM for day, 8:00 PM (20:00) for night.
    """

    if "Night" in period_name or "Overnight" in period_name:
        time_of_day = "Night"
        time_part = "20:00"
    else:
        time_of_day = "Day"
        time_part = "10:00"

    # Current day information
    current_day_of_week = current_datetime.weekday()  # Monday = 0, Sunday = 6

    # Handling special cases for "Today" or "Tonight"
    if "Overnight" in period_name or "Today" in period_name or "Tonight" in period_name:
        period_date = current_datetime.strftime('%Y-%m-%d')
    else:
        # Map day names to days ahead (relative to the current day)
        days_ahead = {
            "Sunday": (6 - current_day_of_week) % 7,  # Days until next Sunday
            "Monday": (7 - current_day_of_week) % 7 + 1,  # Days until next Monday
            "Tuesday": (8 - current_day_of_week) % 7 + 1,  # Days until next Tuesday
            "Wednesday": (9 - current_day_of_week) % 7 + 1,  # Days until next Wednesday
            "Thursday": (10 - current_day_of_week) % 7 + 1,  # Days until next Thursday
            "Friday": (11 - current_day_of_week) % 7 + 1,  # Days until next Friday
            "Saturday": (12 - current_day_of_week) % 7 + 1,  # Days until next Saturday
        }

        # Extract the day name from the period (e.g., "Sunday Night" -> "Sunday")
        day_name = period_name.split()[0]
        if day_name in days_ahead:
            # Calculate the date for that day based on how many days ahead it is
            period_date = (current_datetime + timedelta(days=days_ahead[day_name])).strftime('%Y-%m-%d')
        else:
            period_date = current_datetime.strftime('%Y-%m-%d')  # Default to current date if no match

    # Return date, time, and time of day
    return period_date, time_part, time_of_day

# Step 4: Function to get the weather forecast for a stadium
def fetch_weather_for_stadium(stadium_name, lat, lon, team_name, headers):
    try:
        print(f"Fetching weather for {stadium_name}...")

        # Get gridpoint for the stadium
        gridpoint_url = f"https://api.weather.gov/points/{lat},{lon}"
        grid_response = requests.get(gridpoint_url, headers=headers)
        
        if grid_response.status_code != 200:
            print(f"Failed to retrieve gridpoint data for {stadium_name}: {grid_response.status_code}")
            return

        grid_data = grid_response.json()
        forecast_url = grid_data['properties']['forecast']

        # Get the actual forecast
        forecast_response = requests.get(forecast_url, headers=headers)
        if forecast_response.status_code != 200:
            print(f"Failed to retrieve forecast data for {stadium_name}: {forecast_response.status_code}")
            return

        forecast_data = forecast_response.json()

        # Define filenames
        primary_filename = os.path.join(primary_output_folder, f"{stadium_name.lower().replace(' ', '-')}-forecast.csv")
        secondary_filename = os.path.join(secondary_output_folder, f"{stadium_name.lower().replace(' ', '-')}-forecast-{current_date}.csv")

        # Step 5: Write data to CSVs
        with open(primary_filename, mode='w', newline='') as primary_file, open(secondary_filename, mode='w', newline='') as secondary_file:
            writer_primary = csv.writer(primary_file)
            writer_secondary = csv.writer(secondary_file)

            # Write headers
            headers = ["Team", "Actual Date", "Period", "Time (Day/Night)", "Temperature", "Temperature Unit", "Wind Speed", "Wind Direction", "Detailed Forecast", "Combined Date Time", "Date Ran", "DateTime Ran"]
            writer_primary.writerow(headers)
            writer_secondary.writerow(headers)

            # Step 6: Loop through periods
            for period in forecast_data['properties']['periods']:
                period_name = period['name']
                period_temp = period['temperature']
                period_temp_unit = period['temperatureUnit']
                period_wind_speed = period['windSpeed']
                period_wind_direction = period['windDirection']
                period_forecast = period['detailedForecast']

                # Calculate period date and time based on day/night
                period_date, time_part, time_of_day = get_period_date_and_time(period_name)
                combined_datetime = f"{period_date} {time_part}"

                row = [
                    team_name, current_date, period_name, time_of_day, period_temp, period_temp_unit,
                    period_wind_speed, period_wind_direction, period_forecast, combined_datetime,
                    current_date, current_datetime_str  # Adding the new columns
                ]

                writer_primary.writerow(row)
                writer_secondary.writerow(row)

        print(f"Weather data for {stadium_name} ({team_name}) saved successfully.")

    except Exception as e:
        print(f"An error occurred while processing {stadium_name} ({team_name}): {e}")

# Step 7: Loop through all stadiums
for stadium_name, data in nfl_stadiums.items():
    fetch_weather_for_stadium(stadium_name, data['lat'], data['lon'], data['team'], headers)
