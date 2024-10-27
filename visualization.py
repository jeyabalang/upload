import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot sentiment analysis for each company
def plot_sentiment_for_each_company(df, output_dir='sentiment_plots'):
    """
    Plots sentiment analysis results for each company in the provided DataFrame.

    Args:
    - df (pd.DataFrame): DataFrame containing sentiment results with 'company_name' and 'sentiment_category' columns.
    - output_dir (str): Directory to save the sentiment plots. Defaults to 'sentiment_plots'.
    """
    # Check for required columns
    required_columns = ['company_name', 'sentiment_category']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"DataFrame must contain '{col}' column.")

    # Create a directory to save sentiment plots
    os.makedirs(output_dir, exist_ok=True)

    # Define a color map for sentiment categories
    color_map = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'grey',
        # Add more sentiment categories if needed
    }

    # Group the DataFrame by company
    grouped = df.groupby('company_name')

    for company_name, company_data in grouped:
        # Count the occurrences of each sentiment category for this company
        sentiment_counts = company_data['sentiment_category'].value_counts()

        # Ensure the sentiment categories have corresponding colors
        colors = [color_map.get(sentiment, 'blue') for sentiment in sentiment_counts.index]

        # Create a bar plot for this company's sentiment
        plt.figure(figsize=(10, 5))
        sentiment_counts.plot(kind='bar', color=colors)

        # Add titles and labels
        plt.title(f'Sentiment Analysis for {company_name}', fontsize=14)
        plt.xlabel('Sentiment Category', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot as an image file
        plot_filename = os.path.join(output_dir, f'{company_name}_sentiment_analysis.png')
        plt.savefig(plot_filename)
        plt.close()  # Close the figure to avoid display overlap during iteration
        
        print(f'Sentiment plot saved for {company_name} at {plot_filename}')

# Load company data from ind_nifty500list.csv
company_data_path = os.path.join('data', 'ind_nifty500list.csv')
companies_df = pd.read_csv(company_data_path)
companies_df = companies_df[['Company Name', 'Symbol']]  # Only select relevant columns
companies_df.columns = ['company_name', 'symbol']  # Rename columns for consistency

# Example DataFrame containing sentiment analysis results for multiple companies
# Here, you'll want to replace this example data with the actual sentiment results you generate
sentiment_results = [
    {'company_name': 'Company A', 'sentiment_category': 'positive'},
    {'company_name': 'Company A', 'sentiment_category': 'negative'},
    {'company_name': 'Company B', 'sentiment_category': 'neutral'},
    {'company_name': 'Company B', 'sentiment_category': 'positive'},
    {'company_name': 'Company C', 'sentiment_category': 'negative'}
]

# Convert sentiment results to DataFrame
df_sentiment = pd.DataFrame(sentiment_results)

# Plot the sentiment analysis results for each company
plot_sentiment_for_each_company(df_sentiment)

# Optional: Save insights to a CSV file for reporting
insights = df_sentiment  # Assuming insights DataFrame is based on your sentiment analysis
insights.to_csv('reports_nse500_insights.csv', index=False)
