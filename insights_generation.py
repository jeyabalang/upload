import os
import pandas as pd
from src.sentiment_analysis import analyze_sentiment

# Function to categorize data based on content
def categorize_data(df):
    """
    Categorizes each row of the DataFrame based on the content.

    Args:
    - df (pd.DataFrame): DataFrame containing the sentiment results with 'content' column.

    Returns:
    - pd.DataFrame: The original DataFrame with an additional 'category' column.
    """
    # Define categorization keywords
    category_keywords = {
        'Company Performance': ['performance'],
        'Management Updates': ['management'],
        'Growth Outlook': ['growth'],
        'Risk Factors': ['risk'],
        'Market Sentiment': []  # Default category
    }
    
    def categorize_row(row):
        content = row['content'].lower()
        for category, keywords in category_keywords.items():
            if any(keyword in content for keyword in keywords):
                return category
        return 'Market Sentiment'  # Default if no keywords match
    
    # Check if 'content' column exists
    if 'content' not in df.columns:
        raise ValueError("The DataFrame must contain a 'content' column for categorization.")

    # Apply the categorize_row function to each row and create a new 'category' column
    df['category'] = df.apply(categorize_row, axis=1)
    return df

# Function to generate insights based on categories and sentiment
def generate_insights(df):
    """
    Generates insights based on sentiment analysis results categorized by company and content type.

    Args:
    - df (pd.DataFrame): DataFrame containing categorized sentiment analysis results.

    Returns:
    - pd.DataFrame: A DataFrame containing insights with counts and average sentiment.
    """
    # Check required columns
    required_columns = ['company_name', 'category', 'sentiment']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The DataFrame must contain a '{col}' column for insights generation.")

    # Generate insights
    insights = df.groupby(['company_name', 'category']).agg({
        'content': 'count',     # Count the number of messages per category
        'sentiment': 'mean'     # Get the average sentiment score for each category
    }).reset_index()
    
    # Rename columns for clarity
    insights.columns = ['Company Name', 'Category', 'Message Count', 'Average Sentiment']
    
    return insights
