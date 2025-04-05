import os
import sys
import pandas as pd

def merge_data(company, folder):
    # 1) Identify current script directory and target folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, folder, company)

    # 2) Identify file paths
    emotional_file = os.path.join(folder_path, "weighted_emotion_scores.csv")
    segment_file = os.path.join(folder_path, "segment_sentiment_means.csv")
    stock_segments_file = os.path.join(folder_path, "stock_segments.csv")
    final_data_file = os.path.join(current_dir, "final_weighted_data.csv")

    # 3) Read the two main CSV files into dataframes
    emotional_df = pd.read_csv(emotional_file)
    segment_df = pd.read_csv(segment_file)

    # 4) Merge these two dataframes on 'company' and 'segment'
    combined_df = pd.merge(emotional_df, segment_df, on=["company", "segment"], how="outer")

    # 5) Read and merge the stock segments data
    #    Rename 'company_name' to 'company' to match your existing data
    stock_df = pd.read_csv(stock_segments_file)
    stock_df.rename(columns={"company_name": "company"}, inplace=True)

    # We only need to join on ['segment', 'company']
    # Use a left join to keep all existing rows, and fill in percentage_difference (and starting_time) if they match
    combined_df = pd.merge(
        combined_df,
        stock_df[["segment", "company", "percentage_difference", "starting_time"]],
        on=["segment", "company"],
        how="left"
    )

    # 6) Check if final_data.csv already exists
    if os.path.exists(final_data_file):
        # 6a) Read existing final_data
        final_df = pd.read_csv(final_data_file)

        # 6b) Merge final_data with the newly combined data
        merged_final = pd.merge(
            final_df,
            combined_df,
            on=["company", "segment"],
            how="outer",
            suffixes=("", "_new")
        )

        # 6c) If any columns appear both in old final_data and combined_df,
        #     handle them by preferring the new data when it's not NaN
        for col in merged_final.columns:
            if col.endswith("_new"):
                original_col = col[:-4]  # remove "_new"
                # Use combine_first() to prefer new data if it's available
                merged_final[original_col] = merged_final[col].combine_first(merged_final[original_col])
                merged_final.drop(columns=[col], inplace=True)

        final_df = merged_final
    else:
        # 6d) If no final_data.csv, just use combined_df as our final
        final_df = combined_df

    # 7) Write out the updated final data to final_data.csv
    final_df.to_csv(final_data_file, index=False)
    print(f"Data merged successfully! File saved as {final_data_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_data.py <company> <folder>")
        sys.exit(1)

    company = sys.argv[1]
    folder = sys.argv[2]
    merge_data(company, folder)
