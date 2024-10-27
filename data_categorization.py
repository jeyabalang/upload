import pandas as pd

def categorize_data(sentiment_results):
    categorized_data = {}

    for result in sentiment_results:
        try:
            company_name = result['company_name']
            sentiment = result['sentiment']  # 'positive', 'negative', or 'neutral'
            mention = result['mention']  # Text of the mention
        except KeyError as e:
            print(f"Missing key in result: {e}")
            continue  # Skip this iteration if keys are missing

        # If the company is not already in categorized_data, add it
        if company_name not in categorized_data:
            categorized_data[company_name] = {
                'positive_mentions': 0,
                'negative_mentions': 0,
                'neutral_mentions': 0,
                'mentions': []
            }

        # Increment sentiment counts and add mentions
        if sentiment == 'positive':
            categorized_data[company_name]['positive_mentions'] += 1
        elif sentiment == 'negative':
            categorized_data[company_name]['negative_mentions'] += 1
        elif sentiment == 'neutral':
            categorized_data[company_name]['neutral_mentions'] += 1
        
        # Add the mention text along with its sentiment
        categorized_data[company_name]['mentions'].append({
            'mention': mention,
            'sentiment': sentiment
        })

    # Convert the dictionary to a DataFrame for easier analysis
    categorized_df = pd.DataFrame.from_dict(categorized_data, orient='index').reset_index()
    categorized_df.rename(columns={'index': 'company_name'}, inplace=True)
    
    return categorized_df
