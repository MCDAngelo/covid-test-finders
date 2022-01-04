import os
import pandas as pd
import requests
from covid_test_finders.constants import BASE_URL

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

BASE_URL = 'https://api.twitter.com/2'

# def daterange(start_date, end_date, freq):
#     return pd.date_range(start=start_date, end=end_date, freq=freq)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def create_url(user_names_list, user_fields ):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    user_names = ','.join(user_names_list) if len(user_names_list)>1 else user_names_list[0]

    usernames = f"usernames={user_names}"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
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


def get_user_info(users_list, user_fields):
    url = create_url(users_list,user_fields)
    response = connect_to_endpoint(url)
    response_list = response.get('data')
    response_df = pd.DataFrame(response_list)
    return response_df
