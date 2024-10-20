import subprocess

# List of scripts to run in sequence (no SQL appending script)
scripts = [
    "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/scripts/web-scrapers/nfl-com/nfl-com-team-scraper.py",
    "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/scripts/weather/nfl-stadiums-weather-api.py",  # Update the path if necessary
    "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/scripts/weather/all-nfl-stadiums-weather.py"  # Update the path if necessary
]

for script in scripts:
    try:
        print(f"Running script: {script}")
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
        print(f"Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running script {script}:\n{e.stderr}")
