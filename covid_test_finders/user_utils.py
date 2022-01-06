import os

import pandas as pd
import requests
from dotenv import load_dotenv

from covid_test_finders.constants import BASE_URL


load_dotenv()
# Set a .env file with your bearer token
# BEARER_TOKEN = <your_bearer_token>
bearer_token = os.getenv("BEARER_TOKEN")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def create_user_id_url(user_names_list, user_fields):
    """
    Returns the url to pull user information (including user id) from usernames contained in user_names_list
    """
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    user_names = ','.join(user_names_list) if len(user_names_list) > 1 else user_names_list[0]

    usernames = f"usernames={user_names}"
    url = f"{BASE_URL}/users/by?{usernames}&{user_fields}"
    print(url)
    return url


def connect_to_endpoint(url):
    """
    Returns response retrieved by url request
    """
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def clean_response(response):
    """
    Converts data object in response from json to dataframe
    """
    response_list = response.get('data')
    response_df = pd.DataFrame(response_list)
    return response_df


def retrieve_clean_response(url):
    """
    Returns dataframe of data object contained in the endpoint response
    """
    response = connect_to_endpoint(url)
    response_df = clean_response(response)
    return response_df


def get_user_info(users_list, user_fields):
    """
    Returns user information for a set of users in users_list
    """
    url = create_user_id_url(users_list, user_fields)
    response_df = retrieve_clean_response(url)
    return response_df
