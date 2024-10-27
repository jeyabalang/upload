import pandas as pd
from textblob import TextBlob

def analyze_sentiment(df):
    # Check if the DataFrame has a 'message' column
    if 'message' not in df.columns:
        raise ValueError("The DataFrame must contain a 'message' column for sentiment analysis.")
    
    # Function to analyze sentiment
    def analyze_text(text):
        if pd.isna(text):  # Handle missing messages
            return None, 'missing'
        analysis = TextBlob(text)
        return analysis.sentiment.polarity, analysis.sentiment.subjectivity

    # Apply the analyze_text function to the 'message' column
    df[['sentiment', 'subjectivity']] = df['message'].apply(lambda x: pd.Series(analyze_text(x)))

    # Define sentiment labels based on polarity
    def get_sentiment_label(polarity):
        if polarity is None:
            return 'unknown'
        elif polarity > 0:
            return 'positive'
        elif polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # Assign sentiment labels
    df['sentiment_label'] = df['sentiment'].apply(get_sentiment_label)

    # Optional: Add more granular sentiment categorization based on subjectivity
    def categorize_sentiment(row):
        try:
            polarity = float(row['sentiment'])
            subjectivity = float(row['subjectivity'])
        except (ValueError, TypeError):
            return 'Unknown'  # Handle non-numeric or missing values
        
        if polarity > 0:
            return 'Highly Positive' if subjectivity > 0.5 else 'Mildly Positive'
        elif polarity < 0:
            return 'Highly Negative' if subjectivity > 0.5 else 'Mildly Negative'
        else:
            return 'Neutral'

    # Add granular sentiment category
    df['granular_sentiment_label'] = df.apply(categorize_sentiment, axis=1)

    return df
