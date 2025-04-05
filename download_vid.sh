#!/bin/bash

set -e

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: $0 <company> <video_url> <folder>"
  exit 1
fi

COMPANY=$1
VIDEO_URL=$2
FOLDER=$3

# Download video and audio files
mkdir -p "$FOLDER/$COMPANY"
cd "$FOLDER/$COMPANY"
yt-dlp -f "bv,ba" -o "$%(title)s.f%(format_id)s.%(ext)s" "$VIDEO_URL"

