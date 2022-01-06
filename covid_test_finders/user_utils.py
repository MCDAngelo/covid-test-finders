from covid_test_finders.constants import BASE_URL
from covid_test_finders.utils import retrieve_clean_response


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


def get_user_info(users_list, user_fields):
    """
    Returns user information for a set of users in users_list
    """
    url = create_user_id_url(users_list, user_fields)
    response_df = retrieve_clean_response(url)
    return response_df
