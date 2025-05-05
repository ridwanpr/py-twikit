import asyncio
import os
from twikit import Client
from dotenv import load_dotenv

load_dotenv()

SEARCH_QUERY = 'SEARCH_QUERY'
# Type: 'latest','Top'
SEARCH_TYPE = 'Top'

# Credentials
AUTH_USER = os.getenv('AUTH_USER')
AUTH_EMAIL = os.getenv('AUTH_EMAIL')
AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')
COOKIES_FILE = os.getenv('COOKIES_FILE')
LANGUAGE = os.getenv('LANGUAGE')

client = Client(LANGUAGE)

async def main():
    try:
        if os.path.exists(COOKIES_FILE):
            print(f"Attempting to load session from {COOKIES_FILE}...")
            client.load_cookies(COOKIES_FILE)
            print("Session loaded successfully.")
        else:
            print("No existing session. Logging in with credentials...")
            await client.login(
                auth_info_1=AUTH_USER,
                auth_info_2=AUTH_EMAIL,
                password=AUTH_PASSWORD,
                cookies_file=COOKIES_FILE
            )
            print("Login successful. Session saved.")
    except Exception as e:
        print(f"Login or session load failed: {e}")
        return

    try:
        print(f"\nSearching for '{SEARCH_QUERY}' tweets (Type: {SEARCH_TYPE})...")
        search_results = await client.search_tweet(SEARCH_QUERY, SEARCH_TYPE)
        if search_results:
            print(f"Found tweets matching '{SEARCH_QUERY}':")
            count = 0
            max_tweets_to_print = 5

            if hasattr(search_results, '__aiter__'):
                async for tweet in search_results:
                    if count >= max_tweets_to_print:
                        print(f"\n(Stopped printing after {max_tweets_to_print} tweets)")
                        break
                    print(f"\n--- Tweet {count + 1} ---")
                    print(f"User: {tweet.user.name} (@{tweet.user.screen_name})")
                    print(f"Date: {tweet.created_at}")
                    print(f"Text: {tweet.text}")
                    count += 1
            else:
                for tweet in search_results:
                    if count >= max_tweets_to_print:
                        print(f"\n(Stopped printing after {max_tweets_to_print} tweets)")
                        break
                    print(f"\n--- Tweet {count + 1} ---")
                    print(f"User: {tweet.user.name} (@{tweet.user.screen_name})")
                    print(f"Date: {tweet.created_at}")
                    print(f"Text: {tweet.text}")
                    count += 1

            if count == 0:
                print(f"No tweets found for '{SEARCH_QUERY}' with type '{SEARCH_TYPE}'.")
        else:
            print(f"No tweets found for '{SEARCH_QUERY}' with type '{SEARCH_TYPE}'.")
    except Exception as e:
        print(f"An error occurred while searching for tweets: {e}")

if __name__ == "__main__":
    asyncio.run(main())
