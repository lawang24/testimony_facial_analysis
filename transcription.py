import os
import sys
import whisper


def transcribe_audio_files(company_directory, audio_extension):
    # Ensure the company directory exists
    splits_folder = os.path.join(company_directory, "splits")
    if not os.path.isdir(splits_folder):
        print(f"Error: The directory {splits_folder} does not exist.")
        return

    # Load the Whisper model
    model = whisper.load_model("turbo")  

    # Iterate over all subdirectories in 'splits'
    for root, dirs, files in os.walk(splits_folder):
        for curr_dir in dirs:
            folder_path = os.path.join(root, curr_dir)

            # get the audio path
            for segment_root, _, files in os.walk(folder_path):
                file_path = ""
                for file in files:
                    if file.endswith(f".{audio_extension}"):
                        file_path = os.path.join(segment_root, file)
                        break
                if file_path == "":
                    raise RuntimeError("No audio file found")
                break

            result = model.transcribe(file_path, verbose=True, language='en')

            # write result into file
            output_file_name = f"{curr_dir}_transcription.txt"
            output_file_path = os.path.join(folder_path, output_file_name)
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(result["text"])

        # only do top level, no recursive
        break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <company_directory> <audio_extension>")
    else:
        company_directory = sys.argv[1]
        audio_extension = sys.argv[2]
        transcribe_audio_files(company_directory, audio_extension)
