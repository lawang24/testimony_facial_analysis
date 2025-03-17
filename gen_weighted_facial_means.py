import os
import sys
import pandas as pd
import ast


def generate_emotion_data_points(folder_path, output, segment_name, company_directory):
    facial_analysis_data_path = os.path.join(
        folder_path, "analysis_results_emotions.csv"
    )

    if not os.path.exists(facial_analysis_data_path):
        return output

    df = pd.read_csv(facial_analysis_data_path)

    # Define emotion polarity
    emotion_score_map = {
        "angry": -1,
        "disgust": -1,
        "fear": -1,
        "sad": -1,
        "happy": 1,
        "surprise": 1,
        "neutral": 0,
    }
    # Step 1 - Collect emotion scores into a list
    # Neutral emotion doesn't count
    emotion_score = 0

    for emotion in df["dominant_emotion"]:
        emotion_score += emotion_score_map[emotion]

    # Step 3 - Build the dataframe entry (row) for this segment and company
    dataframe_entry = {
        "segment": segment_name,
        "company": company_directory,
        "emotion_score": emotion_score / df["dominant_emotion"].count(),
        "emotional_entry_count": df["dominant_emotion"].count(),
    }

    # Step 4 - Create DataFrame
    emotion_df = pd.DataFrame([dataframe_entry])
    output = pd.concat([output, emotion_df], ignore_index=True)

    return output


def generate_data_points(company_directory_path, company_dir_name):
    splits_folder = os.path.join(company_directory_path, "splits")
    if not os.path.isdir(splits_folder):
        print(f"Error: The directory {splits_folder} does not exist.")
        return

    # Creating an empty DataFrame with the specified columns
    columns = ["company", "segment", "emotion_score", "emotional_entry_count"]
    df = pd.DataFrame(columns=columns)

    for root, dirs, _ in os.walk(splits_folder):
        for curr_dir in dirs:
            print("Processing segment:", curr_dir)
            folder_path = os.path.join(root, curr_dir)
            df = generate_emotion_data_points(
                folder_path, df, curr_dir, company_dir_name
            )
        break  # Only process the top-level directories (segments)

    df.to_csv(f"{company_directory_path}/weighted_emotion_scores.csv", index=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python emotion_multi_regression.py <company_directory>")
    else:
        company_directory = sys.argv[1]
        generate_data_points(f"data/{company_directory}", company_directory)
