#!/bin/bash

# Define the data folder and the Python script
DATA_FOLDER="data"

# Check if the data folder exists
if [ ! -d "$DATA_FOLDER" ]; then
    echo "Error: Data folder '$DATA_FOLDER' does not exist."
    exit 1
fi

# Exit on any error
set -e

# Iterate over all directories in the data folder
for folder in "$DATA_FOLDER"/*/; do
    # Remove trailing slash to get the folder name
    folder_name=$(basename "$folder")
    echo "Processing folder: $folder_name"
    
    # Run the Python script with the folder name as an argument
    python "gen_weighted_facial_means.py" "$folder_name"

    python "concat_all_data.py" "$folder_name"


done
