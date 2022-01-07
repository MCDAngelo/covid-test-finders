import datetime as dt
import time

import pandas as pd

from covid_test_finders.constants import BASE_URL
from covid_test_finders.utils import retrieve_clean_response


metadata_col = 'public_metrics'
twitter_api_limit_window = 900  # 15 minutes = 900 seconds
timeline_api_limit = 900
tweet_api_limit = 180
timeline_api_limit_wait_time = twitter_api_limit_window/timeline_api_limit
tweet_api_limit_wait_time = twitter_api_limit_window/tweet_api_limit
api_max_results = 100


def create_tweet_timeline_url(
    user_id,
    max_results,
    start_date,
    end_date,
):
    """
    Creates the url to pull timeline of tweets for user_id starting at start_time
    """
    start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.00Z')
    end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.00Z')
    url = (
        f"{BASE_URL}/users/{user_id}/tweets?start_time={start_date}&end_time={end_date}"
        f"&tweet.fields=created_at&max_results={max_results}"
    )
    print(url)
    return url


def create_multiple_tweets_url(tweet_ids_list):
    """
    Returns the url to pull tweet data for tweets in tweet_ids_list
    """
    tweet_ids = ','.join(tweet_ids_list) if len(tweet_ids_list) > 1 else tweet_ids_list[0]
    url = f"{BASE_URL}/tweets?ids={tweet_ids}&tweet.fields=public_metrics,created_at"
    print(url)
    return url


def clean_tweet_metadata(df, metadata_col=metadata_col):
    """
    Unnests metadata contained in json format from a column (metadata_col) and returns
    df with metadata in new columns
    """
    expanded_col = pd.json_normalize(df[metadata_col])
    df = (df.join(expanded_col)
            .drop(columns=metadata_col))
    return df


def get_hashtags(df):
    """
    Returns hashtags contained within column labeled 'text' in a new column labeled 'hashtags'
    """
    df['hashtags'] = df.text.str.findall(r'#.*?(?=\s|$)')
    return df


def get_clean_tweets(tweet_ids_list, metadata_col):
    """
    Returns dataframe containing tweets from list tweet_ids_list with the associated metadata and hashtags
    """
    tweets_url = create_multiple_tweets_url(tweet_ids_list)
    tweets_df = retrieve_clean_response(tweets_url)
    clean_metadata_tweets_df = clean_tweet_metadata(tweets_df)
    clean_tweets_df = get_hashtags(clean_metadata_tweets_df)
    clean_tweets_df = clean_tweets_df.sort_values(by=['id'])
    return clean_tweets_df


def get_user_tweets(user_id, max_results, start_date, end_date):
    """
    Returns a dataframe containing tweets and asscoiated metadata for a user
    """
    clean_tweets_df_list = []
    tweet_ids_list = []
    timeline_request_count = 0
    tweet_request_count = 0
    print(f"initial start_date: {start_date} and end_date: {end_date}")

    # Get timeline of tweets
    while start_date <= dt.datetime.today() + dt.timedelta(days=-1):
        # Wait if you are about to hit api limit
        if timeline_request_count >= (timeline_api_limit - 1):
            print(f"Reached API limit, waiting {timeline_api_limit_wait_time} second before the next attempt.")
            time.sleep(timeline_api_limit_wait_time)
        print(f"run {timeline_request_count} through while loop")
        timeline_url = create_tweet_timeline_url(user_id, max_results, start_date, end_date)
        tmp_timeline_df = retrieve_clean_response(timeline_url)
        tmp_tweet_ids_list = tmp_timeline_df['id'].tolist()
        tweet_ids_list.extend(tmp_tweet_ids_list)
        print(f"{len(tmp_tweet_ids_list)} tweet ids retrieved from timeline")
        # If we previously found tweets, update the start/end dates based on the tweets retrieved
        if len(tmp_tweet_ids_list) > 1:
            print(f"Min & max created_at: {min(tmp_timeline_df.created_at)} - {max(tmp_timeline_df.created_at)}")
            start_date = max(tmp_timeline_df.created_at)
            start_date = dt.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            end_date = start_date + dt.timedelta(days=2)
        # If no tweets were retrieved, slide the start/end dates
        else:
            start_date = end_date
            end_date = start_date + dt.timedelta(days=2)
        print(f"updated start_date: {start_date} and end_date: {end_date}")
        timeline_request_count = timeline_request_count + 1

    # Get tweets with metadata
    tweet_chunks = [tweet_ids_list[x:x+api_max_results] for x in range(0, len(tweet_ids_list), api_max_results)]
    for tweet_ids in tweet_chunks:
        tmp_clean_tweets_df = get_clean_tweets(tweet_ids, metadata_col)
        clean_tweets_df_list.append(tmp_clean_tweets_df)
        tweet_request_count = tweet_request_count + 1
        # Wait if you are about to hit api limit
        if tweet_request_count >= (tweet_api_limit - 1):
            print(f"Reached API limit, waiting {tweet_api_limit_wait_time} second before the next attempt.")
            time.sleep(tweet_api_limit_wait_time)

    clean_tweets_df = pd.concat(clean_tweets_df_list)
    return clean_tweets_df
