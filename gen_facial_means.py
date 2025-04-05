import os
import sys
from transformers import pipeline
import pandas as pd
import ast
import collections


def generate_emotion_data_points(folder_path, output, segment_name, company_directory):

    facial_analysis_data_path = os.path.join(
        folder_path, "analysis_results_emotions.csv"
    )

    if not os.path.exists(facial_analysis_data_path):
        return output

    # Load the DataFrame from a CSV file
    df = pd.read_csv(facial_analysis_data_path)

    def parse_dict(entry):
        if isinstance(entry, str):
            return ast.literal_eval(
                entry
            )  # Convert string representation of dict to an actual dict
        return entry

    # Apply the function to the 'emotion' column
    df["emotion_dict"] = df["emotion"].apply(parse_dict)

    # Step 1 - Collect emotion scores into a defaultdict of lists (same as before)
    emotional_values = collections.defaultdict(list)
    for dict_entry in df["emotion_dict"]:
        for emotion, score in dict_entry.items():
            emotional_values[emotion].append(score)

    # Step 2 - Compute mean for each emotion
    emotion_means = {emotion: sum(values) / len(values) for emotion, values in emotional_values.items()}

    # Step 3 - Build the dataframe entry (row) for this segment and company
    dataframe_entry = {"segment": segment_name, "company": company_directory, "emotional_entry_count": len(list(emotional_values.values())[0])}
    dataframe_entry.update(emotion_means)

    # Step 4 - Create DataFrame
    emotion_df = pd.DataFrame([dataframe_entry])

    output = pd.concat([output, pd.DataFrame(emotion_df)], ignore_index=True)

    return output


def generate_data_points(company_directory):

    # Ensure the company directory exists
    splits_folder = os.path.join(company_directory, "splits")
    if not os.path.isdir(splits_folder):
        print(f"Error: The directory {splits_folder} does not exist.")
        return

    # Iterate over all subdirectories in 'splits'
    # 1. Cumulative score for transcription from {segment}_sentence_sentiment.csv
    # 2. Cumulative score for facial analysis from analysis_results.csv

    # Creating an empty DataFrame with the specified columns
    columns = [
        "company",
        "segment",
        "angry",
        "disgust",
        "fear",
        "happy",
        "neutral",
        "sad",
        "surprise",
    ]

    df = pd.DataFrame(columns=columns)

    for root, dirs, files in os.walk(splits_folder):
        for curr_dir in dirs:
            print("Processing segment:", curr_dir)
            folder_path = os.path.join(root, curr_dir)
            df = generate_emotion_data_points(
                folder_path, df, curr_dir, company_directory
            )

        # only do at top level to traverse through segments, don't recurse into segments
        break

    df.to_csv(
        f"{company_directory}/emotion_separated_means.csv", index=False
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python emotion_multi_regression.py <company_directory>")
    else:
        company_directory = sys.argv[1]
        generate_data_points(company_directory)