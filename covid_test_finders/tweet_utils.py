import os
import pandas as pd
import requests
from dotenv import load_dotenv
from covid_test_finders.constants import BASE_URL
from covid_test_finders.user_utils import retrieve_clean_response

load_dotenv()
# Set a .env file with your bearer token
# BEARER_TOKEN=<your_bearer_token>
bearer_token = os.getenv("BEARER_TOKEN")


def create_tweet_timeline_url(user_id, max_results=20):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={max_results}"
    print(url)
    return url


def create_multiple_tweets_url(tweet_ids_list):
    tweet_ids = ','.join(tweet_ids_list) if len(tweet_ids_list)>1 else tweet_ids_list[0]
    url = f"https://api.twitter.com/2/tweets?ids={tweet_ids}&tweet.fields=public_metrics,created_at"
    print(url)
    return url


def get_user_tweets(user_id, max_results):
    timeline_url = create_tweet_timeline_url(user_id, max_results)
    timeline_df = retrieve_clean_response(timeline_url)
    tweet_ids_list = timeline_df['id'].tolist()
    tweets_url = create_multiple_tweets_url(tweet_ids_list)
    tweets_df = retrieve_clean_response(tweets_url)
    return tweets_df
