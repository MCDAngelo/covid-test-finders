import pathlib

from datetime import datetime as dt

from covid_test_finders.constants import USER_FIELDS
from covid_test_finders.constants import USERS_LIST
from covid_test_finders.tweet_utils import get_user_tweets
from covid_test_finders.user_utils import get_user_info


acct_name = 'COVID Test Finders'
acct_id_col = 'id'
max_results = 100
output_directory = './data'
date_str = dt.today().strftime('%Y%m%d')


def main():
    user_info_df = get_user_info(USERS_LIST, USER_FIELDS)
    mask = user_info_df['name'] == acct_name, acct_id_col
    user_id = user_info_df.loc[mask].values[0]
    tweets_df = get_user_tweets(user_id, max_results)
    n_rows = len(tweets_df.index)
    print(f"Retrieved {n_rows} tweets.")
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)
    output_path = f"{output_directory}/raw_tweets_{date_str}.csv"
    print(f"Saving data to {output_path}")
    tweets_df.to_csv(output_path)
    return tweets_df


if __name__ == '__main__':
    output = main()
    print(output)
