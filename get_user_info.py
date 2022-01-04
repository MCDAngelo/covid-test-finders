import pandas as pd
from covid_test_finders.constants import USER_FIELDS, USERS_LIST
from covid_test_finders.user_utils import get_user_info

def main():
    user_info_df = get_user_info(USERS_LIST, USER_FIELDS)
    n_rows = len(user_info_df.index)
    print(f"Retrieved {n_rows} row(s) of data for {len(USERS_LIST)} user(s) in the list.")


if __name__ == '__main__':
    main()
