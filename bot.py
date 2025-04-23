# This code will act as a Twitter bot that fetches recent tweets containing specific hashtags.
# It will use the Twitter API v2 to search for tweets and print their URLs.
# It will also handle rate limits by waiting for the appropriate time before making another request.
# It requires the `requests` library for making HTTP requests and `python-dotenv` for loading environment variables.
# It will also use the `datetime` library to handle time-related operations.
# It will run indefinitely until it successfully fetches tweets or encounters an error.
# It will print the URLs of the tweets in the format "https://twitter.com/{username}/status/{tweet_id}".
# It will also print the error message if the request fails for any reason.
# It will wait for the rate limit to reset if it encounters a 429 status code.
# It will also print the wait time before making another request.
# Make sure you have .env file associated with TWITTER_BEARER_TOKEN It will use the `dotenv` library to load the Twitter Bearer Token from a `.env` file.
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
import time

# --- Load environment ---
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
SEARCH_QUERY = "#XRP OR #Bitcoin -is:retweet lang:en" # CHANGE THIS TO YOUR DESIRED QUERY BY INCLUDING HASHTAGS
# Example: "#XRP OR #Bitcoin -is:retweet lang:en" will search for tweets containing either #XRP or #Bitcoin, excluding retweets, in English.
MAX_RESULTS = 10

def fetch_tweets():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": SEARCH_QUERY,
        "max_results": MAX_RESULTS,
        "tweet.fields": "author_id",
        "expansions": "author_id",
        "user.fields": "username"
    }

    while True:
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            users = {u["id"]: u["username"] for u in data.get("includes", {}).get("users", [])}
            for tweet in data.get("data", []):
                uid = tweet["author_id"]
                username = users.get(uid, "unknown")
                print(f"https://twitter.com/{username}/status/{tweet['id']}")
            break  # Exit after successful run

        elif response.status_code == 429:
            reset = response.headers.get("x-rate-limit-reset")
            wait_time = int(reset) - int(datetime.now(tz=timezone.utc).timestamp()) + 1 if reset else 900
            print(f"Rate limit hit. Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

if __name__ == "__main__":
    if not BEARER_TOKEN:
        print("Missing Twitter Bearer Token in .env!")
    else:
        fetch_tweets()
