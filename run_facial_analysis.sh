#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <folder_name>"
  exit 1
fi

# run facial attribute analysis on /frames folder - outputting a score
COMPANY=$1

for folder in $COMPANY/splits/*/; do
  echo $folder
  python 'facial_attribute_script.py' "$COMPANY/base_photo.jpeg" "${folder}frames/" "${folder}"
done
