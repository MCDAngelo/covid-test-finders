import pandas as pd


from covid_test_finders.constants import BASE_URL
from covid_test_finders.utils import retrieve_clean_response

metadata_col = 'public_metrics'


def create_tweet_timeline_url(user_id, max_results=20):
    """
    Creates the url to pull timeline of tweets for user_id
    """
    url = f"{BASE_URL}/users/{user_id}/tweets?max_results={max_results}"
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
    return clean_tweets_df


def get_user_tweets(user_id, max_results):
    """
    Returns a dataframe containing tweets and asscoiated metadata for a user
    """
    timeline_url = create_tweet_timeline_url(user_id, max_results)
    timeline_df = retrieve_clean_response(timeline_url)
    tweet_ids_list = timeline_df['id'].tolist()
    clean_tweets_df = get_clean_tweets(tweet_ids_list, metadata_col)
    return clean_tweets_df
