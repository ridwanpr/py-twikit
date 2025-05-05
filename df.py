import os
from dotenv import load_dotenv
from twikit import Client
import pandas as pd
import csv
import asyncio

load_dotenv()

def get_tweets():
    SEARCH_QUERY = 'madrid'
    SEARCH_TYPE = 'Top'
    SEARCH_LIMIT = 20
    AUTH_USER = os.getenv('AUTH_USER')
    AUTH_EMAIL = os.getenv('AUTH_EMAIL')
    AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')
    COOKIES_FILE = os.getenv('COOKIES_FILE')
    LANGUAGE = os.getenv('LANGUAGE')

    client = Client(LANGUAGE)
    
    try:
        if os.path.exists(COOKIES_FILE):
            client.load_cookies(COOKIES_FILE)
        else:
            asyncio.run(client.login(
                auth_info_1=AUTH_USER,
                auth_info_2=AUTH_EMAIL,
                password=AUTH_PASSWORD,
                cookies_file=COOKIES_FILE
            ))
    except Exception as e:
        print(f"Login/session error: {e}")
        return pd.DataFrame()

    try:
        search_results = asyncio.run(client.search_tweet(SEARCH_QUERY, SEARCH_TYPE))
        
        tweets = []
        for count, tweet in enumerate(search_results):
            if count >= SEARCH_LIMIT:
                break
            tweets.append({
                "user": tweet.user.screen_name,
                "name": tweet.user.name,
                "date": tweet.created_at,
                "text": tweet.text
            })
        
        return pd.DataFrame(tweets)
    
    except Exception as e:
        print(f"Search error: {e}")
        return pd.DataFrame()

df = get_tweets()
print(df)
df['text'] = df['text'].str.replace('\n', ' ').str.replace('\r', ' ')
df.to_csv('df.csv', encoding='utf-8', index=False, quoting=csv.QUOTE_ALL)
