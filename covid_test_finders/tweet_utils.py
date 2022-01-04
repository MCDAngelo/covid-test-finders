import os
import pandas as pd
import requests
# from covid_test_finders.constants import BASE_URL
BASE_URL = 'https://api.twitter.com/2'


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


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


user_id = '1441129611144826880'
tweet_timeline_url = get_tweet_timeline_url(user_id, 20)
output = connect_to_endpoint(tweet_timeline_url)
print(output)
# def get_user_info(users_list, user_fields):
#     url = create_url(users_list,user_fields)
#     response = connect_to_endpoint(url)
#     response_list = response.get('data')
#     response_df = pd.DataFrame(response_list)
#     return response_df
