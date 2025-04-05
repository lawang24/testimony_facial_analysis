import os
import sys
from transformers import pipeline
import pandas as pd

def split_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # silence defaults to "Thank you and Hello"
            cleaned_sentences = [sentence.strip() for sentence in content.split('.') if sentence.strip() and sentence.strip() not in {"Thank you", "Hello"}]
        return cleaned_sentences
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"

def run_sentiment_analysis(company_directory, folder_name):
   
    # Ensure the company directory exists
    splits_folder = os.path.join(folder_name,company_directory, "splits")
    if not os.path.isdir(splits_folder):
        print(f"Error: The directory {splits_folder} does not exist.")
        return
    
    classifier = pipeline('sentiment-analysis')
    
    # Iterate over all subdirectories in 'splits', analyzing the {segment}_transcription.txt file
    
    for root, dirs, files in os.walk(splits_folder):
        for curr_dir in dirs:
            print("Processing segment:", curr_dir)
            
            folder_path = os.path.join(root, curr_dir)

            # get the transcription file
            for segment_root, _, files in os.walk(folder_path):
                
                for file in files:
                    if file.endswith("transcription.txt"):
                        file_path = os.path.join(segment_root, file)
                        break
                if file_path == "":
                    raise RuntimeError("No transcription file found")
                break
            
            sentences = split_text_file(file_path)
            
            try:
                results = classifier(sentences)
                data = {
                "Text": sentences,
                "Label": [result['label'] for result in results],
                "Score": [result['score'] for result in results]
            }
                df = pd.DataFrame(data)
                # Export to CSV
                output_file_path = os.path.join(folder_path, f"{curr_dir}_sentence_sentiment.csv")
                df.to_csv(output_file_path, index=False)
                
            except RuntimeError as e:
                print(f"An error occurred in {curr_dir}: {e}")
            
            
        # only do at top level to traverse through segments, don't recurse into segments
        break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <company_directory> <folder>")
    else:
        company_directory = sys.argv[1]
        folder_name = sys.argv[2]
        
        run_sentiment_analysis(company_directory, folder_name)
