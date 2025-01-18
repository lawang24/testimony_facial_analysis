#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
  echo "Usage: $0 <company> <video_extension> <audio_extension> <segment_length>"
  exit 1
fi

# Window length of analysis (seconds)
COMPANY=$1
VIDEO_EXTENSION=$2
AUDIO_EXTENSION=$3
SEGMENT_LENGTH=$4

# Split downloaded video
cd $COMPANY
mkdir "splits"
ffmpeg -i *.${VIDEO_EXTENSION} -c copy -map 0 -f segment -segment_time $SEGMENT_LENGTH -reset_timestamps 1 "splits/output%03d.${VIDEO_EXTENSION}"

# Split downloaded audio 
# MAKE SURE EXTENSION ALIGNS
mkdir 'split_audios'
ffmpeg -i *.${AUDIO_EXTENSION} -f segment -segment_time $SEGMENT_LENGTH -c copy -reset_timestamps 1 "split_audios/output%03d.${AUDIO_EXTENSION}"
cd "splits"

# Group corresponding audio and video segments into folders
for segment in *.${VIDEO_EXTENSION}; do
  segment_name="${segment%.$VIDEO_EXTENSION}"
  mkdir -p "$segment_name"
  mv "$segment" "$segment_name/"
  mv "../split_audios/${segment_name}.${AUDIO_EXTENSION}" "$segment_name/"
done

cd ..

# break video into frames for facial attribute analysis
for folder in splits/*/; do
  echo "Processing folder: $folder"
  mkdir "${folder}/frames"
  file_name=$(ls ${folder}/*.${VIDEO_EXTENSION})
  ffmpeg -i $file_name -vf fps=1 "${folder}/frames/frame_%05d.png"
done

rm -rf split_audios

