#!/bin/bash

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <company> <video_url>"
  exit 1
fi

COMPANY=$1
VIDEO_URL=$2

# Download video and audio files
mkdir -p "data/$COMPANY"
cd "$COMPANY"
yt-dlp -f "bv,ba" -o "$%(title)s.f%(format_id)s.%(ext)s" "$VIDEO_URL"

