import os
import re
import tweepy
import pandas as pd
from telethon import TelegramClient
from textblob import TextBlob
import os
import pandas as pd

# Base API url, your Gateway API token and a phone number
BASE_URL = 'https://gatewayapi.telegram.org/'
TOKEN = 'AAEFAAAAQKI_mDsJppSEQRr3kLOz9SatBxq48BgQLSHLRv'
PHONE = '+391234567890'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}




# Telegram API credentials
API_ID = '24712771'
API_HASH = '4402ab5bbde13bfdfe36b1016b07895d'
PHONE_NUMBER = '+918369713235'


# Twitter API credentials
TWITTER_API_KEY = 'b4VxwHdtfzJuS1QjDeVl89A6Z'
TWITTER_API_SECRET = '0fvmIr6Z8W7Ls3IkDkdEFPFks089SrgyZ4Voo4JoZEY4Hq2nmT'
TWITTER_ACCESS_TOKEN = '997431273734815744-i75LB5ItFuwqgqgZbaVv5duL5EUrHxb'
TWITTER_ACCESS_TOKEN_SECRET = 'VqjYf8j2mRPHt59Iqb8PvSnYHVZjyO4Hjoaj36TEGzAe4'
# Initialize Telegram client
telegram_client = TelegramClient('session_name', API_ID, API_HASH)

# Initialize Twitter client
auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET,
                                  TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_client = tweepy.API(auth)

# List of NSE 500 company names (for demonstration purposes)
#nse_companies = ['Company1', 'Company2', 'Company3']

import pandas as pd

# Load the CSV file
nifty500_df = pd.read_csv('ind_nifty500list.csv')

# Extract company names and symbols for the first few companies (for demonstration)
nse_companies = nifty500_df[['Company Name', 'Symbol']]

# Print the list
print(nse_companies)


# Telegram channels to scrape
telegram_channels = [
    'Companyupdate',
    'researchreportss',
    'btsreports',
    'aoiventuresltd',
    'ipoinfo3',
]

# Twitter accounts to scrape
twitter_accounts = [
    'drprashantmish6',
    'SoundOffoicfinance',
    'Sudheep8531',
    'BeatTheStreet10',
    'AI_Feb21',
    'LearningEleven',
    'caniravkaria',
    'MarketScientist',
    'alchemist1320',
    'unseenvalue',
    'nid_rockz',
    'safiranand',
    'dhandhoinves',
    'wegro_app'
]

def extract_telegram_data():
    telegram_data = []
    with telegram_client:
        for channel in telegram_channels:
            try:
                for message in telegram_client.iter_messages(channel, limit=100):
                    print("message",message)
                    for company in nse_companies:
                        print("nse_companies",nse_companies)
                        if  r"(?:Company:|Parent Company:)\s*([A-Za-z\s]+)":
                            print("nse_companies",nse_companies)
                            telegram_data.append({
                                'source': 'Telegram',
                                'company': company,
                                'content': message.message,
                                'date': message.date
                            })
                            # Combine data into DataFrame
                            data = telegram_data 
                            df = pd.DataFrame(data)
                            print(df,"telegram_data")
            except Exception as e:
                print(f"Error extracting from telegram {channel}: {e}")
    return df

def extract_twitter_data():
    twitter_data = []
    for account in twitter_accounts:
        try:
            tweets = twitter_client.user_timeline(screen_name=account, count=100, tweet_mode='extended')
            for tweet in tweets:
                for company in nse_companies:
                    if re.search(r'\b' + re.escape(company) + r'\b', tweet.full_text, re.IGNORECASE):
                        twitter_data.append({
                            'source': 'Twitter',
                            'company': company,
                            'content': tweet.full_text,
                            'date': tweet.created_at 
                        })
        except Exception as e:
            print(f"Error extracting from twitter {account}: {e}")
           
    return twitter_data 

# Extract data
telegram_data = extract_telegram_data()
#twitter_data = extract_twitter_data()

# Combine data into DataFrame
data = telegram_data



df = pd.DataFrame(data)

# Check if data extraction was successful
if df.empty:
    print("No data extracted.")
else:
    print(f"Extracted {len(df)} records.")

    



