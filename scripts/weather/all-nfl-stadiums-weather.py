import os
import csv

# Path where the individual stadium forecast CSV files are stored
input_folder = "C:/Users/liles/OneDrive/Documents/GitHub/nfl-analysis/data/weather/"

# Path for the combined output file
combined_filename = os.path.join(input_folder, "all-nfl-stadiums-weather-forecasts.csv")

# Step 1: List all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv') and 'combined' not in f]

# Step 2: Combine all CSV files into one
with open(combined_filename, mode='w', newline='') as combined_file:
    writer_combined = csv.writer(combined_file)
    header_written = False

    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        
        # Step 3: Check if the file is empty
        if os.path.getsize(file_path) == 0:
            print(f"File {file} is empty, skipping.")
            continue

        # Step 4: Read each individual CSV file and check for valid rows
        with open(file_path, mode='r', newline='') as individual_file:
            reader = csv.reader(individual_file)
            header = next(reader, None)  # Get header from the file

            # Check if the header is valid and file has more than just a header
            if header and len(header) > 0:
                if not header_written:
                    writer_combined.writerow(header)  # Write the header to the combined file once
                    header_written = True

                # Write the content of the file to the combined file if valid rows exist
                rows_written = False
                for row in reader:
                    if any(row):  # Check if the row is not empty
                        writer_combined.writerow(row)
                        rows_written = True

                if not rows_written:
                    print(f"File {file} has no valid content, skipping.")
            else:
                print(f"File {file} is empty or has no valid header, skipping.")

print(f"All individual weather files have been combined into {combined_filename}")


