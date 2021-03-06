import os

import pandas as pd
import requests
from dotenv import load_dotenv


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
