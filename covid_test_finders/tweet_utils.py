import os
import pandas as pd
import requests
from dotenv import load_dotenv
from covid_test_finders.constants import BASE_URL

load_dotenv()
# Set a .env file with your bearer token
# BEARER_TOKEN=<your_bearer_token>
bearer_token = os.getenv("BEARER_TOKEN")



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def get_tweet_timeline_url(user_id, max_results=20):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={max_results}"
    print(url)
    return url


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user_timeline(user_id, max_results):
    url = get_tweet_timeline_url(user_id, max_results)
    response = connect_to_endpoint(url)
    response_list = response.get('data')
    response_df = pd.DataFrame(response_list)
    return response_df
