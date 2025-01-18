#!/bin/bash

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <company> <video_url>"
  exit 1
fi

COMPANY=$1
VIDEO_URL=$2

# Download video and audio files
mkdir -p "$COMPANY"
cd "$COMPANY"
yt-dlp -f "bv,ba" -o "$%(title)s.f%(format_id)s.%(ext)s" "$VIDEO_URL"

echo 'Done splitting frames for each split..'

cd ..


# transcribe audio segments using whisper model

# run sentiment analysis on transcribed segments - outputting a score 
# Options: hugginface/transformers, NLTK VADER, TextBlob

# get stock price movement data


# cleanup 
# cd ..
# rmdir 'split_audios/'

# # Split the video into 1-second frames using ffmpeg
# echo "Splitting the video into 1-second frames..."
# mkdir -p "$OUTPUT_FOLDER/frames"
# ffmpeg -i "$MERGED_VIDEO" -vf fps=1 "$OUTPUT_FOLDER/frames/frame_%05d.png"

# # # Notify the user of completion
# echo "All files have been saved in the '$OUTPUT_FOLDER' directory."