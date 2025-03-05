import os
import re
import json


# Function to extract topic from a given file
def extract_pattern_from_file(file_path):
    print(f"Extracting data from file: {file_path}")
    pattern = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if pattern is None:  # Assuming the topic appears first in the file
                    pattern_match = re.search(r'Final pattern output: (.+)', line)
                    if pattern_match:
                        pattern = pattern_match.group(1)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return pattern


# Function to traverse directories and process files
def extract_data_from_directory(root_dir):
    print(f"Traversing directory: {root_dir}")
    output_data = {}
    for subdir, _, files in os.walk(root_dir):
        subdir_name = os.path.basename(subdir)
        output_data[subdir_name] = {}
        for file in files:
            file_path = os.path.join(subdir, file)
            e_pattern = extract_pattern_from_file(file_path)
            output_data[subdir_name][file] = {
                "pattern": e_pattern if e_pattern else "N/A",
            }
    return output_data


def main():
    print("Starting data extraction...")
    # Specify the root directory
    root_directory = './Output'

    # Extract data
    pattern = extract_data_from_directory(root_directory)

    # Print extracted data
    # print("Extracted Data:")
    # print(json.dumps(pattern, indent=4))

    # Save the extracted data to an output file
    output_file = 'extracted_pattern.json'
    try:
        with open(output_file, 'w') as file:
            json.dump(pattern, file, indent=4)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving data to file {output_file}: {e}")


if __name__ == '__main__':
    main()
