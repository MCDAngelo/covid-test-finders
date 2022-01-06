import pathlib
import datetime as dt

from covid_test_finders.constants import USER_FIELDS
from covid_test_finders.constants import USERS_LIST
from covid_test_finders.tweet_utils import get_user_tweets
from covid_test_finders.user_utils import get_user_info


acct_name = 'COVID Test Finders'
acct_id_col = 'id'
max_results = 100
output_directory = './data'
date_str = dt.datetime.today().strftime('%Y%m%d')


def main():
    user_info_df = get_user_info(USERS_LIST, USER_FIELDS)
    mask = user_info_df['name'] == acct_name, acct_id_col
    user_id = user_info_df.loc[mask].values[0]
    mask = user_info_df['name'] == acct_name, 'created_at'
    user_created_date_str = user_info_df.loc[mask].values[0]
    user_created_date = dt.datetime.strptime(user_created_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_date = user_created_date + dt.timedelta(days=2)
    tweets_df = get_user_tweets(user_id, max_results, start_date=user_created_date, end_date=end_date)
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
