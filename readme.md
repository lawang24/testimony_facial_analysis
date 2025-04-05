1. Download Vid (download_vid.sh)
2. Split Video into Segments (split_videos.sh)
3. Run Facial Analysis (run_facial_analysis.sh)
4. Run Transcription Process (transcription.py)
5. Run Sentiment Analysis (sentiment_analysis.py)

# data analysis
1. Generate weighted facial means per section (gen_weighted_facial_means.py)
2. Generate weighted sentiment means per section (gen_sentiment_means.py)
3. Get stock_data.csv from WRDS
4. Calculate stock percentage movements per segment (process_stock_data.py)
5. Concatenate facial, sentiment, and stock data (concat_all_data.py)

# regressions
1. look at single emotion (single_emotion_regression.ipynb)