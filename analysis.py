import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('zuckerberg_analysis_results.csv')

# Count occurrences of different values in each column
for column in df.columns:
    print(f"Value counts for {column}:")
    print(df[column].value_counts())
    print()