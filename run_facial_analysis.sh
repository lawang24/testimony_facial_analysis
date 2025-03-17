#!/bin/bash
set -e

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <folder_name> <data_folder>"
  exit 1
fi

# run facial attribute analysis on /frames folder - outputting a score
COMPANY=$1
DATA_FOLDER=$2

for folder in $DATA_FOLDER/$COMPANY/splits/*/; do
  echo $folder
  python 'extract_facial_attribute.py' "$DATA_FOLDER/$COMPANY/base_photo.jpeg" "${folder}frames/" "${folder}"
done
