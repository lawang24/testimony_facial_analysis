import pandas as pd
import argparse
import os
from datetime import datetime, timedelta

def load_and_prepare_data(folder, start_time_str):
    csv_file = os.path.join(folder, 'stock_data.csv')
    
    # Load the data
    df = pd.read_csv(csv_file)
    
    # Drop rows where ASK is 0
    df = df[df['ASK'] != 0]

    # Combine DATE and TIME_M into a single datetime column
    df['timestamp'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])

    # Extract the single date present (since there's only one date in the file)
    unique_date = df['DATE'].iloc[0]

    # Combine that date with the provided starting time
    start_time = pd.to_datetime(f"{unique_date} {start_time_str}")

    return df, start_time

def compute_segments(df, company_name, start_time):
    results = []
    segment_count = 0

    while not df.empty:
        # Each segment is 30 minutes long
        end_time = start_time + timedelta(minutes=30)

        # Extract this 30-minute window
        segment_df = df[(df['timestamp'] >= start_time) & (df['timestamp'] < end_time)].copy()
        
        if segment_df.empty:
            break

        # Group by minute and average ASK per minute
        segment_df['minute'] = segment_df['timestamp'].dt.floor('min')  # Floor to minute
        minute_averages = segment_df.groupby('minute')['ASK'].mean().reset_index()

        # First and last minute's average ASK price
        first_ask = minute_averages['ASK'].iloc[0]
        last_ask = minute_averages['ASK'].iloc[-1]
        print(first_ask, last_ask, segment_count)

        pct_diff = (last_ask - first_ask) / first_ask * 100

        # Segment label (output001, output002, etc.)
        segment_label = f"output{segment_count:03d}"

        results.append({
            'segment': segment_label,
            'company_name': company_name,
            'percentage_difference': pct_diff,
            'starting_time': start_time.strftime('%H:%M:%S')
        })

        # Advance to next segment
        segment_count += 1
        start_time = end_time

        # Filter df for future timestamps only
        df = df[df['timestamp'] >= start_time]

    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(description="Process stock data into 30-minute segments.")
    parser.add_argument("company_folder", type=str, help="Path to the company folder (contains stock_data.csv)")
    parser.add_argument("start_time", type=str, help="Start time (format: HH:MM:SS)")
    args = parser.parse_args()

    # Extract company name from folder name
    company_name = os.path.basename(os.path.normpath(args.company_folder))

    # Load and filter data
    df, start_time = load_and_prepare_data(args.company_folder, args.start_time)

    # Compute segments
    result_df = compute_segments(df, company_name, start_time)

    # Save to output CSV
    result_df.to_csv(f'{args.company_folder}/stock_segments.csv', index=False)

if __name__ == "__main__":
    main()
