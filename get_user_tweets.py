from covid_test_finders.constants import USER_FIELDS
from covid_test_finders.constants import USERS_LIST
from covid_test_finders.tweet_utils import get_user_tweets
from covid_test_finders.user_utils import get_user_info


acct_name = 'COVID Test Finders'
acct_id_col = 'id'
max_results = 20


def main():
    user_info_df = get_user_info(USERS_LIST, USER_FIELDS)
    mask = user_info_df['name'] == acct_name, acct_id_col
    user_id = user_info_df.loc[mask].values[0]
    tweets_df = get_user_tweets(user_id, max_results)
    n_rows = len(tweets_df.index)
    print(f"Retrieved {n_rows} tweets.")
    return tweets_df


if __name__ == '__main__':
    output = main()
    print(output)
