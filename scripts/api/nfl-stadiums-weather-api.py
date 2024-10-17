import requests
import csv
from datetime import datetime
import os

# Step 1: Define the forecast URL for Lambeau Field (Green Bay)
forecast_url = "https://api.weather.gov/points/44.5013,-88.0622"

# Step 2: Set up headers (NWS requires a User-Agent header)
headers = {
    "User-Agent": "(myweatherapp.com, contact@myweatherapp.com)"  # You can customize this
}

# Step 3: Make the GET request to the API for the location gridpoint
response = requests.get(forecast_url, headers=headers)

# Step 4: Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data to get the forecast URL
    grid_data = response.json()
    forecast_url = grid_data['properties']['forecast']

    # Now get the actual weather forecast
    forecast_response = requests.get(forecast_url, headers=headers)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()

        # Get the current date in YYYY-MM-DD format
        date_str = datetime.now().strftime('%Y-%m-%d')

        # Define the output path to the weather folder
        weather_folder = os.path.join("..", "data", "weather")
        if not os.path.exists(weather_folder):
            os.makedirs(weather_folder)

        # Define the full file path for the CSV file
        filename = os.path.join(weather_folder, f"green-bay-forecast-{date_str}.csv")

        # Step 5: Open the CSV file to write the forecast data
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["Period", "Temperature", "Temperature Unit", "Wind Speed", "Wind Direction", "Detailed Forecast"])

            # Step 6: Loop through each period and write to the CSV
            for period in forecast_data['properties']['periods']:
                writer.writerow([
                    period['name'], 
                    period['temperature'], 
                    period['temperatureUnit'], 
                    period['windSpeed'], 
                    period['windDirection'], 
                    period['detailedForecast']
                ])
        print(f"Weather data saved to {filename}")
    else:
        print(f"Failed to retrieve forecast data: {forecast_response.status_code}")
else:
    print(f"Failed to retrieve grid data: {response.status_code}")
