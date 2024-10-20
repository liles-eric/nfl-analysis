import os
import csv

# Path where the individual stadium forecast CSV files are stored
input_folder = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/weather/"

# Path for the combined output file
combined_filename = os.path.join(input_folder, "all-nfl-stadiums-weather-forecasts.csv")

# Step 1: List all CSV files in the input folder, exclude the combined file
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv') and 'combined' not in f]

# Step 2: Combine all CSV files into one
with open(combined_filename, mode='w', newline='') as combined_file:
    writer_combined = csv.writer(combined_file)
    header_written = False

    for file in csv_files:
        file_path = os.path.join(input_folder, file)

        # Step 3: Read each individual CSV file
        with open(file_path, mode='r', newline='') as individual_file:
            reader = csv.reader(individual_file)

            # Check if the file is empty by attempting to get the header
            try:
                header = next(reader)  # Try to read the header

                # Only write the header if it hasn't been written yet
                if not header_written:
                    writer_combined.writerow(header)  # Write the header once
                    header_written = True

                # Write the remaining content of the file to the combined file
                for row in reader:
                    writer_combined.writerow(row)

            except StopIteration:
                print(f"File {file} is empty or has no valid content, skipping.")
                continue

print(f"All individual weather files have been combined into {combined_filename}")

