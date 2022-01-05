import pandas as pd
from covid_test_finders.constants import USER_FIELDS, USERS_LIST
from covid_test_finders.tweet_utils import get_user_timeline
from covid_test_finders.user_utils import get_user_info

acct_name = 'COVID Test Finders'
acct_id_col = 'id'
max_results = 20

def main():
    user_info_df = get_user_info(USERS_LIST, USER_FIELDS)
    n_rows = len(user_info_df.index)
    print(f"Retrieved {n_rows} row(s) of data for {len(USERS_LIST)} user(s) in the list.")
    user_id = user_info_df.loc[user_info_df['name'] == acct_name, acct_id_col].values[0]
    tweet_timeline_df = get_user_timeline(user_id, max_results)
    return user_info_df


if __name__ == '__main__':
    output = main()
    print(output)
