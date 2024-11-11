import pandas as pd
import os

def combine_csv_files():
    # Ask for the source directory where CSV files are located
    source_folder = input("Enter the full path to the folder containing your CSV files: ")
    
    # Check if the folder exists
    if not os.path.isdir(source_folder):
        print("The provided folder does not exist. Please try again.")
        return
    
    # Ask for the destination file paths (including filenames) for both "off" and "def" files
    off_destination_file = input("Enter the full path (including filename, e.g., combined_offense.csv) for the combined offensive CSV file: ")
    def_destination_file = input("Enter the full path (including filename, e.g., combined_defense.csv) for the combined defensive CSV file: ")
    
    # Initialize lists to hold data for offensive and defensive files
    off_data = []
    def_data = []
    
    # Iterate over each file in the folder
    for file in os.listdir(source_folder):
        if file.endswith('.csv'):
            file_path = os.path.join(source_folder, file)
            # Check if "off" is in the filename (case insensitive) for offensive files
            if 'off' in file.lower():
                print(f"Processing offensive file: {file_path}")
                off_data.append(pd.read_csv(file_path))
            # Check if "def" is in the filename (case insensitive) for defensive files
            elif 'def' in file.lower():
                print(f"Processing defensive file: {file_path}")
                def_data.append(pd.read_csv(file_path))
    
    # Combine and save the offensive files
    if off_data:
        off_combined_df = pd.concat(off_data, ignore_index=True)
        try:
            off_combined_df.to_csv(off_destination_file, index=False)
            print(f"All offensive CSV files have been combined into {off_destination_file}")
        except PermissionError:
            print("Permission denied: Unable to write to the specified offensive file path. Please check the file path and permissions.")
    else:
        print("No offensive CSV files found in the specified folder.")
    
    # Combine and save the defensive files
    if def_data:
        def_combined_df = pd.concat(def_data, ignore_index=True)
        try:
            def_combined_df.to_csv(def_destination_file, index=False)
            print(f"All defensive CSV files have been combined into {def_destination_file}")
        except PermissionError:
            print("Permission denied: Unable to write to the specified defensive file path. Please check the file path and permissions.")
    else:
        print("No defensive CSV files found in the specified folder.")

# Main loop to repeat the process if needed
while True:
    combine_csv_files()
    # Ask if the user wants to process more files
    more_files = input("Do you have other files to process? (yes/no): ").strip().lower()
    if more_files != 'yes':
        print("Script has completed.")
        break



