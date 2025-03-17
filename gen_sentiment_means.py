import os
import sys
from transformers import pipeline
import pandas as pd
import ast
import re


def generate_sentiment_analysis_points(
    folder_path, output, segment_name, company_directory
):
    sentiment_analysis_data_path = os.path.join(
        folder_path, f"{segment_name}_sentence_sentiment.csv"
    )
    
    if not os.path.exists(sentiment_analysis_data_path):
        return output

    # Load the DataFrame from a CSV file
    df = pd.read_csv(sentiment_analysis_data_path)
    existing_entries = len(df.index)

    sentiment_scores = {
        "POSITIVE": 1,
        "NEGATIVE": -1,
    }

    # Map the sentiment scores to the Label column
    df["mapped_score"] = df["Label"].map(sentiment_scores).fillna(0)

    # Create new data
    new_data = {
        "company": [company_directory] * existing_entries,  # Custom company names
        "segment": [segment_name] * existing_entries,  # Custom segments
        "sentiment_score": df["Score"] * df["mapped_score"],
    }

    output = pd.concat([output, pd.DataFrame(new_data)], ignore_index=True)
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
        "sentiment_score",
        "facial_attribute_score",
        "dominant_emotion",
    ]
    df = pd.DataFrame(columns=columns)
    
    for root, dirs, files in os.walk(splits_folder):
        for curr_dir in dirs:
            print("Processing segment:", curr_dir)
            folder_path = os.path.join(root, curr_dir)
            df = generate_sentiment_analysis_points(
                folder_path, df, curr_dir, company_directory
            )

        # only do at top level to traverse through segments, don't recurse into segments
        break

    # Group by 'segment' and calculate the average sentiment score
    average_sentiment_scores = (
        df.groupby(["company","segment"])["sentiment_score"].agg(["mean", "count"]).reset_index()
    )
    average_sentiment_scores.rename(
        columns={"mean": "average_sentiment_score", "count": "sentiment_entry_count"},
        inplace=True,
    )
    average_sentiment_scores.to_csv(
        f"{company_directory}/segment_sentiment_means.csv", index=False
    )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <company_directory>")
    else:
        company_directory = sys.argv[1]
        generate_data_points(company_directory)
